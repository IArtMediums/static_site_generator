def markdow_to_blocks(md):
    blocks = md.split("\n\n")
    result = []
    for i in range(len(blocks)):
        block = blocks[i]
        proccessed_block = strip_whitespace(block)
        result.append(proccessed_block)

    return result


def strip_whitespace(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.strip())
    return "\n".join(clear_empty_items(new_lines))


def clear_empty_items(list):
    if len(list) == 0:
        return []
    result = []
    for i in list:
        if i != "":
            result.append(i)
    return result
