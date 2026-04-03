import os
from datetime import datetime

class PostMetaData:
    def __init__(self, title : str, author : str, date : str, link : str, hidden : bool = False):
        self.title = title
        self.author = author
        self.date = date
        self.link = link
        self.hidden = hidden

    def parsed_date(self) -> datetime:
        for fmt in ('%B, %d, %Y', '%B %d, %Y'):
            try:
                return datetime.strptime(self.date, fmt)
            except ValueError:
                pass
        raise ValueError(f"Unrecognized date format: {self.date!r}")

def parse_metadata(path : str) -> PostMetaData:
    with open(path, 'r') as f:
        content = f.readlines()[:4]
    basename_without_extension = os.path.splitext(os.path.basename(path))[0]
    title = parse_line(content[0], path, 1)
    author = parse_line(content[1], path, 2)
    date = parse_line(content[2], path, 3)
    hidden = len(content) > 3 and content[3].startswith('%') and parse_line(content[3], path, 4).lower() == 'hidden'
    link = f'/posts/{basename_without_extension}.html'
    return PostMetaData(title, author, date, link, hidden)

class InvalidMetadataException(Exception):
    pass


def parse_line(line : str, file : str, lineno : int) -> str:
    if line[0] == '%':
        return line[1:].strip()
    else:
        raise InvalidMetadataException(f"{file}:{lineno}: expected metadata line starting with '%'")
