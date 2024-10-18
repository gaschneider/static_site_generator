import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        props = {"id": "abc", "href": "https://url.com"}
        node = HTMLNode("a", props=props)
        self.assertEqual(node.props_to_html(), ' id="abc" href="https://url.com"')

    def test_repr(self):
        node = HTMLNode()
        self.assertEqual("", repr(node))

    def test_repr_tag_value(self):
        node = HTMLNode("a", "click me")
        self.assertEqual("<a>click me", repr(node))

    def test_repr_props(self):
        props = {"id": "abc", "href": "https://url.com"}
        node = HTMLNode("a", "click me", props=props)
        self.assertEqual("<a>click me - Props:[('id', 'abc'), ('href', 'https://url.com')]", repr(node))
    
    def test_repr_children(self):
        child_node = HTMLNode("b", "click me")
        node = HTMLNode("a", children=[child_node])
        self.assertEqual("<a> - Children count 1", repr(node))

    def test_to_html(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    # LeafNode Tests
    def test_leafnode_raw_text(self):
        node = LeafNode(None, "This is a raw text")
        self.assertEqual(node.to_html(), "This is a raw text")

    def test_leafnode_tag(self):
        node = LeafNode("a", "Click me!")
        self.assertEqual(node.to_html(), '<a>Click me!</a>')

    def test_leafnode_props(self):
        props = {"href": "https://url.com"}
        node = LeafNode("a", "Click me!", props=props)
        self.assertEqual(node.to_html(), '<a href="https://url.com">Click me!</a>')

    def test_leafnode_no_value(self):
        node = LeafNode()
        self.assertRaises(ValueError, node.to_html)

    # ParentNode Tests
    def test_parentnode_raw_text(self):
        node = ParentNode("div", None, [LeafNode(None, "click me")])
        self.assertEqual(node.to_html(), "<div>click me</div>")

    def test_parentnode_leaf_node(self):
        node = ParentNode("div", None, [LeafNode("a", "click me")])
        self.assertEqual(node.to_html(), "<div><a>click me</a></div>")

    def test_parentnode_nested_parent_node(self):
        leaf_node = LeafNode("a", "click me")
        nested_parent_node = ParentNode("div", None, [leaf_node])
        node = ParentNode("div", None, [nested_parent_node, leaf_node])
        self.assertEqual(node.to_html(), "<div><div><a>click me</a></div><a>click me</a></div>")

    def test_parentnode_raw_text(self):
        leaf_node = LeafNode("a", "click me")
        nested_parent_node = ParentNode("div", None, [leaf_node])
        node = ParentNode("div", None, [nested_parent_node, leaf_node])
        self.assertEqual(node.to_html(), "<div><div><a>click me</a></div><a>click me</a></div>")

    def test_parentnode_bootdev_example(self):
        node = ParentNode(
            "p",
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parentnode_no_tag(self):
        node = ParentNode(None, [LeafNode("a", "click me")])
        self.assertRaises(ValueError, node.to_html)

    def test_parentnode_no_children(self):
        node = ParentNode("div", [])
        self.assertRaises(ValueError, node.to_html)

    def test_parentnode_no_children_2(self):
        node = ParentNode("div", None)
        self.assertRaises(ValueError, node.to_html)

if __name__ == "__main__":
    unittest.main()