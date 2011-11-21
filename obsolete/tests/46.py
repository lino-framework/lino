# coding: latin1

"""
openmail
"""
import unittest

from lino.tools.mail import readmail, mailto_url

class Case(unittest.TestCase):

	def test01(self):
		""
		self.assertEqual(
			mailto_url(to="fritz.eierschale@lummerland.org"),
			"mailto:fritz.eierschale@lummerland.org"
			)
	def test02(self):
		self.assertEqual(
			mailto_url(to="eierschale@irgend.wo",
						  cc="heidi.bratze@vergiss.es"),
			"mailto:eierschale@irgend.wo?cc=heidi.bratze@vergiss.es"
			)
	def test03(self):
		self.assertEqual(
			mailto_url(to="eierschale@irgend.wo",
						  subject="eine Mail von deinen Web-Seiten"),
			"mailto:eierschale@irgend.wo?subject=eine%20Mail%20von%20deinen%20Web-Seiten"
			)
	def test04(self):
		self.assertEqual(
			mailto_url(to="eierschale@irgend.wo",
						  body="""\
Hallo Fritz,

ich wollte nur sagen, daß"""),
		"mailto:eierschale@irgend.wo?body=Hallo%20Fritz%2C%0D%0A%0D%0Aich%20wollte%20nur%20sagen%2C%20da%DF")

	def test05(self):
		self.assertEqual(
			mailto_url(
			to="eierschale@irgend.wo, heidi.bratze@vergiss.es"),
			"mailto:eierschale@irgend.wo,%20heidi.bratze@vergiss.es")


	def test06(self):
		self.assertEqual(
			mailto_url(
			to="Jürgen Honigsüß <juergen@honig.net>",
			subject="[Test] Häschen saß und schlief",
			body="""
			
			Hier eine Mail mit längerem Body.
			Auch Text in "Gänsefüßchen" ist erlaubt.

			Und Sonderzeichen:
			  & : ampersand
			  @ : at
			  < : less than
			  
		  """),
		  'mailto:J%FCrgen%20Honigs%FC%DF%20%3Cjuergen@honig.net%3E?subject=%5BTest%5D%20H%E4schen%20sa%DF%20und%20schlief&body=%0D%0A%09%09%09%0D%0A%09%09%09Hier%20eine%20Mail%20mit%20l%E4ngerem%20Body.%0D%0A%09%09%09Auch%20Text%20in%20%22G%E4nsef%FC%DFchen%22%20ist%20erlaubt.%0D%0A%0D%0A%09%09%09Und%20Sonderzeichen%3A%0D%0A%09%09%09%20%20%26%20%3A%20ampersand%0D%0A%09%09%09%20%20%40%20%3A%20at%0D%0A%09%09%09%20%20%3C%20%3A%20less%20than%0D%0A%09%09%09%20%20%0D%0A%09%09%20%20')


if __name__ == '__main__':
	unittest.main()

