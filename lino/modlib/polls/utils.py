# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Utilities, choicelists, mixins used by :mod:`lino.modlib.polls`.

"""

from lino.api import dd
from django.utils.translation import ugettext_lazy as _


class PollStates(dd.Workflow):
    """
    The list of possible states of a :class:`Poll`. Default is:

    .. django2rst::

       rt.show(polls.PollStates)

    """
    verbose_name_plural = _("Poll States")
    required_roles = dd.required(dd.SiteStaff)


add = PollStates.add_item
add('10', _("Draft"), 'draft')
add('20', _("Published"), 'published')
add('30', _("Closed"), 'closed')

PollStates.published.add_transition(
    _("Publish"), required_states='draft')
PollStates.closed.add_transition(
    _("Close"), required_states='draft published')
PollStates.draft.add_transition(
    _("Reopen"), required_states='published closed')


class ResponseStates(dd.Workflow):
    """
    The list of possible states of a :class:`Poll`. Default is:

    .. django2rst::

       rt.show(polls.ResponseStates)


    """
    verbose_name_plural = _("Response States")
    required_roles = dd.required(dd.SiteStaff)


add = ResponseStates.add_item
add('10', _("Draft"), 'draft', editable=True)
add('20', _("Registered"), 'registered', editable=False)


ResponseStates.registered.add_transition(
    _("Register"), required_states='draft')
ResponseStates.draft.add_transition(
    _("Deregister"), required_states="registered")


