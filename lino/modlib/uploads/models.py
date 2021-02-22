# -*- coding: UTF-8 -*-
# Copyright 2008-2021 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

import os
from os.path import join, exists
import glob
from pathlib import Path

from django.db import models
from django.db.models.fields.files import FieldFile
from django.conf import settings
from django.utils.text import format_lazy
# from lino.api import string_concat
from django.utils.translation import pgettext_lazy as pgettext
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError

from etgen.html import E, join_elems, tostring
from lino.api import dd, rt, _
from lino.core.utils import model_class_path
from lino import mixins
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.users.mixins import UserAuthored, My
from lino.modlib.office.roles import OfficeUser, OfficeStaff, OfficeOperator
from lino.mixins import Referrable
from lino.modlib.checkdata.choicelists import Checker

from .choicelists import Shortcuts, UploadAreas
from .mixins import UploadController, safe_filename


def filename_leaf(name):
    i = name.rfind('/')
    if i != -1:
        return name[i + 1:]
    return name


class Volume(Referrable):

    class Meta:
        app_label = 'uploads'
        verbose_name = _("Library volume")
        verbose_name_plural = _("Library volumes")

    preferred_foreignkey_width = 5

    root_dir = dd.CharField(_("Root directory"), max_length=255)
    base_url = dd.CharField(_("Base URL"), max_length=255, blank=True)
    description = dd.CharField(_("Description"), max_length=255, blank=True)

    def __str__(self):
        return self.ref or self.root_dir

    def get_filenames(self):
        root_len = len(self.root_dir) + 1
        for (root, dirs, files) in os.walk(self.root_dir):
            relroot = root[root_len:]
            if relroot:
                relroot += "/"
            for fn in files:
                # print(relroot + "/" + fn)
                yield relroot + fn


class UploadType(mixins.BabelNamed):
    class Meta(object):
        abstract = dd.is_abstract_model(__name__, 'UploadType')
        verbose_name = _("Upload type")
        verbose_name_plural = _("Upload types")

    upload_area = UploadAreas.field(default='general')

    max_number = models.IntegerField(
        _("Max. number"), default=-1,
        # help_text=string_concat(
        #     _("No need to upload more uploads than N of this type."),
        #     "\n",
        #     _("-1 means no limit.")))
        help_text=format_lazy(
            "{}\n{}",
            _("No need to upload more uploads than N of this type."),
            _("-1 means no limit.")))
    wanted = models.BooleanField(
        _("Wanted"), default=False,
        help_text=_("Add a (+) button when there is no upload of this type."))

    shortcut = Shortcuts.field(blank=True)

class UploadBase(dd.Model):

    class Meta(object):
        abstract = True

    file = models.FileField(
        _("File"), blank=True, upload_to=dd.plugins.uploads.upload_to_tpl)
    mimetype = models.CharField(
        _("MIME type"), blank=True, max_length=255, editable=False)

    def handle_uploaded_files(self, request, file=None):
        #~ from django.core.files.base import ContentFile
        if not file and not 'file' in request.FILES:
            dd.logger.debug("No 'file' has been submitted.")
            return
        uf = file or request.FILES['file']  # an UploadedFile instance
        #~ cf = ContentFile(request.FILES['file'].read())
        #~ print f
        #~ raise NotImplementedError
        #~ dir,name = os.path.split(f.name)
        #~ if name != f.name:
            #~ print "Aha: %r contains a path! (%s)" % (f.name,__file__)
        self.size = uf.size
        self.mimetype = uf.content_type

        if self.size > dd.plugins.uploads.max_file_size:
            raise ValidationError(
                _("File size is {}! Must be below {}.").format(
                    filesizeformat(self.size),
                    filesizeformat(dd.plugins.uploads.max_file_size)))

        # Certain Python versions or systems don't manage non-ascii filenames,
        # so we replace any non-ascii char by "_". In Py3, encode() returns a
        # bytes object, but we want the name to remain a str.

        #~ dd.logger.info('20121004 handle_uploaded_files() %r',uf.name)
        name = safe_filename(uf.name)

        # Django magics:
        self.file = name  # assign a string
        ff = self.file  # get back a FileField instance !
        #~ print 'uf=',repr(uf),'ff=',repr(ff)

        #~ if not ispure(uf.name):
            #~ raise Exception('uf.name is a %s!' % type(uf.name))

        ff.save(name, uf, save=False)

        # The expression `self.file`
        # now yields a FieldFile instance that has been created from `uf`.
        # see Django FileDescriptor.__get__()

        dd.logger.info("Wrote uploaded file %s", ff.path)

    def get_file_button(self, text=None):
        if text is None:
            text = str(self)
        if self.file.name:
            url = settings.SITE.build_media_url(self.file.name)
            return E.a(text, href=url, target="_blank")
        return text


