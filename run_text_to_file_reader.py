import os

import torch

from phonemizer.backend.espeak.wrapper import EspeakWrapper
from InferenceInterfaces.InferenceFastSpeech2 import InferenceFastSpeech2

EspeakWrapper.set_library("C:\\Program Files\\eSpeak NG\\libespeak-ng.dll")

def read_texts(model_id, sentence, filename, device="cpu", language="en"):
    tts = InferenceFastSpeech2(device=device, model_name=model_id)
    tts.set_language(language)
    if type(sentence) == str:
        sentence = [sentence]
    tts.read_to_file(text_list=sentence, file_location=filename)
    del tts


def read_texts_as_ensemble(model_id, sentence, filename, device="cpu", language="en", amount=10):
    """
    for this function, the filename should NOT contain the .wav ending, it's added automatically
    """
    tts = InferenceFastSpeech2(device=device, model_name=model_id)
    tts.set_language(language)
    if type(sentence) == str:
        sentence = [sentence]
    for index in range(amount):
        tts.default_utterance_embedding = torch.zeros(704).float().random_(-40, 40).to(device)
        tts.read_to_file(text_list=sentence, file_location=filename + f"_{index}" + ".wav")


def read_harvard_sentences(model_id, device):
    tts = InferenceFastSpeech2(device=device, model_name=model_id)

    with open("Utility/test_sentences_combined_3.txt", "r", encoding="utf8") as f:
        sents = f.read().split("\n")
    output_dir = "audios/harvard_03_{}".format(model_id)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    for index, sent in enumerate(sents):
        tts.read_to_file(text_list=[sent], file_location=output_dir + "/{}.wav".format(index))

    with open("Utility/test_sentences_combined_6.txt", "r", encoding="utf8") as f:
        sents = f.read().split("\n")
    output_dir = "audios/harvard_06_{}".format(model_id)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    for index, sent in enumerate(sents):
        tts.read_to_file(text_list=[sent], file_location=output_dir + "/{}.wav".format(index))


def read_contrastive_focus_sentences(model_id, device):
    tts = InferenceFastSpeech2(device=device, model_name=model_id)

    with open("Utility/contrastive_focus_test_sentences.txt", "r", encoding="utf8") as f:
        sents = f.read().split("\n")
    output_dir = "audios/focus_{}".format(model_id)
    os.makedirs(output_dir, exist_ok=True)
    for index, sent in enumerate(sents):
        tts.read_to_file(text_list=[sent], file_location=output_dir + "/{}.wav".format(index))


if __name__ == '__main__':
    exec_device = "cuda" if torch.cuda.is_available() else "cpu"
    os.makedirs("audios", exist_ok=True)

    # sentence = "This is a sentence about a little boy, and his canoes."
    import io

    # all = io.open('rachel.txt', encoding='utf8').read().split('\n\n')
    # print(all[0])
    # read_texts(model_id="Meta", sentence=all, filename="audios/rachel.wav", device="cpu", language="en")
    import os.path
    import time
    start = time.time()
    chapters = os.listdir('Inspired')
    for i, name in enumerate(chapters):
        if name.endswith('.txt'):
            text = io.open('Inspired/' + name, encoding='utf8').read()
            mid = time.time()
            read_texts(model_id="Meta", sentence=text.split('\n'), filename="Inspired/" + name + ".wav", device="cpu", language="en")
            print(name, 'took', time.time() - mid)
            total = time.time() - mid
            per = total / (i + 1)
            print('So far', total, i, 'out of', len(chapters), per, 'per chapter', (total - i - 1) * per, 'left')
            # 394.4415681362152
    # read_texts(model_id="Meta", sentence=sentence, filename="audios/read_speech.wav", device="cpu", language="en")
    # read_texts_as_ensemble(model_id="Meta", sentence=sentence, filename="audios/read_ens", device="cpu", language="en")
    # read_harvard_sentences("Meta", "cpu")
    # read_contrastive_focus_sentences("Meta", "cpu")
