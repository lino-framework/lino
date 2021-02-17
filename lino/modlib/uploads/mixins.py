# -*- coding: UTF-8 -*-
# Copyright 2008-2021 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from django.db import models
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError

from etgen.html import E
from lino.api import dd, _
from .choicelists import UploadAreas


class UploadBase(dd.Model):

    class Meta(object):
        abstract = True

    file = models.FileField(
        _("File"), blank=True, upload_to='uploads/%Y/%m')
    mimetype = models.CharField(
        _("MIME type"),
        blank=True, max_length=255, editable=False)

    def full_clean(self):
        super(UploadBase, self).full_clean()
        if self.file and self.file.size > dd.plugins.uploads.max_file_size:
            raise ValidationError(_("File size is {}! Must be below {}.").format(
                filesizeformat(self.file.size), filesizeformat(dd.plugins.uploads.max_file_size)))

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

        # Certain Python versions or systems don't manage non-ascii filenames,
        # so we replace any non-ascii char by "_". In Py3, encode() returns a
        # bytes object, but we want the name to remain a str.

        #~ dd.logger.info('20121004 handle_uploaded_files() %r',uf.name)
        name = uf.name.encode('ascii', 'replace').decode('ascii')
        name = name.replace('?', '_')

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


class UploadController(dd.Model):

    class Meta(object):
        abstract = True

    def get_upload_area(self):
        return UploadAreas.general

    def get_uploads_volume(self):
        return None

    if dd.is_installed("uploads"):

        show_uploads = dd.ShowSlaveTable(
            'uploads.UploadsByController',
            react_icon_name= "pi-upload",
            button_text="🖿")  # u"\u1F5BF"
