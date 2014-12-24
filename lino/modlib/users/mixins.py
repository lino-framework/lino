# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
:class:`UserLevels`
:class:`UserGroups`
:class:`UserProfiles`

:class:`AnonymousUser`
:class:`UserAuthored`

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.db.models.fields import NOT_PROVIDED

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.conf import settings


from lino.core.choicelists import ChoiceList, Choice

from lino.core import fields
from lino.core import model
from lino.core import workflows
from lino.core import actions
from lino.core import dbtables
from lino.core.dbutils import obj2str


class UserLevel(Choice):
    short_name = None


class UserLevels(ChoiceList):
    "See :class:`ml.users.UserLevels`."

    verbose_name = _("User Level")
    verbose_name_plural = _("User Levels")
    required = settings.SITE.get_default_required(user_level='admin')
    short_name = models.CharField(
        _("Short name"), max_length=2,
        help_text=_("Used when defining UserProfiles"))

    @classmethod
    def get_column_names(self, ar):
        return 'value name short_name text remark'

    @classmethod
    def field(cls, module_name=None, **kw):
        """
        Extends :meth:`lino.core.fields.ChoiceListField.field` .
        """
        kw.setdefault('blank', True)
        if module_name is not None:
            kw.update(verbose_name=string_concat(
                cls.verbose_name, ' (', module_name, ')'))
        return super(UserLevels, cls).field(**kw)


add = UserLevels.add_item
add('10', _("Guest"), 'guest', short_name='G')
add('30', _("User"), "user", short_name='U')
add('40', _("Manager"), "manager", short_name='M')
add('50', _("Administrator"), "admin", short_name='A')
UserLevels.SHORT_NAMES = dict(
    A='admin', U='user', _=None, M='manager', G='guest')


class UserProfile(Choice):

    hidden_languages = None
    """
    A subset of :setting:`languages`
    which should be hidden in this user profile.
    Default value is :attr:`hidden_languages <UserProfiles.hidden_languages>`.
    This is used on multilingual sites with more than 4 or 5 languages.
    See the source code of :meth:`lino_welfare.settings.Site.setup_choicelists`
    for a usage example.
    """

    def __init__(self, cls, value, text,
                 name=None, memberships=None, authenticated=True,
                 readonly=False,
                 #~ expert=False,
                 **kw):

        super(UserProfile, self).__init__(value, text, name)
        #~ keys = ['level'] + [g+'_level' for g in choicelist.groups_list]
        #~ keys = ['level'] + [g+'_level' for g in choicelist.membership_keys]
        self.readonly = readonly
        #~ self.expert = expert
        self.authenticated = authenticated
        self.memberships = memberships
        self.kw = kw

    def attach(self, cls):
        super(UserProfile, self).attach(cls)
        self.kw.setdefault('hidden_languages', cls.hidden_languages)
        if self.memberships is None:
            for k in cls.membership_keys:
                #~ kw[k] = UserLevels.blank_item
                #~ kw.setdefault(k,UserLevels.blank_item) 20120829
                self.kw.setdefault(k, None)
        else:
        #~ if memberships is not None:
            if len(self.memberships.split()) != len(cls.membership_keys):
                raise Exception(
                    "Invalid memberships specification %r : "
                    "must contain %d letters"
                    % (self.memberships, len(cls.membership_keys)))
            for i, k in enumerate(self.memberships.split()):
                self.kw[cls.membership_keys[i]
                        ] = UserLevels.get_by_name(UserLevels.SHORT_NAMES[k])

        #~ print 20120705, value, kw

        assert 'level' in self.kw

        for k, vf in cls.virtual_fields.items():
            if vf.has_default():
                self.kw.setdefault(k, vf.get_default())
            elif vf.return_type.blank:
                self.kw.setdefault(k, None)

        for k, v in self.kw.items():
            setattr(self, k, v)

        for k in cls.default_memberships:
            setattr(self, k, self.level)

        if self.hidden_languages is not None:
            self.hidden_languages = set(
                settings.SITE.resolve_languages(self.hidden_languages))

        del self.kw
        del self.memberships

    def __repr__(self):
        #~ s = self.__class__.__name__
        s = str(self.choicelist)
        if self.name:
            s += "." + self.name
        s += ":" + self.value + "("
        #~ s += "level=%s" % self.level.name
        s += "level=%s" % self.level
        for g in UserGroups.items():
            if g.value:  # no level for UserGroups.blank_item
                v = getattr(self, g.value + '_level', None)
                if v is not None:
                    s += ",%s=%s" % (g.value, v.name)
        s += ")"
        return s


