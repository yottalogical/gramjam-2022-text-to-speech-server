## Repository Structure

| Path                    | Purpose                                                         |
| :---------------------- | :-------------------------------------------------------------- |
| `.env`                  | Environmental variables for running locally                     |
| `.flaskenv`             | Environmental variables for running locally in development mode |
| `.gitignore`            | Files to be ignored by Git                                      |
| `app.py`                | Flask app                                                       |
| `Procfile`              | Tells Heroku what to run                                        |
| `README.md`             | Information about the repository                                |
| `requirements.txt`      | Python dependencies                                             |
| `sudo-requirements.txt` | Python dependencies that must be installed as root              |
| `runtime.txt`           | Tells Heroku what version of Python to use                      |

## Server Setup

These need to be installed on your system for pyttsx3 to work.

 * [eSpeak](http://espeak.sourceforge.net/)
 * [FFmpeg](https://ffmpeg.org/)

Then install the Python dependancies:

```sh
pip3 install -r requirements.txt
sudo pip3 install -r sudo-requirements.txt
```

Set the following environmental variables to the appropriate values:

 * `AWS_ACCESS_KEY_ID`
 * `AWS_SECRET_ACCESS_KEY`

Finally run the server:

```sh
gunicorn app:app
```

## Using the API

Make an HTTP GET requests to one of the following endpoints:

 * `/text-to-speech/espeak`
 * `/text-to-speech/gtts`
 * `/text-to-speech/polly`

Use the query string key `text` for the text you want spoken. Example:

```
/text-to-speech/espeak?text=Hello+world!
```
