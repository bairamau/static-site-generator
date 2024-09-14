import unittest

from parser import markdown_to_html_node

class TestParser(unittest.TestCase):
    def test_markdown_to_html_node(self):
        md = 'A beautiful day'
        self.assertEqual(markdown_to_html_node(md).to_html(), '<div><p>A beautiful day</p></div>')

        md = '''# A beautiful day.

        Indeed it is.
        '''
        self.assertEqual(markdown_to_html_node(md).to_html(), '<div><h1>A beautiful day.</h1><p>Indeed it is.</p></div>')

        md = '''###### A beautiful day.

        Indeed it is.
        '''
        self.assertEqual(markdown_to_html_node(md).to_html(), '<div><h6>A beautiful day.</h6><p>Indeed it is.</p></div>')       
        
        md = '''```f(x) = x^3 + C```'''
        self.assertEqual(markdown_to_html_node(md).to_html(), '<div><code>f(x) = x^3 + C</code></div>')

        md = '''> An
> inspirational
> quote
'''
        self.assertEqual(markdown_to_html_node(md).to_html(), '<div><blockquote>An inspirational quote</blockquote></div>')

        md = '''* An
- Unordered
* List
'''
        self.assertEqual(markdown_to_html_node(md).to_html(), '<div><ul><li>An</li><li>Unordered</li><li>List</li></ul></div>')

        md = '''1. An
2. Ordered
3. List
'''
        self.assertEqual(markdown_to_html_node(md).to_html(), '<div><ol><li>An</li><li>Ordered</li><li>List</li></ol></div>')

        md = '''
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

'''
        self.assertEqual(markdown_to_html_node(md).to_html(), '<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>')
        
