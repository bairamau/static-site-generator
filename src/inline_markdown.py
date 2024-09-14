import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception('did not find a closing delimiter')
            new_nodes.extend([TextNode(text, TextType.TEXT if idx % 2 == 0 else text_type) for idx, text in enumerate(parts) if text])
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"(!\[(.+?)\]\((.+?)\))", text)

def extract_markdown_links(text):
    return re.findall(r"(\[(.+?)\]\((.+?)\))", text)

# instead of else keyword in a loop we can use early continue, similar to early return
def split_nodes_media(old_nodes, text_type, extractor):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        matches = extractor(original_text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue

        for match in matches:
            parts = original_text.split(match[0], 1)
            if len(parts) != 2:
                raise ValueError("Invalid markdown")
            if len(parts[0]) > 0:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(match[1], text_type, match[2]))

            original_text = parts[1]
        if len(original_text) > 0:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
                    
    return new_nodes

def split_nodes_image(old_nodes):
    return split_nodes_media(old_nodes, TextType.IMAGE, extract_markdown_images)

def split_nodes_link(old_nodes):
    return split_nodes_media(old_nodes, TextType.LINK, extract_markdown_links)

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    bold_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes, '*', TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes, '`', TextType.CODE)
    image_nodes = split_nodes_image(code_nodes)
    final_nodes = split_nodes_link(image_nodes)
    return final_nodes
