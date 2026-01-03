import re

from textnode import TextNode, TextType


def split_node_delimiter(old_nodes, delimiter, text_type):
    if len(old_nodes) == 0:
        return []
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        new_nodes.extend(split_text_v2(node.text, delimiter, text_type))
    return new_nodes


def split_text_v2(text, delimiter, text_type):
    escaped_delimiter = re.escape(delimiter)
    str_pattern = escaped_delimiter + "(.+?)" + escaped_delimiter
    pattern = re.compile(str_pattern)
    nodes = []
    last_end = 0
    for match in pattern.finditer(text):
        if match.start() > last_end:
            new_text = text[last_end : match.start()]
            text_node = TextNode(new_text, TextType.TEXT)
            nodes.append(text_node)
        delimiter_text = match.group(1)
        node = TextNode(delimiter_text, text_type)
        nodes.append(node)
        last_end = match.end()
    if last_end < len(text):
        new_text = text[last_end:]
        text_node = TextNode(new_text, TextType.TEXT)
        nodes.append(text_node)
    return nodes


def split_text(text, delimiter, text_type):
    words = text.split(" ")
    start_found = False
    new_nodes = []
    new_text = []
    for word in words:
        #       print(f"processing word: {word}")
        extract_delimiter = word.split(delimiter)
        #       print(f"extraction result: {extract_delimiter}")
        if len(extract_delimiter) == 3:
            #           print("one word delimiter found")
            if len(new_text) != 0:
                #               print("adding previous text")
                text_node = TextNode(" ".join(new_text), TextType.TEXT)
                new_nodes.append(text_node)
                new_text.clear()
            delimiter_node = TextNode(extract_delimiter[1], text_type)
            new_nodes.append(delimiter_node)
            #           print("one word delimiter added")
            continue
        if len(extract_delimiter) == 2:
            #           print("delimiter found")
            if start_found:
                #               print("processing closing delimiter")
                start_found = False
                new_text.append(extract_delimiter[0])
                delimiter_node = TextNode(" ".join(new_text), text_type)
                new_nodes.append(delimiter_node)
                new_text.clear()
            #               print("multi word delimiter added")
            else:
                #               print("processing opening delimiter")
                start_found = True
                if len(new_text) != 0:
                    #                   print("adding previous text")
                    text_node = TextNode(" ".join(new_text), TextType.TEXT)
                    new_nodes.append(text_node)
                    new_text.clear()
                new_text.append(extract_delimiter[1])
            #               print("opening delimiter processed")
            continue
        #       print("non delimiter word added")
        new_text.append(extract_delimiter[0])
    if len(new_text) != 0:
        #       print(f"post processing adding leftover text: {new_text}")
        text_node = TextNode(" ".join(new_text), TextType.TEXT)
        new_nodes.append(text_node)
    if start_found:
        #       print("closing delimiter not found")
        raise Exception("invalid markdown syntax, matching closing delimiter not found")
    return new_nodes
