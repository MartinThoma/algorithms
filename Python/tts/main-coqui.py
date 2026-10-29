import sys

from TTS.api import TTS  # pip install TTS


def get_text() -> str:
    with open(sys.argv[1]) as fp:
        text = fp.read()
    text = text.replace("”", '"').replace("“", '"')
    return text


def gen(model_name: str, text: str, out_file: str) -> None:
    # Init TTS with the target model name
    tts = TTS(model_name=model_name, progress_bar=False, gpu=False)
    print("#" * 80)
    print(f"model={model_name}")
    print(f"speakers={tts.speakers}")
    print(f"languages={tts.languages}")
    speaker = None
    if tts.speakers is not None:
        speaker = tts.speakers[0]

    # Select language and speaker
    if speaker == "":
        speaker = None
    language = None
    if tts.languages:
        language = "en"

    # Generate it!
    tts.tts_to_file(text=text, speaker=speaker, language=language, file_path=out_file)


if __name__ == "__main__":
    model_name = "tts_models/multilingual/multi-dataset/your_tts"
    speaker = ""
    if len(sys.argv) < 3:
        out_file = f"coqui.wav"
    else:
        out_file = sys.argv[2]
    # if you want to see which models are available: TTS.list_models()
    gen(model_name=model_name, text=get_text(), out_file=out_file)
