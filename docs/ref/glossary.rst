========
Glossary
========

.. glossary::
  :sorted:
  
  customization functions
    See :doc:`/topics/customization`.
    
  mod_wsgi
   :doc:`/admin/install`
    
  dummy module
    See :func:`lino.core.dbutils.resolve_app`.

  testing
    The version that is currently being tested.
  
  DavLink
    See :doc:`/davlink/index`
    
  WebDAV
    See :doc:`/davlink/index`
    
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
     the first real user of a Lino application
     :mod:`lino.projects.pcsw`.
     
  dump
    "To dump" means to write the content of a database into a text file.
    This is used to backup data and for Data Migration.
    
  Data Migration
    Data Migration is when your database needs to be converted after 
    an upgrade to a newer Lino version. See :doc:`/admin/datamig`.

  CSC
    Context-sensitive ComboBox. 
    See :mod:`lino.utils.choices`.
    
  remote field
    We sometimes use this term for 
    `field lookups that refer to a joined model    <https://docs.djangoproject.com/en/dev/topics/db/queries/#lookups-that-span-relationships>`__.
    For example in a `Table` on a model `Invoice` that has a 
    ForeignKey `customer` to `Partner`, 
    then you can add a column `customer__city`. 
    
    
  field lookups
    See https://docs.djangoproject.com/en/dev/topics/db/queries/#field-lookups  
    
  GC
    Grid Configuration. 
    See :blogref:`20100809`,...
    
  disabled fields
    Fields that the user cannot edit (read-only fields). 
    
  initdb
    See :mod:`lino.management.commands.initdb`
    
  initdb_tim
    See :mod:`lino.projects.pcsw.management.commands.initdb_tim`
    
  watch_tim
    A daemon process that synchronizes data from TIM to Lino.
    See :mod:`lino_welfare.modlib.pcsw.management.commands.watch_tim`

  welcome message 
     A user-specific message that you get in your main page.  welcome
     messages are being generated dynamically each time your main page
     is being displayed. See :meth:`lino.core.actors.Actor.get_welcome_messages`.


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

  Active fields

    See :attr:`dd.Model.active_fields`.
    
  Table
    See :class:`dd.Table` and :class:`dd.AbstractTable`.
    
  Slave Table 

    A Slave Table is a :term:`Table` which displays only rows that
    "belong" to a given master instance. 

    For example if you have two models `City` and `Person`, with a
    `ForeignKey` `Person.city` pointing to `City`, then you might
    define a slave table `PersonsByCity` which displays only Persons
    who live in a given City.

  Dialog Action

    A dialog action is an action which opens a window where the user
    can specify "action parameters" before actually running the
    action.  

    An :class:`lino.core.actions.Action` is a dialog action if it has
    :attr:`lino.core.actions.Action.parameters` defined and
    :attr:`lino.core.actions.Action.no_params_window` has not been enabled.
    

  Detail Window

    A window that displays data of a single record.  Used for viewing,
    editing or inserting new records.  Besides fields, a Detail Window
    can possibly include :term:`Slave Tables <Slave Table>`.
    
  Insert Window

    The window used to edit data of a new record before it is being
    saved for the first time.

  GFK
    Generic ForeignKey. This is a ForeignKey that can point to 
    different tables.
    
  Minimal application
    See :doc:`/topics/minimal_apps`
