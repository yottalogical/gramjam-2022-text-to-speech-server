import flask
import pyttsx3
import random
import string
import pathlib
import gtts
import io
import os
import boto3
import inotify.adapters

app = flask.Flask(__name__)


@app.route('/text-to-speech/espeak', methods=['GET'])
def text_to_speech_espeak():
    text = flask.request.args['text']

    random_str = ''.join(random.choice(string.ascii_lowercase)
                         for _ in range(32))
    filepath = pathlib.Path('/') / 'tmp' / f'gram-jam-server-{random_str}.mp3'

    waiter = FileWaiter(filepath)
    engine: pyttsx3.Engine = pyttsx3.init()
    engine.save_to_file(text, filepath)
    engine.runAndWait()
    waiter.wait()

    return flask.send_file(
        filepath,
        as_attachment=True,
        attachment_filename='speech.mp3',
        mimetype='audio/mpeg'
    )


@app.route('/text-to-speech/gtts', methods=['GET'])
def text_to_speech_gtts():
    text = flask.request.args['text']

    audio = io.BytesIO()

    tts = gtts.gTTS(text)
    tts.write_to_fp(audio)

    audio.seek(0)
    return flask.send_file(
        audio,
        as_attachment=True,
        attachment_filename='speech.mp3',
        mimetype='audio/mpeg'
    )


session = boto3.Session(
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name='us-west-2'
)

polly = session.client('polly')


@app.route('/text-to-speech/polly', methods=['GET'])
def text_to_speech_polly():
    response = polly.synthesize_speech(
        Text=flask.request.args['text'],
        OutputFormat='mp3',
        VoiceId='Joanna'
    )

    return flask.send_file(
        io.BytesIO(response['AudioStream'].read()),
        as_attachment=True,
        attachment_filename='speech.mp3',
        mimetype='audio/mpeg'
    )


class FileWaiter:
    def __init__(self, filepath: pathlib.Path):
        self.inotifier = inotify.adapters.Inotify()
        self.inotifier.add_watch(str(filepath))

    def wait(self):
        for event in self.inotifier.event_gen(yield_nones=False):
            _, event_types, _, _ = event

            if 'IN_CLOSE_WRITE' in event_types:
                return
