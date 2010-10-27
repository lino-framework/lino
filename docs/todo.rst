To-do list
==========

This document is in German because it is rather for internal use. 
See also :doc:`/tickets/index` which is a list of tickets 
for which I hope for help from other people.


Short-term
----------

- IE sagt beim Öffnen von :menuselection:`Kontakte --> Personen`::

    Message: 'id' is null or not an object
    Line: 11
    Char: 166504
    Code: 0
    URI: http://localhost:8080/media/extjs/ext-all.js


- Im Detail der Personen sind manche Tabs anfangs nicht korrekt gelayoutet. 
  Dann muss man jeweils auf den Pin-Button oben rechts klicken (der die Seite mit Permalink 
  neu öffnet) um das korrekte Layout sehen zu können. 
  Condors Antwort in :doc:`/tickets/closed/1` 
  war leider nur die Lösung für den dort beschriebenen spezifischen Fall.
  Aber er hat mich auf eine Idee gebracht: die vbox-Layouts sind "schuld" am Problem. 
  Deshalb hatte ich ja auch VBorderPanel geschrieben, aber das wird zumindest in "Profil 1" nicht benutzt.

- Externe Links (Lesezeichen) notieren können, indem man sie von einem anderen Browserfenster 
  per drag & drop auf die HtmlBox zieht.   
  :doc:`/tickets/8` 

- WebDAV installieren und testen, wie das Bearbeiten von RTF- und ODT-Dokumenten in der Praxis läuft.

- Dokumentvorlagen machen  

Undecided
---------

- Man kann z.B. noch nicht nach Personen suchen, die ein bestimmtes Studium haben.

- Momentan wird der Synchronisierungs-Prozess (watch_tim) nach einem Server-Restart nicht automatisch neu gestartet. 
  Ich habe nämlich lediglich in `/usr/local/django/myproject` eine Datei namens `watch_tim` mit folgendem Inhalt::

    nohup python manage.py watch_tim \  
      /mnt/server/TIM/CPAS/changelog > \
      /var/log/lino/watch_tim.log
      
  Und diese Datei starte ich manuell nach einem Release. 
  :command:`nohup` sorgt dafür, dass der Prozess nicht beendet wird, wenn ich mich auslogge. 
  Aber stattdessen muss natürlich ein Skript in der :file:`/etc/init.d` gemacht werden.


- iCal-Dateien generieren. 
  Im :class:`notes.NoteType` wird definiert, ob Lino einen Termin (oder Erinnerung oder Task) 
  per E-Mail an den Benutzer verschicken soll.

- :doc:`/tickets/2`. Also Vorsicht beim Löschen von Notizarten, Studienarten, 
  AG-Sperrgründen, Begleitungsarten, Städten, Ländern usw.!

- Wenn man z.B. in Companies.insert manuell eine ID eingibt, 
  dann ignoriert der Server die und vergibt trotzdem seine automatische nächste ID.

Long-term
---------

- Wie soll ich es machen, dass der Benutzer beim Auswählen der Krankenkasse einer Person nicht alle Firmen, sondern nur die Krankenkassen angezeigt bekommt? Etwa ein eigenes Feld `Company.is_health_insurance`?

- Fenstertitel ändern bzw. anzeigen, welche GC momentan aktiv ist.

- Das Passfoto in dsbe.PersonDetail ist manchmal verzerrt oder noch nicht korrekt ausgeschnitten.

- Die Buttons der tbar sollten mit Icons versehen werden. Für manche Funktionen (Insert,Delete) gibt es vielleicht schon Icons aus der ExtJS.

- Abfragen mit komplexen Bedingungen zur Suche nach Personen

- Die Zeilenhöhe einer Grid muss einen sinnvollen Maximalwert kriegen. In Explorer / Notes hat man momentan den Eindruck, dass es nur eine Zeile gibt; in Wirklichkeit ist der Memo-Text der ersten Zeile so lang, dass die Zeilenhöhe größer als das Fenster ist.

- Hinter das QuickFilter-Feld muss ein Button, um den Filter zu aktivieren. Dass man einfach nur TAB drücken muss ist nicht intuitiv.

