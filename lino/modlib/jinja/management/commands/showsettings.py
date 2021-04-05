# -*- coding: UTF-8 -*-
# Copyright 2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = __doc__

    def handle(self, *args, **options):
        for k in dir(settings):
            if not k.startswith("_") and k == k.upper():
                print(k, "=", getattr(settings, k))
