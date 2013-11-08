Lino is not Django
==================

When I discovered Django in the end of 2008, after having worked 
many months on my own database model, I was quickly fascinated.
The ORM and database model based on 'apps' is simply genial.
The way of how this is integrated into a web application server system: genial.
But one thing disturbed me: the 
`admin interface <http://docs.djangoproject.com/en/dev/ref/contrib/admin/#ref-contrib-admin>`_  
has obviously not been designed to write complete database applications.
That's why I started to write Lino.
Lino is an alternative for Django's `django.contrib.admin` module.

The decision of *not using* some part of an established framework 
of course needs some audacity (or foolishness if you prefer), 
and I beg your pardon for daring to explain my decisions here.

.. include:: /include/tellme.rst


- Lino is a replacement for `django.contrib.admin`.

  I believe that `django.contrib.admin`
  is not a usable base for representing a desktop-style application.
  For example it lets you define only one ModelAdmin per Model.
  
- Lino also replaces `django.contrib.auth` by :mod:`lino.modlib.users`.
  I believe that `django.contrib.auth`
  is not suitable for defining and maintaining complex permission 
  systems because it lacks the concepts of user roles and functional 
  groups.
  
- Lino doesn't use `django.forms` which is somehow "hooked into the 
  wrong place" and forces application developers to write redundant 
  code.
  
- Lino suggests (but doesn't enfore) to use :ref:`north` 
  migrations instead of Django's default `Migrations
  <https://docs.djangoproject.com/en/dev/topics/migrations/>`_ 
  system.
  
- Lino prefers Jinja2 templates over the 
  `default Django engine <https://docs.djangoproject.com/en/dev/topics/templates/>`_
  to generate its own stuff.  
  For the plain Django part of your application you can use 
  the system of your choice.

