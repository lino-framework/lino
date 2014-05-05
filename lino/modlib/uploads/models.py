# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
"""

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
# from django.utils.encoding import force_unicode

from lino import dd
from lino import mixins
from lino.utils.xmlgen.html import E
from lino.utils import join_elems


class UploadAreas(dd.ChoiceList):
    verbose_name = _("Upload Area")
    verbose_name_plural = _("Upload Areas")
add = UploadAreas.add_item
add('10', _("Career related uploads"), 'cv')
add('20', _("Medical uploads"), 'medical')
add('30', _("Other uploads"), 'other')


class UploadType(dd.BabelNamed):
    """The type of an upload."""
    class Meta:
        abstract = dd.is_abstract_model('uploads.UploadType')
        verbose_name = _("Upload Type")
        verbose_name_plural = _("Upload Types")

    upload_area = UploadAreas.field(default=UploadAreas.cv)


class UploadTypes(dd.Table):
    """The table with all existing upload types.

This usually is accessible via the `Configure` menu.
    """
    required = dd.required(user_level='admin')
    model = 'uploads.UploadType'
    column_names = "upload_area name *"
    order_by = ["upload_area", "name"]

    insert_layout = """
    name
    upload_area
    """

    detail_layout = """
    id upload_area
    name
    uploads.UploadsByType
    """


class Upload(
        dd.Uploadable,
        dd.UserAuthored,
        dd.Controllable):

    class Meta:
        abstract = dd.is_abstract_model('uploads.Upload')
        verbose_name = _("Upload")
        verbose_name_plural = _("Uploads")

    upload_area = UploadAreas.field(default=UploadAreas.cv)

    type = dd.ForeignKey(
        "uploads.UploadType",
        blank=True, null=True)

    description = models.CharField(
        _("Description"), max_length=200, blank=True)

    def __unicode__(self):
        if self.description:
            s = self.description
        else:
            s = self.file.name
            i = s.rfind('/')
            if i != -1:
                s = s[i + 1:]
        if self.type:
            s = unicode(self.type) + ' ' + s
        return s

    @dd.chooser()
    def type_choices(self, upload_area):
        M = dd.resolve_model('uploads.UploadType')
        logger.info("20140430 type_choices %s", upload_area)
        if upload_area is None:
            return M.objects.all()
        return M.objects.filter(upload_area=upload_area)


class Uploads(dd.Table):
    "Shows all Uploads"
    required = dd.required(user_level='admin')
    model = 'uploads.Upload'
    column_names = "file type user owner description *"

    detail_layout = """
    file user
    upload_area type description
    owner
    """

    insert_layout = """
    type
    description
    file
    user
    """


class UploadsByType(Uploads):
    master_key = 'type'
    column_names = "file description user * "


class MyUploads(Uploads, mixins.ByUser):
    """Shows only my Uploads (i.e. those whose author is current user)."""
    required = dd.required()
    column_names = "file description user owner *"
    # order_by = ["modified"]


class UploadsByController(Uploads):
    "UploadsByController"
    required = dd.required()
    master_key = 'owner'
    column_names = "file type description user * "
    stay_in_grid = True
    _upload_area = None

    insert_layout = """
    file
    type
    description
    """

    slave_grid_format = 'summary'

    @classmethod
    def get_known_values(self):
        return dict(upload_area=self._upload_area)

    @classmethod
    def get_actor_label(self):
        if self._upload_area is not None:
            return self._upload_area.text
        return self._label or self.__name__

    @classmethod
    def get_slave_summary(self, obj, ar):
        """Displays the uploads related to this controller as a list grouped
by uploads type.

Note that this also works on
:class:`lino_welfare.modlib.uploads.models.UploadsByClient` and their
subclasses for the different `_upload_area`.

        """
        UploadType = dd.modules.uploads.UploadType
        # Upload = dd.modules.uploads.Upload
        elems = []
        types = []
        for ut in UploadType.objects.filter(
                upload_area=self._upload_area):
            sar = ar.spawn(
                self, master_instance=obj,
                known_values=dict(
                    type_id=ut.id))
            # logger.info("20140430 %s", sar.data_iterator.query)
            files = []
            for m in sar:
                def fmt(o):
                    return m.description or m.file.name or unicode(m.id)
                edit = ar.obj2html(
                    m,  fmt(m), # _("Edit"),
                    # icon_name='application_form',
                    title=_("Edit metadata of the uploaded file."))
                if m.file.name:
                    show = ar.renderer.href_button(
                        settings.SITE.build_media_url(m.file.name),
                        _(" [show]"),  # fmt(m),
                        target='_blank',
                        # icon_name='page_go',
                        # style="vertical-align:-30%;",
                        title=_("Open the uploaded file in a new browser window"))
                    # logger.info("20140430 %s", E.tostring(e))
                    files.append(E.span(show, edit))
                else:
                    files.append(edit)
            if True:
                files.append(sar.insert_button())
            if len(files) > 0:
                e = E.p(unicode(ut), ': ', *join_elems(files, ', '))
                types.append(e)
        # logger.info("20140430 %s", [E.tostring(e) for e in types])
        if len(types) == 0:
            elems.append(E.ul(E.li(ar.no_data_text)))
        else:
            elems.append(E.ul(*[E.li(e) for e in types]))
        return E.div(*elems)


class MedicalUploadsByController(UploadsByController):
    _upload_area = UploadAreas.medical


class CareerUploadsByController(UploadsByController):
    _upload_area = UploadAreas.cv


class OtherUploadsByController(UploadsByController):
    _upload_area = UploadAreas.other


system = dd.resolve_app('system')


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
    m.add_action('uploads.MyUploads')


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
    m.add_action('uploads.UploadTypes')


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
    m.add_action('uploads.Uploads')
    m.add_action('uploads.UploadAreas')
