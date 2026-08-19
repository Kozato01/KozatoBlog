import re
from datetime import datetime
from pathlib import Path

import markdown

MESES = ("jan", "fev", "mar", "abr", "mai", "jun",
         "jul", "ago", "set", "out", "nov", "dez")

# A ordem daqui é a ordem dos chips no site. Mora aqui e não no app.py porque
# quem lê o front matter é este módulo — é aqui que dá pra corrigir a grafia.
CATEGORIAS = ("Posts", "Projeto", "Python", "Data", "IA", "Delírio")

# "posts", "POSTS" e "Posts" são a mesma coisa. Sem isso, escrever a categoria
# em minúscula no front matter fazia o post sumir de todos os filtros calado.
_CANONICA = {c.casefold(): c for c in CATEGORIAS}


def categoria_valida(bruta):
    """Devolve a categoria canônica. Grafia que não existe cai em Delírio."""
    return _CANONICA.get((bruta or "").strip().casefold(), "Delírio")


def data_curta(iso):
    """2026-08-19 -> 19 ago 2026. Data torta volta como veio."""
    try:
        d = datetime.strptime(iso, "%Y-%m-%d")
    except ValueError:
        return iso
    return f"{d.day} {MESES[d.month - 1]} {d.year}"

def parse_post(file_path):
    """Parse markdown file with YAML front matter.

    Returns: {title, date (str), category, tags, preview, content, slug, filename}
    """
    text = file_path.read_text(encoding="utf-8")

    # Extract front matter
    fm_match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not fm_match:
        return None

    fm_text, body = fm_match.groups()
    fm = {}
    for line in fm_text.split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            k, v = k.strip(), v.strip()
            if k == 'tags':
                fm[k] = [t.strip() for t in v.strip('[]').split(',')]
            else:
                fm[k] = v

    # Extract slug from filename (YYYY-MM-DD-slug.md)
    slug = file_path.stem.split('-', 3)[-1] if len(file_path.stem.split('-')) > 3 else file_path.stem

    # Generate preview if not provided
    preview = fm.get('preview', '')
    if not preview:
        # First 150 chars of body
        preview = re.sub(r'\[.*?\]\(.*?\)', '', body)[:150].strip() + '...'

    return {
        'title': fm.get('title', 'Sem título'),
        'date': fm.get('date', ''),
        'date_display': data_curta(fm.get('date', '')),
        'category': categoria_valida(fm.get('category')),
        'tags': fm.get('tags', []),
        'preview': preview,
        'content': markdown.markdown(body, extensions=['extra', 'sane_lists']),
        'slug': slug,
        'filename': file_path.name,
    }

def load_posts_from_disk():
    """Scan content/posts/ and return sorted list of parsed posts."""
    posts_dir = Path(__file__).parent.parent / 'content' / 'posts'
    posts = []

    if not posts_dir.exists():
        return posts

    for md_file in sorted(posts_dir.glob('*.md'), reverse=True):
        post = parse_post(md_file)
        if post:
            posts.append(post)

    return posts
