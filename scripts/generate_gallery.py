#!/usr/bin/env python3
"""
Scan the `images/` folder for files beginning with `khaeby` and
inject carousel items into `index.html` between the
`<!-- GALLERY-START -->` and `<!-- GALLERY-END -->` markers.

Run from the repository root:

    python3 scripts/generate_gallery.py

This script overwrites only the portion between the markers.
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGES_DIR = ROOT / 'images'
INDEX_FILE = ROOT / 'index.html'

VALID_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
PREFIX = 'khaeby'

T_START = '<!-- GALLERY-START -->'
T_END = '<!-- GALLERY-END -->'

ITEM_TEMPLATE = (
    '                        <div class="item animate-box" data-animate-effect="fadeIn">\n'
    '                            <a href="{href}" class="image-popup">\n'
    '                                <img src="{src}" alt="{alt}" style="width:100%; height:auto; border-radius:6px;" />\n'
    '                            </a>\n'
    '                        </div>\n'
)


def find_images():
    if not IMAGES_DIR.exists():
        print(f"Images directory not found: {IMAGES_DIR}")
        return []
    files = []
    for p in sorted(IMAGES_DIR.iterdir()):
        if not p.is_file():
            continue
        name = p.name
        stem = p.stem
        if not stem.lower().startswith(PREFIX.lower()):
            continue
        if p.suffix.lower() not in VALID_EXT:
            continue
        files.append(name)
    return files


def generate_items(files):
    items = []
    for name in files:
        href = f"images/{name}"
        src = href
        alt = os.path.splitext(name)[0]
        items.append(ITEM_TEMPLATE.format(href=href, src=src, alt=alt))
    return ''.join(items)


def main():
    imgs = find_images()
    if not imgs:
        print('No images found with prefix "{0}" in {1}'.format(PREFIX, IMAGES_DIR))
        return

    items_html = generate_items(imgs)

    text = INDEX_FILE.read_text(encoding='utf-8')
    if T_START not in text or T_END not in text:
        print('Markers not found in', INDEX_FILE)
        return

    pre, rest = text.split(T_START, 1)
    _, post = rest.split(T_END, 1)

    new_text = pre + T_START + '\n' + items_html + '                        ' + T_END + post

    INDEX_FILE.write_text(new_text, encoding='utf-8')
    print(f'Injected {len(imgs)} images into {INDEX_FILE}')


if __name__ == '__main__':
    main()
