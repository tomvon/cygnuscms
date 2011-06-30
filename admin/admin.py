import cgi
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from datetime import datetime
from google.appengine.api import images
import string
import re
import models
import getmime


class BaseRequestHandler(webapp.RequestHandler):
	def generate(self, template_name, template_values={}):

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		user = users.get_current_user()
		nickname = user.nickname()

		msg = self.request.get('msg')

		sps = models.SiteProperties.all().fetch(1)
		if len(sps) > 0:
			for sp in sps:
				sitetitle = sp.sitetitle
		else:
			sitetitle = 'A CygnusCMS Site'

		if template_name == 'imageform.html':
			upload_url = blobstore.create_upload_url('/admin/manageimages')
		elif template_name == 'mediaform.html':
			upload_url = blobstore.create_upload_url('/admin/managemedia')
		else:
			upload_url = ''

		values = {
			'url': url,
			'url_linktext': url_linktext,
			'nickname': nickname,
			'msg' : msg,
			'sitetitle' : sitetitle,
			'upload_url' : upload_url
			}

		values.update(template_values)
		directory = os.path.dirname(__file__)
		path = os.path.join(directory, 'theme', template_name)
		self.response.out.write(template.render(path, values))


def adminlist(self,allcontent,page):

	more = 'no'
	start = self.request.get('start')
	if start:
		content = allcontent.fetch(10,int(start))
		nextcontent = allcontent.fetch(10,int(start) + 10)
		if len(nextcontent) > 0:
			more = 'yes'
	else:
		content = allcontent.fetch(10)
		nextcontent = allcontent.fetch(10,10)
		if len(nextcontent) > 0:
			more = 'yes'

	self.generate(page,
		template_values = {
			'content': content,
			'start' : start,
			'more' : more
			})


class MainPage(BaseRequestHandler):
	def get(self):

		allcontent = models.Article.all().order("-pubdate")
		adminlist(self,allcontent,'index.html')


class ManageExtend(BaseRequestHandler):
	def get(self):

		self.generate('extend.html',
			template_values = {
				})


class ImageForm(BaseRequestHandler):
	def get(self):

		allcontent = models.Image.all().order("-pubdate")
		adminlist(self,allcontent,'imageform.html')


class MediaForm(BaseRequestHandler):
	def get(self):

		allcontent = models.Media.all().order("-pubdate")
		adminlist(self,allcontent,'mediaform.html')

class TweetsForm(BaseRequestHandler):
	def get(self):

		allcontent = models.Tweet.all().order("-date")
		adminlist(self,allcontent,'tweetform.html')

class FlickrForm(BaseRequestHandler):
	def get(self):

		allcontent = models.FlickrPhoto.all().order("-date")
		adminlist(self,allcontent,'flickrform.html')


class ManageSiteProperties(BaseRequestHandler):
	def get(self):

		sps = models.SiteProperties.all().fetch(1)
		if len(sps) > 0:
			for sp in sps:
				sitetitle = sp.sitetitle
				sitedescription = sp.sitedescription
				email = sp.email
				twitteruser = sp.twitteruser
				flickruser = sp.flickruser
				flickrapikey = sp.flickrapikey
				lastfmuser = sp.lastfmuser
				lastfmapikey = sp.lastfmapikey
		else:
			sitetitle = ''
			sitedescription =''
			email =''
			twitteruser = ''
			flickruser = ''
			flickrapikey = ''
			lastfmuser = ''
			lastfmapikey = ''

		self.generate('properties.html',
			template_values = {
				'sitetitle': sitetitle,
				'sitedescription' : sitedescription,
				'twitteruser' : twitteruser,
				'flickruser' : flickruser,
				'flickrapikey' : flickrapikey,
				'lastfmuser' : lastfmuser,
				'lastfmapikey' : lastfmapikey,
				'email' : email,
				})


class UpdateSiteProperties(webapp.RequestHandler):
	def post(self):

		def updatesp(sp):
			sp.sitetitle = self.request.get('sitetitle')
			sp.sitedescription = self.request.get('sitedescription')
			sp.twitteruser = self.request.get('twitteruser')
			sp.flickruser = self.request.get('flickruser')
			sp.flickrapikey = self.request.get('flickrapikey')
			sp.lastfmuser = self.request.get('lastfmuser')
			sp.lastfmapikey = self.request.get('lastfmapikey')
			sp.email = self.request.get('email')
			return sp

		sps = models.SiteProperties.all().fetch(1)
		if len(sps) > 0:
			for sp in sps:
				updatesp(sp)
				db.put(sp)
				self.redirect('/admin/siteproperties?msg=Site Properties Updated')
		else:
			sp = models.SiteProperties()
			updatesp(sp)
			sp.put()
			self.redirect('/admin/siteproperties?msg=Site Properties Updated')


