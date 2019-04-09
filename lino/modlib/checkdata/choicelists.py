# Copyright 2015-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Choicelists for `lino.modlib.checkdata`.


"""

from __future__ import unicode_literals, print_function
from builtins import str
import six

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
    """Base class for the choices of :class:`Checkers`.

    """
    verbose_name = None
    severity = None
    self = None
    model = None
    """
    The model to be checked.  If this is a string, Lino will resolve it at startup.
      
    If this is an abstract model, :meth:`get_checkable_models`  will
    potentially yield more than one model.
    
    If this is `None`, the checker is unbound, i.e. the problem messages will
    not be bound to a particular database object.
    
    You might also define your own
    :meth:`get_checkable_models` method.

    """

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
        """Application developers must call this on their subclass in order to
        "register" or "activate" it.

        This actually just creates an instance and adds it as a choice
        to the :class:`Checkers` choicelist.

        """
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
        """
        Run :meth:`get_checkdata_problems` on this checker for the given
        instance.
        """
        return cls.self.get_checkdata_problems(*args, **kwargs)
        
    def get_checkable_models(self):
        """Return a list of the models to check.

        The default implementation uses the :attr:`model`.
        """
        if self.model is None:
            return [None]
        return rt.models_by_base(self.model, toplevel_only=True)

    def resolve_model(self, site):
        if isinstance(self.model, six.string_types):
            self.model = dd.resolve_model(self.model, strict=True)

    def update_problems(self, obj=None, delete=True, fix=False):
        """Update the problems of this checker for the specified object.

        ``obj`` is `None` on unbound checkers.

        When `delete` is False, the caller is responsible for deleting
        any existing objects.

        """
        Problem = rt.models.checkdata.Problem
        if delete:
            qs = Problem.objects.filter(
                **gfk2lookup(Problem.owner, obj, checker=self))
            qs.delete()

        done = []
        todo = []
        for fixable, msg in self.get_checkdata_problems(obj, fix):
            if fixable:
                # attn: do not yet translate
                # msg = string_concat(u"(\u2605) ", msg)
                msg = format_lazy(u"(\u2605) {}", msg)
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
                msg = '\n'.join([str(s) for s in todo])
            prb = Problem(owner=obj, message=msg, checker=self, user=user)
            prb.full_clean()
            prb.save()
        return (todo, done)

    def get_checkdata_problems(self, obj, fix=False):
        """Return or yield a series of `(fixable, message)` tuples, each
        describing a data problem. `fixable` is a boolean
        saying whether this problem can be automatically fixed. And if
        `fix` is `True`, this method is also responsible for fixing
        it.

        """
        return []

    def get_responsible_user(self, obj):
        """The :attr:`user <lino.modlib.checkdata.models.Problem.user>` to
        be considered responsible for problems detected by this
        checker on the given database object `obj`.

        The given `obj` will always be an instance of :attr:`model`.

        The default implementation returns the *main checkdata
        responsible* defined for this site (see
        :attr:`responsible_user
        <lino.modlib.checkdata.Plugin.responsible_user>`).

        """
        return dd.plugins.checkdata.get_responsible_user(self, obj)


class Checkers(dd.ChoiceList):
    """The list of data problem types known by this application.

    This was the first use case of a :class:`ChoiceList
    <lino.core.choicelists.ChoiceList>` with a :attr:`detail_layout
    <lino.core.actors.Actor.detail_layout>`.

    """
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
