
from typing import List
from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup, Tag
import os
import time
from common import PostMetaData, parse_metadata

environment = Environment(loader=FileSystemLoader('.'))
template  = environment.get_template('posts_list_template.html')

def load_posts() -> List[PostMetaData]:
    posts_dir = 'posts_md'
    return [parse_metadata(os.path.join(posts_dir, f)) for f in os.listdir(posts_dir) if os.path.isfile(os.path.join(posts_dir, f))]


def render_post_index(posts : List[PostMetaData]):
    with open('head_contents.html', 'r') as f:
        head_contents = f.read()
    with open('navbar.html', 'r') as f:
        navbar = f.read()
    content = template.render(posts=posts, head_contents=head_contents, navbar=navbar)
    with open('posts.html', 'w') as f:
        f.write(content)

render_post_index(load_posts())
