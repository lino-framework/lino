# -*- coding: UTF-8 -*-
# Copyright 2015-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from builtins import object

from django.db import models

from lino.api import dd, _


class Commentable(dd.Model):
    class Meta(object):
        abstract = True

    private = models.BooleanField(_("Private"), default=False)
    
    def on_commented(self, comment, ar, cw):
        pass
    
    def get_rfc_description(self, ar):
        return ''

        
