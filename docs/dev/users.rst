==============
Managing users
==============

User management in Lino deserves documentation since it is different
from Django.

.. This is a tested document. You can test it using:

    $ python setup.py test -s tests.LibTests.test_users

   doctests initialization:
    
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...     'lino.projects.docs.settings.demo'
    >>> from lino.api.doctest import *

.. contents::

Why do we replace Django's user management?
===========================================

Django's `django.contrib.auth
<https://docs.djangoproject.com/en/dev/topics/auth/>`_ module has a
few problems which are solved by Lino's :mod:`lino.modlib.users`
module.

- Django's permission system is not suitable for developing complex
  applications because maintaining permissions becomes a hell when you
  develop an application which runs on different sites. Also it provides
  no means for defining instance-specific permissions and has no
  built-in concept of user profiles.

- 


Passwords
=========

Note that the `password` field of a newly created user is empty,
and the account therefore cannot be used to log in.  If you create
a new user manually using the web interface, you must click their
:class:`ChangePassword` action and set their password.

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

