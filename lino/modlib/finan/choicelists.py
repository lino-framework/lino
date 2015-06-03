# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Choicelists for `lino.modlib.finan`.

"""

from lino.api import dd, _


# class VoucherStates(dd.Workflow):
#     """The list of possible states for a voucher."""
#     @classmethod
#     def get_editable_states(cls):
#         return [o for o in cls.objects() if o.editable]

# add = VoucherStates.add_item
# add('10', _("Draft"), 'draft', editable=True)
# add('20', _("Registered"), 'registered', editable=False)


# @dd.receiver(dd.pre_analyze)
# def setup_workflow(sender=None, **kw):
#     VoucherStates.registered.add_transition(
#         _("Register"), states='draft', icon_name='accept')
#     VoucherStates.draft.add_transition(
#         _("Deregister"), states="registered", icon_name='pencil')


