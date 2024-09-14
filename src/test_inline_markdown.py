import unittest

from textnode import TextNode, TextType
from inline_markdown import (
        split_nodes_delimiter,
        extract_markdown_images,
        extract_markdown_links,
        split_nodes_image,
        split_nodes_link,
        text_to_textnodes
        )

class InlineMarkdown(unittest.TestCase):
    def test_delimiter(self):
        nodes = split_nodes_delimiter(
                [TextNode("aye `what's good` my friend", TextType.TEXT),
                 TextNode("this is code node", TextType.CODE)],
                "`",
                TextType.CODE)
        
        self.assertEqual(nodes, [TextNode("aye ", TextType.TEXT), 
                                 TextNode("what's good", TextType.CODE), 
                                 TextNode(" my friend", TextType.TEXT),
                                 TextNode("this is code node", TextType.CODE)])

    def test_invalid(self):
        self.assertRaises(Exception, split_nodes_delimiter, [TextNode("aye **what's good my friend", TextType.TEXT)], "**", TextType.BOLD)

    def test_several(self):
        nodes = split_nodes_delimiter([TextNode("aye **what** **is** **good**", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(nodes,[TextNode("aye ", TextType.TEXT),
                                TextNode("what", TextType.BOLD),
                                TextNode(" ", TextType.TEXT),
                                TextNode("is", TextType.BOLD),
                                TextNode(" ", TextType.TEXT),
                                TextNode("good", TextType.BOLD)])

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [('![rick roll](https://i.imgur.com/aKaOqIh.gif)',
                                    'rick roll',
                                    'https://i.imgur.com/aKaOqIh.gif'),
                                   ('![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)',
                                    'obi wan',
                                    'https://i.imgur.com/fJRm4Vk.jpeg')
                                   ]
                         )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [('[to boot dev](https://www.boot.dev)', 
                                    'to boot dev', 
                                    'https://www.boot.dev'),
                                   ('[to youtube](https://www.youtube.com/@bootdotdev)',
                                    'to youtube',
                                    'https://www.youtube.com/@bootdotdev')
                                   ]
                         )

    def test_split_nodes_image(self):
        node = TextNode('![dog playing with a bone](doggie.jpg)', TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [TextNode("dog playing with a bone", TextType.IMAGE, "doggie.jpg")]) 

        node = TextNode(
                "This is text with an image ![cat](cat.jpg) and ![dog](dog.jpg)",
                TextType.TEXT
                )
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "dog", TextType.IMAGE, "dog.jpg"
            ),
            ])

    def test_split_nodes_link(self):
        node = TextNode("[home](google.com)", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [TextNode("home", TextType.LINK, "google.com")])
                         
        node = TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT,
                )
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
             TextNode("This is text with a link ", TextType.TEXT),
             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
             TextNode(" and ", TextType.TEXT),
             TextNode(
                 "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
             ),
         ])

    def test_text_to_textnodes(self):
        text = 'This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        output = [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                ]
        self.assertEqual(text_to_textnodes(text), output)

        text = ''
        output = []
        self.assertEqual(text_to_textnodes(text), output)
if __name__ == "__main__":
    unittest.main()

