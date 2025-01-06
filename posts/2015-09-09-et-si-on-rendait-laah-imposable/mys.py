import re
import os
import shutil

# Dossiers source et destination pour les images
UPLOADS_DIR = "../uploads"
IMAGES_DIR = "images"
INPUT_FILE = "index_prev.qmd"
OUTPUT_FILE = "index.qmd"

# Créer le dossier images s'il n'existe pas
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# Lire le fichier d'entrée
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    input_text = file.read()


def transform_links_and_footnotes(input_text):
    # Transformation des liens
    def transform_links(match):
        image_path = match.group(1)
        # Suppression des dimensions s'il y en a
        image_path = re.sub(r'-\d+x\d+(?=\.\w+)', '', image_path)
        # Extraction du chemin de l'image
        local_path = re.search(r"images/.*", image_path)
        filename = os.path.basename(image_path)

         # Copier l'image
        src_path = os.path.join(UPLOADS_DIR, filename)
        dest_path = os.path.join(IMAGES_DIR, filename)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
        return f"![]({local_path.group(0)})" if local_path else f"![]({image_path})"

    transformed_text = re.sub(r"\[!\[.*?\]\((.*?)\)\]\((.*?)\)", transform_links, input_text)

    # Transformation des footnotes
    footnote_counter = 1
    footnotes = []

    def replace_footnotes(match):
        nonlocal footnote_counter
        content = match.group(1).strip()
        # S'assurer que les parenthèses sont correctement fermées
        if content.count("(") > content.count(")"):
            content += ")"
        footnote = f"[^{footnote_counter}]"
        footnotes.append(f"{footnote}: {content}")
        footnote_counter += 1
        return footnote

    transformed_text = re.sub(r"\(\((.*?)\)\)", replace_footnotes, transformed_text)

    # Ajout des footnotes en bas
    if footnotes:
        transformed_text += "\n\n" + "\n".join(footnotes)

    # Suppression des parenthèses superflues dans les footnotes
    transformed_text = re.sub(r"\[\^(\d+)\]\)", r"[^\1]", transformed_text)

    return transformed_text


# Transformation
output_text = transform_links_and_footnotes(input_text)

# Écriture dans le fichier de sortie
with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
    file.write(output_text)