# -*- coding: UTF-8 -*-
# Copyright 2012-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from django.core.management.base import BaseCommand
from django.conf import settings
from lino.api import dd, rt


class Command(BaseCommand):
    help = __doc__

    def handle(self, *args, **options):
        settings.SITE.startup()
        ar = rt.login()
        # fn = rt.find_config_file("status.jinja.rst", "jinja")
        fn = "jinja/status.jinja.rst"
        context = ar.get_printable_context()
        print(dd.plugins.jinja.render_jinja(ar, fn, context))
