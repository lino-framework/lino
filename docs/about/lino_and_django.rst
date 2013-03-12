Lino and Django
===============

Lino sites are Django projects. Lino depends on Django. 
You need to install Django before you can use Lino.
  
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

Unlike Django, Lino provides an out-of-the box user interface. 
Application developers don't need to write 
a single line of HTML, CSS, Javascript or URL configuration. 

Lino replaces some important Django components by its own system:

- `django.contrib.admin`
  is not usable to represent a desktop-style application
  because it lets you define only one ModelAdmin per Model.
  
- `django.contrib.auth` is not suitable to define 
  and maintain complex permission systems because it lacks the 
  concepts of user roles and functional groups.
  
None of the above are absolute truths,
I just try to formulate the beliefs behind my design decisions.
  
Lino prefers Jinja2 templates over the default Django engine 
to generate its own stuff.
For the plain Django part of your application you can use 
the system of your choice.

