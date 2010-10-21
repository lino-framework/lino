About Lino
==========

Lino is a framework for writing enterprise-level database applications, 
using :term:`Django's <Django>` database model and application server behind the scenes,
and the :term:`ExtJS` Javascript library to provide a modern user interface.

One of Lino's design goals is to keep a maximum of application 
logic independant of your choice of user interface.

Lino currently provides only one user interface (:mod:`lino.ui.extjs`),
but we can imagine to write other interfaces in the future 
(simple HTML, curses, Qt, ...).
For the moment we are just satisfied with ExtJS.

Lino has no users yet, but we are currently working on getting 
it started on a site in Belgium. 
We hope for success until the end of 2010.

Don't hesitate to contact the author:

  | E-mail: luc *dot* saffre *at* gmail *dot* com
  | Skype: lsaffre

History
-------

Luc Saffre, the author of Lino, is also the author of :term:`TIM`, 
a DOS-based framework for writing database applications for small enterprises. 
TIM is over 15 years old, but Luc lives from maintaining 
it and giving support to its users. 

TIM users have relatively wide-spread profiles, 
ranging from the independant craftsman who writes 50 invoices per year 
to the government agency with 30 users and hundreds of documents per day.

Luc has been working on writing a successor for TIM since the early 1990s. He has done and dropped projects in C++, PHP and Java. Since August 2004 he's doing this using Python. In March 2009 he discovered :term:`Django` whose database model and application server concepts seem ideal for Lino. In August 2009 he started to use the ExtJS Javascript framework.

When Luc discovered Django in the end of 2008, he was quickly seized by
the clear design and mature implementation. "The ORM and database model based on *applications* is simply genial.
The way of how this is integrated into a web application server system: genial."
But one thing disturbed me: the 
`admin application <http://docs.djangoproject.com/en/dev/ref/contrib/admin/#ref-contrib-admin>`_  
has obviously not been designed to write complete database applications.
That's why I started to write Lino.
Lino is an alternative for Django's :mod:`django.contrib.admin` module."


Lino explained to Django users
------------------------------

Lino sites are normal Django sites, but 
your :setting:`INSTALLED_APPS` will 
usually contain applications designed to use Lino.

Lino comes with a collection of such Django applications (:mod:`lino.modlib`).

With Lino you don't need to write any `urls.py`, you don't even need to 
set :setting:`ROOT_URLCONF` in your :xfile:`settings.py` if you use the 
default settings by starting your :xfile:`settings.py` with::

  from lino.demos.std.settings import *
  
You also don't need to write any :file:`.html` templates when using Lino.





.. toctree::
   :maxdepth: 1
   
   why_gpl
   why_extjs
