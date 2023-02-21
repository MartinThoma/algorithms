import sys
from gtts import gTTS  # pip install gtts

with open(sys.argv[1]) as fp:
    text = fp.read()

print(text)

tts = gTTS(text=text, lang="en")
filename = "gtts-text.mp3"
tts.save(filename)
