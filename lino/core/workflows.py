    # -*- coding: UTF-8 -*-
# Copyright 2012-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
Defines the classes used for defining workflows.  See
:doc:`/dev/workflows`.
"""
from builtins import str
import six

from django.utils.functional import Promise
from django.utils.translation import ugettext_lazy as _
from django.utils.text import format_lazy
from django.db import models

from lino.core import actions
from lino.core import choicelists
from lino.core.utils import models_by_base

# from django.utils.encoding import force_text
# from django.utils.functional import lazy
# def _string_format(tpl, *args, **kwargs):
#     args = tuple([force_text(s) for s in args])
#     return tpl.format(*args, **kwargs)
# string_format = lazy(_string_format, basestring)


class State(choicelists.Choice):
    """
    A `State` is a specialized :class:`Choice
    <lino.core.choicelists.Choice>` that adds the
    :meth:`add_transition` method.

    .. attribute:: button_text

        The text to appear on buttons representing this state.

    """

    button_text = None

    def add_transition(self, label=None,
                       help_text=None,
                       notify=False,
                       name=None,
                       #~ icon_file=None,
                       icon_name=None,
                       debug_permissions=None,
                       required_states=None,
                       required_roles=None):
        """
        Declare an transition action which makes an object enter this
        state.

        `label` can be a string, a subclass of
        :class:`ChangeStateAction` or `None`. If it is `None`, then
        the state's :attr:`button_text` or :attr:`text
        <lino.core.choicelists.Choice.text>` will be used as label.

        You can specify an explicit `name` in order to allow replacing
        the transition action later by another action.  Otherwise Lino
        will generate an internal name.
        """
        workflow_actions = self.choicelist.workflow_actions
        i = len(workflow_actions)
        
        kw = dict()
        if help_text is not None:
            kw.update(help_text=help_text)
        if icon_name is not None:
            kw.update(icon_name=icon_name)
        kw.update(sort_index=200 + i)
        if label and not isinstance(label, (six.string_types, Promise)):
            # it's a subclass of ChangeStateAction
            assert isinstance(label, type)
            assert issubclass(label, ChangeStateAction)
            if name is None:
                name = label.action_name
            if required_roles:
                raise Exception(
                    "Cannot specify requirements when using your own class")
            if required_states:
                raise Exception(
                    "Cannot specify requirements when using your own class")
            if notify:
                raise NotImplementedError(
                    "Cannot specify notify=True when using your own class")
            if debug_permissions:
                raise Exception(
                    "Cannot specify debug_permissions "
                    "when using your own class")
            for a in workflow_actions:
                if isinstance(a, label):
                    raise Exception("Duplicate transition label %s" % a)
            a = label(self, **kw)
        else:
            if required_states:
                kw.update(required_states=required_states)
            if notify:
                raise NotImplementedError(
                    "Since 20160718 you must write your own action "
                    "class if you want it to be notifying.")
                # cl = NotifyingChangeStateAction
            else:
                cl = ChangeStateAction
            if label is None:
                label = self.button_text or self.text
            a = cl(self, required_roles, label=label, **kw)
            if debug_permissions:
                a.debug_permissions = debug_permissions

        if name is None:
            #~ name = 'mark_' + self.value
            name = 'wf' + str(i + 1)
        
        for x in workflow_actions:
            if x.action_name == name:
                raise Exception(
                    "Duplicate transition name {0}".format(name))
    
        a.attach_to_workflow(self.choicelist, name)

        self.choicelist.workflow_actions = workflow_actions + [a]

    # add_workflow = add_transition  # backwards compat


class Workflow(choicelists.ChoiceList):
    """
    A workflow is a specialized choicelist used for defining the
    states of a workflow.  Every choice is an instance of
    :class:`State`.

    .. attribute:: verbose_name

        The translatable designation for a given state in this workflow.

    .. attribute:: verbose_name_plural

        The translatable designation for the set of existing states in this workflow.

        The default value for this is built during startup: if the workflow is
        being used on a single model (which is the case for most workflows),
        the default text is "{} states" where {} is the model's verbose name.


    """
    item_class = State

    verbose_name = _("State")
    # verbose_name_plural = _("States")
    verbose_name_plural = None
    button_text = models.CharField(_("Button text"), blank=True)
    column_names = "value name text button_text"
    abstract = True

    @classmethod
    def on_analyze(cls, site):
        """
        Add workflow actions to the models which use this workflow so that
        we can access them as InstanceActions.
        """
        super(Workflow, cls).on_analyze(site)
        if cls.abstract:
            return
        # logger.info("20150602 Workflow.on_analyze %s", cls)
        used_on_models = []
        for fld in cls._fields:
            model = getattr(fld, 'model', None)
            if model:
                used_on_models.append(model)
                # logger.info("20150602 %s, %s", model, cls.workflow_actions)
                for a in cls.workflow_actions:
                    # if not a.action_name.startswith('wf'):
                    if not hasattr(model, a.action_name):
                        setattr(model, a.action_name, a)
        if cls.verbose_name_plural is None:
            if len(used_on_models) == 1:
                concrete_models = list(models_by_base(used_on_models[0]))
                if len(concrete_models) == 1:
                    m = concrete_models[0]
                else:
                    m = used_on_models[0]
                name = m._meta.verbose_name
                cls.verbose_name_plural = format_lazy(_("{} states"), name)
            # elif len(used_on_models) > 1:
            #     raise Exception(
            #         "20190103 {} is used in more than one model : {}".format(
            #             cls, used_on_models))
            else:
                cls.verbose_name_plural = _("States")
        cls.sort()


    @classmethod
    def before_state_change(cls, obj, ar, oldstate, newstate):
        pass

    @classmethod
    def after_state_change(cls, obj, ar, oldstate, newstate):
        pass

    @classmethod
    def override_transition(cls, **kw):
        """
        """
        for name, cl in kw.items():
            found = False
            for i, a in enumerate(cls.workflow_actions):
                if a.action_name == name:
                    new = cl(
                        a.target_state, a.required_roles,
                        sort_index=a.sort_index)
                    new.attach_to_workflow(cls, name)
                    cls.workflow_actions[i] = new
                    found = True
                    break
            if not found:
                raise Exception(
                    "There is no workflow action named {0}".format(name))

    @classmethod
    def clear_transitions(cls):
        assert cls._state_to_disabled_actions is None
        cls.workflow_actions = []
        

class ChangeStateAction(actions.Action):
    """
    This is the class used when generating automatic "state
    actions". For each possible value of the Actor's
    :attr:`workflow_state_field` there will be an automatic action
    called `mark_XXX`
    """

    show_in_bbar = False
    show_in_workflow = True
    readonly = False
    # sort_index = 200

    def __init__(self, target_state, required_roles=None,
                 help_text=None, **kw):
        self.target_state = target_state
        assert 'required' not in kw
        assert 'required_roles' not in kw
        new_required = set(self.required_roles)
        if required_roles is not None:
            new_required |= required_roles
        kw.update(required_roles=new_required)
        if self.help_text is None:
            if help_text is None:
                # help_text = string_format(
                #     _("Mark this as {0}"), target_state.text)
                # help_text = string_concat(
                #     _("Mark this as"), ' ', target_state.text)
                help_text = target_state.text
            kw.update(help_text=help_text)

        super(ChangeStateAction, self).__init__(**kw)
        #~ logger.info('20120930 ChangeStateAction %s %s', actor,target_state)
        if self.label is None:
            self.label = target_state.text
            
        if self.button_text is None:
            self.button_text = target_state.button_text

        if self.icon_name:
            self.help_text = format_lazy(u"{}. {}",self.label,self.help_text)

    # def get_action_permission(self, ar, obj, state):
    #     if not super(ChangeStateAction, self).get_action_permission(ar, obj, state):
    #         return False
    #     if state.value == self.target_state.value:
    #         return False
    #     return True


    def run_from_ui(self, ar):
        # print(20170116, ar.action_param_values)
        for row in ar.selected_rows:
            self.execute(ar, row)
        ar.set_response(refresh=True)
        ar.success()

    confirmation_msg_template = None

    def get_confirmation_msg_context(self, ar, obj, **kwargs):
        kwargs.update(
            user=ar.get_user(),
            state=self.target_state)
        return kwargs

    def before_execute(self, ar, obj):
        """This may raise a Warning with a user message to prevent execution.

        Usage example : lino_noi.lib.noi.workflows.MarkVoteassigned.

        """
        pass
    
    def execute(self, ar, obj):
        def doit(ar):
            self.before_execute(ar, obj)
            obj.set_workflow_state(
                ar,
                ar.actor.workflow_state_field,
                self.target_state)
            
        
        
        if self.confirmation_msg_template is None:
            doit(ar)
        else:
            ctx = self.get_confirmation_msg_context(ar, obj)
            msg = self.confirmation_msg_template.format(**ctx)
            ar.confirm(doit, msg, _("Are you sure?"))

