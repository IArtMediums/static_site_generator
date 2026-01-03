import re


def extract_title(md):
    header = find_header(md)
    return header


def find_header(md):
    pattern = re.compile(r"^# (.+)")
    match = pattern.search(md)
    if not match:
        raise Exception("header was not found for provided md")
    return match.group(1).strip()
