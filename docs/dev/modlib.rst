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


  
