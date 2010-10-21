Lino and Django
===============

When in the end of 2008 I discovered Django, I was quickly seized by
its clear design and mature implementation.
The ORM and database model based on "applications" is simply genial.
The way of how this is integrated into a web application server system: genial.

Only one thing disturbed me: the 
`admin application <http://docs.djangoproject.com/en/dev/ref/contrib/admin/#ref-contrib-admin>`_  
has obviously not been designed to write complete database applications.
That's why I started to write Lino.
Lino is an alternative for Django's :mod:`django.contrib.admin` module.

One of Lino's design goals is to keep a maximum of application 
logic independant of your choice of user interface.
Lino currently provides only one user interface, 
which itself makes extensive use of :term:ExtJS.
This is because at the moment I am just satisfied with ExtJS.
But it is possible to write other interfaces in the future. 
I can imagine simple HTML, curses, Qt, ...


How I'd explain Lino to Django users
------------------------------------

Lino sites are normal Django sites, but 
your :setting:`INSTALLED_APPS` will 
usually contain applications designed to use Lino.

Lino comes with a collection of such Django applications (:mod:`lino.modlib`).

With Lino you don't need to write any `urls.py`, you don't even need to 
set :setting:`ROOT_URLCONF` in your :xfile:`settings.py` if you use the 
default settings by starting your :xfile:`settings.py` with::

  from lino.demos.std.settings import *
  
You also don't need to write any :file:`.html` templates when using Lino.


Writing your own Lino applications
----------------------------------

Lino applications are basically normal Django applications, but 
instead of writing `Admin` classes for your Django models, you write Reports 
(subclasses of :class:`lino.reports.Report`)
that are located in your application's 'models' module.
A Report describes a collection of tabular data : title, columns, model, queryset.

You will also define Layouts for your detail forms.

A Layout describes an entry form in a GUI-independent way.
Users see them as Tabs of a Detail window (whose main component is a 
`FormPanel <http://www.extjs.com/deploy/dev/examples/form/xml-form.html>`)

Instead of having each application register its models to the admin site, 
you write a main menu for your site that uses your Reports. 
This is is currently done in a file :xfile:`lino_settings.py`, 
usually in the same directory as Django's :xfile:`settings.py`.
This approach is less pluggable than Admin-based applications, 
but enterprise solutions don't need to be plug and play.


