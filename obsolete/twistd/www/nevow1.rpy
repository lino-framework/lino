import random
from nevow import rend, tags, loaders

class Greeter(rend.Page):
	def greet(self, context, data):
		return random.choice(["Hello", "Greetings", "Hi"]), " ",	data
		
	docFactory = loaders.stan(
		tags.html[
		tags.head[ tags.title[ "Greetings!" ]],
		tags.body[
		tags.h1(style="font-size: large")[ "Now I will greet you:" ],
		greet
		]
		])


resource = Greeter("My name is Luc.")

		
