import sys

from generate_page import generate_page_recursive
from transfer_static_to_public import prepare_directories


def main():
    basepath = get_argument()
    prepare_directories()
    generate_page_recursive("content", "template.html", "docs", basepath)


def get_argument():
    if len(sys.argv) == 2:
        return sys.argv[1]
    return "/"


main()
