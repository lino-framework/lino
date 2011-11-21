#coding: latin1


#from lino.schemas.sprl.demo import getDemoDB
#from lino.adamo.twisted_ui import webserver, UiResource, DbResource

from forum.normalDate import ND


def populate(db):
	db.installto(globals())

	# LANG.appendRow(id='de',name='de')

	home = PAGES.appendRow(
		match="index",
		title='Hauptseite',
		abstract="""

		Willkommen auf der Homepage des VOR
		(Verband Ostbelgischer Radfahrer).
		
		""",body="""

		[url ORGS Links]


		""")

	PAGES.appendRow(
		match=None,
		super=home,
		title="Teilnehmerregeln 2003",
		abstract="""Hier die offiziellen Regeln für die Teilnehmer an Veranstaltungen des VOR.
		""", body="""

<h4>Artikel 1:   Art der Wettkämpfe - Rennen:</h4>

Der Wettkampf für Jugendliche und Erwachsene ist ein XC Rennen mit
einer Länge zwischen 25 Km und 45 Km.
[ref EVENTTYPES:2 Veranstaltungen XC-Rennen].

Die Kids starten auf einem kürzeren und leichteren Parcours. Zwei Starts
mit einer Distanz von +/- 6 Km und +/- 8 Km.

<h4>Artikel 2:   Kategorien 2003:</h4>

<u>Kids, Mädchen und Jungen</u>

Schüler - Minimes (7-11)             Jahrgang 1992+1993+1994+1995+1996
<br>Schüler - Aspiranten (12-14)       Jahrgang 1989+1990+1991.

<u>Mädchen und Frauen</u>

Damen (15 + mehr)                      Jahrgang 1988 und eher.

<u>Jungen und Herren</u>

Jugend - Debütanten (15-16)       Jahrgang 1987 bis 1988
<br>Junioren (17-18)                           Jahrgang 1985 bis 1986
<br>U23 (Espoirs) + Elite (19-29)       Jahrgang 1974 bis 1984
<br>Master 1 (30-39)                          Jahrgang 1964 bis 1973
<br>Master 2 (40-49)                          Jahrgang 1954 bis 1963
<br>Master 3 (50 + mehr)                   Jahrgang 1953 und eher.

<h4>Artikel 3:   Verteilung der Punkte:</h4>

<table>

<tr>
<td>
1. Platz     250  Punkte
<br>2. Platz     240  Punkte
<br>3. Platz     232  Punkte
<br>4. Platz     226  Punkte
<br>5. Platz     222  Punkte

<td>
6. Platz          220  Punkte
<br>7. Platz          219  Punkte
<br>8. Platz          218  Punkte
<br>9. Platz          217  Punkte
<br>10. Platz         216  Punkte
<br>usw.

</tr>
</table>

* für alle Rennen, erster (1.) Fahrer ins Ziel, bedeutet Rennende.

Bei Aufgabe, vorausgesetzt der Teilnehmer ist an den Start gegangen,
erhält 20 Punkte.

Es gibt keine Streichresultate.

Die Organisatorenhelfer erhalten Durchschnitt-Punkte. Der Helfer
(Teilnehmer) kann nur für eine (1) Organisation, Durchschnitt-Punkte
erhalten.

Die Namen der Helfer müssen vor dem Rennen bestimmt und bekannt gegeben
werden.

Ein Organisator, der an seiner Veranstaltung teilnimmt, wird als
Teilnehmer definiert.

<h4>Artikel 4:   Anmeldung -  Einschreibung - Start:</h4>

Rechtzeitig vor dem Start
das Einschreibeformular komplett und lesbar ausfüllen.

Gebühren:
<table>
<tr><td>Kids   (7-14)             <td>&euro;  3,00
<tr><td>Jugend (15-18)            <td>&euro;  6,00
<tr><td>Erwachsene   (19 + mehr)  <td>&euro;  8,00
</table>

Die Kaution für die Startnummer ist &euro;  10,00 oder den Personalausweis.

Die Startnummer muss nach jedem Rennen zurückgegeben werden.

Die Teilnehmer müssen mindest 10 Minuten vor dem Start in die hierfür
vorgesehene Zone anwesend sein.


<h4>Artikel 5:   Wertungen:</h4>

Tageswertung für alle Kategorien - Offen. Gesamtwertung für alle Kategorien -
Offen. Offene Ostbelgische Meisterschaft in allen Kategorien (Strasse/St.Vith
- MTB/Eupen)
(Der 1. Fahrer mit Wohnsitz in Ostbelgien ist Ostbelgischer Meister)

<h4>Artikel 6:   Preisverteilungen:</h4>

Die Preisverteilung "Tageswertungen - Alle Kategorien" wird in einer
angemessenen Zeit, nach dem Rennen, vorgenommen. Es werden 10/5 Preise pro
Kategorie verteilt. Ergebnisse: http://www.chronorace.be
Die Preisverteilung "Gesamtwertungen - Alle Kategorien" wird am 18. Oktober
2003 in KELMIS abgehalten.

<h4>Artikel 7:   Reklamationen:</h4>

Vorfälle während der Rennen sind innerhalb 30 Minuten nach dem Rennende bei
der Jury einzureichen. Nach der Bekanntgabe der Wertung, sind Reklamationen
innerhalb von 30 Minuten zugelassen.
Äußergewöhnliche, nicht im Regelement vorgesehene Situationen werden vom
Organisator und vom V.O.R.- Komitee geregelt.

<h4>Artikel 8:   Jeder Teilnehmer verpflichtet sich:</h4>

<ul>
<li>alle aufgeführten Regeln zu beachten,
<li>die Natur zu respektieren und keine Abfälle zu hinterlassen,
<li>bei Unfall oder Verletzung, Hilfe zu leisten,
<li>faires und sportliches Verhalten,
<li>Straßenverkehrordnung zu respektieren,
<li>den Anweisungen des Organisators und der Streckenposten zu folgen,
<li>nur mit einen MTB in guten Zustand teilzunehmen,
<li><b>Helmpflicht</b>, sonst keine Starterlaubnis,
<li>Laufräder oder kompletter Rad-Wechsel ist verboten,
<li><b>Dopingmittel</b> sind verboten.
</ul>

Bei Missachtung der Regeln darf der Organisator den Teilnehmer
disqualifizieren.
		
		"""
		)

	
	
	PAGES.appendRow(
		match=None,
		super=home,
		title="Der Verband Ostbelgischer Radfahrer",
		abstract="""
		Was ist der Verband Ostbelgischer Radfahrer? Wozu? Geschichte.
		""", body="""
		"""
		)


	PAGES.appendRow(
		match="impressum",
		super=home,
		title="Impressum",
		abstract="""
		Diese Website ist ein Prototyp im Auftrag des
		[ref PARTNERS:1 V.O.R.].
		""", body="""
		Ich weiß selber, dass noch viel daran zu tun ist,
		aber freue mich über Rückmeldungen und Verbesserungsideen.

		Luc Saffre.
		
		"""
		)








