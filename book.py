import os

for i, name in enumerate([x for x in os.listdir('Inspired') if x.endswith('.wav')]):
    os.system('ffmpeg.exe -i Inspired/{} Inspired/out/Inspired-Part{:02}.mp3'.format(
        name, 
        i
    ))
