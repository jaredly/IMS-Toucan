from ebooklib import epub
from bs4 import BeautifulSoup as bs4

book = epub.read_epub('./Inspired.epub')

i = 0
for item in book.items:
    if item.id.startswith('Chapter_') or item.id in ['Introduction', 'Epilogue']:
        print(item.id)
        contents = item.get_content()
        soup = bs4(contents)
        lines = [x for x in soup.get_text().split('\n') if x.strip()]
        # print(lines)
        open('Inspired/{:02}_{}.txt'.format(i, item.id), 'wb').write('\n'.join(lines).encode('utf8'))
        i += 1
        
