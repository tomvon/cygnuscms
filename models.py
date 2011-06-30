from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.db import polymodel

class SiteProperties(db.Model):
	sitetitle = db.StringProperty()
	sitedescription = db.StringProperty(multiline=True)
	email = db.StringProperty()
	twitteruser = db.StringProperty()
	flickruser = db.StringProperty()
	flickrapikey = db.StringProperty()
	lastfmuser = db.StringProperty()
	lastfmapikey = db.StringProperty()
	imagesizes = db.ListProperty(str)

class Content(polymodel.PolyModel):
	title = db.StringProperty()
	pubdate = db.DateTimeProperty()
	text = db.TextProperty()
	acl = db.StringProperty()
	license = db.StringProperty()
	tags = db.ListProperty(str)
	type = db.StringProperty()
	contenttype = db.StringProperty()

class Article(Content):
	featured = db.StringProperty()
	status = db.StringProperty()
	slug = db.StringProperty()
	images = db.ListProperty(db.Key)
	media = db.ListProperty(db.Key)

class Image(Content):
	file = blobstore.BlobReferenceProperty()
	furl = db.StringProperty()
	prop = db.FloatProperty()

class Media(Content):
	file = blobstore.BlobReferenceProperty()
	fkey = db.StringProperty()

class Tweet(db.Model):
	id = db.StringProperty()
	content = db.StringProperty(multiline=True)
	date = db.DateTimeProperty()

class FlickrPhoto(db.Model):
	id = db.StringProperty()
	title = db.StringProperty()
	url = db.StringProperty()
	date = db.DateTimeProperty()