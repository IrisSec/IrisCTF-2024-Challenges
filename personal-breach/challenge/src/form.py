import random
import time

from app import *

# Make these in lowercase please.
ANSWER_KEY = {
	"q1": ["27", "twenty seven", "twenty-seven"],
	"q2": ["lenox hill hospital"],
	"q3": ["mountain peak hiring agency"],
}

FLAG = "irisctf{s0c1al_m3d1a_1s_an_1nf3cti0n}"

# Delay just discourages someone from sitting down and bruting every possible
# number for the age question. It isn't protection, just deterrence.
DELAY_A = 2
DELAY_B = 5

@app.route("/", methods=["GET"])
def index():

	return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():

	time.sleep(random.uniform(DELAY_A, DELAY_B))

	try:
		response = {
			"q1": request.json["q1"].lower().strip() in ANSWER_KEY["q1"],
			"q2": request.json["q2"].lower().strip() in ANSWER_KEY["q2"],
			"q3": request.json["q3"].lower().strip() in ANSWER_KEY["q3"],
		}

		if response == {"q1": True, "q2": True, "q3": True}:
			response["flag"] = FLAG
		else:
			response["flag"] = "Not quite. Try again."

		return response, 200
	except:
		return {
			"q1": False, "q2": False, "q3": False,
		}, 400

