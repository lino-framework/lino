To-do list
==========


Bis 20130902
------------

#.  In Demo-Daten einen mit Angaben in eID-Feldern. 
    Falls nötig Übersetzungen von lino_welfare nach lino rüber holen.
    fab mm in beiden Projekten. Test case(s) schreiben.
    
#.  Wenn man in "Meine Aufgaben" manuell eine Aufgabe erstellt, dann 
    wird diese anschließend nicht auf der Startseite angezeigt. 
    Zustand ist "Begonnen" statt "Zu tun".

#.  Warnung wenn eID-Karte abgelaufen ist.
  
#.  Passfoto einlesen
  
#.  Aktionen "eID einlesen" und "Create visit" aus "Arbeitsablauf" raus.
  
#.  CreateNote (Issue attestation) nicht als HtmlBox im Detail-Fenster, 
    sondern "wie in TIM" als Button mit Auswahlliste statt Dialogfenster.
    
#.  Tabelle CoachingsByClients komplett übernehmen, mit pro Zeile zwei 
    Aktionen "Visite"  und "Termin". Aber dann müssen diese beiden Aktionen 
    auch auf der Phantomzeile stehen...
    
#.  In :ref:`welfare.cal.MyEvents`: Visiten rausfiltern
  
#.  "Bescheinigung erstellen" für pdf-Bescheinigungen ohne Parameter 
    sollte sofort kommen.
    
#.  Übersetzungen
  

Nach 20130909
-------------

#.  Familienbeziehungen
  
#.  HelpText erweitern : auch `verbose_name` der Felder, sowie der 
    Modelle lokal konfigurierbar machen.
    
#.  Views (GridConfigs) konfigurierbar pro User in der Datenbank (d.h. 
    verwaltbar via Web und automatisch migrierbar)
  
#.  Was ist mit Dublettenkontrolle beim Erstellen eines Klienten?
  
#.  Empfang: Kann ein Klient auf zwei Agenten zugleich warten? 
    Soll Lino das verhindern? 
    
#.  Eigene Tabelle für einfache Bescheinigungen 
    (statt SiteConfig.attestation_note_nature und NoteType.is_attestation)

#.  AMK-Bescheinigungen, Einkommensbescheinigungen
    
#.  Volatile Variablen z.B. für "Ausländerbeihilfe":
    "seit dem", "bis zum", "Datum der Bescheinigung"
    Also lokal konfigurierbare Parameterfenster pro Bescheinigung.
    Äquivalent zu den .dlg-Dateien in TIM
  
#.  Uploads should be ProjectRelated. Uploads controlled by a notes.Note 
    should be visible in UploadsByProject
    Uploads pro Notiz sollten auch vom Klienten aus sichtbar sein.



Bugs
----

#. Sometimes, when dialog has many tabs, when I switch to another tab I see 
   numerical indexes in comboboxes - not the textual values. After hitting 
   refresh, everything is OK. This happens every time.
   
#.  Ein Bug, der auch schon in der 1.4.8 war: wenn man das Detail eines Uploads, 
    der keine Reminder hat, via Permalink öffnet, dann ist die Tabelle der 
    Aufgaben nicht leer, sondern voll irgendwelcher Einträge.
    
    Oder das gleiche Problem an anderer Stelle:     
    VSEs eines Klienten im eigenen Fenster öffnen. 
    Doppelklick in Phantomzeile, um neuen VSE ze erstellen.
    VSE-Art auswählen und Fenster bestätigen.  
    --> der neue VSE hat dann scheinbar eine ganze Reihe von Terminen.
    Erst bei Klick auf den Refresh-Button wird die Tabelle leer.



Feature requests
----------------

#.  convert all App.verbose_name to their translations on startup?
    store the App class object in `Site.modules`. 


#.  Have plain renderer use the new attribute 
    :attr:`lino.core.actors.Actor.get_row_class`, 
    deprecate apply_cell_format and convert existing application code.


#.  Convert Presto to use overridden apps.

#.  Momentan kann man leider keine Regel einbauen, dass Systemverwalter 
    nach jeweiliger Bestätigung auch importierte Partner löschen und 
    bearbeiten können. This would require to extend the actions API.