- Links ordentlich anzeigen und bequem erfassen können.

- Benutzbarkeit per Tastatur verbessern (issue 11, issue 64) 

- Sehen können, nach welcher Kolonne eine Grid sortiert ist.

- Nach Duplikaten suchen vor Erstellen einer neuen Person (issue 85)

- URLs per drag & drop registrieren können

- `lino.test_apps.journals` funktioniert nicht bzw. wird nicht ausgeführt. Sieht aus als Django-Ticket 11696 doch noch nicht behoben ist. Aber mein Patch 20091107.diff funktioniert nicht mehr und ich bin auch noch nicht sicher. Muss vielleicht mal einen Testcase schreiben, um das Problem zu identifizieren...

- Prüfen, ob die neuen ExtJS-Features `Forms with vbox Layout <http://dev.sencha.com/deploy/dev/examples/form/vbox-form.html>`_ und
  `Composite Form Fields <http://dev.sencha.com/deploy/dev/examples/form/composite-field.html>`_ für Lino interessant sind.


- Filter auf virtuelle Kolonnen setzen können. Siehe :doc:`/blog/2010/0811`.

- In Kolonne Sprachkenntnisse kann man noch keinen Filter setzen. 
  Wenn man es tut, kommt auf dem Server ein 
  `FieldDoesNotExist: Person has no field named u'LanguageKnowledgesByPerson'`.
  Schnelle Lösung ist, dass ich hier einen einfach Textfilter mache.
  Aber um das richtig zu lösen, müsste das Filters-Menü für diese Kolonne 
  nicht nur ein einfaches Textfeld haben, sondern für jede Kolonne 
  des Ziel-Reports ein Suchfeld. Damit man z.B. nach allen Personen suchen kann, 
  die eine Sprache "mündlich mindestens gut und schriftlich mindestens ausreichend" kennen
  
- Projekte einführen? Pro Person müsste man per Klick leicht ein Begleitungsprojekt anlegen können. Bei Import und Synchronisierung würden automatisch auch diese Projekte synchron gehalten. Dienstleistungen sind nicht mehr einer Person und/oder einer Firma, sondern allgemein einem Projekt zugewiesen. 

- Layout von Detail-Fenstern : in Lino sind die "Zeilen" momentan ja immer im "Blocksatz" (also links- und rechtsbündig). Das ist unkonventionell: alle RIA die ich kenne, machen ihre Formulare nur linksbündig.

- HtmlEditor oder TextArea? Der HtmlEditor verursacht deutliche Performanceeinbußen beim Bildschirmaufbau von Detail-Fenstern. Die Wahl sollte konfigurierbar sein. Markup auch.

- "About"-Fenster mit `thanks_to()` muss irgendwo sichtbar gemacht werden.

- lino.test_apps.properties funktioniert nicht, scheinbar ist `actors.discover()` nicht aufgerufen worden.

- Das Detail-Fenster sollte vielleicht par défaut nicht im Editier-Modus sein, sondern unten ein Button "Edit", und erst wenn man darauf klickt, werden alle Felder editierbar (und der Record in der Datenbank blockiert), und unten stehen dann zwei Buttons "Save" und "Cancel". Wobei darauf zu achten ist was passiert, wenn man während des Bearbeitens in der Grid auf eine andere Zeile klickt. Dann muss er am besten das Detail-Fenster speichern, und falls dort ungültige Daten stehen, in der Grid den Zeilenwechsel verweigern.

- `Report.date_format` muss in der Syntax des UI (d.h. ExtJS) angegeben werden. 

- Prüfen, ob Dokumentvorlagen im `XSL-FO-Format <http://de.wikipedia.org/wiki/XSL-FO>`__ besser wären. `Apache FOP <http://xmlgraphics.apache.org/fop/>`__ als Formatierer. Warum OpenOffice.org nicht schon lange XSL-FO kann, ist mir ein Rätsel. AbiWord dagegen soll es können (laut `1 <http://www.ibm.com/developerworks/xml/library/x-xslfo/>`__ und `2 <http://searjeant.blogspot.com/2008/09/generating-pdf-from-xml-with-xsl-fo.html>`__).

