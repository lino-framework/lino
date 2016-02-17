# Copyright 2012 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Not used.
"""
from builtins import str
from builtins import object

#~ raise Exception("Not used")

import logging
logger = logging.getLogger(__name__)

import cgi

from django.conf import settings
#~ from django.contrib.auth import models as auth
#~ from django.contrib.sessions import models as sessions
from django.contrib.contenttypes import models as contenttypes
from django.utils.encoding import force_text

#~ from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

import lino
from lino import mixins
from lino.api import dd, rt
#~ from lino import commands
from lino.core import actors
from lino.mixins import printable
#~ from lino import choices_method, simple_choices_method
from lino.core.utils import obj2str, sorted_models_list
from lino.core.utils import resolve_field
from lino.utils.choosers import chooser
from lino.core import actions
#~ from lino.utils.choicelists import UserLevel, UserGroup
#~ from lino.modlib.users.models import UserLevel, UserGroup

#~ from lino.modlib.users.models

MODULE_LABEL = _("Workflows")

#~ WORKFLOWABLE_ACTORS = dict()
#~ WORKFLOWABLE_CONTENTTYPES = []


def action_text(a):
    return "%s (%s)" % (a.name, str(a.label))

if settings.SITE.user_model and settings.SITE.is_installed('contenttypes'):

    #~ class Rule(mixins.Duplicable,mixins.Sequenced):
    class Rule(mixins.Sequenced):
        #~ class Meta:
            #~ sort_order = ['content_type','seqno']

        #~ content_type = models.ForeignKey(contenttypes.ContentType)
        #~ app_name = models.CharField(_("Module"),max_length=50)
        #~ actor_name = models.CharField(_("Actor"),max_length=50)
        actor_name = models.CharField(
            _("Actor"), max_length=settings.SITE.max_actor_name_length)
        action_name = models.CharField(_("Action"),
                                       max_length=settings.SITE.max_action_name_length,
                                       blank=True,
            help_text="""
          The action to allow if this rule applies.
          If this is empty, the permission applies for all workflow actions of the actor.
          """)
        state = models.CharField(
            _("State"), max_length=settings.SITE.max_state_value_length,
            blank=True,
            help_text="""
          Permission applies only for objects in the given state.
          If this is empty, the permission applies for all states.
          """)
        #~ state_after = models.CharField(_("State after"),max_length=20)
        user_level = dd.UserLevels.field(blank=True,
            help_text="""
          If not empty, this permission applies only for users having at least the given level.
          """)
        # ~ user_groups = UserGroup.field(max_length=200,blank=True,force_selection=False) # TODO: multiple=True
        user_group = dd.UserGroups.field(
            help_text="""
          If not empty, this permission applies only for members of the given group.
          """)  # TODO: multiple=True
        #~ user_groups = models.CharField(_("user groups"),max_length=200,blank=True)
        owned_only = models.BooleanField(_("owned only"), default=False,
            help_text="""
          Allow this action only for objects owned by the user
          """)

        #~ def get_siblings(self):
            #~ "Overrides :meth:`lino.mixins.Sequenced.get_siblings`"
            #~ return self.__class__.objects.filter(actor_name=self.actor_name).order_by('seqno')

        @chooser()
        def actor_name_choices(cls):
            #~ return WORKFLOWABLE_ACTORS.items()
            #~ return settings.SITE.workflow_actors.items()
            return settings.SITE.workflow_actor_choices

        def get_actor_name_display(self, value):
            return str(value)

        #~ @chooser()
        #~ def content_type_choices(cls):
            #~ return WORKFLOWABLE_CONTENTTYPES

        #~ @chooser(multiple=True)
        #~ def state_before_choices(cls,content_type):
            #~ return cls.state_choices(content_type)
        @chooser()
        def action_name_choices(cls, actor_name):
            choices = []
            if not actor_name:
                return choices
            actor = settings.SITE.workflow_actors.get(actor_name)
            if actor is None:
                return choices
            #~ actor = WORKFLOWABLE_ACTORS.get(actor_name)
            for a in actor.workflow_actions:
                choices.append((a.name, action_text(a)))
            return choices

        def get_action_name_display(self, action_name):
            actor = settings.SITE.workflow_actors.get(self.actor_name)
            if actor is None:
                return ''
            a = getattr(actor, action_name)
            return action_text(a)

        @chooser()
        def state_choices(cls, actor_name):
            choices = []
            if not actor_name:
                return choices
            actor = settings.SITE.workflow_actors.get(actor_name)
            if actor is None:
                return choices
            return actor.workflow_state_field.choices

        #~ def get_state_after_display(self,value):
            #~ return self.get_state_display(value)
        def get_state_display(self, value):
            actor = settings.SITE.workflow_actors.get(self.actor_name)
            if actor is None:
                return ''
            return actor.workflow_state_field.choicelist.get_text_for_value(value)

            #~ if self.content_type is not None:
                #~ model = self.content_type.model_class()
                #~ return model.workflow_state_field.choicelist.get_text_for_value(value)
            #~ return ''

        #~ def get_permission(self,user):
            #~ """
            #~ Returns True if this Workflow is enabled for the given `user`.
            #~ """
            #~ vp = ViewPermissionInstance(required_user_level=self.user_level)
            #~ if self.user_group:
                #~ vp.required_user_groups = [self.user_group.value]
            #~ return vp.get_view_permission(user)
    class Rules(dd.Table):
        model = Rule
        column_names = "actor_name:20 action_name:20 state user_level user_group owned_only *"
        #~ detail_layout = """
        #~ content_type seqno id
        #~ name
        #~ user_level user_groups owned_only
        #~ state_before state_after
        #~ """


    #~ class Workflowable(actors.Actor):
        #~ """
        #~ Mixin for Actors that are aware of workflows.
        #~ """
        #~ class Meta:
            #~ abstract = True
else:

    # dummy classes for sites without contenttypes
    class Rule(object):
        pass

    class Rules(object):
        pass


def site_setup(site):
    site.workflow_actors = dict()


def setup_config_menu(config, site, profile, m):
    m = m.add_menu("workflows", MODULE_LABEL)
    m.add_action(Rules)


