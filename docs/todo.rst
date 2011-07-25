To-do list
==========

Public calls for help
---------------------

See also :doc:`/tickets/index` which is a list of tickets.

.. todolist::


The rest of this document is partly in German 
because it is rather for internal use. 


Short-term
----------

#.  Jetzt wo es aktive Felder gibt, sollte das Formular während des submit 
    deaktiviert werden, immerhin dauert das manchmal eine Sekunde.
    
#.  Man kann scheinbar weder in GroupWise noch in Zarafa 
    externe ("remote") Kalender konfigurieren (so wie `Google und Sunbird
    <http://www.google.com/support/calendar/bin/answer.py?answer=99358#sunbird>`_)
    Lino muss also nicht selber Server sein, 
    sondern eher als Client mit einem CalDAV-Server arbeiten. 

#.  Lino könnte per LDAP-Request verschiedene Angaben 
    in :class:`auth.User` (Name, E-Mail,...) 
    direkt vom LDAP-Server anfragen.
    Dazu wären wahrscheinlich
    http://www.python-ldap.org/
    und
    http://www.openldap.org/
    nötig.

#.  Listings : Listing.odt muss noch gemacht werden.

#.  Ausdruck Verträge: jetzt wo die mehrzeiligen Textfelder formatierbar 
    sind, kommt vielleicht ein kleines Problem: Bisher wurde z.B. in der 
    Dokumentvorlage ein Wort vor dem eigentlichen Text eingefügt, 
    wenn dieser nicht leer war. Z.B. Wenn man im Feld "Zielsetzungen" 
    den Text "Blablabla..." eintrug, dann wurde "Zielsetzungen: Blablabla..." 
    gedruckt. Um das in dieser Form zu erhalten, müsste ich einen Patch für 
    :term:`appy.pod` schreiben, der folgendes ermöglicht::
    
      do text
      from html(self.goals,wrapper="<p><b>Zielsetzungen</b>: %s </p>")

#.  Button "Cache löschen" deaktivieren, wenn
    :attr:`lino.mixins.printable.Printable.must_build` `True` ist.
    Dazu muss `disabled_fields` in der :xfile:`linolib.js` auch 
    auf actions angewendet werden.

#.  Externe Links (Lesezeichen) und Uploads per drag & drop machen können, 
    indem man sie von einer anderen Anwendung auf die HtmlBox zieht.
    (u.a. :doc:`/tickets/8`)

#.  :doc:`Benutzerspezifische Gridkonfiguration </tickets/39>`

#.  Feldgruppen: Die Felder Note.person und Note.company 
    sollten als Gruppe mit Bezeichung "Partner" ersichtlich sein.
    Um eine Gruppe von Feldern mit einem Label 
    versehen zu können, 
    brauche ich wahrscheinlich die :doc:`neue Syntax in .dtl-Dateien </tickets/34>`.
    
#.  Doppelklick auf Memo-Text einer Note bewirkt *nichts*. 
    Sollte doch wenigstens das Detail-Fenster öffnen.
    
#.  Buttons sollten gleich nach einem Klick deaktiviert werden, 
    bis die Aktion abgeschlossen ist.
    Wenn man z.B. auf den Lebenslauf-Button doppelt klickt, versucht 
    er zweimal kurz hintereinander das gleiche Dokument zu generieren. 
    Beim zweiten Mal schlägt das dann logischerweise fehl. 
    Er öffnet dann zwei Fenster, eines mit dem Lebenslauf und ein 
    anderes mit der Fehlermeldung 
    "Action Lebenslauf failed for Person #22315: I
    need to use a temp folder
    "/usr/local/django/dsbe_eupen/media/cache/appypdf/contacts.Person-22315.pdf.temp"
    but this folder already exists."


Medium-term
-----------

#.  Bug in :term:`appy.pod`: https://bugs.launchpad.net/appy/+bug/815019

#.  Beim Entserialisieren mit `lino.utils.dpy` gehen alle modified-Daten 
    verloren (werden auf den Zeitpunkt des Wiedereinlesens gesetzt).

#.  Client-seitiger Ersatz für den "Memo"-Button, der seit 
    :doc`/blog/2011/0605` wieder raus ist.
    Mir war klargeworden, dass diese Lösung (Memo-Felder auf Anfrage 
    schon serverseitig abzuschneiden) erstens theoretisch Unsinn war 
    und zweitens in der Praxis noch einige Bugs hatte. Momentan wird 
    in der Grid immer nur die Kurzform angezeigt (`overflow:hidden;`), 
    und irgendwann muss ich mal eine client-seitige Lösung in Javascript 
    machen. Interessant wäre, wenn man die Höhe einzelner Zeilen 
    manuell verändern kann. Eventuell den Text-Editor im eigenen 
    Fenster aufrufen bei Doppelklick.


