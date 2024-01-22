from app import *

import re
from datetime import datetime

def fmtime(t):

	return datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S")

def censor(s):

	return s[:s.find(".")] + re.sub("\d", "*", s[s.find("."):])

@app.route("/", methods=["GET"])
def index():

	return render_template("index.html")

@app.route("/manage/<uuid>", methods=["GET"])
def manage(uuid):

	if uuid != "d25d-44ff-b3aa-1bd573335cbf":
		return "NOT FOUND", 404

	hits = [(fmtime(h.timestamp), censor(h.ipAddress)) for h in Hit.query.all()][::-1]
	return render_template("manage.html", hits=hits)
