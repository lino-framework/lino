To-Do-Liste
===========

Kurzfristig
-----------

- Kolonnenfilter. Beispiel: 
  `1 <http://www.ajung.de/2009/03/24/extjs-erweiterter-list-filter/>`__ 
  `2 <http://www.sk-typo3.de/ExtJS-Filter-Grid.345.0.html>`__ 
  `3 <http://extjs.com/forum/showthread.php?t=14503>`__

- Der Tool-Button zum Speichern der Konfiguration gehört nicht mehr in den Rahmen des "Fensters", sondern in die tbar des GridPanels. Das Ganze heißt auch nicht mehr "window config", sondern "grid config". 
  Neben Kolonnenbreiten müssen darin auch Kolonnenreihenfolge, Kolonnenfilter und Daten-Sortierfolge
  gespeichert werden.
  Außerdem sollte man benutzerdefinierte grid configs erstellen und auswählen können.

- Sprachabhängige Auswahl der Notizvorlage. Wenn Sprache der Notiz nicht die Hauptsprache des Lino-Sites ist, dann wird der Name des zu verwendenden Templates aus dem Standardnamen par convention abgeleitet, indem das Sprachkürzel als Suffix vor der Erweiterung eingefügt wird. Zum Beispiel für eine Telefonnotiz in `fr` auf einer Site mit Hauptsprache `de` (und Telefonnotizen haben `NoteType.template` den Wert `phone.odt` ) sucht Lino zuerst nach einer Datei `phone_fr.odt`. Wenn es so eine Datei nicht gibt, nimmt er die `phone.odt`. (Korrektur: nicht als Suffix, sondern in einem separaten Verzeichnis. Sonst muss ich ja beim Füllen der Auswahlliste die Fremdsprachen rausfiltern).

- South aktivieren


Kleinkram
---------

- Das Passfoto in dsbe.PersonDetail ist manchmal verzerrt oder noch nicht korrekt ausgeschnitten.

- Die Buttons der tbar sollten mit schönen Icons versehen werden. Für manche Funktionen (Insert,Delete) gibt es vielleicht schon Icons aus der ExtJS.

- Abfragen mit komplexen Bedingungen zur Suche nach Personen

- Die Zeilenhöhe einer Grid muss einen sinnvollen Maximalwert kriegen. In Explorer / Notes hat man momentan den Eindruck, dass es nur eine Zeile gibt; in Wirklichkeit ist der Memo-Text der ersten Zeile so lang, dass die Zeilenhöhe größer als das Fenster ist.

- Hinter das QuickFilter-Feld muss ein Button, um den Filter zu aktivieren. Dass man einfach nur ENTER drücken muss ist nicht intuitiv.

- Links ordentlich anzeigen und bequem erfassen können.

- Kolonnen-Reihenfolge speichern können.

- Benutzbarkeit per Tastatur verbessern (issue 11, issue 64) 

- Sehen können, nach welcher Kolonne eine Grid sortiert ist.

- Nach Duplikaten suchen vor Erstellen einer neuen Person (issue 85)

- URLs per drag & drop registrieren können

- `lino.test_apps.journals` funktioniert nicht bzw. wird nicht ausgeführt. Sieht aus als Django-Ticket 11696 doch noch nicht behoben ist. Aber mein Patch 20091107.diff funktioniert nicht mehr und ich bin auch noch nicht sicher. Muss vielleicht mal einen Testcase schreiben, um das Problem zu identifizieren...

- Prüfen, ob die neuen ExtJS-Features `Forms with vbox Layout <http://dev.sencha.com/deploy/dev/examples/form/vbox-form.html>`_ und
  `Composite Form Fields <http://dev.sencha.com/deploy/dev/examples/form/composite-field.html>`_ für Lino interessant sind.

Dokumentation
-------------

- Anwendung lino.demo, die zum Generieren der Sphinx-Dokumentation bentuzt wird.
- Intersphinx nutzen und Lino von Lino-DSBE trennen
- dsbe.saffre-rumma.ee und igen.saffre-rumma.ee sollten nicht die Demo, sondern die Projekt-Doku zeigen. Für Demos wäre es ja elegant, einen Site demos.s-r.ee zu haben. Aber einfacher ist wahrscheinlich dsbe-demo.s-r-ee

Langfristig
-----------

- Filter auf virtuelle Kolonnen setzen können. Siehe :doc:`/blog/2010/0811`.

- Layout von Detail-Fenstern : in Lino sind die "Zeilen" momentan ja immer im "Blocksatz" (also links- und rechtsbündig). Das ist unkonventionell: alle RIA die ich kenne, machen ihre Formulare nur linksbündig.

