=====
Users
=====

.. module:: ml.users


.. This document is part of the test suite. To run (almost) only this
   test:

    $ python setup.py test -s tests.DocsTests.test_docs

    General stuff:

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...     'lino.projects.docs.settings.demo'
    >>> import json
    >>> from lino.runtime import *
    >>> from lino import dd
    >>> from django.test import Client
    >>> client = Client()

Models
======

.. class:: User

  .. attribute:: username

  .. attribute:: profile

  The profile of a user is what defines her or his permissions.
 
  Users with an empty `profile` field are considered inactive and
  cannot log in.


  .. attribute:: partner

    Pointer to the :class:`ml.contacts.Partner` instance related to
    this user.

    This is a DummyField when :mod:`ml.contacts` is not installed.


.. class:: ChangePassword

Note that the `password` field of a new user is empty, and the account
therefore cannot be used to log in.  If you create a new user manually
using the web interface, you must click their :class:`ChangePassword`
action and set their password.

>>> try:
...     users.User.objects.get(username="test").delete()
... except users.User.DoesNotExist:
...    pass
>>> u = users.User(username="test")
>>> u.save()
>>> print u.has_usable_password()
False


The `password` field is empty, and the :meth:`User.check_password`
method returns `False`:

>>> print repr(u.password)
u''
>>> print u.check_password('')
False

When setting the password for a newly created user, leave the
field :guilabel:`Current password` empty.

>>> ses = rt.login('robin')
>>> values = dict(current="", new1="1234", new2="1234")
>>> rv = ses.run(u.change_password, action_param_values=values)
>>> print(rv['message'])
New password has been set for 1 users.



Choicelists
===========

.. currentmodule:: ml.users

.. class:: UserGroups

    TODO: Rename this to "FunctionalGroups" or sth similar.
    
    Functional Groups are another way of differenciating users when 
    defining access permissions and workflows. 
    
    Applications can define their functional groups
    


.. class:: UserLevels

    The level of a user is one way of differenciating users when 
    defining access permissions and workflows. 
    
    .. django2rst:: rt.show(users.UserLevels,
                            column_names='value name text')


.. class:: UserProfiles

    The list of user profiles available on this site. 
    
    Each user profile is a set of user levels 
    (one for each functional group), 
    leading to an individual combination of permissions.
    
    The demo database has defined the following user profiles:

    .. django2rst:: rt.show(users.UserProfiles,
                            column_names='value name text level')

    Note that we show here only the "general" or "system" userlevel.
    Open :menuselection:`Explorer --> System --> User Profiles`
    in your Lino to see all application-specific userlevels.


Fixtures
========

.. module:: ml.users.fixtures.demo

The :mod:`lino.modlib.users.fixtures.demo` module installs fictive
root users (administrators), one for each language.  These names are
being used by the :doc:`Online demo sites </demos>`.

Lino currently knows demo users for the following languages:

.. django2rst::

  from lino.runtime import *
  ses = rt.login()
  ses.show(users.Users, 
    column_names="username first_name last_name language")

We are trying to sound realistic without actually hitting any real
person.  If one of the above names happens to match yours, just let us
know and we will change it.
