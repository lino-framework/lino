.. _lino.tutorial.polls:

The Lino Polls tutorial 
=======================

In this tutorial we are going to take the "Polls" application from
Django's tutorial and turn it into a Lino application.

.. currentmodule:: lino.core.site

.. contents:: Table of Contents
 :local:
 :depth: 2


Create a local Django project
-----------------------------

Before reading on, please follow Part 1 of the Django tutorial.  Lino
is just a set of extensions for a Django project, so there is a lot of
Django know-how which applies entirely for a Lino application.

There we go: 

  `Writing your first Django app, part 1
  <https://docs.djangoproject.com/en/1.6/intro/tutorial01/>`_.  

Just part 1, not the whole tutorial.  Afterwards we meet here again.
See you later!  And don't panic if you read the warning "This document
is for an insecure version of Django that is no longer
supported. Please upgrade to a newer release!" (when your first
application is ready for production, we will have updated Lino to play
with newer Django versions).

Done? Okay, here we continue.

You have now a set of files in your "project directory"::

    mysite/
        manage.py
        mysite/
            __init__.py
            settings.py
            urls.py
            wsgi.py
        polls/
            __init__.py
            admin.py
            models.py
            tests.py
            views.py


The Django tutorial continues (in part 2) by introducing Django's
**Admin** module to create a web interface.  We now leave the Django
philosophy and continue "the Lino way" of defining our application's
web interface.  Lino is an alternative to Django's Admin module.

Most files remain unchanged, they are the same as with every Django project:
:xfile:`__init__.py`, :xfile:`manage.py`,
:xfile:`urls.py`, :xfile:`views.py` and :xfile:`wsgi.py`.

But we are now going to modify the files 
:file:`mysite/settings.py` and
:file:`polls/models.py`.

The :file:`settings.py` file
-----------------------------

Lino uses some tricks to make :ref:`Django settings <settings>` more
pleasant to work with, especially if you maintain Lino sites for
several customers. We will come back to this later.  For the moment
just change the contents of your :xfile:`settings.py` to the
following:

.. literalinclude:: settings.py

A few explanations:

#.  A Lino :xfile:`settings.py` file always defines (or imports) a
    **class** named ``Site`` and then **instantiates** this class into
    a variable named ``SITE``. Our example also **overrides** the
    class before instantiating it.

#.  In Lino you don't code your :setting:`INSTALLED_APPS` directly
    into your :xfile:`settings.py` file, you override your Site's
    :meth:`get_installed_apps
    <lino.core.site.Site.get_installed_apps>` method.  Our example
    does the equivalent of ``INSTALLED_APPS = ['polls']``, except for
    the fact that Lino automagically adds some more apps.
    
#.  The **main menu** of a Lino application is defined in
    :meth:`setup_main_menu <lino.core.site.Site.setup_main_menu>`
    method.
    
More about all this in :doc:`/dev/settings` and :doc:`/dev/site`

If you are curious:

    One of the Django settings managed by Lino is
    :setting:`INSTALLED_APPS`. You probably have been wondering why we
    removed it from our :xfile:`settings.py`. Actually it *is* being
    defined, but automatically and behind the scenes.
    Let's be curious and have a look at them.  Open a Django shell in your
    project directory::

      $ python manage.py shell

    And then enter the following Python instructions there:  

    >>> from pprint import pprint
    >>> from django.conf import settings
    >>> pprint(settings.INSTALLED_APPS)
    ('django.contrib.staticfiles',
     'lino.modlib.about',
     'lino.modlib.extjs',
     'lino.modlib.jinja',
     'lino.modlib.bootstrap3',
     'lino.modlib.lino',
     'polls')

    At the moment you don't need to worry about those additional "system"
    apps, you can just trust Lino that he will fill into
    :setting:`INSTALLED_APPS` what is needed.


The :file:`models.py` file
--------------------------

- Change the contents of your :xfile:`polls/models.py` to the
  following:

.. literalinclude:: ../polls/models.py

A few explanations while looking at that file:

- The :mod:`lino.dd` module is a shortcut to most Lino extensions 
  used by application programmers in their `models.py` modules. 
  `dd` stands for "data design".
  
