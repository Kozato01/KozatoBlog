import re
from pathlib import Path

import app
from utils.markdown import data_curta, parse_post

EXEMPLO = """---
title: Construindo meu servidor Debian
date: 2026-08-19
category: Projeto
tags: [Linux, Docker, Homelab]
---

Comecou quando decidi controlar meu proprio hardware.
"""


def test_parse_post(tmp_path):
    arquivo = tmp_path / "2026-08-19-servidor-debian.md"
    arquivo.write_text(EXEMPLO, encoding="utf-8")

    post = parse_post(arquivo)

    assert post["title"] == "Construindo meu servidor Debian"
    assert post["date"] == "2026-08-19"
    assert post["date_display"] == "19 ago 2026"
    assert post["category"] == "Projeto"
    assert post["tags"] == ["Linux", "Docker", "Homelab"]
    assert post["slug"] == "servidor-debian"
    assert "<p>" in post["content"]
    # sem preview no front matter, sai das primeiras linhas do corpo
    assert post["preview"].startswith("Comecou quando")


def test_parse_post_sem_front_matter(tmp_path):
    arquivo = tmp_path / "2026-01-01-solto.md"
    arquivo.write_text("so o corpo, sem front matter", encoding="utf-8")

    assert parse_post(arquivo) is None


def test_data_curta_aceita_data_torta():
    assert data_curta("2018-03-14") == "14 mar 2018"
    assert data_curta("ontem") == "ontem"


def test_lista_traz_todos_os_posts_do_disco():
    no_disco = len(list(Path("content/posts").glob("*.md")))
    corpo = app.app.test_client().get("/api/posts").get_json()

    assert corpo["total"] == no_disco
    assert len(corpo["posts"]) == no_disco
    # mais novo primeiro
    datas = [p["date"] for p in corpo["posts"]]
    assert datas == sorted(datas, reverse=True)


def test_filtro_por_categoria():
    cliente = app.app.test_client()
    todos = cliente.get("/api/posts").get_json()
    alvo = todos["posts"][0]["category"]

    filtrado = cliente.get(f"/api/posts?category={alvo}").get_json()

    assert filtrado["posts"], "a categoria do primeiro post nao devolveu nada"
    assert all(p["category"] == alvo for p in filtrado["posts"])
    # total continua sendo o do acervo, nao o do filtro
    assert filtrado["total"] == todos["total"]


def test_categoria_inexistente_devolve_vazio():
    corpo = app.app.test_client().get("/api/posts?category=Xadrez").get_json()
    assert corpo["posts"] == []


def test_feed_rss():
    resposta = app.app.test_client().get("/feed.xml")
    xml = resposta.get_data(as_text=True)

    assert resposta.status_code == 200
    assert resposta.mimetype == "application/rss+xml"

    # o catch-all /<slug> nao pode ter engolido a rota
    assert xml.startswith("<?xml")

    posts = app.load_posts_from_disk()
    assert xml.count("<item>") == len(posts)

    primeiro = posts[0]
    assert f"{app.SITE}/posts/{primeiro['slug']}" in xml
    # pubDate em RFC 822: "Wed, 19 Aug 2026 00:00:00 -0300"
    assert re.search(r"<pubDate>\w{3}, \d{2} \w{3} \d{4} .+? [-+]\d{4}</pubDate>", xml)
    # o HTML do post vai escapado, nao cru, senao o XML quebra
    assert "<description>&lt;p&gt;" in xml


def test_rotas_do_cliente_respondem_200():
    cliente = app.app.test_client()
    for caminho in ("/", "/sobre", "/projetos", "/posts/servidor-debian"):
        assert cliente.get(caminho).status_code == 200, caminho

    assert cliente.get("/nao-existe").status_code == 404
