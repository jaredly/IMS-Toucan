#!/usr/bin/env python3.8
import sys
from ebooklib import epub
import ebooklib
import os.path
from bs4 import BeautifulSoup as bs4

def convert_book(bookpath):
    name = os.path.basename(bookpath)
    out = os.path.dirname(bookpath) + '/convert_' + name
    os.makedirs(out, exist_ok=True)
    book = epub.read_epub(bookpath)
    for i, item in enumerate(book.get_items_of_type(ebooklib.ITEM_DOCUMENT)):
        print(item.id)
        contents = item.get_content()
        soup = bs4(contents)
        lines = [x for x in soup.get_text().split('\n') if x.strip()]
        open('{}/{:02}_{}.txt'.format(out, i, item.id), 'wb').write('\n'.join(lines).encode('utf8'))

if __name__ == '__main__':
    bookpath = sys.argv[1]
    convert_book(bookpath)
    # book = epub.read_epub(bookpath)

    # for item in book.items:
    #     print(item.id)
        
