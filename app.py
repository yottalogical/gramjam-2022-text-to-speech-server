import flask
import pyttsx3
import random
import string
import pathlib
import time

app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    text = flask.request.get_data(as_text=True)
    filepath = text_to_speech(text)

    time.sleep(0.05)

    return flask.send_file(filepath)


def text_to_speech(text: str) -> pathlib.Path:
    engine: pyttsx3.Engine = pyttsx3.init()

    random_str = ''.join(random.choice(string.ascii_lowercase)
                         for _ in range(32))
    filepath = pathlib.Path('/') / 'tmp' / f'{random_str}.mp3'

    engine.save_to_file(text, filepath)
    engine.runAndWait()

    return filepath