#.  render `models.NullBooleanField` using a `tri-state checkbox
    <http://www.sencha.com/forum/showthread.php?98241-Tri-state-checkbox-for-ExtJs-3.0>`_
    (workaround, with maybe even more intuitive usage is to use a 
    `lino.core.choicelists.YesNo.field` with bnlank=True.
    
#.  Negative Zahlen in Rot formatieren können 
    (z.B. Gesamtsumme Zusammenfassung Budget)

#. Speicherbare Tabellenansichten :
    - pro Benutzer
    - Button "Restore factory defaults" ("Standard-Ansicht
      wiederherstellen" bzw. "Anpassungen löschen")
    - Auch die Option "auto_fit_column_widths" speichern

#.  (Nicht so sicher:) 
    Neben dem momentanen csv-Export eine neue Möglichkeit, lokale 
    Exportfilter zu definieren, die dann in ein für den Benutzer 
    nicht änderbares "stabiles" Format exportieren.
    Eine allgemeine Tabellen-Export-API. 
    Am elegantesten ist das wahrscheinlich mittels Jinja-Templates.

#.  Lino has currently no possibility to specify a default 
    `preferred_width` for a field. 
    modlib.accounts.models.Group : the `ref` field has a max_length of 50, 
    but most people use only up to 6 positions. 
    And I'd prefer to not add ":6" to every layout template.
    

#.  lino.ui.boy :
    - rename "plain" to "boy" (?)
    - cell_html() and "as_plain_html"?
    - detail of a pcsw.client doesn't work because as_plain_html doesn't 
    pass the `ar` to `value_from_object`.

#.  implement the fields Client.applies_from and applies_until as 
    "summary fields". This is a new concept: :doc:`/topics/summary_fields`

#.  Inform about active column filters when building the title of table
    (using title tags).

#.  Is it really necessary that Voucher is a non-abstract class?

#.  Wenn man den Begleitungszeitraum einer *Person* ändert, dann merkt Lino nicht,
    falls durch diese Änderung ein Vertrag ungültig wird.

#.  Übersetzung für "Scheduled" ist momentan "Geplant". 
    Sollte besser "Festgelegt" o.ä. sein.
    Und statt "vorgeschlagen" sollte Lino vielleicht besser "vorgemerkt" sagen.

#.  Ein festgelegter Termin darf nicht verschoben werden können. 
    Auch nicht im Kalender-Panel.

#.  Wie soll es funktionieren, wenn ein einmal festgelegter und offiziel 
    mitgeteilter Termin dann doch verschoben werden muss?
    Momentan kann man den Terminzustand auf "Verlegt" setzen und dann auf 
    "per Mail" klicken, und in der Mail steht dann schon ein entsprechender Satz.

#.  Brauchen wir die Notion von "Teams"? Oder besser Partnerlisten?
    Momentan ist die Konfigurierung etwas skurril: 
    jeder Benutzer stellt sich "sein Team" zusammen.
    Pro Kalender sollte neben `invite_team_members` auch stehen, 
    welches das Team ist.
    
#.  Und in einem könnten wir auch eine Option `auto_subscribe` 
    in Calendar machen: solche Kalender brauchen gar nicht erst 
    explizit abonniert zu werden.
    
#.  Einladung sollte ein ical haben, damit der Empfänger es in seinen
    Calendar-client importieren kann

#.  Man sieht im Kalender-Panel noch nicht, wenn man nur Gast ist und
    noch zusagen bzw. absagen muss.

#.  extensible-lang-fr.js translates "Calendar" to "Agenda". 
    Disturbing.

#.  Wenn man auf einem Auswertungstermin (der automatisch generiert wurde 
    durch eine VSE oder VBE), auf "Duplizieren" klickt, dann dupliziert Lino 
    ihn zwar intern, löscht ihn aber anschließend gleich wieder, weil die 
    VSE die komplette Serie neu generiert. Zu analysieren, wann so eine 
    Aktion da überhaupt Sinn macht. 

#.  Die Kolonne "Workflows" wird beim Ausdruck nicht korrekt gerendert. 
    Weil das Feld :meth:`action_buttons <lino.core.actors.Actor.action_buttons>` 
    noch nicht xmlgen.html verwendet.
    Hat beim Ausdruck sowieso keinen Sinn und sollte automatisch 
    versteckt werden.
    Workaround: En attendant müssen die Benutzer wissen, dass sie 
    diese Kolonne vor dem Ausdruck selber ausblenden müssen.

#.  Optisch kennzeichnen, wenn ein Kolonnentitel einen Hilfetext hat.

#.  Versteckte Reiter werden nicht aktualisiert. 
    Das ist irritierend beim Arbeiten mit Budgets. 
    Z.B. im Reiter Vorschau muss man generell immer noch Refresh klicken, 
    wenn man in den anderen Reitern Eingaben geändert hat. Oder
    
    > Wenn ich die Kolonnenüberschriften bei den Akteuren ändere, stehen in
    > der Dropdown der Ausgaben immer noch die alten. Nur im "eigenen Fenster"
    > sind sie aktualisiert.

#.  Hilfetexte: er könnte eigentlich auch gleich die Felder der 
    Basisklassen anzeigen. 
    Der Unterschied ist für den Benutzer nicht wichtig.

#.  Picker for calendar color. Or at least a ChoiceList with names.
    http://ext.ensible.com/forum/viewtopic.php?f=2&t=339
    See :file:`calendar-colors.css`

#.  http://www.sencha.com/learn/grid-faq/

#.  http://code.google.com/p/support/wiki/ScriptedUploads
    http://wiki.python.org/moin/CheeseShopTutorial
    
#.  Checkboxen können nicht aktiv sein, weil sie aufs change-Event nicht reagieren. 
    Und das check-Event kann ich auch nicht nutzen, weil das auch schon beim 
    loadRecord abgefeuert wird. Doof, aber scheinbar wahr.
    
    Stattdessen könnte ich ein spezielles `keyword attribute`
    für Checkboxen machen::
    
      all_day = ExtAllDayField(_("all day"),disables=('end_time','start_time'))
      
    - :attr:`disables` : a list or tuple of names of fields which should become
      disabled when the field is checked (and enabled when it is unchecked)
    - :attr:`enables` : a list or tuple of names of fields which should become
      enabled when the field is checked (and disabled when it is unchecked)
      
    Das hätte vor allem auch den Vorteil, dass dann überhaupt kein Ajax-Call 
    nötig ist.
    
    En attendant ist das Feld Ganztags nicht aktiv, und die Uhrzeit-Felder 
    werden *nicht* disabled wenn es angekreuzt ist. Weil man sonst nicht 
    einfach einem Ganztagstermin eine Uhrzeit zuweisen kann.
    
#.  When a user tries to sort a column on a RemoteField, the server says::

      FieldError
      Cannot resolve keyword u'applies_until' into field. Choices are: activity, addr1, addr2, aid_type, bank_account1, bank_account2, birth_country, birth_date, birth_place, broker, cal_guest_by_contact, card_issuer, card_number, card_type, card_valid_from, card_valid_until, city, civil_state, coach1, coach2, coached_from, coached_until, contact_ptr, country, email, event, faculty, fax, first_name, gender, gesdos_id, group, gsm, health_insurance, id, identifypersonrequest, in_belgium_since, income_ag, income_kg, income_misc, income_rente, income_wg, is_active, is_cpas, is_deprecated, is_seeking, is_senior, job_agents, job_office_contact, language, last_name, mails_by_sender, name, national_id, nationality, needs_residence_permit, needs_work_permit, newcomer, noble_condition, note, obstacles, pharmacy, phone, recipient, recurrenceset, region, remarks, remarks2, residence_type, rolesbyperson, skills, street, street_box, street_no, street_prefix, task, third, title, unavailable_until, unavailable_why, unemployed_since, url, work_permit_suspended_until, zip_code

      TRACEBACK:
        File "l:\snapshots\django\django\core\handlers\base.py", line 111, in get_response
          response = callback(request, *callback_args, **callback_kwargs)

        File "t:\hgwork\lino\lino\ui\extjs3\ext_ui.py", line 1409, in api_list_view
          rows = [ rh.store.row2list(ar,row) for row in ar.sliced_data_iterator]

        File "l:\snapshots\django\django\db\models\query.py", line 104, in _result_iter
          self._fill_cache()

        File "l:\snapshots\django\django\db\models\query.py", line 776, in _fill_cache
          self._result_cache.append(self._iter.next())

        File "l:\snapshots\django\django\db\models\query.py", line 266, in iterator
          for row in compiler.results_iter():

        File "l:\snapshots\django\django\db\models\sql\compiler.py", line 699, in results_iter
          for rows in self.execute_sql(MULTI):

        File "l:\snapshots\django\django\db\models\sql\compiler.py", line 744, in execute_sql
          sql, params = self.as_sql()

        File "l:\snapshots\django\django\db\models\sql\compiler.py", line 62, in as_sql
          ordering, ordering_group_by = self.get_ordering()

        File "l:\snapshots\django\django\db\models\sql\compiler.py", line 359, in get_ordering
          self.query.model._meta, default_order=asc):

        File "l:\snapshots\django\django\db\models\sql\compiler.py", line 388, in find_ordering_name
          opts, alias, False)

        File "l:\snapshots\django\django\db\models\sql\query.py", line 1283, in setup_joins
          "Choices are: %s" % (name, ", ".join(names)))


