#!/usr/bin/env python3
# postprocess_biblio_links.py
# Replace visible URL text by "🔗" only inside bibliography / margin entries

from bs4 import BeautifulSoup
from pathlib import Path
import sys

# chemin vers le fichier HTML à modifier — adapte si nécessaire
# exemple : site statique dans docs/ (Quarto)
default_paths = [
    "docs/posts/2025-10-27-le-jeu-de-taquin/index.html",
    "_site/index.html",
    "index.html"
]

def find_html_files():
    # si l'utilisateur passe un chemin en argument, on l'utilise
    if len(sys.argv) > 1:
        p = Path(sys.argv[1])
        return [p] if p.exists() else []
    # sinon cherche aux emplacements probables
    out = [p for p in (Path(x) for x in default_paths) if p.exists()]
    # aussi tous les fichiers docs/**/*.html
    out += list(Path("docs").rglob("*.html")) if Path("docs").exists() else []
    return out

def process_file(path: Path):
    html = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    changed = False

    # 1) cibles : div.csl-entry (entrées bibliographiques) et divs dans column-margin container
    selectors = [
        "div.csl-entry a",                 # ancre directement dans entrée bibliographique
        "div.column-margin a",             # lien dans bloc de marge
        "div.column-container a",
        "div.column-margin div.csl-entry a"
    ]

    for sel in selectors:
        for a in soup.select(sel):
            href = a.get("href", "")
            if href and href.startswith("http"):
                # si le texte visible est déjà l'URL ou contient l'URL -> remplacer
                txt = (a.get_text() or "").strip()
                if txt == href or href in txt or txt.startswith("http"):
                    a.string = "🔗"
                    changed = True
                else:
                    # pour être sûr, on remplace seulement si l'URL apparaît littéralement
                    # (ne touche pas aux textes personnalisés)
                    pass

    if changed:
        path.write_text(str(soup), encoding="utf-8")
        print(f"[OK] modifié : {path}")
    else:
        print(f"[SKIP] rien à faire dans : {path}")

if __name__ == "__main__":
    files = find_html_files()
    if not files:
        print("Aucun fichier HTML trouvé. Passe le chemin du fichier HTML en argument.")
        sys.exit(1)
    for f in files:
        process_file(Path(f))