class UserProfiles(ChoiceList):
    "See :class:`ml.users.UserProfiles`."
    required = settings.SITE.get_default_required(user_level='admin')
    #~ item_class = UserProfile
    verbose_name = _("User Profile")
    verbose_name_plural = _("User Profiles")
    show_values = True
    max_length = 20
    membership_keys = ('level',)

    preferred_foreignkey_width = 20

    hidden_languages = settings.SITE.hidden_languages
    """Default value for the :attr:`hidden_languages
    <UserProfile.hidden_languages>` of newly attached choice item.

    """

    level = UserLevels.field(_("System"))

    @classmethod
    def reset(cls, groups=None, hidden_languages=None):
        """
        Deserves a docstring.
        """
        if hidden_languages is not None:
            cls.hidden_languages = hidden_languages
        expected_names = set(
            ['*'] + [g.value for g in UserGroups.items() if g.value])
        if groups is None:
            groups = ' '.join(expected_names)
        s = []
        for g in groups.split():
            if not g in expected_names:
                raise Exception("Unexpected name %r (UserGroups are: %s)" % (
                    g, [g.value for g in UserGroups.items() if g.value]))
            else:
                expected_names.remove(g)
                if g == '*':
                    s.append('level')
                else:
                    if not UserGroups.get_by_value(g):
                        raise Exception("Unknown group %r" % g)
                    s.append(g + '_level')
        #~ if len(expected_names) > 0:
            #~ raise Exception("Missing name(s) %s in %r" % (expected_names,groups))
        cls.default_memberships = expected_names
        cls.membership_keys = tuple(s)
        cls.clear()

    @classmethod
    def add_item(cls, value, text, memberships=None, name=None, **kw):
        return cls.add_item_instance(UserProfile(
            cls, value, text, name, memberships, **kw))

#~ UserProfiles choicelist is going to be filled in `lino.core.site_def.Site.setup_choicelists`
#~ because the attributes of each item depend on UserGroups


class UserGroups(ChoiceList):
    "See :class:`ml.users.UserGroups`."

    required = settings.SITE.get_default_required(user_level='admin')
    verbose_name = _("User Group")
    verbose_name_plural = _("User Groups")
    show_values = True
    max_length = 20
    """
    """

# add = UserGroups.add_item
# add('system', _("System"))
# filled using add_user_group()


def add_user_group(name, label):
    """
    Add a user group to the :class:`UserGroups <lino.core.perms.UserGroups>` 
    choicelist. If a group with that name already exists, add `label` to the 
    existing group.
    """
    #~ logging.info("add_user_group(%s,%s)",name,label)
    #~ print "20120705 add_user_group(%s,%s)" % (name,unicode(label))
    g = UserGroups.items_dict.get(name)
    if g is None:
        g = UserGroups.add_item(name, label)
    else:
        if g.text != label:
            g.text += " & " + unicode(label)
    #~ if False:
        # TODO: 'UserProfile' object has no attribute 'accounting_level'
    k = name + '_level'
    UserProfiles.inject_field(k, UserLevels.field(g.text, blank=True))
    UserProfiles.virtual_fields[k].lino_resolve_type()


