import unittest
from functools import reduce
from textnode import TextNode, TextType
from utils import text_to_textnodes

class TestTextToNodes(unittest.TestCase):
    def test_bootdev_example(self):
        new_nodes = text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        expected_result = [
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
        self.assertListEqual(new_nodes, expected_result)

    def test_only_image(self):
        new_nodes = text_to_textnodes("![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)")
        expected_result = [
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(new_nodes, expected_result)

    def test_empty_string(self):
        new_nodes = text_to_textnodes("")
        expected_result = [TextNode("", TextType.TEXT)]
        self.assertListEqual(new_nodes, expected_result)

    def test_single_level(self):
        new_nodes = text_to_textnodes("This is **text *italic* text** with an word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text *italic* text", TextType.BOLD),
            TextNode(" with an word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(new_nodes, expected_result)

if __name__ == "__main__":
    unittest.main()