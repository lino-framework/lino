# coding: latin1
# originally copied from http://www.mastel.ch/andre/weisheiten.htm
# manually added and deleted

import re

def populate(db,**kw):
	db.installto(globals())
	q = QUOTES.query('lang abstract')
	s = """\
Abgeordnete sind immer zu tausend Spesen aufgelegt.
Alle können denken; nur bleibt es den meisten erspart.
Alle Menschen werden [noch!] als Original geboren, die meisten sterben als Kopie.
Allen Leuten recht getan ist Sauerkraut mit Lebertran.
Aller Mannfang ist schwer.
Alles Geschmackssache, dachte der Affe und biss in die Seife.
Alles hat Grenzen, nur die Dummheit ist unendlich.
Alles ist so, wie es ist, nur schlechter.
Alles schreitet fort, nur der Fortschritt nicht.
Alles wird schlechter, nur eins wird besser: die Moral wird schlechter.
Alle wollen zurück zur Natur; aber keiner zu Fuss.
Alter schützt nicht vor Torheit, aber Dummheit vor Intelligenz.
Alles wird besser, nichts wird gut.
Am Abend werden die Faulen fleissig und die Hungrigen durstig.
An die Waffeln, Bürger!
Anything goes, nur nicht Albrecht Goes.
Arbeit adelt; wir aber bleiben bürgerlich.
Arbeit ist der Untergang der trinkenden Klasse.
Arbeit ist eine lustvolle Variante des Schwachsinns.
Arbeit ist süss; ich bin aber Diabetiker.
Arbeit macht das Leben süss; Faulheit stärkt die Glieder.
Arbeit macht Spass; aber wer kann schon Spass vertragen?
Arbeit macht Spass; man kann stundenlang zuschauen.
Arbeit ist süss, aber sauer macht lustig.
Arbeitskraft? Nein danke.
Auch die Stimme des Gewissens hat mal Stimmbruch.
Auch ein Anzug von BOSS macht aus Ihnen keinen CHEF.
Auch ein Spaßvogel kann es so weit treiben, dass er fliegt.
Auf dem Baum, da saß ein Specht; der Baum war hoch, dem Specht war schlecht.
Auf die Pauke hauen will jeder, nur tragen will sie keiner.
Auf diese Frage antworte ich mit einem entschiedenen Vielleicht.
Betrachten Sie Ihr Gehalt als Anwesenheitsprämie.
Billard ist bekannter als Billzdf. (Ergebnis einer Medienumfrage)
Biss demnächst, sagte der Vampir.
Biste in der EDV, kennt deine Daten jede Sau.
Blumen, die nicht wachsen, nennt man Wachsblumen.
Brennt dem Bauern mal der Kittel, lag's am scharfen Düngemittel.
Charme ist das einzige, das sich nicht unter Druck versprühen lässt.
Chirurgen tragen Gummihandschuhe, um keine Fingerabdrücke zu hinterlassen.
Computer lösen die Probleme, die wir ohne sie nicht hätten.
Damit wir andere Sterne sehen, muss unsere Sonne untergehen.
Das Denken sollte man den Pferden überlassen. Sie sind beschlagen.
Das einzig Echte an manchen Menschen ist ihre Falschheit.
Das einzige, was Reiche nicht haben, ist kein Geld.
Das ewig Weibliche zieht uns hinunter und hält uns frisch, gesund und munter.
Das Faustrecht ist nicht abgeschafft; es ist nur in die Ellenbogen umgezogen.
Das Hemd hemmt den Politiker weniger als die weiße Weste.
Das Leben gibt's gratis, der Rest ist käuflich.
Das nehm ich dir übel, sprach der Dübel, und verschwand in der Wand, wo ihn niemand wiederfand.
Dem Alltags-Stress kann man entgehen, vermeidet man es aufzustehen.
Dem Philosoph ist nichts zu doof.
Den Blick in die Welt kann eine Zeitung versperren.
Denen habe ich's gegeben, sagte der Steuerzahler, als er das Finanzamt verliess.
Denken ist Arbeit, Arbeit ist Energie, und Energie soll man sparen.
Der Apfel fällt nicht weit vom Zank.
Der Arbeit kann man leicht entgehen, vermeidet man es aufzustehen.
Der Arbeitstag beginnt um sieben; doch nicht, wenn du im Bett geblieben.
Der Computer ist die Antwort...Was war eigentlich die Frage?
Der deutsche Humor ist seiner Seltenheit wegen besonders wertvoll.
Der direkteste Weg der Listigen ist die Schlangenlinie.
Der Geist denkt, das Geld lenkt.
Der Glatzkopf, der die Glatze föhnt, hat mit dem Schicksal sich versöhnt.
Der Hektiker rast bei Gelb über die Ampel. Der Besonnene wartet, bis Rot ist.
Der Kanzler lenkt - aber wer denkt?
Der Klügere gibt so lange nach, bis er der Dumme ist.
Der Klügere gibt vor, nachzugeben.
Der Klügere zählt nach.
So lange der Klügere nachgibt, wird die Welt von Dummen beherrscht.
Der Mensch sollte nicht gesünder leben als ihm guttut.
Der Mohr hat seine Schuldigkeit getan, der Mohr kann kaum noch gehn.
Der Mond ist nicht nur kleiner als die Erde, sondern auch weiter von ihr entfernt.
Der Mond ist voll, und ich hab auch schon Durst.
Der Opi der nahm Opium; bums, da fiel der Opi um.
Der Papst zu Thomas Gottschalk: Wetten, dass ich 200 Flughäfen am Geschmack erkenne?
Der Plebs trinkt Schweppes.
Der Schwätzer sagt, was der Kopflose denkt.
Der Spekulant verdient sein Brot mit Hausverfall und Wohnungsnot.
Der Student studiert, der Arbeiter arbeitet, der Chef scheffelt.
Der Verstand ist unser grösstes Vermögen, aber Armut schändet nicht.
Der Wintereinbruch ist nicht strafbar.
Diäten hoch, Phrasen platt - wie schön is dat!
Die Axt im Haus ist die Mutter der Porzellankiste.
Die Basis des Fundamentalen ist das Grundlegende.
Die dämlichsten Herren haben oft die herrlichsten Damen.
Die Elbe ist ein Jungbrunnen: ein Schluck, und du wirst nicht alt.
Die Entfernung zwischen Brett und Kopf nennt man Horizont.
Die Frauen sind viel zu liebenswert, als dass man sie den Feministinnen überlassen sollte.
Die kluge Frau folgt ihrem Mann, wohin sie will.
Die Liebe ist ein Feuer; man weiss nie, wie es ausgeht.
Die Luft ist Schein, und der trügt.
Die meisten Holzwege enden in einer Sackgasse.
Die meisten Menschen werden kleiner, wenn man sie unter die Lupe nimmt.
Die meisten Leute reden nur, weil sie zu faul zum Lesen sind.
Die nächste Steinzeit kommt bestimmt.
Die Pflicht ruft? Wir rufen zurück.
Die Publikationen des Dozenten sind so gut wie die Seminararbeiten seiner Studenten.
Die Regierung spart, jetzt müssen sich 20 Minister ein Gehirn teilen.
Die Schlankheitskur verliert den Schrecken, lässt du dir alles weiter schmecken.
Die Unterdrückten der Gegenwart sind die Unterdrücker der Zukunft.
Die Wahrheit hat noch keinem geschadet - ausser dem, der sie ausspricht.
Die Welt erstickt in Plastiktüten; die Einkaufstasche kann's verhüten.
Die Zeit zurückdrehen hiesse Milch aus Käse zu produzieren.
Die Zunge ist das einzige Werkzeug, das durch ständigen Gebrauch noch schärfer wird.
Drinnen ist es wie draussen: bloss anders.
Drum prüfe, wer sich ewig schindet ...
Du hast so schöne Zähne: gibt's die auch in weiss?
Dummheit, verlass ihn nicht, sonst steht er ganz allein.
Echte Bankgeheimnisse gibt es nur in Parkanlagen.
EDV = Ende der Vernunft.
Eher kommt ein Kamel durchs Nadelöhr als ein Elefant ins Mausoleum.
Ei laf ju änd ju laf mi - laf ma zam, wo laf ma hi?
Ein blindes Huhn findet auch mal eine lahme Ente.
Ein deutscher Mann misstraut allem Fremden; es sei denn, es lässt sich trinken.
Eine Frau ohne Mann ist wie ein Fisch ohne Fahrrad.
Eine Schwalbe macht noch keinen Elfmeter.
Ein Gehirn wäscht das andere.
Eine spitze Zunge ist in vielen Ländern schon unerlaubter Waffenbesitz.
Ein Masochist, der zurückhaut, ist pervers.
Ein Schwein kommt selten allein.
Ein Student geht so lange zur Mensa, bis er bricht.
Ein voller Bauch fällt nicht weit vom Stamm.
Eine Kuh macht muh; viele Kühe machen Mühe.
Eine Lösung hatte ich, aber sie passte nicht zum Problem.
Einstein ist tot, Newton ist tot, und mir ist auch schon schlecht.
Ein voller Kopf studiert nicht gern.
Ende gut, alles putt.
Energiesparer: heizt mit Meerwasser, das ist fast reines Öl.
Enthaltsamkeit ist aller Laster Anfang.
Er hat Haare auf der Brust. Na und? Lassie etwa nicht?
Er sagte 'Isabelle'. Und Isa bellte.
Erst schliessen wir die Augen; dann sehen wir weiter.
Er war Mathematiker, sie war unberechenbar.
Es gibt Menschen, die nur in aufgeblasenem Zustand sichtbar werden.
Es gibt viel zu tun, nix wie weg.
Es genügt nicht, unfähig zu sein; man muss auch in die Politik gehen.
Es ist ein Brauch von alters her: die Dicken sind besonders schwer.
Es sind nicht nur die Optiker, die ständig nach Kontakt linsen.
Es tut NIVEA als beim ersten Mal.
Es wird nicht alles so heiss gegessen wie man sich fühlt.
Es wird schon schiefgehen, sagte der Turmbauer von Pisa.
Fällt der Bauer tot vom Traktor, ist in der Nähe ein Reaktor.
Färbt der Patient sich plötzlich lila, desinfiziert man mit Tequila.
Faulenzen schafft Arbeitsplätze.
Faulheit ist: sich ausruhen, bevor man müde wird.
Flauten sind halb so schlimm, wenn man rechtzeitig von ihnen Wind bekommt.
Frauen gemeinsam sind stark geschädigt.
Frauenpower macht uns sauer.
Frech gesagt ist halb gefeuert.
*Freies Chatten für alle! Macht die Wände dünner!
Freiheit für alle! Weg mit der Schwerkraft!
Freiheit für Grönland! Nieder mit dem Packeis!
Frei ist, wer will, was er ohnehin muss.
Friedhelm statt Stahlhelm.
Friert's den Bauern arg am Schuh, steht er in der Tiefkühltruh'.
Friert's im Dezember Stein und Bein, dann könnte das der Winter sein.
Frisch gewachst ist halb gefallen.
Frisch gewagt ist halb verschrottet. (Autobahn-Motto)
Frisch verzagt ist halb verzweifelt.
Früher fuhren wir jedes Wochenende in den Wald. Heute haben wir die Müllabfuhr.
Früher haben wir uns vor der Arbeit gedrückt, heute schauen wir stundenlang zu.
Früher las ich Karl Marx, doch dann entdeckte ich Pippi Langstrumpf.
Früher wusste ich nicht, was Liebe ist; dann entdeckte ich den Computer.
Früh gewagt ist früh gestorben.
Für einen Anlass gibt es immer eine Gelegenheit.
Für Geld tue ich alles, sogar arbeiten.
Für manche Leute ist ein Gehirnschlag ein Schlag ins Leere.
Gäste, die voll kommen, sind nicht vollkommen.
Gefährlich wird es, wenn die Dummen fleissig werden.
Gehirnschlag = ein Schlag ins Leere.
Gemeinsam sind wir unausstehlich.
Geniesse das Leben beständig, denn du bist länger tot als lebendig.
Gepflegter Bart küsst weich und zart.
Gescheit, gescheiter, gescheitert.
Gesunde Verdorbenheit ist besser als verdorbene Gesundheit.
Gewollte Brillanz ergibt nur Brillantine.
Gib mir Deinen Ausweis, und ich sage Dir, wer Du bist.
Gott ist allmächtig, nur nicht auf der Erde.
Gott ist nicht tot; nur beim Wort zum Sonntag eingeschlafen.
Gott ist tot (Nietzsche). Nietzsche ist tot (Gott).
Gott sei Punk.
Gute Mädchen kommen in den Himmel; böse überallhin.
Guter Staat ist teuer.
Gut gemeint ist auch nicht besser.
Gut Kind will Keile haben (nach M. Luther)
Haben Krawattenträger nicht schon genug am Halse?
Haben Sie keine Angst vor Fachbüchern. Ungelesen sind sie alle harmlos.
Hängst du im Sommer auf der Schüssel, kam das Hähnchen wohl aus Brüssel.
Harrisburger: da strahlt die ganze Familie.
Hasse dich nicht schon am Morgen: schlaf bis Mittag.
Hast du im Bett dich heissgewühlt, trink Coca-Cola eisgekühlt.
Hat der Bauer kalte Hände, flieht die Kuh in das Gelände.
Hau niemals ab - hau einfach zu!
Heiliger Sankt Benedikt, ich bin schon wieder eingenickt.
Heiratest du aus Liebe, hast du schöne Nächte und schlechte Tage.
Hey Kids, let's kotz.
Hic Rhodos, hic Malta.
Hinter den Drahtziehern stehen die Stacheldrahtzieher.
Hunde, die schielen, beissen daneben.
Ich bin ein Vampir: wasch dir den Hals!
Ich bin intelligent, schön und gebildet, doch das Beste an mir ist meine Bescheidenheit.
Ich bin nicht feige; ich bin nur stärker als der Held in mir.
Ich bin tolerant; wem das nicht passt, dem hau ich eine.
Ich bin wirklich kein Zyniker; ich habe nur Erfahrung.
Ich bin zutiefst gerührt, sprach der Teig.
Ich brauch kein Hasch; ich nehme DASH.
Ich denke, also spinn ich.
Ich hab' die Kantine satt, ich esse nur noch Kitekat.
Ich hab' im Traum dein Bild gesehn, da blieb vor Schreck mein Wecker stehn.
Ich kann fliegen, sagte der Wurm, als er mit dem Apfel vom Baum fiel.
Ich sage, was ich denke, damit ich höre, was ich weiss.
Ich schaue in den Spiegel und denk', ich hab' Besuch.
Ich stehe hier am Mittelmeer und habe keine Mittel mehr.
Ich summe, also bien ich.
Ich verspreche nichts; und das halte ich auch.
Ihr da Ohm, macht doch Watt ihr Volt.
Ihr habt das Land, doch wir haben die Wand.
Im Falle eines Falles ist richtig fallen alles.
Im Herbst, da fallen die Blätter; das liegt wohl am Wetter.
Immer wenn der Chef rot sieht, ärgere ich mich schwarz und mache blau.
Im Schatten ist es ruhig, weil man das Licht nicht hört.
In mir schlummert ein Genie, nur wird das Biest nicht wach.
Input - Output - ganz putt.
In Wirklichkeit ist die Realität ganz anders.
Irgendwann begegnet man dem Whisky seines Lebens.
Ist das Freibad voll wie nie, läuft Wimbledon im Pay-TV.
Ist Silvester hell und klar, ist am andern Tag Neujahr.
It's nice to be a Preiss and it's higher to be a Bayer, but it's a Gottesgab to be a Schwab.
Jedem Analphabeten sein Diktiergerät!
Jeder Bürger wird zum Wurm, sieht er eine Unifurm.
Jeder ist seines Glückes Störenfried.
Jedes Pro und Contra hat sein Für und Wider.
Je grösser das Konfekt, desto grösser die Konfektion.
Je leerer die Versprechungen, desto voller die Absicht.
Je tiefer das Loch, desto plumps.
Jetzt gehen wir der Sache auf den Grund, sprach der Bauer und sprang in die Jauchegrube.
Je weniger Haare man hat, desto mehr Gesicht muss man waschen.
Je zwölfer der Mittag, desto knurrer der Magen.
"Jetzt geht's rund !", sprach der Spatz und flog in den Ventilator.
Jodelt laut die Magd im Stall, kriegt die Kuh 'nen Herzanfall.
Karneval ist Nonsens in Rheinkultur.
Kein Atom-Müll zum Mars! Mars bringt verbrauchte Energie sofort zurück.
Keine Angst: wir kommen nicht in die Hölle. Wir leben schon drin.
Keiner ist unnütz: er kann immer noch als schlechtes Beispiel dienen.
Keiner redet dümmer als er ist.
Kein Fachmann ohne Flachmann.
Kein Versicherungsschutz bei Einbruch der Dunkelheit.
Kinder unter fünf Jahren sind mit Klebeband oder Vorhängeschloss zu sichern.
Kippt Kaiser Franz von der Empore, gab's in der Nachspielzeit zwei Tore.
Kleine Bosheiten erhalten die Feindschaft.
Kluge leben von den Dummen, Dumme von der Arbeit.
Kommt der Gockel untern Trecker, gibt es morgens keinen Wecker.
Kräht der Bauer auf dem Mist, hat der Gockel sich verpisst.
Kräht der Maulwurf auf dem Dach, liegt der Hahn vor Lachen flach.
Kreuzbrave sind meist piksauber.
Langweilige Frauen haben blitzsaubere Küchen.
Legt die Nordsee trocken, wir wollen nach England.
Lehrer sind Menschen, die nach der Schule in Pension gehen.
Leihen Sie Geld lieber bei Pessimisten; sie erwarten keine Rückzahlung.
Lerne lachen ohne zu weinen.
Libero als gekocht.
Licht ist nicht vorhandene Dunkelheit.
Liebe deinen Nächsten, aber lass dich nicht erwischen.
Liebe deinen Nächsten wie dein Auto.
Liebe ist Elektrizität; in der Ehe kommt die Stromrechnung.
Liebe ist mir zu philosophisch; ich bleibe lieber beim Bier.
Liebe ist, wenn man trotzdem lacht.
Liebe ist, zusammen ins Deutsche Museum zu gehen.
Lieber am Hungertuch nagen als mit Hammer und Sichel essen.
Lieber Arm ab als arm dran.
Lieber aussteigen als eingehen.
Lieber Blödeleien als blöde Laien.
Lieber ein Altbier als eine Neurose.
Lieber ein Blatt vorm Mund als ein Brett vorm Kopf.
Lieber ein Bund fürs Leben als ein Leben für den Bund.
Lieber eine dunkle Kneipe als ein lichter Arbeitsplatz.
Lieber ein erregter Bekannter als ein unbekannter Erreger.
Lieber eine Flasche Bier als ne Wanne Eickel.
Lieber eine Flinte im Korn als Waffen im Weltraum.
Lieber eine Meise als gar keinen Vogel.
Lieber einmal Sydne Rome als zweimal Paris-Dakar.
Lieber ein schwarzes Schaf als ein Blauer Bock.
Lieber ein verwanztes Telefon als ein lausiges Fernsehprogramm!
Lieber ein Zebra streifen als einen Bullen anfahren.
Lieber entlarvt als entschärft.
Lieber FKK als FDP.
Lieber Frust im Kopf als Faust auf's Auge.
Lieber fünf Minuten feige als ein Leben lang tot.
Lieber fünf vor zwölf als keine nach eins.
Lieber Glück im Unglück als Pech in der Strähne.
Lieber Gold in der Kehle als Silber im Blick.
Lieber Gott, mach micht nicht gross, ich werd ja doch bloss arbeitslos.
Lieber Hahn im Korb als Hähnchen im Wienerwald.
Lieber halbstark mit Sturzhelm als ganz stark mit Stahlhelm.
Lieber Himbeergeist als Männerverstand.
Lieber Hochstapler als Tiefflieger.
Lieber Hosenträger als gar keinen Halt.
Lieber in Form als infam.
Lieber Kies in der Tasche als Sand im Koffer.
Lieber kleckern als kotzen.
Lieber lächerlich als bürgerlich.
Lieber leb' ich meiner Lust als Stempeluhr und Arbeitsfrust.
Lieber locker vom Hocker als hektisch über'n Ecktisch.
Lieber mit einer kleinen Maus aufwachen als mit einem grossen Kater.
Lieber Mixed Pickles als Akne.
Lieber natürliche Dummheit als künstliche Intelligenz.
Lieber 'n Altbier als 'ne Neurose.
Lieber 'ne frohe Kunde als 'ne traurige Verkäuferin.
Lieber 'n Glas Dortmunder als 'ne Wanne Eickel.
Lieber Ostern als Western.
Lieber Ouzo als Juso.
Lieber reich und gesund als arm und krank.
Lieber Rosinen im Kopf als Haare im Kuchen.
Lieber Schweissperlen als gar keinen Schmuck.
Lieber sechs Stunden Uni am Tag als gar keinen Schlaf.
Lieber spät und richtig als nie und falsch.
Lieber süssen Nebel als sauren Regen.
Lieber träumen unter Bäumen als schaffen unter Affen.
Lieber ungebunden als angebunden.
Lieber von Picasso gemalt als vom Schicksal gezeichnet.
Lieber Wein, Weib und Gesang als Bier, Mann und Gebrüll.
Lieber Wurstfinger als Knoblauchzehen.
Lieber zusammen aus- als allein eingehen.
Literatur - Sekundärliteratur - Tertiärliteratur - Makulatur.
Löwenmaul und Leumund haben nur wenig gemeinsam.
Lügen haben kurze Beine, aber tausend Füsse.
Macht der Blechknopf plötzlich peng, waren deine Jeans zu eng.
Männer suchen das gewisse Etwas, Frauen etwas Gewisses.
Magerquark macht uns stark; Haferbrei macht uns frei.
Manche Ehefrau lässt lieber den Ofen ausgehen als ihren Mann.
Manche halten zehnmal leichter eine Rede als einmal ihr Wort.
Mancher fasst sich da an den Kopf - und greift ins Leere.
Manche sind wie die Erde: immer auf Achse und trotzdem rund.
Manche tun so viel für ihre Gesundheit, dass sie ganz krank davon werden.
Manche würden eher sterben als nachdenken. Und sie tun es auch.
Man kann sich an allem gewöhnen, auch am Dativ.
Man soll den Tag nicht vor dem Elternabend loben.
Man soll die Gäste feuern, wie sie fallen.
Meine Glotze ist kaputt, drum lern' ich lesen.
Mein Geist verfolgt mich, aber ich bin schneller.
Mens sana in Campari Soda.
Menschen mit sehr grossen Ohren sind für's Segeln wie geboren.
*Mercedes, Villa, Swimming Pool - von Stoa reden ist so cool.
Mich kennen heisst mich lieben.
Milch trinken ist besser als Quark reden.
Mit den Händen in den Taschen kann man keine Fliegen haschen.
Mit einer Mieze feierte er Silvester, und mit einem Kater Neujahr.
Mit Haaren bunt so wie ein Smartie ist man der Hit auf jeder Party.
Mit leerem Kopf nickt es sich leichter.
Mitleid bekommt man geschenkt; Neid muss man sich verdienen.
Mit Phantasie kommt man leichter zu Geld als mit Geld zu Phantasie.
Mit Wein, Weib und Gesang wird man garantiert nicht krank.
Montagmorgen 10 nach 8, und die Woche nimmt kein Ende.
Müde und satt, wie schön is dat.
Muss es erst duster sein, bevor uns ein Licht aufgeht?
Narrenhände betatschen Brust und Lende.
Nicht Güte zählt, sondern Bonität.
Nicht jeder, der einen Vogel hat, ist ein Star.
Nicht jeder, der aus dem Rahmen fällt, war vorher im Bilde.
Nicht jeder Mann, der raucht, ist ein Vulkan.
Nichts ist wahr in der Seemansbar.
Nichts ist schwerer zu ertragen als Reissverschluss auf vollem Magen.
Nieder mit der Schwerkraft - es lebe der Leichtsinn!
Niemand verschönt den Betriebsausflug so wie die, die nicht dabei sind.
Nimm alles, dann brauchst du nichts.
Nimm 's leicht, sonst nimmt 's ein anderer.
Nirwana ist nirgendwo, Banana ist überall.
Nonsens ist der Sieg des Geistes über die Vernunft.
Nostalgie genügt nicht; du musst auch jünger werden!
Nur Idioten halten Ordnung; ein Genie beherrscht das Chaos.
Oh, frivol ist mir am Abend.
Ohne Fleiss kein Preis; ohne Leim kein Reim.
Ohne Lärm und viel Gebrüll macht das Blatt sein Chlorophyll.
Pessimisten finden auch in der Fischsuppe ein Haar.
Planung ist der Ersatz des Zufalls durch den Irrtum.
Praktisch denken - Särge schenken.
Politik bedeutet Steuern zu erheben, die man selbst nicht zahlt.
Polygamie ist Demokratie im Bett.
Praxis ist, wenn alles funktioniert und keiner weiss warum.
Professorenglatze ist Waldsterben auf höherer Ebene.
Pubertät ist, wenn die Eltern anfangen schwierig zu werden.
Rache ist süss: jede Süssigkeit rächt sich.
Raritäten, die in Massen auftreten, sind besonders selten.
Rauche jetzt, zahle später.
Regnet's im Mai, ist der April vorbei. (Bauernregel)
Riech' ich dein Aroma, fall ich gleich ins Koma.
Rot denken, grün wählen, blau machen, schwarz schaffen.
Rote Lippen sind erotisch, blaue leider nicht eblautisch.
Rückgrat bitte beim Chef abgeben.
Rülpst im Schweinestall der Knecht, wird's sogar den Schweinen schlecht.
Ruhe ist der erste Bürgerfluch.
Sage mir, warum, und ich sage dir, weshalb.
Schafft Weihnachten ab! Josef [nicht: Fischer] hat alles zugegeben.
Schnauze, sonst Beule.
Schönheitschirurgen können auch ein langes Gesicht machen.
Schützt die Glühbirnen vor dem Lampenfieber.
Schule macht Angst, Angst macht Schule.
Schutzhaft für alle, dann gibt's keine Krawalle.
Schwimmen die Fische mit dem Bauch nach oben, hat der Chef vom AKW gelogen.
Schwitzt der Bauer unterm Arm, wird der Sommer wieder warm.
Seh'n wir uns nicht in dieser Welt, dann seh'n wir uns in Bielefeld.
Sei schlau, bleib dumm.
Seit ich ihm Kitekat ins Essen tue, geht es mir besser als je zuvor.
Selig, wer nichts zu sagen hat und doch schweigt.
Selten Dumme sind nicht selten, aber dumm.
Semmelbrösel in den Socken hält den ärgsten Schweissfuss trocken.
Service ist Verdienst vom Kunden.
Setz dich ruhig in die Nesseln; wer weiss, wie lange es die noch gibt.
Sie giessen Wahnsinn in Beton und Unrecht in Gesetze.
Sie haben die Macht, doch wir haben die Nacht.
Sind die Brötchen leuchtend grün, dann war's Team-Telekom-Urin.
Sitzt der Hahn auf einer Krähe, war kein Huhn in seiner Nähe.
Snobs sind Leute, die sich ihre Petersilie mit FLEUROP ins Haus schicken lassen.
Sogar eine halbe Portion kann ein Doppelleben führen.
"So nehmen Sie doch Vernunft an!"-"Ich darf nichts annehmen, ich bin Beamtin." (Tatort WDR 3, 16.2.2000)
Sommersprossen sind auch Gesichtspunkte.
Sonderlinge lachen sogar beim Zwiebelschneiden.
Spare in der Not, dann hast du Zeit dazu.
Spontaneität will wohlüberlegt sein.
Spieglein, Spieglein im Regal: die Männer sind mir scheissegal.
Sprach Abraham zu Bebraham: "Kann ich mal dein Zebra ham?"
Der Herr zum Knecht: "Heut geht's mir schlecht!" Der Knecht zum Herrn: "Das hört man gern!"
Sprühen bringt Beton zum Blühen.
Sterben ist nicht so schlimm, aber man fühlt sich am nächsten Tag so kaputt.
Sterben muss man sowieso, schneller geht's mit Marlboro.
Steter Tropfen leerts das Hirn.
Steter Tropfen schützt vor Torheit nicht.
Steuern werden immer nur erhoben, nie erniedrigt.
Stille Nacht, heilige Nacht; alles zahlt, ALDI lacht.
Stille Wasser beissen nicht.
Tarzan auf dem Klosterdach: da wurden selbst die Nonnen wach.
Tausche betonierte Zukunft gegen blühende Vergangenheit.
Tausend Volt in den Armen, aber im Kopf die Birne kaputt.
Teigwaren heissen Teigwaren, weil sie mal Teig waren.
To be is to do (Kant). To do is to be (Sartre). Do be do be do (Sinatra).
Tollkirschen schmecken nicht so toll, wie sie heissen.
Trag nie eine Anstecknadel, wenn du erkältet bist.
Treib Sport, oder du bleibst gesund.
Trimm dich, spring mal über deinen Schatten.
Trinkt der Bill viel Kölsch vom Fass, macht's auch mit Hilary wieder Spass.
Tut Ench Amun, was Nofre täte?
Tu was für's Vaterland: wandre aus.
Überlegen macht überlegen.
Und von wem haben Sie Ihre Meinung?
Unfug und Unrecht werden mit Fug und Recht bestraft.
Unrecht Gut gedeiht, nicht?
Unter kleinen Steppdecken kann ein grosser Depp stecken.
Unterstützt die Wiedervereinigung der Spalttablette!
Vater Staat bringt uns noch alle unter Mutter Erde.
Vendi laus amoris, paxe, trixe, caputisse.
Verbietet Posaunenchöre! (Bürgerinitiative Jericho)
Verblühen die Frauen, verduften die Männer.
Verliert im August der Bauer die Hose, war schon im Juli das Gummiband lose.
Viele Ängste sind des Hasen Fuss.
Viele Köche sind des Hasen Tod.
Viele Stoppschilder bringen den Fahrer zum Rasen.
Vorsicht: der Schütze schützt nicht, er schiesst!
Wanzen im Telefon schaffen Unterhaltung.
Warum sachlich werden, wenn es auch persönlich geht.
Waschen allein genügt nicht, man muss auch ab und zu das Wasser wechseln.
Was dem einen sein Beat [bi:t], ist dem anderen seine Beate.
Was dem einen sein Karl May, ist dem anderen sein Sepp Tember.
Was dem einen sein Ulmer Monster, ist dem anderen sein Kölner Gnom.
Was dem Enkel sein Mofa, ist dem Opa sein Sofa.
*Was dem Nessie sein Nessessär, ist der Kuhlen ihr Fridschidär.
Was der Bauer nicht kennt, vergisst er nicht.
Was Du heute hältst geborgen, wird auch morgen Dich versorgen.
Was du heute kannst besorgen, brauchst du morgen nicht zu borgen.
Was du nicht willst, das man dir tu, das tu auch nicht - was willst du denn?
Was keiner kann, das kann ich auch.
Was liegt bei Reisen näher als die Ferne?
Was meinen Sie als Unbeteiligter zum Thema Intelligenz?
Was nicht allzu teuer ist, das können wir erlösen.
Was sagen Sie als Unbeteiligter zum Thema Intelligenz?
Was tut das Volk? Es folgt!
Was Vatikan, kann Mutti schon lange.
Wem du's heute kannst besorgen, den verschone nicht bis morgen.
Wem nicht zu helfen ist, dem ist vielleicht zu schaden.
Wenn Albert ruht, albert Ruth. Und wenn Albert albert, ruht Ruth.
Wenn alle täten, was sie mich könnten, käme ich nicht mehr zum Sitzen.
Wenn alles schläft und einer spricht, den Zustand nennt man Unterricht.
Wenn am Sarg die Witwe kichert, war ihr Alter gut versichert.
Wenn der Bauer schneller rennt, hinter ihm der CASTOR brennt.
Wenn dich Hass und Neid umringen, denk an Götz von Berlichingen.
Wenn die Dunstglocke läutet, hat das Sterbeglöckchen Hochkonjunktur.
Wenn die Erde schreien könnte, wären wir alle taub.
Wenn die Milch nach Krypton schmeckt, hat's im AKW geleckt.
Wenn du nicht willst, du dumme Kuh, dann mach auch keinem andern muh.
Wenn es Politikern die Sprache verschlägt, halten sie eine Rede.
Wenn man das Licht schnell genug ausschaltet, kann man sehen, wie die Dunkelheit aussieht.
Wenn man gut sitzt, braucht man keinen Standpunkt.
Wenn man auch überall aneckt, geht's noch lange nicht rund.
Wenn sich zwei streiten, freut sich der Anwalt.
Wenn Sie nichts zu tun haben, tun Sie's bitte nicht hier.
Wer A sagt, kann auch gleich Halstabletten nehmen.
Wer A sagt, muss auch HOI sagen (Seemannsspruch).
Wer abnehmen möchte, sollte den Mund nicht so voll nehmen.
Wer abnimmt, hat mehr vom Telefon.
Wer am Fleischwolf steht, sollte nicht gleich durchdrehen.
Wer am lautesten quakt, hat die meisten Kröten.
Wer anderen eine Grube gräbt, kommt leicht ins Grübeln.
Wer anderen eine Schule baut, muss selbst hinein.
Wer ATA braucht, ist noch lange nicht bescheuert.
Wer beim Schwimmen ins Schwimmen kommt, geht beim Baden baden.
Wer Blüten druckt, muss rechtzeitig verduften.
Wer dauernd auf die Pauke haut, geht eines Tages flöten.
Wer dem Chef in den Hintern kriecht, muss damit rechnen, dass er ihm eines Tages zum Hals heraushängt.
Wer den Feind umarmt, macht ihn bewegungsunfähig.
Wer den Pfennig nicht ehrt, hat Gold im Mund.
Wer den Schaden hat, braucht für den Schrott nicht zu sorgen.
Wer den Teufel an die Wand malt, spart die Tapete.
Wer die Wahrheit sagt, braucht ein schnelles Pferd.
Wer dir glaubt, wird garantiert nicht selig.
Wer drei Eier durch vier teilt, muss mit einem Bruch rechnen.
Wer seinen Traum verwirklichen will, muss erst mal aufwachen.
Wer faul ist, schaft Arbeitsplätze.
Wer für die Katz arbeitet, kommt auf den Hund.
Wer finden will, der muss verlieren können.
Wer früher stirbt, ist länger tot.
Wer Glauben schenkt, ist ihn los.
Wer glaubt, er wisse, muss wissen, er glaubt.
Wer hat denn den Käse ins Fernsehn gerollt?
Wer heute den Kopf in den Sand steckt, knirscht morgen mit den Zähnen.
Wer heute normal ist, ist nicht mehr normal.
Wer Hundefleisch isst, darf sich nicht wundern, wenn der Magen knurrt.
Wer im Gasthaus sitzt, sollte nicht mit Scheinen werfen.
*Wer im Museum sitzt, sollte nicht mit Schreinen werfen.
*Wer im Schlachthaus sitzt, sollte nicht mit Schweinen werfen.
Wer in sich geht, darf sich nicht wundern, wenn er dort niemanden antrifft (P. Frankenfeld)
Wer kein Schwein ist, wird bald zur Sau gemacht.
Wer keinen Spass versteht, den sollte man nicht ernst nehmen.
Wer kein Geld hat, sollte wenigstens nicht arbeiten.
Wer Klinken putzt, wird schneller krank.
Wer lächeln kann, wenn's schiefgeht, der weiß, wen er verantwortlich machen kann.
Wer langsam geht, kommt auch zu spät.
Wer mehr kann, kann bald nicht mehr.
Wer mit dem Strom schwimmt, treibt irgendwann ins Meer.
Wer mit vierzig noch ein -aner, ist ein geistiger Sextaner.
Wer morgens zerknittert ist, hat den Tag über viel mehr Entfaltungsmöglichkeiten.
Wer nicht hören will, muss fernsehen.
Wer nichts weiss, muss alles glauben.
Wer nichts wird, wird Zwischenwirt.
Wer Ordnung hält, ist nur zu faul zum Suchen.
Wer redet, was er nicht sollte, muss hören, was er nicht wollte.
Wer sich ausschliesslich mit Philosophie beschäftigt, der verblödet.
Wer sich verlobt zur rechten Zeit, braucht nicht zu nehmen, was übrigbleibt.
Wer Stil und Ideen hat, wird Schriftsteller. Wer Stil hat, aber keine Ideen, wird Journalist. Wer weder Stil noch Ideen hat, wird Germanist.
Wer stirbt, ist nur zu faul zum Leben.
Wer sündig durch die Jugend tapst, im Alter meist nach Tugend japst.
Wer sündigt, schläft nicht.
Wer tagelang ohne Getränke auskommt, ist ein Kamel.
Wer trinkt, schadet dem Durst.
Wer über Humor streitet, hat keinen.
Wer vom eigenen Schnarchen aufwacht, sollte das Zimmer wechseln.
Wer Wind sät, scheut das Feuer.
Wer zu allem seinen Senf gibt, gerät in den Verdacht, ein Würstchen zu sein.
Wer zuletzt lacht, hat es nicht früher begriffen.
Wer zuletzt lacht, stirbt wenigstens fröhlich.
Wie man sich fettet, so riecht man.
Wie man sich füttert, so wiegt man.
Will der Bauer schneller pflügen, tät ein Porsche schon genügen.
Will der Mensch die Eier eckig, geht's den Hühnern ganz schön dreckig.
Wir haben schwach angefangen, aber dafür lassen wir stark nach.
Wird das Leben dir zuviel, trink doch rasche 'ne Flasche Pril.
Wir fordern Haftpflicht für künstliche Gebisse.
Wir sind zu nichts zu gebrauchen, aber zu allem fähig.
Wir sparen jeden Pfennig - koste es was es wolle.
Wirst du des Lebens nicht mehr froh, dann stürze dich in H2O.
Wir wollen endlich alle Kanzler werden.
Wir wollen keine Entsorgung; lasst uns wenigstens unsere Sorgen.
Wissen ist Macht; nichts wissen macht nichts.
Wo die Frau nicht kocht, da kocht der Mann.
Wo eine Villa ist, ist auch ein Weg.
Woher soll ich wissen, was ich denke, bevor ich gehört habe, was ich sage?
Wo nix läuft, läuft der Fernseher [oder: Computer].
Wo viel Lid ist, ist auch viel Schatten.
Wozu AKWs? Bei uns kommt der Strom aus der Steckdose.
Wozu Flüsse und Seen? Bei uns kommt das Wasser aus der Leitung.
Wohltätig ist des Feuers Macht, entsteht kein Brandstiftungsverdacht.
Wut tut gut.
Zeige mir Deine Krawatte und ich sage Dir, was Du gegessen hast.
Zum Leben muss man geboren sein.
Zwei im Büro, und einer arbeitet? Ein Beamter und ein Ventilator."""

	de = LANGS.peek('de')
	for line in s.split('\n'):
		q.appendRow(de,line)
	#return s.split('\n')

	#db.flush()


