from blocktype import BlockType, block_to_blocktype
from htmlnode import LeafNode, ParentNode
from markdown_to_blocks import markdow_to_blocks
from text_to_textnodes import text_to_textnode
from textnode import text_node_to_html_node


def markdown_to_html_node(md):
    blocks = markdow_to_blocks(md)
    div_children = []
    for block in blocks:
        if len(block) == 0:
            continue
        htmlnode = text_to_children(block)
        div_children.append(htmlnode)
    root = ParentNode("div", div_children)
    return root


def text_to_children(text):
    tag = block_to_tag(text)
    if tag == "ul" or tag == "ol":
        return process_list(tag, text)
    if tag != "pre":
        formated_text = format_text(text, tag)
        nodes = text_to_textnode(formated_text)
        children = textnodes_to_children(nodes)
        parent = ParentNode(tag, children)
        return parent
    node = LeafNode("code", format_text(text, tag))
    parent = ParentNode(tag, [node])
    return parent


def format_text(text, tag):
    if tag == "blockquote":
        lines = text.split("\n")
        items = []
        for line in lines:
            items.append(line[1:].strip())
        return " ".join(items)
    if tag[0] == "h":
        h_count = count_heading(text)
        return text[h_count + 1 :]
    if tag == "pre":
        return text.split("```")[1]
    if tag == "p":
        lines = text.split("\n")
        return " ".join(lines)


def process_list(tag, text):
    lines = text.split("\n")
    items = []
    for line in lines:
        formated_line = line[2:]
        nodes = text_to_textnode(formated_line.strip())
        children = textnodes_to_children(nodes)
        parent = ParentNode("li", children)
        items.append(parent)
    list = ParentNode(tag, items)
    return list


def textnodes_to_children(nodes):
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children


def block_to_tag(text):
    block_type = block_to_blocktype(text)
    match block_type:
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case BlockType.HEADING:
            return f"h{count_heading(text)}"
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.CODE:
            return "pre"


def count_heading(text):
    count = 0
    for c in text:
        if c == "#":
            count += 1
        else:
            break
    return count
