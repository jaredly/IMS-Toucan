import os

dirname = 'Inspired'
for i, name in enumerate([x for x in os.listdir(dirname) if x.endswith('.wav')]):
    os.system('ffmpeg.exe -i {}/{} {}/out/{}-Part{:02}.mp3'.format(
        dirname,
        name, 
        dirname,
        dirname,
        i
    ))