class Upload(UploadBase, UserAuthored, Controllable):

    class Meta(object):
        abstract = dd.is_abstract_model(__name__, 'Upload')
        verbose_name = _("Upload file")
        verbose_name_plural = _("Upload files")

    upload_area = UploadAreas.field(default='general')
    type = dd.ForeignKey("uploads.UploadType", blank=True, null=True)
    volume = dd.ForeignKey("uploads.Volume", blank=True, null=True)
    library_file = models.CharField(_("Library file"), max_length=255, blank=True)
    file_size = models.IntegerField(_("File size"), editable=False, null=True)

    description = models.CharField(
        _("Description"), max_length=200, blank=True)

    def __str__(self):
        if self.description:
            s = self.description
        elif self.file:
            s = filename_leaf(self.file.name)
        elif self.library_file:
            s = "{}:{}".format(self.volume.ref, self.library_file)
        else:
            s = str(self.id)
        if self.type:
            s = str(self.type) + ' ' + s
        return s

    @dd.displayfield(_("Description"))
    def description_link(self, ar):
        if self.description:
            s = self.description
        elif self.file:
            s = filename_leaf(self.file.name)
        elif self.type:
            s = str(self.type)
        else:
            s = str(self.id)
        if ar is None:
            return s
        return self.get_file_button(s)

    @dd.chooser(simple_values=True)
    def library_file_choices(self, volume):
        if volume is None:
            return []
        return list(volume.get_filenames())

    @dd.chooser()
    def type_choices(self, upload_area):
        M = dd.resolve_model('uploads.UploadType')
        # logger.info("20140430 type_choices %s", upload_area)
        if upload_area is None:
            return M.objects.all()
        return M.objects.filter(upload_area=upload_area)

    def full_clean(self, *args, **kw):
        super(Upload, self).full_clean(*args, **kw)
        if self.type is not None:
            self.upload_area = self.type.upload_area

        self.file_size = self.get_real_file_size()

    def get_real_file_size(self):
        if self.file:
            return self.file.size
        if self.volume_id and self.library_file:
            pth = join(self.volume.root_dir, self.library_file)
            return os.path.get_size(pth)


dd.update_field(Upload, 'user', verbose_name=_("Uploaded by"))


class UploadChecker(Checker):
    verbose_name = _("Check metadata of upload files")
    model = Upload

    def get_checkdata_problems(self, obj, fix=False):
        if obj.file:
            if not exists(join(settings.MEDIA_ROOT, obj.file.name)):
                yield (False, format_lazy(
                    _("Upload entry {} has no file"), obj.file.name))
                return

        file_size = obj.get_real_file_size()

        if obj.file_size != file_size:
            tpl = "Stored file size {} differs from real file size {}"
            yield (False, format_lazy(tpl, obj.file_size, file_size))

UploadChecker.activate()


class UploadsFolderChecker(Checker):
    verbose_name = _("Find orphaned files in uploads folder")

    def get_checkdata_problems(self, obj, fix=False):
        assert obj is None  # this is an unbound checker
        Upload = rt.models.uploads.Upload
        pth = dd.plugins.uploads.get_uploads_root()
        start = len(settings.MEDIA_ROOT) + 1
        # for filename in glob.iglob(join(pth,"**/*")):
        for filename in Path(pth).rglob("*"):
            # print(filename)
            if filename.is_dir():
                continue
            rel_filename = str(filename)[start:]
            qs = Upload.objects.filter(file=rel_filename)
            n = qs.count()
            if n == 0:
                msg = format_lazy(_("File {} has no upload entry."), rel_filename)
                # print(msg)
                yield (dd.plugins.uploads.remove_orphaned_files, msg)
                if fix and dd.plugins.uploads.remove_orphaned_files:
                    filename.unlink()
                    # obj = Upload(file=FieldFile(rel_filename))
                    # # obj = Upload(file=filename)
                    # obj.full_clean()
                    # obj.save()
            # else:
            #     print("{} has {} entries.".format(filename, n))
            # elif n > 1:
            #     msg = _("Multiple upload entries for {} ").format(filename)
            #     yield (False, msg)
            #     This is no problem. A same file should be linkable to diffeerent controlers.