#.  http://ckeditor.com/demo

#.  [pdf] button : generate html table without THEAD, TFOOT and TBODY.
    Am besten sogar separate Methoden Table.header_html() und Table.body_html().
    Dazu muss ich vielleicht voerher den Store generalisieren
    :doc:`/tickets/57`.
    "StoreField" wird nach "Atomizer" umbenannt und im Model gespeichert
    
#.  Listings 
    "Personnes par phase d'intégration par AI" 
    and
    "Contrats par Employeur et par AI":
    how to manage grouping in a report.

#.  User permissions, levels, profiles

#.  Zwei Ideen zur besseren Ermittlung der Konstruktionsmethode einer Notiz: 

    - noch einen optionalen benutzerspezifischen Parameter
      "Default-Konstruktionsmethode", 
      der Vorrang vor dem entsprechenden globalen Parameter hat.
      Printable.get_build_method()
      `CachedPrintable.get_cache_mtime` muss dann allerdings einen 
      optionalen Parameter `user` kriegen.
    - verwendete Konstruktionsmethode pro Notiz speichern. 
      Vorteil: zum Testen kann man dann leichter auf eine andere Method umschalten.
      Nachteile: (1) ein relativ unnützes Datenfeld (20 bytes pro Notiz) hinzu, 
      und (2) bei DirectPrintAction ist das auch keine Lösung.

