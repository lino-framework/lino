# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models for `lino.modlib.plausibility`.

.. autosummary::

"""

from __future__ import unicode_literals, print_function
from builtins import object
from collections import OrderedDict

from django.db import models

from lino.core.gfks import gfk2lookup
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.users.mixins import UserAuthored
from lino.core.roles import SiteStaff

from lino.api import dd, rt, _

from .choicelists import Checker, Checkers

from .roles import PlausibilityUser


class UpdateProblem(dd.Action):
    icon_name = 'bell'
    label = _("Check plausibility")
    combo_group = "plausibility"
    fix_them = False
    sort_index = 90
    # custom_handler = True
    # select_rows = False
    default_format = None

    def run_from_ui(self, ar, fix=None):
        if fix is None:
            fix = self.fix_them
        Problem = rt.modules.plausibility.Problem
        # print(20150327, ar.selected_rows)
        for obj in ar.selected_rows:
            assert isinstance(obj, Problem)
            chk = obj.checker
            owner = obj.owner
            # not tested: what happens if the following deletes
            # another obj from selected_rows?
            qs = Problem.objects.filter(
                **gfk2lookup(Problem.owner, owner, checker=chk))
            qs.delete()
            chk.update_problems(owner, False, fix)
        ar.set_response(refresh_all=True)


class FixProblem(UpdateProblem):
    label = _("Fix plausibility problems")
    fix_them = True
    sort_index = 91


class UpdateProblemsByController(dd.Action):
    """Updates the table of plausibility problems for a given database
    object, also removing those messages which no longer exist. This
    action does not change anything else in the database.

    This action is automatically being installed on each model for
    which there is at least one active :class:`Checker
    <lino.modlib.plausibility.choicelists.Checker>`.

    """
    icon_name = 'bell'
    label = _("Check plausibility")
    combo_group = "plausibility"
    fix_them = False

    def __init__(self, model):
        self.model = model
        super(UpdateProblemsByController, self).__init__()

    def run_from_ui(self, ar, fix=None):
        if fix is None:
            fix = self.fix_them
        Problem = rt.modules.plausibility.Problem
        gfk = Problem.owner
        checkers = get_checkable_models()[self.model]
        for obj in ar.selected_rows:
            assert isinstance(obj, self.model)
            qs = Problem.objects.filter(**gfk2lookup(gfk, obj))
            qs.delete()
            for chk in checkers:
                chk.update_problems(obj, False, fix)
        ar.set_response(refresh=True)


class FixProblemsByController(UpdateProblemsByController):
    """Update plausibility problems, repairing those which are
    automatically fixable.

    """
    label = _("Fix plausibility problems")
    fix_them = True


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

    .. attribute:: user

       The :class:`user <lino.modlib.users.models.User>` reponsible
       for fixing this problem.

       This field is being filled by the :meth:`get_responsible_user
       <lino.modlib.plausibility.choicelists.Checker.get_responsible_user>`
       method of the :attr:`checker`.

    """
    class Meta(object):
        app_label = 'plausibility'
        verbose_name = _("Plausibility problem")
        verbose_name_plural = _("Plausibility problems")
        ordering = ['owner_type', 'owner_id', 'checker']

    # problem_type = ProblemTypes.field()
    checker = Checkers.field()
    # severity = Severities.field()
    # feedback = Feedbacks.field(blank=True)
    message = models.CharField(_("Message"), max_length=250)
    # fixable = models.BooleanField(_("Fixable"), default=False)

    update_problem = UpdateProblem()
    fix_problem = FixProblem()


dd.update_field(Problem, 'user', verbose_name=_("Responsible"))
Problem.set_widget_options('checker', width=10)
Problem.set_widget_options('user', width=10)
Problem.set_widget_options('message', width=50)


class Problems(dd.Table):
    "The base table for :class:`Problem` objects."
    model = 'plausibility.Problem'
    column_names = "user owner message #fixable checker *"
    auto_fit_column_widths = True
    editable = False
    cell_edit = False
    parameters = dict(
        user=models.ForeignKey(
            'users.User', blank=True, null=True,
            verbose_name=_("Responsible"),
            help_text=_("""Only problems for this responsible.""")),
        checker=Checkers.field(
            blank=True, help_text=_("Only problems by this checker.")),
        )
    params_layout = "user checker"

    # simple_parameters = ('user', 'checker')
    detail_layout = dd.DetailLayout("""
    user owner checker id
    message""", window_size=(70, 'auto'))

    @classmethod
    def get_simple_parameters(cls):
        s = super(Problems, cls).get_simple_parameters()
        s.add('user')
        s.add('checker')
        return s


class AllProblems(Problems):
    """Show all plausibility problems.

    This table can be opened by system managers using
    :menuselection:`Explorer --> System --> Plausibility problems`.

    """
    required_roles = dd.required(SiteStaff)


class ProblemsByOwner(Problems):
    master_key = 'owner'
    column_names = "message checker user #fixable *"


class ProblemsByChecker(Problems):
    """Show the plausibility problems by checker.

    This was the first use case of a slave table with a master which
    is something else than a model instance.

    """
    master_key = 'checker'

    column_names = "user owner message #fixable *"

    @classmethod
    def get_master_instance(cls, ar, model, pk):
        return Checkers.get_by_value(pk)

    @classmethod
    def get_filter_kw(self, ar, **kw):
        kw.update(checker=ar.master_instance)
        return kw


class MyProblems(Problems):
    """Shows the plausibility problems assigned to this user.

    """
    required_roles = dd.required(PlausibilityUser)
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


@dd.receiver(dd.pre_analyze)
def set_plausibility_actions(sender, **kw):
    """Installs the :class:`UpdateProblemsByController` action on every
    model for which there is at least one Checker

    """
    for m in list(get_checkable_models().keys()):
        assert m is not Problem
        m.define_action(check_plausibility=UpdateProblemsByController(m))
        m.define_action(fix_problems=FixProblemsByController(m))


def get_checkable_models(*args):
    """Return an `OrderedDict` mapping each model which has at least one
    checker to a list of these checkers.

    The dict is ordered to avoid that checkers run in a random order.

    """
    checkable_models = OrderedDict()
    for chk in Checkers.objects():
        if len(args):
            skip = True
            for arg in args:
                if arg in chk.value:
                    skip = False
            if skip:
                continue
        for m in chk.get_checkable_models():
            lst = checkable_models.setdefault(m, [])
            lst.append(chk)
    return checkable_models



