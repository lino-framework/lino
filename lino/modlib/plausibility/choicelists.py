# Copyright 2015-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Choicelists for `lino.modlib.plausibility`.


"""

from __future__ import unicode_literals, print_function
from builtins import str
from past.builtins import basestring

from django.utils import translation
from lino.core.gfks import gfk2lookup
from lino.core.roles import SiteStaff

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
    self = None
    model = None
    """The model to be checked. This may be an abstract model.  It can
    also be None, but then you must define your own
    :meth:`get_checkable_models` method.

    """

    help_text = None

    def __init__(self):
        # value = self.__module__ + '.' + self.__class__.__name__
        value = self.__module__.split('.')[-2] + '.' + self.__class__.__name__
        # if isinstance(self.model, basestring):
        #     value = self.model + '.' + self.__class__.__name__
        # else:
        #     value = self.model.__name__ + '.' + self.__class__.__name__
        if self.verbose_name is None:
            text = value
        else:
            text = self.verbose_name
        super(Checker, self).__init__(value, text, None)

    @classmethod
    def activate(cls):
        """Application developers must call this on their subclass in order to
        "register" or "activate" it.

        This actually just creates an instance and adds it as a choice
        to the :class:`Checkers` choicelist.

        """
        if cls.self is not None:
            raise Exception("Duplicate call to {0}.activate()".format(cls))
        cls.self = cls()
        Checkers.add_item_instance(cls.self)

    def get_checkable_models(self):
        """Return a list of the models to check.

        The default implementation expects :attr:`model` to be set.
        """
        return rt.models_by_base(self.model, toplevel_only=True)

    def resolve_model(self, site):
        if isinstance(self.model, basestring):
            self.model = site.modules.resolve(self.model)

    def update_problems(self, obj, delete=True, fix=False):
        """Update the problems of this checker and the specified object.

        When `delete` is False, the caller is responsible for deleting
        any existing objects.

        """
        Problem = rt.modules.plausibility.Problem
        if delete:
            gfk = Problem.owner
            qs = Problem.objects.filter(**gfk2lookup(gfk, obj, checker=self))
            qs.delete()

        done = []
        todo = []
        for fixable, msg in self.get_plausibility_problems(obj, fix):
            if fixable:
                msg = u"(\u2605) " + str(msg)
            if fixable and fix:
                done.append(msg)
            else:
                todo.append(msg)
        if len(todo):
            user = self.get_responsible_user(obj)
            if user is None:
                lang = dd.get_default_language()
            else:
                lang = user.language
            with translation.override(lang):
                msg = '\n'.join([str(s) for s in todo])
            prb = Problem(owner=obj, message=msg, checker=self, user=user)
            prb.full_clean()
            prb.save()
        return (todo, done)

    def get_plausibility_problems(self, obj, fix=False):
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

    This was the first use case of a :class:`ChoiceList
    <lino.core.choicelists.ChoiceList>` with a :attr:`detail_layout
    <lino.core.actors.Actor.detail_layout>`.

    """
    required_roles = dd.required(SiteStaff)
    verbose_name = _("Plausibility checker")
    verbose_name_plural = _("Plausibility checkers")
    item_class = Checker
    max_length = 250
    # e.g. "lino_welfare.modlib.pcsw.models.ClientCoachingsChecker"
    column_names = "value text"
    show_values = False

    detail_layout = """
    value text
    plausibility.ProblemsByChecker
    """


@dd.receiver(dd.pre_analyze)
def resolve_checkers(sender, **kw):
    for chk in Checkers.objects():
        chk.resolve_model(sender)
