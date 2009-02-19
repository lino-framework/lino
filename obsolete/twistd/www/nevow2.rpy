from formless.annotate import TypedInterface, Integer, String

class ISimpleMethod(TypedInterface):
	def simple(self,
				  name=String(description="Your name."),
				  age=Integer(description="Your age.")):
		"""Simple
		
		Please enter your name and age.
		"""

class Implementation(object):
	__implements__ = ISimpleMethod,
	
	def simple(self, name, age):
		print "Hello, %s, you are %s years old." % (name, age)


from nevow import rend, tags, loaders
from formless import webform

class WebForm(rend.Page):
	docFactory = loaders.stan(
		tags.html[
		tags.body[
		tags.h1["Here is the form:"],
		webform.renderForms('original')
		]
		])
	
resource = WebForm(Implementation()) 
															  
