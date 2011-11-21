# coding: latin1
## Copyright 2003-2006 Luc Saffre

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


"""
20040429

"""
from lino.misc.tsttools import TestCase, main
from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import Nation

class Case(TestCase):
    #todo="Crash in big addrbook demo"
    def setUp(self):
        TestCase.setUp(self)
        self.db = startup(langs='en de fr',big=True)
        
    def tearDown(self):
        self.db.shutdown()
        
    def test01(self):
        NATIONS = self.db.query(Nation)
        #from lino.schemas.sprl.data import nations_de
        #nations_de.populate(self.db)
        NATIONS.setBabelLangs('de')
        l1 = []
        l2 = []
        for nation in NATIONS.query(orderBy="name"):
            lbl = unicode(nation)
            if lbl is None:
                l1.append(nation)
            else:
                l2.append(lbl)
        self.assertEqual(len(l1),0)
        #s = "\n".join(l1)
        #print s
        s = " ".join(l2)
        #print s
        
        self.assertEquivalent(s,u"""\
        Afghanistan Albanien Algerien Amerikanisch Samoa Andorra
        Angola Anguilla Antarktis Antigua und Barbuda Argentinien
        Armenien Aruba Ascension (Himmelfahrtsinsel) Aserbaidschan
        Australien Bahamas Bahrain Bangladesch Barbados Belarus
        Belgien Belize Benin Bermuda Bhutan Bolivien
        Bosnien-Herzegowina Botswana Bouvet Island Brasilien British
        Indian Ocean Territory Brunei Darussalam Bulgarien Burkina
        Faso Burundi Chile China Cocos (Keeling) Islands Cook-Inseln
        Costa Rica Demokratische Republik Kongo (früher zr)
        Deutschland Djibouti Dominika Dominikanische Republik Dänemark
        Ecuador Ehemalige Jugoslawische Republik Mazedonien Siehe [2b]
        Ehemalige UdSSR El Salvador Elfenbeinküste Eritrea Estland
        Falkland-Inseln (Malvinas) Fidschi Finnland Frankreich
        Französisch Polynesien Französisch-Guyana Französische Süd-
        und Antarktisgebiete Färöer Gabun Gambia Georgien Ghana
        Gibraltar Grenada Griechenland Großbritannien (UK) Grönland
        Guadeloupe Guam Guatemala Guinea Guinea-Bissau Guyana Haiti
        Heard and McDonald Inseln Honduras Hong Kong Indien Indonesien
        Insel Man Irak Iran Irland Island Israel Italien Jamaika Japan
        Jemen Jersey Jordanien Jungferninseln (Britisch)
        Jungferninseln (U.S.A.) Kambodscha Kamerun Kanada Kap Verde
        Kasachstan Katar Kayman-Inseln Kenia Kirgisien Kiribati
        Kolumbien Komoren Kongo Kroatien (Hrvatska) Kuba Kuwait Laos
        Lesotho Lettland Libanon Liberia Libyen Liechtenstein Litauen
        Luxemburg Macao Madagaskar Malawi Malaysia Malediven Mali
        Malta Marokko Marshall Inseln Martinique Mauretanien Mauritius
        Mayotte Mexiko Mikronesien Moldavien Monaco Mongolei
        Montserrat Mosambik Myanmar Namibia Nauru Nepal Neukaledonien
        Neuseeland (Aotearoa) Neutrale Zone Nicaragua Niederlande
        Niederländische Antillen Niger Nigeria Niue Nordkorea Norfolk
        Inseln Northern Mariana Islands Norwegen Oman Osttimor
        Pakistan Palau Palästina (okkupierte Gebiete) Panama
        Papua-Neuguinea Paraguay Peru Philippinen Pitcairn Polen
        Portugal Puerto Rico Reunion Ruanda Rumänien Russland
        S. Georgia and S. Sandwich Islands Saint Kitts und Nevis Saint
        Lucia Saint Vincent und die Grenadinen Salomonen Sambia Samoa
        San Marino Saudi Arabien Schweden Schweiz (Confoederatio
        Helvetica) Senegal Serbien und Montenegro Seychellen Sierra
        Leone Simbabwe Singapur Slowakei Slowenien Somalia Spanien Sri
        Lanka St. Helena St. Pierre und Miquelon Sudan Surinam
        Svalbard und Jan Mayen Islands Swasiland Syrien São Tomé und
        Principe Südafrika Südkorea Tadschikistan Taiwan Tansania
        Thailand Togo Tokelau Tonga Trinidad und Tobago Tschad
        Tschechien Tschechoslowakei (ehemalige) Tunesien Turkmenistan
        Turks and Caicos Islands Tuvalu Türkei Uganda Ukraine Ungarn
        Uruguay Usbekistan Vanuatu Vatikan (Heiliger Stuhl) Venezuela
        Vereinigte Arabische Emirate Vereinigte Staaten von Amerika
        Vereinigtes Königreich Vietnam Wallis und Futuna
        Weihnachtsinseln Westsahara Zaire (jetzt cd)
        Zentralafrikanische Republik Zypern Ägypten Äquatorialguinea
        Äthiopien Österreich
""")
        
if __name__ == '__main__':
    main()

