import time
from app import db

class Hit(db.Model):

	__tablename__ = "hits"

	id = db.Column(db.Integer, primary_key=True)
	ipAddress = db.Column(db.String(256), unique=False, nullable=False)
	timestamp = db.Column(db.Integer    , unique=False, nullable=False)

	def __init__(self, ipAddress):

		self.ipAddress = ipAddress
		self.timestamp = int(time.time())

