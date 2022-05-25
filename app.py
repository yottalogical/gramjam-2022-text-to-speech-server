import flask
import gtts
import io

app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    text = flask.request.get_data(as_text=True)

    return text_to_speech(text)


def text_to_speech(text: str) -> bytes:
    audio = io.BytesIO()

    tts = gtts.gTTS(text)
    tts.write_to_fp(audio)

    return audio.getvalue()
