import re

class BlockType:
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def markdown_to_blocks(text):
    blocks = [stripped for b in text.split('\n\n') if len(stripped := b.strip('\n ')) > 0]
    return blocks

def block_to_block_type(block_text):
    if re.fullmatch(r'^#{1,6} .*$', block_text, re.DOTALL):
        return BlockType.HEADING
    if re.fullmatch(r'^```.*```$', block_text, re.DOTALL):
        return BlockType.CODE
    lines = block_text.splitlines()
    if all([re.fullmatch(r'^> .*$', line) for line in lines]):
        return BlockType.QUOTE
    if all([re.fullmatch(r'^[\*\-] .*$', line) for line in lines]):
        return BlockType.UNORDERED_LIST
    if all([re.fullmatch(rf'^{idx}\. .*$', line) for idx, line in enumerate(lines, 1)]):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
    
