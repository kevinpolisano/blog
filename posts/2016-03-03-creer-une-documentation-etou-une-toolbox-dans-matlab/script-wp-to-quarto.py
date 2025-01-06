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
    content = file.read()

# Fonction pour traiter les images
def process_images(content):
    image_pattern = re.compile(
        r'<a [^>]*?href="[^"]*?/([^/"]+)"[^>]*?><img [^>]*?src="[^"]*?/([^/"]+)"[^>]*?></a>'
    )
    
    def replace_image(match):
        image_file = match.group(1)
        base_name, ext = os.path.splitext(image_file)
        
        # Vérifier si le nom contient les dimensions WxH
        dimension_pattern = re.compile(r"^(?P<name>.+)-\d+x\d+$")
        dimension_match = dimension_pattern.match(base_name)
        
        if dimension_match:
            base_name = dimension_match.group("name")  # Nom sans dimensions
            original_image_file = base_name + ext
            original_path = os.path.join(UPLOADS_DIR, original_image_file)
            
            # Si l'image sans dimensions existe, utiliser celle-ci
            if os.path.exists(original_path):
                image_file = original_image_file
        
        # Copier l'image
        src_path = os.path.join(UPLOADS_DIR, image_file)
        dest_path = os.path.join(IMAGES_DIR, image_file)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
        
        return f"![](images/{image_file})"
    
    return image_pattern.sub(replace_image, content)

# Fonction pour traiter les blocs de code
def process_code_blocks(content):
    code_block_pattern = re.compile(
        r'<pre class="brush:[^"]+">(.*?)</pre>', re.DOTALL
    )
    
    def replace_code_block(match):
        code_content = match.group(1).replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")
        return f"```matlab\n{code_content}\n```"
    
    return code_block_pattern.sub(replace_code_block, content)

# Fonction pour traiter les footnotes
def process_footnotes(content):
    footnote_body_pattern = re.compile(
        r'<sup id="(?P<id>[^"]+)"><a href="#[^"]+" title="(?P<title>[^"]+)"[^>]*>\d+</a></sup>'
    )
    
    def replace_footnote_body(match):
        footnote_id = match.group("id")
        footnote_content = match.group("title").replace("&#039;", "'").replace("&quot;", '"')
        markdown_footnote = f"[^{footnote_id}]"
        markdown_definition = f"[^{footnote_id}]: {footnote_content}"
        return markdown_footnote, markdown_definition
    
    paragraphs = content.split("\n\n")  # Diviser en paragraphes
    updated_paragraphs = []
    
    for paragraph in paragraphs:
        matches = list(footnote_body_pattern.finditer(paragraph))
        if matches:
            definitions = []
            for match in matches:
                footnote_markdown, footnote_definition = replace_footnote_body(match)
                paragraph = paragraph.replace(match.group(0), footnote_markdown)
                definitions.append(footnote_definition)
            updated_paragraphs.append(paragraph)
            updated_paragraphs.extend(definitions)
        else:
            updated_paragraphs.append(paragraph)
    
    return "\n\n".join(updated_paragraphs)

# Fonction pour supprimer les balises <li id=X>
def remove_list_items(content):
    list_item_pattern = re.compile(r'<li id="[^"]+">.*?</li>', re.DOTALL)
    return list_item_pattern.sub("", content)

# Fonction pour supprimer l’indentation des balises de paragraphes
def remove_paragraph_indentation(content):
    paragraph_pattern = re.compile(r"\s*<(/?p)>")
    return paragraph_pattern.sub(r"<\1>", content)

# Appliquer les transformations
content = process_images(content)
content = process_code_blocks(content)
content = process_footnotes(content)
content = remove_list_items(content)
content = remove_paragraph_indentation(content)

# Écrire le fichier de sortie
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write(content)

print(f"Transformation terminée. Résultat enregistré dans {OUTPUT_FILE}.")
