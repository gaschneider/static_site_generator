from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, HEADING_PATTERN
import re

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for b in blocks:
        b_type = block_to_block_type(b)
        if b_type == BlockType.HEADING:
            lines = b.split("\n")
            for line in lines:
                regex = re.match(HEADING_PATTERN, line)
                hashtag_string = regex.group(1)
                if len(hashtag_string) == 1:
                    return line[2:].strip(" ")
                
    raise Exception("No header found")