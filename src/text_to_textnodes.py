from textnode import TextNode, TextType


def text_to_textnode(text):
    root = TextNode(text, TextType.TEXT)
    split_code = TextType.CODE.get_splitting_function()
    split_code_result = split_code([root])
    split_images = TextType.IMAGE.get_splitting_function()
    split_images_result = split_images(split_code_result)
    split_links = TextType.LINK.get_splitting_function()
    split_links_result = split_links(split_images_result)
    split_bold = TextType.BOLD.get_splitting_function()
    split_bold_result = split_bold(split_links_result)
    split_italic = TextType.ITALIC.get_splitting_function()
    split_italic_result = split_italic(split_bold_result)
    return split_italic_result
