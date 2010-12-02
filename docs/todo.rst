To-do list
==========

This document is partly in German because it is rather for internal use. 
See also :doc:`/tickets/index` which is a list of tickets 
for which I hope for help from other people.


Before version 1.0
------------------

#. Feld `Person.user` wird noch nicht importiert. 
   Dazu muss LOCAL_TIM2LINO umfunktioniert werden in eine TIM2LINO_USERNAME o.ä.

#. Stundensatz: wo speichern? Manueller Wert möglich?
   Noch ein neues separates Feld für Rückerstattung?

#. Arbeitsregime und Stundenplan sind bisher nur in Deutsch.

#. WebDAV installieren und testen, wie das Bearbeiten von ODT-Dokumenten in der Praxis läuft.

#. Dokumentvorlagen weiter

#. Doppelklick in einer Grid sollte das Detail-Fenster öffnen. 

#. Mit :kbd:`[F2]` sollte die Zeile einer Grid bearbeiten können.

#. Button "Insert" : wenn man das Insert-Fenster bestätigt und keine Fehlermeldung kommt, 
   wird das Fenster geschlossen. Aber wenn man das von der Grid aus tut, 
   wird auch die Grid geschlossen.

#. "Insert as copy"

#. `watch_tim` automatisch nach reboot starten.
   Irgendwie müssen ungefähr die folgenden Befehle in der :file:`/etc/init.d` 
   gerufen werden::
  
     /usr/local/django/myproject/watch_tim

   Siehe auch:
  
    | http://www.debian-administration.org/articles/28
    | http://girasoli.org/?p=120
    | `How to LSBize an Init Script <http://wiki.debian.org/LSBInitScripts>`_
  
   Das Loggen von watch_tim geht scheinbar noch nicht so richtig.  

Waiting for feedback
--------------------

#. Vorschlag: im Tab "Profile 2" die Felder "auch Schichtarbeit" und "auch am WE" 
   ersetzen durch ihr Gegenteil ("keine Schichtarbeit" und "nicht am WE"), damit alle 
   Checkboxen in der oberen Hälfe Hindernisse sind.

#. Externe Links (Lesezeichen) notieren können, indem man sie von einem anderen Browserfenster 
   per drag & drop auf die HtmlBox zieht.   
   :doc:`/tickets/8` 

#. How to import, render & edit BIC:IBAN account numbers?

#. The main window also needs a `Refresh` button. 
   Or better: should be automatically refreshed when it was hidden by another 
   window and becomes visible again.
  
#. MyUploads müsste eigentlich nach `modified` sortiert sein. Ist er aber nicht.
   Idem für MyContracts. 

#. wenn man in einem Vertrag eine Angabe ändert und dann "Drucken" klickt, dann wird die 
   Änderung irritierenderweise nicht gespeichert.
  
#. Im Kontextmenü sollten auch Aktionen erscheinen, die spezifisch 
   für das Feld (die Kolonne) sind. 
  
#. Im Hauptmenü könnten zwei Befehle :menuselection:`Help --> User Manual` 
   und :menuselection:`Help --> About` kommen, dann hätten wir den ganzen 
   Platz für Erinnerungen.

#. Wenn man z.B. in Companies.insert manuell eine ID eingibt, 
   dann ignoriert der Server die und vergibt trotzdem seine automatische nächste ID.

After version 1.0
-----------------

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
   (which is the default and which cannot be changed).
   Maybe add a button to switch between the two selection models?
   Caution: delete_selected currently probably works only with a CellSelectionModel.

#. Make it configurable (site-wide, per user,...)
   whether external links should open a new window or not.

#. do we need a general button "Printer-friendly view"?

#. Formatierung der :xfile:`welcome.html` lässt zu wünschen übrig.  

#. Wenn man die Konsole aufklappt, könnten dort die letzten par Meldungen angezeigt werden...

