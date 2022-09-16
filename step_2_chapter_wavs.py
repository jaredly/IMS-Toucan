import os

import torch

from phonemizer.backend.espeak.wrapper import EspeakWrapper
from InferenceInterfaces.InferenceFastSpeech2 import InferenceFastSpeech2

# If windows
# EspeakWrapper.set_library("C:\\Program Files\\eSpeak NG\\libespeak-ng.dll")

def read_texts(model_id, sentence, filename, device="cpu", language="en"):
    tts = InferenceFastSpeech2(device=device, model_name=model_id)
    tts.set_language(language)
    if type(sentence) == str:
        sentence = [sentence]
    tts.read_to_file(text_list=sentence, file_location=filename)
    del tts

import io
import os.path
import time

def convert_all_chapters(dirname):
    exec_device = "cuda" if torch.cuda.is_available() else "cpu"
    os.makedirs("audios", exist_ok=True)

    start = time.time()
    chapters = os.listdir(dirname)
    for i, name in enumerate(chapters):
        if name.endswith('.txt'):
            text = io.open(dirname + '/' + name, encoding='utf8').read()
            mid = time.time()
            read_texts(model_id="Meta", sentence=text.split('\n'), filename=dirname + "/" + name + ".wav", device="cpu", language="en")
            print(name, 'took', time.time() - mid)
            total = time.time() - mid
            per = total / (i + 1)
            print('So far', total, i, 'out of', len(chapters), per, 'per chapter', (total - i - 1) * per, 'left')
            # 394.4415681362152