## 	PAGES.appendRow(
## 		match=None,
## 		super=home,
## 		title="",
## 		abstract="""
## 		""", body="""
## 		"""
## 		)



	
	
	ORGS.appendRow(name="ChronoRace - Electronic Timing SPRL",
						website="http://www.chronorace.be",
						phone="+32 (0)476 282 004",
						fax= "+32 (0)61 28 77 07",
						email="christian.lemasson@chronometrage.be"
						)
	

	kids = EVENTTYPES.appendRow(
		title="Kids Trophy",
		abstract="""
		Minimes (7J - 11J)  +  Aspiranten (12 J -14J)
		""")

	xc = EVENTTYPES.appendRow(
		title="Cross Country / XC Rennen",
		abstract="""
Damen(15 + mehr) Debütanten (15-16) Junioren (17-18)
Elite (19-29) Master I (30-39) Master II (40-49)
Master III (50 + mehr)
		""")
	
	etc = EVENTTYPES.appendRow(
		title="Andere Veranstaltungen",
		abstract="""
		""")


	be = NATIONS.appendRow(id='be',name_de="Belgien")
	de = NATIONS.appendRow(id='de',name_de="Deutschland")
## 	from lino.schemas.sprl.data import nations
## 	nations.populate(db)
## 	be = NATIONS['be']
## 	de = NATIONS['de']


	p = PARTNERS.appendRow(name="Verband Ostbelgischer Radfahrer",
								  logo="vor.jpg",
								  nation=be)

	member = PARTYPES['m']
	sponsor = PARTYPES['d']
	
	p = PARTNERS.appendRow(name="VC Kelmis",
								  type=member,
								  logo="vc-calamine.png",
								  nation=be)
	q = p.eventsByResponsible
	q.appendRow(
		date=ND(20030511),
		time="11:00",
		type=kids)
	q.appendRow(
		date=ND(20030511),
		#date="11.05.2003",
		time="12:00",
		type=xc)

	p = PARTNERS.appendRow(name="Einruhr",
								  logo="sv-einruhr.png",
								  type=member,
								  nation=de)
	q = p.eventsByResponsible
	q.appendRow(
		date=ND(20030622),
		#date="22.06.2003",
		time="11:00",
		type=kids)
	q.appendRow(
		date=ND(20030622),
		#date="22.06.2003",
		time="14:00",
		type=xc)
	
	p = PARTNERS.appendRow(name="Lontzen",
								  website="http://www.helowa.be",
								  type=member,
								  nation=be)
	q = p.eventsByResponsible
	q.appendRow(
		date=ND(20030629),
		#date="29.06.2003",
		time="11:00",
		type=kids)
	q.appendRow(
		date=ND(20030629),
		#date="29.06.2003",
		time="14:00",
		type=xc)

	p = PARTNERS.appendRow(name="RSV Sankt Vith",
								  nation=be,
								  type=member,
								  logo='rsv-stvith.png')
	q = p.eventsByResponsible
	q.appendRow(
		date=ND(20030706),
		#date="06.07.2003",
		time="11:00",
		type=kids)
	q.appendRow(
		date=ND(20030706),
		#date="06.07.2003",
		time="14:00",
		type=xc)
	q.appendRow(
		date=ND(20030706),
		#date="06.07.2003",
		time="7:00 - 10:00",
		title='26.Int.Touristik-Dreiländerfahrt / UCI "Classics"',
		abstract="""
		151 Km – 110 Km – 75 Km – 45 Km
		MTB Touristik
		50 Km – 30 Km
		""",
		type=etc)
	q.appendRow(
		date=ND(20030718),
		#date="18.07.2003",
		time="19:00",
		title="Sommerkriterium - Strasse (*) / Offen – 45 Km",
		abstract="Ostbelgische Meisterschaft Strasse",
		type=etc)


	

	p = PARTNERS.appendRow(name="Eifelbiker Bütgenbach",
								  nation=be,
								  type=member,
								  logo="ebb.png")
	#p = PARTNERS.appendRow(name="Bütgenbach",nation=be)
	q = p.eventsByResponsible
	q.appendRow(
		date=ND(20030816),
		#date="16.08.2003",
		time="17:30",
		type=kids)
	q.appendRow(
		title="Kindersprint",
		date=ND(20030816),
		#date="16.08.2003",
		time="13:00-16:00",
		type=kids)
	q.appendRow(
		title="14.Int.MTB Rennen",
		date=ND(20030817),
		#date="17.08.2003",
		time="14:00",
		type=xc)

	p = PARTNERS.appendRow(name="RSK Eupen",
								  website="http://www.rskeupen.be",
								  type=member,
								  nation=be)
	q = p.eventsByResponsible
	q.appendRow(
		date=ND(20031005),
		#date="05.10.2003",
		time="11:00",
		type=kids)
	q.appendRow(
		title="Ostbelgische Meisterschaft  MTB",
		date=ND(20031005),
		#date="05.10.2003",
		time="14:00",
		type=xc)
	q.appendRow(
		title="8.MTB Ausfahrt 25-35-45-55 Km",
		date=ND(20030330),
		#date="30.03.2003",
		time="08:00 - 12:00",
		type=etc)


	p = PARTNERS.appendRow(name="Deutschsprachige Gemeinschaft",
								  type=sponsor,
								  nation=be,
								  logo="dg.png")
	
	p = PARTNERS.appendRow(name="Tour de Belgique/Ronde van België",
								  nation=be,
								  logo='tour.be.jpg'
								  )
	q = p.eventsByResponsible
	q.appendRow(date=ND(20040523),
					title="Belgienrundfahrt",
					type=etc)

	if False:

		p = PARTNERS.appendRow(name="Testveranstalter",
									  nation=be)
		q = p.eventsByResponsible
		d=ND(20040415)
		for i in range(32):
			for j in range(32):
				q.appendRow(
					date=d,
					title="Testveranstaltung Nummer %d am %s"%(j,str(d)),
					time="11:11",
					type=etc)
			d += 1
	


	#from lino.schemas.sprl import demo2
	#demo2.populateDemo(db)
	
	db.commit()


## db = getDemoDB(isTemporary=True,populator=populate)


## dbr = DbResource(db, staticDirs = {
## 	'files': 'files',
## 	'images': 'images',
## 	'thumbnails': 'thumbnails'
## 	})

## root = UiResource(db.ui)
## root.putChild(arg,dbr)


## webserver(root,showOutput=False)
