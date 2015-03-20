# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Choicelists for `lino.modlib.plausibility`.

.. autosummary::


"""

from __future__ import unicode_literals, print_function

from django.conf import settings
from lino.core.utils import gfk2lookup

from lino.api import dd, rt, _


if False:

    class Feedbacks(dd.ChoiceList):
        verbose_name = _("Plausibility feedback")
        verbose_name_plural = _("Plausibility feedback")

    add = Feedbacks.add_item()
    add("10", _("Ignorable"), 'ignorable')
    add("20", _("Serious"), 'serious')

    class Severities(dd.ChoiceList):
        verbose_name = _("Severity")
        verbose_name_plural = _("Plausibility problem severities")

    add = Severities.add_item()
    add("10", _("Note"), 'note')
    add("20", _("Warning"), 'warning')
    add("30", _("Error"), 'error')


class Checker(dd.Choice):
    """Base class for the choices of :class:`Checkers`.

    """
    verbose_name = None
    severity = None
    model = None
    help_text = None

    def __init__(self, model):
        assert isinstance(model, basestring)
        value = self.model + '.' + self.__class__.__name__
        text = self.verbose_name or value
        super(Checker, self).__init__(value, text, None)

    @classmethod
    def activate(cls):
        self = cls(cls.model)
        Checkers.add_item_instance(self)

    def update_for_object(self, obj, delete=True):
        """Update the problems of this checker and the specified object.
        """
        Problem = rt.modules.plausibility.Problem
        if delete:
            gfk = Problem.owner
            qs = Problem.objects.filter(**gfk2lookup(gfk, obj, checker=self))
            qs.delete()
        msg = '\n'.join([unicode(s) for s in self.get_checker_problems(obj)])
        if msg:
            prb = Problem(
                owner=obj, message=msg, checker=self,
                user=self.get_responsible_user(obj))
            prb.full_clean()
            prb.save()
            return prb

    def get_checker_problems(self, obj):
        """Return or yield a series of messages, each describing a
        plausibility problem.

        """
        return []

    def get_responsible_user(self, obj):
        return None


class Checkers(dd.ChoiceList):
    """The list of plausibility problem types known by this application.

    """
    required = dd.required(user_level='admin')
    verbose_name = _("Plausibility checker")
    verbose_name_plural = _("Plausibility checkers")
    item_class = Checker
    max_length = 50
    column_names = "name text"

    # the following would be nice but is currently ignored:
    detail_layout = """
    value name text
    plausibility.ProblemsByChecker
    """