#.  Pro Ereignisart könnte ein Feld "muss manuell erledigt werden" kommen, 
    das würde dann verhindern, dass entsprechende Erinnerungen 
    automatisch aus dem Hauptbildschirm verschwinden.

#.  Mail-Interface, Posteingang : 
    Lino-Server empfängt E-Mails, die teilweise geparst werden und/oder 
    manuell durch den Benutzer weiter verwaltet werden.
    
#.  Hinter das QuickFilter-Feld sollte ein Button, um den Filter zu aktivieren. 
    Dass man einfach nur TAB drücken muss ist nicht intuitiv.

#.  CheckColumns sollten auf Tastendruck SPACE toggeln.

#.  Auswahllisten in FKs zu `languages.Language` und `countries.Country`: 
    Einträge sollten alphabetisch sortiert sein.
    
#.  Wie kann man in der Dokumentvorlage `cv.odt`
    an Führerschein und Informatikkenntnisse rankommen?

#.  Wenn man in einer Grid das Detail eines Records aufruft, 
    dann erscheint kein "Bitte warten" bis das Fenster erscheint.
    Und bei Personen dauert das mehrere Sekunden.
    :doc:`/tickets/21`.


Later
-----

#.  Ein Test in der Lino-Suite funktioniert offenbar nur, wenn man `de` als 
    Hauptsprache hat::

      FAIL: test_them_all (lino.apps.dsbe.tests.dsbe_demo_tests.DemoTest)
      ----------------------------------------------------------------------
      Traceback (most recent call last):
        File "/var/snapshots/lino/lino/utils/test.py", line 87, in test_them_all
          v(self)
        File "/var/snapshots/lino/lino/apps/dsbe/tests/dsbe_demo_tests.py", line 71, in test02
          self.assertEqual(row[0],"Gehorsam")
      AssertionError: u'Ob\xe9issant' != 'Gehorsam'

#.  An makedocs müsste ich bei Gelegenheit mal ein bisschen weiter machen. 
    Das ist noch lange nicht fertig.
    
#.  In einer Grid mit Notizen die Hintergrundfarbe jeder Reihe 
    abhängig von Notizart und/oder Ereignisart machen.

#.  Welche weiteren Felder müssen (ähnlich wie "Stadt") lernfähig werden? 
    Vorschläge: 
    
    - lino.mixins.reminders.Reminder.reminder_subject
    - lino.apps.dsbe.models.Study.content
    
#.  :doc:`/tickets/41`

#.  Erinnerungen gar nicht mehr im Lino-Hauptbildschirm, sondern nach GW schicken?
    Oder GW neu schreiben?
    
#.  igen : Partner.get_invoice_suggestions()

#.  MTI auch für Personen anwenden: 
    in lino.dsbe für "normale" Personen nur die 
    Standard-Kontaktangaben speichern, und die DSBE-spezifischen Felder 
    in einer eigenen Tabelle. 

#.  Momentan ist es nicht möglich, "mal eben" eine Suche zu machen, 
    die **nicht** gespeichert wird.
    Stört das?
    Deshalb ist momentan übrigens der Titel einer Suchliste ein 
    obligatorisches Feld.

#.  Wenn die Konfiguration einer Grid verändert wurde und man 
    aus Versehen auf einen Kolonnentitel klickt, dann wird die Grid 
    sortiert und neu geladen, und alle ungespeicherte Konfiguration ist futsch.
    Vor dem Sortieren nachfragen "Änderungen in GC speichern ?".
    Diese Frage wohl nur für Benutzer, die GCs auch speichern dürfen.

#.  save_grid_config könnte nachfragen bevor er die GC abspeichert.

#.  Die Konfigurationsparameter 
    `residence_permit_upload_type`, 
    `work_permit_upload_type` und 
    `driving_licence_upload_type`, 
    die momentan als Klassenattribute 
    in :class:`lino.apps.dsbe.settings.Lino`
    implementiert sind, sollten 
    ebenfalls zu Feldern in der SiteConfig konvertiert werden.
    Aber Vorsicht, denn wenn die verändert werden muss 
    vielleicht die :xfile:`lino.js` 
    neu generiert werden.

