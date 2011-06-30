# import the webapp module
from google.appengine.ext import webapp
# get registry, we need it to register our filter later.
register = webapp.template.create_template_register()

def multiply(value,num):
	try:
		return int(float(value) * float(num))
	except:
		return None
register.filter(multiply)
