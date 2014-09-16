=====
Users
=====

.. module:: ml.users


.. This document is part of the test suite. To run (almost) only this
   test:

    $ python setup.py test -s tests.DocsTests.test_docs

    General stuff:

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.docs.settings'
    >>> import json
    >>> from lino.runtime import *
    >>> from lino import dd
    >>> from django.test import Client
    >>> client = Client()



.. class:: User

  .. attribute:: username

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

>>> ses = dd.login('robin')
>>> values = dict(current="", new1="1234", new2="1234")
>>> rv = ses.run(u.change_password, action_param_values=values)
>>> print(rv['message'])
New password has been set for 1 users.