- :class:`dd.Model <lino.core.model.Model>` is an optional (but
  recommended) wrapper around Django's Model class.  For this tutorial
  you could use Django's `models.Model` as well, but we recommend to
  use :class:`dd.Model <lino.core.model.Model>`.

- There's one **custom action** in our application, defined as the
  `vote` method on the `Choice` model, using the :func:`dd.action
  <lino.core.actions.action>` decorator. More about actions in the
  Actions_ section.

The last line imports everything from a new file you should create
now: the :file:`ui.py` file.


The :file:`ui.py` file
----------------------

- :class:`dd.Table <lino.core.dbtables.Table>` is used as base class
  for the three **Table** definitions in our application.  That's an
  important new concept in Lino, and we'll talk about it soon in the
  Tables_ section.

  
  
Changing the database structure
-------------------------------

One more thing before seeing a result.  We made at least one change in
our :xfile:`models.py` file after the Django tutorial: we added the
`hidden` field of a Poll::

    hidden = models.BooleanField(
        "Hidden",
        help_text="Whether this poll should not be shown in the main window.",
        default=False)

To be more precise: Django and Lino "know" that we added a field named
`hidden` in the `Polls` table of our database, **but** the database
doesn't yet know it.  If you would run your application now, then you
would get some "operational" database error because Lino would ask the
database to read or update this field, and the database would answer
that there is no field named "hidden".  We must tell our database that
the structure has changed.

For the moment we are just going to *reinitialize* our database,
i.e. *delete* any data you may have manually entered during the Django
Polls tutorial and turn the database into a virgin state::

    $ python manage.py initdb

The output should be::

      Creating tables ...
      Installing custom SQL ...
      Installing indexes ...

..
  >>> from django.core.management import call_command
  >>> call_command('initdb', interactive=False)
  Creating tables ...
  Installing custom SQL ...
  Installing indexes ...
    

Adding a demo fixture
---------------------

This section is optional and recommended in case you were frustrated
when we deleted the data you had manually entered during the Django
Polls tutorial.

When you are developing and maintaining a database application, it
happens very often that you need to change the database structure.

Instead of manually filling your demo data again and again after every
database change, you write it once as a *fixture*.

With Lino it is easy and fun to write demo fixtures because you can
write them in Python.  Read more about them in
:ref:`lino.tutorial.dpy`, or simply stay here and learn by doing.

We are now going to add a **demo fixture**.

- Create a directory named :file:`fixtures` in your :file:`polls`
  directory.

- Create an empty file named :xfile:`__init__.py` in that directory.

- Still in the same directory, create another file named ``demo.py``
  with the following content:

  .. literalinclude:: ../polls/fixtures/demo1.py

- If you prefer, the following code does exactly the same but has the
  advantage of being more easy to maintain:

  .. literalinclude:: ../polls/fixtures/demo.py

- Run the following command (from your project directory) 
  to install these fixtures::

    python manage.py initdb demo

  The output should be::

      Creating tables ...
      Installing custom SQL ...
      Installing indexes ...
      Installed 13 object(s) from 1 fixture(s)

..
  >>> from django.core.management import call_command
  >>> call_command('initdb', 'demo', interactive=False)
  Creating tables ...
  Installing custom SQL ...
  Installing indexes ...
  Installed 13 object(s) from 1 fixture(s)
    
  
Starting the web interface
--------------------------

Now we are ready to start the development web server on our project::

  $ cd ~/mypy/mysite
  $ python manage.py runserver
  
or (on Windows)::

  c:\mypy\mysite> python manage.py runserver
  
and point your browser to http://127.0.0.1:8000/ 
to see your first Lino application running.

- Please play around and create some polls before reading on.



The main index
--------------
  
The following template is used to build the HTML to be displayed in
our Main Window.

Create a directory named ``config`` under your project directory, and
in that directory create a file named `admin_main.html` with the
following content:

.. literalinclude:: config/admin_main.html

Explanations:

- ``<div class="htmlText">`` specifies that this fragment 
  contains simple html text inside an ExtJS component. 
  This is required because ExtJS does a lot of CSS magic which 
  neutralizes the "usual" effects of most html tags.

    
