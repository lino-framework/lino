Lino and Django
---------------

**Summary**

- Lino sites are Django projects. Lino depends on Django. 
  You need to install Django before you can use Lino.
  Technically speaking:
  Lino just adds a setting ``LINO`` to your 
  :xfile:`settings.py`, which is an 
  instance of :class:`lino.Lino`.
  
  
  
- Lino provides an out-of-the box user interface. 
  Application developers don't write HTML templates and 
  don't reinvent their own URL structure.
  
- Lino replaces some important Django components 
  by its own:
  ``django.contrib.admin``,
  ``django.forms`` 
  and 
  ``django.contrib.auth``.



When Luc discovered Django in the end of 2008, he was quickly seized by
the great ideas behind Django and the mature implementation. 
He wrote:

  "The ORM and database model based on *applications* is simply genial.
  The way of how this is integrated into a web application server system: genial.
  But one thing disturbed me: the 
  `admin application <http://docs.djangoproject.com/en/dev/ref/contrib/admin/#ref-contrib-admin>`_  
  has obviously not been designed to write complete database applications.
  That's why I started to write Lino.
  Lino is an alternative for Django's `django.contrib.admin` module."

Unlike a Django application developer, 
a Lino application developer doesn't write a single 
line of HTML, CSS or Javascript. 



Why I don't use certain parts of Django
---------------------------------------

None of the following are absolute truths. I just try to explain 
my design decisions. I maybe missed certain things and 
invite you to explain my what they are or to ask more concrete 
questions.

`django.contrib.admin`
----------------------


- Django lets your define only one ModelAdmin per Model, and Admin is 
  not usable to representat a desktop-style application.
- `django.contrib.auth` is not usable to define (and maintain) complex
  permission systems.
  