#!/usr/bin/env python3.8
import os

import torch

from phonemizer.backend.espeak.wrapper import EspeakWrapper
from InferenceInterfaces.InferenceFastSpeech2 import InferenceFastSpeech2

import io
import os.path
import time
import sys

# If windows
# EspeakWrapper.set_library("C:\\Program Files\\eSpeak NG\\libespeak-ng.dll")


'''
Roadmap
- [ ] each paragraph gets written as its own file, for better interruptibility
- [ ] show a progress bar on the CLI for the current chapter, along with (words per minute), (remanining words) and (estimated time remaining)
    progress bar can be done by writing `\r` at the end of a line, forcing it to flush and bringin the cursor to the beginning of the line
    - [ ] progress bar for the current chapter, and also for the book as a whole.
    - [ ] \033[2F moves the cursor up 2 lines \0332K clears the line

'''


def read_texts(model_id, sentence, filename, device="cpu", language="en"):
    tts = InferenceFastSpeech2(device=device, model_name=model_id)
    tts.set_language(language)
    if type(sentence) == str:
        sentence = [sentence]
    tts.read_to_file(text_list=sentence, file_location=filename, silent_after=True)
    del tts

def convert_all_chapters(dirname):
    exec_device = "cuda" if torch.cuda.is_available() else "cpu"
    os.makedirs("audios", exist_ok=True)

    start = time.time()
    chapters = [name for name in sorted(os.listdir(dirname)) if name.endswith('.txt')]
    texts = [io.open(dirname + "/" + name, encoding="utf-8").read() for name in chapters]
    wordcounts = [len(text.split()) for text in texts]
    total_words = sum(wordcounts)

    words_read = 0
    last_few_wps = []

    tts = InferenceFastSpeech2(device=exec_device, model_name="Meta")
    tts.set_language("en")
    # tts.read_to_file(text_list=sentence, file_location=filename, silent_after=True)

    print('Begin', total_words, 'words')

    for i, name in enumerate(chapters):
        text = texts[i]
        dest = dirname + "/" + name + ".wav"
        if os.path.exists(dest):
            print("Already completed", dest)
            continue

        chapter_words = wordcounts[i]
        chapter_read = 0

        for j, sentence in enumerate(x for x in text.split('\n') if x.strip()):
            dest_j = "{}/{}_{:02}.wav".format(dirname, name, j)
            before = time.time()
            # read_texts(model_id="Meta", sentence=sentence, filename=dest_j, device="cpu", language="en")
            tts.read_to_file(text_list=[sentence], file_location=dest_j, pause_after=True, silent=True)
            after = time.time()
            wps = len(sentence.split()) / (after - before)
            last_few_wps.append(wps)
            if len(last_few_wps) > 10:
                last_few_wps = last_few_wps[-10:]

            words_read += len(sentence.split())
            chapter_read += len(sentence.split())
            estimated_wps = sum(last_few_wps) / len(last_few_wps)

            print_status(words_read, total_words, estimated_wps, chapter_read, chapter_words)

        # print(name, 'took', time.time() - mid)
        # total = time.time() - mid
        # per = total / (i + 1)
        # print('So far', total, i, 'out of', len(chapters), per, 'per chapter', (total - i - 1) * per, 'left')
        # 394.4415681362152

def progressbar(width, percent):
    return '[' + '=' * int(width * percent) + ' ' * (width - int(width * percent)) + ']'

def print_status(words_read, total_words, estimated_wps, chapter_read, chapter_words):
    print(progressbar(100, words_read / total_words), "{:.2f} wps".format(estimated_wps), "{:.2f} minutes remaining".format((total_words - words_read) / estimated_wps / 60))
    print(progressbar(100, chapter_read / chapter_words), "{:.2f} minutes remaining for this chapter".format((chapter_words - chapter_read) / estimated_wps / 60), end='\r')
    print('\033[1F', end='')

if __name__ == '__main__':
    bookpath = sys.argv[1]
    convert_all_chapters(bookpath)