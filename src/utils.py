import re
from textnode import TextNode, TextType

IMAGES_REGEX = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
LINKS_REGEX = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        sections = node.text.split(delimiter)
        inside = False
        possible_nodes = []
        for text in sections:
            new_node = TextNode(text, text_type if inside else TextType.TEXT)
            possible_nodes.append(new_node)
            inside = not inside
        
        if len(possible_nodes) % 2 == 0:
            raise Exception("Not valid markdown syntax")
        
        new_nodes.extend(possible_nodes)

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(IMAGES_REGEX, text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(LINKS_REGEX, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue

        current_text = node.text

        for image in images:
            image_alt, image_url = image
            sections = current_text.split(f"![{image_alt}]({image_url})", 1)

            if len(sections) == 0:
                break

            text_before_image = sections[0]
            if len(text_before_image) > 0:
                new_nodes.append(TextNode(text_before_image, TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))

            if len(sections) > 1:
                current_text = sections[1]

        if len(current_text) > 0:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        current_text = node.text

        for link in links:
            link_alt, link_url = link
            sections = current_text.split(f"[{link_alt}]({link_url})", 1)

            if len(sections) == 0:
                break

            text_before_link = sections[0]
            if len(text_before_link) > 0:
                new_nodes.append(TextNode(text_before_link, TextType.TEXT))

            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))

            if len(sections) > 1:
                current_text = sections[1]

        if len(current_text) > 0:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    initial_node = TextNode(text, TextType.TEXT)

    nodes_image_split = split_nodes_image([initial_node])
    nodes_link_split = split_nodes_link(nodes_image_split)
    nodes_bold_split = split_nodes_delimiter(nodes_link_split, "**", TextType.BOLD)
    nodes_italic_split = split_nodes_delimiter(nodes_bold_split, "*", TextType.ITALIC)
    nodes_code_split = split_nodes_delimiter(nodes_italic_split, "`", TextType.CODE)

    return nodes_code_split    