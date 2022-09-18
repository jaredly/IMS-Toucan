import os
import os.path
import sys
import tempfile

# dirname = 'Inspired'
def convert_folder(dirname):
    all = sorted(os.listdir(dirname))
    for i, name in enumerate([x for x in all if x.endswith('.txt')]):
        wavs = [x for x in all if x.startswith(name) and x.endswith('.wav')]
        print('####----', i, name, len(wavs), '----####')
        if not len(wavs):
            continue
        
        tf = tempfile.mktemp(suffix='.txt')
        print(tf)
        open(tf, 'w').write(
                    '\n'.join(["file '{}'".format(os.path.join(dirname, x)) for x in wavs]))
        cmd = 'ffmpeg -f concat -safe 0 -i {} {}'.format(
            tf,
            os.path.join(dirname, name + '.mp3')
        )
        os.system(cmd)
        os.unlink(tf)
        # print(cmd)
        # fial

        # os.system('ffmpeg.exe -i {}/{} {}/out/{}-Part{:02}.mp3'.format(
        #     dirname,
        #     name, 
        #     dirname,
        #     dirname,
        #     i
        # ))

if __name__ == '__main__':
    bookpath = sys.argv[1]
    convert_folder(bookpath)