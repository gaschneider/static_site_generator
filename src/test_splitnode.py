import unittest
from functools import reduce
from textnode import TextNode, TextType
from utils import split_nodes_delimiter, split_nodes_image, split_nodes_link

def validate_new_and_expected_nodes(new_nodes, expected_result):
    return reduce(lambda c, t: c and t[0] == t[1], tuple(zip(new_nodes, expected_result)), True)

class TestSplitNodes(unittest.TestCase):
    def test_bootdev_example(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [TextNode("This is text with a ", TextType.TEXT),TextNode("code block", TextType.CODE),TextNode(" word", TextType.TEXT)]
        self.assertTrue(validate_new_and_expected_nodes(new_nodes, expected_result))

    def test_bootdev_example_error(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "`", TextType.CODE)

    def test_multiple_delimiter(self):
        node = TextNode("This is text with a `code block` and a `second code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [TextNode("This is text with a ", TextType.TEXT),TextNode("code block", TextType.CODE),TextNode(" and a ", TextType.TEXT),TextNode("second code block", TextType.CODE),TextNode(" word", TextType.TEXT)]
        self.assertTrue(validate_new_and_expected_nodes(new_nodes, expected_result))

    def test_different_delimiter(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_result = [TextNode("This is text with a ", TextType.TEXT),TextNode("bold block", TextType.BOLD),TextNode(" word", TextType.TEXT)]
        self.assertTrue(validate_new_and_expected_nodes(new_nodes, expected_result))

class TestSplitNodesLink(unittest.TestCase):
    def test_bootdev_example(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_result = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            )
        ]
        self.assertTrue(validate_new_and_expected_nodes(new_nodes, expected_result))
    
    def test_image_and_not_link(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_result = [node]
        self.assertTrue(validate_new_and_expected_nodes(new_nodes, expected_result))

    def test_starting_with_link(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_result = [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ![to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)]
        self.assertTrue(validate_new_and_expected_nodes(new_nodes, expected_result))

    def test_only_link(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_result = [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")]
        self.assertTrue(validate_new_and_expected_nodes(new_nodes, expected_result))

class TestSplitNodesImage(unittest.TestCase):
    def test_bootdev_example(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected_result = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
            )
        ]
        self.assertTrue(validate_new_and_expected_nodes(new_nodes, expected_result))
    
    def test_link_and_not_image(self):
        node = TextNode(
            "This is text with an image [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected_result = [node]
        self.assertTrue(validate_new_and_expected_nodes(new_nodes, expected_result))

    def test_starting_with_image(self):
        node = TextNode(
            "![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected_result = [
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
            )
        ]
        self.assertTrue(validate_new_and_expected_nodes(new_nodes, expected_result))

    def test_only_image(self):
        node = TextNode(
            "![to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected_result = [TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev")]
        self.assertTrue(validate_new_and_expected_nodes(new_nodes, expected_result))

if __name__ == "__main__":
    unittest.main()