- Inwiefern überschneiden sich :mod:`lino.modlib.system.models.SiteConfig` und :mod:`django.contrib.sites`? 

- Benutzerverwaltung von der Kommandozeile aus. 
  In Lino-DSBE gibt es :xfile:`make_staff.py`, aber das ist nur ein sehr primitives Skript.
  
- Im Fenster :menuselection:`System --> Site Configuration` müssten Delete und Insert noch weg. 

- http://code.google.com/p/extjs-public/
  und
  http://www.sencha.com/blog/2009/06/10/building-a-rating-widget-with-ext-core-30-final-and-google-cdn/
  lesen.  
  
- Feldgruppen. Z.B. bei den 3 Feldern für Arbeitserlaubnis (:attr:`dsbe.models.Person.work_permit`) in DSBE wäre es interessant, 
  dass das Label "Arbeitserlaubnis" einmal über der Gruppe steht und in den Labels der einzelnen Felder nicht wiederholt wird.

- Comboboxen auf Integerfeldern funktionieren nicht. Zeigen NaN als Text an.

- Der JS-Code, der ein Detail-Fenster definiert, wird in der :xfile:`site.js` 
  für jeden Report zweimal generiert (detail und insert).
  Ein einziges Mal für alle Reports würde reichen.
  
- :xfile:`site.js` und :xfile:`lino.js` sollten eigentlich eine einzige Datei sein. 
  Also die :file:`lino.js` muss templatisiert werden (wobei z.B. die dortigen Meldungen 
  auch endlich übersetzbar würden), und am Ende würde das Template dann 
  das Äquivalent von :meth:`lino.ui.extjs.ext_ui.ExtUI.build_site_js` aufrufen.
  
  
- Layout-Editor: 

  - Schade, dass das Editorfenster das darunterliegende Fenster verdeckt 
    und auch nicht aus dem Browserfenster rausbewegt werden kann. 
    Mögliche Lösungen: 
    
    - Fenster allgemein wieder mit maximizable=true machen
    - dass das Editorfenster sich die east region pflanzt. 
    
  - Button um Feldnamen komfortabel auszuwählen


- Ich würde in der Rückfrage zum Löschen eine oder mehrerer Records ja auch 
  gerne die `__unicode__` der zu löschenden Records anzeigen.
  FormPanel und GridPanel.get_selected() geben deshalb jetzt nicht mehr bloß eine Liste der IDs, sondern eine Liste der Records.
  Aber das nützt (noch) nichts, denn ich weiß nicht, wie ich den Grid-Store überredet bekomme, außer `data` 
  auch eine Eigenschaft `title` aus jedem Record rauszulesen. 
  Auf Serverseite wäre das kein Problem: ich bräuchte einfach nur title in `elem2rec1` statt in `elem2rec_detailed` zu setzen.
  Aber das interessiert den Store der Grid nicht. Kann sein, dass ich ihn konfigurieren kann...
  Oder ich würde es wie mit `disabled_fields` machen. Also ein neues automatisches virtuelles Feld __unicode__.
  
- Insert-Fenster: Für die Situationen, wo man viele neue Records hintereinander erfasst, könnte
    vielleicht ein zusätzlicher Knopf "Save and insert another" (wie im Django-Admin), 
    oder aber das automatische Schließen des Insert-Fensters im Report abschalten können.

- Die Labels der Details werden zwar übersetzt, aber nicht von makemessages gefunden.

- Das Folgende macht er noch nicht:
  Falls ein Template in der Sprache der Notiz nicht existiert 
  (z.B. weil die Vorlage noch nicht übersetzt wurde oder multilingual ist), 
  nimmt er die Standard-Vorlage aus der Hauptsprache.

- :doc:`/tickets/taken/6`.

- Generic Foreign Keys: 

  - In einem Detail sind ist owner_type ja schon eine ComboBox, 
    aber der Owner könnte doch eigentlich auch eine sein. 
    Müsste er einen automatischen chooser kriegen.
  - Wenn ein GFK explizit in Report.column_names angegeben sit, 
    müssten zwei Kolonnen erzeugt werden 
    (statt momentan einer Kolonne, die dann nicht korrekt angezeigt wird)
  
