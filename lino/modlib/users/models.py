# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for `lino.modlib.users`.

.. autosummary::

See also :doc:`/dev/users`

"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable)


from lino.api import dd
from lino.utils.xmlgen.html import E
from lino.core import actions

from lino.mixins import CreatedModified

from .choicelists import UserProfiles
from .mixins import UserAuthored


class ChangePassword(dd.Action):
    """Dialog action to change the password of a user.

    """
    label = _("Change password")
    parameters = dict(
        current=dd.PasswordField(_("Current password"), blank=True),
        new1=dd.PasswordField(_("New password"), blank=True),
        new2=dd.PasswordField(_("New password again"), blank=True)
    )
    params_layout = """
    current
    new1
    new2
    """

    def run_from_ui(self, ar, **kw):
        
        pv = ar.action_param_values
        if pv.new1 != pv.new2:
            ar.error("New passwords didn't match!")
            return
        count = 0
        for obj in ar.selected_rows:
            if not obj.has_usable_password() \
               or obj.check_password(pv.current):
                obj.set_password(pv.new1)
                obj.full_clean()
                obj.save()
                count += 1
            else:
                ar.info("Incorrect current password for %s." % obj)

        msg = _("New password has been set for %d users.") % count
        ar.success(msg, alert=True)


class User(CreatedModified):
    """Represents a user of this site.

    .. attribute:: username
    
        The primary key.

    .. attribute:: profile

        The profile of a user is what defines her or his permissions.

        Users with an empty `profile` field are considered inactive and
        cannot log in.


    .. attribute:: partner

        Pointer to the :class:`lino.modlib.contacts.models.Partner`
        instance related to this user.

        This is a DummyField when :mod:`lino.modlib.contacts` is not
        installed.

    """

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        abstract = dd.is_abstract_model(__name__, 'User')
        ordering = ['last_name', 'first_name']

    preferred_foreignkey_width = 15

    hidden_columns = 'password remarks'

    authenticated = True
    """This is always `True`.
    See also :attr:`lino.modlib.users.utils.AnonymousUser.authenticated`.
    """

    username = models.CharField(
        _('Username'), max_length=30,
        unique=True,
        help_text=_("""Required. Must be unique."""))

    password = models.CharField(_('Password'), max_length=128)

    profile = UserProfiles.field(
        blank=True,
        help_text=_("Users with an empty `profile` field are considered "
                    "inactive and cannot log in."))

    initials = models.CharField(_('Initials'), max_length=10, blank=True)
    first_name = models.CharField(_('First name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True)
    email = models.EmailField(_('e-mail address'), blank=True)

    remarks = models.TextField(_("Remarks"), blank=True)  # ,null=True)

    language = dd.LanguageField(default=models.NOT_PROVIDED, blank=True)

    if dd.is_installed('contacts'):

        partner = models.ForeignKey('contacts.Partner', blank=True, null=True)

    else:

        partner = dd.DummyField()

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        "Returns the first_name plus the last_name, with a space in between."
        if not self.first_name and not self.last_name:
            return self.username
        return u'%s %s' % (self.first_name.strip(), self.last_name.strip())

    @dd.displayfield(_("Name"), max_length=15)
    def name_column(self, request):
        #~ return join_words(self.last_name.upper(),self.first_name)
        return unicode(self)

    if dd.is_installed('contacts'):
        def get_person(self):
            if self.partner:
                return self.partner.get_mti_child('person')
    else:
        def get_person(self):
            return None

    person = property(get_person)

    def get_row_permission(self, ar, state, ba):
        """
        Only system managers may edit other users.
        See also :meth:`User.disabled_fields`.
        """
        #~ print 20120621, self, user, state, action
        if not ba.action.readonly:
            user = ar.get_user()
            if user != self:
                if not isinstance(user.profile.role, dd.SiteAdmin):
                    return False
        return super(User, self).get_row_permission(ar, state, ba)
        #~ return False

    def disabled_fields(self, ar):
        """
        Only System admins may change the `profile` of users.
        See also :meth:`Users.get_row_permission`.
        """
        rv = super(User, self).disabled_fields(ar)
        if not isinstance(ar.get_user().profile.role, dd.SiteAdmin):
            rv.add('profile')
        return rv

    def full_clean(self, *args, **kw):
        p = self.person
        if p is not None:
            for n in ('first_name', 'last_name', 'email', 'language'):
                if not getattr(self, n):
                    setattr(self, n, getattr(p, n))
            #~ self.language = p.language
        if not self.language:
            #~ self.language = settings.SITE.DEFAULT_LANGUAGE.django_code
            self.language = settings.SITE.get_default_language()
        if not self.password:
            self.set_unusable_password()
        if not self.initials:
            if self.first_name and self.last_name:
                self.initials = self.first_name[0] + self.last_name[0]
        super(User, self).full_clean(*args, **kw)

    def get_received_mandates(self):
        #~ return [ [u.id,_("as %s")%u] for u in self.__class__.objects.all()]
        return [[u.id, unicode(u)] for u in self.__class__.objects.all()]
        #~ return self.__class__.objects.all()

    change_password = ChangePassword()

    # the following methods are unchanged copies from Django's User
    # model

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            self.save()
        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        return is_password_usable(self.password)

    def as_list_item(self, ar):
        return E.li(E.strong(self.username), ' : ',
                    unicode(self), ', ',
                    unicode(self.profile), ', ',
                    E.strong(settings.SITE.LANGUAGE_DICT.get(self.language)))

    @classmethod
    def get_by_username(cls, username, default=models.NOT_PROVIDED):
        """
        `User.get_by_username(x)` is equivalent to
        `User.objects.get(username=x)` except that the text 
        of the DoesNotExist exception is more useful.
        """
        try:
            return cls.objects.get(username=username)
        except cls.DoesNotExist:
            if default is models.NOT_PROVIDED:
                raise cls.DoesNotExist(
                    "No %s with username %r" % (
                        unicode(cls._meta.verbose_name), username))
            return default


class UserDetail(dd.FormLayout):

    box1 = """
    username profile:20 partner
    first_name last_name initials
    email language
    id created modified
    """

    main = """
    box1 #MembershipsByUser:20
    remarks:40 AuthoritiesGiven:20
    """


class UserInsert(dd.FormLayout):

    window_size = (60, 'auto')

    main = """
    username email
    first_name last_name
    partner
    language profile
    """


class Users(dd.Table):
    help_text = _("""Shows the list of all users on this site.""")
    #~ debug_actions  = True
    required_roles = dd.required(dd.SiteAdmin)
    model = 'users.User'
    #~ order_by = "last_name first_name".split()
    order_by = ["username"]
    active_fields = 'partner'

    #~ column_names = 'username first_name last_name is_active is_staff is_expert is_superuser *'
    column_names = 'username profile first_name last_name *'
    detail_layout = UserDetail()
    insert_layout = UserInsert()

    #~ @classmethod
    #~ def get_row_permission(cls,action,user,obj):
        #~ """
        #~ Only system managers may edit other users.
        #~ See also :meth:`User.disabled_fields`.
        #~ """
        #~ if not super(Users,cls).get_row_permission(action,user,obj):
            #~ return False
        #~ if user.level >= UserLevel.manager: return True
        #~ if action.readonly: return True
        #~ if user is not None and user == obj: return True
        #~ return False


class MySettings(Users):
    use_as_default_table = False
    hide_top_toolbar = True
    required_roles = dd.required()
    default_list_action_name = 'detail'

    @classmethod
    def get_default_action(cls):
        return actions.ShowDetailAction()


class UsersOverview(Users):

    """
    A variant of :ddref:`users.Users` showing only active users
    and only some fields. 
    This is used on demo sites in :xfile:`admin_main.py` to display the 
    list of available users.
    """
    column_names = 'username profile language'
    exclude = dict(profile='')


class Authority(UserAuthored):

    """
    An Authority is when a User gives another User the right to "represent him"
   
    :user: points to the user who gives the right of representation. author of this Authority
    :authorized: points to the user who gets the right to represent the author
    
    """

    class Meta:
        verbose_name = _("Authority")
        verbose_name_plural = _("Authorities")

    #~ quick_search_fields = ('user__username','user__first_name','user__last_name')

    authorized = models.ForeignKey(
        settings.SITE.user_model,
        help_text=_("The user who gets authority to act in your name."))

    @dd.chooser()
    def authorized_choices(cls, user):
        qs = settings.SITE.user_model.objects.exclude(
            profile=None)
            #~ profile=UserProfiles.blank_item) 20120829
        if user is not None:
            qs = qs.exclude(id=user.id)
            #~ .exclude(level__gte=UserLevels.admin)
        return qs


class Authorities(dd.Table):
    required_roles = dd.required(dd.SiteAdmin)
    model = Authority


class AuthoritiesGiven(Authorities):
    required_roles = dd.required()
    master_key = 'user'
    label = _("Authorities given")
    column_names = 'authorized'
    auto_fit_column_widths = True


class AuthoritiesTaken(Authorities):
    required_roles = dd.required()
    master_key = 'authorized'
    label = _("Authorities taken")
    column_names = 'user'
    auto_fit_column_widths = True
