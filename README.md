# Kozato World

Meu blog. Um arquivo HTML e um Flask rodando num Debian que mora na minha sala.

Sem bundler, sem framework de front, sem build step, sem gerador estático. Antes eu passava mais tempo escolhendo ferramenta do que escrevendo, então tirei todas.

No ar em <https://kozato.app.br>.

Tem também as páginas de privacidade e exclusão de conta do Treino-UP aqui dentro, porque o Google exigiu e eu não ia subir um site inteiro só pra isso.

## Escrever um post

Cria um arquivo em `content/posts/`. É isso.

```markdown
---
title: Construindo meu servidor Debian
date: 2026-08-19
category: Projeto
tags: [linux, docker, homelab]
preview: A linha que aparece na home. Se faltar, ele rouba as primeiras do texto.
---

E aí escreve.
```

O nome do arquivo vira a URL: `2026-08-19-servidor-debian.md` abre em `/posts/servidor-debian`.

Categoria tem que ser uma destas: `Posts`, `Projeto`, `Python`, `Data`, `IA`, `Delírio`. Maiúscula não importa, `posts` e `Posts` dão na mesma. Se você inventar uma que não existe, o post cai em `Delírio`, o que costuma ser justo.

Imagem vai em `assets/images/` e o caminho **começa com barra**:

```markdown
![Legenda](/assets/images/foto.webp)
```

Sem a barra ele vai procurar dentro de `/posts/` e não achar nada.

O site relê os markdown a cada acesso. Não tem rebuild, não tem restart, não tem botão de publicar. O arquivo existir no servidor já é a publicação.

## Rodar

```bash
pip install -r requirements.txt
python app.py
```

Abre em <http://localhost:8080>. Os testes são `python -m pytest`.

Com Docker:

```bash
docker compose up -d --build
```

Escuta na 3000 dentro do container, publicado na 8080 do host. O túnel do Cloudflare resolve o resto.

## Tem RSS

`/feed.xml`. Porque estamos em 2026 e eu ainda acho um negocio gostoso.

## Onde mora o quê

`index.html` é o site inteiro, CSS e JS lá dentro. `app.py` é o Flask. `utils/markdown.py` lê os posts. `content/posts/` são os posts. O resto é Docker e imagem.

Não existe rota que escreve nada. Nem post, nem comentário, nem recado. Já teve guestbook e contador de visitas, mas isso é assunto pra um post, não pra um README.

## Licença

MIT. Feito por Wylliams Diogo.
