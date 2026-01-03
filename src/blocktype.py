import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "c"
    QUOTE = "q"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"


def block_to_blocktype(block):
    pattern_map = {
        BlockType.HEADING: r"^#{1,6} .+(?:\n.+)*$",
        BlockType.QUOTE: r"^(?:>.*\n?)+$",
        BlockType.CODE: r"^```\n[\s\S]*?\n```$",
        BlockType.UNORDERED_LIST: r"^(?:- .*\n?)+$",
        BlockType.ORDERED_LIST: r"^(?:\d+.*\n?)+$",
    }
    type_found = BlockType.PARAGRAPH
    for type in pattern_map:
        if is_match_found(pattern_map[type], block):
            type_found = type
            break
    if type_found == BlockType.ORDERED_LIST and not is_list_ordered(block):
        type_found = BlockType.PARAGRAPH
    return type_found


def is_match_found(pattern, text):
    result = re.fullmatch(pattern, text)
    return True if result else False


def is_block_code(text):
    count = 0
    is_opened = False
    for c in text:
        if c == "`":
            count += 1
        if count == 3:
            is_opened = True
    if count == 6 and is_opened:
        return True
    else:
        return False


def is_list_ordered(num_list):
    lines = num_list.split("\n")
    last_num = 0
    for line in lines:
        str_num = line[0]
        current_num = int(str_num)
        if current_num == last_num + 1:
            last_num = current_num
            continue
        else:
            return False
    return True
