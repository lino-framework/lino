About Lino
==========

What is Lino?
-------------

Lino is a framework for creating customized enterprise-level 
Rich Internet Applications 
using `Sencha ExtJS <http://www.sencha.com/products/extjs/>`_
and `Django <https://www.djangoproject.com/>`_.

This website is for professional Python developers who
want to develop Lino applications for their customers.
Primary target customers for Lino applications 
are agencies and companies who 
need a customized database application.



Design goals
------------

- agile programming
- rapid prototyping 
- libraries of reusable code
- short release cycles
- maintainable code
- stable 


Lino and Django
---------------

Lino explained to Django users:

- Lino sites are Django projects. Lino depends on Django. 
  You need to install Django before you can use Lino.
- Lino provides an out-of-the box user interface. 
  Application developers don't write HTML templates.
- Lino works by adding a setting ``LINO`` to your 
  :xfile:`settings.py`, which is an 
  instance of :class:`lino.Lino`.
- Lino replaces Django's
  ``django.contrib.admin`` and 
  ``django.contrib.auth`` modules by its own methods.


Features
--------
    
- :doc:`/topics/layouts`
- :doc:`/topics/babel`
- :doc:`/topics/datamig`
- :doc:`/topics/mti`
- :doc:`/topics/perms`
- :doc:`/topics/workflow`

The user interface
------------------

People tend to judge a framework by it's user interface (UI). 
This approach is not completely wrong since the UI is the 
first "visible" part.

Lino is designed to have many possible user interfaces,
but your choice is currently limited to the :term:`ExtJS` UI.
This means that Lino applications currently always 
"look like" those you can see at :doc:`/demos`.

We started working on a first alternative user interface 
that uses the :doc:`Qooxdoo library </topics/qooxdoo>`,
and we can imagine to write other interfaces in the future 
(simple HTML, curses, Qt, ...), but for the moment 
Lino relies on ExtJS, because ExtJS is so cool, 
and because writing and optimizing a user interface 
is a rather boring work, 
and because there are many other, 
more interesting tasks that are waiting to be done.


History
-------

Luc Saffre, the author of Lino, is also the author of :term:`TIM`, 
a DOS-based framework for writing database applications for small enterprises. 
Lino is a successor for TIM.
TIM is over 15 years old, but Luc continues to live from maintaining 
it and giving professional support to its users. 
TIM users have relatively wide-spread profiles, 
ranging from the independant craftsman who writes 50 invoices per year 
to the government agency with 30 users and hundreds of documents per day.

Luc has been working on writing a successor for TIM **since the early 1990s**.
He has done and dropped projects in C++, PHP and Java. 
Since **August 2004** he's mostly working in Python. 
In **March 2009** he discovered :term:`Django` whose database model and application 
server concepts seem ideal for Lino. 
In **August 2009** he started to use the :term:`ExtJS` Javascript framework.

The first real-world Lino application started 
in a Belgian *Public Centre for Social Welfare* 
(PCSW) in **January 2011**.
In **August 2012** we forked it into a separate project 
`Lino-Welfare <http://welfare.lino-framework.org>`_
to be maintained by an independant organization.

In September 2012 we purchased the domain name `lino-framework.org`.

In December 2012 we 
`announced 
<http://blog.lino-framework.org/2012/12/belgian-accounting-made-simple.html>`_
a first prototype of `Lino Così`.



.. toctree::
   :maxdepth: 1
   
   license
   why_gpl
   thanks
   compared
   lino_and_django
   why_extjs
