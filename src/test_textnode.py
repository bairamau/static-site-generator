import unittest

from textnode import TextNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.url, None)

    def test_convert(self):
        self.assertEqual(text_node_to_html_node(TextNode('an image of dinosaur', 'image', 'dinosaur.jpeg')).to_html(),
                                                '<img src="dinosaur.jpeg" alt="an image of dinosaur"></img>')
if __name__ == "__main__":
    unittest.main()
