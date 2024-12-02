from flask import Flask

app = Flask(__name__)

@app.route("/")
def BlauweBagger():
    return "<p>Blauwe Bagger</p>"