#http://www.sternstunden-des-lebens.net/weisheiten.htm
# (c) Sternstunden des Lebens
		
def populate2(db,**kw):
	db.installto(globals())
	
	s = """\

   1.

      Sobald wir verstanden haben dass, das Geheimnis des Glücks 
      nicht im Besitz liegt sondern im Geben, werden wir, 
      indem wir um uns herum glücklich machen, selbst glücklich werden.
      Verfasser unbekannt

       
   2.

      Die Schönheit der Natur, ihre Farben und Düfte,
      sind ein Ausdruck von Gottes Liebe
      für uns Menschen.
      Verfasser unbekannt

   3.

      Es ist nicht so wichtig, wie lange unser Leben währt,
      sondern welche Qualität wir dem Leben geben,
      wie wir es sinnvoll gestalten
      und wie viel Freude und Liebe wir weitergeben.
      Verfasser unbekannt

   4.

      Meistens entsteht Unglück allein durch
      die falsche Art über etwas nachzudenken.
      Verfasser unbekannt

   5.

      Was jemand glaubt, das will er glauben.
      Verfasser unbekannt

   6.

      Wie wir in unserem Herzen sind,
      so sind wir zum Herzen des Anderen.
      Verfasser unbekannt

   7.

      Achte stets auf deine Gedanken, sie werden zu Worten.
      Achte auf deine Worte, sie werden zu Handlungen.
      Achte auf deine Handlungen, sie werden zu Gewohnheiten.
      Achte auf deine Gewohnheiten, sie werden zu Charaktereigenschaften.
      Achte auf deinen Charakter, er wird dein Schicksal .
      Verfasser unbekannt
   8.

      Wer mit dem Strom schwimmt, landet irgendwann im Meer.
      Wer sich gegen den Strom bewegt gelangt sicher zur Quelle.
      Verfasser unbekannt

   9.

      Ich erkenne jetzt, dass alles zusammengehört.
      Ohne das etwas stirbt, gibt es kein Neuwerden,
      ohne Schwere, keine Flügel.
      Ingrid Abel

  10.

      Ausdauer ist ein Talisman für das Leben.
      Afrikanisches Sprichwort

  11.

      Wende dein Gesicht der Sonne zu,
      dann lässt du die Schatten hinter dir.
      Afrikanisches Sprichwort

  12.

      Nimm das Wohlwollen aus dem menschlichen Verkehr,
      und es wird sein, als hättest
      du die Sonne aus der Welt genommen.
      Ambrosius

  13.

         Nur wenigen Menschenherzen ist es eingepflanzt,
      den Freund, umlacht von Segen,
      ohne Neid zu schauen.
      Aischylos

  14.

      Der Mensch hat das Wissen immer gehabt; er hat gewusst, 
      dass das Leben grundsätzlich gut ist, dass das Universum, die Sterne am Himmel, die Tiere, Pflanzen, Mineralien, 
      die Elemente der Erde nicht feindselig sind, 
      sondern kosmisch mit sinnstiftender Ordnung erfüllt sind.
      Der Sinn ist die innewohnende Heiligkeit, 
      die Ordnung des Universums.
      Als der Mensch diese Heiligkeit noch wahrgenommen, 
      ja, sie durch Bescheidenheit und geistige Ausrichtung in 
      das Muster seines Herzens gewebt hat, da hat auch die menschliche Gesellschaft diese Heiligkeit und Ordnung reflektiert, 
      die allen Dingen innewohnt.
      Jose' Arguelles

  15.

      Was ewig ist, ist kreisförmig, und was kreisförmig ist, ist ewig.
      Aristoteles

  16.

      Klug kann nur ein guter Mensch sein.
      Aristoteles

  17.

      Nichts tut die Natur zwecklos.
      Aristoteles

  18.

      Was gut ist, wird, wenn es in die Jahre kommt, immer noch besser.
      Herbert Asmodi

  19.

      Ärgere dich nicht darüber, dass der Rosenstrauch Dornen trägt, 
      sondern freue dich darüber, das der Dornenstrauch Rosen trägt.
      Arabisches Sprichwort

  20.

      Finde dich, sei dir selber treu,
      lerne dich verstehen, folge deiner Stimme,
      nur so kannst du das Höchste erreichen.
      Bettina von Arnim

  21.

      Die Zeit kommt aus der Zukunft,
      die nicht existiert,
      in der Gegenwart, die keine Dauer hat,
      und geht in die Vergangenheit,
      die aufgehört hat zu bestehen.
      Aurelius Augustinus

  22.

      Der hat immer etwas zu geben,
      dessen Herz voll ist von Liebe.
      Aurelius Augustinus

  23.

       Dringe in das Innere der Menschenseele ein, 
      und du wirst sehen,
      vor was für Richtern du dich fürchtest 
      und was für Richter sie über sich selbst sind.
      Marc Aurel

  24.

      Vergiss nicht - 
      man benötigt nur wenig, um ein glückliches Leben zu führen.
      Marc Aurel

  25.

      Keinem Menschen widerfährt etwas,
      das er nicht seiner Natur nach auch ertragen könnte.
      Marc Aurel




  26.

      Die Liebe lebt vom Geben und Vergeben.
      Das Selbst lebt vom Nehmen und Vergessen.
      Sathya Sai Baba

  27.

      Wenn ihr mich fragt, wie man sich entspannt,
      dann sage ich: Tut gar nichts.
      Entspannt euch einfach.
      Legt euch hin und wartet ab, ohne das geringste zu tun,
      denn was auch immer ihr tut, ist ein Hindernis.
      Bhagwan Shree Rajneesh

  28.

      Unsere Träume können wir erst dann verwirklichen,
      wenn wir uns entschließen, einmal daraus zu erwachen.
      Josephine Baker

  29.

      Die Liebe erscheint als das schnellste, 
      ist jedoch das langsamste aller Gewächse. 
      Für jeden Menschen kommt einmal der Augenblick, 
      wo er sein Leben ändern muss,
      um sich aufs Wesentliche zu konzentrieren.
      Grigori Baklanow

  30.

      Für jeden Menschen kommt einmal
      der Augenblick, wo er sein Leben ändern muss, 
      um sich aufs Wesentliche zu konzentrieren.
      Grigori Baklanow

  31.

      Die Erinnerungen verschönern das Leben, 
      aber das Vergessen allein macht es erträglich
      Honore de Balzac

  32.

      Durchdenke das Verständliche und du kommst zu dem Schluss, 
      dass nur das Unverständliche Licht spendet.
      Saul Bellow

  33.

      Wissen nennen wir jenen kleinen Teil der Unwissenheit,
      den wir geordnet und klassifiziert haben.
      Ambrose Bierce

  34.

      Es ist eine Kraft der Ewigkeit,
      und diese Kraft ist grün.
      Hildegard von Bingen

  35.

      Das Vertrauen ist eine zarte Pflanze.
      Ist es zerstört, so kommt es sobald nicht wieder.
      Otto von Bismark

  36.

      Würden die Pforten der Wahrnehmung gereinigt,
      erschiene den Menschen alles so, wie es ist:
      unendlich.
      William Blake

  37.

      Es gibt Dinge, die sind unbekannt und es gibt Dinge, 
      die sind bekannt, dazwischen gibt es Türen.
      William Blake

  38.

        Wer A sagt, muss auch B sagen.
      Er kann auch erkennen das A falsch war.
      Berthold Brecht

  39.

      Ehrlichkeit ohne Offenheit ist wie ein Haus ohne Tür.
      Andre Brie

  40.

      Nichts bereuen ist aller Weisheit Anfang
      Ludwig Böme

  41.

      Die Bewunderung preist, die Liebe ist stumm.
      Ludwig Böme

  42.

      Freude ist keine Gabe des Geistes;
      sie ist eine Gabe des Herzens.
      Ludwig Böme

  43.

      Nimm dir Zeit, um glücklich zu sein.
      Zeit ist keine Schnellstrasse
      zwischen Wiege und Grab,
      sondern Platz zum Parken in der Sonne.
      Phil Bosmans

  44.

        Die Zeit ist von der Art des Lebens,
      das uns geheimnisvoll geschenkt,
      das in eigenartigem
      und unabänderlichen Rhythmus dahinfließt,
      das wiederum geheimnisvoll aufhört,
      um sich in ewiges Leben zu wandeln.
      Theodor Bovet

  45.

      Nimmer vergeht die Seele, vielmehr vergeht die frühere Wohnung, 
      welche sie mit neuem Sitze tauscht und lebt und wirket in diesem. 
      Alles wechselt, doch nichts geht unter.
      Giordano Bruno

  46.

      In jedermann ist etwas Kostbares, 
      das in keinem anderen ist.
      Martin Buber

  47.

      Sie sagen DU zum Baum und geben sich ihm hin,
      und er sagt DU zu Ihnen und gibt sich Ihnen hin.
      Etwas leuchtet auf und nähert sich uns
      von der Quelle des Seins.
      Martin Buber

  48.

      Alles, was wir sind,
      ist das Ergebnis dessen,  was wir dachten.
      Buddha

  49.

      Glaube nicht an das, was du gehört hast;
      glaube nicht an die Überlieferungen, 
      weil sie von Generation zu Generation weitergegeben worden sind;
      glaube nicht an das, was als Gerücht umgeht oder in vieler Munde ist; 
      glaube nicht einfach deswegen, 
      weil ein schriftliches Zeugnis eines alten Weisen vorgelegt wird;
      glaube nicht an Mutmaßungen;
      glaube nicht an das als wahr,
      woran du dich durch Gewohnheit gebunden hast;
      glaube nicht einfach an die Autorität deiner Lehrer und Älteren.
      Nach Beobachtung und Analyse, 
      wenn etwas mit Vernunft übereinstimmt 
      und Wohl und Nutzen des einzelnen und der Gesamtheit fördert, 
      dann nimm es an, übe es und lebe danach.
      Buddha

  50.

      Ereignisse geschehen, Handlungen werden ausgeführt,
      doch es gibt keinen individuellen Täter oder Handelnden,
      der sie ausführt.
      Buddha

  51.

      Wahrheit ist das, was funktioniert.
      Buddha




  52.

       Solange das Gehirn ein Geheimnis ist, 
      wird auch das Universum ein Geheimnis bleiben.
      Santiago Ramony Cajal

  53.

      Erst wenn man die Oberfläche der Dinge kennen gelernt hat, 
      kann man sich aufmachen, herauszufinden, was darunter sein mag.
      Doch die Oberfläche der Dinge ist unerschöpflich.
      Italo Calvino

  54.

      Die Erde ist ein Ganzes. 
      Die Menschheit ist ein Ganzes.
      Der Kosmos ist ein Ganzes.
      Und ich selbst bin dieses Ganze.
      Don Juan Castaneda

  55.

      Die Welt ist nur "dies - und - das"
      oder "so - und - so" weil wir uns sagen, 
      dass sie so sei.
      Don Juan/Castaneda

  56.

      Bis zu diesem Jahrhundert hat sich die menschliche Evolution
      ohne unser Bewusstsein entfaltet.
      Die enorme Veränderung, die das 20. Jahrhundert mit sich brachte,
      besteht vor allem darin, dass die menschliche Evolution
      sich von nun an bewusst vollziehen wird.
      James Redfield, Celestine

  57.

      Tue alles im Geist des Loslassens. 
      Erwarte weder Lob noch Gewinn. 
      Wenn du wenig loslässt, wirst du wenig Frieden haben. 
      Wenn du viel loslässt, wirst du viel Frieden haben. 
      Wenn du ganz loslässt, dann wirst du wissen, 
      was Frieden und Freiheit wirklich sind. 
      Deine Kämpfe mit der Welt werden zu Ende sein.
      Achaan Chah

  58.

      Heilen heißt nicht vergessen.
      Heilen heißt, dass du dich innerlich davon frei machen kannst, 
      dein Leben vom Gestern bestimmen zu lassen.
      Celli

  59.

      Ein Tag ohne Lächeln ist ein verlorener Tag.
      Sir Charles Spencer Chaplin (Charlie Chaplin)

  60.

      Wenn ich einen grünen Zweig im herzen trage,
      wird sich ein Singvogel darauf niederlassen.
      Chinesisches Sprichwort

  61.

      Wissen ist ein Schatz,
      der seine Besitzer überallhin begleitet.
      Chinesisches Sprichwort

  62.

         Nicht die Gabe ist kostbar,
      sondern die Liebe mit der sie gegeben wird.
      Chinesisches Sprichwort

  63.

      Verwandle große Sorgen in kleine und kleine in gar keine.
      Chinesisches Sprichwort

  64.

      Wer keinen Eifer zeigt,
      dem soll man nichts erklären.
      Chinesisches Sprichwort

  65.

      Steigst du nicht auf die Berge,
      so siehst du auch nicht in die Ferne.
      Chinesisches Sprichwort

  66.

         Wer nach dem Guten strebt, hat niemals ausgelernt.
      Er bleibt immer ein Schüler
      Chinesische Volksweisheit

  67.

      Die Menschheit ist zu weit vorwärtsgegangen, 
      um sich zurückzuwenden, 
      und bewegt sich zu rasch, um stehen zu bleiben.
      Winston Churchill

  68.

      Wird das Nachdenken über irgend ein
      Problem auf die lange Bank geschoben,
      dann bleibt erfahrungsgemäß keine Zeit,
      das Problem überhaupt gründlich zu durchdenken.
      C. West Churmann

  69.

      Jeder Mensch kann irren,
      der Dumme nur verharrt im Irrtum.
      Marcus Tullius Cicero

  70.

      Durch Zweifel gelangen wir zur Wahrheit.
      Marcus Tullius Cicero

  71.

      Suche nicht andere,
      sondern dich selbst zu übertreffen.
      Marcus Tullius Cicero

  72.

      Nicht geboren zu werden ist unbestreitbar die beste Lösung, 
      die es gibt. Leider steht sie in niemanden's Macht.
      E. M. Cioran

  73.

      Die großen Gedanken kommen aus dem Herzen.
      Luc de Clapier

  74.

      Demut ist der Grundstein des Guten. 
      Mit jenem Sinn im Herzen kann der Mensch ein gutes Gewissen haben 
      und ruhig abwarten, dass ihm vom Himmel gegeben werde, 
      was sich der Mensch nicht nehmen kann.
        Matthias Claudius

  75.

      Wenn wir auch nicht sicher wissen, wie eine Handlung ausgeht,
      so müssen wir doch handeln, 
      denn sonst kommt es zu keiner Veränderung. 
      Ein Fehlgreifen in der Wahl der Mittel ist besser, als nichts zu tun. 
      Clausewitz
       
  76.

      Das wahre Glück besteht nicht in dem, was man empfängt,
      sondern in dem, was man gibt.
      Johannes Chrysostomus






#

Jung zu bleiben und alt zu werden ist das höchste Gut.
Deutsches Sprichwort

#

Ein bisschen Güte von Mensch zu Mensch,
ist besser als alle Liebe zur Menschheit.
Richard Dehmel

#

Das Wachstum eines Mannes wird immer dann optimiert,
wenn er seine Grenzen, seine Beschränkungen,
seine Ängste ein klein wenig hinter sich lässt.
Er sollte nicht zu faul sein und in der Zone der Sicherheit
und des Wohlbehagens stagnieren.
Er sollte seine Grenzen aber auch nicht zu weit überschreiten,
sich nicht selbst unnötig unter Druck setzen
und unfähig werden, seine Erfahrungen zu verdauen.
Er sollte die Grenzen seiner Angst und seines Unbehagens
immer ein klein wenig hinter sich lassen.
Ständig. In allem, was er tut.
David Deida

#

Beschreibt man die Bedeutung der Worte
so genau wie möglich, dann wird man die Menschheit
von der Hälfte ihrer Irrtümer befreien.
René Descartes

#

Das Privileg der Götter wie der Menschen ist das Lachen.
Demokrites

#

Nichts auf der Welt ist so gerecht verteilt wie der Verstand.
Niemand glaubt, mehr davon zu brauchen als er hat.
René Descartes

#

Im übrigen haben es diejenigen, die befähigt sind, 
sich von Vorurteilen zu befreien, 
nicht nötig, sich belehren zu lassen.
Denis Diderot

#

Mitternacht. Keine Wellen, 
kein Wind, das leere Boot ist vom Mondlicht überflutet.
Dogen

#

Völlig frei wird der Mensch nur dann, wenn es ihm einerlei sein wird, 
ob er lebt oder nicht. Das ist das Ziel aller Bestrebungen.
Dostojewski

#

Es scheint wohl wahr zu sein, dass die zweite Hälfte des menschlichen Lebens
sich gewöhnlich nur aus Gewohnheiten zusammensetzt,
die man in der ersten Hälfte erworben hat.
Dostojewski

#

    Geborenwerden und Sterben, Leben und Tod,
Glück und Unglück, Lob und Tadel,
Hunger und Durst, Hitze und Kälte-
alle sind sie Wechselbilder natürlicher
Gegebenheiten und schicksalhafter Zufälle.
Deswegen die innere Harmonie stören lassen,
lohnt nicht die Mühe.
Dschuang Dsi

#

  Die Zeit für das Glück
ist heute, nicht morgen.
Ein Strom von Gelegenheiten
fließt ununterbrochen an uns vorüber:
wo immer wir sind und
was immer wir tun.
David Dunn

#

Je planmäßiger der Mensch vorgeht,
um so wirkungsvoller trifft ihn der Zufall.
Friedrich Dürrenmatt

#

Der Schatten ist das Licht 
in der Gestalt dessen, der es verstellt.
Dürckheim

#

Die Liebe ist ein Spielzeug für Augenblicke, 
das Aufbrausen des jungen Blutes;
das Herz ist das Beben nicht gestählter Nerven.
Józef Dzierzkowski

#

   Unsere größte Schwäche liegt im Aufgeben.
Der sicherste Weg zum Erfolg ist immer,
es doch noch einmal zu versuchen.
Thomas Alva Edison

#

Es gibt keinen Gott,
es ist Gott.
Andreas Eggebrecht

#

Schönheit ist die Kunst, das Geheimnis zu bewahren.
Andreas Eggebrecht 

#

Das Anerkennen des Nicht-Erkennbaren ist die Voraussetzung,
Zugang zur Weite der Wirklichkeit zu finden. 
Es erfordert ein "Beiseitetreten" des Verstandes oder 
ein Heraustreten aus dem Verstand.
Nicht erkennbar zu sein ist ein wesentlicher Aspekt
der unendlichen Weite. 
Sie ist ein Raum, der nicht mit dem Verstand betreten werden kann.
Andreas Eggebrecht

#

Ein Freund ist ein Mensch,
vor dem man laut denken kann.
Ralph Waldo Emerson

#

Man muss das Gute tun, damit es in der Welt sei.
Marie von Ebner - Eschenbach




#

Man muss sein Glück teilen, um es zu multiplizieren.
Marie von Ebner - Eschenbach

#

An das Gute glauben nur die wenigen,
die es üben.
Marie von Ebner - Eschenbach

#

Wenn es einen Glauben gibt,
der Berge versetzen kann,
so ist es der Glaube an die eigene Kraft.
Marie von Ebner - Eschenbach

#

Wirklich gute Freunde sind Menschen,
die uns ganz genau kennen und trotzdem zu uns halten.
Marie von Ebner - Eschenbach

#

Es ist ja das Ziel jeder Tätigkeit des Intellekts, 
ein "Wunder" in etwas zu verwandeln, 
was man begreifen kann.
Albert Einstein

#

Fantasie ist wichtiger als Wissen.
Albert Einstein

#

Es ist schwieriger, eine vorgefasste Meinung
zu zertrümmern als ein Atom.
Albert Einstein

#

Der wahre Wert eines Menschen ist in erster Linie
dadurch bestimmt, in welchem Grad und im welchem Sinn er zur
Befreiung vom Ich gelangen kann.
Albert Einstein

#

Der Mensch vermeidet es gewöhnlich, 
einem anderen Klugheit zuzuschreiben, 
wenn es sich nicht etwa um einen Feind handelt.
Albert Einstein

#

Das schönste und tiefste Gefühl, das wir erleben können, 
ist die Empfindung des Mystischen. 
Sie ist Quelle aller wahren Wissenschaft. 
Wem dieses Gefühl fremd ist, wer nicht mehr staunen
und nicht mehr in Ehrfurcht versinken kann, der ist so gut wie tot. 
Zu wissen, dass das, was für uns undurchdringlich ist, 
wirklich existiert und sich als höchste Weisheit 
und strahlende Schönheit manifestiert, 
von unseren stumpfen Sinnen nur in primitivster Form erfasst - 
dieses Wissen, dieses Gefühl ist der Kern wahrer Religiosität. 
Meine Religion besteht in bescheidener Ehrfurcht vor dem Höheren, 
das sein Licht in den kleinsten Details offenbart, 
die wir mit unserem schwachen, zerbrechlichen Geist wahrnehmen können. 
Die tiefe Überzeugung, dass es eine übergeordnete Vernunft gibt,
deren Kraft sich im unermesslichen Universum offenbart, 
bildet meine Idee von Gott.
Albert Einstein

#

Ich will Gottes Gedanken kennenlernen.
Der Rest ist Nebensache.
Albert Einstein

#

Je mehr eine Kultur begreift, dass ihr aktuelles Weltbild eine Fiktion ist, 
desto höher ist ihr wissenschaftliches Niveau.
Albert Einstein

#

Kein Ziel ist so hoch,
dass es unwürdige Methoden rechtfertige.
Albert Einstein

#

Frieden kommt in die Seelen der Menschen, 
wenn sie ihre Einheit mit dem Universum erkennen und wissen,
dass im Mittelpunkt der Welt das Große Geheimnis wohnt
und dass diese Mitte in jedem von ist.
Black Elch

#

 Ein Freund ist ein Mensch,
vor dem man laut denken kann.
Ralph Waldo Emerson

#

Handle, und das Geschick selbst beugt sich!
Ralph Waldo Emerson

#

Die Intelligenz nimmt in dem Maße zu, 
wie der Mensch die Welt erkennt. 
Empedokles

#

Nicht die Sprüche sind es, woran es fehlt; 
Die Bücher sind davon voll. 
Woran es fehlt sind die Menschen, die sie anwenden.
Epiktet

#

Nicht darauf richte deinen Sinn, dass die Dinge gehen,
wie du wünschest,
sondern dass du wünschest, wie die Dinge gehen -
so wirst du gute Fahrt haben.
Epiktet

#

Man darf das Schiff nicht an einen einzigen Anker
und das Leben nicht an eine einzige Hoffnung binden.
Epiktet

#

Reich ist man nicht durch das, was man besitzt,
sondern mehr durch das,
was man mit Würde zu entbehren weiß.
Epikur




#

Das Wort ist die schlichte Gewalt des Gedankens, 
das all seine Berechtigung, 
all seine Eleganz aus seiner vollkommenen Übereinstimmung 
mit der wiederzugebenden Idee bezieht.
Dominique Fernandez

#

Unsere Erde ist nur ein kleines Stück dieses Weltalls, 
aber ihre Gesetze sind die des ganzen Weltgebäudes.
Fersman

#

Sich zu beeilen nützt nichts.
Zur rechten Zeit aufzubrechen, ist die Hauptsache.
Jean de la Fontane

#

Es gibt nur ein Mittel, sich wohl zu fühlen: Man muss lernen,
mit dem gegebenen zufrieden zu sein
und nicht immer das verlangen, was gerade fehlt.
Theodor Fontane

#

Das wichtigste für den Menschen,
ist der Mensch, da liegt nicht bloß sein Glück,
da liegt auch seine Gesundheit.
Theodor Fontane

#

Die meisten Menschen verwenden mehr, Kraft darauf,
um die Probleme herumzureden, statt sie anzupacken
Henry Ford

#

Erhören - ohne zu verurteilen
Nahebringen - ohne überzeugen zu wollen
Geben - ohne zu erwarten
Einfühlen - ohne sich selbst zu verlieren
Lieben - ohne zu besitzen
Sabrina Fox

#

Wer euch sagt, dass ihr anders reich werden könnt
als durch Arbeit und Sparsamkeit,
der betrügt Euch, der ist ein Schelm.
Benjamin Franklin

#

Jemanden zu lieben, ist nicht einfach nur ein
starkes Gefühl - es ist eine Entscheidung,
es ist ein Urteil, es ist ein Versprechen. 
Erich Fromm












 126.

      Die Frucht des Geistes ist Liebe, Freude, Frieden Geduld,
      Freundlichkeit, Güte und Treue.
      Galater 5, 22

 127.

      Genieße, was dir Gott beschieden,
      entbehre gern, was du nicht hast;
      ein jeder Stand hat seinen Frieden,
      ein jeder Stand hat seine Last.
      Christian Fürchtegott Gellert

 128.

      Du kannst deinen Kindern deine Liebe geben, 
      aber nicht deine Gedanken, 
      denn sie haben eigene Gedanken.
      Kahlil Gibran

 129.

      Wenn du arbeitest, bist du eine Flöte,
      durch deren Herz sich das Flüstern der Stunden
      in Musik verwandelt.

      Und wenn man mit Liebe arbeitet?
      Dann webt man Fäden in das Tuch,
      die dem Herzen entstammen, so,
      als würde die eigene Geliebte dieses Tuch tragen.
      Khalil Gibran

 130.

      Von den Geschwätzigen habe ich das Schweigen gelernt.
      Von den Intoleranten, die Toleranz
      und von Unfreundlichen die Freundlichkeit.
      Ich sollte diesen Lehrern nicht undankbar sein! 
      Kahlil Gibran

 131.

      Der Mensch kann nicht zu neuen Ufern vordringen,
      wenn er nicht dem Mut aufbringt,
      die alten zu verlassen.
      André Gide

 132.

      Das verkörperte Lebewesen empfindet gegenüber
      den Sinnesobjekten Anziehung und Abneigung.
      Doch sollte man vermeiden,
      unter die Herrschaft der Sinne und der
      Sinnesobjekte zu geraten,
      denn sie sind Hindernisse auf dem Pfad zur Selbstverwirklichung.
      Bhagavad-Gita, Kap. 3, Vers 34

 133.

      Die Laster stritten, wer von ihnen am eifrigsten 
      gewesen sei, dem Bösen auf der Welt zu dienen; 
      den Preis erhielt die Heuchelei.
      Johann Ludwig Glenn

 134.

      Nichts bleibt weniger genutzt 
      als zweckmäßige Tätigkeit.
      Johann Wolfgang von Goethe

 135.

      Derjenige, der sich mit Einsicht für beschränkt erklärt,
      ist der Vollkommenheit am nächsten.
      Johann Wolfgang von Goethe

 136.

      Willst du aber das Beste tun,
      so bleib nicht auf dir selber ruhn
      sondern folg eines Meisters Sinn,
      mit ihm zu irren, ist dir Gewinn
      Johann Wolfgang von Goethe

 137.

      In der Ehe muss man sich manchmal streiten.
      Nur so erfährt man etwas voneinander.
      Johann Wolfgang von Goethe

 138.

      Nichts ist gefährlicher für die neue Wahrheit 
      als der alte Irrtum.
      Johann Wolfgang von Goethe

 139.

        Leider lässt sich eine wahre Dankbarkeit
      mit Worten nicht ausdrücken.
      Johann Wolfgang von Goethe

 140.

      Alles Vergängliche ist nur ein Gleichnis;
      das Unzulängliche, hier wird's Ereignis;
      das Unbeschreibliche, hier ist's getan;
      das Ewig-Weibliche zieht uns hinan.
      Johann Wolfgang von Goethe (Faust II)

 141.

      Was immer Du auch tun kannst 
      oder erträumst zu können, 
      beginne es. 
      Kühnheit besitzt Genie, 
      Macht und magische Kraft. 
      Beginne es jetzt. 
      Johann Wolfgang Goethe

 142.

      Dein Geist wird dich leiten,
      in jedem Augenblick das Rechte zu wirken.
      Johann Wolfgang von Goethe

 143.

      Wir behalten von unseren Studien am Ende nur noch das,
      was wir praktisch anwenden.
      Johann Wolfgang von Goethe

 144.

      Lehre tut viel,
      aber Aufmunterung tut alles.
      Johann Wolfgang von Goethe

 145.

      Wer die menschliche Schönheit erblickt, 
      den kann nichts Übles anwehen: 
      er fühlt sich mit sich selbst und der 
      Welt in Übereinstimmung.
      Johann Wolfgang von Goethe

 146.

      Auch aus Steinen, die in den Weg gelegt werden,
      kann man schönes bauen.
      Johann Wolfgang von Goethe

 147.

      Das ist ewig wahr:
      Wer nichts für andere tut,
      tut nichts für sich.
      Johann Wolfgang von Goethe

 148.

      Des Menschen Seele gleicht dem Wasser:
      Vom Himmel kommt es, Zum Himmel steigt es,
      Und wieder nieder Zur Erde muss es,
      Ewig wechselnd.
      Johann Wolfgang von Goethe

 149.

      Ich bin gewiss, wie Sie mich hier sehen, 
      schon tausendmal dagewesen zu sein, 
      und hoffe, wohl noch tausendmal  wiederzukommen. 
      Johann Wolfgang von Goethe

 150.

      Eigentlich weiß man nur, wenn man wenig weiß;
      mit dem Wissen wächst der Zweifel.
      Johann Wolfgang von Goethe

 151.

      Mit dem wissen wächst der Zweifel.
      Johann Wolfgang von Goethe

 152.

      Nutze deine jungen Tage,
      lerne zeitig klüger sein.
      Auf des Glückes großer Waage
      steht die Zunge selten ein.
      Du musst steigen oder sinken,
      du musst herrschen und gewinnen
      oder dienen und verlieren,
      leiden oder triumphieren,
      Amboss oder Hammer sein!
      Johann Wolfgang von Goethe

 153.

      Unsere Wünsche sind Vorgefühle der Fähigkeiten, 
      die in uns liegen, Vorboten desjenigen,
      was wir zu leisten imstande sein werden.
       Johann Wolfgang von Goethe

 154.

      Die Güte des Herzens nimmt einen weiteren Raum ein,
      als der Gerechtigkeit geräumiges
      Johann Wolfgang von Goethe

 155.

      Unglück bildet den Menschen und zwingt ihn,
      sich selber zu kennen.
      Leiden gibt dem Gemüt doppeltes Streben nach Kraft.
      Uns lehrt eigener Schmerz,
      der anderen Schmerzen zu teilen.
      Eigener Fehler erhält Demut und billigen Sinn.
      Johann Wolfgang von Goethe

 156.

       „Du hast gar vielen nicht gedankt,
      die dir so manches Gute gegeben!“
      Darüber bin ich erkrankt,
      ihre Gaben mir im Herzen Leben.
      Johann Wolfgang von Goethe

 157.

      Bewusstsein ist das Medium für die Botschaften,
      aus denen sich Erfahrung zusammensetzt.
      Psychotherapien befassen sich mit diesen Botschaften 
      und ihrer Bedeutung; Meditation hingegen 
      ist auf das Wesen des Mediums,
      das Bewusstsein selbst, gerichtet.
      Diese beiden Ansätze schließen sich in keiner Weise aus,
      vielmehr ergänzen sie sich gegenseitig.
      Die Therapie der Zukunft wird vielleicht die Techniken 
      beider Ansätze verbinden und dadurch 
      eine tiefgreifende Veränderung im Menschen bewirken, 
      als es eine der beiden Methoden für sich allein könnte.
      Daniel Goleman

 158.

      Durch die Parallelität von Körper, Geist und Rede, 
      die Koordination von Bewegung, Gedanken und Wort
      und die Harmonie von Gefühl, schöpferischer Phantasie,
      Vorstellungskraft und verbalem Ausdruck gelangen wir
      zur Einheit aller Funktionen unseres bewussten Seins;
      dadurch wird nicht nur die Oberfläche 
      unserer Persönlichkeit verändert
      - nämlich unsere Sinne unser Intellekt -
      sondern auch die tieferen Regionen unseres Geistes.
      Durch die regelmäßige Ausübung eines solchen religiösen Ritus
      werden die Grundlagen unseres Wesens langsam,
      aber sicher transformiert und für das innere Licht empfänglich.
      Lama Govinda

 159.

      Wenn etwas gehört werden soll,
      muss man Männer fragen.
      Wenn etwas getan werden soll, 
      muss man Frauen fragen.
      Raissa Gorbatschowa

 160.

        Nicht im Kopfe,
      sondern im Herzen liegt der Anfang!
      Maxim Gorki

 161.

       Wenn doch die Leute dächten, dass nicht die Gaben 
      Gott wohl gefallen,
      sondern das Herz, das die Gaben gibt!
      Jeremias Gotthelf

 162.

      Jemandem große Verbindlichkeiten
      schuldig zu sein, hat nichts
      Unangenehmes, denn die
      Dankbarkeit ist eine süße Pflicht.
      Nur kleine Verpflichtungen sind quälend.
      Franz Grillparzer

 163.

       Will unsere Zeit mich bestreiten, ich lass es ruhig geschehen.
      Ich komme aus anderen Zeiten, um fort in andere zu gehen. 
      Franz Grillparzer

 164.

      Schlechte Argumente bekämpft man am besten dadurch, 
      dass man ihre Darlegung nicht stört.
      Alec Guinness









 165.

      Unsere Sicht der Evolution wird sich gänzlich wandeln.
      Es wird sicherlich weiterhin den Begriff
      der Natürlichen Auslese geben und den der Mutation und der DNS. 
      Aber an Stelle einer mechanischen Evolution
      durch Zufallsereignisse, die dann am Ende Bewusstsein
      hervorbringt, wird die Auffassung treten,
      dass Bewusstsein der Rahmen ist,
      in dem die materielle Evolution sich abspielt,
      und dass Bewusstsein schon immer existierte.
      Willis Harman ( Institute of Noetic Sciences, Kalifornien)

 166.

        Katastrophen stören unseren Schlaf,
      aber sie rufen uns zur Besinnung.
      Ernst. R. Hauschka

 167.

      Die Freiheit ist wie das Meer: 
      Die einzelnen Wogen vermögen nicht viel, 
      aber die Kraft der Brandung ist unwiderstehlich.
      Vaclav Havel

 168.

      Das wahre und sichtbare Glück des Lebens liegt nicht außerhalb,
      sondern in uns.
      J. P. Hebel

 169.

      Alle Gelegenheit, glücklich zu werden, hilft nichts,
      wer den Verstand nicht hat, sie zu benutzen.
      Johann Peter Hebel

 170.

      Mit Blitzen kann man die Welt erleuchten, 
      aber keinen Ofen heizen. 
      Friedrich Hebbel

 171.

      Es gehört mehr Mut dazu, seine Meinung zu ändern,
      als ihr treu zu bleiben.
      Friedrich Hebbel

 172.

      Genie ist Bewusstheit in der Welt.
      Friedrich Hebbel

 173.

      Wahrheit ist es, vor der die Meinung erbleicht.
      Hegel

 174.

      Wir kommen nie zu Gedanken.
      Sie kommen zu uns.
      Martin Heidegger

 175.

      Wir kommen für die Götter zu spät
      und zu früh für das Sein.
      Dessen angefangenes Gedicht ist der Mensch.
      Martin Heidegger

 176.

      Oh Mensch! Gib Acht!
      Aller Mut des Gemüts ist der Widerklang
      auf die Anmutung des Seins, die unser Denken
      in das Spiel der Welt versammelt.

      In der Langmut gedeiht Großmut.
      Wer groß denkt, muss groß irren.
      Martin Heidegger

 177.

      Furcht ist Furcht vor etwas,
      Angst ist Angst vor nichts.
      Martin Heidegger

 178.

      Der Glaube der meisten Menschen 
      ist Befangenheit ohne Klarheit.
      Heinse

 179.

      Niemand weiß,
      was in ihm drinsteckt,
      solange er nicht versucht hat,
      es herauszufinden.
      Ernest Hemingway

 180.

      Das Denken ist der größte Vorzug,
      und die Weisheit besteht darin,
      die Wahrheit zu sagen und nach der Natur zu handeln,
      auf sie hinhörend. 
      Heraklit

 181.

      Es gibt nichts Dauerhaftes außer der Veränderung.
      Heraklit

 182.

      Nicht gut ist, dass sich alles erfüllt, was du wünschest,
      durch Krankheit erkennst du den Wert der Gesundheit,
      am Bösen den Wert des Guten,
      durch Hunger die Sättigung,
      in der Anstrengung den Wert der Ruhe.
      Heraklit

 183.

        Eine gute Vision erwächst aus
      der Balance zwischen Realitätssinn und Utopie.
      Visionen sind das gerade noch machbare.
      Herrmann

 184.

      Verschiedene haben verschiedene Meinungen,
      aber kaum einer kennt die Wahrheit.
      Hesiod

 185.

      Der Glauben ist eben eine Sache des menschlichen Wollens, 
      nicht des Verstandes, 
      zu diesem Wollen mit allen seinen Konsequenzen
      sich zu entschließen, darin liegt die Schwierigkeit,
      das, was der Mensch selbst
      tun muss und was ihm auch keine Gnade ganz ersetzen kann.
      C. Hilty

 186.

       Ohne ganz persönliches Verhältnis zu Gott
      hat beten überhaupt eigentlich keinen Sinn.
      C. Hilty

 187.

       Verzeihe selbst, wenn du Verzeihung brauchst.
      Horaz

 188.

      Wie mit den Lebenszeiten, so ist es auch mit den Tagen.
      Keiner ist ganz schön, und jeder hat, wo nicht seine Plage,
      doch seine Unvollkommenheit, aber rechne sie zusammen,
      so kommt eine Summe Freude und Leben heraus.
      Friedrich Hölderlin

 189.

      Wer das Tiefste gedacht, liebt das Lebendigste.
      Friedrich Hölderlin

 190.

      Wage es, weise zu sein.
      Horaz

 191.

      Die Zukunft hat viele Namen.
      Für die Schwachen ist sie das Unerreichbare.
      Für die Furchtsamen ist sie das Unbekannte.
      Für die Tapferen ist sie die Chance.
      Victor Hugo

 192.

      Bevor ein Instrument benutzt werden kann, 
      muss es geschaffen werden. 
      Es ist wahr, dass die meisten von uns lernen, 
      sich auf weltliche Dinge zu konzentrieren, 
      aber alle Anstrengungen dieser Art richten sich auf die Analyse, 
      Synthese und den Vergleich von Tatsachen und Ideen; 
      dagegen zielt Konzentration als notwendige 
      Vorstufe zur Meditation darauf, 
      die Aufmerksamkeit ohne Schwanken auf ein Ding 
      oder eine Idee der eigenen Wahl zu richten, 
      unter Ausschluss jedes anderen Gegenstandes... 
      völlige Zielgerichtetheit des Denkens 
      auf den vorliegenden Gegenstand, sei es ein Bleistift, 
      eine Tugend oder ein im Geist vorgestelltes Diagramm.
      Christmas Humphreys

 193.

      Wer sich gering geschätzt fühlt, tut gut daran, 
      geringschätzig in die Welt zu sehen.
       Aldous Huxley

 194.

       Erfahrung ist nicht etwas,
      was einem Menschen geschieht.
      Erfahrung ist das, was ein Mensch aus dem,
      was ihm geschieht; macht.
      Aldous Huxley












#

Das Geheimnis, mit allen Menschen in Frieden zu leben, 
besteht in der Kunst, 
jeden seiner Individualität nach zu verstehen. 
Friedrich Ludwig Jahn 

#

Die größte Revolution in unserer Generation, 
ist die Entdeckung, 
dass Menschen durch den Wandel 
ihrer inneren Einstellung
die äußeren Aspekte ihres Lebens verändern können. 
William James

#

Wer lächelt, statt zu toben,
ist immer der Stärkere.
Aus Japan
#

Achte auf den Rat des Gewissens,
denn einen treueren Ratgeber hast du nicht.
Jesaja, sir. 37.13.

#

Deine Vision wird klar, wenn du in dein Herz schaust.
Wer nach draußen schaut, träumt.
Wer nach innen schaut, erwacht.
Carl Gustav Jung

#

Das Problem der Liebe gehört
zu den großen Leiden der Menschheit,
und niemand sollte sich der Tatsache schämen,
dass er seinen Tribut daran zu zahlen hat.
C. G. Jung

#

Die Frau weiß in zunehmendem Maße,
dass nur die Liebe ihr völligere Gestalt gibt,
so wie der Mann zu ahnen beginnt,
dass nur der Geist seinem Leben höchsten Sinn verleiht,
und beide suchen im Grunde die seelische Beziehung zueinander,
weil zur Vollendung die Liebe des Geistes
und der Geist der Liebe bedarf.
C. G. Jung

#

Wo die Liebe herrscht, da gibt es keinen Machtwillen,
und wo die Macht den Vorrang hat, da fehlt die Liebe.
Das eine ist der Schatten des andern.
C. G. Jung

#

Es ist ein Kennzeichen der Frau,
dass sie alles aus Liebe zu einem Menschen tun kann. 
Diejenigen Frauen aber, die aus Liebe zu einer Sache
Bedeutendes leisten, sind die größten
Ausnahmen, weil das ihrer Natur nicht entspricht.
Die Liebe zur Sache ist eine männliche Prärogative.
Da aber der Mensch Männliches und Weibliches
in seiner Natur vereinigt, so kann ein Mann Weibliches
und eine Frau Männliches leben.
Jedoch steht dem Manne das Weibliche im Hintergrund
sowie der Frau das Männliche.
Lebt man nun das Gegengeschlechtliche,
so lebt man in seinem eigenen Hintergrund,
wobei das Eigentliche zu kurz kommt.
Ein Mann sollte als Mann leben
und eine Frau als Frau.
C. G. Jung

#

Gott ist die Liebe, und wer in der liebe bleibt,
der bleibt in Gott und Gott in ihm.
Johannes 4, 16
#

Wer an mich glaubt, wie die Schrift sagt,
von dessen Leib werden Ströme
lebendigen Wassers fließen
Johannes 7, 38
#

Wenn ihr bleiben werdet an meinem Wort, 
so seid ihr wahrhaftig meine Jünger
und werdet die Wahrheit erkennen,
und die Wahrheit wird euch frei machen.
Johannes 8, 31-32
#

Wenn ihr in mir bleibt und meine Worte in euch bleiben
werdet ihr bitten, was ihr wollt, und es wird euch widerfahren.
Johannes 15, 7
#

Vater, ich will, dass wo ich bin, auch die bei mir seien,
die du mir gegeben hast,
damit sie meine Herrlichkeit sehen, die du mir gegeben hast.
Johannes 17, 24
#

Stelle dir selbst - und nur dir selbst - eine einzige Frage:
Hat dieser Weg ein Herz?
Alle Wege sind gleich - sie führen ins Nirgendwo.
Es sind Wege, die durch das Dickicht und in das Dickicht führen...
Hat dieser Weg ein Herz?
Wenn ja, ist es ein guter Weg.
Wenn nein, ist er nutzlos.
Don Juan bei Castaneda




#

Jeder, der sich die Fähigkeit erhält, 
Schönes zu erkennen, wird nie alt werden.
Franz Kafka

#

 Habe Mut, 
dich deines ganzen Verstandes zu bedienen.
Immanuel Kant

#

Die Aufgabe des Menschengeistes besteht nicht darin, 
die Wahrheit zu suchen, 
sondern ein möglichst treffliches Bild 
der Wahrheit zu bekommen. 
Immanuel Kant

#

Der Himmel hat dem Menschen als Gegengewicht
gegen die vielen Mühseligkeiten des Lebens
drei Dinge gegeben:
die Hoffnung, den Schlaf und das Lachen. 
Immanuel Kant

#

Kühner, als das Unbekannte zu erforschen, 
kann sein, das Bekannte zu bezweifeln.
H. Kaspar

#

Der wirkliche Gedanke erzeugt zunächst naturgemäß
den Widerstand der Wirklichkeit,
da er ja diese nicht bestätigen, sondern verändern will.
H. Kasper

#

Es gibt zwei Möglichkeiten, Karriere zu machen: 
Entweder leistet man wirklich etwas, 
oder man behauptet, etwas zu leisten. 
Ich rate zur ersten Methode, 
denn hier ist die Konkurrenz bei weitem nicht so groß.
Danny Kaye

#

Die Tore zu Himmel und Hölle liegen direkt nebeneinander
und gleichen einander aufs Haar.
Nikos Kazantzakis

#

Es ist gesünder, zu hoffen und das Mögliche zu schaffen,
als zu schwärmen und nichts zu tun.
Gottfried Keller

#

Das Werk, glaubt mir, das mit Gebet beginnt,
das wird mit Heil und Ruhm und Sieg sich krönen.
Heinrich von Kleist

#

Dankbarkeit ist das erste und letzte Gefühl des Menschen.
Adolf Kolping

#

Wenn du einen Würdigen siehst,
dann trachte ihm nachzueifern.
Wenn du einen Unwürdigen siehst,
dann prüfe dich in deinem Inneren.
Konfuzius

#

Feingedrechselte Worte und ein wohlgefälliges Gebaren
sind selten Zeichen wahrer Menschlichkeit.
Konfuzius

#

Der Meister sagte: "Wo es Bildung gibt, 
darf es keine Klassen geben." 
Konfuzius 

#

Es ist besser ein kleines Licht zu entzünden,
als über die große Dunkelheit zu fluchen.
Konfuzius 

#

Der Mensch hat dreierlei Wege,
klug zu handeln:
Erstens durch nachdenken,
das ist der edelste;
zweitens durch Nachahmen,
das ist der leichteste;
drittens durch Erfahrung,
das ist der bitterste.
Konfuzius 

#

Wer wirklich gütig ist, kann nie unglücklich sein;
wer wirklich weise ist, kann nie verwirrt werden.
Wer wirklich tapfer ist, fürchtet sich nie.
Konfuzius
 
#

Konfuzius sprach:
"Man kann dem Volk wohl Gehorsam befehlen,
aber kein Wissen."
Konfuzius

#

Es betrübt mich nicht, 
wenn mich die Menschen nicht kennen, 
aber es betrübt mich, 
wenn ich die Menschen nicht kenne.
Konfuzius

#

Sei dir bewusst, was du weißt.
Was du hingegen nicht weißt, das gib zu. 
Das ist das richtige Verhältnis zum Wissen.
Konfuzius

#

    Lernen ohne zu denken, ist vergebene Mühe.
Denken, 
ohne etwas gelernt zu haben,
ist unheilvoll.
Konfuzius

#

Wohin du auch gehst, geh mit deinem ganzen Herzen.
Konfuzius

#

In zweifelhaften Fällen entscheide man sich 
für das richtige.
Karl Kraus

#

Weil sich Sonne und Mond nicht im trüben Gewässer
widerspiegeln können, so kann sich der Allmächtige
nicht in einem Herzen widerspiegeln,
das nur von der Idee des "Ich und Mein" getrübt ist.
Sri Rama Krishna

#

Ich bin der Ursprung dieser Welt,
ich bin zugleich ihr Untergang.
Es gibt nichts Höheres als mich,
das Einzig - Eine bin ich nur.
Um mich ist dieses All gereiht
wie Perlen an der Seidenschnur.

Jenseits des Unentfalteten
ist eine ewige Wesenheit,
die, mag die Welt auch untergehn,
bestehen bleibt in Ewigkeit.

Der ewige, der höchste Geist,
der nur durch Liebe wird erkannt.
Von mir, dem Unentfalteten
wird ausgespannt die ganze Welt.
Krishna / Bhagavadgita












 235.

      Verantwortlich ist man nicht nur für das, 
      was man tut,
      sondern auch für das, was man nicht tut.
      Laotse

 236.

      Wahrheit kommt mit wenigen Worten aus.
      Laotse

 237.

      Der Edle weiß, ohne irgendwo hinzugehen,
      sieht, ohne hinzublicken und hat Erfolg
      ohne eigenes Zutun
      Laotse

 238.

      Nicht wer nach ihm sucht und ausschaut,
      sondern wer die Augen schließt,
      wird des Unsichtbaren gewahr.
      Laotse

 239.

      Wer nicht auf das Kleine schaut,
      scheitert am Großen.
      Laotse

 240.

           Das Böse lebt nicht in der Welt der Menschen.
      Es lebt allein im Menschen
      Laotse

 241.

      Mit dem Wort "Zufall" gibt der Mensch nur
      seiner Unwissenheit Ausdruck.
      Laplace

 242.

      Was du für den Gipfel hältst,
      ist nur eine Stufe.
      Lateinisches Sprichwort

 243.

      Es ist viel schwerer gegen die düsteren Mächte 
      im Menschen zu kämpfen,
      als eine interplanetare Reise zu planen.
      Stanislaw Lem

 244.

      Das Ringen der Menschen nach Erkenntnis: 
      Das ist ein Prozess, dessen Ziel im Unendlichen liegt. 
      Die Philosophie aber ist der Versuch,
      dieses Ziel auf Anhieb, durch Kurzschluss zu erreichen, 
      der uns ein vollkommenes und unerschütterliches Wissen verbürgt.
      Stanislaw Lem

 245.

      Die Unwissenheit ist der Wahrheit näher als das Vorurteil.
      Lenin

 246.

      Kein Mensch muss, müssen. (Nathan der Weise)
      Gotthold Ephraim Lessing

 247.

      Die Suche nach Wahrheit ist köstlicher
      als deren gesicherter Besitz. 
      Gotthold Ephraim Lessing

 248.

      Nur die Sache ist verloren,
      die man selber aufgibt.
      Gotthold Ephraim Lessing

 249.

      Von allem, was ausgerechnet wird in der Welt,
      geschehen zwei Drittel gedankenlos.
      Lichtenberg

 250.

      Die Neigung der Menschen, kleine Dinge
      für wichtig zu halten, hat sehr
      viel großes hervorgebracht.
      Georg Christoph Lichtenberg

 251.

      Man kann auf eine Art zuhören,
      die mehr wert ist als das Gefälligste,
      was man sagen kann.
      Charles-Joseph de Ligne

 252.

      Wünscht Du glücklich zu sein, 
      strebe nicht nach Freiheit von etwas, 
      sondern nach Freiheit für etwas, 
      das Du als zutiefst sinnvoll verstanden hast.
      Walter Lübeck

 253.

      Das Wassermannzeitalter beginnt tatsächlich nur für den,
      der sich traut, in seinem Geist zu leben.
      Walter Lübeck

 254.

      Bei Gott ist kein Ding unmöglich.
      Lukas, Kap. 1, Vers 37

 255.

      Liebet eure Feinde, tut Gutes und leiht wo ihr nichts
      dafür zu bekommen hofft.
      So wird euer Lohn groß sein, und ihr werdet
      Kinder des Allerhöchsten sein.
      Lukas, Kap. 6, Vers 35

 256.

      Richtet andere nicht, damit auch ihr nicht gereichtet werdet.
      Verurteilt andere nicht, damit auch ihr nicht verurteilt werdet.
      Sprecht die frei, die sich gegen euch vergangen haben,
      dann werdet auch ihr von euren vergehen freigesprochen.
      Gebt und so wird euch gegeben werden.
      Denn mit dem selben Maß, mit dem ihr andere messt,
      wird euch auch wieder gemessen werden.
      Lukas, Kap. 6, Vers 37-38

 257.

      Wer da bittet, der empfängt;
      und wer da sucht der findet;
      und wer da anklopft dem wird aufgetan.
      Liebet eure Feinde, tut Gutes und leiht wo ihr nichts
      dafür zu bekommen hofft.
      So wird euer Lohn groß sein, und ihr werdet
      Kinder des Allerhöchsten sein.
      Lukas, Kap. 11, Vers 10

 258.

      Sardinen wissen, dass Gleichmachen mit
      Kopfabschneiden beginnt.
      Jeannine Luczak




 259.

      Das Lächeln ist das Gebet
      einer jeden Zelle.
      Gitta Mallasz

 260.

      Wir kennen uns noch nicht, 
      wir haben noch nicht gewagt,
      zusammen zu schweigen.
      Maeterlinck

 261.

      Starke Menschen bleiben ihrer Natur treu,
      mag das Schicksal sie auch in schlechte Lebenslagen bringen.
      Ihr Charakter bleibt fest, und ihr Sinn wird niemals schwankend.
      Über solche Menschen kann das Schicksal keine Gewalt bekommen.
      Niccolo Machivelli

 262.

      Unsere tiefste Angst ist nicht,
      dass wir unzulänglich sind.
      Unsere tiefste Angst ist,
      dass wir grenzenlose Macht in uns haben.
      Es ist unser Licht und nicht unsere Dunkelheit,
      vor der wir uns am meisten fürchten.
      Wer bin ich schon, fragen wir uns,
      dass ich schön, talentiert
      und fabelhaft sein soll?
      Aber ich frage dich, wer bist du, es nicht zu sein?
      Du bist ein Kind Gottes.
      Dich kleiner zu machen dient unser Welt nicht.
      Es ist nichts erleuchtetes dabei,
      sich zurückzuziehen und zu schrumpfen,
      damit andere Leute nicht unsicher werden,
      wenn sie in deiner Nähe sind.
      Wir wurden geboren, um die Herrlichkeit Gottes,
      die in uns ist, zu offenbaren.
      Sie ist nicht nur in einigen von uns,
      sie ist in jedem von uns.
      Wenn wir unser eigenes Licht strahlen lassen,
      geben wir unterbewusst unseren Mitmenschen
      die Erlaubnis, dasselbe zu tun.
      Nelson Mandela

 263.

      Wo uns auch immer menschliche Wesen begegnen mögen,
      stets meinen wir, 
      dass sie sich über andere Leute wundern.
      Mead

 264.

      Alles geschieht, wie es geschieht.
      Unglücke, von Natur oder Menschenhand erzeugt, 
      geschehen, und es gibt keinen Grund, entsetzt zu sein.
      Sri Nisargadatta Maharaj

 265.

      Die Frage "Wer bin ich"
      ist die einzige Methode,
      allem Elend ein Ende zu setzen und höchste
      Glückseligkeit einzuleiten.
      Sri Ramana Maharishi

 266.

       Dankbarkeit  ist das Gedächtnis des Herzens.
      Massieu

 267.

      Denn viele sind berufen,
      aber nur wenige sind auserwählt.
      Matthäus 22, 14

 268.

      Leben ist eine Vorbedingung des Erkennens.
      Wer nicht zu leben versteht, 
      wird nicht erkennen können.
      Gottfried Meinhold

 269.

            Begehren ist nicht nur wünschen.
      Begehren ist, das zu werden,
      was man im wesentlichen ist.
      Miller

 270.

      Sieh nicht, was andere tun, der andren sind so viel.
      Du kommst nur in ein Spiel,
      das nimmermehr wird ruhn.

      Geh einfach Gottes Pfad.
      Lass nichts sonst Führer sein.
      So gehst du recht und grad
      und gingst du ganz allein.
      Christian Morgenstern

 271.

      Wer sich selbst treu bleiben will,
      kann nicht immer anderen treu bleiben.
      Christian Morgenstern

 272.

      Die Natur ist die große Ruhe gegenüber 
      unserer Beweglichkeit. 
      Darum wird sie der Mensch immer mehr lieben, 
      je feiner und beweglicher er wird. 
      Christian Morgenstern

 273.

      Der Klügere gibt so lange nach, 
      bis er der Dumme ist.
      Werner Mitsch

 274.

      Das Schicksal war herrisch zu mir,
      aber herrischer war mein Wille. 

 275.

      Das Wissen um den richtigen Zeitpunkt
      ist oft der halbe Erfolg.
      Maurice Couve de Murville









 276.

       Verdoppeln lässt sich das Glück nur,
      wenn man es teilt.
      Johann Nepomuk Nestroy

 277.

      Jetzt erkenne ich stückweise, dann aber werde ich erkennen,
      gleichwie ich erkannt bin.
      Nun aber bleibt Glaube, Hoffnung, Liebe,
      diese drei; aber die Liebe ist die größte unter ihnen.
      Neues Testament, Korinther

 278.

      Liebet nicht mit Worten noch mit der Zunge,
      sondern in der Tat und in der Wahrheit.
      Neues Testament

 279.

      Die Liebe ist langmütig und freundlich, die Liebe eifert nicht,
      die Liebe treibt nicht Mutwillen, sie blähet sich nicht,
      sie stellet sich nicht ungebärdig,
      sie suchet nicht das ihre, sie lässt sich nicht erbittern,
      sie rechnet das Böse nicht zu,
      sie freuet sich nicht der Ungerechtigkeit,
      sie freuet sich aber der Wahrheit,
      sie verträgt alles, sie glaubet alles, 
      sie hoffet alles, sie duldet alles.
      Neues Testament, Korinther

 280.

      Was wir wissen, ist ein Tropfen,
      was wir nicht wissen - ein Ozean.
      Isaac Newton

 281.

      Die Hoffnung ist der Regenbogen über den
      herabstürzenden Bach des Lebens
      Friedrich Nietzsche

 282.

      Ohne Musik wäre das ganze Leben nur ein Irrtum.
      Friedrich Nietzsche

 283.

      Wer die Unfreiheit des Willens fühlt,
      ist geisteskrank, wer sie leugnet dumm.
      Friedrich Nietzsche

 284.

      Der Mensch ist ein mittelmäßiger Egoist; 
      auch der Klügste nimmt seine Gewohnheit
      wichtiger als seinen Vorteil.
      Friedrich Nietzsche

 285.

      Jeder, der geheimnisvoll von seinem Vorhaben spricht,
      stimmt seine Mitmenschen ironisch.
      Friedrich Nietzsche

 286.

      Was spricht die tiefe Mitternacht?
      Ich schlief, 
      ich schlief -, 
      Aus tiefem Traum bin ich erwacht: -
      Die Welt ist tief,  
      und tiefer als der Tag gedacht.
      Tief ist ihr Weh -,
      Lust - tiefer noch als Herzeleid:
      Weh spricht: Vergeh!
      Doch alle Lust will Ewigkeit -,
      - will tiefe, tiefe Ewigkeit"
      Friedrich Nietzsche
       (Zarathustra)

 287.

      Dem Reinen ist alles rein" - so spricht das Volk.
      Ich aber sage euch: den Schweinen wird alles Schwein!
      Friedrich Nietzsche
       (Zarathustra)

 288.

       Alles geht, alles kommt zurück; ewig rollt das Rad des Seins. 
         Alles stirbt, alles blüht wieder auf; ewig läuft das Jahr des Seins. 
      Alles bricht, alles wird neu gefügt; 
      ewig baut sich das gleiche Haus des Seins.
      Alles scheidet, alles grüßt sich wieder; 
      ewig bleibt sich treu der Ring des Seins.
      Friedrich Nietzsche

 289.

      Mitfreude, nicht Mitleiden macht den Freund.
      Friedrich Nietzsche

 290.

      Wenn du einmal Erfolg hast, kann es Zufall sein.
      Wenn du zweimal Erfolg hast, kann es Glück sein.
      Wenn du dreimal Erfolg hast,
      so ist es Fleiß und Tüchtigkeit.
      Sprichwort aus der Normandie

 291.

        Idealist sein heißt :
      Kraft haben für andere.
      Novalis

 292.

      Krankheiten, besonders langwierige,
      sind Lehrjahre des Lebenskunst und der Gemütsbildung.
      Novalis

 293.

      Wo Kinder sind, da ist
      ein goldenes Zeitalter.
      Novalis




 294.

      Wo immer du mit mir bist, werde ich mit dir sein.
      ONE
 295.

      Man kann nicht kämpfen,
      wenn die Hosen voller sind als die Herzen
      Carl von Ossietzky

 296.

      Als du auf die Welt kamst, weintest du,
      und um dich herum freuten sich alle.
      Lebe so, dass, wenn du die Welt verlässt,
      alle weinen und du alleine lächelst.
      Östliche Weisheit 




 297.

      Da es nichts gibt, um darüber zu meditieren,
      gibt es keine Meditation.
      Da man nicht vom Weg abkommen kann,
      gibt es kein Verirren.
      Es gibt zwar eine unendliche Vielfalt
      von tiefgehenden Praktiken,
      doch existieren sie für den Verstand
      in seinem wahren Zustand nicht.
      Da es weder die Praktiken
      noch den Praktizierenden gibt, wird,
      wenn von jenen - ob sie praktizieren oder nicht - erkannt wird, 
      dass der die Praktiken Praktizierende nicht existiert,
      dadurch das Ziel der Praktiken erreicht
      und auch das Ende der Praktiken selbst.
      Padmasambhava

 298.

      Der Irrtum ist nichts anderes als eine durch
      gelockerten Wortgebrauch verletzte Wahrheit.
      Mario Pamilio

 299.

      Wo man mit Ernst beginnt ein Werk zu treiben,
      wo man die schlaffe Trägheit niederhält,
      wo zu der Klugheit sich der Mut gesellt:
      da wohnt das Glück - da will es bleiben.
      Panchatantra (Indische Fabelsammlug)

 300.

      Wer nichts weiß, liebt nichts.
      Wer nichts tun kann, versteht nichts.
      Wer nichts versteht, ist nichts wert.
      Aber wer versteht, 
      der liebt, bemerkt und sieht auch ...
      Je mehr Erkenntnis einem Ding innewohnt,
      desto größer ist die Liebe ...
      Wer meint, alle Früchte würden gleichzeitig
      mit den Erdbeeren reif, versteht nichts von den Trauben.
      Paracelsus

 301.

      Das Herz hat seine eigene Logik,
      die der Verstand nicht kennt.
      Blaise Pascal

 302.

      Je mehr man Menschen kennt,
      desto weniger schildert man Individuen.
      Jean Paul

 303.

      Nicht das Zeitliche, sondern das Ewige
      bestimmt die Würde des Menschen.
      Jean Paul

 304.

      Nicht unser Hirn, sondern unser Herz 
      denkt die größten Gedanken.
      Unser Herz aber, oder unsere Seele,
      oder der Kern unserer Persönlichkeit 
      ist ein Funke aus dem Lebenslichtermeer Gottes.
       Jean Paul

 305.

         Wie dem Geiste nichts zu groß ist,
      so ist der Güte nichts zu klein.
      Jean Paul

 306.

      Die Menschen widerlegen einander ewig nur die Irrtümer,
      die der andere nicht behauptet.
      Jean Paul

 307.

      Das Beste in einem Menschen ist das,
      was er selber nicht kennt.
      Jean Paul

 308.

      Wo Religion ist, werden Menschen geliebt und Tiere
      und das All.
      Jedes leben ist ja ein beweglicher Tempel des Unendlichen.
      Jean Paul

 309.

      Der Glaube ist Liebe.
      J. Heinrich Pestalozzi

 310.

      Wenn der Mensch sich etwas vornimmt,
      so ist ihm mehr möglich, als man glaubt.
      J. Heinrich Pestalozzi

 311.

      Wenn jeder im Dunkel der Menschlichkeit
      ein kleines Licht entzündete,
      dann wäre die Welt bald ein Lichtermeer 
      und Leben viel leichter.
      Susanne Petersen

 312.

      Unter den Menschen gibt es viel mehr Kopien
      als Originale.
      Pablo Picasso

 313.

      Der Liebende blickt in einen Spiegel,
      in dem er sein Selbst entdeckt.
      Plato

 314.

      Nicht die Seele ist im Universum,
      sondern das Universum ist in ihr.
      Plotin

 315.

      Gott ist mein Fels, meine Hilfe und mein Schutz,
      dass ich nicht fallen werde.
      Psalm 62, Vers 7

 316.

      Lass meinen Gang in deinem Wort fest sein
      und lass kein Unrecht über mich herrschen.
      Psalm 119, Vers 133

 317.

      Gegen Schmerzen der Seele gibt es nur
      zwei Arzneimittel:
      Hoffnung und Geduld.
      Pythagoras




 318.

      Gott ist in allen Menschen.
      Aber nicht alle Menschen sind in Gott.
      Dies ist die Ursache, warum sie leiden
      Ramakrishna

 319.

      Es ist nicht wichtig, ob man erster, 
      zweiter oder dritter ist.
      Wichtig ist, dass du Haltung hast.
      Erich Ribbeck

 320.

      Was dir jetzt dunkel erscheint,
      wirst du mit glühendem Herzen erhellen.
      Rainer Maria Rilke

 321.

      Denn nur dem Einsamen wird offenbart,
      und vielen Einsamen der gleichen Art
      wird mehr gegeben als dem schmalen Einen.
      Denn jedem wird ein anderer Gott erscheinen,
      bis sie erkennen, nah am Weinen,
      dass durch ihr meilenweites Meinen,
      durch ihr Vernehmen und Verneinen,
      verschieden nur in hundert Seinen 
      EIN Gott wie eine Welle geht.
      Rainer Maria Rilke

 322.

      Nur, wir vergessen so leicht, 
      was der lachende Nachbar uns nicht bestätigt oder beneidet.
      Sichtbar wollen wir's heben,
      wo doch das sichtbarste Glück uns erst zu erkennen sich gibt,
      wenn wir es innen verwandeln.
      Rainer Maria Rilke

 323.

      O Herr, gib jedem seinen eignen Tod,
      Das Sterben, das aus jenem Leben geht,
      darin er Liebe hatte, Sinn und Not.

      Denn wir sind nur die Schale und das Blatt.
      Der große Tod, den jeder in sich hat,
      das ist die Frucht, um die sich alles dreht.
      Rainer Maria Rilke

 324.

      Die Blätter fallen, fallen wie von weit,
      als welkten in den Himmeln ferne Gärten;
      sie fallen mit verneinender Gebärde.

      Und in den Nächten fällt die schwere Erde 
      aus allen Sternen in die Einsamkeit.

      Wir alle fallen. Diese Hand da fällt. 
      Und sieh dir andre an: es ist in allen.

      Und doch ist einer, welcher dieses Falle
      unendlich sanft in seinen Händen hält.
      Rainer Maria Rilke

 325.

      Nirgends, Geliebte, wird die Welt sein, als innen.
      Unser Leben geht hin mit Verwandlung.
      Und immer geringer schwindet das Außen.
      Rainer Maria Rilke

 326.

      Alle, welche dich suchen, versuchen dich.
      Und die, so dich finden, binden dich an Bild und Gebärde.
      Ich aber will dich begreifen wie dich die Erde begreift;
      mit meinem Reifen reift dein Reich.
      Rainer Maria Rilke

 327.

      Die Vernunft umfasst die Wahrheiten, 
      die man aussprechen, 
      und solche, die man verschweigen darf.
      Antoine Rivarol

 328.

      Das Dasein ist köstlich, man muss nur den Mut haben,
      sein eigenes leben zu führen.
      Peter Rosegger

 329.

      Ich habe an der Schwelle des Wahnsinn gelebt,
      wollte die Gründe wissen und klopfte an eine Tür.
      Sie öffnete sich.
      Ich hatte von innen geklopft.
      Rumi

 330.

      Das Herz ist fenstergleich, das Haus wird so erhellt.
      Der Leib drängt zum vergehen, 
      das Herz drängt zum Bestehen!
      Rumi

 331.

       Was es auch großes und Unsterbliches
      zu erstreben gibt: Dem Mitmenschen
      Freude zu machen ist doch das Beste,
      was man auf der Welt tun kann
      Peter Rosegger

 332.

      Unser Wille reicht weniger weit als unsere Kraft,
      und wir stellen uns Dinge oft als unmöglich vor,
      um uns vor uns selbst zu entschuldigen.
      Francois de la Rochefoucault

 333.

        Wären wir selbst ohne Fehler,
      dann suchten wir nicht mit Eifer
      solche bei anderen aufzudecken.
      Francois de la Rochefoucault

 334.

      Selbstvertrauen ist die Quelle des
      Vertrauens zu anderen.
      Francois de la Rochefoucault

 335.

      Gleichheit am Anfang (Startgleichheit)
      kann man im Namen der Gerechtigkeit fordern.
      Gleichheit am Ende nur im Namen des Neides.
      Rüstow










 336.

      Man weiß selten, was Glück ist, 
      aber man weiß meistens was Glück war. 
      Francoise Sagan

 337.

      Sei mit jedem geduldig, aber vor allem mit dir selbst. 
      Lasse dich von deiner Unvollkommenheit
      nicht niederschlagen, 
      sondern erhebe dich immer wieder mit neuem Mut. 
      Wie können wir mit den Fehlern unser Nachbarn geduldig sein, 
      wenn wir mit unseren eigenen Fehlern ungeduldig sind? 
      Wer sich über sein eigenes Versagen ärgert und grämt, 
      der wird es nicht korrigieren. 
      Nutzbringende Korrektur kann nur einem ruhigen, 
      friedvollen Geist entspringen.
      ST. Francis de Sales

 338.

      Wie groß die Finsternis auch sei,
      wir sind immer dem Lichte nahe.
      Franz von Sales

 339.

      Man sieht nur mit dem Herzen gut.
      Das Wesentliche ist dem Auge unsichtbar.
      Antoine de Saint-Exupery

 340.

      Denn Liebe ist stark wie der Tod.
      Hohelied Salomos 8,6

 341.

      Drei Verhaltensweisen unterstützen das gesunde Leben:
      Gesunde Nahrung, ausreichend Schlaf und geregeltes Sexualleben.
      Wird der Körper von diesen wohl regulierten Faktoren getragen,
      wird er Stärke, Ausstrahlung und Wachstum besitzen
      und die volle Lebensspanne ausschöpfen.
      Deshalb gebt euch nicht mit Verhaltensweisen ab,
      die euer Gesundheit abträglich sind.
      Caraka Samhita, Kap. 11, Vers 35

 342.

      Um seinen Lebensunterhalt zu verdienen,
      sollte man nur solche Tätigkeiten wählen,
      die nicht den frommen Pfad widersprechen.

      Man sollte dem Pfad des Friedens folgen
      und sich dem Studium der heiligen Schriften widmen.
      Nur so kann man Glückseligkeit erlangen.
      Caraka Samhita, Kap. 5, Vers 105

 343.

      Nur solche physischen Aktivitäten sind erstrebenswert,
      die Körperliche Stabilität und Stärke bringen.
      Und diese sollten in Harmonie ausgeführt werden.
      Caraka Samhita, Kap. 7, Vers 31




 344.

      Ich habe alles gehabt, was ich wollte,
      aber nie so wie, ich es wollte.
      Jean Paul Sartre

 345.

      Zwischen entweder und oder, 
      führt noch manches Sträßlein.
      Josef Victor von Scheffel

 346.

      Wir hätten alle mindestens eine Stunde 
      Einsamkeit am Tag nötig,
      um aufzufüllen und Atem zu schöpfen.
      Maria Schell

 347.

      Lieber ein Ende mit Schrecken, 
      als ein schrecken ohne Ende.
      Ferdinand von Schill

 348.

      Die Stimme der Freundschaft in der Not zu vernehmen 
      ist das Göttlichste,
      was dem herzen widerfahren kann.
      Charlotte Schiller

 349.

       Waren unsere Wesen schon verflochten? 
      War es darum, dass unsere Herzen pochten? 
      Waren wir ein Strahl erlosch'ner Sonnen? 
      In den Tagen lang' verrauschter Wonnen schon in eins zerronnen? 
      Ja wir waren's ! - Innig mir verbunden. 
      Warst Du in Äonen, die verschwunden.
      Friedrich von Schiller

 350.

      Wohl dem, der gelernt hat, zu ertragen,
      was er nicht ändern kann,
      und preiszugeben mit Würde, 
      was er nicht retten kann. 
      Friedrich von Schiller

 351.

      Der Erfolg ruht in des Himmels Hand.
      Friedrich von Schiller

 352.

      Nicht in die ferne Zeit verliere dich!
      Den Augenblick ergreife, er ist dein.
      Friedrich von Schiller

 353.

      Sei dankbar der Chance, die dir die Tür öffnet, 
      und den Freunden, die die Scharniere schmieren.
      Lothar Schmidt

 354.

      Wer die Zukunft fürchtet, verdirbt sich die Gegenwart.
      Lothar Schmidt

 355.

      Toleranz heißt: Die Fehler der anderen entschuldigen.
      Takt heißt: Sie nicht bemerken.
      Arthur Schnitzler

 356.

      Die Menschenliebe ist das Herz des Menschen,
      die Pflicht sein Weg.
      Den Weg aus den Augen verlieren
      und sich nicht darum kümmern.
      Arthur Schnitzler

 357.

      Was wir Illusion nennen,
      ist entweder Wahn, Irrtum oder Selbstbetrug-
      wenn sie nicht eine höhere Wirklichkeit bedeutet,
      die als solche  anzuerkennen wir zu bescheiden,
      zu skeptisch oder zu zaghaft sind.
      Arthur Schnitzler




 358.

       Lass dir keine Grenzen setzen
      in deiner Liebe,
      nicht Maß, nicht Art, nicht Dauer!
      Friedrich Schleieremacher

 359.

      Der innerste Kern jeder echten und wirklichen Erkenntnis
      ist eine Anschauung; auch ist jede neue Wahrheit
      die Ausbeute aus einer solchen. 
      Alles Denken geschieht in Bildern;
      darum ist die Phantasie ein so notwendiges Werkzeug
      desselben und werden Phantasielose nie etwas Großes leisten; 
      es sei denn in der Mathematik.
      Arthur Schoppenhauer

 360.

      Der Begriff ist ein Gedankenprodukt,
      die Idee aber ist eine Anschauung.
        Arthur Schoppenhauer

 361.

      Stark sein im Schmerz, nicht wünschen,
      was unerreichbar oder wertlos.
      Für tausend bittre Stunden sich mit einer einzigen
      trösten, welche schön ist,
      und mit Herz und Können sein Bestes geben, 
      auch wenn es keinen Dank erfährt.
      Wer das kann, der ist ein Glücklicher.
      Arthur Schoppenhauer

 362.

      ....Jedes neugeborene Wesen tritt frisch und freudig 
      in das neue Dasein ein und genießt es als ein geschenktes; 
      aber es gibt und kann kein geschenktes geben; 
      sein frisches Dasein ist bezahlt durch Alter und Tod eines abgelebten, 
      welches untergegangen ist, aber den unzerstörbaren Keim enthielt, 
      aus dem dieses neu entstanden ist; sie sind ein Wesen.
      Arthur Schoppenhauer

 363.

      Wer ein gutes Gewissen hat,
      der braucht sich um den Verlust der Wertschätzung
      der anderen nicht zu kümmern.
      Arthur Schoppenhauer

 364.

      Moral predigen ist leicht, Moral begründen schwer.
      Arthur Schoppenhauer

 365.

      Keine Antwort ist auch eine Antwort.
      Sprichwort

 366.

      Arbeite, als ob du ewig leben würdest, und lebe so,
      als ob du morgen sterben würdest.
      Rosemarie Schuder

 367.

      Natürlich ist es nötig, alles zu wissen, was man sagt.
      Aber man muss nicht alles sagen, was man weiß.
      Rosemarie Schuder

 368.

      Die unendliche Weite ist ganz einfach unvorstellbar.
      Auch wenn sie ständig vorhanden ist,
      kann der Verstand sie nicht erkennen,
      denn das Unendliche wird nicht mit dem Verstand wahrgenommen
      Das Unendliche nimmt sich durch sich selbst wahr.
      Suzanne Segal

 369.

      Wir alle sitzen im gleichen Boot.
      Wir alle bestehen aus der gleichen unendlichen Substanz, 
      und wenn eine Anzahl von menschlichen Kreisläufen
      gleichzeitig und bewusst am Unendlichen teilhaben, 
      dann steigert sich das Ausmaß an Liebe,
      die das Unendliche für sich selbst empfindet, ganz ungemein.
      Das ist die Kraft dessen, was allgemein
      als Gemeinschaft bezeichnet wird.
      Suzanne Segal

 370.

      Flitterwochen sind eine Probezeit, 
      in der keine Reklamationen mehr angenommen werden.
      Peter Selters

 371.

      Alles, was Menschen tun, gleicht ihren ersten Anfängen,
      und ihr ganzer Lebenslauf verdient nicht mehr Würde und Ernst
      als ihre Empfängnis. 
      Aus dem Nichts entstehen sie, ins Nichts kehren sie zurück.
      Bion in Seneca

 372.

      Es soll ein Freund des Freundes Schwächen tragen.
      William Shakespeare

 373.

      Der Kummer, der nicht spricht, raunt leise zu dem Herzen,
      bis es bricht.
      William Shakespeare

 374.

      Fasse frischen Mut!
      Solange ist keine Nacht, das endlich nicht der Morgen lacht.
      William Shakespeare

 375.

      Deine Sehnsucht nach mir bin ich selbst in dir.
      Shakti zu ihrem Geliebten

 376.

      Freiheit wird gewonnen durch die Wahrnehmung
      der Einheit des Selbst mit dem Ewigen,
      nicht aber durch Lehrsätze von der Vereinigung
      mit demselben oder von Zahlen,
      noch durch Formeln und Wissenschaften.
      Shankara




 377.

      Jeder von uns besitzt alles, was er braucht,
      um sein tiefstes Wesen zu erforschen...
      in der ganzen Menschheit gibt es niemanden, 
      der das für uns tun könnte.
      Die Verantwortung und die Möglichkeit,
      uns unser wahres Wesen bewusst zu machen und es mit
      anderen zu teilen, liegt letztlich bei uns.
      Dean Sharpio und Roger Walsh

 378.

      Wer auch immer einen Skorpion parfümiert,
      wird seinem Stachel dadurch nicht entrinnen.
      Shah

 379.

      Nichts kann bedingungslos sein:
      folglich kann nichts frei sein.
      George Bernhard Shaw
       
 380.

      Der nächste Weg zu Gott ist durch der liebe Tür.
      Der Weg der Wissenschaft bringt dich gar langsam für.
      Angelus Silesius

 381.

      Je logischer eine Überlegung,
      desto weiter ist sie von der Wahrheit entfernt.
      Sergej Snegow

 382.

      Schönheit ist Vollkommenheit, das heißt ein Maximum
      des stets Erwarteten und Gewünschten.
      Sergej Snegow

 383.

      Wo aber die Fähigkeit zur Gemeinschaft im Menschen fehlt,
      da fehlt auch die Freundschaft.
      Sokrates

 384.

           Der Tod macht einen nicht von allem Schlechten frei.
      Durch die Unsterblichkeit der Seele
      gibt es für den Sünder keinen anderen Weg,
      als gut und einsichtsvoll zu sein.
      Sokrates

 385.

      Bedenke, dass die menschlichen Verhältnisse
      insgesamt unbeständig sind.
      Dann wirst du im Glück nicht übermütig
      und im Unglück nicht zu traurig sein.
      Sokrates


 386.

      Die Würfel Gottes fallen immer richtig.
      Sophokles

 387.

      Die Kraft der Gedanken wird unterschätzt.
      Wir können sie nicht sehen, nicht anfassen,
      aber sie wirken.
      Du sollst nie denken," ich bin ein Sünder".
      Du bist ein Kind Gottes!
 388.

      Du bist Teil des kosmischen Bewusstseins.
      Pedro de Souza

 389.

      Nicht materiellen Gütern musst du entsagen,
      aber deinen negativen Gedanken.
      Pedro de Souza

 390.

      Bete, als ob alles von Gott abhinge,
      aber arbeite, als ob alles von Dir abhinge.
      Francis Joseph Spellmann

 391.

      Wir sollen unsere eigenen Wünsche ernst nehmen,
      Spielräume erkennen und den Mut finden,
      Entscheidungen zu treffen.
      Es geht darum, die Verantwortung für das eigene
      - das einzige- Leben zu übernehmen.
      Reinhard K. Sprenger

 392.

      Wer eine helfende Hand sucht,
      findet sie am Ende seiner Arme.
      Reinhard K. Sprenger

 393.

      Ärger bedeutet immer, dass sie jemanden
      Verantwortung zuschieben, die sie selber haben.
      Reinhard K. Sprenger

 394.

      Glück ist keine Glückssache.
      Glück, was auch immer sie persönlich darunter verstehen,
      ist nicht etwas, das ihnen "zustösst".
      Glück ist das Ergebnis von selbstverantwortlichem,
      entschiedenen Handeln.
      Reinhard K. Sprenger

 395.

      "Keine Zeit" heißt: Anderes ist mir wichtiger.
      Reinhard K. Sprenger

 396.

      Tun sie das, was sie tun, mit Liebe und Hingabe.
      Oder lassen sie es ganz.
      Reinhard K. Sprenger

 397.

      Wer immer in die Fußstapfen anderer tritt, 
      hinterlässt keine Eindrücke.
      Reinhard K. Sprenger

 398.

      Lob ist wie Falschgeld:
      Es macht denjenigen ärmer, der es empfängt.
      Reinhard K. Sprenger

 399.

      Das Gefühl der Kontrolle über das eigene Leben
      ist die wichtigste Voraussetzung für
      körperliche und seelische Gesundheit.
      Reinhard K. Sprenger

 400.

      Stress gibt es nur wenn sie "Ja" sagen
      und "Nein" meinen.
      Reinhard K. Sprenger

 401.

      Erzähle es mir und ich werde es vergessen,
      zeige es mir und ich werde mich vielleicht daran erinnern,
      beziehe mich ein und ich werde es verstehen.
      Sprichwort der nordamerikanischen Indianer

 402.

      Beneide niemanden, denn du weißt nicht,
      ob der Beneidetet im Stillen nicht etwas verbirgt,
      was du bei einem Tausch nicht übernehmen möchtest.
      August Strindberg

 403.

      Dein tägliches Quantum Sonnenschein musst
      Du Dir täglich selbst verdienen.
      Hermann Sudermann

 404.

      Die Methode des Zen besteht darin,
      in den Gegenstand selbst einzudringen
      und ihn sozusagen von innen zu sehen.
      Die Blume sehen heißt, zur Blume werden, 
      die Blume sein, als Blume blühen und sich an Sonne 
      und Regen erfreuen.
      Wenn ich das tue, so spricht die Blume zu mir, 
      und ich kenne alle ihre Geheimnisse.
      Und nicht nur das: Gleichzeitig mit meiner "Kenntnis" der Blume 
      kenne ich alle Geheimnisse meines eigenen Ich, 
      das mir bisher mein Leben lang ausgewichen war, 
      weil ich mich in eine Dualität, 
      in Wahrnehmenden und Wahrgenommenes,
      in den Gegenstand und Nicht-Gegenstand, geteilt hatte. 
      Kein Wunder, dass es mir niemals gelang,
      mein Ich zu erfassen.
      Und jetzt kenne ich jedoch mein Ich,
      indem ich die Blume kenne.
      Das heißt, indem ich mich in der Blume verliere,
      kenne ich mein Ich ebenso wie die Blume.
      Suzuki

 405.

      Das Beste, was der Mensch für einen anderen tun kann,
      ist doch immer das, was er für ihn ist.
      Adalbert Stifter

 406.

      Reichtum, Ansehen, Macht, alles ist unbedeutend 
      und nichtig gegen die Größe des Herzens; 
      das Herz allein ist das einzige Kleinod auf der Welt.
      Adalbert Stifter

 407.

      Karma ist die ewige Bestätigung
      der menschlichen Freiheit...
      Unsere Gedanken, unsere Worte und Taten
      sind die Fäden in einem Netz, das wir uns umhängen.
      Swami Vivekananda
		



		


		
		
	
 408.

       Sterben ist das Auslöschen 
      der Lampe im Morgenlicht,
      nicht das Auslöschen der Sonne.
      Rabindranat Tagore

 409.

      Am reichsten sind die Menschen,
      die auf das meiste verzichten können. 
      Tagore

 410.

      Ich schlief und träumte, das Leben sei Freude.
      Ich erwachte und sah, das Leben war Pflicht.
      Ich handelte und siehe, die Pflicht war Freude.
      Tagore

 411.

      Gott achtet mich, wenn ich arbeite-
      aber er liebt mich, wenn ich singe.
      Tagore

 412.

      Wir sehen die Dinge nicht wie sie sind,
      sondern wie wir sind.
      Talmud

 413.

      Aus reiner Wonne entspringt die Schöpfung.
      Durch Wonne wird sie erhalten.
      Zu ihr strebt sie hin und kehrt in sie ein.
      Aus dem Tantra

 414.

      Man muss durch das steigen, 
      durch das man fallen kann.
      Hevajra -Tantra

 415.

      Ich existiere nicht, doch das Universum
      ist mein Selbst.
      Shih T'ou

 416.

       Ein liebes, gutes Wort ist immer ein Lichtstrahl, 
      der von Seele zu Seele geht.
      Hans Thoma

 417.

      Am wahrsten leben wir, 
      wenn wir in unseren Träumen wach sind.
      Thoreau

 418.

      Jeder den die Liebe beseelt,
      geht sicher im Schutze der Götter.
      Tibull

 419.

      Vergangenheit hängt nicht mehr von uns ab, 
      doch die Zukunft bestimmen wir.
      Tschaadjewv

 420.

      Von jedem Menschen geht ein Licht aus, 
      das direkt zum Himmel hinauf strahlt. 
      Wenn sich zwei Seelen finden, 
      die füreinander bestimmt sind, 
      dann fließen ihre beiden Lichtströme zusammen, 
      und aus der Vereinigung ihres Wesens steigt ein einziges, 
      helleres Licht nach oben.
      Baal Shem Toy

 421.

      Wo Fehler sind, da ist auch Erfahrung.
      AntonTschechow

 422.

      Denken macht intelligent, Leben klug.
      Peter Tille

 423.

      Die Einwohnende Herrlichkeit umfaßt alle Welten,
      alle Kreaturen, Gute und Böse.
      Und sie ist die wahre Einheit.
      Wie kann sie denn Gegensätze des Guten 
      und des Bösen in sich tragen?
      Aber in Wahrheit ist da kein Gegensatz,
      denn das Böse ist der Thronsitz des Guten.
      Baal Schem Tow

 424.

      Vergangenheit hängt nicht mehr von uns ab,
      doch die Zukunft bestimmen wir.
      Tschaadjew

 425.

         Der verständige Zuhörer ist der
      Geburtshelfer meiner Gedanken.
      Charles Tschopp

 426.

      Reusen werden gebraucht, um Fisch zu fangen, 
      wenn aber der Fisch gefangen ist, 
      vergessen die Menschen die Reusen.
      Fallen werden gebraucht, um Hasen zu fangen, 
      wenn aber die Hasen gefangen sind, 
      vergessen die Menschen die Fallen. 
      Worte werden gebraucht, um Ideen mitzuteilen, 
      wenn die Ideen aber begriffen sind, 
      vergessen die Menschen die Worte.
      Tschuang Tse

 427.

      Weder Mann noch Frau wissen, 
      was vollkommene Liebe ist,
      ehe sie nicht ein Vierteljahrhundert verheiratet waren.
      Mark Twain

 428.

        Freundlichkeit ist eine Sprache,
      die der Blinde lesen und der Taube hören kann.
      Mark Twain




 429.

      Besonnenheit ist die unzertrennliche 
      Begleiterin der Weisheit.
      Eine Änderung des Bewusstseins 
      ändert unbewusst auch das Sein.
      Gerhard Uhlenbruck

 430.

      Nicht die Aufgaben sollen einem über den Kopf wachsen,
      sondern der Kopf über den Aufgaben wachsen.
      Gerhard Uhlenbruck

 431.

      Du bist wie deine tiefen, drängenden Wünsche.
      Wie deine Wünsche, so ist dein Wille.
      Wie dein Wille, so ist deine Tat,
      und wie deine Tat, so ist dein Schicksal.
      Upanischaden

       

 432.

      Menschlichkeit ist die erste Tugend.
      Vauvenargues

 433.

      Heute wird es Zeit für all das, 
      was gestern noch Unsinn war.
      E. Verharren

 434.

      Die Menschen sind doch dazu da,
      einander auszuhelfen.
      Voltaire




 435.

      Jeder von uns besitzt alles, was er braucht, 
      um sein tiefstes Wesen zu erforschen... 
      in der ganzen Menschheit gibt es niemanden,
      der das für uns tun könnte. 
      Die Verantwortung und die Möglichkeit, 
      uns unser wahres Wesen bewusst zu machen und es
      mit anderen zu teilen, liegt letztlich bei uns.
      Roger Walsh und Dean Sharpio

 436.

      Das Hohe der Menschen ist ihr Verstand, 
      aus der Prägung desselben ergibt sich die Vernunft.
      Jürgen Weiprecht

 437.

      Eine Erkenntnis in der Welt ist nicht der Stein der Weisen,
      sondern ein neuer Anfang.
      Jürgen Weiprecht

 438.

      Das Wissen um das morgige Dasein ersetzt nicht 
      das Wissen um das Sein. 
      Jürgen Weiprecht

 439.

      Wir sind selbst verantwortlich für das,
      was kommt, und wir müssen deshalb
      auf unsere Vernunft und unser Gewissen
      hören und gegebenenfalls unsere Stimme erheben.
      Jürgen Weiprecht

 440.

      Ein jeder hat ein Recht sich vom anderen zu erholen,
      um seine Gedanken und Ideen zu fassen.
      Jürgen Weiprecht

 441.

      Das Schöne ist meist nur ein Traum. 
      Aber ein Traum wirkt im Verstand 
      und dieser wirkt nach außen.
      Jürgen Weiprecht

 442.

      Intelligenz stellt eine der unendlich vielen Galaxien dar,
      welche in einem Mikrokosmos auftreten, 
      doch sind diese Galaxien im Makrokosmos 
      auch als Mensch umschrieben.
      Jürgen Weiprecht

 443.

      Die Welt zu begreifen, heißt sie zu verändern, 
      auch auf die Gefahr hin, 
      dass diese Veränderung progressiver ausfällt, 
      als das, was als progressiv gilt.
      Jürgen Weiprecht

 444.

      Das menschliche Vorstellungsvermögen muss in der Lage sein, 
      die Grenzen physikalischer Gesetze zu überschreiten, 
      ehe es diese Gesetze überhaupt verstehen kann.
      Joseph Weizenbaum

 445.

         Wir sind immer erbitterte Moralisten,
      wenn es sich um andere handelt.
      Orson Welles

 446.

       Das beste Mittel gegen Verdrossenheit ist es,
      sich selbst zu aktivieren.
      Richard von Weizsäcker

 447.

      Affekte sind unterlassene Handlungen.
      Carl Friedrich von Weizsäcker

 448.

      Der sicherste Reichtum ist die Armut an Bedürfnissen.
      Franz Werfel

 449.

      Die Welt ist in zwei Klassen geteilt:
      In diejenigen, die das Unglaubliche glauben
      und diejenigen,
      welche das Unwahrscheinliche tun.
      Oscar Wilde

 450.

        Fortschritt ist die Verwirklichung von Ideen.
      Oscar Wilde

 451.

      Unzufriedenheit ist der erste Schritt zum Erfolg.
      Oscar Wilde

 452.

      Wir sind selbst verantwortlich für das, was kommt,
      und wir müssen deshalb auf unsere Vernunft 
      und unser Gewissen hören
      und gegebenenfalls unsere Stimme erheben.
      Adolf Wirz

 453.

      Worüber man nicht sprechen kann, 
      darüber muss man schweigen.
      L. Wittgenstein

 454.

      Eine der am meisten irreführenden Darstellungsweisen
      unserer Sprache ist der Gebrauch des Wortes "ich"...
      Ludwig Wittgenstein

 455.

      Mutig ist, der weiß, dass vor ihm eine Gefahr liegt,
      sich aber dennoch mit ihr auseinandersetzt.
      Xenophon

 456.

      Wer einmal sich selbst gefunden,
      der kann nichts auf der Welt verlieren.
      Stefan Zweig 		

"""
	author = AUTHORS.appendRow(name="TODO")
	de = LANGS.peek('de')
	for z in re.split("#|[0123456789]+\."):
		z = z.strip()
		l = z.splitlines()
		body = "\n<br>".join(l[:-1])
		authorName = l[:-1]
		db.installto(globals())

		ds = QUOTES.findone(name=authorName)
		QUOTES.appendRow(abstract=body,author=author,lang=de)
			
			
			
	
	
