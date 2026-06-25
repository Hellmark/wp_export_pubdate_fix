#!/usr/bin/env python3
"""Fill in empty <pubDate> tags in a WordPress export XML using <wp:post_date>.

Usage: python3 fix_pubdate.py export.xml
Edits the file in place -- make a backup first.
"""
import re
import sys
from datetime import datetime

POST_DATE = re.compile(r"<wp:post_date><!\[CDATA\[(.*?)\]\]></wp:post_date>")
ITEM_RE = re.compile(r"<item>.*?</item>", re.DOTALL)


def fix_item(item_text):
    if "<pubDate></pubDate>" not in item_text:
        return item_text
    m = POST_DATE.search(item_text)
    if not m:
        return item_text
    dt = datetime.strptime(m.group(1).strip(), "%Y-%m-%d %H:%M:%S")
    formatted = dt.strftime("%a, %d %b %Y %H:%M:%S +0000")
    return item_text.replace(
        "<pubDate></pubDate>", f"<pubDate>{formatted}</pubDate>", 1
    )


def main():
    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    fixed_count = 0

    def repl(match):
        nonlocal fixed_count
        item_text = match.group(0)
        new_text = fix_item(item_text)
        if new_text != item_text:
            fixed_count += 1
        return new_text

    new_content = ITEM_RE.sub(repl, content)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Fixed {fixed_count} items")


if __name__ == "__main__":
    main()
