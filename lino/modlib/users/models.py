# -*- coding: UTF-8 -*-
# Copyright 2011-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from builtins import str
from builtins import object

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

from lino.api import dd, rt, _
from etgen.html import E
from lino.core import userprefs
# from lino.core.fields import NullCharField
from lino.core.roles import SiteAdmin

from lino.mixins import CreatedModified, Contactable
from lino.mixins import DateRange

from .choicelists import UserTypes
from .mixins import UserAuthored  #, TimezoneHolder
from .actions import ChangePassword, SignOut
# from .actions import SendWelcomeMail
# from .actions import SignIn
from lino.core.auth.utils import AnonymousUser
from lino.modlib.about.choicelists import TimeZones
from lino.modlib.printing.mixins import Printable


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('user_type', UserTypes.user)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('user_type', UserTypes.admin)
        return self._create_user(username, email, password, **extra_fields)




@python_2_unicode_compatible
class User(AbstractBaseUser, Contactable, CreatedModified, DateRange,
           Printable):
    class Meta(object):
        app_label = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        abstract = dd.is_abstract_model(__name__, 'User')
        ordering = ['last_name', 'first_name', 'username']

    USERNAME_FIELD = 'username'
    _anon_user = None
    objects = UserManager()

    preferred_foreignkey_width = 15
    hidden_columns = 'password remarks'
    authenticated = True
    quick_search_fields = 'username user_type first_name last_name remarks'

    # seems that Django doesn't like nullable username
    # username = dd.NullCharField(_('Username'), max_length=30, unique=True)
    username = models.CharField(_('Username'), max_length=30, unique=True)
    
    user_type = UserTypes.field(blank=True)
    initials = models.CharField(_('Initials'), max_length=10, blank=True)
    first_name = models.CharField(_('First name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True)
    remarks = models.TextField(_("Remarks"), blank=True)  # ,null=True)

    if settings.USE_TZ:
        time_zone = TimeZones.field(default='default')
    else:
        time_zone = dd.DummyField()

    change_password = ChangePassword()
    # sign_in = SignIn()
    sign_out = SignOut()

    def __str__(self):
        return self.get_full_name()

    @property
    def is_active(self):
        if self.start_date and self.start_date > dd.today():
            return False
        if self.end_date and self.end_date < dd.today():
            return False
        return True
        
    def get_as_user(self):
        """
        Overrides :meth:`lino_xl.lib.contacts.Partner.get_as_user`.
        """
        return self
    
    def get_full_name(self):
        if not self.first_name and not self.last_name:
            return self.initials or self.username or str(self.pk)
        return u'{} {}'.format(self.first_name, self.last_name).strip()

    @dd.displayfield(_("Name"), max_length=15)
    def name_column(self, request):
        # return join_words(self.last_name.upper(),self.first_name)
        return str(self)

    # @dd.displayfield(_("Other authentication providers"))
    # def social_auth_links(self, ar=None):
    #     return settings.SITE.get_social_auth_links        ()
    #     # elems = []
    #     # for backend in get_social_auth_backends()
    #     # elems.append(E.a("foo"))
    #     # return E.p(elems)
    
    def get_person(self):
        if self.partner:
            return self.partner.get_mti_child('person')

    person = property(get_person)

    def is_editable_by_all(self):
        return False
    
    def get_row_permission(self, ar, state, ba):
        # import pdb ; pdb.set_trace()
        if not ba.action.readonly:
            user = ar.get_user()
            if user != self:
                if not user.user_type.has_required_roles([SiteAdmin]):
                    if not self.is_editable_by_all():
                        return False
        return super(User, self).get_row_permission(ar, state, ba)
        #~ return False

    def disabled_fields(self, ar):
        """
        Only System admins may change the `user_type` of users.
        See also :meth:`Users.get_row_permission`.
        """
        rv = super(User, self).disabled_fields(ar)
        user = ar.get_user()
        if not user.user_type.has_required_roles([SiteAdmin]):
            rv.add('send_email')
            rv.add('user_type')
            if user != self:
                rv.add('change_password')
        return rv

    def full_clean(self, *args, **kw):
        p = self.get_person()
        if p is not None and p != self:
            for n in ('first_name', 'last_name', 'email', 'language'):
                if not getattr(self, n):
                    setattr(self, n, getattr(p, n))
            #~ self.language = p.language
        if not self.language:
            #~ self.language = settings.SITE.DEFAULT_LANGUAGE.django_code
            self.language = settings.SITE.get_default_language()
        if not self.password:
            self.set_unusable_password()
        # if not self.initials:
        #     if self.first_name and self.last_name:
        #         self.initials = self.first_name[0] + self.last_name[0]
        super(User, self).full_clean(*args, **kw)
        
    def on_create(self, ar):
        self.start_date = dd.today()
        super(User, self).on_create(ar)

    def get_received_mandates(self):
        #~ return [ [u.id,_("as %s")%u] for u in self.__class__.objects.all()]
        return [[u.id, str(u)] for u in self.__class__.objects.all()]
        #~ return self.__class__.objects.all()

    # @dd.htmlbox(_("Welcome"))
    # def welcome_email_body(self, ar):
    #     # return join_words(self.last_name.upper(),self.first_name)
    #     return self.get_welcome_email_body(ar)

    def get_welcome_email_body(self, ar):
        template = rt.get_template('users/welcome_email.eml')
        context = self.get_printable_context(ar)
        # dict(obj=self, E=E, rt=rt)
        return template.render(**context)
        
    def as_list_item(self, ar):
        pv = dict(username=self.username)
        if settings.SITE.is_demo_site:
            pv.update(password='1234')
        btn = rt.models.users.UsersOverview.get_action_by_name('sign_in')
        # print btn.get_row_permission(ar, None, None)
        btn = btn.request(
            action_param_values=pv,
            renderer=settings.SITE.kernel.default_renderer)
        btn = btn.ar2button(label=self.username)
        items = [ btn, ' : ',
                  str(self), ', ',
                  str(self.user_type)]
        if self.language:
            items += [', ',
            E.strong(str(settings.SITE.LANGUAGE_DICT.get(self.language)))]
        return E.li(*items)
        # if settings.SITE.is_demo_site:
        #     p = "'{0}', '{1}'".format(self.username, '1234')
        # else:
        #     p = "'{0}'".format(self.username)
        # url = "javascript:Lino.show_login_window(null, {0})".format(p)
        # return E.li(E.a(self.username, href=url), ' : ',
        #             str(self), ', ',
        #             str(self.user_type), ', ',
        #             E.strong(settings.SITE.LANGUAGE_DICT.get(self.language)))

    @classmethod
    def get_by_username(cls, username, default=models.NOT_PROVIDED):
        """
        `User.get_by_username(x)` is equivalent to
        `User.objects.get(username=x)` except that the text of the
        DoesNotExist exception is more useful.
        """
        try:
            return cls.objects.get(username=username)
        except cls.DoesNotExist:
            if default is models.NOT_PROVIDED:
                raise cls.DoesNotExist(
                    "No %s with username %r" % (
                        str(cls._meta.verbose_name), username))
            return default

    def get_preferences(self):
        """
        Return the preferences of this user. The returned object is a
        :class:`lino.core.userprefs.UserPrefs` object.
        """
        return userprefs.reg.get(self)
    
    @classmethod
    def get_anonymous_user(cls):
        return AnonymousUser()
    
    # @dd.action(label=_("Send e-mail"),
    #            show_in_bbar=True, show_in_workflow=False,
    #            button_text="✉")  # u"\u2709"
    # def do_send_email(self, ar):
    #     self.send_welcome_email()

    # send_email = SendWelcomeMail()

class Authority(UserAuthored):
    class Meta(object):
        app_label = 'users'
        verbose_name = _("Authority")
        verbose_name_plural = _("Authorities")


    authorized = dd.ForeignKey(settings.SITE.user_model)

    @dd.chooser()
    def authorized_choices(cls, user):
        qs = settings.SITE.user_model.objects.exclude(
            user_type=None)
            #~ user_type=UserTypes.blank_item) 20120829
        if user is not None:
            qs = qs.exclude(id=user.id)
            #~ .exclude(level__gte=UserLevels.admin)
        return qs

dd.update_field(Authority, 'user', null=False)    

@dd.receiver(dd.pre_startup)
def inject_partner_field(sender=None, **kwargs):

    User = sender.models.users.User

    if dd.is_installed('contacts'):
        Partner = sender.models.contacts.Partner
        if not issubclass(User, Partner):
            dd.inject_field(User, 'partner', dd.ForeignKey(
                'contacts.Partner', blank=True, null=True,
                related_name='users_by_partner',
                on_delete=models.PROTECT))
            # a related_name is needed so that Avanti can have aClient
            # who inherits from both Partner and UserAuthored
            return
    dd.inject_field(User, 'partner', dd.DummyField())

    
class Permission(dd.Model):
    class Meta(object):
        app_label = 'users'
        abstract = True


@dd.receiver(dd.post_startup)
def setup_memo_commands(sender=None, **kwargs):
    # See :doc:`/specs/memo`

    mp = sender.kernel.memo_parser

    mp.add_suggester(
        "@",
        sender.models.users.User.objects.filter(
            username__isnull=False).order_by('username'),
        'username')



