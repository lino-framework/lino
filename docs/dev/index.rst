Developing Lino applications
============================

(This document is currently not well maintained. Don't read it!)


Introduction
------------

Lino applications are basically normal Django applications, but 
instead of writing `Admin` classes for your Django models, you write Reports 

A Report describes a set of tabular data
independently of *user interface* and *medium* (paper, screen, interactive or not), 
but with all the meta-data information necessary for any user interface 
to produce a satisfying result on any medium.
This is the theory.

Because we don't yet have carefully selected examples, 
we suggest here that you look at the code of the :mod:`lino.modlib.contacts` 
module which should be relatively self-explanatory.
For example :srcref:`/lino/lino/modlib/contacts/models.py`

Your Reports are subclasses of :class:`lino.reports.Report`, and they 
must be defined in your application's 'models' module because Lino 'discovers' 
and instantiates them automatically at startup.

You will also define Layouts for your detail forms.

A Layout describes an entry form in a GUI-independent way.
Users see them as Tabs of a Detail window (whose main component is a 
`FormPanel <http://www.extjs.com/deploy/dev/examples/form/xml-form.html>`_)

Instead of having each application register its models to the admin site, 
you write a main menu for your site that uses your Reports. 
This is is currently done in a file :xfile:`lino_settings.py`, 
usually in the same directory as Django's :xfile:`settings.py`.
This approach is less pluggable than Admin-based applications, 
but enterprise solutions don't need to be plug and play.


Overriding modlib models
------------------------


The :mod:`lino.modlib` modules are ready-to-use 
application modules (Django calls them "applications") 
that may be included in your :setting:`INSTALLED_APPS`::

  INSTALLED_APPS = (
  
    # manatory django.contrib applications needed by Lino
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    
    # your selection of lino.modlib applications:
    
    'lino.modlib.system',
    'lino.modlib.countries',
    'lino.modlib.contacts',
    'lino.modlib.projects',
    'lino.modlib.notes',
    
    # optionally you may write your own Django application that adds new models or reimplements models from lino.modlib.
    'myapp',  
  )

Django identifies models and SQL tables using a string of format `app_label.model_name`. 
The `app_label` is usually added automatically by taking the second-last 
part of the full Python module name. 

For example if you define two classes
`foo.sales.models.Invoice` and `bar.sales.models.Invoice` 
(both subclasses of django.db.models.Model) and install them both 
using ``INSTALLED_APPS = ['foo.sales', 'bar.sales']``, 
then `bar.sales.models.Invoice` will "override" 
`foo.sales.models.Invoice`, and 
`sales.Invoice` 
will be implemented by `foo.sales`, not by `bar.sales`.

Lino uses this behaviour to provide a collection of reusable Models, Reports and Menus that 
are not limited to a known implementation of a model will be used.



Optionally you may write your own Django application that adds new models or reimplements models from lino.modlib.

For example if you have a Django application `myapp` and want to extend :class:`contacts.Person`, then in :file:`myapp/models.py` you write::

  from lino.modlibe.contacts import models as contacts
  class Person(contacts.Person):

      class Meta:
          app_label = 'contacts'
          
      my_field = models.CharField(...)
      ...

The important thing is to manually specify `Meta.app_label` because otherwise your model would be called `myapp.Person`.


Conventions
-----------

- I'll try to always set verbose model names to uppercase.

    verbose_name = _("Person")           # not _("person")
    verbose_name_plural = _("Companies") # not _("companies")
    verbose_name = _("Note Type")        # not _("Note type")
  
  

.. toctree::
   :maxdepth: 2

   ../ref/model_methods