def make_permission_handler(*args, **kw):
    """Return a function that will test whether permission is given or not.
    
    `elem` is not used (either an Action or a Permittable.)
    
    `actor` is who contains the workflow state field
    
    `readonly`
    
    `debug_permissions`
    
    The generated function will always expect three arguments user, obj and state.
    The latter two may be None depending on the context
    (for example a read_required is expected to not test on obj or 
    state because these values are not known when generating the 
    :xfile:`lino*.js` files.).
    
    The remaining keyword arguments are aka "requirements":
    
    `user_level`

        A string (e.g. ``'manager'``, ``'user'``,...)

        The minimum user level required to get the permission.  The
        default value `None` means that no special user level is
        required.
        
        When `user_groups` is not specified, then the profile's
        default level (`UserProfile.level`) is being tested, otherwise
        the userlevel for the group membership.
        E.g. `dd.required(user_level='manager',user_groups='integ')`
        will pass when `profile.level` is "user" and
        `profile.integ_level` is "manager"
        
        
    `user_groups`

        List of strings naming the user groups for which membership is
        required to get permission to view this Actor.  The default
        value `None` means that no special group membership is
        required.  Alternatively, if this is a string, it will be
        converted to a list of strings.
        
    `states`
        List of strings naming the user groups for which membership is required 
    
    `allow`
        An additional custom permission handler
        
    `auth`
        If True, permission is given for any authenticated user 
        (and not for :class:`AnonymousUser`).
        
    `owner`
        If True, permission is given only to the author of the object. 
        If False, permission is given only to users who are not the author of the object. 
        This requirement is allowed only on models that have a field `user` 
        which is supposed to contain the author.
        Usually a subclass of :class:`lino.modlib.users.mixins.UserAuthored`,
        but e.g. :class:`lino.modlib.cal.models.Guest` 
        defines a property `user` because it has no own `user` field).

    """
    #~ try:
    return make_permission_handler_(*args, **kw)
    #~ except Exception,e:
        #~ raise Exception("Exception while making permissions for %s: %s" % (actor,e))


def make_view_permission_handler(*args, **kw):
    """
    Similar to :func:`make_permission_handler`, but for static view permissions 
    which don't have an object nor states.
    """
    return make_view_permission_handler_(*args, **kw)


def make_view_permission_handler_(
        actor, readonly, debug_permissions,
        user_level=None, user_groups=None,
        allow=None, auth=False, owner=None, states=None):
    #~ if states is not None:
        #~ logger.info("20121121 ignoring required states %s for %s",states,actor)
    #~ if owner is not None:
        #~ logger.info("20121121 ignoring required owner %s for %s",owner,actor)
    #~ if allow is None:
    if allow is not None:
        if not isinstance(actor.action, workflows.ChangeStateAction):
            raise Exception("20130724 %s" % actor)
    if True:
        # ignore `allow` requirement for view_permission because
        # workflows.Choice.add_transition
        def allow(action, profile):
            return True
    # if settings.SITE.user_model is not None:
    if True:  # e.g. public readonly site
        if auth:
            allow_before_auth = allow

            def allow(action, profile):
                if not profile.authenticated:
                    return False
                return allow_before_auth(action, profile)

        if user_groups is not None:
            if isinstance(user_groups, basestring):
                user_groups = user_groups.split()
            if user_level is None:
                user_level = UserLevels.user
            else:
                user_level = getattr(UserLevels, user_level, None)
                if user_level is None:
                    raise Exception("Invalid user_level %r for %s" %
                                    (user_level, actor))
            for g in user_groups:
                # raise Exception if no such group exists
                UserGroups.get_by_value(g)
                #~ if not UserGroups.get_by_name(g):
                    #~ raise Exception("Invalid UserGroup %r" % g)
            allow1 = allow

            def allow(action, profile):
                if not allow1(action, profile):
                    return False
                for g in user_groups:
                    level = getattr(profile, g + '_level', NOT_PROVIDED)
                    if level is NOT_PROVIDED:
                        # We need to report the guilty actor,
                        # otherwise it is difficult to locate the error.
                        raise Exception(
                            "user_group '%s' required by %s does not exist" %
                            (g, actor))
                        return False
                    if level >= user_level:
                        return True
                    #~ elif debug_permissions:
                        #~ logger.info("20130704 level %r < %r",level,user_level)
                return False

        elif user_level is not None:
            user_level = getattr(UserLevels, user_level)
            allow_user_level = allow

            def allow(action, profile):
                if profile.level < user_level:
                    return False
                return allow_user_level(action, profile)

    if not readonly:
        allow3 = allow

        def allow(action, profile):
            if not allow3(action, profile):
                return False
            if profile.readonly:
                return False
            return True

    if debug_permissions:  # False:
        #~ logger.info("20130424 install debug_permissions for %s",
            #~ [actor,readonly,debug_permissions,
            #~ user_level,user_groups,allow,auth,owner,states])
        allow4 = allow

        def allow(action, profile):
            v = allow4(action, profile)
            if True:  # not v:
                logger.info(
                    u"debug_permissions (view) %r required(%s,%s), allow(%s)--> %s",
                    action, user_level, user_groups, profile, v)
            return v
    return allow


