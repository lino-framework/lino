Lino Django Utilities
=====================


:mod:`lino.django.utils` 
is a framework to write 
`Django <http://docs.djangoproject.com>`_ applications.

It enables you to get a functional web application using the Django
models database. It can be considered an alternative to Django's 
admin interface, with some fundamental differences: 

- Instead of writing :class:`Admin` classes for your models, 
  you write :class:`Report` and :class:`Layout` classes.
  
- Layouts are a unique new approch to design entry forms
  without having to fiddle with templates.
  
- Instead of registering your models to the admin site,
  you install your reports into the Lino site's main menu.  

When I discovered Django, I was amazed by the clear design and mature
implementation, but one piece of the puzzle was missing: 
when writing a web interface for multi-user database applications,
Django's `admin site <http://docs.djangoproject.com/en/dev/ref/contrib/admin/#ref-contrib-admin>`_ 
wants me to define my application's behaviour 
from "inside" the database models.
This approach seemed to me like climbing a tree with your legs 
bound together.

Lino's new approach removes the sling from your legs:
the metadata and application logic becomes a layer 
around the database logic instead of sitting inside the models.

The disadvantage of Lino's approach is that it is not ready 
for use in a production environment.

Applications that use lino.django.utils:

.. toctree::
   :maxdepth: 2

   igen/index




