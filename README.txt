==========================
lino README
==========================
A framework for writing desktop-like web applications using Django and ExtJS

Description
-----------

Lino is a framework for writing desktop-like web applications 
using `Django <https://www.djangoproject.com/>`_
and `Sencha ExtJS <http://www.sencha.com/products/extjs/>`_.

Lino is for Python developers who want to develop 
Lino applications for their customers.
Primary target customers for Lino applications 
are agencies and companies who need a 
*customized database application*.

Lino the framework consists of different parts:

- `django-site <http://site.lino-framework.org>`__
  (split off from main project in March 2013)
  provides startup signals and the `settings.SITE` object
  
- `django-north <https://code.google.com/p/django-north/>`__
  (split off from main project in March 2013)
  provides python dumps, babel fields and data migration.

- :mod:`lino.modlib`, a collection of reusable Django apps
- A collection of out-of-the-box demo applications
- The default "plain" user interface 
- The optional ExtJS user interface 

The following real-world applications use the Lino framework:

- `Lino-Welfare <http://welfare.lino-framework.org>`__
  
  

Read more on http://www.lino-framework.org
