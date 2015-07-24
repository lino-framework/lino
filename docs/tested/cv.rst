.. _lino.tested.cv:

==================================
Career module (tested)
==================================


.. How to test only this document:

    $ python setup.py test -s tests.DocsTests.test_cv
    
    doctest init:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino.projects.docs.settings.demo'
    >>> from lino.api.doctest import *

.. contents:: 
   :local:
   :depth: 2


>>> UserProfiles = rt.modules.users.UserProfiles
>>> LanguageKnowledges = rt.modules.cv.LanguageKnowledges

>>> rt.show(UserProfiles)
======= =========== ===============
 value   name        text
------- ----------- ---------------
 000     anonymous   Anonymous
 100     user        User
 900     admin       Administrator
======= =========== ===============
<BLANKLINE>

>>> a = UserProfiles.admin
>>> a
users.UserProfiles.admin:900

>>> u = UserProfiles.user
>>> u
users.UserProfiles.user:100

>>> LanguageKnowledges.required_roles
set([<class 'lino.modlib.cv.roles.CareerStaff'>])

>>> LanguageKnowledges.default_action.get_view_permission(u)
False

>>> LanguageKnowledges.default_action.get_view_permission(a)
False
