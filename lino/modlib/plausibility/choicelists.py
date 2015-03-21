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

    def __init__(self):
        if isinstance(self.model, basestring):
            value = self.model + '.' + self.__class__.__name__
        else:
            value = self.model.__name__ + '.' + self.__class__.__name__
        text = self.verbose_name or value
        super(Checker, self).__init__(value, text, None)

    @classmethod
    def activate(cls):
        self = cls()
        Checkers.add_item_instance(self)

    def resolve_model(self, site):
        if isinstance(self.model, basestring):
            self.model = site.modules.resolve(self.model)

    def update_for_object(self, obj, delete=True, fix=False):
        """Update the problems of this checker and the specified object.

        When `delete` is False, the caller is responsible for deleting
        any existing objects.

        """
        Problem = rt.modules.plausibility.Problem
        if delete:
            gfk = Problem.owner
            qs = Problem.objects.filter(**gfk2lookup(gfk, obj, checker=self))
            qs.delete()
        repairable = False
        done = []
        todo = []
        for rep, msg in self.get_checker_problems(obj, fix):
            if rep:
                repairable = True
            if fix and rep:
                done.append(msg)
            else:
                todo.append(msg)
        msg = '\n'.join([unicode(s) for s in todo])
        if msg:
            prb = Problem(
                owner=obj, message=msg, checker=self,
                repairable=repairable,
                user=self.get_responsible_user(obj))
            prb.full_clean()
            prb.save()
        return (todo, done)

    def get_checker_problems(self, obj, fix=False):
        """Return or yield a series of `(fixable, message)` tuples, each
        describing a plausibility problem. `fixable` is a boolean
        saying whther this problem can be automatically fixed. And if
        `fix` is `True`, this method is also responsible for fixing
        it.

        """
        return []

    def get_responsible_user(self, obj):
        """The :attr:`user <lino.modlib.plausibility.models.Problem.user>` to
        be considered as reponsible for problems detected by this
        checker on the given database object `obj`.

        The given `obj` will always be an instance of :attr:`model`.

        The default implementation returns the *main plausibility
        responsible* defined for this site (see
        :attr:`responsible_user
        <lino.modlib.plausibility.Plugin.responsible_user>`).

        """
        return dd.plugins.plausibility.get_responsible_user(self, obj)


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

    # @classmethod
    # def on_analyze(cls, site):
    #     super(Checkers, cls).on_analyze(site)
    #     for chk in cls.objects():
    #         chk.resolve_model(site)


@dd.receiver(dd.pre_analyze)
def resolve_checkers(sender, **kw):
    for chk in Checkers.objects():
        chk.resolve_model(sender)
