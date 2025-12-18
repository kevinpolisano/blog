import xml.etree.ElementTree as ET
import csv
from datetime import datetime

# Chemin vers le fichier XML exporté
xml_file = "wp.xml"
output_file = "comments.csv"

# Charger le fichier XML
tree = ET.parse(xml_file)
root = tree.getroot()

# Namespace de WordPress
ns = {"wp": "http://wordpress.org/export/1.2/"}

# Extraire les commentaires
comments = []
for item in root.findall(".//item"):
    post_title = item.find("title").text
    post_url = item.find("link").text
    for comment in item.findall("wp:comment", ns):
        author = comment.find("wp:comment_author", ns).text
        content = comment.find("wp:comment_content", ns).text
        date = comment.find("wp:comment_date", ns).text
        comments.append([post_title, post_url, author, content, date])

# Trier les commentaires par date croissante
comments.sort(key=lambda x: datetime.strptime(x[4], "%Y-%m-%d %H:%M:%S"))

# Écrire dans un fichier CSV
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter='$')
    writer.writerow(["Post Title", "Post URL", "Author", "Comment", "Date"])
    writer.writerows(comments)

print(f"Commentaires exportés dans {output_file}")