class EditContent(BaseRequestHandler):
	def get(self):

		ekey = self.request.get('ekey')

		c = db.get(db.Key(ekey))

		#Global Properties
		title = c.title
		text = c.text
		pubdate = c.pubdate
		acl = c.acl
		license = c.license
		tags = c.tags
		type = c.type
		contenttype = c.contenttype

		featured = ''
		status = ''
		text = ''
		images = ''
		media = ''
		furl = ''
		file = ''
		filename = ''
		filesize = ''
		rimages = ''

		if type == 'article':
			featured = c.featured
			status = c.status
			text = c.text
			for image in c.images:
				images += str(image) + ','
			rimages = [db.get(image) for image in c.images]
			media = c.media

		elif type == 'image':
			featured = 'no'
			status = 'published'
			furl = c.furl

		elif type == 'media':
			featured = 'no'
			status = 'published'
			file = c.file.key()
			filename = c.fkey
			contenttype = blobstore.BlobInfo(file).content_type
			filesize = blobstore.BlobInfo(file).size
			filesize = filesize / 1000
			if filesize > 1000:
				filesize = str(float(filesize / 1000)) + 'MB'
			else:
				filesize = str(filesize) + 'K'

		if type == 'article':
			page = 'index.html'
		elif type == 'media':
			page = 'mediaform.html'
		elif type == 'image':
			page = 'imageform.html'

		self.generate(page,
			template_values = {
				'ekey' : ekey,
				'title' : title,
				'text' : text,
				'images' : images,
				'rimages' : rimages,
				'media' : media,
				'pubdate' : pubdate,
				'featured' : featured,
				'status' : status,
				'acl' : acl,
				'license' : license,
				'tags' : tags,
				'type' : type,
				'file' : file,
				'filename' : filename,
				'filesize' : filesize,
				'furl' : furl,
				'contenttype' : contenttype,
				})


class ManageArticle(BaseRequestHandler):
	def post(self):

		def slugify(string):
			string = re.sub('\s+', '-', string)
			string = re.sub('[^\w.-]', '', string)
			return string.strip('_.- ').lower()

		def slugcheck(slug):
			currentarticles = models.Article.all()
			for article in currentarticles:
				if slug == article.slug:
					try:
						newnum = int(slug[-1]) + 1
						slug = slug[:-1] + str(newnum)
					except:
						slug = slug + '-2'
			return slug

		ekey = self.request.get('ekey')
		if ekey != 'new':
			c = db.get(db.Key(ekey))
		else:
			c = models.Article()
			c.slug = slugify(self.request.get('title'))
			c.slug = slugcheck(c.slug)

		# Global Properties
		c.title = self.request.get('title')
		c.pubdate = datetime.strptime(self.request.get('pubdate'), '%b %d %Y %I:%M %p')
		c.acl = self.request.get('acl')
		c.license = self.request.get('license')
		tags = string.split(string.replace(self.request.get('tags'),', ',','),',')
		c.type = self.request.get('type')
		cleantags = []
		for tag in tags:
			if tag != '':
				cleantags.append(string.strip(tag))
		c.tags = cleantags
		c.type = self.request.get('type')
		c.contenttype = self.request.get('content-type')

		c.featuredimage = self.request.get('featuredimage')
		c.featured = self.request.get('featured')
		c.status = self.request.get('status')
		c.text = self.request.get('text')

		if self.request.get('images') != '':
			images = string.split(self.request.get('images'),',')
			ikeys  = []
			for imagekey in images:
				if imagekey != '':
					i = models.Image(key=imagekey)
					ikeys.append(i.key())
					c.images = ikeys
		else:
			c.images = []

		media = string.split(self.request.get('media'),',')
		#for med in media:
		#	c.media = db.Key(med)

		db.put(c)

		if ekey != 'new':
			self.redirect('/admin/editcontent?ekey=' + ekey + '&msg=' + c.title + ' Edited')
		else:
			self.redirect('/admin?msg=' + c.title + ' Added')


