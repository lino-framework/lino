.. _lino.tutorials.myroles:

============================================
Local customizations to the user permissions
============================================

.. How to test only this document:

    $ python setup.py test -s tests.DocsTests.test_myroles
    
    doctest init:

    >>> from lino.api.doctest import *

.. contents::
   :depth: 1
   :local:


The roles module
================

The standard system or user roles and profiles is defined by
:mod:`lino.projects.polly.roles`.

This system is used by default:

>>> from lino.projects.polly.settings import Site
>>> print(Site.user_profiles_module)
lino.modlib.polls.roles

The local roles module
======================

On this site we created a local roles module.

First step is to **create and activate a local roles module**:

- Create a file named :file:`myroles.py` next to your local
  :xfile:`settings.py` with this content::

    from lino.projects.polly.roles import *

- In your :xfile:`settings.py` file, set :attr:`user_profiles_module
  <lino.core.site.Site.user_profiles_module>` to the Python path of
  above file::
    
    user_profiles_module = 'mysite.myroles'

This first step should have no visible effect at all. We've just
prepared a hook for defining local customizations.  The only
difference is that our local :file:`myroles.py` module is being
imported at startup:

>>> print(settings.SITE.user_profiles_module)
myroles.myroles

Second step is to add customizations to that :file:`myroles.py` file.

An example
==========

For example the default permission system of Lino Polly says that only
a site administrator can see the global list of all polls. This list
is visible through :menuselection:`Explorer --> Polls --> Polls`.  A
normal user does not see that menu command.  But we apply a local
customization. In our variant of a Lino Polly application, every
authenticated user can see that table.

Here is the :xfile:`settings.py` file used by this tutorial:

.. literalinclude:: settings.py

And here is the :file:`myroles.py` file used by this tutorial:

.. literalinclude:: myroles.py


The following code snippets are to test whether a normal user now
really can see all polls (i.e. has the :menuselection:`Explorer -->
Polls --> Polls` menu command):

>>> u = users.User(username="user", profile="100")
>>> u.full_clean()
>>> u.save()
>>> rt.login('user').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Polls : My Polls, My Responses
- Explorer :
  - Polls : Polls
- Site : About
