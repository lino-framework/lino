To-do list
==========

See also :doc:`/tickets/index` which is a list of tickets.

.. todolist::

The rest of this document is partly in German because it 
is rather for internal use. 


Short-term
----------

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




#.  Continue with BCSS-Connection: 

    - add more fields to existing first service
    - button to quickly create a request
    
#.  Mails verschicken: notes.Note und mails.OutMail könnten 
    zusammengeführt werden. Kann sein, dass thirds.Third dann 
    unnötig wird.
    
#.  User profiles and one lino.js per user profile. 
    Because this would save a lot of JS code to download for most users.
    
#.  Kontakte als common base class für Personen und Firmen : 
    beibehalten oder wieder trennen?

#.  The CalendarPanel when starting, calls all Events. 
    Should call only those of current month.
    http://ext.ensible.com/forum/viewtopic.php?f=2&t=477

#.  Layout problem "wrong background color" in Detail of a Note 
    and parameter panels.
    
#.  [pdf] button : generate html table without THEAD, TFOOT and TBODY.
    Am besten sogar separate Methoden Table.header_html() und Table.body_html().
    Dazu muss ich vielleicht voerher den Store generalisieren
    :doc:`/tickets/57`.
    "StoreField" wird nach "Atomizer" umbenannt und im Model 
    
#.  Continue with Report Generator (:doc:`/tickets/54`).
    Listings 
    "Personnes par phase d'intégration par AI" 
    and
    "Contrats par Employeur et par AI":
    how to manage grouping in a report.

#.  User permissions, roles, functions

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
    
#.  notes.Notes nicht mehr PartnerDocument sondern ProjectBased.
    In einer Notiz wie Nr. 1019 würde dann die Zuweisung zur 
    Firma verloren gehen. Kann ggf. als Drittpartner eingegeben 
    werden. Betroffen sind folgende Notizen::
    
      >>> from lino.apps.dsbe.models import Note
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

#.  Die virtuellen Felder `applies_from` und `applies_until` 
    in :class:`Meine Klienten <lino.apps.dsbe.models.MyPersons>` 
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
    the items of `settings.LINO.modules`.
    
#.  Ich gebe zu bedenken, dass wir den Begriff "aktiv" dann demnächst in 
    zwei verschiedenen Bedeutungen verwenden:
    (a) Checkbox "aktiv" angeschaltet (Feld wird aus TIM importiert) 
    (b) einer aktiven Integrationsphase zugewiesen
    Ich könnte z.B. das aus TIM importierte "aktiv" umbenennen 
    nach "versteckt" (und bei der Migration die Werte umkehren). 
    Lohnt sich die Arbeit?

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

#.  Idée venue avec Gaëtan: .dtl files in Python, not yaml

#.  What about Cédric Krier's `HgNested extension
    <http://mercurial.selenic.com/wiki/HgNestedExtension>`_?

#.   There is also an almost philosphical question: where should the label "Calendar" 
    (and it's translations) be defined? Currently it is in 
    :class:`lino.reports.Calendar`. The whole pot-pourri of actors and actions 
    (Report, Frame, Detail, Action) might get an internal revision soon: 
    - is it necessary to instantiate Actors? 
      Should the instantiation of an actor represent a request?
    - Split "Report" into "List" and "Detail": both of them get their own store. 
      Note that one Detail would contain the equivalent of all .dtl files.
      Replace .dtl files (one per tab) by a single configuration file.
      The possibility of local configuration should remain, but convert them to Python code.
    - Actions should be rather like fields: instantiated within the subclass definition.


#.  Support for eID cards: (1) read data from card and (2) user authentication.

    http://code.google.com/p/eid-javascript-lib/downloads/list
    
    http://www.e-contract.be/
    http://code.google.com/p/eid-applet/
    
#.  Notizen per E-Mail verschicken können.    
    Soll Text der Notiz in den Body der E-Mail kopiert werden 
    und dort bearbeitbar sein? Dadurch würden die Benutzer allerdings 
    zu redundanter Arbeitsweise erzogen... zu meditieren.
    
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
    See :doc:`/blog/20110725` and :doc:`/blog/20110809`.

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
    See :doc:`/blog/2011/1207`.

#.  lino.apps.dsbe has a database design flaw: 
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

http://lino/api/dsbe/LanguageKnowledgesByPerson?_dc=1315554805581&sort=written&dir=DESC&filter=%5B%7B%22type%22%3A%22boolean%22%2C%22value%22%3Atrue%2C%22field%22%3A%22native%22%7D%5D&fmt=json&mt=20&mk=20069



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
    :doc`/blog/2011/0605` wieder raus ist.
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

#.  An makedocs müsste ich bei Gelegenheit mal ein bisschen weiter machen. 
    Das ist noch lange nicht fertig.
    
#.  In einer Grid mit Notizen die Hintergrundfarbe jeder Reihe 
    abhängig von Notizart und/oder Ereignisart machen.

#.  Welche weiteren Felder müssen (ähnlich wie "Stadt") lernfähig werden? 
    Vorschläge: 
    
    - lino.apps.dsbe.models.Study.content
    
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