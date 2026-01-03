import os
import re

from extract_title import extract_title
from markdown_to_html_node import markdown_to_html_node


def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    current_content_list = os.listdir(dir_path_content)
    if len(current_content_list) == 0:
        return
    current_content_dir = dir_path_content
    current_dest_dir = dest_dir_path
    for dir in current_content_list:
        content_dir = os.path.join(current_content_dir, dir)
        dest_dir = os.path.join(current_dest_dir, dir)
        if os.path.isfile(content_dir):
            html_file = dir.replace(".md", ".html")
            dest_html = os.path.join(current_dest_dir, html_file)
            generate_page(content_dir, template_path, dest_html)
        else:
            os.mkdir(dest_dir)
            generate_page_recursive(content_dir, template_path, dest_dir)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md = f.read()
    with open(template_path, "r") as f:
        temp = f.read()

    node = markdown_to_html_node(md)
    html = node.to_html()
    title = extract_title(md)
    generated_html = replace_placeholders(temp, html, title)
    set_up_directory(dest_path)
    with open(dest_path, "w") as f:
        f.write(generated_html)


def replace_placeholders(template, content, title):
    title_pattern = r"{{ Title }}"
    content_pattern = r"{{ Content }}"
    temp_with_title = re.sub(title_pattern, title, template)
    return re.sub(content_pattern, content, temp_with_title)


def set_up_directory(file_path):
    dir_list = file_path.split("/")
    current_dir = dir_list.pop(0)
    for dir in dir_list:
        if "html" in dir.split("."):
            continue
        if not os.path.exists(current_dir):
            os.mkdir(current_dir)
        current_dir = os.path.join(current_dir, dir)
