Lino is not Django
==================

The decision of *not using* some part of an established framework 
of course needs some audacity, foolishness, self-confidence or however 
you might call it.

Lino replaces some important Django components by its own system,
and on this page I try to explain these design decisions.

- `django.contrib.admin`
  is not usable to represent a desktop-style application
  because it lets you define only one ModelAdmin per Model.
  
- `django.contrib.auth` is not suitable to define 
  and maintain complex permission systems because it lacks the 
  concepts of user roles and functional groups.
  
- `django.forms` is somehow hooked into the wrong place. 
  It forces application developers to write redundant code.
  
- Lino prefers Jinja2 templates over the default Django engine 
  to generate its own stuff.  
  For the plain Django part of your application you can use 
  the system of your choice.

