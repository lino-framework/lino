# Copyright 2011-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Defines the choicelists for :mod:`lino.modlib.users`.

"""

from django.conf import settings
from rstgen.utils import unindent

from lino.core.choicelists import ChoiceList, Choice
from lino.core.roles import SiteAdmin, check_required_roles
from .utils import UserTypeContext

from lino.api import dd, _


class UserType(Choice):
    role = None
    hidden_languages = None
    readonly = False

    # authenticated = True
    # """Whether users with this user_type should be considered authenticated."""

    def __init__(self, value, text, role_class,
                 name=None,  # authenticated=True,
                 readonly=False,
                 **kw):
        # if value is None:
        #     value = self.__module__.split('.')[-2] + '.' \
        #         + self.__class__.__name__
        super(UserType, self).__init__(value, text, name)
        if isinstance(role_class, (tuple, list)):
            raise Exception("No longer supported")
            # self.roles = set([rc() for rc in role_class])
        self.role = role_class()
        self.readonly = readonly
        self.kw = kw
        self.mask_message_types = set([])

    def context(self):
        return UserTypeContext(self)

    def attach(self, cls):
        super(UserType, self).attach(cls)
        self.kw.setdefault('hidden_languages', cls.hidden_languages)
        if 'remark' not in self.kw:
            s = self.role.__doc__
            if s is not None:
                self.kw['remark'] = unindent(s)

        for k, vf in cls.virtual_fields.items():
            if vf.has_default():
                self.kw.setdefault(k, vf.get_default())
            elif vf.return_type.blank:
                self.kw.setdefault(k, None)

        for k, v in self.kw.items():
            setattr(self, k, v)

        if self.hidden_languages is not None:
            self.hidden_languages = set(
                settings.SITE.resolve_languages(self.hidden_languages))

        del self.kw

    # def __repr__(self):
    #     #~ s = self.__class__.__name__
    #     s = str(self.choicelist)
    #     if self.name:
    #         s += "." + self.name
    #     s += ":" + self.value
    #     return s
    #

    def mask_notifications(self, *args):
        """
        Add the given notification message types to the notification mask.
        Notifications will not be forwarded to users whose user_type
        filters them away.
        """
        for mt in args:
            self.mask_message_types.add(mt)

    def has_required_roles(self, required_roles):
        """
        Return `True` if this user type's :attr:`role` satisfies the
        specified requirements.
        """
        # for role in self.roles:
        return self.role.satisfies_requirement(required_roles)

    def find_menu_item(self, bound_action):
        """
        Find the item of the main menu for the specified bound action.
        """
        mnu = settings.SITE.get_site_menu(self)
        return mnu.find_item(bound_action)

##


class UserTypes(ChoiceList):
    required_roles = dd.login_required(SiteAdmin)
    item_class = UserType
    verbose_name = _("User type")
    verbose_name_plural = _("User types")
    show_values = True
    max_length = 20
    # column_names = "value name text user_role"
    column_names = "value name text"

    preferred_foreignkey_width = 20

    # readonly = models.BooleanField(_("Read-only"), default=False)

    hidden_languages = settings.SITE.hidden_languages
    """Default value for the
    :attr:`hidden_languages<UserType.hidden_languages>` of newly
    attached choice item.

    """

    @dd.displayfield(_("User role"))
    def user_role(cls, obj, ar):
        return obj.role.__class__.__module__ + '.' + obj.role.__class__.__name__

# add = UserTypes.add_item
# add('000', _("Anonymous"), UserRole, 'anonymous', readonly=True)
# add('100', _("User"), SiteUser, 'user')
# add('900', _("Administrator"), SiteAdmin, 'admin')
