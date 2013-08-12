Configure :mod:`notes <lino.modlib.notes>` templates
====================================================

TODO: translate this to English.

When rendering a :class:`lino.modlib.notes.models.Note`, 
there is an additional name ``body`` 
(besides the standard names documented in :doc:`templates_api`), 
and this ``body`` is the entry point to what we call "body templates".

The purpose of body templates is to provide a system for defining 
default text content templates. 
For example :ref:`welfare` comes with a lot of predefined 
attestations whose content is the same for every PCSW.

Im Web-Interface unter :menuselection:`Configure --> NoteTypes` müssen die Notizarten definiert werden.

.. image:: 1010a.jpg
    :scale: 70


- print_method:
 
  - Wenn dieses Feld leer ist, kann eine Notiz dieser Art nur am Bildschirm konsultiert werden und ist nicht druckbar.
  - In der Auswahlliste stehen zwar weitere Methoden, aber funktionieren tut bis auf weiteres nur die Methode AppyPrintMethod.

- template:

  - Wenn eine Druckmethode angegeben ist, muss außerdem im Feld `template` eine Vorlagedatei ausgewählt werden.
  
- body_template

  - Defines an optional template which will be rendered into the `body` variable.


Für den Systemverwalter
-----------------------

Seit Mai waren wir uns ja einig, dass AppyPrintMethod die einzige gangbare Strategie ist. 
Dabei wird das Modul `pod <http://appyframework.org/pod.html>`_ (Python Open Document) 
aus dem Framework "Appy" (Applications in python) benutzt.
"pisa" werden wir so schnell nicht benutzen, weil man dann HTML-Dateien editieren muss, um Dokumentvorlagen zu bearbeiten. 
Bevor ich mit Pisa anfinge, würde ich eher LaTeX benutzen.
RTF funktioniert noch nicht, dazu müsste ich zunächst ein neues Templatesystem finden oder selberschreiben, denn das Template-System von Django verträgt keine RTF-Dateien. 


Der Lino-Server sucht die Vorlagedateien im Verzeichnis :file:`/usr/local/lino/templates/appy/de`
(`de` weil das die :attr:`Standardsprache <lino.utils.babel.DEFAULT_LANGUAGE>` des Lino-Sites ist,
`/usr/local/lino` weil das in :setting:`DATA_DIR` als euer lokales Lino-Verzeichnis definiert ist).
Das templates-Verzeichnis muss pro unterstützter Sprache ein entsprechendes Unterverzeichnis (`de`, `fr`, `en`,...) haben. 
Die Sprache wird in :attr:`lino.mixins.printable.PrintableType.template` nicht gespeichert und erscheint auch nicht in der Auswahlliste. 
Dort werden immer die Templates der Hauptsprache angezeigt. 


Um die Dateien auch von einem Windows-Rechner aus bearbeiten zu können, könnte
`/usr/local/lino` ein Link nach (z.B.) :file:`F:\\ANWPROG\\LINO` sein.

Die Vorlagedateien müssen ausgehend von den bestehenden Word-Dateien mit OpenOffice erstellt werden. 
Die einzelnen Felder müssen dabei, wie bei appy_pod dokumentiert eingebunden werden:

- http://appyframework.org/podWritingTemplates.html
- http://appyframework.org/podWritingAdvancedTemplates.html


