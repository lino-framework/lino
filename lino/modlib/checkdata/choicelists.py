# Copyright 2015-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.utils import translation
from lino.core.gfks import gfk2lookup
from lino.core.roles import SiteStaff
from django.utils.text import format_lazy

from lino.api import dd, rt, _

if False:

    class Feedbacks(dd.ChoiceList):
        verbose_name = _("Checkdata feedback")
        verbose_name_plural = _("Checkdata feedback")

    add = Feedbacks.add_item()
    add("10", _("Ignorable"), 'ignorable')
    add("20", _("Serious"), 'serious')

    class Severities(dd.ChoiceList):
        verbose_name = _("Severity")
        verbose_name_plural = _("Data problem severities")

    add = Severities.add_item()
    add("10", _("Note"), 'note')
    add("20", _("Warning"), 'warning')
    add("30", _("Error"), 'error')


class Checker(dd.Choice):
    verbose_name = None
    severity = None
    self = None
    model = None

    help_text = None

    def __init__(self):
        # value = self.__module__ + '.' + self.__class__.__name__
        value = self.__module__.split('.')[-2] + '.' + self.__class__.__name__
        # if isinstance(self.model, six.string_types):
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
        if cls.self is not None:
            raise Exception("Duplicate call to {0}.activate()".format(cls))
        cls.self = cls()
        Checkers.add_item_instance(cls.self)

    @classmethod
    def update_unbound_problems(cls, **kwargs):
        assert cls.self.model is None
        cls.self.update_problems(**kwargs)
        todo, done = cls.self.update_problems(**kwargs)
        msg = "Found {0} and fixed {1} data problems for {2}."
        dd.logger.info(msg.format(len(todo), len(done), cls.self))

    @classmethod
    def check_instance(cls, *args, **kwargs):
        return cls.self.get_checkdata_problems(*args, **kwargs)

    def get_checkable_models(self):
        if self.model is None:
            return [None]
        return rt.models_by_base(self.model, toplevel_only=True)

    def resolve_model(self, site):
        if isinstance(self.model, str):
            self.model = dd.resolve_model(self.model, strict=True)

    def update_problems(self, obj=None, delete=True, fix=False):
        Problem = rt.models.checkdata.Problem
        if delete:
            # if obj is None:
            #     flt = {
            #         Problem.owner.ct_field.name + "__isnull": True,
            #         Problem.owner.fk_field.name + "__isnull": True
            #     }
            # else:
            #     flt = gfk2lookup(Problem.owner, obj, checker=self)
            flt = gfk2lookup(Problem.owner, obj, checker=self)
            qs = Problem.objects.filter(**flt)
            qs.delete()

        done = []
        todo = []
        for fixable, msg in self.get_checkdata_problems(obj, fix):
            if fixable:
                # attn: do not yet translate
                # msg = string_concat(u"(\u2605) ", msg)
                msg = format_lazy("(\u2605) {}", msg)
            if fixable and fix:
                done.append(msg)
            else:
                todo.append(msg)
        if len(todo):
            # dd.logger.info("%s : %s", obj, todo)
            user = self.get_responsible_user(obj)
            if user is None:
                lang = dd.get_default_language()
            else:
                lang = user.language
            with translation.override(lang):
                if obj is None:
                    for msg in todo:
                        prb = Problem(message=str(msg), checker=self, user=user)
                        prb.full_clean()
                        prb.save()
                else:
                    msg = '\n'.join([str(s) for s in todo])
                    prb = Problem(owner=obj, message=msg, checker=self, user=user)
                    prb.full_clean()
                    prb.save()
        return (todo, done)

    def get_checkdata_problems(self, obj, fix=False):
        return []

    def get_responsible_user(self, obj):
        return dd.plugins.checkdata.get_responsible_user(self, obj)


class Checkers(dd.ChoiceList):
    required_roles = dd.login_required(SiteStaff)
    verbose_name = _("Data checker")
    verbose_name_plural = _("Data checkers")
    item_class = Checker
    max_length = 250
    # e.g. "lino_welfare.modlib.pcsw.models.ClientCoachingsChecker"
    column_names = "value text"
    show_values = False

    detail_layout = """
    value text
    checkdata.ProblemsByChecker
    """


@dd.receiver(dd.pre_analyze)
def resolve_checkers(sender, **kw):
    for chk in Checkers.get_list_items():
        chk.resolve_model(sender)