def make_permission_handler_(
    elem, actor, readonly, debug_permissions,
        user_level=None, user_groups=None,
        allow=None, auth=False, owner=None, states=None):

    #~ if str(actor) == 'courses.PendingCourseRequests':
        #~ if allow is None: raise Exception("20130424")

    # ~ if debug_permissions: # False:
        #~ logger.info("20130424 install debug_permissions for %s",
            #~ [elem,actor,readonly,debug_permissions,
            #~ user_level,user_groups,states,allow,owner,auth])

    if allow is None:
        def allow(action, user, obj, state):
            return True
    # if settings.SITE.user_model is not None:
    if True:  # e.g. public readonly site
        if auth:
            allow_before_auth = allow

            def allow(action, user, obj, state):
                if not user.profile.authenticated:
                    #~ if action.action_name == 'wf7':
                        #~ logger.info("20130424 allow_before_auth returned False")
                    return False
                return allow_before_auth(action, user, obj, state)

        if owner is not None:
            allow_owner = allow

            def allow(action, user, obj, state):
                if obj is not None and (user == obj.user) != owner:
                    #~ if action.action_name == 'wf7':
                        #~ logger.info("20130424 allow_owner returned False")
                    return False
                return allow_owner(action, user, obj, state)

        if user_groups is not None:
            if isinstance(user_groups, basestring):
                user_groups = user_groups.split()
            if user_level is None:
                user_level = UserLevels.user
            else:
                user_level = getattr(UserLevels, user_level)
            for g in user_groups:
                # raise Exception if no such group exists
                UserGroups.get_by_value(g)
                #~ if not UserGroups.get_by_name(g):
                    #~ raise Exception("Invalid UserGroup %r" % g)
            allow1 = allow

            def allow(action, user, obj, state):
                if not allow1(action, user, obj, state):
                    #~ if action.action_name == 'wf7':
                        #~ logger.info("20130424 allow1 returned False")
                    return False
                for g in user_groups:
                    level = getattr(user.profile, g + '_level')
                    if level >= user_level:
                        return True
                return False

        elif user_level is not None:
            user_level = getattr(UserLevels, user_level)
            allow_user_level = allow

            def allow(action, user, obj, state):
                #~ if user.profile.level is None or user.profile.level < user_level:
                if user.profile.level < user_level:
                    #~ print 20120715, user.profile.level
                    #~ if action.action_name == 'wf7':
                        #~ logger.info("20130424 allow_user_level returned False")
                    return False
                return allow_user_level(action, user, obj, state)

    if states is not None:
        #~ if not isinstance(actor.workflow_state_field,choicelists.ChoiceListField):
        if actor.workflow_state_field is None:
            raise Exception(
                """\
%s cannot specify `states` when %s.workflow_state_field is %r.
                """ % (elem, actor, actor.workflow_state_field))
        #~ else:
            #~ print 20120621, "ok", actor
        lst = actor.workflow_state_field.choicelist
        #~ states = frozenset([getattr(lst,n) for n in states])
        #~ possible_states = [st.name for st in lst.items()] + [BLANK_STATE]
        ns = []
        if isinstance(states, basestring):
            states = states.split()
        for n in states:
            if n is not None:
                if n == '_':
                    n = None
                else:
                    n = lst.get_by_name(n)
            ns.append(n)
            #~ if n:
                #~ ns.append(getattr(lst,n))
            #~ else:
                #~ ns.append(lst.blank_item)

            #~ if not st in possible_states:
                #~ raise Exception("Invalid state %r, must be one of %r" % (st,possible_states))
        states = frozenset(ns)
        allow2 = allow
        #~ if debug_permissions:
            #~ logger.info("20121009 %s required states: %s",actor,states)

        def allow(action, user, obj, state):
            if not allow2(action, user, obj, state):
                return False
            if obj is None:
                return True
            return state in states
    #~ return perms.Permission(allow)

    if not readonly:
        allow3 = allow

        def allow(action, user, obj, state):
            if not allow3(action, user, obj, state):
                return False
            if user.profile.readonly:
                return False
            return True

    if debug_permissions:  # False:
        allow4 = allow

        def allow(action, user, obj, state):
            v = allow4(action, user, obj, state)
            logger.info(
                u"debug_permissions %r required(%s,%s,%s), allow(%s,%s,%s)--> %s",
                action, user_level, user_groups, states, user.username, obj2str(obj), state, v)
            return v
    return allow


