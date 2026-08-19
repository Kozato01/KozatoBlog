import os
import sys
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

import markdown
from flask import (Flask, Response, abort, jsonify, redirect, render_template,
                   request, send_file)

from utils.markdown import CATEGORIAS, load_posts_from_disk

BASE_DIR = Path(__file__).resolve().parent
CONTENT_DIR = BASE_DIR / "content"

# Serve APENAS o que é público. O static_folder é assets/ e nada mais:
# apontar para a raiz exporia .env, requirements.txt e o currículo em PDF.
app = Flask(__name__, static_folder="assets", static_url_path="/assets")

# As páginas markdown do Treino-UP; o arquivo é content/<slug>.md
PAGINAS_MD = ("privacidade", "exclusao-conta", "patch-notes")

# Rotas que o index.html resolve sozinho no cliente
SPA = ("sobre", "projetos")

# Endereço público do site: toda página tem que terminar aqui, e não num
# subdomínio herdado.
SITE = "https://kozato.app.br"

# O front matter só tem a data, sem hora. Meia-noite em Brasília é o suficiente
# para o leitor de feed ordenar; o que não pode é sair sem fuso nenhum.
FUSO = timezone(timedelta(hours=-3))


# ===== POSTS =====
@app.get("/api/posts")
def listar_posts():
    # relido a cada acesso, como as páginas markdown: publicar é copiar o
    # arquivo, sem reiniciar o processo
    # ponytail: reparse por request; cachear por mtime se passar de ~100 posts
    todos = load_posts_from_disk()
    categoria = request.args.get("category", "").strip()
    selecionados = (
        todos if categoria in ("", "todos")
        else [p for p in todos if p.get("category") == categoria]
    )
    return jsonify(posts=selecionados, categories=list(CATEGORIAS), total=len(todos))


# ===== FEED =====
@app.get("/feed.xml")
def feed():
    # A regra estática ganha do catch-all /<slug> na resolução do Flask, então
    # /feed.xml chega aqui e não no 404 das páginas markdown.
    def rfc822(iso):
        # data em RFC 822 escrita na mão erra fuso e nome de mês em locale
        # não-inglês; format_datetime é stdlib e acerta os dois
        try:
            return format_datetime(
                datetime.strptime(iso, "%Y-%m-%d").replace(tzinfo=FUSO))
        except ValueError:
            return ""

    itens = "".join(f"""
    <item>
      <title>{escape(p["title"])}</title>
      <link>{SITE}/posts/{p["slug"]}</link>
      <guid isPermaLink="true">{SITE}/posts/{p["slug"]}</guid>
      <category>{escape(p["category"])}</category>
      <pubDate>{rfc822(p["date"])}</pubDate>
      <description>{escape(p["content"])}</description>
    </item>""" for p in load_posts_from_disk())

    # o HTML do post vai escapado no description em vez de CDATA: post que
    # contenha "]]>" quebraria o bloco, e todo leitor entende escapado
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Wylliams Diogo</title>
    <link>{SITE}</link>
    <description>Engenharia de dados, IA, Python e projetos que dão errado antes de dar certo.</description>
    <language>pt-BR</language>
    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>{itens}
  </channel>
</rss>
"""
    return Response(xml, mimetype="application/rss+xml")


@app.get("/api/health")
def health():
    return jsonify(status="ok", posts=len(load_posts_from_disk()))


# ===== PÁGINAS =====
@app.before_request
def dominio_canonico():
    # privacidade.kozato.app.br tinha um servidor só dele (o privacy-server.js
    # na porta 3333) e continua chegando aqui pelo túnel. Tudo que entra por
    # ele volta para o site principal — a raiz cai na política de privacidade,
    # que é a URL registrada no Play Console.
    if request.host.split(":")[0].startswith("privacidade."):
        caminho = "/privacidade" if request.path == "/" else request.path
        return redirect(SITE + caminho)


@app.get("/")
def inicio():
    return send_file(BASE_DIR / "index.html")


@app.get("/posts/<slug>")
def post(slug):
    return send_file(BASE_DIR / "index.html")


@app.get("/<slug>")
def pagina_markdown(slug):
    if slug in SPA:
        return send_file(BASE_DIR / "index.html")

    if slug not in PAGINAS_MD:
        abort(404)

    # lido a cada acesso de propósito: editar o .md e recarregar a página basta,
    # sem reiniciar o servidor
    fonte = (CONTENT_DIR / f"{slug}.md").read_text(encoding="utf-8")

    return render_template(
        "pagina.html",
        slug=slug,
        titulo=fonte.partition("\n")[0].lstrip("# ").strip(),  # o `# ` do topo
        conteudo=markdown.markdown(fonte, extensions=["extra", "sane_lists"]),
    )


@app.errorhandler(404)
def nao_encontrado(_erro):
    return send_file(BASE_DIR / "index.html"), 404


if __name__ == "__main__":
    # o console do Windows abre em cp1252 e engasga com os emojis do banner
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    porta = int(os.environ.get("PORT", 8080))
    print(f"🎮 Kozato World rodando em http://localhost:{porta}")
    print(f"   {len(load_posts_from_disk())} posts em content/posts/")
    app.run(host="0.0.0.0", port=porta)
