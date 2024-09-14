import unittest

from block_markdown import BlockType, markdown_to_blocks, block_to_block_type

class BlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
       blocks = markdown_to_blocks('''# This is a heading



                       
                                

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
'''
                                   )
       self.assertEqual(blocks, 
                         ['# This is a heading', 
                          'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
                          '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
                         )


    def test_block_to_block_heading(self):
        self.assertEqual(block_to_block_type('# heading'), BlockType.HEADING)
        self.assertEqual(block_to_block_type('## heading'), BlockType.HEADING)
        self.assertEqual(block_to_block_type('### heading'), BlockType.HEADING)
        self.assertEqual(block_to_block_type('#### heading'), BlockType.HEADING)
        self.assertEqual(block_to_block_type('##### heading'), BlockType.HEADING)
        self.assertEqual(block_to_block_type('###### heading'), BlockType.HEADING)
        self.assertEqual(block_to_block_type('# '), BlockType.HEADING)
        self.assertEqual(block_to_block_type('# \nnew line'), BlockType.HEADING)
 
 
        self.assertEqual(block_to_block_type('#heading'), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type('###'), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(' # heading'), BlockType.PARAGRAPH)

    def test_block_to_block_code(self):
        self.assertEqual(block_to_block_type('```some code```'), BlockType.CODE)
        self.assertEqual(block_to_block_type('```\nsome\nelaborate\npiece\nof code```'), BlockType.CODE)
        self.assertEqual(block_to_block_type('``````'), BlockType.CODE)

        self.assertEqual(block_to_block_type('```some code``'), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type('`some code`'), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type('\nsome\n```elaborate\npiece```\nof code'), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type('```code'), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type('\nsome\n```elaborate\npiece```\nof code'), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type('\nsome\n```elaborate\npiece```\nof code'), BlockType.PARAGRAPH)

    def test_block_to_block_quote(self):
        self.assertEqual(block_to_block_type('> chiken'), BlockType.QUOTE)
        self.assertEqual(block_to_block_type('> chiken\n> wing'), BlockType.QUOTE)
        self.assertEqual(block_to_block_type('> >chiken'), BlockType.QUOTE)
        self.assertEqual(block_to_block_type('> An\n> Inspirational\n> Quote'), BlockType.QUOTE)

    def test_block_to_block_ul(self):
        self.assertEqual(block_to_block_type('* chiken'), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type('- chiken'), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type('* chiken\n* wing'), BlockType.UNORDERED_LIST)
        
        self.assertEqual(block_to_block_type('*chiken\n* wing\n* swing'), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type('* chiken\n*wing\n* swing'), BlockType.PARAGRAPH)
    
    def test_block_to_block_ol(self):       
        self.assertEqual(block_to_block_type('1. one'), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type('1. one\n2. two\n3. three'), BlockType.ORDERED_LIST)
        
        self.assertEqual(block_to_block_type('2. two'), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type('1. one\n3. three'), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type('1.one'), BlockType.PARAGRAPH)

    def test_block_to_block_paragraph(self):  
        self.assertEqual(block_to_block_type('anything at all'), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type('. a dot for a change'), BlockType.PARAGRAPH)
