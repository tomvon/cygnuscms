import paths
import os
import cgi
import string
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
import random
import urllib, hashlib
import urllib2
import lastfm
import models

webapp.template.register_template_library('django_extensions.extensions')

themeid = 'cygnus'

class BaseRequestHandler(webapp.RequestHandler):
	def generate(self, template_name, template_values={}):

		user = users.get_current_user()
		is_admin = users.is_current_user_admin()
		if user:
			log_in_out_url = users.create_logout_url(self.request.path)
		else:
			log_in_out_url = users.create_login_url(self.request.path)
		log_in_out_url = cgi.escape(log_in_out_url)

		sps = models.SiteProperties.all().fetch(1)
		if len(sps) > 0:
			for sp in sps:
				if sp.email != '':
					email = sp.email
				else:
					email = 'test@gravatar.com'
			gremail = email
			grdefault = ""
			grsize = 40
			gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(gremail.lower()).hexdigest() + "?"
			gravatar_url += urllib.urlencode({'d':grdefault, 's':str(grsize)})
			sitetitle = sp.sitetitle
			sitedescription = sp.sitedescription
		else:
			sitetitle = 'CygnusCMS'
			sitedescription ='A CygnusCMS Website.'
			gravatar_url = '/themes/' + themeid + '/static/images/gravatar.png'

		mphotos = models.FlickrPhoto.all().order('-date').fetch(8)
		if len(mphotos) > 0:
			random.shuffle(mphotos)
			mphoto = mphotos[0]
		else:
			mphoto = ''

		values = {
			'themeid' : themeid,
			'user': user,
			'log_in_out_url': log_in_out_url,
			'is_admin' : is_admin,
			'gravatar': gravatar_url,
			'mphoto': mphoto,
			'sitetitle': sitetitle,
			'sitedescription': sitedescription,
			}
		values.update(template_values)
		directory = os.path.dirname(__file__)
		path = os.path.join(directory, 'themes/' + themeid, template_name)
		self.response.out.write(template.render(path, values))


class MainPage(BaseRequestHandler):
	def get(self):

		articles = models.Article.all().order('-pubdate').fetch(9)
		for article in articles:
			article.rimages = [db.get(image) for image in article.images]

		tweets = models.Tweet.all().order('-date').fetch(6)
		flickrphotos = models.FlickrPhoto.all().order('-date').fetch(6)

		self.generate('index.html',
			template_values = {
				'articles' : articles,
				'tweets' : tweets,
				'flickrphotos' : flickrphotos,
				})


"""class MainPage(BaseRequestHandler):
	def get(self):

		tweets = models.Tweet.all().order('-date').fetch(18)
		photos = models.FlickrPhoto.all().order('-date').fetch(500)
		random.shuffle(photos)
		photos = photos[0:27]

		mytunes = memcache.get("mytunes")
		if mytunes is not None:
			albums = mytunes
		else:
			mytunes = lastfm.mytunes()
			memcache.add(key="mytunes", value=mytunes, time=900)
			albums = lastfm.mytunes()

		self.generate('index.html',
			template_values = {
				'tweets': tweets,
				'photos': photos,
				'albums': albums,
				})"""

class BrowseHandler(BaseRequestHandler):

	def get(self, pageid):

		articles = models.Article.all()
		articles.filter("slug =", pageid)
		article = articles.fetch(1)
		for art in article:
			rimages = []
			rheights = []
			for image in art.images:
				rimages.append(db.get(image))
				img = images.Image(blob_key=str(db.get(image).file.key()))
				img.im_feeling_lucky()
				img.execute_transforms(output_encoding=images.JPEG,quality=1)
				rheights.append(float(img.height) / float(img.width))
			art.rimages = rimages

		articles = models.Article.all().order('-pubdate').fetch(20)
		for sarticle in articles:
			sarticle.rimages = [db.get(image) for image in sarticle.images]

		self.generate('page.html',
			template_values = {
				'articles' : articles,
				'article' : article,
				'rheights' : rheights,
				'pageid': pageid,
				})

class PhotoHandler(BaseRequestHandler):

	def get(self, pageid):

		pageid = urllib2.unquote(pageid)

		tweets = models.Tweet.all().order('-date').fetch(18)
		photos = db.GqlQuery("SELECT * FROM Photo WHERE title = :1", pageid)

		self.generate('photos.html',
			template_values = {
				'tweets': tweets,
				'pageid': pageid,
				'photos': photos,
				})


class FileHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info, save_as=True)


application = webapp.WSGIApplication(
									 [
									 ('/', MainPage),
									 (r'/page/(.*)', BrowseHandler),
									 (r'/file/(.*)', FileHandler),
									 (r'/photos/(.*)', PhotoHandler),
									 ],
									 debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
