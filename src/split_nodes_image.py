import re

from textnode import TextNode, TextType


def split_nodes_image(old_nodes):
    if len(old_nodes) == 0:
        return []
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        new_nodes.extend(get_nodes_from_text(text))
    return new_nodes


def get_nodes_from_text(text):
    pattern = re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")
    nodes = []
    last_end = 0
    for match in pattern.finditer(text):
        if match.start() > last_end:
            new_text = text[last_end : match.start()]
            text_node = TextNode(new_text, TextType.TEXT)
            nodes.append(text_node)
        alt = match.group(1)
        url = match.group(2)
        node = TextNode(text=alt, text_type=TextType.IMAGE, url=url)
        nodes.append(node)
        last_end = match.end()
    if last_end < len(text):
        new_text = text[last_end:]
        text_node = TextNode(new_text, TextType.TEXT)
        nodes.append(text_node)
    return nodes