#.  Decide some relatively stable Django version to use,
    because simply getting the latest snapshot each time 
    is a bit dangerous on a production server.

#.  DELETE (per Taste) auf einer Zeile in Teilnehmer oder Kandidaten funktioniert. 
    Aber dort soll man nicht löschen können.

#.  Die Titel der Reiter (.dtl-Dateien) sind momentan noch nicht 
    internationalisiert, stehen also in den Konfigurationsdateien 
    in hardkodiertem Deutsch drin. 
    Also bis zur ersten Lino-Demo in FR oder NL muss ich mir dazu
    noch was einfallen lassen.

#.  Wenn man die Rückfrage nach "Delete" zu schnell beantwortet, 
    wird die Grid nicht aktualisiert. 
    Der Fehler funktioniert nicht immer. 
    Ich warte auf weitere Beobachtungen.

#.  Reminders als "gelesen" markieren können.
    
#.  Im `search_field` funktionieren die Tasten HOME und END nicht.
    Oder genauer gesagt werden die von der Grid abgefangen und verarbeitet.

#.  DuplicateRow / Insert as copy (Kopie erstellen). 
    Evtl. stattdessen zwei Buttons "Export" und "Import". 
    Mit "Export" lässt man den aktuellen Record in eine 
    lokale Datei abspeichern (Format z.B. json oder xml), und mit "Import" 
    überschreibt man den aktuellen Record durch die Daten aus einer 
    hochzuladenden Datei.
    
#.  Lästig ist, dass nach dem Bearbeiten einer Zelle der Focus auf die 
    erste Zeile zurück springt.

#.  Man kann momentan keine Filter "not empty" und "empty" setzen.

#.  CompositeFields nutzen:
    http://dev.sencha.com/deploy/dev/examples/form/composite-field.html
    
#.  Minify :xfile:`lino.js`
    http://en.wikipedia.org/wiki/Minification_(programming)

#.  Dublettenkontrolle. Nach Duplikaten suchen vor Erstellen einer neuen Person.
    Erstellen einer neuen Person muss verweigert werden, wenn 
    Name und Vorname identisch sind **außer** wenn beide ein unleeres Geburtsdatum 
    haben (und nicht das gleiche).

#.  Im Hauptmenü könnten zwei Befehle :menuselection:`Help --> User Manual` 
    und :menuselection:`Help --> About` kommen, dann hätten wir den ganzen 
    Platz für Erinnerungen.

#.  Wenn man z.B. in Companies.insert manuell eine ID eingibt, 
    dann ignoriert der Server die und vergibt trotzdem seine automatische nächste ID.

#.  Reminders arbeiten momentan mit zwei Feldern delay_value und delay_type.
    Schöner wäre ein TimeDelaField wie in 
    http://djangosnippets.org/snippets/1060/


#.  Idee: Vielleicht müsste contacts.Person doch nicht abstract sein, und
    lino.dsbe stattdessen ein neues Modell CoachedPerson(contacts.Person) 
    definieren. 
    Dann hätten "normale" Kontaktpersonen von Firmen gar 
    nicht die vielen Felder des DSBE.
    Dazu wäre ein Feld Person.type nötig.
  
#.  Idee: Module umstrukturieren:

    | lino.dsbe.models : Contract usw.
    | lino.dsbe.contacts.models : Person, Company,...
    
    also nicht mehr mit einem manuellen `app_label` arbeiten. 
    Kann sein, dass South dann funktioniert.

#.  Auswahlliste `Contract.exam_policy` (Auswertungsstrategie) 
    wird auch in französischen Verträgen deutsch angezeigt.
    Das ist nicht schlimm und vielleicht sogar erwünscht.

#.  Arbeitsregime und Stundenplan: 
    Nach Ändern der Sprache ändert sich nicht immer die Auswahlliste.
    Vielleicht sollten diese Felder auch wie 
    die Auswertungsstrategie als ForeignKeys 
    (ohne die Möglichkeit von manuellen Eingaben) implementiert werden.
   
#.  Liste der Personen sollte zunächst mal nur "meine" Personen anzeigen.
    Evtl. neue Menübefehle "Meine Personen" und "Meine Coachings".

#.  HTML-Editoren haben noch Probleme (Layout und Performance) und sind deshalb 
    momentan deaktiviert. 
    