- HtmlEditor oder TextArea? Der HtmlEditor verursacht deutliche Performanceeinbußen beim Bildschirmaufbau von Detail-Fenstern. Die Wahl sollte konfigurierbar sein. Markup auch.

- "About"-Fenster mit `thanks_to()` muss irgendwo sichtbar gemacht werden.

- lino.test_apps.properties funktioniert nicht, scheinbar ist `actors.discover()` nicht aufgerufen worden.

- Das Detail-Fenster sollte vielleicht par défaut nicht im Editier-Modus sein, sondern unten ein Button "Edit", und erst wenn man darauf klickt, werden alle Felder editierbar (und der Record in der Datenbank blockiert), und unten stehen dann zwei Buttons "Save" und "Cancel". Wobei darauf zu achten ist was passiert, wenn man während des Bearbeitens in der Grid auf eine andere Zeile klickt. Dann muss er am besten das Detail-Fenster speichern, und falls dort ungültige Daten stehen, in der Grid den Zeilenwechsel verweigern.

- `Report.date_format` muss in der Syntax des UI (d.h. ExtJS) angegeben werden. 

- Scripts wie :xfile:`fill.py`, :xfile:`load_tim.py`, :xfile:`send_invoices.py` usw. sollten durch `django-admin commands <http://docs.djangoproject.com/en/dev/howto/custom-management-commands/#howto-custom-management-commands>`_ ersetzt werden. Dazu brauche ich wahrscheinlich ein `Signal <http://docs.djangoproject.com/en/dev/topics/signals/>`_, das bei jedem Start eines Management Tools nach dem Laden der Modelle gefeuert wird. Vor load_data. Dort würde ich dann mein LinoSite.setup() aufrufen. Sieht aus wie `Django-Ticket 13024 <http://code.djangoproject.com/ticket/13024>`_.

- Prüfen, ob Dokumentvorlagen im `XSL-FO-Format <http://de.wikipedia.org/wiki/XSL-FO>`__ besser wären. `Apache FOP <http://xmlgraphics.apache.org/fop/>`__ als Formatierer. Warum OpenOffice.org nicht schon lange XSL-FO kann, ist mir ein Rätsel. AbiWord dagegen soll es können (laut `1 <http://www.ibm.com/developerworks/xml/library/x-xslfo/>`__ und `2 <http://searjeant.blogspot.com/2008/09/generating-pdf-from-xml-with-xsl-fo.html>`__).

- Inwiefern überschneiden sich :mod:`lino.modlib.system.models.SiteConfig` und :mod:`django.contrib.sites`? 

- Actions:

  - Aktionen brauchen nicht unbedingt in :meth:`lino.reports.Report.do_setup` instanziert zu werden. Von den Standard-Aktionen GridEdit, DeleteSelected usw. reicht eine einzige Instanz. :attr:`Action.actor` käme dann weg, und :meth:`Action.__str__` könnte dann in dieser Form nicht mehr benutzt werden.
  - :attr:`Action.name` ist ja im Grunde ein kurzer Name, der pro Actor identifizierend ist. Der Vorteil ist, dass man sich beim Entwerfen von Reports keinen solchen Namen auszudenken braucht, also dass der Programmierer einer  Aktion auch deren Namen festlegt. Wenn zwei verschiedene Aktionen den gleichen Namen haben, wird nur die letzte beibehalten und eine Warnung in der :file:`lino.log` gemacht.
  - Übersicht der Aktionen, die momentan benutzt werden:

  ====================== ============= =======================================================
  Klasse                 Name
  ====================== ============= =======================================================
  actions.Action
  mixins.PrintAction     
  mixins.DocumentAction  print         Dokument für diesen Record anzeigen (vorher falls nötig generieren)
  mixins.ImageAction     image         Bild für diesen Record anzeigen 
  reports.ListAction
  GridEdit               grid          Report im Listeneditor zum Bearbeiten anzeigen
  ShowDetailAction       detail        Diesen Record in Detail-Fenster zum Bearbeiten anzeigen
  InsertRow              insert        Insert-Fenster anzeigen (mit leeren Feldern bzw. Standardwerten, und mit OK-Button)
  SubmitDetail           SubmitDetail  OK-Button in detail
  SubmitInsert           SubmitInsert  OK-Button in insert
  ====================== ============= =======================================================

- Die interne Kolonnenliste eines Reports ist ja konstant. Also sollte ein Record im fmt=json nicht als ``dict`` sondern als ``list`` repräsentiert werden.

   