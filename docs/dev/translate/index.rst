============================
Instructions for translators
============================

Here is how your can help translating Lino into your own language.

Preliminaries
-------------

We suppose that you have installed the *development version* (not a
released version from PyPI) for both Lino and the application you want
to translate.  We suppose that :ref:`cosi` is the application you want
to translate, and that you have installed it as explained in
:ref:`cosi.install`.  And let's say for example that you want to
translate them to *Spanish*.


Overview
--------

You are going to edit a series of :xfile:`.po` files which are part of
the code repositories of both Lino and :ref:`cosi`.  

To edit these :xfile:`.po` files you will be using either your
preferred plain text editor or a tool like Poedit_.  We recommend the
latter. On Debian you install it with ``apt-get install poedit``.

.. _Poedit: http://www.poedit.net

When you are satisfied with your work, you will make a pull request to
ask me to integrate your changes into the public repositories of Lino
and :ref:`cosi`.
More about pull requests:

- http://git-scm.com/book/en/Distributed-Git-Contributing-to-a-Project
- https://help.github.com/articles/creating-a-pull-request

Note about copyright: you will be contributing your :file:`.po` files
to Lino. These files are *per definitionem* your spiritual property.
You express this by writing your name and email address to the headers
of these :file:`.po` files (Poedit_ does this for you if you fill your
preferences correctly). By contributing your work to the Lino project,
you implicitly declare that you give us the permission to publish your
work together with Lino under the LGPL.

Instructions
------------

Go to your copy of the :ref:`cosi` repository::

  $ cd ~/mysite

Change your project's :xfile:`settings.py` file once more so that it
looks as follows:

.. literalinclude:: settings.py

Initialize the demo database::

  $ python manage.py initdb_demo

Run the development server on the demo database::

  $ python manage.py runserver

Point your browser to view the application. Log in as the Spanish user.

.. image:: translate_1.png
  :scale: 80

The translatable strings on this page (`gettext` and Poedit_ call them
"messages" ) are for exampe the menu labels ("Contacts", "Producs"
etc), but also content texts like "Welcome", "Hi, Rodrigo!" or "This
is a Lino demo site."

Now you must locate these strings in the :file:`.po` file.

Open another terminal window and go to the Lino repository. 

  $ cd ~/repositories/lino

Note: You must go to the *Lino* repository because these strings are
part of Lino, not of :ref:`cosi`. In fact :ref:`cosi` has almost no
translatable string of its own, it is mostly a combination of
different modules from :mod:`lino.modlib`.

Launch Poedit_, specifying the :file:`.po` file for the Spanish
translation (international language code for Spanish is ``es``)::

  $ poedit lino/locale/es/LC_MESSAGES/django.po

It looks similar to this screenshot:

.. image:: poedit_es_1.png
  :scale: 60

Translate one or a few messages. In our example we translated the
following message::

  Hi, %(first_name)s!

into::

  ¡Hola, %(first_name)s!

Save your work in Poedit_.

Now you should first `touch` your `settings.py` file in order to tell
the development server process that something has changed. Open a
third terminal window and type::

  $ cd ~/mysite
  $ touch settings.py

This will cause the server process (which is running in the first
terminal window) to reload and to rewrite any cache files.

Refresh your browser page:

.. image:: cosi_es_hola.png
  :scale: 80



Trucs et astuces
----------------

Voici un pitfall: la traduction du string suivant::

  msgid "%(person)s has been unregistered from %(course)s"
  
ne doit pas être::

  msgstr "%(personne)s a été désinscrit du %(cours)"

mais bien::

  msgstr "%(person)s a été désinscrit du %(course)s"

C.-à-d. les mots-clés entre parenthèses sont des variables, 
et il *ne faut pas* les modifier.

À noter également que le ``s`` derrière la parenthèse ne sera pas 
imprimé mais est obligatoire 
(il indique à Python qu'il s'agit d'un remplacement de type `string`).
