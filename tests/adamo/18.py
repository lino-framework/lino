# coding: latin1
"""
20040429

"""
from lino.misc.tsttools import TestCase
from lino.schemas.sprl import demo
from lino.adamo.datatypes import DataVeto

class Case(TestCase):
	def setUp(self):
		self.db = demo.getDemoDB(populator=None,
										 langs='en de fr')
		demo.populate(self.db,big=True)
		self.db.installto(globals())
		
	def tearDown(self):
		self.db.shutdown()
		
	def test01(self):
		from lino.schemas.sprl.data import nations_de
		nations_de.populate(self.db)
		setBabelLangs('de')
		l1 = []
		l2 = []
		for nation in NATIONS.query(orderBy="name"):
			lbl = nation.getLabel()
			if lbl is None:
				l1.append(repr(nation))
			else:
				l2.append(lbl)
		self.assertEqual(len(l1),0)
		#s = "\n".join(l1)
		#print s
		s = " ".join(l2)
		#print s
		
		self.assertEquivalent(s,"""\
Afghanistan Albanien Algerien Amerikanisch Samoa Andorra Angola
Anguilla Antarktis Antigua und Barbuda Argentinien Armenien Aruba
Aserbaidschan Australien Bahamas Bahrain Bangladesch Barbados Belarus
Belgien Belize Benin Bermuda Bhutan Bolivien Bosnien-Herzegowina
Botswana Bouvet Island Brasilien British Indian Ocean Territory Brunei
Darussalam Bulgarien Burkina Faso Burundi Chile China Cocos (Keeling)
Islands Cook Inseln Costa Rica Demokratische Republik Kongo (früher
Zaire) Deutschland Djibouti Dominika Dominikanische Republik Dänemark
Ecuador Ehemalige Jugoslawische Republik Mazedonien Siehe [2b]
Ehemalige UdSSR El Salvador Elfenbeinküste Eritrea Estland
Falkland-Inseln (Malvinas) Fidschi Finnland France, Metropolitan
Frankreich Französisch Polynesien Französisch-Guyana French Southern
Territories Färöer Gabun Gambia Georgien Ghana Gibraltar Grenada
Griechenland Großbritannien (UK) Grönland Guadeloupe Guam Guatemala
Guinea Guinea-Bissau Guyana Haiti Heard and McDonald Inseln Honduras
Hong Kong Indien Indonesien Irak Iran Irland Island Israel Italien
Jamaika Japan Jemen Jordanien Jungferninseln (British) Jungferninseln
(U.S.) Kambodscha Kamerun Kanada Kap Verde Kasachstan Katar
Kayman-Inseln Kenia Kirgisien Kiribati Kolumbien Komoren Kongo
Kroatien (Hrvatska) Kuba Kuwait Laos Lesotho Lettland Libanon Liberia
Libyen Liechtenstein Litauen Luxemburg Macao Madagaskar Malawi
Malaysia Malediven Mali Malta Marokko Marshall Inseln Martinique
Mauretanien Mauritius Mayotte Mexiko Mikronesien Moldavien Monaco
Mongolei Montserrat Mosambik Myanmar Namibia Nauru Nepal Neukaledonien
Neuseeland (Aotearoa) Neutrale Zone Nicaragua Niederlande
Niederländische Antillen Niger Nigeria Niue Nordkorea Norfolk Inseln
Northern Mariana Islands Norwegen Oman Osttimor Pakistan Palau Panama
Papua-Neuguinea Paraguay Peru Philippinen Pitcairn Polen Portugal
Puerto Rico Reunion Ruanda Rumänien Russland S. Georgia and
S. Sandwich Islands Saint Kitts und Nevis Saint Lucia Saint Vincent
und die Grenadinen Sambia Samoa San Marino Saudi Arabien Schweden
Schweiz (Confoederatio Helvetica) Senegal Serbien und Montenegro
(Jugoslawien, wird vermutlich demnächst geändert) Seychellen Sierra
Leone Simbabwe Singapur Slowakei Slowenien Solomon Inseln Somalia
Spanien Sri Lanka St. Helena St. Pierre und Miquelon Sudan Surinam
Svalbard und Jan Mayen Islands Swasiland Syrien São Tomé und Príncipe
Südafrika Südkorea Tadschikistan Taiwan Tansania Thailand Togo Tokelau
Tonga Trinidad und Tobago Tschad Tschechien Tschechoslowakei
(ehemalige) Tunesien Turkmenistan Turks and Caicos Islands Tuvalu
Türkei US Minor Outlying Islands Uganda Ukraine Ungarn Uruguay
Usbekistan Vanuatu Vatikan (Heiliger Stuhl) Venezuela Vereinigte
Arabische Emirate Vereinigte Staaten von Amerika Vereinigtes
Königreich Vietnam Wallis und Futuna Weihnachtsinseln Westsahara Zaire
(jetzt CD - Demokratische Republik Kongo) Zentralafrikanische Republik
Zypern Ägypten Äquatorialguinea Äthiopien Österreich""")
		
if __name__ == '__main__':
	import unittest
	unittest.main()

