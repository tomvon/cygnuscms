from google.appengine.ext import db
from google.appengine.api import urlfetch
from xml.dom import minidom
import string
import datetime
import models

def convertlinks(input):
	input = string.split(input,' ')
	for lnk in input:
		if string.find(lnk, 'http://') > -1:
			pos = input.index(lnk)
			lnksm = lnk[:25]
			cleanlnk = string.replace(lnk,'(','')
			cleanlnk = string.replace(cleanlnk,')','')
			if len(lnk) > 25:
			  newlnk = '<a href="' + cleanlnk + '" target="_blank">' + lnksm + '...</a>'
			else:
			  newlnk = '<a href="' + cleanlnk + '" target="_blank">' + lnksm + '</a>'
			input = list(input)
			input.remove(lnk)
			input.insert(pos,newlnk)
	input = ' '.join(input)
	return input

def parse(url):
	r = urlfetch.fetch(url)
	if r.status_code == 200:
		return minidom.parseString(r.content)

newtweets = 0

sps = models.SiteProperties.all().fetch(1)
for sp in sps:
	twitteruser = sp.twitteruser

dom = parse('http://twitter.com/statuses/user_timeline.xml?screen_name=' + twitteruser)
for tw in dom.getElementsByTagName('status'):
	ttext = convertlinks(tw.getElementsByTagName('text')[0].firstChild.data)
	tid = tw.getElementsByTagName('id')[0].firstChild.data
	tdate = tw.getElementsByTagName('created_at')[0].firstChild.data
	if (db.GqlQuery("SELECT * FROM Tweet WHERE id = :twid", twid=tid ).get() == None):
		newtweet = models.Tweet()
		newtweet.id = tid
		newtweet.date = datetime.datetime.strptime(string.replace(tdate,' +0000',''),'%a %b %d %H:%M:%S %Y')
		newtweet.content = ttext
		newtweet.put()
		newtweets += 1

if newtweets > 0:
	print '<html>Added ' + str(newtweets) + ' New Tweets</html>'
else:
	print '<html>No New Tweets</html>'