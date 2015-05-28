.. _lino.tested.cv:

==================================
Career module (tested)
==================================


.. How to test only this document:

  $ python setup.py test -s tests.DocsTests.test_cv

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino.projects.docs.settings.demo'
>>> from lino.api.doctest import *

.. contents:: 
   :local:
   :depth: 2


>>> UserProfiles = rt.modules.users.UserProfiles
>>> UserLevels = rt.modules.users.UserLevels
>>> LanguageKnowledges = rt.modules.cv.LanguageKnowledges

>>> rt.show(UserLevels)
======= ========= ============ =============== ========
 value   name      Short name   text            Remark
------- --------- ------------ --------------- --------
 10      guest     G            Guest
 30      user      U            User
 40      manager   M            Manager
 50      admin     A            Administrator
======= ========= ============ =============== ========
<BLANKLINE>

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
users.UserProfiles.admin:900(level=Administrator,reception=Administrator,polls=Administrator,accounts=Administrator,courses=Administrator,beid=Administrator,office=Administrator)

>>> u = UserProfiles.user
>>> u
users.UserProfiles.user:100(level=User,reception=User,polls=User,accounts=User,courses=User,beid=User,office=User)

>>> manager = UserLevels.manager
>>> u.level
<UserLevels.user:30>

>>> manager
<UserLevels.manager:40>

>>> u.level < manager
True

>>> u.level
<UserLevels.user:30>

>>> LanguageKnowledges.required
{'user_level': u'manager'}

>>> LanguageKnowledges.default_action.get_view_permission(u)
False

