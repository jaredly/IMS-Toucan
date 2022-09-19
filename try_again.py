
import TTS
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
from pathlib import Path

def ok():
    # load model manager
    path = Path(TTS.__file__).parent / ".models.json"
    manager = ModelManager(path)

    model_name = "tts_models/en/ljspeech/tacotron2-DDC"
    model_path = None
    config_path = None
    speakers_file_path = None
    language_ids_file_path = None
    vocoder_path = None
    vocoder_config_path = None
    encoder_path = None
    encoder_config_path = None

    # # CASE3: load pre-trained model paths
    # if args.model_name is not None and not args.model_path:
    model_path, config_path, model_item = manager.download_model(model_name)
    vocoder_name = model_item["default_vocoder"]

    # if vocoder_name is not None and not vocoder_path:
    vocoder_path, vocoder_config_path, _ = manager.download_model(vocoder_name)

    # # CASE4: set custom model paths
    # if args.model_path is not None:
    #     model_path = args.model_path
    #     config_path = args.config_path
    #     speakers_file_path = args.speakers_file_path
    #     language_ids_file_path = args.language_ids_file_path

    # if args.vocoder_path is not None:
    #     vocoder_path = args.vocoder_path
    #     vocoder_config_path = args.vocoder_config_path

    # if args.encoder_path is not None:
    #     encoder_path = args.encoder_path
    #     encoder_config_path = args.encoder_config_path

    # load models
    synthesizer = Synthesizer(
        model_path,
        config_path,
        speakers_file_path,
        language_ids_file_path,
        vocoder_path,
        vocoder_config_path,
        encoder_path,
        encoder_config_path,
        False,
    )

    text = open('/Users/jared/Downloads/Arbitrary Lines/01_aip01.txt', encoding='utf8').read()

    # kick it
    wav = synthesizer.tts(
        text,
        None,
        None,
        None,
        reference_wav=None,
        style_wav=None,
        style_text=None,
        reference_speaker_name=None,
    )
    synthesizer.save_wav(wav, "done.wav")

ok()