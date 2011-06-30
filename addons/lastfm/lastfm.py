def mytunes():

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

	lfm = 'no'

	sps = models.SiteProperties.all().fetch(1)
	for sp in sps:
		if sp.lastfmuser != '':
			lastfmuser = sp.lastfmuser
			lastfmapikey = sp.lastfmapikey
			lfm = 'yes'

	if lfm == 'yes':

		albums = []

		dom = parse('http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user=' + lastfmuser +'&period=3month&api_key=' + lastfmapikey)
		num = 0
		for mus in dom.getElementsByTagName('album'):
			if num < 9:
				muslist= []
				musname = mus.getElementsByTagName('name')[0].firstChild.data
				musurl = mus.getElementsByTagName('url')[0].firstChild.data
				muscover = mus.getElementsByTagName('image')[2].firstChild.data
				musrank = mus.attributes["rank"].value
				muspc = mus.getElementsByTagName('playcount')[0].firstChild.data
				period = '7day'
				musartist = mus.getElementsByTagName('name')[1].firstChild.data
				muslist.append(musname)
				muslist.append(musurl)
				muslist.append(muscover)
				muslist.append(musrank)
				muslist.append(muspc)
				muslist.append(period)
				muslist.append(musartist)
				albums.append(muslist)
				num += 1

	else:

		albums = ["","","You need to enter a Last.fm username and API Key to display recently scrobbled tracks.","","","","",""]

	return albums