- ``site.modules`` : Every Lino site has an instance attribute ``modules``
  which is a shortcut to access the models and tables of the application.
  Usually it is better to write
  
  ::

    Poll = site.modules.polls.Poll

  instead of
  
  ::

    from site.modules.polls.models import Poll
  
  because the latter hard-wires the location of the `polls` app.
    
- If `objects`, `filter()` and `order_by()` are new to you, 
  then please read the `Making queries 
  <https://docs.djangoproject.com/en/dev/topics/db/queries>`_
  chapter of Django's documentation. 
  Lino is based on Django, and Django is known for its good documentation. Use it!

- If `joiner` and `sep` are a riddle to you, you'll find the 
  solution in Jinja's `Template Designer 
  Documentation <http://jinja.pocoo.org/docs/templates/#joiner>`__.
  Lino applications by default replace Django's template engine by Jinja.

- ``obj.vote`` is an :class:`InstanceAction <lino.core.actions.InstanceAction>`,
  and we call its 
  :meth:`as_button <lino.core.actions.InstanceAction.as_button>`
  method
  which returns a HTML fragment that displays a button-like 
  link which will run the action when clicked.
  More about this in Actions_.




Screenshots
-----------

Make sure that you understand and can reproduce 
the concepts explained in this section.


The **Main Window** is the top-level window of your application:

.. image:: polls1.jpg
    :scale: 50
    
Your application specifies what to put there, and there are several 
methods to do this.
If you don't want to use an `admin_main.html` template
you may override the
:meth:`get_main_html <lino.lino_site.Site.get_main_html>` method 
which returns a chunk of generated html.
    
After clicking on a vote, here is the `vote` method 
of our `Choice` model in action:

.. image:: polls2.jpg
    :scale: 50
    
    
After selecting :menuselection:`Polls --> Polls` in the main menu, 
Lino opens that table in a **Grid Window**:
    
.. image:: polls3.jpg
    :scale: 50
    
Every table can be displayed in a **Grid Window**, a tabular 
representation with common functionality such as sorting, 
setting column filters, editing individual cells, 
and a context menu.
  
After double-clicking on a row in the previous screen, Lino shows 
the **Detail Window** on that Poll:

.. image:: polls4.jpg
    :scale: 50
    
This window has been designed by the following code in 
your :file:`models.py` file::

    detail_layout = """
    id question 
    hidden pub_date
    ChoicesByPoll
    """

To add a Detail Window to a table, you simply add a
:attr:`detail_layout <lino.core.actors.Actor.detail_layout>` attribute to the
Table's class definition.
    
Not all tables have a Detail Window.  In our case the `Polls` table
has one, but the `Choices` and `ChoicesByPoll` tables don't.
Double-clicking on a cell of a Poll will open the Detail Window, but
double-clicking on a cell of a Choice will start cell editing.  Note
that can still edit an individual cell of a Poll in a Grid Window by
pressing the :kbd:`F2` key.
  
After clicking the :guilabel:`New` button, you can admire 
an **Insert Window**:

.. image:: polls5.jpg
    :scale: 50
    
This one exists because Polls has the following 
:attr:`insert_layout <lino.core.actors.Actor.insert_layout>` attribute:: 

    insert_layout = dd.FormLayout("""
    question
    hidden
    """,window_size=(40,'auto'))
    
(Again: see :doc:`/tutorials/layouts` for more explanations.)

After clicking the :guilabel:`[html]` button:

.. image:: polls6.jpg
    :scale: 50
    
