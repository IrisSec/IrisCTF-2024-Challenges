from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/<path:filename>")
def serve_file(filename):
    return send_from_directory("site", filename)

@app.route("/")
def index():
    return send_from_directory("site", "website.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337)