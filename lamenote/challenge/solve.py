import json
from flask import Flask, request, make_response, send_file

app = Flask(__name__)

@app.route("/")
def index():
    return send_file("solve.html")

@app.route("/csp")
def csp():
    r = make_response()
    r.headers['Content-Security-Policy'] = "img-src 'none';"
    return r
