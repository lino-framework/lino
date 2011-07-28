========
Glossary
========


.. glossary::
  :sorted:

  Tups
     The machine that is serving the `saffre-rumma.net` domain.

  DSBE
     "Dienst für Sozial-Berufliche Eingliederung"     
     A public service in Eupen (Belgium) who helped develop
     the Lino application of the same name :doc:`/dsbe/index`.
     
  ExtJS
    http://www.sencha.com/products/js/
    
  Django
    http://docs.djangoproject.com
    
  dump
    See :doc:`/admin/datamig`.

  CSC
    Context-sensitive ComboBox
    
  GC
    Grid Configuration. 
    See :doc:`/blog/2010/0809`,...
    
  TIM
    http://code.google.com/p/tim
      
  disabled fields
    Fields that the user cannot edit (read-only fields). 
  
  initdb
    See :mod:`lino.management.commands.initdb`
    
  initdb_tim
    See :mod:`lino.apps.dsbe.management.commands.initdb_tim`
    
  watch_tim
    A daemon process that synchronizes data from TIM to Lino.
    See :mod:`lino.apps.dsbe.management.commands.watch_tim`

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

  Detail Window
    A window that displays data of a single record 
    (possibly including slave records).
    Used for viewing, editing or to insert new records.
    
  GFK
    Generic ForeignKey. This is a ForeignKey that can point to 
    different tables.