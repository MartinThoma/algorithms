import sys
from pathlib import Path
import os

import pyttsx3 as tts  # pip install pyttsx3==2.90

engine = tts.init()

with open(sys.argv[1]) as fp:
    data = fp.read()

print(data)


# Say directly - more useful to me right now, but not so good for sharing
# the results on stack exchange
# engine.say(data)

# Store as a file so that I can share the result
out = str(Path("speech.mp3").resolve())
print(out)

print(engine.save_to_file(data, out))

engine.runAndWait()
