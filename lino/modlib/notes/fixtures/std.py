# -*- coding: UTF-8 -*-
# Copyright 2008-2010 Luc Saffre
# License: BSD (see file COPYING for details)


from django.utils.translation import ugettext_lazy as _

from lino.utils.instantiator import Instantiator, i2d
from lino.core.utils import resolve_model


def objects():

    noteType = Instantiator('notes.NoteType', "name").build
    yield noteType(
        _("Default"), build_method='appyodt', template='Default.odt')
    #~ yield noteType((u"Test (rtf)"),build_method='rtf',template='test.rtf')
