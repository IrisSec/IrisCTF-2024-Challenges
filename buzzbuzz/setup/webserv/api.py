from app import *

from uuid import uuid4
import time

@app.route("/trigger", methods=["POST"])
def trigger():

	db.session.add(Hit(request.json["address"]))
	db.session.commit()
	return {}, 200

@app.route("/make", methods=["POST"])
def make():

	#return str(uuid4()), 200
	return "", 503

