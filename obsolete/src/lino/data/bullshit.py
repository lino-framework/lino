#coding: latin1
import random

bullshitWords = """\
Synergie
Bilateral
zielführend
Corporate Identity
Chance/Risiko
kommunizieren
Portfolio
Kick-off
Engagement
Benchmark
wertschöpfend
Visionen
Global Player
prägnant
Strategie
ergebnisorientiert
Offensive
Matrix
Total Quality
Focussieren
Sich schlau machen
Kundenorientiert
Szenario
Visualisieren
Problematik
Komponenten
Faktor
aussichtslos
""".splitlines()

def abstract():
	return """\
Wie wird gespielt?: Kreuzen Sie einen Block an, wenn Sie das
entsprechende Wort während einer Besprechung, eines Seminars oder
einer Konferenz hören. Wenn Sie horizontal, vertikal oder diagonal 5
Blöcke in einer Reihe haben, stehen Sie auf und rufen ganz laut
"BULLSHIT"!!
"""


def body():
	random.shuffle(bullshitWords)
	i = 0
	body1 = "<table border=1>"
	for r in range(5):
		body1 += "<tr>"
		for c in range(5):
			body1 += "<td>"
			body1 += bullshitWords[i]
			i+=1
			body1 += "</td>"
		body1 += "</tr>"
	body1 += "</table>"
	return body1 +"""\
		
Hier ein paar Aussagen von Kollegen die das Spiel getestet haben:

<ul>
<li>“Ich war gerade einmal 5 Minuten in einer Besprechung, als ich schon gewonnen hatte.” –Martin P., Frankfurt

<li>“Meine Aufmerksamkeit während Besprechungen ist dramatisch angestiegen." – Karl A., München

<li>“Was für ein Spiel! Nach meinem ersten Sieg sind Besprechungen
nicht mehr dasselbe für mich.” --- Chris R., Hamburg

<li>“Die Atmosphäre während der letzten Se-Besprechung war zum
Zerreißen gespannt, als 6 von uns auf den letzten Block warteten.”
--- Thomas S., Duisburg

<li>"Der Moderator war sprachlos als 5 Mann in der Besprechung zum
dritten Mal während einer zweistündigen Besprechung gleichzeitig
aufsprangen und "Bullshit" riefen." --- Bernd S. Düsseldorf

</ul>
		"""

	