#.  Arbeitsregime und Stundenplan: 
    Texte in Konfigurationsdateien auslagern

#.  How to import, render & edit BIC:IBAN account numbers?

#.  The main window also needs a `Refresh` button. 
    Or better: should be automatically refreshed when it was hidden by another 
    window and becomes visible again.
  
#.  MyUploads müsste eigentlich nach `modified` sortiert sein. Ist er aber nicht.
    Idem für MyContracts. 

#.  Im Kontextmenü sollten auch Aktionen erscheinen, die spezifisch 
    für das Feld (die Kolonne) sind. 
  
#. Im Detail eines Links wäre dessen Vorschau interessant.

#. RtfPrintMethod geht nicht immer: 
   http://127.0.0.1:8000/api/dsbe/ContractsByPerson/2?mt=14&mk=16&fmt=print 
   sagt "ValueError: 'allowed_path' has to be a directory."

#. Ein ``<a href="..." target="blank">`` öffnet zumindest in Chrome kein neues Fenster, 
   sondern einen neuen Tab im gleichen Fenster. 
   Idem für `window.open('URL','_blank')`.
   Ich weiß nicht, wie man das abstellen kann, aber hier immerhin ein Workaround: 
   wenn man den Titel des 
   Browser-Tabs aus dem Browserfenster raus zieht, dann öffnet er ein neues Fenster.

#. ui.get_detail_url() gibt eine URL, die den betreffenden Record öffnet. 
   Wird benutzt, um in der `welcome.html` die Reminder eines Vertrags oder eines Uploads anklickbar zu machen.
   In diesem Detail sollten jedoch keine Navigations-Buttons sein, 
   denn die beziehen sich ja dann auf den selten benutzten Model-Report Contracts bzw. Uploads, 
   der die Records aller Benutzer und Personen durchblättert.

