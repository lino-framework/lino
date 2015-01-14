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
    >>> import json
    >>> from lino.runtime import *
    >>> from lino import dd
    >>> from django.test import Client
    >>> client = Client()

Discussion
==========

Don't take the following statements as my definitive opinion.  I
formulated them in order to get feedback and to understand if I were
missing something.

- The :mod:`lino.modlib.users` module is useful on Django sites with
  HTTP authentication where a central user management system is
  already running.

- Django's 
  `django.contrib.auth <https://docs.djangoproject.com/en/dev/topics/auth/>`_ 
  module is overkill in such cases.
  
- Not only overkill, but also it's tests suite reports 
  failures for things that are not used in the above 
  configuration.
  
The `Django documentation 
<https://docs.djangoproject.com/en/dev/topics/auth/#permissions>`_ says:

  Permissions are set globally per type of object, not per specific
  object instance. For example, it's possible to say "Mary may change
  news stories," but it's not currently possible to say "Mary may
  change news stories, but only the ones she created herself" or "Mary
  may only change news stories that have a certain status, publication
  date or ID." The latter functionality is something Django developers
  are currently discussing.

Suggested readings related to the topic:

- Documentation of module :mod:`lino.modlib.users`
- The `Other authentication sources
  <http://docs.djangoproject.com/en/dev/topics/auth/#other-authentication-sources>`_
  section in the Django docs.
- `Authentication using REMOTE_USER
  <http://docs.djangoproject.com/en/dev/howto/auth-remote-user/>`_
- `Role-based access control
  <http://en.wikipedia.org/wiki/Role-based_access_control>`_  
  

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