#. Wie kann ich die Test-Templates für Notizen in den code repository rein kriegen?
   Er soll sie dann auch unabhängig von der Sprache finden. 
   Vielleicht werde ich doctemplates in die config-directories verschieben 
   und mein System von config-Dateien erweitern, dass es auch Unterverzeichnisse verträgt.
   Siehe :doc:`/blog/2010/1029`, :doc:`/blog/2010/1112`.
  
#. Hauptmenü nicht anzeigen, wenn ein Fenster offen ist. 
   Stattdessen ein bequemer Button, um ein weiteres Browserfenster mit Lino zu öffnen.
   Weil die Benutzer sonst irgendwann einen Stack overflow kriegen, 
   weil sie sich nicht dessen bewusst sind, 
   dass ihre Fenster offen bleiben.
   (Das hätte möglicherweise später als Folge, dass das Hauptmenü gar kein Pulldown-Menü mehr zu sein braucht, 
   sondern eine für Webseiten klassischere Ansicht benutzen.)
  
#. Man kann z.B. noch nicht nach Personen suchen, die ein bestimmtes Studium haben.

#. Einheitliches Interface um Reihenfolge zu verändern (Journals, DocItems, LinksByOwner,...). Erster Schritt: Abstract model "Ordered" mit einem Feld `pos` und zwei Actions "move up" und "move down".

#. Eingabe im Detail eines SalesDocument funktioniert noch nicht: 
   Wenn man ein 
   Produkt auswählt, antwortet der Server 
   `{'unit_price': ValidationError([u'This value must be a decimal number.'])}` 
   statt den Stückpreis selber auszufüllen.
  
#. Fenstertitel ändern bzw. anzeigen, welche GC momentan aktiv ist.

#. Das Passfoto in dsbe.PersonDetail ist manchmal verzerrt oder noch nicht korrekt ausgeschnitten.

#. Was soll passieren wenn man Contract.company ändert, nachdem Contract.contact schon ausgefüllt ist?
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

#. Die Buttons der tbar sollten mit Icons versehen werden. Für manche Funktionen (Insert,Delete) gibt es vielleicht schon Icons aus der ExtJS.

#. Abfragen mit komplexen Bedingungen zur Suche nach Personen

#. Die Zeilenhöhe einer Grid muss einen sinnvollen Maximalwert kriegen. In Explorer / Notes hat man momentan den Eindruck, dass es nur eine Zeile gibt; in Wirklichkeit ist der Memo-Text der ersten Zeile so lang, dass die Zeilenhöhe größer als das Fenster ist.

#. Hinter das QuickFilter-Feld muss ein Button, um den Filter zu aktivieren. Dass man einfach nur TAB drücken muss ist nicht intuitiv.

#. Benutzbarkeit per Tastatur verbessern (issue 11, issue 64) 

#. Sehen können, nach welcher Kolonne eine Grid sortiert ist.

#. Nach Duplikaten suchen vor Erstellen einer neuen Person (issue 85)

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
  
#. Layout von Detail-Fenstern : in Lino sind die "Zeilen" momentan ja immer im "Blocksatz" (also links- und rechtsbündig). Das ist unkonventionell: alle RIA die ich kenne, machen ihre Formulare nur linksbündig.

#. HtmlEditor oder TextArea? Der HtmlEditor verursacht deutliche Performanceeinbußen beim Bildschirmaufbau von Detail-Fenstern. Die Wahl sollte konfigurierbar sein. Markup auch.

#. Das Detail-Fenster sollte vielleicht par défaut nicht im Editier-Modus sein, sondern unten ein Button "Edit", und erst wenn man darauf klickt, werden alle Felder editierbar (und der Record in der Datenbank blockiert), und unten stehen dann zwei Buttons "Save" und "Cancel". Wobei darauf zu achten ist was passiert, wenn man während des Bearbeitens in der Grid auf eine andere Zeile klickt. Dann muss er am besten das Detail-Fenster speichern, und falls dort ungültige Daten stehen, in der Grid den Zeilenwechsel verweigern.

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

#. Der JS-Code, der ein Detail-Fenster definiert, wird in der :xfile:`site.js` 
   für jeden Report zweimal generiert (detail und insert).
   Ein einziges Mal für alle Reports würde reichen.
  