class ManageMedia(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):

		def process(self, ufile):

			ekey = self.request.get('ekey')
			if ekey != 'new':
				c = db.get(db.Key(ekey))
			else:
				c = models.Media()

			# Global Properties
			c.title = self.request.get('title')
			c.pubdate = datetime.strptime(self.request.get('pubdate'), '%b %d %Y %I:%M %p')
			c.text = self.request.get('text')
			c.acl = self.request.get('acl')
			c.license = self.request.get('license')
			tags = string.split(string.replace(self.request.get('tags'),', ',','),',')
			c.type = self.request.get('type')
			cleantags = []
			for tag in tags:
				if tag != '':
					cleantags.append(string.strip(tag))
			c.tags = cleantags
			c.type = self.request.get('type')
			c.contenttype = self.request.get('content-type')

			c.fkey = self.request.get('key')
			if ufile != 'exist':
				c.file = ufile.key()

			db.put(c)

			if ekey != 'new':
				self.redirect('/admin/editcontent?ekey=' + ekey + '&msg=' + c.title + ' Edited')
			else:
				self.redirect('/admin/mediaform?msg=' + c.title + ' Added')

		upload_files = self.get_uploads('file')
		if len(upload_files) > 0:
			for ufile in upload_files:
				process(self, ufile)
		else:
			process(self, 'exist')


class ManageImages(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):

		def process(self, ufile):

			ekey = self.request.get('ekey')
			if ekey != 'new':
				c = db.get(db.Key(ekey))
			else:
				c = models.Image()

			# Global Properties
			c.title = self.request.get('title')
			c.pubdate = datetime.strptime(self.request.get('pubdate'), '%b %d %Y %I:%M %p')
			c.text = self.request.get('text')
			c.acl = self.request.get('acl')
			c.license = self.request.get('license')
			tags = string.split(string.replace(self.request.get('tags'),', ',','),',')
			c.type = self.request.get('type')
			cleantags = []
			for tag in tags:
				if tag != '':
					cleantags.append(string.strip(tag))
			c.tags = cleantags
			c.type = self.request.get('type')
			c.contenttype = self.request.get('content-type')

			if ufile != 'exist':
				c.file = ufile.key()
				c.furl = images.get_serving_url(str(ufile.key()))
				img = images.Image(blob_key=str(ufile.key()
				))
				img.im_feeling_lucky()
				img.execute_transforms(output_encoding=images.JPEG,quality=1)
				c.prop = float(img.height) / float(img.width)
			c.fkey = self.request.get('key')

			db.put(c)

			if ekey != 'new':
				self.redirect('/admin/editcontent?ekey=' + ekey + '&msg=' + c.title + ' Edited')
			else:
				self.redirect('/admin/imageform?msg=' + c.title + ' Added')

		upload_files = self.get_uploads('file')
		if len(upload_files) > 0:
			for ufile in upload_files:
				process(self, ufile)
		else:
			process(self, 'exist')


class BrowseImages(BaseRequestHandler):
	def get(self):

		images = models.Image().all()

		self.generate('browseimages.html',
			template_values = {
				'images': images,
				})


class Delete(webapp.RequestHandler):
	def get(self):
		ekey = self.request.get('ekey')
		type = self.request.get('type')
		title = self.request.get('title')
		c = db.get(db.Key(ekey))
		if type == 'image':
			try:
				img = blobstore.BlobInfo.get(c.file.key())
				img.delete()
			except:
				pass
		db.delete(c)
		if type == 'image':
			self.redirect('/admin/imageform?msg=' + title + ' Deleted')
		if type == 'article':
			self.redirect('/admin?msg=' + title + ' Deleted')
		if type == 'tweet':
			self.redirect('/admin/tweetsform?msg=' + title + ' Deleted')
		if type == 'flickr':
			self.redirect('/admin/flickrform?msg=' + title + ' Deleted')

class GetMime(webapp.RequestHandler):
	def get(self):

		fileid = self.request.get('fileid')
		mimetype = getmime.find(fileid)
		self.response.out.write(mimetype)


application = webapp.WSGIApplication(
									[('/admin', MainPage),
									('/admin/editcontent', EditContent),
									('/admin/managearticle', ManageArticle),
									('/admin/imageform', ImageForm),
									('/admin/manageimages', ManageImages),
									('/admin/browseimages', BrowseImages),
									('/admin/mediaform', MediaForm),
									('/admin/tweetsform', TweetsForm),
									('/admin/flickrform', FlickrForm),
									('/admin/managemedia', ManageMedia),
									('/admin/delete', Delete),
									('/admin/extend', ManageExtend),
									('/admin/siteproperties', ManageSiteProperties),
									('/admin/updateproperties', UpdateSiteProperties),
									('/admin/getmime', GetMime),
									],
									debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