#.  :class:´lino.modlib.jobs.Function` : "Funktionen" 
    umbenennen nach "Qualifikationen"?
    Weil auch :class:´lino.modlib.contacts.RoleType` so übersetzt wird.
    Oder aber Modelle :class:´lino.modlib.jobs.Function` 
    und :class:´lino.modlib.contacts.RoleType` vereinigen?
    Eher Letzteres.
    Aber was passiert dann mit den Sektoren?
    Antwort: Function.sector wird optional. 
    Es gibt Funktionen, die nicht sektorgebunden sind (Lagerarbeiter, 
    Direktor, Sekretär)
    Es könnte Stellenanfragen geben, die für einen bestimmten Sektor, 
    aber nicht für eine bestimmte Funktion gemeint sind 
    ("Ich suche einen Job im Horeca-Bereich, egal was")
    
    Als *Qualifikationen* würde ich eher noch eine weitere Tabelle 
    vorschlagen: pro Stellenangebot bzw. Personensuche 
    eine Liste von "erforderlichen Ausbildungen". 
    Vielleicht auch keine Liste, sondern nur ein Feld, 
    weil meistens nur ein Ausbildungsabschluss erforderlich ist.

#.  Der Ausdruck einer Notiz "Aktennotiz" - "Stand der Dinge" geht nur
    unformatiert (TinyMCE). Sobald man z. B.  den Titel formatiert, kommt
    beim Ausdruck nicht alles raus.
    
#.  Listing "Übersicht Verträge": die diversen Stellen sollten auf der 
    Übersicht der Verträge optisch noch nach Arbeitgeber gruppiert sein.
    
#.  Die neue Tabelle Berufswünsche sollte auch in der
    Personensuche integriert werden, damit falls dem DSBE verfügbare externe
    Stellen zugetragen werden, schnell ein geeigneter Kandidat gefunden
    werden kann.

#.  Remote calendars (:doc:`/tickets/47`):

    - recursion rules and recursive events
    - get calendarserver running on :term:`Jana`.
    
#.  notes.Notes nicht mehr PartnerDocument sondern ProjectRelated.
    In einer Notiz wie Nr. 1019 würde dann die Zuweisung zur 
    Firma verloren gehen. Kann ggf. als Drittpartner eingegeben 
    werden. Betroffen sind folgende Notizen::
    
      >>> from lino.projects.pcsw.models import Note
      >>> [int(n.pk) for n in Note.objects.filter(company__isnull=False)]
      [499, 501, 616, 349, 1019, 825, 425, 996, 117, 508, 822, 342, 841, 842]
      
#.  Attachments of outgoing mails.
    An UploadsByOwner slave in the detail of a mail will be enough for 
    users to upload their files.
    But how can we add files that are already on the server?
    For example, writing a mail from an invoice would automatically 
    attach the invoice's .pdf without having to upload it. 
    The .pdf in such a case is not in `media/uploads` but in `media/cache`.
    Both types of attachments should be possible and mixable.
    Note that Uploadable.file is a FileField(upload_to='/media/uploads').
    Maybe another field "local_file", a simple CharField?
    
#.  In Übersichtsliste die Benutzer des DSBE und die vom allgemeinen 
    Sozialdienst trennen. Also ein neues Feld `User.department`. 
    Sich dabei jedoch an der Struktur des LDAP-Verzeichnisses 
    orientieren in Hinblick auf spätere Synchronisierung.

#.  Automatische Erinnerung Arbeitserlaubnis 2 Monate vor dem in 
    "Gültig bis" angegebenen Datum gemacht werden. Die Dauer "2 Monate" 
    am besten konfigurierbar in zwei neuen Felder `UploadType.alarm_value`
    `UploadType.alarm_unit`.
    
#.  auf Jana werden Tabellen nicht korrekt gerendert, auf Armand wohl.

      - OOo-Version? auf Jana ist 3.2:
        zless /usr/share/doc/openoffice.org-core/README.gz
      - appy.pod-Version?

#.  Lino könnte per LDAP-Request verschiedene Angaben 
    in :class:`auth.User` (Name, E-Mail,...) 
    direkt vom LDAP-Server anfragen.
    Dazu wären wahrscheinlich
    http://www.python-ldap.org/
    und
    http://www.openldap.org/
    nötig.

#.  Externe Links (Lesezeichen) und Uploads per drag & drop machen können, 
    indem man sie von einer anderen Anwendung auf die HtmlBox zieht.
    (u.a. :doc:`/tickets/8`)

#.  :doc:`Benutzerspezifische Gridkonfiguration </tickets/39>`
    
#.  Doppelklick auf Memo-Text einer Note in einer Grid
    bewirkt *nichts*. 
    Sollte doch wenigstens das Detail-Fenster öffnen.
    

Medium-term
-----------

#.  "it took me almost an hour to create my first working Lino user."
    --> 
    Maybe this can be solved for future newcomers by adding some 
    dbinit hook which asks to create a superuser, as 
    `django.contrib.auth` does.


#.  Must I implement a way to make sure that for any existing 
    Voucher record there's always one and only one MTI child in one of the 
    VoucherType tables?

#.  User stories: 
    Alicia: Hubert hatte in meinem Urlaub eine Telefonnotiz auf einem meiner 
    Klienten gemacht, und mir nun mündlich noch ein paar Zusatzinfos gesagt, 
    die er nur vergessen hatte, rein zu schreiben. Ich will jetzt an seiner 
    Stelle seine 
    Notiz nachträglich korrigieren, damit das direkt beim ersten Lesen deutlich ist.


#.  Historique des "choses" consultées pendant une session 
    pour facilement naviguer d’une "chose" à l’autre.
    Chose = configurable: Personnes, Clients, Demandes,...

#.  ManageAccessRequest now also has a separate insert_layout. 
    But we cannot inherit here from ManageAccessRequestDetail 
    and thus had to (almost) duplicate the `setup_handle`::
  
      def setup_handle(self,lh):
          lh.p1.label = _("Requested action")
          lh.proof.label = _("Proof of authentication")
          super(ManageAccessRequestInsert,self).setup_handle(lh)
  
    TODO: more transparent/reusable system to specify labels.


#.  Make ChoiceLists visible through the web interface. 
    Show UserGroups and UserProfiles in :class:`lino.models.About`.

#.  Was Lino noch braucht und nicht hat, ist die Möglichkeit, 
    dass beim Klicken auf den Button einer Aktion vor deren Abschicken 
    noch ein Dialogfenster mit Optionen kommt. 
    Zum Beispiel eine Aktion `cal.Event.defer`, 
    die vorher noch wissen muss, um wieviele Tage (Wochen, Monate) oder 
    bis zu welchem Datum sie verschieben soll.

#.  Tabelle der Benutzerprofile (und generell alle choicelists) in 
    eine lokale Konfigurationsdatei auslagern und dadurch auch für 
    Nichtprogrammierer bearbeitbar machen.

#.  Wenn man auf einer Notiz "per E-Mail" klickt, kommt ein Fenster mit der 
    neu erstellten E-Mail. 
    Die Mail ist da schon in der Datenbank erstellt worden .
    Das ist suboptimal, denn wenn man hier einfach mit Escape abbricht, 
    bleibt die halbfertige Mail bestehen.
    Das kommt, weil Empänger eine Slave-Tabelle ist und wir diese Tabelle 
    doch eigentlich auch schon "beim Erstellen" sehen wollen.
    Eigentlich müsste das insert_layout kommen.
    Probieren, wie es aussieht, wenn wir die Empfängerliste eben erst nach 
    Klick auf "Erstellen" eingeben.

#.  lino*.js aufsplitten: der Teil aus linolib.js ist ja 
    konstant für alle Benutzerprofile.
    
#.  :func:`lino.modlib.cal.models.default_calendar` is called only when 
    a user has created at least one Event or Task. Problem: when a user 
    create their first event using CalendarPanel, they don't see their 
    own Calendar because it doesn't yet exist. 
    Creating a User should automatically create a corresponding Calendar.

#.  :meth:`lino.utils.appy_pod.Renderer.insert_table`: 
    Zero values are currently *always* hidden (printed as 
    empty cells, not "0" or "0,00") 
    It is not yet possible to configure this behaviour.

#.  :meth:`lino.utils.appy_pod.Renderer.insert_table`: 
    Accept the table's width as a parameter. Currently is it hardcoded to "18cm".

#.  Lino doesn't yet support :term:`remote fields <remote field>` 
    that point to a *virtual* field.
    That's why we don't have columns `person__age` 
    and `person__address_column` in :class:`Offene Kursanfragen 
    <lino.modlib.courses.models.PendingCourseRequests>`.

#.  Rechtschreibungshilfe in TinyMCE? 

#.  Redundant code in js_render_GridPanel_class() and ext_elems.GridPanel.

#.  Country, Region and City. Belgium is -despite their constant language 
    disputes- obviously a very *united* country since they don't need 
    a `region` field when entering a postal address. 
    In many other countries such a field is required.
    There should be a configuration option to handle this preference.
    Also a Regions table.

#.  Die virtuellen Felder `applies_from` und `applies_until` 
    in :class:`Meine Klienten <lino.projects.pcsw.models.MyPersons>` 
    machen jedes seinen eigenen Datenbank-Request 
    Also zwei zusätzlichen Requests für jede Zeile. 
    Einer für beide Felder würde reichen. 
    Noch besser wäre natürlich gar keiner:
    https://docs.djangoproject.com/en/dev/ref/models/querysets/#annotate
    https://docs.djangoproject.com/en/dev/topics/db/managers/
    https://docs.djangoproject.com/en/dev/topics/db/aggregation/

#.  Unerwünschte Scrollbars:

    - Beim Passbild (nur mit Firefox und Chromium 17, aber nicht mit Chrome 16)
    - Im Detail Kursangebot (manchmal)
    
#.  Automatische Auswertungstermine eines Vertrags: 
    Warnung, wenn sie nicht alle generiert wurden, 
    weil die maximale Anzahl überschritten wurde.


#.  Eigentlich ist ein TableRequest per se jetzt nicht mehr iterable. 
    Man muss sich entscheiden für entweder `data_iterator` oder `sliced_data_iterator`.
    Ob das so toll ist? Sollte ich nicht doch die `__iter__()` wieder reintun, 
    und die loopt dann über den `sliced_data_iterator`? 
    Wenn man explizit das 
    offset und limit ignorieren will (was außer von get_total_count auch 
    von den druckbaren Versionen (csv, html, pdf) benutzt wird, fragt man 
    sich den `data_iterator`.


#.  The `setup_*` methods in models modules should be inside a Module class which 
    also has a userfriendly (and translated) description of the module.
    The kernel would instantiate these Module classes and store them as 
    the items of `settings.SITE.modules`.
    
#.  Links to :class:`lino.dd.Table` don't work. 
    Must say :class:`lino.core.table.Table`

#.  Datenkontrollliste erweitern. Meldungen im Stil:

    - "Benutzer hat is_dsbe eingeschaltet, begleitet aber nur 2 Personen"
    - "Person gilt als begleitet, hat aber keine Anfragen / keine
       Verträge / keine Notizen"
    - ...
     
    Und ich müsste dann eine solche Liste vor und nach dem Release
    ausdrucken, oder besser gesagt die Dinger müssten von der
    Kommandozeile aus als Textdateien gespeichert werden, damit ich
    sie leicht vergleichen kann.

#.  EditTemplateAction auf PrintableType kann jetzt implementiert werden.

#.  Idée reconfirmée par Gaëtan: .dtl files in Python, not yaml

#.  What about Cédric Krier's `HgNested extension
    <http://mercurial.selenic.com/wiki/HgNestedExtension>`_?

