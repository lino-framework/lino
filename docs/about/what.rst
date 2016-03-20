=============
What is Lino?
=============

Lino is a high-level framework for writing :doc:`desktop-like
<desktop>` :doc:`customized <customized>` database applications.

Lino applications are based on `Django
<https://www.djangoproject.com/>`_ and `Sencha ExtJS
<http://www.sencha.com/products/extjs/>`_: technically they are Django
projects with an out-of-the box user interface.  For example you don't
not need to write any URLconf, HTML, CSS nor Javascript.  More about
this in :doc:`lino_and_django`.

Advantages: everything gets much easier: writing a prototype, changing
database structures and business logic, long-term maintenance,
documentation.  More in :doc:`why`.

Disadvantage: you are limited to applications that fit into this
out-of-the box user interface.  More in :doc:`limitations`.



Target users
============

Lino is designed to be used by professional developers who write and
maintain a customized database application, either for internal use by
themselves or their employer, or for internal use by their customer,
or for public use as a service to their customers.

The growing collection of :ref:`lino.projects` is meant to be used by
service providers who offer professional hosting of one of these
applications.


Target applications
===================

Typical Lino applications have a rather **complex database
structure**.  For example Lino Welfare has 155 models in 65 plugins.
Even Lino Noi (the smallest Lino application which is being used on a
production site) has 44 models in 32 plugins.

