# -*- coding: UTF-8 -*-
# Copyright 2008-2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Defines the
:class:`Language`
model.

"""


from django.db import models
from django.conf import settings

from lino import dd
from django.utils.translation import ugettext_lazy as _

#~ from lino.modlib.contacts import MODULE_LABEL


#~ class Language(dd.Model):
class Language(dd.BabelNamed):

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")
        ordering = ['name']

    id = models.CharField(max_length=3, primary_key=True)
    #~ name = babel.BabelCharField(max_length=200,verbose_name=_("Designation"))
    #~ name = models.CharField(max_length=200,verbose_name=_("Designation"))
    iso2 = models.CharField(max_length=2, blank=True)  # ,null=True)

    #~ def __unicode__(self):
        #~ return babel.babelattr(self,'name')

#~ add_babel_field(Language,'name')


class Languages(dd.Table):
    model = Language
    required = dd.required(user_groups='office')


from lino.modlib.contacts import Plugin


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu("contacts", Plugin.verbose_name)
    m.add_action(Languages)
