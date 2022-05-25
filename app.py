import flask

app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    text = flask.request.get_data(as_text=True)

    return text
