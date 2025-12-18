import re
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python replace_links.py <file.md>")
    sys.exit(1)

path = Path(sys.argv[1])

# Lecture du fichier
text = path.read_text(encoding="utf-8")

# Remplacement des <URL> par [🔗](URL)
text = re.sub(r"<(https?://[^>]+)>.", r"[🔗](\1)", text)

# Réécriture du même fichier
path.write_text(text, encoding="utf-8")

print(f"✅ Liens remplacés dans {path}")

