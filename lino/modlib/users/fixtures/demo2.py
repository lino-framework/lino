# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Set password "1234" for all users.

This is an additive fixture designed to work also on existing data.

"""

from django.conf import settings


def objects():
    for u in settings.SITE.user_model.objects.exclude(user_type=''):
        u.set_password('1234')
        yield u
