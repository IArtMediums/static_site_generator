from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = None
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    LINK = "a"
    IMAGE = "img"

    def get_splitting_function(self):
        from split_node_delimiter import split_node_delimiter
        from split_nodes_image import split_nodes_image
        from split_nodes_link import split_nodes_link

        match self:
            case TextType.TEXT:
                return None
            case TextType.BOLD:
                return lambda nodes: split_node_delimiter(nodes, "**", TextType.BOLD)
            case TextType.ITALIC:
                return lambda nodes: split_node_delimiter(nodes, "_", TextType.ITALIC)
            case TextType.CODE:
                return lambda nodes: split_node_delimiter(nodes, "`", TextType.CODE)
            case TextType.LINK:
                return lambda nodes: split_nodes_link(nodes)
            case TextType.IMAGE:
                return lambda nodes: split_nodes_image(nodes)


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, o):
        return (
            self.text == o.text and self.text_type == o.text_type and self.url == o.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(TextType.TEXT.value, text_node.text)
        case TextType.BOLD:
            return LeafNode(TextType.BOLD.value, text_node.text)
        case TextType.ITALIC:
            return LeafNode(TextType.ITALIC.value, text_node.text)
        case TextType.CODE:
            return LeafNode(TextType.CODE.value, text_node.text)
        case TextType.LINK:
            return LeafNode(
                TextType.LINK.value, text_node.text, {"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                TextType.IMAGE.value, "", {"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise ValueError(
                f"unable to convert {text_node.text_type.value}  - unsupported text type"
            )
