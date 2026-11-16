"""Small classroom content contract, not a complete HTML or security audit."""
from html.parser import HTMLParser
from pathlib import Path
import sys

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1_count = 0
        self.in_title = False
        self.title = []
        self.styles = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.in_title = True
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.styles.append(attrs.get("href", ""))
    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)

def validate_site(directory):
    root = Path(directory).resolve()
    page = root / "index.html"
    if not page.is_file():
        raise ValueError("index.html is missing")
    parser = SiteParser()
    parser.feed(page.read_text(encoding="utf-8"))
    if not "".join(parser.title).strip():
        raise ValueError("Page title must not be empty")
    if parser.h1_count != 1:
        raise ValueError("Page must contain exactly one h1 heading")
    if not parser.styles:
        raise ValueError("At least one local stylesheet is required")
    for href in parser.styles:
        target = (root / href).resolve()
        if not href or not target.is_relative_to(root) or not target.is_file():
            raise ValueError(f"Missing or invalid local stylesheet: {href}")
    return "PASS title, heading and stylesheet contract"

if __name__ == "__main__":
    try:
        print(validate_site(sys.argv[1] if len(sys.argv) > 1 else "src"))
    except (ValueError, OSError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        sys.exit(1)
