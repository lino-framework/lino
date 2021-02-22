# Copyright 2015-2021 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from collections import OrderedDict

from django.db import models
from django.utils import translation
from django.template.defaultfilters import pluralize

from lino.core.gfks import gfk2lookup
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.users.mixins import UserAuthored
from lino.core.roles import SiteStaff

from lino.api import dd, rt, _

from .choicelists import Checker, Checkers

from .roles import CheckdataUser


class UpdateProblem(dd.Action):
    icon_name = 'bell'
    ui5_icon_name = "sap-icon://bell"
    label = _("Check data")
    combo_group = "checkdata"
    fix_them = False
    sort_index = 90
    # custom_handler = True
    # select_rows = False
    default_format = None

    def run_from_ui(self, ar, fix=None):
        if fix is None:
            fix = self.fix_them
        Problem = rt.models.checkdata.Problem
        # print(20150327, ar.selected_rows)
        for obj in ar.selected_rows:
            assert isinstance(obj, Problem)
            chk = obj.checker
            owner = obj.owner
            if owner is None:
                # A problem where owner is None means that the owner
                # has been deleted.
                obj.delete()
            else:
                qs = Problem.objects.filter(
                    **gfk2lookup(Problem.owner, owner, checker=chk))
                qs.delete()
                chk.update_problems(owner, False, fix)
        ar.set_response(refresh_all=True)


class FixProblem(UpdateProblem):
    label = _("Fix data problems")
    fix_them = True
    sort_index = 91


class UpdateProblemsByController(dd.Action):
    icon_name = 'bell'
    ui5_icon_name = "sap-icon://bell"
    label = _("Check data")
    combo_group = "checkdata"
    fix_them = False

    def __init__(self, model):
        self.model = model
        super(UpdateProblemsByController, self).__init__()

    def run_from_ui(self, ar, fix=None):
        if fix is None:
            fix = self.fix_them
        Problem = rt.models.checkdata.Problem
        gfk = Problem.owner
        checkers = get_checkers_for(self.model)
        for obj in ar.selected_rows:
            assert isinstance(obj, self.model)
            qs = Problem.objects.filter(**gfk2lookup(gfk, obj))
            qs.delete()
            for chk in checkers:
                chk.update_problems(obj, False, fix)
        ar.set_response(refresh=True)


class FixProblemsByController(UpdateProblemsByController):
    label = _("Fix data problems")
    fix_them = True


class Problem(Controllable, UserAuthored):
    class Meta(object):
        app_label = 'checkdata'
        verbose_name = _("Data problem")
        verbose_name_plural = _("Data problems")
        ordering = ['owner_type', 'owner_id', 'checker']

    controller_is_optional = False
    allow_merge_action = False
    allow_cascaded_delete = 'owner'

    # problem_type = ProblemTypes.field()
    checker = Checkers.field(verbose_name=_("Checker"))
    # severity = Severities.field()
    # feedback = Feedbacks.field(blank=True)
    message = models.CharField(_("Message"), max_length=250)
    # fixable = models.BooleanField(_("Fixable"), default=False)

    update_problem = UpdateProblem()
    fix_problem = FixProblem()

    # no longer needed after 20170826
    # @classmethod
    # def setup_parameters(cls, **fields):
    #     fields.update(checker=Checkers.field(
    #         blank=True, help_text=_("Only problems by this checker.")))
    #     return fields

    def __str__(self):
        return self.message

    @classmethod
    def get_simple_parameters(cls):
        for p in super(Problem, cls).get_simple_parameters():
            yield p
        yield 'checker'

dd.update_field(Problem, 'user', verbose_name=_("Responsible"))
Problem.set_widget_options('checker', width=10)
Problem.set_widget_options('user', width=10)
Problem.set_widget_options('message', width=50)
Problem.update_controller_field(verbose_name = _('Database object'))


class Problems(dd.Table):
    model = 'checkdata.Problem'
    column_names = "user owner message #fixable checker *"
    auto_fit_column_widths = True
    editable = False
    cell_edit = False
    # parameters = dict(
    #     # user=models.ForeignKey(
    #     #     'users.User', blank=True, null=True,
    #     #     verbose_name=_("Responsible"),
    #     #     help_text=_("""Only problems for this responsible.""")),
    #     )
    params_layout = "user checker"

    # simple_parameters = ('user', 'checker')
    detail_layout = dd.DetailLayout("""
    checker
    owner
    message
    user id
    """, window_size=(70, 'auto'))