#. It is not possible to select multiple rows when using CellSelectionModel 
   (which is Lino's default and which cannot be changed for the moment).
   Maybe add a button to switch between the two selection models?
   Caution: delete_selected currently probably works only with a CellSelectionModel.

#. Make it configurable (site-wide, per user,...)
   whether external links should open a new window or not.

#. do we need a general button "Printer-friendly view"?

#.  Formatierung der :xfile:`welcome.html` lässt zu wünschen übrig.  
    Evtl. stattdessen einen kompletten Kalender:
    http://www.sencha.com/blog/2010/09/08/ext-js-3-3-calendar-component/

#. Wie kann ich die Test-Templates für Notizen in den code repository rein kriegen?
   Er soll sie dann auch unabhängig von der Sprache finden. 
   Vielleicht werde ich doctemplates in die config-directories verschieben 
   und mein System von config-Dateien erweitern, dass es auch Unterverzeichnisse verträgt.
   Siehe :doc:`/blog/2010/1029`, :doc:`/blog/2010/1112`.
  
#.  Hauptmenü nicht anzeigen, wenn ein Fenster offen ist. 
    Stattdessen ein bequemer Button, um ein weiteres Browserfenster mit Lino zu öffnen.
    Weil die Benutzer sonst irgendwann einen Stack overflow kriegen, 
    weil sie sich nicht dessen bewusst sind, 
    dass ihre Fenster offen bleiben.
    (Das hätte möglicherweise später als Folge, dass das Hauptmenü gar kein Pulldown-Menü mehr zu sein braucht, 
    sondern eine für Webseiten klassischere Ansicht benutzen.)
  
#.  Man kann z.B. noch nicht nach Personen suchen, die ein bestimmtes Studium haben.

#.  Einheitliches Interface um Reihenfolge zu verändern (Journals, DocItems, LinksByOwner,...). 
    Erster Schritt: Abstract model "Ordered" mit einem Feld `pos` und zwei Actions "move up" und "move down".

#.  Eingabe im Detail eines SalesDocument funktioniert noch nicht: 
    Wenn man ein 
    Produkt auswählt, antwortet der Server 
    `{'unit_price': ValidationError([u'This value must be a decimal number.'])}` 
    statt den Stückpreis selber auszufüllen.
  
#.  Fenstertitel ändern bzw. anzeigen, welche GC momentan aktiv ist.

#.  Was soll passieren wenn man Contract.company ändert, nachdem Contract.contact schon ausgefüllt ist?
    Automatisch neuen Kontakt mit gleicher Person und Eigenschaft für die andere Firma anlegen?
    ValidationError?
    Am ehesten wäre: contact auf leer setzen.

Long-term
---------

#. :doc:`/tickets/12`

#. Projekte für DSBE einführen? 
   Gibt es nicht in der Praxis den Fall, dass man Notizen machen will, 
   die "in einen Topf" gehören, aber dieser "Topf" kann 
   nicht unbedingt einer (einzigen) Personen zugewiesen werden?
   Falls das häufig vorkommt, schlage ich vor, dass wir noch das Konzept der Projekte einführen.
   Pro Person müsste man per Klick leicht ein Begleitungsprojekt anlegen können. 
   Bei Import und Synchronisierung würden automatisch auch diese Projekte synchron gehalten. 
   Dienstleistungen sind nicht mehr einer Person und/oder einer Firma, 
   sondern allgemein einem Projekt zugewiesen.
   Momentan entspricht sozusagen automatisch jede Person einem einzigen Projekt.
  
#. Das `params={'base_params':{'mk':jnl.pk}}` in der :xfile:`lino_settings.py` 
   in :mod:`lino.demos.igen`
   entspricht natürlich nicht dem Designprinzip, dass das Anwendungsmenü unabhängig 
   vom UI sein soll.
   stattdessen muss dort `master_id=jnl.pk` stehen, und beim Generieren des 
   Menübefehls muss also ein ReportRequest instanziert werden, oder 
   vielleicht nur `Report.get_master_kw(master_instance)` rufen.
  
#. (:mod:`lino.modlib.dsbe` : 
   Wie soll ich es machen, dass der Benutzer beim Auswählen der Krankenkasse einer Person 
   nicht alle Firmen, sondern nur die Krankenkassen angezeigt bekommt? 
   Etwa ein eigenes Feld `Company.is_health_insurance`?
   Oder auf den Berufscode filtern?

#. Die Buttons der tbar sollten mit Icons versehen werden. 
   Für manche Funktionen (Insert,Delete) gibt es vielleicht 
   schon Icons aus der ExtJS.

#. Abfragen mit komplexen Bedingungen zur Suche nach Personen

#. Die Zeilenhöhe einer Grid muss einen sinnvollen Maximalwert kriegen. 
   In Explorer / Notes hat man momentan den Eindruck, dass es nur eine 
   Zeile gibt; in Wirklichkeit ist der Memo-Text der ersten Zeile so lang, 
   dass die Zeilenhöhe größer als das Fenster ist.

#. Benutzbarkeit per Tastatur verbessern (issue 11, issue 64) 

#. Sehen können, nach welcher Kolonne eine Grid sortiert ist.

#. Prüfen, ob die neuen ExtJS-Features für Lino interessant sind:

  - `Forms with vbox Layout <http://dev.sencha.com/deploy/dev/examples/form/vbox-form.html>`_ 
  - `Composite Form Fields <http://dev.sencha.com/deploy/dev/examples/form/composite-field.html>`_ 

#. Filter auf virtuelle Kolonnen setzen können. Siehe :doc:`/blog/2010/0811`.

#. In Kolonne Sprachkenntnisse kann man noch keinen Filter setzen. 
   Wenn man es tut, kommt auf dem Server ein 
   `FieldDoesNotExist: Person has no field named u'LanguageKnowledgesByPerson'`.
   Schnelle Lösung ist, dass ich hier einen einfach Textfilter mache.
   Aber um das richtig zu lösen, müsste das Filters-Menü für diese Kolonne 
   nicht nur ein einfaches Textfeld haben, sondern für jede Kolonne 
   des Ziel-Reports ein Suchfeld. Damit man z.B. nach allen Personen suchen kann, 
   die eine Sprache "mündlich mindestens gut und schriftlich mindestens ausreichend" kennen
  
#.  Layout von Detail-Fenstern : in Lino sind die "Zeilen" momentan ja immer 
    im "Blocksatz" (also links- und rechtsbündig). Das ist unkonventionell: 
    alle RIA die ich kenne, machen ihre Formulare nur linksbündig.

#.  HtmlEditor oder TextArea? Der HtmlEditor verursacht deutliche 
    Performanceeinbußen beim Bildschirmaufbau von Detail-Fenstern. 
    Die Wahl sollte konfigurierbar sein. Markup auch.

#.  Das Detail-Fenster sollte vielleicht par défaut nicht im Editier-Modus 
    sein, sondern unten ein Button "Edit", und erst wenn man darauf klickt, 
    werden alle Felder editierbar (und der Record in der Datenbank blockiert), 
    und unten stehen dann zwei Buttons "Save" und "Cancel". Wobei darauf zu 
    achten ist was passiert, wenn man während des Bearbeitens in der Grid 
    auf eine andere Zeile klickt. Dann muss er am besten das Detail-Fenster 
    speichern, und falls dort ungültige Daten stehen, in der Grid den 
    Zeilenwechsel verweigern.

#. `Report.date_format` muss in der Syntax des UI (d.h. ExtJS) angegeben werden. 

#. Prüfen, ob Dokumentvorlagen im `XSL-FO-Format <http://de.wikipedia.org/wiki/XSL-FO>`__ besser wären. `Apache FOP <http://xmlgraphics.apache.org/fop/>`__ als Formatierer. Warum OpenOffice.org nicht schon lange XSL-FO kann, ist mir ein Rätsel. AbiWord dagegen soll es können (laut `1 <http://www.ibm.com/developerworks/xml/library/x-xslfo/>`__ und `2 <http://searjeant.blogspot.com/2008/09/generating-pdf-from-xml-with-xsl-fo.html>`__).

#. Inwiefern überschneiden sich :mod:`lino.modlib.system.models.SiteConfig` und :mod:`django.contrib.sites`? 

#. Benutzerverwaltung von der Kommandozeile aus. 
   In Lino-DSBE gibt es :xfile:`make_staff.py`, aber das ist nur ein sehr primitives Skript.
  
#. Im Fenster :menuselection:`System --> Site Configuration` müssten Delete und Insert noch weg. 

#. http://code.google.com/p/extjs-public/
   und
   http://www.sencha.com/blog/2009/06/10/building-a-rating-widget-with-ext-core-30-final-and-google-cdn/
   lesen.  
  
#. Feldgruppen. Z.B. bei den 3 Feldern für Arbeitserlaubnis (:attr:`dsbe.models.Person.work_permit`) in DSBE wäre es interessant, 
   dass das Label "Arbeitserlaubnis" einmal über der Gruppe steht und in den Labels der einzelnen Felder nicht wiederholt wird.

  
#. Layout-Editor: 

  #. Schade, dass das Editorfenster das darunterliegende Fenster verdeckt 
     und auch nicht aus dem Browserfenster rausbewegt werden kann. 
     Mögliche Lösungen: 
    
     #. Fenster allgemein wieder mit maximizable=true machen
     #. dass das Editorfenster sich die east region pflanzt. 
    
  #. Button um Feldnamen komfortabel auszuwählen


#. Ich würde in der Rückfrage zum Löschen eine oder mehrerer Records ja auch 
   gerne die `__unicode__` der zu löschenden Records anzeigen.
   FormPanel und GridPanel.get_selected() geben deshalb jetzt nicht mehr bloß eine Liste der IDs, sondern eine Liste der Records.
   Aber das nützt (noch) nichts, denn ich weiß nicht, wie ich den Grid-Store überredet bekomme, außer `data` 
   auch eine Eigenschaft `title` aus jedem Record rauszulesen. 
   Auf Serverseite wäre das kein Problem: ich bräuchte einfach nur title in `elem2rec1` statt in `elem2rec_detailed` zu setzen.
   Aber das interessiert den Store der Grid nicht. Kann sein, dass ich ihn konfigurieren kann...
   Oder ich würde es wie mit `disabled_fields` machen. Also ein neues automatisches virtuelles Feld __unicode__.
  
#. Insert-Fenster: Für die Situationen, wo man viele neue Records hintereinander erfasst, könnte
   vielleicht ein zusätzlicher Knopf "Save and insert another" (wie im Django-Admin), 
   oder aber das automatische Schließen des Insert-Fensters im Report abschalten können.

#. Das Folgende macht er noch nicht:
   Falls ein Template in der Sprache der Notiz nicht existiert 
   (z.B. weil die Vorlage noch nicht übersetzt wurde oder multilingual ist), 
   nimmt er die Standard-Vorlage aus der Hauptsprache.
   
#.  `lino.reports.Report.page_length` (Anzahl Records pro Seite) könnte evtl. 
    in die GC mit reinkommen.
   

#. Generic Foreign Keys: 

  #. In einem Detail sind ist owner_type ja schon eine ComboBox, 
     aber der Owner könnte doch eigentlich auch eine sein. 
     Müsste er einen automatischen chooser kriegen.
  #. Wenn ein GFK explizit in Report.column_names angegeben sit, 
     müssten zwei Kolonnen erzeugt werden 
     (statt momentan einer Kolonne, die dann nicht korrekt angezeigt wird)
  
#. When :djangoticket:`7539` is available, we'll modify these automatic 
   `disable_delete` methods so that they act only for 
   ForeignKey fields with `on_delete=RESTRICT`.
   See :doc:`/tickets/2`

#. ReportRequest und/oder ViewReportRequest sind (glaube ich) ein Fall für 
   `Django-Middleware <http://docs.djangoproject.com/en/dev/topics/http/middleware/>`_.
  
  
#. Wenn ich einen Slave-Report sowohl in der Grid als auch in einem Detail als Element benutze, 
   dann verursacht das einen Konflikt im ext_store.Store, weil er zwei virtuelle fields.HtmlBox-Felder 
   mit dem gleichen Namen erzeugt, die sich nur durch den row_separator unterscheiden.
   Lösung wäre, dass :meth:`lino.reports.Report.slave_as_summary_meth` nicht HTML, sondern JSON zurückgibt.
  
#. Für :class:`lino.utils.printable.LatexBuildMethod` müsste mal ohne viel Aufwand 
   ein kleines Beispiel implementiert werden.
  
#. Sollten Links hierarchisiert werden können? 
   Das hieße ein Feld :attr:`links.Link.parent` und ein TreePenel.
  
#. Die HtmlBox braucht noch ein `autoScroll:true` für wenn viele Links da sind.

#. Neues Feld :attr:`links.Link.sequence`, und :class:`links.LinksByOwner` sollte dann danach sortiert sein.
  
#. Problem mit :meth:`contacts.Contact.address`. 
   Wenn ich dieses Feld in :class:`contacts.Persons` benutze, sagt er
   `TypeError: unbound method address() must 
   be called with Company instance as first argument (got Person instance instead)`.
   Da stimmt was mit der Vererbung von virtuellen Feldern nicht.

#. Bei einem POST (Einfügen) werden die base parameters mk und mt zusammen 
   mit allen Datenfeldern im gleichen Namensraum übertragen.
   Deshalb sind Feldnamen wie mt, mk und fmt momentan nicht möglich.

#. Verändern der Reihenfolge per DnD in :class:`links.LinksByOwner`.
    
#. Wir brauchen in :class:`notes.Note` noch eine Methode `type_choices` und 
   in :class:`notes.NoteType` ein Feld `only_for_owner_model`, das die Auswahlliste 
   für Notizart ggf. auf bestimmte Arten von Owner beschränkt.
  
#. Continue to reanimate iGen. See :doc:`/blog/2010/1028`.

#. Mehrsprachige Dokumentvorlagen: um das zu ermöglichen, muss ich 
   wahrscheinlich im doctemplates-Baum zusätzlich zu 'de', 'fr' usw. 
   ein weiteres Verzeichnis `default` verwenden.
  
#. Lässt sich mein System von config-Dateien unter Verwendung von 
   django.templates.loader neu implementieren? Erste Prognose lautet 
   eher negativ, 
   weil der template loader Django immer Template aus der Datei macht und 
   den tatsächlichen Dateinamen nicht preisgibt.

#. :mod:`lino.modlib.ledger` und :mod:`lino.modlib.finan` 
   könnten zusammengeschmolzen werden, 
   denn ich kann mir nicht vorstellen, 
   wie man das eine ohne das andere haben wollen könnte.
  
#. nosetests lesen: http://packages.python.org/nose/usage.html  

#. Django Test-Suite ans Laufen kriegen und Git-Benutzung lernen, 
   um bei Diskussionen um Django-Tickets mitreden zu können.
   (sh. :doc:`/blog/2010/1103`)
  
#. Use event managers as suggested by Jonathan Julian (Tip #2 in  http://www.slideshare.net/jonathanjulian/five-tips-to-improve-your-ext-js-application). 
   Maybe for each report::
  
     Lino.contacts.Persons.eventManager = new Ext.util.EventManager();
     Lino.contacts.Persons.eventManager.addEvents('changed');
    
   Lino could use this to have an automatic refresh of each window that displays data. Maybe rather only one central event manager because if any data gets changed, basically all open windows may need a refresh.

#. lino.modlib.dsbe und lino.modlib.igen sind ja eigentlich keine 
   normalen "Django applications", sondern Endmodule für Lino... das ist noch unklar.
  
#. :doc:`/tickets/16`

#. Mehr über Nuxeo lesen: http://doc.nuxeo.org/5.3/books/nuxeo-book/html/index.html

#. Use :meth:`Action.run` in general, not only for RowAction. 
   See :doc:`/blog/2010/1124`
  
#. Check whether the approach at http://djangosnippets.org/snippets/14/ 
   is easier than south
  
#. Wenn man im Detail speichert, wird anschließend immer ein Refresh gemacht. 
   Das ist bisher nur bei dsbe.Contract nötig, und statt ein Refresh anzufordern, 
   könnte er auch gleich den aktualisierten Record zurückgeben...
   Da ist also Spielraum zum Optimieren.
  
#. Warnung, wenn das gleiche Feld mehrmals in einem Detail vorkommt.
   Oder besser: diesen Fall zulassen.
   
#.  http://code.google.com/p/extjs-public/   

#.  Soll :mod:`<make_staff> lino.management.commands.make_staff` 
    (auch) über das Web-Interface zur Verfügung stehen?
    Aber ich denke der Befehl muss bleiben, denn jemand der nicht staff ist, 
    darf sich par définition nicht selber in diesen Status versetzen können.

#.  Wenn man z.B. watch_tim oder initdb_tim manuell startet und der 
    ein log-rotate durchführt, dann haben die neu erstellten Dateien 
    anschließend nicht www-data als owner. Resultat: internal server error!

#.  `How to LSBize an Init Script <http://wiki.debian.org/LSBInitScripts>`_

#.  http://de.wikipedia.org/wiki/Xming

#.  Chrome 10 hat scheinbar ein Problem mit ExtJS:
    http://www.google.com/support/forum/p/Chrome/thread?tid=5d3cce9457a1ebb1&hl=en    
    
#.  :doc:`/tickets/25`

#.  :doc:`/tickets/26`

#.  Was ist aus meinem Ticket
    :djangoticket:`BooleanField should work for ExtJS Checkboxes <15497>`
    geworden?
    Falls die das wirklich tun sollten, kann meine 
    :meth:`lino.ui.extjs.ext_store.BooleanStoreField.parse_form_value` 
    komplett raus.
    
#.  Man kann es momentan nicht verhindern, dass ein Babel-Feld expandiert wird.
    
#.  Think about differences and common things between 
    Lino's Report and Django's new 
    `Class-based views
    <http://docs.djangoproject.com/en/dev/topics/class-based-views/>`_ 
    (Discovered :doc:`/blog/2011/0311`)

#.  Check whether Lino should use
    http://django-rest-framework.org/
    instead of reinventing the wheel.
    (Discovered :doc:`/blog/2011/0311`)
    
#.  Demo fixtures should detect whether the database backend supports 
    utf8 encoding or not. If it doesn't, they could skip data 
    like Татьяна Казеннова that would cause trouble. 
    See :doc:`/blog/2011/0527`.
    Alternative: make such data optional in a separate fixture.
    
#.  Wenn ich ein Model importiere, das gar nicht installiert ist
    (also dessen "application" nicht in INSTALLED_APPS drin ist). 
    In diesem Fall wird keine Tabelle in der Datenbank erstellt.
    Aber wie kann ich das testen?
    Lino sollte für solche Modelle keinen Report machen.
    


Documentation
-------------

#.  Anpassungen :doc:`/admin/install` an Debian Squeeze.
    OpenOffice bzw. LibreOffice braucht jetzt wahrscheinlich 
    nicht mehr manuell installiert zu werden.

#.  Wenn ich in der INSTALLED_APPS von lino.demos.std.settings 
    auch die igen-Module reintue, dann kriege ich::
  
     ref\python\lino.modlib.dsbe.rst:17: (WARNING/2) autodoc can't import/find module 'lino.apps.dsbe.models', 
     it reported error: "resolve_model('contacts.Company',app_label='contacts',who=None) found None"

#.  ``make doctest`` nutzbar machen. Siehe :doc:`/blog/2010/1024`

#.  Check whether 
    `pydocweb <https://github.com/pv/pydocweb/tree/master/docweb>`_    
    would be useful.

#.  I'm trying to document several Django applications on a single Sphinx tree. 
    Django modules have the requirement that an environment variable DJANGO_SETTINGS_MODULE be set when importing them. 
    Maybe one way is to add an `environment` option to the `automodule` directive?

#.  Ausprobieren, was David De Sousa am 12.11.2009 auf sphinx-dev gepostet hat.