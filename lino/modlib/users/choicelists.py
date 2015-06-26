# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines the choicelists for :mod:`lino.modlib.users`, i.e.
:class:`UserLevels`, 
:class:`UserGroups` and
:class:`UserProfiles`.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _
from django.conf import settings


from lino.core.choicelists import ChoiceList, Choice


class UserProfile(Choice):

    hidden_languages = None
    """A subset of :setting:`languages` which should be hidden in this
    user profile.  Default value is :attr:`hidden_languages
    <UserProfiles.hidden_languages>`.  This is used on multilingual
    sites with more than 4 or 5 languages.  See the source code of
    :meth:`lino_welfare.settings.Site.setup_user_profiles` for a usage
    example.

    """

    def __init__(self, value=None, text=None,
                 name=None, authenticated=True,
                 readonly=False,
                 **kw):
        if value is None:
            value = self.__module__.split('.')[-2] + '.' \
                + self.__class__.__name__
        super(UserProfile, self).__init__(value, text, name)
        self.readonly = readonly
        self.authenticated = authenticated
        self.kw = kw

    def attach(self, cls):
        super(UserProfile, self).attach(cls)
        self.kw.setdefault('hidden_languages', cls.hidden_languages)

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

    def __repr__(self):
        #~ s = self.__class__.__name__
        s = str(self.choicelist)
        if self.name:
            s += "." + self.name
        s += ":" + self.value
        return s

    def has_required_role(self, required_roles):
        for rr in required_roles:
            if not isinstance(self, rr):
                return False
        return True


class Anonymous(UserProfile):
    text = _("Anonymous")


class SiteUser(UserProfile):
    text = _("Site user")


class StaffMember(SiteUser):
    text = _("Staff member")


class SiteAdmin(StaffMember):
    text = _("Administrator")


##

class UserProfiles(ChoiceList):
    """The list of user profiles available on this site.
    
    Each user profile is a set of user levels (one for each functional
    group), leading to an individual combination of permissions.
    
    The demo database has defined the following user profiles:

    .. django2rst:: rt.show(users.UserProfiles,
                            column_names='value name text level')

    Note that we show here only the "general" or "system" userlevel.
    Open :menuselection:`Explorer --> System --> User Profiles`
    in your Lino to see all application-specific userlevels.

    """
    required_roles = settings.SITE.get_default_required_roles(SiteAdmin)
    item_class = UserProfile
    verbose_name = _("User Profile")
    verbose_name_plural = _("User Profiles")
    show_values = True
    max_length = 20

    preferred_foreignkey_width = 20

    hidden_languages = settings.SITE.hidden_languages
    """Default value for the :attr:`hidden_languages
    <UserProfile.hidden_languages>` of newly attached choice item.

    """
