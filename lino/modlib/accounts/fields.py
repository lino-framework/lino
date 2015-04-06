# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
"""

from __future__ import unicode_literals

from django.db import models
from lino.core.store import BooleanStoreField
from lino.api import _

from .utils import DEBIT, CREDIT

DCLABELS = {
    DEBIT: _("Debit"),
    CREDIT: _("Credit")
}


class DebitOrCreditStoreField(BooleanStoreField):

    """
    This is used as `lino_atomizer_class` for :class:`DebitOrCreditField`.
    """

    def format_value(self, ar, v):
        return unicode(DCLABELS[v])


class DebitOrCreditField(models.BooleanField):

    """A field that stores either :attr:`DEBIT
    <lino.modlib.accounts.utils.DEBIT>` or :attr:`CREDIT
    <lino.modlib.accounts.utils.CREDIT>` (see
    :mod:`lino.modlib.accounts.utils`).

    """
    lino_atomizer_class = DebitOrCreditStoreField

    def __init__(self, *args, **kw):
        kw.setdefault('help_text',
                      _("Debit (checked) or Credit (not checked)"))
        # kw.setdefault('default', None)
        models.BooleanField.__init__(self, *args, **kw)