UploadsFolderChecker.activate()


class Volumes(dd.Table):
    model = 'uploads.Volume'
    required_roles = dd.login_required(OfficeStaff)

    insert_layout = """
    ref description
    root_dir
    base_url
    """
    detail_layout = """
    ref description
    root_dir base_url
    overview
    """



class UploadTypes(dd.Table):
    required_roles = dd.login_required(OfficeStaff)
    model = 'uploads.UploadType'
    column_names = "upload_area name max_number wanted shortcut *"
    order_by = ["upload_area", "name"]

    insert_layout = """
    name
    upload_area
    """

    detail_layout = """
    id upload_area wanted max_number shortcut
    name
    uploads.UploadsByType
    """


class Uploads(dd.Table):
    model = 'uploads.Upload'
    required_roles = dd.login_required((OfficeUser, OfficeOperator))
    column_names = "file type user owner description *"
    order_by = ['-id']

    detail_layout = dd.DetailLayout("""
    file user
    volume:10 library_file:40
    upload_area type description
    owner
    """, window_size=(80, 'auto'))

    insert_layout = """
    type
    description
    file
    volume library_file
    user
    """

    parameters = mixins.ObservedDateRange(
        upload_type=dd.ForeignKey(
            'uploads.UploadType', blank=True, null=True))
    params_layout = "start_date end_date user upload_type"

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        qs = super(Uploads, cls).get_request_queryset(ar, **filter)
        pv = ar.param_values
        if pv.user:
            qs = qs.filter(user=pv.user)
        if pv.upload_type:
            qs = qs.filter(type=pv.upload_type)
        return qs


class AllUploads(Uploads):
    use_as_default_table = False
    required_roles = dd.login_required(OfficeStaff)


class UploadsByType(Uploads):
    master_key = 'type'
    column_names = "file library_file description user * "


class MyUploads(My, Uploads):
    required_roles = dd.login_required((OfficeUser, OfficeOperator))
    column_names = "file library_file description user owner *"
    # order_by = ["modified"]

    # @classmethod
    # def get_actor_label(self):
    #     return _("My %s") % _("Uploads")

    # @classmethod
    # def param_defaults(self, ar, **kw):
    #     kw = super(MyUploads, self).param_defaults(ar, **kw)
    #     kw.update(user=ar.get_user())
    #     return kw

class AreaUploads(Uploads):
    required_roles = dd.login_required((OfficeUser, OfficeOperator))
    stay_in_grid = True
    # _upload_area = UploadAreas.general
    display_mode = 'summary'

    # 20180119
    # @classmethod
    # def get_known_values(self):
    #     return dict(upload_area=self._upload_area)
    # @classmethod
    # def get_actor_label(self):
    #     if self._upload_area is not None:
    #         return self._upload_area.text
    #     return self._label or self.__name__

    @classmethod
    def format_row_in_slave_summary(self, ar, obj):
        """almost as str(), but without the type
        """
        return obj.description or filename_leaf(obj.file.name) \
            or str(obj.id)

    @classmethod
    def get_table_summary(self, obj, ar):
        if obj is None:
            return
        UploadType = rt.models.uploads.UploadType
        # Upload = rt.models.uploads.Upload
        elems = []
        types = []
        perm = ar.get_user().user_type.has_required_roles(self.required_roles)
        qs = UploadType.objects.all()
        if isinstance(obj, UploadController):
            area = obj.get_upload_area()
            if area is not None:
                qs = qs.filter(upload_area=area)
        else:
            return E.div("{} is not an UploadController!".format(
                model_class_path(obj.__class__)))
        volume = obj.get_uploads_volume()
        # print(20190208, volume)
        for ut in qs:
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
                    url = settings.SITE.build_media_url(m.file.name)
                elif m.volume_id and m.volume.base_url and m.library_file:
                    url = m.volume.base_url + m.library_file
                else:
                    url = None
                if url:
                    show = ar.renderer.href_button(
                        url,
                        # u"\u21A7",  # DOWNWARDS ARROW FROM BAR (↧)
                        # u"\u21E8",
                        u"\u21f2",  # SOUTH EAST ARROW TO CORNER (⇲)
                        style="text-decoration:none;",
                        # _(" [show]"),  # fmt(m),
                        target='_blank',
                        # icon_name=settings.SITE.build_static_url(
                        #     'images/xsite/link'),
                        # icon_name='page_go',
                        # style="vertical-align:-30%;",
                        title=_("Open the file in a new browser window"))
                        # title=_("Open the uploaded file in a new browser window"))
                    # logger.info("20140430 %s", tostring(e))
                    files.append(E.span(edit, ' ', show))
                else:
                    files.append(edit)
            if perm and ut.wanted \
               and (ut.max_number < 0 or len(files) < ut.max_number):
                btn = self.insert_action.request_from(
                    sar, master_instance=obj,
                    known_values=dict(type_id=ut.id, volume=volume)).ar2button()
                if btn is not None:
                    files.append(btn)
            if len(files) > 0:
                chunks = (str(ut), ': ') + tuple(join_elems(files, ', '))
                types.append(chunks)
        # logger.info("20140430 %s", [tostring(e) for e in types])
        # elems += [str(ar.bound_action.action.__class__), " "]
        if ar.bound_action.action.window_type == "d":
            if len(types) == 0:
                elems.append(E.ul(E.li(str(ar.no_data_text))))
            else:
                elems.append(E.ul(*[E.li(*chunks) for chunks in types]))
        else:
            if len(types) == 0:
                elems.append(str(ar.no_data_text))
                elems.append(" / ")
            else:
                for chunks in types:
                    elems.extend(chunks)
                    elems.append(" / ")
            elems.append(obj.show_uploads.as_button_elem(ar))
        # ba = self.find_action_by_name("show_uploads")
        return E.div(*elems)


