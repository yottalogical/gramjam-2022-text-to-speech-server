import flask
import pyttsx3
import random
import string
import pathlib
import time

app = flask.Flask(__name__)


@app.route('/text-to-speech', methods=['GET'])
def index():
    text = flask.request.args['text']
    filepath = text_to_speech(text)

    return flask.send_file(
        filepath,
        as_attachment=True,
        attachment_filename='speech.mp3',
        mimetype='audio/mpeg'
    )


def text_to_speech(text: str) -> pathlib.Path:
    engine: pyttsx3.Engine = pyttsx3.init()

    random_str = ''.join(random.choice(string.ascii_lowercase)
                         for _ in range(32))
    filepath = pathlib.Path('/') / 'tmp' / f'{random_str}.mp3'

    engine.save_to_file(text, filepath)
    engine.runAndWait()

    time.sleep(0.05)

    return filepath
