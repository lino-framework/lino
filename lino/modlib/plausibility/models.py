# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models for `lino.modlib.plausibility`.

.. autosummary::

"""

from __future__ import unicode_literals, print_function

from clint.textui import puts, progress

from django.db import models

from lino.core.utils import gfk2lookup
from lino.modlib.contenttypes.mixins import Controllable
from lino.modlib.users.mixins import UserAuthored

from lino.api import dd, rt, _

from .choicelists import Checker, Checkers


class Problem(Controllable, UserAuthored):
    """Represents a detected plausibility problem.

    Database objects of this model are considered temporary data which
    may be updated automatically without user interaction.

    .. attribute:: checker

       The :class:`Checker
       <lino.modlib.plausibility.choicelists.Checker>` which reported
       this problem.

    .. attribute:: message

       The message text. This is a concatenation of all messages that
       were yeld by the :attr:`checker`.

    .. attribute:: fixable

        Whether this problem is fixable, i.e. can be repaired
        automatically.

    .. attribute:: user

       The :class:`user <lino.modlib.users.models.User>` reponsible
       for fixing this problem.

       This field is being filled by the :meth:`get_responsible_user
       <lino.modlib.plausibility.choicelists.Checker.get_responsible_user>`
       method of the :attr:`checker`.

    """
    class Meta:
        verbose_name = _("Plausibility problem")
        verbose_name_plural = _("Plausibility problems")

    # problem_type = ProblemTypes.field()
    checker = Checkers.field()
    # severity = Severities.field()
    # feedback = Feedbacks.field(blank=True)
    message = models.CharField(_("Message"), max_length=250)
    fixable = models.BooleanField(_("Fixable"), default=False)

dd.update_field(Problem, 'user', verbose_name=_("Responsible"))
Problem.set_widget_options('checker', width=10)
Problem.set_widget_options('user', width=10)


class Problems(dd.Table):
    "The table of all :class:`Problem` objects."
    model = 'plausibility.Problem'
    column_names = "user owner message:40 fixable checker *"
    auto_fit_column_widths = True
    parameters = dict(
        user=models.ForeignKey(
            'users.User', blank=True, null=True,
            verbose_name=_("Responsible"),
            help_text=_("""Only problems for this responsible.""")),
        checker=Checkers.field(
            blank=True, help_text=_("Only problems by this checker.")),
        )
    params_layout = "user checker"

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Problems, self).get_request_queryset(ar)
        pv = ar.param_values
        if pv.user:
            qs = qs.filter(user=pv.user)
        if pv.checker:
            qs = qs.filter(checker=pv.checker)

        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Problems, self).get_title_tags(ar):
            yield t
        pv = ar.param_values
        for k in ('user', 'checker'):
            v = getattr(pv, k)
            if v:
                yield unicode(self.parameters[k].verbose_name) \
                    + ' ' + unicode(v)


class AllProblems(Problems):
    required = dd.required(user_level='manager')


class ProblemsByOwner(Problems):
    master_key = 'owner'
    column_names = "message:40 checker user fixable *"


class ProblemsByChecker(Problems):
    master = Checker


class MyProblems(Problems):
    """Shows the plausibility problems assigned to this user.

    """
    label = _("Plausibility problems assigned to me")

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyProblems, self).param_defaults(ar, **kw)
        kw.update(user=ar.get_user())
        return kw

    @classmethod
    def get_welcome_messages(cls, ar, **kw):
        sar = ar.spawn(cls)
        count = sar.get_total_count()
        if count > 0:
            msg = _("There are {0} plausibility problems assigned to you.")
            msg = msg.format(count)
            yield ar.href_to_request(sar, msg)


class CheckPlausibility(dd.Action):
    icon_name = 'bell'
    label = _("Check plausibility")

    def __init__(self, model):
        self.model = model
        super(CheckPlausibility, self).__init__()

    def run_from_ui(self, ar, fix=False):
        """Implements :meth:`lino.core.actions.Action.run_from_ui`.

        """
        Problem = rt.modules.plausibility.Problem
        gfk = Problem.owner
        checkers = get_checkable_models()[self.model]
        for obj in ar.selected_rows:
            assert isinstance(obj, self.model)
            # (todo, done)
            qs = Problem.objects.filter(**gfk2lookup(gfk, obj))
            qs.delete()
            for chk in checkers:
                chk.update_problems(obj, False, fix)


@dd.receiver(dd.pre_analyze)
def set_plausibility_actions(sender, **kw):
    """Installs the :class:`CheckPlausibility` action on every model for
    which there is at least one Checker

    """
    for m in get_checkable_models().keys():
        m.define_action(check_plausibility=CheckPlausibility(m))


def get_checkable_models(*args):
    """Return a `dict` mapping each model which has at least one checker
    to a list of these checkers.

    """
    if len(args):
        selection = [getattr(Checkers, arg) for arg in args]
    else:
        selection = Checkers.objects()
    checkable_models = dict()
    for chk in selection:
        for m in rt.models_by_base(chk.model):
            lst = checkable_models.setdefault(m, [])
            lst.append(chk)
    return checkable_models


def check_plausibility(args=[], fix=True):
    """Called by :manage:`check_plausibility`. See there."""
    Problem = rt.modules.plausibility.Problem
    mc = get_checkable_models(*args)
    for m, checkers in mc.items():
        ct = rt.modules.contenttypes.ContentType.objects.get_for_model(m)
        Problem.objects.filter(owner_type=ct).delete()
        name = unicode(m._meta.verbose_name_plural)
        qs = m.objects.all()
        msg = _("Running {0} plausibility checkers on {1} {2}...").format(
            len(checkers), qs.count(), name)
        puts(msg)
        sums = [0, 0, name]
        for obj in progress.bar(qs):
            for chk in checkers:
                todo, done = chk.update_problems(obj, False, fix)
                sums[0] += len(todo)
                sums[1] += len(done)
        if sums[0] or sums[1]:
            msg = _("Found {0} and fixed {1} plausibility problems in {2}.")
            puts(msg.format(*sums))
        else:
            puts(_("No plausibility problems found in {0}.").format(name))