#.  Support for eID cards: (1) read data from card and (2) user authentication.

    http://code.google.com/p/eid-javascript-lib/downloads/list
    http://www.e-contract.be/
    http://code.google.com/p/eid-applet/
    
#.  contacts.Group: Eine Kontaktgruppe hat keine zusätzlichen Felder, 
    das Modell wäre lediglich da, um eine Liste aller Gruppen anzeigen 
    und ggf. spezifische Detail-Fenster definieren zu können.
    Die Mitglieder einer Gruppe sind die Kontaktpersonen 
    (:class:`lino.modlib.contacts.models.Role`).
    Der eigentliche Unterschied ist, dass Gruppen (im Gegensatz zu Firmen) 
    automatisch ihre Mitgliedsadressen expandieren müssen, 
    wenn sie als Recipient einer Email fungieren.
    Das könnte aber auch bei Firmen und sogar bei Personen ein 
    interessantes Feature sein, 
    in diesem Fall brauchen wir gar keine eigene Tabelle Group.
    Zu meditieren.

#.  Uploads mit Sonderzeichen im Dateinamen funktionieren noch nicht.
    See :blogref:`20110725` and :blogref:`20110809`.

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

#.  Custom Quick filters 
    See :blogref:`20111207`.

#.  lino.projects.pcsw has a database design flaw: 
    Person should be split into "Clients" and "normal" persons.
    Contact Persons of a Company currently need to have an entry in the Person table.
    This is also the reason for many deferred save()s when loading a full backup.

