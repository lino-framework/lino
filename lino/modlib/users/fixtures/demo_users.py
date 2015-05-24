# -*- coding: UTF-8 -*-
# Copyright 2010-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This fixture installs fictive root users (administrators), one for
each language.  These names are being used by the :doc:`Online demo
sites </demos>`.

.. Lino currently knows demo users for the following languages:
  .. lino2rst::
  ses = rt.login()
  ses.show(rt.modules.users.Users,
    column_names="username first_name last_name language")

We are trying to sound realistic without actually hitting any real
person.  If one of the above names happens to match yours, just let us
know and we will change it.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


from django.conf import settings
from lino.modlib.users.choicelists import UserProfiles


def root_user(lang, **kw):
    # ~ kw.update(profile='900') # UserProfiles.admin)
    #~ print 20130219, UserProfiles.items()
    kw.update(profile=UserProfiles.admin)
    kw.update(email=settings.SITE.demo_email)  # 'root@example.com'
    lang = lang.django_code
    kw.update(language=lang)
    lang = lang[:2]
    if lang == 'de':
        kw.update(first_name="Rolf", last_name="Rompen")
    elif lang == 'fr':
        kw.update(first_name="Romain", last_name="Raffault")
    elif lang == 'et':
        kw.update(first_name="Rando", last_name="Roosi")
    elif lang == 'en':
        kw.update(first_name="Robin", last_name="Rood")
    elif lang == 'pt':
        kw.update(first_name="Ronaldo", last_name="Rosa")
    elif lang == 'es':
        kw.update(first_name="Rodrigo", last_name="Rosalez")
    elif lang == 'nl':
        kw.update(first_name="Rik", last_name="Rozenbos")
    else:
        logger.warning("No demo user for language %r.", lang)
        return None
    kw.update(username=kw.get('first_name').lower())
    return kw


def objects():
    # logger.info("20150323 %s", settings.SITE.languages)
    User = settings.SITE.user_model
    if User is not None:
        for lang in settings.SITE.languages:
            if settings.SITE.hidden_languages is None \
               or not lang.django_code in settings.SITE.hidden_languages:
                kw = root_user(lang)
                if kw:
                    yield User(**kw)