- Google-Projekte lino-apps, lino-igen und Lino-DSBE löschen.

- Main-Grids könnten mit `autoHeight=true` arbeiten. Dadurch würde der zweite Ajax-call unnötig.
  autoHeight resizes the height to show all records. 
  `limit` (Anzahl Records pro Seite) müsste dann freilich in die GC mit reinkommen.
  
- ReportRequest und/oder ViewReportRequest sind (glaube ich) ein Fall für 
  `Django-Middleware <http://docs.djangoproject.com/en/dev/topics/http/middleware/>`_.
  
  
- Foreign keys 

  - sollten in der Grid anklickbar sein, 
    so wie die Elemente eines Slave-Reports,
    aber nicht *genau* so, 
    sondern die sollten sich im gleichen Browserfenster öffnen. 
    Außerdem muss natürlich (zumindest in quick_edit-Grids) die Möglichkeit 
    des Bearbeitens erhalten bleiben. 
  - sollten im Detail-Fenster einen Button neben sich haben, 
    mit dem man per permalink auf die foreign row springen kann.
  
- Grid configs 

  - sollten in den config dirs stehen und nicht im DATA_DIR
  - sollten vielleicht besser YAML statt .py sein.  

- Wenn ich einen Slave-Report sowohl in der Grid als auch in einem Detail als Element benutze, 
  dann verursacht das einen Konflikt im ext_store.Store, weil er zwei virtuelle fields.HtmlBox-Felder 
  mit dem gleichen Namen erzeugt, die sich nur durch den row_separator unterscheiden.
  Lösung wäre, dass :meth:`lino.reports.Report.slave_as_summary_meth` nicht HTML, sondern JSON zurückgibt.
  
- LatexPrintMethod. Da müsste ja ohne Aufwand 
  mal ein kleines Beispiel implementiert werden können.  
  
- Benutzermeldungen "wurde gespeichert" & Co bleiben manchmal auch 
  nach der nächsten Aktion noch in der Console stehen.
  Ich muss vielleicht konsequent immer Lino.action_handler benutzen.
  
- Zu prüfen: Wenn ich auf einem production server auf "Drucken" klicke 
  und auf dem Server noch kein Verzeichnis 
  für diese Druckmethode konfiguriert ist, kriegt man keine Fehlermeldung. 
  
- Sollten Links hierarchisiert werden können? 
  Das hieße ein Feld :attr:`links.Link.parent` und ein TreePenel.
  
- Lino könnte per LDAP-Request verschiedene Angaben 
  in :class:`auth.User` (Name, E-Mail,...) 
  direkt vom LDAP-Server anfragen.
  Dazu wären wahrscheinlich
  http://www.python-ldap.org/
  und
  http://www.openldap.org/
  nötig.

- Die HtmlBox braucht noch ein `autoScroll:true` für wenn viele Links da sind.

- Neues Feld :attr:`links.Link.sequence`, und :class:`links.LinksByOwner` sollte dann danach sortiert sein.
  
- Problem mit :meth:`contacts.Contact.address`. 
  Wenn ich dieses Feld in :class:`contacts.Persons` benutze, sagt er
  `TypeError: unbound method address() must 
  be called with Company instance as first argument (got Person instance instead)`.
  Da stimmt was mit der Vererbung von virtuellen Feldern nicht.

  Bei einem POST (Einfügen) werden die base parameters mk und mt zusammen 
  mit allen Datenfeldern im gleichen Namensraum übertragen.
  Deshalb sind Feldnamen wie mt, mk und fmt momentan nicht möglich.

- Verändern der Reihenfolge per DnD in :class:`links.LinksByOwner`.
    
- :doc:`/tickets/10` 


Documentation
-------------

- Wenn ich in der INSTALLED_APPS von lino.demos.std.settings auch die igen-Module reintue, dann 
  kriege ich::
  
    ref\python\lino.modlib.dsbe.rst:17: (WARNING/2) autodoc can't import/find module 'lino.modlib.dsbe.models', 
    it reported error: "resolve_model('contacts.Company',app_label='contacts',who=None) found None"

- ``make doctest`` nutzbar machen. Siehe :doc:`/blog/2010/1024`
