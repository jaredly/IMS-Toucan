import sys
import TTS
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
from pathlib import Path
import json
import time
import os.path

path = Path(TTS.__file__).parent / ".models.json"
manager = ModelManager(path)

def load_model(model_name):
    # model_path = None
    # config_path = None
    speakers_file_path = None
    language_ids_file_path = None

    # # CASE3: load pre-trained model paths
    # if args.model_name is not None and not args.model_path:
    model_path, config_path, model_item = manager.download_model(model_name)
    vocoder_name = model_item["default_vocoder"]

    print(f"Downloading vocoder: {vocoder_name} ...")
    # if not vocoder_name:
    #     vocoder_name = "vocoder_models/en/ljspeech/hifigan_v2"
    #     print("No default vocoder found, using hifigan_v2")
    #     # return None
    vocoder_path = None
    vocoder_config_path = None

    if vocoder_name is not None:
        vocoder_path, vocoder_config_path, _ = manager.download_model(vocoder_name)

    # load models
    return Synthesizer(
        model_path,
        config_path,
        # None,
        # None,
        vocoder_checkpoint = vocoder_path,
        vocoder_config = vocoder_config_path,
        # None,
        # None,
        # False,
        # use_cuda=True
    )

def run_model(model_name, out_wav, text, speaker_name_idx=0):
    synthesizer = load_model(model_name)

    speaker_name = None
    if hasattr(synthesizer.tts_model.speaker_manager, 'ids'):
        print(list(synthesizer.tts_model.speaker_manager.ids.keys()))
        speaker_name = list(synthesizer.tts_model.speaker_manager.ids.keys())[speaker_name_idx]
        print(f"Speaker {speaker_name}")

    before = time.time()
    wav = synthesizer.tts(
        text,
        speaker_name, # speaker_name
        None, # language_name
        None, # speaker_wav
    )
    synthesizer.save_wav(wav, out_wav)
    after = time.time()
    return after - before

def clone_maybe():
    synthesizer = load_model('tts_models/multilingual/multi-dataset/your_tts')
    before = time.time()
    text = 'Thank you for coming to my impromptu party. We have cookies, soda, and unusually ephemeral card games.'
    wav = synthesizer.tts(
        text,
        None, # speaker_name
        "en", # language_name
        "nelson/all.wav", # speaker_wav
    )
    synthesizer.save_wav(wav, 'nelson/your_tts.wav')
    after = time.time()
    return after - before

def ok():
    if len(sys.argv) > 2:
        model_name = sys.argv[2]
    else:
        model_name = "tts_models/en/ljspeech/tacotron2-DDC"

    out_wav = sys.argv[1]

    # text = open('/Users/jared/Downloads/Arbitrary Lines/01_aip01.txt', encoding='utf8').read()
    text = 'Thank you for coming to my impromptu party. We have cookies, soda, and unusually ephemeral card games.'

    run_model(model_name, out_wav, text)

def all_alice():
    # load model manager
    models = json.load(open(path))

    base = 'alice_1p'
    text = open('./alice.txt', encoding='utf8').read().split('\n')[0]

    os.makedirs(base, exist_ok=True)
    # text = 'Thank you for coming to my impromptu party. We have cookies, soda, and unusually ephemeral card games.'
    # text = 'Thank you for coming.'
    times = open(f'./{base}/times.txt', 'a')

    for (model_name, subs) in models['tts_models']['en'].items():
        if model_name == 'ek1' or model_name == 'sam':
            continue # ek1 takes wayyyy too long and sam is just bad
        for sub in subs.keys():
            full = f"tts_models/en/{model_name}/{sub}"
            out = f"{base}/{model_name}_{sub}.wav"
            if os.path.exists(out):
                continue
            print(full)
            synth = load_model(full)
            if hasattr(synth.tts_model.speaker_manager, 'ids'):
                for i, speaker_name in list(enumerate(synth.tts_model.speaker_manager.ids.keys()))[:10]:
                    outt = out + '_' + str(i) + '.wav'
                    if os.path.exists(outt):
                        continue
                    time = run_model(full, outt, text, i)
                    print(time)
                    times.write(f"{full} {i} {time}\n")
                    times.flush()
            time = run_model(full, out, text)
            print(time)
            times.write(f"{full} {time}\n")
            times.flush()

# ok()
# all_alice()
clone_maybe()