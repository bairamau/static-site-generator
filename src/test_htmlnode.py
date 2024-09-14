import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_basic(self):
        node = HTMLNode('p', 'a paragraph\'s content', [HTMLNode(value="raw text")], { 'title': 'some title' })
        self.assertEqual(node.tag, 'p')
        self.assertEqual(node.value, 'a paragraph\'s content')
        self.assertEqual(isinstance(node.children[0], HTMLNode), True)
        self.assertEqual(node.props['title'], 'some title')

    def test_props_to_html(self):
        node = HTMLNode('button', 'open', None, { 'title': 'open' })
        self.assertEqual(node.props_to_html(), ' title="open"')

    def test_none(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_leaf_value(self):
        self.assertRaises(ValueError, LeafNode, None, None)

    def test_leaf_text(self):
        node = LeafNode(None, "Au revoir!", {'class': 'texl-lg'})
        self.assertEqual(node.to_html(), "Au revoir!")

    def test_leaf_tag(self):
        node = LeafNode("p", "Je ne parle pas Francais", { "class": "leading-6 text-xl", "title": "french text"})
        self.assertEqual(node.to_html(), '<p class="leading-6 text-xl" title="french text">Je ne parle pas Francais</p>')

    def test_parent_constraints(self):
        self.assertRaises(TypeError, ParentNode)
        self.assertRaises(ValueError, ParentNode, None, 'value')
        self.assertRaises(ValueError, ParentNode, 'main', None)
        self.assertRaises(ValueError, ParentNode, 'main', [])

    def test_children(self):
        node = ParentNode('main', 
                          [LeafNode('h1', 'Totally legit heading'), 
                           ParentNode('section',[LeafNode('h2', 'Subheading', {"class": "my-6 text-lg"}), LeafNode('p', 'bla bla bla')]),
                           LeafNode(None, 'just hanging around there')],
                          {'class':"grid columns-auto"})
        self.assertEqual(node.to_html(),
                          f'<main class="grid columns-auto"><h1>Totally legit heading</h1><section><h2 class="my-6 text-lg">Subheading</h2><p>bla bla bla</p></section>just hanging around there</main>')

if __name__ == "__main__":
    unittest.main()