class AllProblems(Problems):
    """Show all data problems.

    This table can be opened by system managers using
    :menuselection:`Explorer --> System --> Data problems`.

    """
    required_roles = dd.login_required(SiteStaff)


class ProblemsByOwner(Problems):
    """Show data problems related to this database object.

    """
    master_key = 'owner'
    column_names = "message checker user #fixable *"
    display_mode = 'summary'


class ProblemsByChecker(Problems):
    """Show the data problems by checker.

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

    required_roles = dd.login_required(CheckdataUser)
    label = _("Data problems assigned to me")

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyProblems, self).param_defaults(ar, **kw)
        kw.update(user=ar.get_user())
        return kw

    @classmethod
    def get_welcome_messages(cls, ar, **kw):
        sar = ar.spawn(cls)
        if not sar.get_permission():
            return
        count = sar.get_total_count()
        if count > 0:
            msg = _("There are {0} data problems assigned to you.")
            msg = msg.format(count)
            yield ar.href_to_request(sar, msg)


@dd.receiver(dd.pre_analyze)
def set_checkdata_actions(sender, **kw):
    for m in get_checkable_models().keys():
        if m is None:
            continue
        assert m is not Problem
        m.define_action(check_data=UpdateProblemsByController(m))
        m.define_action(fix_problems=FixProblemsByController(m))
        if False:
            # don't add it automatically because appdev might prefer
            # to show it in a detail_layout:
            m.define_action(show_problems=dd.ShowSlaveTable(
                ProblemsByOwner,
                icon_name = 'bell', combo_group = "checkdata"))


def get_checkers_for(model):
    return get_checkable_models()[model]

def check_instance(obj):
    """
    Run all checkers on the given instance.  Return list of problems.
    """
    for chk in get_checkers_for(obj.__class__):
        for prb in chk.check_instance(obj):
            yield prb

def get_checkable_models(*args):
    checkable_models = OrderedDict()
    for chk in Checkers.get_list_items():
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


def check_data(args=[], fix=True, prune=False):
    """Called by :manage:`checkdata`. See there."""
    Problem = rt.models.checkdata.Problem
    mc = get_checkable_models(*args)
    if len(mc) == 0 and len(args) > 0:
        raise Exception("No checker matches {0}".format(args))
    if prune:
        qs = Problem.objects.all()
        msg = "Prune {} existing messages...".format(qs.count())
        dd.logger.info(msg)
        qs.delete()

    final_sums = [0, 0, 0]
    with translation.override('en'):
        for m, checkers in mc.items():
            if m is None:
                qs = Problem.objects.filter(
                    **gfk2lookup(Problem.owner, None, checker__in=checkers))
                qs.delete()
                qs = [None]
                name = "unbound data"
                msg = "Running {0} checkers on {1}...".format(len(checkers), name)
            else:
                ct = rt.models.contenttypes.ContentType.objects.get_for_model(m)
                qs = Problem.objects.filter(owner_type=ct, checker__in=checkers)
                qs.delete()
                name = str(m._meta.verbose_name_plural)
                qs = m.objects.all()
                msg = "Running {0} data checkers on {1} {2}...".format(
                    len(checkers), qs.count(), name)
            dd.logger.debug(msg)
            sums = [0, 0, name]
            for obj in qs:
                for chk in checkers:
                    todo, done = chk.update_problems(obj, False, fix)
                    sums[0] += len(todo) + len(done)
                    sums[1] += len(done)
            if sums[0] or sums[1]:
                msg = "Found {0} and fixed {1} data problems in {2}."
                dd.logger.info(msg.format(*sums))
            else:
                dd.logger.debug(
                    "No data problems found in {0}.".format(name))
            final_sums[0] += 1
            final_sums[1] += sums[0]
            final_sums[2] += sums[1]
    msg = "Done %d %s, found %d and fixed %d problems."
    done, found, fixed = final_sums
    what = pluralize(done, "check,checks")
    dd.logger.info(msg, done, what, found, fixed)


@dd.schedule_daily()
def checkdata():
    """Run all data checkers."""
    check_data(fix=False)
    # rt.login().run(settings.SITE.site_config.run_checkdata)
