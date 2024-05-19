#!python3
from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup, Tag
import common

environment = Environment(loader=FileSystemLoader('.'))
template  = environment.get_template('template.html')

def render_file(in_path: str, out_path : str):
    with open(in_path, 'r') as f:
        src = f.read()
    with open('head_contents.html', 'r') as f:
        head_content = f.read()
    with open('navbar.html', 'r') as f:
        navbar = f.read()
    soup = BeautifulSoup(src, 'html.parser')
    title = get_title(soup)
    content = template.render(title=title, content = soup.prettify(), head_content = head_content, navbar=navbar)
    with open(out_path, 'w') as f:
        f.write(content)

def get_title(soup: BeautifulSoup) -> str:
    # Get the text from the h1 tag
    if soup.h1:
        text = soup.h1.text
        soup.h1.decompose()
        return text
    else:
        raise Exception("No title found")

import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: script.py markdown_input_path html_input_path output_path")
    else:
        in_path, out_path = sys.argv[1:3]
        render_file(in_path, out_path)
