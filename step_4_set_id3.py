import os
import os.path
import sys
import tempfile

# from mutagen.mp3 import MP3  
from mutagen.mp3 import EasyMP3 as MP3
# from mutagen.easyid3 import EasyID3  
import mutagen.id3  
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER  

# dirname = 'Inspired'
def convert_folder(title, author, dirname):
    all = sorted(os.listdir(dirname))
    chapters = [x for x in all if x.endswith('.txt') and os.path.exists(os.path.join(dirname, x + '.mp3'))]
    for i, name in enumerate(chapters):
        print('####----', i, name, '----####')
        mp3path = os.path.join(dirname, name + '.mp3')
        text = open(os.path.join(dirname, name), encoding='utf8').read()
        first_line = text.split('\n')[0]

        mp3file = MP3(mp3path)
        if i == 0:
            mp3file['title'] = title
        else:
            mp3file['title'] = first_line[0:50]
        print(mp3file['title'])
        mp3file['artist'] = author
        mp3file['album'] = title
        mp3file['tracknumber'] = "{}/{}".format(i + 1, len(chapters))
        mp3file.save()


if __name__ == '__main__':
    title = sys.argv[1]
    author = sys.argv[2]
    bookpath = sys.argv[3]
    convert_folder(title, author, bookpath)