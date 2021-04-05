# Copyright 2009-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from builtins import object

import logging
logger = logging.getLogger(__name__)


from django.db import models
from django.utils.translation import gettext_lazy as _

from lino.modlib.users.mixins import UserAuthored, My
from lino.modlib.office.roles import OfficeUser
from lino.api import dd



class TextFieldTemplate(UserAuthored):

    class Meta(object):
        verbose_name = _("Text Field Template")
        verbose_name_plural = _("Text Field Templates")

    name = models.CharField(_("Designation"), max_length=200)
    description = dd.RichTextField(_("Description"),
                                   blank=True, null=True, format='plain')
        #~ blank=True,null=True,format='html')
    # team = dd.ForeignKey(
    #     'users.Team', blank=True, null=True,
    #     help_text=_("If not empty, then this template "
    #                 "is reserved to members of this team."))
    text = dd.RichTextField(_("Template Text"),
                            blank=True, null=True, format='html')

    def __str__(self):
        return self.name


class TextFieldTemplates(dd.Table):
    model = TextFieldTemplate
    required_roles = dd.login_required(dd.SiteStaff, OfficeUser)
    insert_layout = dd.InsertLayout("""
    name
    user #team
    """, window_size=(60, 'auto'))

    detail_layout = """
    id name user #team
    description
    text
    """


class MyTextFieldTemplates(My, TextFieldTemplates):
    required_roles = dd.login_required(OfficeUser)
