# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
"""

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
# from django.utils.encoding import force_unicode

from lino import dd, rt
from lino import mixins
from lino.utils.xmlgen.html import E
from lino.utils import join_elems

from lino.modlib.contenttypes.mixins import Controllable

system = dd.resolve_app('system')


class UploadAreas(dd.ChoiceList):
    verbose_name = _("Upload Area")
    verbose_name_plural = _("Upload Areas")
add = UploadAreas.add_item
add('90', _("Uploads"), 'general')


class UploadType(mixins.BabelNamed):
    """The type of an upload."""
    class Meta:
        abstract = dd.is_abstract_model(__name__, 'UploadType')
        verbose_name = _("Upload Type")
        verbose_name_plural = _("Upload Types")

    upload_area = UploadAreas.field(default=UploadAreas.general)

    max_number = models.IntegerField(
        _("Max. number"), default=-1,
        help_text=string_concat(
            _("No need to upload more uploads than N of this type."),
            "\n",
            _("-1 means no limit.")))
    wanted = models.BooleanField(
        _("Wanted"), default=False,
        help_text=_("Add a (+) button when there is no upload of this type."))


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
    id upload_area wanted max_number
    name
    uploads.UploadsByType
    """


def filename_leaf(name):
    i = name.rfind('/')
    if i != -1:
        return name[i + 1:]
    return name


class Upload(
        mixins.Uploadable,
        mixins.UserAuthored,
        Controllable):

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Upload')
        verbose_name = _("Upload")
        verbose_name_plural = _("Uploads")

    upload_area = UploadAreas.field(default=UploadAreas.general)

    type = dd.ForeignKey(
        "uploads.UploadType",
        blank=True, null=True)

    description = models.CharField(
        _("Description"), max_length=200, blank=True)

    def __unicode__(self):
        if self.description:
            s = self.description
        elif self.file:
            s = filename_leaf(self.file.name)
        else:
            s = unicode(self.id)
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

    def save(self, *args, **kw):
        if self.type is not None:
            self.upload_area = self.type.upload_area
        super(Upload, self).save(*args, **kw)


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


class AreaUploads(Uploads):
    required = dd.required()
    stay_in_grid = True
    _upload_area = UploadAreas.general
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
    def format_row_in_slave_summary(self, ar, obj):
        """almost as unicode, but without the type
        """
        return obj.description or filename_leaf(obj.file.name) \
            or unicode(obj.id)

    @classmethod
    def get_slave_summary(self, obj, ar):
        """Displays the uploads related to this controller as a list grouped
by uploads type.

Note that this also works on
:class:`lino_welfare.modlib.uploads.models.UploadsByClient` and their
subclasses for the different `_upload_area`.

        """
        UploadType = rt.modules.uploads.UploadType
        # Upload = rt.modules.uploads.Upload
        elems = []
        types = []

        for ut in UploadType.objects.filter(
                upload_area=self._upload_area):
            sar = ar.spawn(
                self, master_instance=obj,
                known_values=dict(type_id=ut.id))
            # logger.info("20140430 %s", sar.data_iterator.query)
            files = []
            for m in sar:
                text = self.format_row_in_slave_summary(ar, m)
                if text is None:
                    continue
                edit = ar.obj2html(
                    m,  text,  # _("Edit"),
                    # icon_name='application_form',
                    title=_("Edit metadata of the uploaded file."))
                if m.file.name:
                    show = ar.renderer.href_button(
                        settings.SITE.build_media_url(m.file.name),
                        _(" [show]"),  # fmt(m),
                        target='_blank',
                        icon_name='../xsite/link',
                        # icon_name='page_go',
                        # style="vertical-align:-30%;",
                        title=_("Open the uploaded file in a new browser window"))
                    # logger.info("20140430 %s", E.tostring(e))
                    files.append(E.span(edit, ' ', show))
                else:
                    files.append(edit)
            if ut.wanted and (
                    ut.max_number < 0 or len(files) < ut.max_number):
                btn = sar.insert_button()
                if btn is not None:
                    files.append(btn)
            if len(files) > 0:
                e = E.p(unicode(ut), ': ', *join_elems(files, ', '))
                types.append(e)
        # logger.info("20140430 %s", [E.tostring(e) for e in types])
        if len(types) == 0:
            elems.append(E.ul(E.li(ar.no_data_text)))
        else:
            elems.append(E.ul(*[E.li(e) for e in types]))
        return E.div(*elems)


class UploadsByController(AreaUploads):
    "UploadsByController"
    master_key = 'owner'
    column_names = "file type description user * "

    insert_layout = """
    file
    type
    description
    """


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