#. :xfile:`site.js` und :xfile:`lino.js` sollten eigentlich eine einzige Datei sein. 
   Also die :file:`lino.js` muss templatisiert werden (wobei z.B. die dortigen Meldungen 
   auch endlich übersetzbar würden), und am Ende würde das Template dann 
   das Äquivalent von :meth:`lino.ui.extjs.ext_ui.ExtUI.build_site_js` aufrufen.
  
  
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

#. Die Labels der Details werden zwar übersetzt, aber nicht von makemessages gefunden.

#. Das Folgende macht er noch nicht:
   Falls ein Template in der Sprache der Notiz nicht existiert 
   (z.B. weil die Vorlage noch nicht übersetzt wurde oder multilingual ist), 
   nimmt er die Standard-Vorlage aus der Hauptsprache.

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
   See :doc:`/tickets/closed/2`

#. Main-Grids könnten mit `autoHeight=true` arbeiten. Dadurch würde der zweite Ajax-call unnötig.
   autoHeight resizes the height to show all records. 
   `limit` (Anzahl Records pro Seite) müsste dann freilich in die GC mit reinkommen.
  
#. ReportRequest und/oder ViewReportRequest sind (glaube ich) ein Fall für 
   `Django-Middleware <http://docs.djangoproject.com/en/dev/topics/http/middleware/>`_.
  
  
#. Foreign keys 

  #. sollten in der Grid anklickbar sein, 
     so wie die Elemente eines Slave-Reports,
     aber nicht *genau* so, 
     sondern die sollten sich im gleichen Browserfenster öffnen. 
     Außerdem muss natürlich (zumindest in quick_edit-Grids) die Möglichkeit 
     des Bearbeitens erhalten bleiben. 
  #. sollten im Detail-Fenster einen Button neben sich haben, 
     mit dem man per permalink auf die foreign row springen kann.
  
#. Grid configs 

  #. sollten in den config dirs stehen und nicht im DATA_DIR
  #. sollten vielleicht besser YAML statt .py sein.  

#. Wenn ich einen Slave-Report sowohl in der Grid als auch in einem Detail als Element benutze, 
   dann verursacht das einen Konflikt im ext_store.Store, weil er zwei virtuelle fields.HtmlBox-Felder 
   mit dem gleichen Namen erzeugt, die sich nur durch den row_separator unterscheiden.
   Lösung wäre, dass :meth:`lino.reports.Report.slave_as_summary_meth` nicht HTML, sondern JSON zurückgibt.
  
#. Für :class:`lino.utils.printable.LatexBuildMethod` müsste mal ohne viel Aufwand 
   ein kleines Beispiel implementiert werden.
  
#. Benutzermeldungen "wurde gespeichert" & Co bleiben manchmal auch 
   nach der nächsten Aktion noch in der Console stehen.
   Ich muss vielleicht konsequent immer Lino.action_handler benutzen.
  
#. Sollten Links hierarchisiert werden können? 
   Das hieße ein Feld :attr:`links.Link.parent` und ein TreePenel.
  
#. Lino könnte per LDAP-Request verschiedene Angaben 
   in :class:`auth.User` (Name, E-Mail,...) 
   direkt vom LDAP-Server anfragen.
   Dazu wären wahrscheinlich
   http://www.python-ldap.org/
   und
   http://www.openldap.org/
   nötig.

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
    
#. Is there a better implementation for :func:`lino.ui.extjs.ext_ui.elem2rec_detailed`?

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


Documentation
-------------

#. Wenn ich in der INSTALLED_APPS von lino.demos.std.settings auch die igen-Module reintue, dann 
   kriege ich::
  
     ref\python\lino.modlib.dsbe.rst:17: (WARNING/2) autodoc can't import/find module 'lino.modlib.dsbe.models', 
     it reported error: "resolve_model('contacts.Company',app_label='contacts',who=None) found None"

#. ``make doctest`` nutzbar machen. Siehe :doc:`/blog/2010/1024`
