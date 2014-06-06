============================
Instructions for translators
============================

Here is how your can help translating Lino into your own language.

We suppose that you have installed the *development version* (not a
released version from PyPI) for both Lino and the application you
want to translate.
In the following instructions we suppose that :ref:`cosi` is the
application you want to translate.
As explained in :ref:`cosi.install`.

You are going to edit a series of :xfile:`.po` files which are part of
the code repositories of both Lino and :ref:`cosi`.  

To edit these :xfile:`.po` files you will be using either your
preferred plain text editor or a tool like `PoEdit
<http://www.poedit.net>`_. We recommend the latter.

When you are satisfied with your work, you will make a pull request to
ask me to integrate your changes into the public repositories of Lino
and :ref:`cosi`.
More about pull requests:

- http://git-scm.com/book/en/Distributed-Git-Contributing-to-a-Project
- https://help.github.com/articles/creating-a-pull-request

But don't simply start to translate all messages using poEdit! The
translations themselves are just the last part.  First learn how it
works!


  $ cd ~/repositories/cosi


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
