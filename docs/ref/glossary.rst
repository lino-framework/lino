========
Glossary
========


.. glossary::
  :sorted:

  DavLink
    See :doc:`/davlink/index`
    
  generateDS
    http://www.rexx.com/~dkuhlman/generateDS.html
  
  Tups
     The machine that served the `saffre-rumma.net` 
     domain until 2010
     when it was replaced by :term:`Mops`.

  Mops
     The machine that is serving the `saffre-rumma.net` domain.

  Jana
     An internal virtual Debian server on our LAN used for testing.

  DSBE
     "Dienst für Sozial-Berufliche Eingliederung"     
     A public service in Eupen (Belgium), 
     the first serious user of a Lino application.
     :mod:`lino.apps.dsbe`.
     
  ExtJS
    http://www.sencha.com/products/js/
    
  Django
    http://docs.djangoproject.com
    
  dump
    "To dump" means to write the content of a database into a text file.
    This is used to backup data and for Data Migration.
    
  Data Migration
    Data Migration is when your database needs to be converted after 
    an upgrade to a newer Lino version. See :doc:`/admin/datamig`.

  CSC
    Context-sensitive ComboBox. 
    See :mod:`lino.utils.choices`.
    
  GC
    Grid Configuration. 
    See :doc:`/blog/2010/0809`,...
    
  TIM
    http://code.google.com/p/tim
      
  disabled fields
    Fields that the user cannot edit (read-only fields). 
    
  appy.pod
    See http://appyframework.org/pod.html
  
  lxml
    See http://lxml.de
  
  initdb
    See :mod:`lino.management.commands.initdb`
    
  initdb_tim
    See :mod:`lino.apps.dsbe.management.commands.initdb_tim`
    
  watch_tim
    A daemon process that synchronizes data from TIM to Lino.
    See :mod:`lino.apps.dsbe.management.commands.watch_tim`

  watch_calendars
    A daemon process that synchronizes remote calendars 
    into the Lino database.
    See :mod:`lino.modlib.cal.management.commands.watch_calendars`

  loaddata
    one of Django's standard management commands.
    See `Django docs <http://docs.djangoproject.com/en/dev/ref/django-admin/#loaddata-fixture-fixture>`_
    
  makeui
    A Lino-specific Django management command that 
    writes local files needed for the user interface.
    See :doc:`/topics/qooxdoo`.
  
  makedocs
    A Lino-specific Django management command that 
    writes a Sphinx documentation tree about the models 
    installed on this site.
    :mod:`lino.management.commands.makedocs`
    
  Report
    One of Lino's central concepts. 
    A report defines metadata about a certain view of the database.
    Deserves more documentation.
    :class:`lino.reports.Report`.
    
  Slave Report
    A Slave Report is a :term:`Report` that needs a master 
    and displays only rows that "belong" 
    to the master instance. For example if `PersonsByCity` displays all 
    Persons that live in a City, then City is the master of `PersonsByCity`.
    

  Detail Window
    A window that displays data of a single record. 
    Used for viewing, editing or inserting new records.
    Besides fields, a Detail Window can possibly include 
    :term:`Slave Reports <Slave Report>`.
    
  GFK
    Generic ForeignKey. This is a ForeignKey that can point to 
    different tables.
    
  BCSS
    Banque Carrefour de la Sécurité Sociale 
    (engl. "Crossroads Bank for Social Security").
    See :doc:`/topics/bcss`.
    
  PyPI
    The Python Package Index.
    Lino source releases are published there.
    See http://pypi.python.org/pypi/lino
    See http://pypi.python.org/pypi/lino/1.4.0
  