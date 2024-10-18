import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownBlocks(unittest.TestCase):
    def test_bootdev_example(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""

        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                """* This is the first list item in a list block
* This is a list item
* This is another list item"""
            ]
        )

    def test_remove_multiple_lines_between_blocks(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.




* This is the first list item in a list block
* This is a list item
* This is another list item
"""

        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                """* This is the first list item in a list block
* This is a list item
* This is another list item"""
            ]
        )

    def test_multiple_blocks_with_multiple_lines(self):
        markdown = """# This is a heading
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.
This is a paragraph of text. It has some **bold** and *italic* words inside of it.



* This is the first list item in a list block
* This is a list item
* This is another list item """

        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            blocks,
            [
                """# This is a heading
# This is a heading""",
                """This is a paragraph of text. It has some **bold** and *italic* words inside of it.
This is a paragraph of text. It has some **bold** and *italic* words inside of it.""",
                """* This is the first list item in a list block
* This is a list item
* This is another list item"""
            ]
        )

    def test_block_type_paragraph(self):
        block_type = block_to_block_type("This is a paragraph")
        self.assertEqual(BlockType.PARAGRAPH, block_type)
    
    def test_block_type_heading(self):
        block_type = block_to_block_type("# This is a heading")
        self.assertEqual(BlockType.HEADING, block_type)
        
        block_type = block_to_block_type("## This is a heading")
        self.assertEqual(BlockType.HEADING, block_type)
        
        block_type = block_to_block_type("### This is a heading")
        self.assertEqual(BlockType.HEADING, block_type)
        
        block_type = block_to_block_type("#### This is a heading")
        self.assertEqual(BlockType.HEADING, block_type)
        
        block_type = block_to_block_type("##### This is a heading")
        self.assertEqual(BlockType.HEADING, block_type)
        
        block_type = block_to_block_type("###### This is a heading")
        self.assertEqual(BlockType.HEADING, block_type)

        block_type = block_to_block_type("####### This is a heading")
        self.assertEqual(BlockType.PARAGRAPH, block_type)
    
    def test_block_type_code(self):
        block_type = block_to_block_type("""```
This is a code block
```""")
        self.assertEqual(BlockType.CODE, block_type)
    
    def test_block_type_quote(self):
        block_type = block_to_block_type(
"""> This is a quote block
>second quote"""            
        )
        self.assertEqual(BlockType.QUOTE, block_type)
    
    def test_block_type_unordered(self):
        block_type = block_to_block_type(
"""* This is an unordered list block
- with two lines
* or maybe three""")
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)

        block_type = block_to_block_type(
"""* This is an unordered list line
- with two lines
*but not a third one that fits the rule"""
)
        self.assertEqual(BlockType.PARAGRAPH, block_type)
    
    def test_block_type_ordered(self):
        block_type = block_to_block_type(
"""1. This is an ordered list block
2. with two lines
3. or maybe three"""
)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)

        block_type = block_to_block_type(
"""1. This is an ordered list line
3. with two lines
3.but not a third one that fits the rule"""
)
        self.assertEqual(BlockType.PARAGRAPH, block_type)


if __name__ == "__main__":
    unittest.main()