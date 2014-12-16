# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)
"""Utilities, choicelists, mixins used by :mod:`lino.modlib.polls`.

"""

from lino import dd
from django.utils.translation import ugettext_lazy as _


class PollStates(dd.Workflow):
    """
    The list of possible states of a :class:`Poll`. Default is:

    .. django2rst::

       rt.show(polls.PollStates)

    """
    verbose_name_plural = _("Poll States")
    required = dd.required(user_level='admin')


add = PollStates.add_item
add('10', _("Draft"), 'draft')
add('20', _("Published"), 'published')
add('30', _("Closed"), 'closed')


class ResponseStates(dd.Workflow):
    """
    The list of possible states of a :class:`Poll`. Default is:

    .. django2rst::

       rt.show(polls.ResponseStates)


    """
    verbose_name_plural = _("Response States")
    required = dd.required(user_level='admin')


add = ResponseStates.add_item
add('10', _("Draft"), 'draft', editable=True)
add('20', _("Registered"), 'registered', editable=False)


ResponseStates.registered.add_transition(_("Register"), states='draft')
ResponseStates.draft.add_transition(_("Deregister"), states="registered")


# class QuestionType(dd.Choice):
    
# class QuestionTypes(dd.ChoiceList):
#     verbose_name_plural = _("Question Types")
#     required = dd.required(user_level='admin')
    
# add = QuestionTypes.add_item
# add('10', _("Draft"), 'draft', editable=True)


