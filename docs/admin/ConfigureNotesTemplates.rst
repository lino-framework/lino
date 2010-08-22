Notizvorlagen konfigurieren
===========================

Allgemeine Vorgehensweise
-------------------------

Im Web-Interface unter Configure / NoteTypes müssen die Notizarten definiert werden.
 
Im Feld `print method` gibt es momentan appy, rtf und pisa. 
"pisa" werden wir so schnell nicht benutzen, weil man dann HTML-Dateien editieren muss, um Dokumentvorlagen zu bearbeiten.
Bevor ich mit Pisa anfinge, würde ich eher LaTeX benutzen.
RTF funktioniert noch nicht, dazu müsste ich zunächst ein neues Templatesystem finden oder selberschreiben, 
denn das Template-System von Django verträgt keine RTF-Dateien. 
Also bleibt nur Appy, und wir waren uns ja auch einig, dass das fürs Erste reicht.

`print method` kann auch leer sein. 
Eine Notiz dieser Art kann dann eben nur am Bildschirm konsultiert werden und ist nicht druckbar.

Dann muss im Feld `template` eine Vorlagendatei ausgewählt werden. Welche Dateien dort angezeigt werden, kann man momentan nicht übers Web-Interface konfigurieren, und bis auf Weiteres sehe ich auch keinen Bedarf dazu. Der Lino-Server sucht diese Dateien im Verzeichnis `/local/lino/templates/appy`. Dieses Verzeichnis könnte z.B. ein Link nach F:\ANWPROG\LINO\TEMPLATES\APPY sein.

Die Vorlagedateien müssen ausgehend von den bestehenden Word-Dateien mit OpenOffice erstellt werden. Die einzelnen Felder müssen dabei, wie in http://appyframework.org/pod.html dokumentiert, eingebunden werden.

Sprachabhängige Auswahl der Notizvorlage
----------------------------------------

Das ist noch nicht implementiert.