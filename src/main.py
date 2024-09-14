import os
import shutil
import re
from parser import markdown_to_html_node
def refresh_static_files():
    if os.path.exists('public'):
        shutil.rmtree('public')

    def move(fromDir, toDir):
        dir = os.listdir(fromDir)
        for item in dir:
            if os.path.isfile(f"{fromDir}/{item}"):
                if not os.path.exists(toDir):
                    os.mkdir(toDir)
                shutil.copy(f"{fromDir}/{item}", f"{toDir}/{item}")
            else:
                move(f"{fromDir}/{item}", f"{toDir}/{item}")

    move('static', 'public')


def extract_title(markdown):
    first_block = markdown.split("\n\n")[0]
    if not first_block.startswith("# "):
        raise Exception("Should have a title")
    title = first_block[2:]
    
    return title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    md = open(from_path).read()
    template = open(template_path).read()

    title = extract_title(md)
    html_string = markdown_to_html_node(md).to_html()
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    open(dest_path, 'w').write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
        dir = os.listdir(dir_path_content)
        for entry in dir:
            if os.path.isfile(f"{dir_path_content}/{entry}"):
                name = entry.split(".")[0]
                generate_page(f"{dir_path_content}/{entry}", "template.html", f"{dest_dir_path}/{name}.html")
            else:
                generate_pages_recursive(f"{dir_path_content}/{entry}", "template.html", f"{dest_dir_path}/{entry}")


def main():
    refresh_static_files()
    generate_pages_recursive("content", "template.html", "public")

main()
