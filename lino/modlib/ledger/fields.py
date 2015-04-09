# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database fields for `lino.modlib.ledger`.


"""


from lino.api import dd, _


# def MatchField(verbose_name=None, **kwargs):
#     """A pointer to another movement which is to be cleared by the owner
#     of this field.

#     """
#     if verbose_name is None:
#         verbose_name = _("Match")
#     kwargs.update(verbose_name=verbose_name)
#     kwargs.update(help_text=_("The movement to be cleared."))
#     kwargs.update(related_name="%(app_label)s_%(class)s_set_by_match",)
#     return dd.ForeignKey('ledger.Movement', **kwargs)


# class MatchField(models.CharField):

#     def __init__(self, verbose_name=None, **kw):
#         if verbose_name is None:
#             verbose_name = _("Match")
#         kw.setdefault('max_length', 20)
#         models.CharField.__init__(self, verbose_name, **kw)


class DcAmountField(dd.VirtualField):
    """An editable virtual field to get and set both database fields
    :attr:`amount` and :attr:`dc`

    """

    editable = True

    def __init__(self, dc, *args, **kw):
        self.dc = dc
        dd.VirtualField.__init__(self, dd.PriceField(*args, **kw), None)

    def set_value_in_object(self, request, obj, value):
        obj.amount = value
        obj.dc = self.dc

    def value_from_object(self, obj, ar):
        if obj.dc == self.dc:
            return obj.amount
        return None
