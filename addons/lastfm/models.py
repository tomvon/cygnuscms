from google.appengine.ext import db

class LastfmMeta(db.Model):
	lfmusername = db.StringProperty()
	lfmapikey = db.StringProperty()
	lfmmethod = db.StringProperty()
	lfmvariable = db.StringProperty()