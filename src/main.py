from generate_page import generate_page_recursive
from transfer_static_to_public import prepare_directories


def main():
    prepare_directories()
    generate_page_recursive("content", "template.html", "public")


main()
