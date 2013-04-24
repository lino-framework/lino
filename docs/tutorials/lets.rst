.. _lino.tutorial.lets:

A Local Exchange Trade System
=============================

This tutorial supposes that you followed :ref:`lino.tutorial.polls`.

In this tutorial we are going to leave Django's 
polls and write a new application.
It is an application to manage a 
Local Exchange Trade System 
(`LETS <http://en.wikipedia.org/wiki/Local_exchange_trading_system>`_),
inspired by a real web site http://www.elavtoit.com

Imagine that after having interviewed your future customer and 
analyzed their needs, you want to show a "first draft" prototype.
The goal of such a prototype is to have something 
to show to your customer that looks a little bit like 
the final product, and with wich you can play to test 
whether your analysis of the database structure is okay.

The code for such a first draft is in 
:srcref:`/lino/tutorials/lets1`.

Please explore these files and and copy 
them to a local project directory 
The directory structure should be as follows:
 
=================================================================== =========================
:file:`__init__.py`                                                 (empty file)
:srcref:`settings.py </lino/tutorials/lets1/settings.py>`           contains the main menu and other application settings
:srcref:`manage.py </lino/tutorials/lets1/manage.py>`               (you may need to adapt this so that it sets a correct value for `DJANGO_SETTINGS_MODULE`)
:file:`lets/__init__.py`                                            (empty file)
:srcref:`lets/models.py </lino/tutorials/lets1/lets/models.py>`     defines the database models
:file:`fixtures/__init__.py`                                        (empty file)
:srcref:`fixtures/demo.py </lino/tutorials/lets1/fixtures/demo.py>` defines demo data
=================================================================== =========================

To get the prototype running, first run the following command 
to populate your database with some demo data::

  python manage.py initdb_demo
  
  
Then start the development web server using::

  python manage.py runserver

And point your browser to http://127.0.0.1:8000/

Here are some screenshots.

.. image:: t3a-1.jpg
    :scale: 70
    
.. image:: t3a-2.jpg
    :scale: 70
    
.. image:: t3a-3.jpg
    :scale: 70

