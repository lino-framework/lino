.. _lino.tutorial.watch:

Watching database changes
-------------------------

This tutorial explains how to 
implement a kind of `audit trail <https://en.wikipedia.org/wiki/Audit_trail>`_.
using the :mod:`lino.modlib.changes` 
app for logging changes to individual rows of database tables.

To enable database change watching, you add :mod:`lino.modlib.changes` 
to your :setting:`INSTALLED_APPS` 
and then 
register "change watchers" for every type of change you want to watch.

You will also want to make your changes visible for users by adding 
the `ChangesByOwner` slave table to some detail layout.

The example in this tutorial uses the 
:mod:`lino.modlib.contacts` module for convenience.
It also adds a model `Entry` (imagine some journal entry to be audited) 
as an example of a watched model.

The "master" of a change watcher is the object to which every Change 
should be attributed.
In this example, every change to *Entry*, *Partner* **or** *Company* will be 
logged and attributed to (i.e. visible from) their *Partner* record.


We define our own subclass of `Site` for this tutorial 
(which is the recommended way except for very simple examples).

Here is the settings.py file:

.. literalinclude:: settings.py


We need to redefine the default list of user profiles.
by overriding :setting:`setup_choicelists` 
because `contacts` adds a user group "office", 
required to see most commands.

The :setting:`get_installed_apps` shows that 
:mod:`lino.modlib.changes` depends on the following apps:
:mod:`lino.modlib.users`, 
:mod:`lino.modlib.system` and
:mod:`django.contrib.contenttypes`.
Application developers currently need to specify these themselves.

Here is our :mod:`models` 
module  which defines the Entry model
and some few startup event listeners:

.. literalinclude:: models.py

You can play with this application by cloning the latest development 
version of Lino, then ``cd`` to the :file:`/docs/tutorials/watch_tutorial` 
directory where you can run::

    $ python manage.py initdb_demo
    $ mkdir media 
    $ python manage.py runserver

