import wave
import os

'''
this was to fix the extra .5s of silence at the end of the per-sentence files
that I put there accidentally.
'''
# fname = '/Users/jared/Downloads/arbitrary-lines-copy.epub/03_tit01.txt_01.wav'

def fix_wave(fname):
	w = wave.open(fname, 'rb')
	params = w.getparams()
	data = w.readframes(int(w.getnframes() - w.getframerate() / 2))
	w.close()

	o = wave.open(fname, 'wb')
	o.setparams(params)
	o.writeframes(data)
	o.close()

# fix_wave(fname)

base = '/Users/jared/Downloads/arbitrary-lines-copy.epub/'
for name in os.listdir(base):
	if name.endswith('.wav') and '.txt_' in name:
		print(name)
		fix_wave(base + name)

