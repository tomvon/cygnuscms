import paths
import os
import cgi
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import images
import urllib, hashlib
import urllib2
import models

class GetImage(webapp.RequestHandler):
	def get(self, pageid):
		width = self.request.get('width')
		img = db.get(db.Key(pageid))
		if (img and img.file):
			self.response.headers['Content-Type'] = 'image/jpeg'
			self.response.out.write(images.get_serving_url(img.file.key(),size=200))
		else:
			self.redirect('/static/noimage.jpg')


application = webapp.WSGIApplication([(r'/images/(.*)', GetImage),],debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()