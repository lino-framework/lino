# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
.. autosummary::
   :toctree:

   models
   management.commands

"""
from __future__ import print_function

# from lino.api.ad import Plugin, _


# class Plugin(Plugin):

#     ui_label = _("Lino")

#     # media_name = 'lino'

from lino import AFTER17, site_startup

if AFTER17:

    from django.apps import AppConfig

    class LinoConfig(AppConfig):
        name = 'lino.modlib.lino_startup'

        # def __init__(self):
        #     # raise Exception("20150820")
        #     super(LinoConfig, self).__init__()
        #     startup()

        def ready(self):
            # raise Exception("20150820")
            # print "20151010 LinoConfig.ready() gonna call Site.startup"
            try:
                site_startup()
            except Exception as e:
                print(e)
                raise

    default_app_config = 'lino.modlib.lino_startup.LinoConfig'