class UploadsByController(AreaUploads):
    master_key = 'owner'
    column_names = "file volume library_file type description user *"

    insert_layout = dd.InsertLayout("""
    file
    volume library_file
    type
    description
    """, hidden_elements="volume", window_size=(60, 'auto'))

    @classmethod
    def format_upload(self, obj):
        return str(obj.type)


@dd.receiver(dd.pre_analyze)
def before_analyze(sender, **kwargs):
    # This is the successor for `quick_upload_buttons`.

    # remember that models might have been overridden.
    UploadType = sender.models.uploads.UploadType
    Shortcuts = sender.models.uploads.Shortcuts

    for i in Shortcuts.items():

        def f(obj, ar):
            if obj is None or ar is None:
                return E.div()
            try:
                utype = UploadType.objects.get(shortcut=i)
            except UploadType.DoesNotExist:
                return E.div()
            items = []
            target = sender.modules.resolve(i.target)
            sar = ar.spawn_request(
                actor=target,
                master_instance=obj,
                known_values=dict(type=utype))
                # param_values=dict(pupload_type=et))
            n = sar.get_total_count()
            if n == 0:
                iar = target.insert_action.request_from(
                    sar, master_instance=obj)
                btn = iar.ar2button(
                    None, _("Upload"), icon_name="page_add",
                    title=_("Upload a file from your PC to the server."))
                items.append(btn)
            elif n == 1:
                after_show = ar.get_status()
                obj = sar.data_iterator[0]
                items.append(sar.renderer.href_button(
                    sender.build_media_url(obj.file.name),
                    _("show"),
                    target='_blank',
                    icon_name='page_go',
                    style="vertical-align:-30%;",
                    title=_("Open the uploaded file in a "
                            "new browser window")))
                after_show.update(record_id=obj.pk)
                items.append(sar.window_action_button(
                    sar.ah.actor.detail_action,
                    after_show,
                    _("Edit"), icon_name='application_form',
                    title=_("Edit metadata of the uploaded file.")))
            else:
                obj = sar.sliced_data_iterator[0]
                items.append(ar.obj2html(
                    obj, pgettext("uploaded file", "Last")))

                btn = sar.renderer.action_button(
                    obj, sar, sar.bound_action,
                    _("All {0} files").format(n),
                    icon_name=None)
                items.append(btn)

            return E.div(*join_elems(items, ', '))

        vf = dd.VirtualField(dd.DisplayField(i.text), f)
        dd.inject_field(i.model_spec, i.name, vf)
        # logger.info("Installed upload shortcut field %s.%s",
        #             i.model_spec, i.name)
