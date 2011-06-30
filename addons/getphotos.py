from google.appengine.ext import db
from google.appengine.api import urlfetch
from xml.dom import minidom
import string
import datetime
import models

def parse(url):
	r = urlfetch.fetch(url)
	if r.status_code == 200:
		return minidom.parseString(r.content)

newphotos = 0

sps = models.SiteProperties.all().fetch(1)
for sp in sps:
	flickruser = sp.flickruser
	flickrapikey = sp.flickrapikey

dom = parse('http://api.flickr.com/services/rest/?method=flickr.people.getPublicPhotos&user_id=' + flickruser + '&per_page=500&api_key=' + flickrapikey)
for ph in dom.getElementsByTagName('photo'):
	phid = ph.attributes["id"].value
	phtitle = ph.attributes["title"].value
	phurl = 'http://farm' + ph.attributes["farm"].value + '.static.flickr.com/' + ph.attributes["server"].value + '/' + ph.attributes["id"].value + '_' + ph.attributes["secret"].value
	pdom = parse('http://api.flickr.com/services/rest/?method=flickr.photos.getInfo&photo_id=' + phid + '&api_key=' + flickrapikey)
	for pd in pdom.getElementsByTagName('dates'):
		phdate =pd.attributes["taken"].value

	if (db.GqlQuery("SELECT * FROM FlickrPhoto WHERE id = :phoid", phoid=phid ).get() == None):
		newphoto = models.FlickrPhoto()
		newphoto.id = phid
		newphoto.title = phtitle
		newphoto.date = datetime.datetime.strptime(phdate,'%Y-%m-%d %H:%M:%S')
		newphoto.url = phurl
		newphoto.put()
		newphotos += 1

if newphotos > 0:
	print '<html>Added ' + str(newphotos) + ' New Flickr Photos</html>'
else:
	print '<html>No New Flickr Photos</html>'