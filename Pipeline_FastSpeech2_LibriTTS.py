"""
Train a non-autoregressive FastSpeech 2 model on the german single speaker dataset by Hokuspokus

This requires having a trained TransformerTTS model in the right directory to knowledge distill the durations.
"""

import os
import random
import warnings

import torch

from FastSpeech2.FastSpeech2 import FastSpeech2
from FastSpeech2.FastSpeechDataset import FastSpeechDataset
from FastSpeech2.fastspeech2_train_loop import train_loop

warnings.filterwarnings("ignore")

torch.manual_seed(17)
random.seed(17)


def build_path_to_transcript_dict():
    path_train = "/mount/resources/speech/corpora/LibriTTS/train-clean-100"
    path_valid = "/mount/resources/speech/corpora/LibriTTS/dev-clean"

    path_to_transcript = dict()
    # we split training and validation differently, so we merge both folders into a single dict
    for speaker in os.listdir(path_train):
        for chapter in os.listdir(os.path.join(path_train, speaker)):
            for file in os.listdir(os.path.join(path_train, speaker, chapter)):
                if file.endswith("normalized.txt"):
                    with open(os.path.join(path_train, speaker, chapter, file), 'r',
                              encoding='utf8') as tf:
                        transcript = tf.read()
                    wav_file = file.split(".")[0] + ".wav"
                    path_to_transcript[os.path.join(path_train, speaker, chapter, wav_file)] = transcript
    for speaker in os.listdir(path_valid):
        for chapter in os.listdir(os.path.join(path_valid, speaker)):
            for file in os.listdir(os.path.join(path_valid, speaker, chapter)):
                if file.endswith("normalized.txt"):
                    with open(os.path.join(path_valid, speaker, chapter, file), 'r',
                              encoding='utf8') as tf:
                        transcript = tf.read()
                    wav_file = file.split(".")[0] + ".wav"
                    path_to_transcript[os.path.join(path_valid, speaker, chapter, wav_file)] = transcript
    return path_to_transcript


if __name__ == '__main__':
    print("Preparing")
    cache_dir = os.path.join("Corpora", "LibriTTS")
    save_dir = os.path.join("Models", "FastSpeech2", "MultiSpeaker", "LibriTTS")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    path_to_transcript_dict = build_path_to_transcript_dict()

    train_set = FastSpeechDataset(path_to_transcript_dict,
                                  train=True,
                                  acoustic_model_name="Transformer_English_Multi.pt",
                                  cache_dir=cache_dir,
                                  lang="en",
                                  min_len=0,
                                  max_len=1000000)
    valid_set = FastSpeechDataset(path_to_transcript_dict,
                                  train=False,
                                  acoustic_model_name="Transformer_English_Multi.pt",
                                  cache_dir=cache_dir,
                                  lang="en",
                                  min_len=0,
                                  max_len=1000000)

    model = FastSpeech2(idim=131, odim=80, spk_embed_dim=256)

    print("Training model")
    train_loop(net=model,
               train_dataset=train_set,
               eval_dataset=valid_set,
               device=torch.device("cpu"),
               config=model.get_conf(),
               save_directory=save_dir,
               epochs=300000,  # just kill the process at some point
               batchsize=32,
               gradient_accumulation=1,
               spemb=True)