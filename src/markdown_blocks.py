import re
from functools import reduce
from enum import Enum
from htmlnode import ParentNode, LeafNode
from utils import text_to_textnodes
from textnode import text_node_to_html_node

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"

HEADING_PATTERN = r"^(#{1,6})\s"
UNORDERED_LIST_PATTERN = r'^[*-]\s'
ORDERED_LIST_PATTERN = r'^(\d+)\.\s'

def markdown_to_blocks(markdown):
    possible_blocks = markdown.split("\n")
    blocks = []

    current_block = None
    for b in possible_blocks:
        if len(b) == 0:
            if not current_block is None:
                blocks.append(current_block.strip(" "))
                current_block = None
            continue

        current_block = b if current_block is None else f"{current_block}\n{b}"

    if not current_block is None:
        blocks.append(current_block.strip(" "))

    return blocks

def markdown_to_blocks_simplified(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    if re.match(HEADING_PATTERN, block):
        return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")
    is_quote = reduce(lambda c, l: c and l.startswith(">"), lines, True) 
    if is_quote:
        return BlockType.QUOTE
    
    is_unordered_list = reduce(lambda c, l: c and re.match(UNORDERED_LIST_PATTERN, l), lines, True) 
    if is_unordered_list:
        return BlockType.UNORDERED_LIST
    
    line_should_match_number = 1
    is_ordered_list = True
    for line in lines:
        check = re.match(ORDERED_LIST_PATTERN, line)
        if not check:
            is_ordered_list = False
            break

        if check.group(1) == line_should_match_number:
                line_should_match_number += 1
    
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def process_block(block):
    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_block_to_html_nodes(block)
        case BlockType.HEADING:
            return heading_block_to_html_nodes(block)
        case BlockType.CODE:
            return code_block_to_html_nodes(block)
        case BlockType.QUOTE:
            return quote_block_to_html_nodes(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_block_to_html_nodes(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_block_to_html_nodes(block)
        case _:
            raise Exception("Invalid block type")

def text_to_children(text):
    return list(map(text_node_to_html_node, text_to_textnodes(text)))                

def paragraph_block_to_html_nodes(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    nodes_in_paragraph = text_to_children(paragraph)
    return [ParentNode("p", None, nodes_in_paragraph)]

def heading_block_to_html_nodes(block):
    nodes_in_heading = []
    lines = block.split("\n")
    for line in lines:
        regex = re.match(HEADING_PATTERN, line)
        hashtag_string = regex.group(1)
        nodes_in_heading.append(ParentNode(f"h{len(hashtag_string)}", None, text_to_children(line[len(hashtag_string)+1:])))

    return nodes_in_heading

def code_block_to_html_nodes(block):
    nodes_in_code = text_to_children(block[3:-3])
    code_node = ParentNode("code", None, nodes_in_code)
    return [ParentNode("pre", None, [code_node])]

def quote_block_to_html_nodes(block):
    nodes_in_quote = []
    lines = block.split("\n")
    for line in lines:
        if len(nodes_in_quote) > 0:
            nodes_in_quote.append(LeafNode("br", ""))

        nodes_in_quote.extend(text_to_children(line[1:].strip(" ")))

    return [ParentNode("blockquote", None, nodes_in_quote)]

def unordered_list_block_to_html_nodes(block):
    nodes_in_list = []
    lines = block.split("\n")
    for line in lines:
        nodes_in_line = text_to_children(line[2:])
        nodes_in_list.append(ParentNode("li", None, nodes_in_line))
    return [ParentNode("ul", None, nodes_in_list)]

def ordered_list_block_to_html_nodes(block):
    nodes_in_list = []
    lines = block.split("\n")
    for line in lines:
        regex = re.match(ORDERED_LIST_PATTERN, line)
        number_string = regex.group(1)
        nodes_in_line = text_to_children(line[len(number_string)+2:])
        nodes_in_list.append(ParentNode("li", None, nodes_in_line))
    return [ParentNode("ol", None, nodes_in_list)]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    nodes_per_block = []
    for b in blocks:
        nodes_per_block.extend(process_block(b))

    return ParentNode("div", None, nodes_per_block)
