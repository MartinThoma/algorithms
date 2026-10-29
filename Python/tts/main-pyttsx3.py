import sys
from pathlib import Path

import pyttsx3 as tts  # pip install pyttsx3==2.90

# Get the data
with open(sys.argv[1]) as fp:
    data = fp.read()
print(data)

engine = tts.init()

# engine.say(data)  # say it directly
engine.save_to_file(data, Path(sys.argv[2]).resolve())  # store to file

engine.runAndWait()
