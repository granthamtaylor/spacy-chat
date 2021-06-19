import os
import json
import re

from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, request
from flask_socketio import SocketIO

from formatters.manage import format_message
from classifiers.manage import Engine

# set current working directory
PATH = os.path.dirname(os.path.realpath(__file__))

# initiate application
app = Flask(__name__)
socket = SocketIO(app)

# load ML models
toxic = Engine("toxic")
emotion = Engine("emotion")

def respond(message):

    """
    returns a response with outputs from the machine learning
    models and the Spacy formatter
    """

    return {
        "tokens": format_message(message),
        "emotion": emotion.predict(message),
        "toxic": toxic.predict(message),
    }

@app.route("/")
def index():

    """initialize chatbot page"""

    global MESSAGES

    return render_template("index.html", messages=MESSAGES)

@socket.on("transmit-user-input")
def update(message):

    """update chatbox with message and its appropriate response"""

    # if message of expected pattern (to prevent XSS)
    pattern = re.compile(r"([^\s][A-z0-9À-ž\s @:;_.,?!&quot;'/$]+)")
    if pattern.match(message):

        # render html response and emit back via socket
        response = template.render(message=respond(message))
        socket.emit("transmit-spacy-tokens", response, room=request.sid)

if __name__ == "__main__":

    # load and process initial messages.
    with open(os.path.join(PATH, "static", "intro.json")) as file:
        MESSAGES = [respond(message) for message in json.loads(file.read())]

    # load Jinja message template for outgoing responses
    templates = os.path.join(PATH, "templates")
    with open(os.path.join(templates, "outgoing.html")) as f:
        template_str = f.read()
        template = Environment(loader=FileSystemLoader(templates)).from_string(template_str)

    socket.run(app, debug=True, host="0.0.0.0")
