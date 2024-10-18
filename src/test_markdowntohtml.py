import unittest
from markdown_blocks import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
    def test_bootdev_example(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""

        html_node = markdown_to_html_node(markdown)
        self.assertEqual(
            html_node.to_html(),
            "<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul></div>"
        )
    
    def test_multiple_headings(self):
        markdown = """
# This is a heading
## This is a heading
### This is a heading
#### This is a heading
##### This is a heading
###### This is a heading
"""

        html_node = markdown_to_html_node(markdown)
        self.assertEqual(
            html_node.to_html(),
            "<div><h1>This is a heading</h1><h2>This is a heading</h2><h3>This is a heading</h3><h4>This is a heading</h4><h5>This is a heading</h5><h6>This is a heading</h6></div>"
        )
    
    def test_code_block(self):
        markdown = """```
This is a
code block
with some **bold**
and *italic* words
in it
```
"""

        html_node = markdown_to_html_node(markdown)
        self.assertEqual(
            html_node.to_html(),
            "<div><pre><code>\nThis is a\ncode block\nwith some <b>bold</b>\nand <i>italic</i> words\nin it\n</code></pre></div>"
        )

    def test_ol(self):
        markdown = """1. First item
2. Second item
3. Third item
"""

        html_node = markdown_to_html_node(markdown)
        self.assertEqual(
            html_node.to_html(),
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>"
        )

    def test_ul(self):
        markdown = """* First unordered item
- Second **unordered** item
* Third *unordered* item
"""

        html_node = markdown_to_html_node(markdown)
        self.assertEqual(
            html_node.to_html(),
            "<div><ul><li>First unordered item</li><li>Second <b>unordered</b> item</li><li>Third <i>unordered</i> item</li></ul></div>"
        )

    def test_quote(self):
        markdown = """>Quote 1
>Quote 2
> Quote 3
"""

        html_node = markdown_to_html_node(markdown)
        self.assertEqual(
            html_node.to_html(),
            "<div><blockquote>Quote 1<br />Quote 2<br /> Quote 3</blockquote></div>"
        )

if __name__ == "__main__":
    unittest.main()