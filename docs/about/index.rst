About Lino
==========

Lino is a framework for creating enterprise-level 
Rich Internet Applications that use :term:`Django's <Django>`
database model combined with an out-of-the box user interface.

Lino is still young: 
there's only one real-world Lino application, 
running on a non-public site in Eupen since January 2011.
Our goal is to write at least two other applications 
until the end of 2011.

Some of Lino's features:

- Designed for rapid prototyping and shord release cycles.
- A solution for :doc:`/topics/datamig`
- A solution for :doc:`ui transparent form design </topics/dtl>`
- A solution for :doc:`multilingual database content </topics/babel>`

Luc Saffre, the author of Lino, is also the author of :term:`TIM`, 
a DOS-based framework for writing database applications for small enterprises. 
Lino is a successor for TIM.
TIM is over 15 years old, but Luc continues to live from maintaining 
it and giving support to its users. 
TIM users have relatively wide-spread profiles, 
ranging from the independant craftsman who writes 50 invoices per year 
to the government agency with 30 users and hundreds of documents per day.


History
-------

Luc has been working on writing a successor for TIM since the early 1990s. 
He has done and dropped projects in C++, PHP and Java. 
Since August 2004 he's mostly working in Python. 
In March 2009 he discovered :term:`Django` whose database model and application 
server concepts seem ideal for Lino. 
In August 2009 he started to use the ExtJS Javascript framework.
Since January 2011 a first Lino application is being 
used on a real (non-public) site.

Lino explained to Django users
------------------------------

When Luc discovered Django in the end of 2008, he was quickly seized by
the clear design and mature implementation. Some of his statements:
"The ORM and database model based on *applications* is simply genial.
The way of how this is integrated into a web application server system: genial.
But one thing disturbed me: the 
`admin application <http://docs.djangoproject.com/en/dev/ref/contrib/admin/#ref-contrib-admin>`_  
has obviously not been designed to write complete database applications.
That's why I started to write Lino.
Lino is an alternative for Django's `django.contrib.admin` module."

Unlike Django developers, 
a Lino application developer doesn't write a single 
line of HTML, CSS or Javascript. 
Since Lino is young, your choice is currently limited 
to the :term:`ExtJS` UI.
Although we are satisfied with ExtJS, 
we also started working on a first alternative user interface 
which  will be using the :doc:`Qooxdoo library </topics/qooxdoo>`.
And we can imagine to write other interfaces in the future 
(simple HTML, curses, Qt, ...).



See also :doc:`/tutorials/t1`


.. toctree::
   :maxdepth: 1
   
   why_gpl
   why_extjs