class AnonymousUser(object):

    """
    Similar to Django's approach to represent anonymous visitors
    as a special kind of user.
    """
    #~ authenticated = False
    email = None
    username = 'anonymous'
    modified = None
    partner = None
    language = None
    #~ id = None
    pk = None

    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = AnonymousUser()
            try:
                cls._instance.profile = UserProfiles.get_by_value(
                    settings.SITE.anonymous_user_profile)
                
                # if cls._instance.profile.authenticated:
                #     logger.warning(
                #         "20121121 profile specified by \
                #         `anonymous_user_profile` is `authenticated`")
            except KeyError:
                raise Exception(
                    "Invalid value %r for `SITE.anonymous_user_profile`. "
                    "Must be one of %s" % (
                        settings.SITE.anonymous_user_profile,
                        [i.value for i in UserProfiles.items()]))
        return cls._instance

    def __str__(self):
        return self.username

    def get_typed_instance(self, model):
        # 20131022 AttributeError at /api/outbox/MyOutbox : 'AnonymousUser'
        # object has no attribute 'get_typed_instance'
        return self


class UserAuthored(model.Model):

    """
    Mixin for models that have a `user` field which is automatically
    set to the requesting user.
    Also defines a `ByUser` base table which fills the master instance
    from the web request.
    """
    required = dict(auth=True)

    class Meta:
        abstract = True

    if settings.SITE.user_model:

        workflow_owner_field = 'user'

        user = models.ForeignKey(
            settings.SITE.user_model,
            verbose_name=_("Author"),
            related_name="%(app_label)s_%(class)s_set_by_user",
            blank=True, null=True
        )

    else:

        user = fields.DummyField()

    def on_create(self, ar):
        """
        Adds the requesting user to the `user` field.

        When acting as another user, the default implementation
        still inserts the real user, not subst_user.
        This is important for cal.Event.
        """
        if self.user_id is None:
            #~ u = ar.get_user()
            u = ar.user
            if u is not None:
                self.user = u
        super(UserAuthored, self).on_create(ar)

    manager_level_field = 'level'
    """Only system managers can edit other users' work.  But if the
    application defines customized UserGroups, then we may want to
    permit it also to department managers.  If an application defines
    a UserGroup `foo`, then it can set this attribute to `'foo_level'`
    on a model to specify that a manager level for the foo department
    is enough to get edit permission on other users' instances.
    
    Usage examples see
    :class:`lino.modlib.notes.models.Note`
    or
    :class:`lino.modlib.cal.models.Component`.

    """

    def get_row_permission(self, ar, state, ba):
        """
        Only system managers can edit other users' work.
        """
        if not super(UserAuthored, self).get_row_permission(ar, state, ba):
            #~ logger.info("20120919 no permission to %s on %s for %r",action,self,user)
            return False
        user = ar.get_user()
        if self.user != ar.user and \
           (ar.subst_user is None or self.user != ar.subst_user) \
           and getattr(user.profile, self.manager_level_field) < \
           UserLevels.manager:
            return ba.action.readonly
        return True

AutoUser = UserAuthored  # backwards compatibility


if settings.SITE.user_model:

    class ByUser(dbtables.Table):
        master_key = 'user'
        #~ details_of_master_template = _("%(details)s of %(master)s")
        details_of_master_template = _("%(details)s")

        @classmethod
        def get_actor_label(self):
            if self.model is None:
                return self._label or self.__name__
            return self._label or \
                _("My %s") % self.model._meta.verbose_name_plural

        @classmethod
        def setup_request(self, ar):
            #~ logger.info("ByUser.setup_request")
            if ar.master_instance is None:
                u = ar.get_user()
                if not isinstance(u, AnonymousUser):
                    ar.master_instance = u
            super(ByUser, self).setup_request(ar)

        @classmethod
        def get_view_permission(self, profile):
            if not profile.authenticated:
                return False
            return super(ByUser, self).get_view_permission(profile)

else:

    # dummy Table for userless sites
    class ByUser(dbtables.Table):
        pass


class AuthorAction(actions.Action):

    """
    """
    manager_level_field = 'level'

    def get_action_permission(self, ar, obj, state):
        user = ar.get_user()
        if obj.user != user and getattr(
                user.profile, self.manager_level_field) < UserLevels.manager:
            return self.readonly
        return super(
            AuthorAction, self).get_action_permission(ar, obj, state)


