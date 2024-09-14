from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
import re
def markdown_block_to_html_node(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            tag = 'p'
            text = " ".join(block.split("\n"))
        case BlockType.CODE:
            tag = 'code'
            match = re.fullmatch(r'^```(.*)```$', block, re.DOTALL)
            text = match.group(1)
        case BlockType.QUOTE:
            tag = 'blockquote'
            text = block
        case BlockType.UNORDERED_LIST:
            tag = 'ul'
            text = block
        case BlockType.ORDERED_LIST:
            tag = 'ol'
            text = block
        case BlockType.HEADING:
           match = re.fullmatch(r'^(#{1,6}) (.*)$', block, re.DOTALL)
           tag = f'h{len(match.group(1))}'
           text = match.group(2)
        case _: raise Exception('unsupported block type')
    return ParentNode(tag=tag, children=text_to_children(text, block_type))


def text_to_children(text, block_type):
    match block_type:
        case BlockType.QUOTE:
            lines = text.splitlines()
            text = " ".join([re.fullmatch(r'^> (.*)$', line).group(1) for line in lines])
            return [text_node_to_html_node(text_node) for text_node in text_to_textnodes(text)]

        case BlockType.UNORDERED_LIST:
            lines = text.splitlines()
            textnode_lines = [text_to_textnodes(re.fullmatch(r'^[\*\-] (.*)$', line).group(1)) for line in lines]
            list_nodes = [ParentNode(tag='li', children=[text_node_to_html_node(node) for node in line]) for line in textnode_lines]
            return list_nodes

        case BlockType.ORDERED_LIST:
            lines = text.splitlines()
            textnode_lines = [text_to_textnodes(re.fullmatch(r'^\d\. (.*$)', line).group(1)) for line in lines]
            list_nodes = [ParentNode(tag='li', children=[text_node_to_html_node(node) for node in line]) for line in textnode_lines]
            return list_nodes

    return [text_node_to_html_node(text_node) for text_node in text_to_textnodes(text)]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = markdown_block_to_html_node(block, block_type)
        html_nodes.append(html_node)
    return ParentNode(tag='div', children=html_nodes)