#.  Split :class:`lino.reports.Report` into :class:`lino.List` and :class:`lino.Detail`.
    :class:`lino.ui.extjs3.ext_store.Store` should then create one Store per Model.

#.  Write test cases with different cases of jobs.contract and isip.Contract

#.  Il est vrai que Lino devrait désactiver le bouton "save grid config" 
    pour les utilisateurs qui n'ont pas la permission (et chez qui Lino 
    réagit en disant error_response {'message': u"L'utilisateur user ne peut 
    pas configurer contacts.Persons.", 'success': False, 'alert': True})

#.  notes : Note.body füllen aus Note.eventtype.body 
    und dabei wahrscheinlich Djangos templating language verwenden.

#.  Simplified installation process without system wide configuration changes 
    for people who just want to give a try to Lino. (:doc:`/admin/install`) 

#.  Hauptmenü:
    Was noch fehlt, wäre eine Leiste mit Shortcuts (die am besten pro Benutzer konfiguriert werden können)


#.  GridFilter on BooleanField doesn't work.
    In `reports.add_gridfilters` there's an exception 
    "Join on field 'native' not permitted. Did you misspell 'equals' for the lookup type?" when 

http://lino/api/pcsw/LanguageKnowledgesByPerson?_dc=1315554805581&sort=written&dir=DESC&filter=%5B%7B%22type%22%3A%22boolean%22%2C%22value%22%3Atrue%2C%22field%22%3A%22native%22%7D%5D&fmt=json&mt=20&mk=20069



#.  Rapport pour Actiris (Office Régional Bruxellois de l'Emploi). 
    Donc ce rapport pour Actiris doit mentionner, par assistant social, 
    le nombre d’ouvertures et de fermetures de dossier pendant un certain 
    laps de temps.

#.  Enhance performance by using xtype instead of instantiating directly:
    http://iamtotti.com/blog/2011/05/what-makes-your-extjs-application-run-so-slow/
    Note that I started to prefer direct instantiation when I had had some 
    problems that solved simply be switching from "xtype" to "direct".
    But at that time I didn't imagine that 
    interacting with the DOM is always expensive.
    
#.  Dojo now has a
    `datagrid <http://dojotoolkit.org/documentation/tutorials/1.6/datagrid/>`_
    and looks easy to learn.

#.  Rename "lino.mixins.Owned" to "Anchored" 
    (and XxxByOwner to XxxByAnchor"?
    
#.  Ich habe momentan noch kein Beispiel dafür, wie man eine eigene 
    ROOT_URLCONF setzen kann, um einen Site zu machen, bei dem Lino nur 
    "draufgesetzt" ist (so wie "admin" in der Tutorial-Anwendung von Django).

#.  Jetzt wo es aktive Felder gibt, sollte das Formular während des submit 
    deaktiviert werden, immerhin dauert das manchmal eine Sekunde.
    
#.  Bug in :term:`appy.pod`: https://bugs.launchpad.net/appy/+bug/815019

#.  Client-seitiger Ersatz für den "Memo"-Button, der seit 
    :blogref`20110605` wieder raus ist.
    Mir war klargeworden, dass diese Lösung (Memo-Felder auf Anfrage 
    schon serverseitig abzuschneiden) erstens theoretisch Unsinn war 
    und zweitens in der Praxis noch einige Bugs hatte. Momentan wird 
    in der Grid immer nur die Kurzform angezeigt (`overflow:hidden;`), 
    und irgendwann muss ich mal eine client-seitige Lösung in Javascript 
    machen. Interessant wäre, wenn man die Höhe einzelner Zeilen 
    manuell verändern kann. Eventuell den Text-Editor im eigenen 
    Fenster aufrufen bei Doppelklick.

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

#.  Logging to a database. 
    Rotating logs haben den Nachteil, dass sie nicht ewig bestehen bleiben und nicht archiviert werden können. Die momentane Lösung hat den Nachteil, dass watch_tim und apache u.U. in verschiedene Dateien loggen, weil der Dateiname beim Start des Prozesses ermittelt wird. Ich denke momentan als nächstes adaran, in eine Datenbank zu loggen. Hier zwei Stackoverflow als Einstieg zum Thema:

      http://stackoverflow.com/questions/2314307/python-logging-to-database
      http://stackoverflow.com/questions/1055917/server-logging-in-database-or-logfile

#.  An makedocs müsste ich bei Gelegenheit mal ein bisschen weiter machen. 
    Das ist noch lange nicht fertig.
    
#.  Welche weiteren Felder müssen (ähnlich wie "Stadt") lernfähig werden? 
    Vorschläge: 
    
    - lino.projects.pcsw.models.Study.content
    
#.  igen : Partner.get_invoice_suggestions()

#.  MTI auch für Personen anwenden: 
    in lino.pcsw für "normale" Personen nur die 
    Standard-Kontaktangaben speichern, und die DSBE-spezifischen Felder 
    in einer eigenen Tabelle.  Neues Model "Client(Person)"

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
    in :class:`lino.projects.pcsw.settings.Lino`
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
    lino.pcsw stattdessen ein neues Modell CoachedPerson(contacts.Person) 
    definieren. 
    Dann hätten "normale" Kontaktpersonen von Firmen gar 
    nicht die vielen Felder des DSBE.
    Dazu wäre ein Feld Person.type nötig.
  
#.  Idee: Module umstrukturieren:

    | lino.pcsw.models : Contract usw.
    | lino.pcsw.contacts.models : Person, Company,...
    
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
   http://127.0.0.1:8000/api/pcsw/ContractsByPerson/2?mt=14&mk=16&fmt=print 
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
   Siehe :blogref:`20101029`, :blogref:`20101112`.
  
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
  
#. (:mod:`lino.modlib.pcsw` : 
   Wie soll ich es machen, dass der Benutzer beim Auswählen der Krankenkasse einer Person 
   nicht alle Firmen, sondern nur die Krankenkassen angezeigt bekommt? 
   Etwa ein eigenes Feld `Company.is_health_insurance`?
   Oder auf den Berufscode filtern?

#. Die Buttons der tbar sollten mit Icons versehen werden. 
   Für manche Funktionen (Insert,Delete) gibt es vielleicht 
   schon Icons aus der ExtJS.

#. Abfragen mit komplexen Bedingungen zur Suche nach Personen

#. Benutzbarkeit per Tastatur verbessern (issue 11, issue 64) 

#. Sehen können, nach welcher Kolonne eine Grid sortiert ist.

#. Prüfen, ob die neuen ExtJS-Features für Lino interessant sind:

  - `Forms with vbox Layout <http://dev.sencha.com/deploy/dev/examples/form/vbox-form.html>`_ 
  - `Composite Form Fields <http://dev.sencha.com/deploy/dev/examples/form/composite-field.html>`_ 

#. Filter auf virtuelle Kolonnen setzen können. Siehe :blogref:`20100811`.

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
   In Lino-PCSW gibt es :xfile:`make_staff.py`, aber das ist nur ein sehr primitives Skript.
  
#. Im Fenster :menuselection:`System --> Site Configuration` müssten Delete und Insert noch weg. 

#. http://code.google.com/p/extjs-public/
   und
   http://www.sencha.com/blog/2009/06/10/building-a-rating-widget-with-ext-core-30-final-and-google-cdn/
   lesen.  
  
#. Feldgruppen. Z.B. bei den 3 Feldern für Arbeitserlaubnis (:attr:`pcsw.models.Person.work_permit`) in DSBE wäre es interessant, 
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
   FormPanel und GridPanel.get_selected() geben deshalb jetzt nicht mehr bloß eine Liste der IDs, 
   sondern eine Liste der Records.
   Aber das nützt (noch) nichts, denn ich weiß nicht, wie ich den Grid-Store überredet bekomme, 
   außer `data` auch eine Eigenschaft `title` aus jedem Record rauszulesen. 
   Auf Serverseite wäre das kein Problem: ich bräuchte einfach nur title 
   in `elem2rec1` statt in `elem2rec_detailed` zu setzen.
   Aber das interessiert den Store der Grid nicht. Kann sein, dass ich ihn konfigurieren kann...
   Oder ich würde es wie mit `disabled_fields` machen. Also ein neues automatisches 
   virtuelles Feld __unicode__.
  
#. Insert-Fenster: Für die Situationen, wo man viele neue Records hintereinander erfasst, könnte
   vielleicht ein zusätzlicher Knopf "Save and insert another" (wie im Django-Admin), 
   oder aber das automatische Schließen des Insert-Fensters im Report abschalten können.

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
   (sh. :blogref:`20101103`)
  
#.  Use event managers as suggested by Jonathan Julian (Tip #2 in
    http://www.slideshare.net/jonathanjulian/five-tips-to-improve-your-ext-js-application). 
    Maybe for each report::
  
      Lino.contacts.Persons.eventManager = new Ext.util.EventManager();
      Lino.contacts.Persons.eventManager.addEvents('changed');
    
    Lino could use this to have an automatic refresh of each window that displays data. 
    Maybe rather only one central event manager because if any data gets changed, 
    basically all open windows may need a refresh.

#.  :doc:`/tickets/16`

#.  Mehr über Nuxeo lesen: http://doc.nuxeo.org/5.3/books/nuxeo-book/html/index.html

#.  Use :meth:`Action.run` in general, not only for RowAction. 
    See :blogref:`20101124`
  
#.  Warnung, wenn das gleiche Feld mehrmals in einem Detail 
    vorkommt (z.B. in verschiedenen Reitern).
    Oder besser: diesen Fall zulassen.
   
#.  http://code.google.com/p/extjs-public/   

#.  Wenn man z.B. watch_tim oder initdb_tim manuell startet und der 
    ein log-rotate durchführt, dann haben die neu erstellten Dateien 
    anschließend nicht www-data als owner. Resultat: internal server error!

#.  http://de.wikipedia.org/wiki/Xming

#.  Chrome 10 hat scheinbar ein Problem mit ExtJS:
    http://www.google.com/support/forum/p/Chrome/thread?tid=5d3cce9457a1ebb1&hl=en    
    
#.  :doc:`/tickets/25`

#.  :doc:`/tickets/26`

#.  Man kann es momentan nicht verhindern, dass ein Babel-Feld expandiert wird.
    
#.  Check whether Lino should use
    http://django-rest-framework.org/
    instead of reinventing the wheel.
    (Discovered :blogref:`20110311`)
    
    
    
Together with a Linux freak
---------------------------

#.  `How to LSBize an Init Script <http://wiki.debian.org/LSBInitScripts>`_

#.  all_countries.py : load english countries from 
    `/usr/share/zoneinfo/iso3166.tab`
    But how to find the same in French, German, Estonian?
    Or, maybe better, use `python-babel`.
    
#.  The file `sihtnumbrid.csv` (:blogref:`20120514`) is still in the 
    repository.
    That's because it's rather difficult to really remove something from history.
    As explained in http://mercurial.selenic.com/wiki/EditingHistory

#.  Move from Mercurial to Git and from Google to Gitorious.
    See :blogref:`20130818`.
    
    


Documentation
-------------

#.  Anpassungen :doc:`/admin/install` an Debian Squeeze.
    OpenOffice bzw. LibreOffice braucht jetzt wahrscheinlich 
    nicht mehr manuell installiert zu werden.

#.  Wenn ich in der INSTALLED_APPS von lino.demos.std.settings 
    auch die igen-Module reintue, dann kriege ich::
  
     ref\python\lino.modlib.dsbe.rst:17: (WARNING/2) autodoc can't import/find module 'lino.projects.dsbe.models', 
     it reported error: "resolve_model('contacts.Company',app_label='contacts',who=None) found None"

#.  ``make doctest`` nutzbar machen. Siehe :blogref:`20101024`

#.  Check whether 
    `pydocweb <https://github.com/pv/pydocweb/tree/master/docweb>`_    
    would be useful.

#.  I'm trying to document several Django applications on a single Sphinx tree. 
    Django modules have the requirement that an environment variable DJANGO_SETTINGS_MODULE be set when importing them. 
    Maybe one way is to add an `environment` option to the `automodule` directive?

#.  Ausprobieren, was David De Sousa am 12.11.2009 auf sphinx-dev gepostet hat.

#.  Creating application-specific DetailLayouts disables the effect of eventual 
    `add_detail_tab` calls by other installed apps.
    Example: :mod:`lino.projects.pcsw` used 
    to create its own UserDetail, a subclass of 
    :class:`lino.modlib.users.models.UserDetail`. 
    But then we started to use :meth:`lino.core.actor.Actor.add_detail_tab` 
    in :mod:`lino.modlib.cal` and :mod:`lino.modlib.newcomers`.
    This didn't work since `pcsw` then created her own UserDetail.
    
Lino workshop
-------------

Die folgenden Punkte möchte ich bei Gelegenheit mal live mit den 
Benutzern überlegen. 

#.  Uwe hat einen Bug gefunden: man kann in der Liste "Meine Klienten" 
    momentan noch nicht auf die Kolonnen "Vertrag beginnt" und 
    "Vertrag endet" sortieren. 
    Liegt daran, dass das virtual fields sind.
    Es ist zumindest nicht einfach, das zu ermöglichen. 
    Wahrscheinlich müssten wir dazu custom functions definieren, 
    was nicht alle db-Backends können.
    Eher stelle ich mir die Frage, ob da nicht ein Analysefehler 
    vorliegt. 
    Der Vorfall bestätigt Gerds Bedenken, als die Benutzerfrage kam.
    Eigentlich müsstet ihr die gleichen Infos auch 
    über die Befehle `Meine VSEs` und `Meine Art-60-7-Konventionen` 
    kriegen können.
    Zu analysieren mit den Benutzern.



Tickets
-------

.. toctree::
   :maxdepth: 2
   
   tickets/index