The :guilabel:`[pdf]` button works only if you have 
an OpenOffice or LibreOffice server running in 
background (don't worry about that for the moment).
    
.. image:: polls7.jpg
    :scale: 50


Tables
------

A Table is the "abstract" definition of a tabular view.
It is not only used for the Grid Window but also to implement 
the :guilabel:`[html]` and :guilabel:`[pdf]` views.

A Table definition has attributes like `filter` and `sort_order` which
you know from Django's QuerySet.

But it also has Lino-specific attributes like 
:attr:`column_names <dd.AbstractTable.column_names>`,
:attr:`detail_layout <lino.core.actors.Actor.detail_layout>` 
or
:attr:`parameters <lino.core.actors.Actor.parameters>`.

To define Tables, you simply need to declare their classes.
Tables never get instantiated.
Lino discovers and analyzes them when it initializes.

Each Table class must have at least one class attribute 
`model` defined. This points to the Model on which this 
table will "work".

There are a lot of other options for tables, 
and a consistent overview has yet to be written.
But you can try to work through the API docs, 
knowing that
:class:`dd.Table` 
inherits from
:class:`dd.AbstractTable` 
who inherits from
:class:`lino.core.actors.Actor`.

Since tables are normal Python classes 
they can use inheritance.
In our code `ChoicesByPoll` inherits from `Choices`. 
That's why we don't need to explicitly specify 
a `model` attribute for `ChoicesByPoll`.

`ChoicesByPoll` is an example of a **slave table**.
`ChoicesByPoll` means: the table of `Choices` of a given `Poll`. 
This given Poll is called the "master" of these Choices.
We also say that a slave table *depends* on its master.

Lino manages this dependency almost automatically.  The application
developer just needs to specify a class attribute :attr:`master_key
<dd.Table.master_key>`.  This is attribute, when set, must be a string
containing the name of a `ForeignKey` field which must exist in the
Table's model.

Note that you can define more than one Table per Model.  This is a
fundamental difference from Django's concept of the `ModelAdmin` class
and `Model._meta` options.


Actions
-------

Lino has a class :class:`Action <lino.core.actions.Action>` 
which represents the methods who have a clickable button 
or menu item in the user interface. 

Each :class:`Action <lino.core.actions.Action>` instance holds a few important pieces
of information:

- label : the text to place on the button or menu item
- help_text : the text to appear as tooltip when the mouse is over that button
- permission requirements : specify for whom and under which
  conditions this action is available (a complex subject, we'll talk
  about it in a later tutorial)
- handler function : the function to execute when the action is invoked

Many actions are created automatically by Lino. For example:

- each table has a "default action" which is 
  to open a window which displays this table as a grid.
  That's why (in the :meth:`setup_main_menu <dd.Site.setup_main_menu>`
  function of your :file:`polls/models.py`) you can say::

    def setup_main_menu(site, ui, profile, main):
        m = main.add_menu("polls", "Polls")
        m.add_action('polls.Polls')
        m.add_action('polls.Choices')


  The :meth:`add_action <lino.core.menus.Menu.add_action>` method of Lino's 
  :class:`lino.core.menus.Menu` is smart enough to understand that if you 
  specify a Table, you mean in fact that table's default action.

- The :guilabel:`Save`, :guilabel:`Delete` and :guilabel:`New` buttons
  in the bottom toolbar of the Detail window have their own
  :class:`Action <lino.core.actions.Action>` instance.
  
Custom actions are the actions defined by the application developer.
Our tutorial has one of them:

.. code-block:: python

    @dd.action(help_text="Click here to vote this.")
    def vote(self, ar):
        def yes(ar):
            self.votes += 1
            self.save()
            return ar.success(
                "Thank you for voting %s" % self,
                "Voted!", refresh=True)
        if self.votes > 0:
            msg = "%s has already %d votes!" % (self, self.votes)
            msg += "\nDo you still want to vote for it?"
            return ar.confirm(yes, msg)
        return yes(ar)

The :func:`@dd.action <dd.action>` decorator can have keyword
parameters to specify information about the action. In practice these
may be :attr:`label <lino.core.actions.Action.label>`, :attr:`help_text
<lino.core.actions.Action.help_text>` and :attr:`required <lino.core.actions.Action.required>`.

The action method itself should have the following signature::

    def vote(self, ar, **kw):
        ...
        return ar.success(kw)
        
Where ``ar`` is an :class:`rt.ar` instance that holds
information about the web request and provides methods like

- :meth:`callback <rt.ar.callback>` 
  and :meth:`confirm <rt.ar.confirm>`
  lets you define a dialog with the user using callbacks.

- :meth:`success <rt.ar.success>` and
  :meth:`error <rt.ar.error>` are possible return values
  where you can ask the client to do certain things.



Summary
-------

In this tutorial we followed Part 1 of the Django Tutorial, 
then continued the Lino way and explained two important new Lino concepts: 
Tables and Actions

The result of this tutorial is available as a public 
live demo at http://demo1.lino-framework.org




