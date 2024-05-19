import os

class PostMetaData:
    def __init__(self, title : str, author : str, date : str, link : str):
        self.title = title
        self.author = author
        self.date = date
        self.link = link

def parse_metadata(path : str) -> PostMetaData:
    with open(path, 'r') as f:
        content = f.readlines()[:3]
    basename_without_extension = os.path.splitext(os.path.basename(path))[0]
    title = parse_line(content[0])
    author = parse_line(content[1])
    date = parse_line(content[2])
    link = f'/posts/{basename_without_extension}.html'
    return PostMetaData(title, author, date, link)


def parse_line(line : str) -> str:
    if line[0] == '%':
        return line[1:].strip()
    else:
        raise Exception("Invalid metadata line")
