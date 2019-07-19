# Copyright 2010-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Defines the :class:`Uploadable` mixin.
"""

from builtins import object

import logging ; logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from etgen.html import E
from lino.core.model import Model


class Uploadable(Model):
    """Mixin for objects that represent an uploadable file.

    Used by :class:`lino.modlib.uploads.Upload`.

    .. attribute:: file

        Pointer to the file itself (a `Django FileField
        <https://docs.djangoproject.com/en/1.11/ref/models/fields/#filefield>`_).

    .. attribute:: mimetype

        The `Media type <https://en.wikipedia.org/wiki/Media_type>`_
        of the file.  See also `this thread
        <http://stackoverflow.com/questions/643690/maximum-mimetype-length-when-storing-type-in-db>`_
        about length of MIME type field.

    """

    # file_field_class = models.FileField

    class Meta(object):
        abstract = True
        # verbose_name = _("upload")
        # verbose_name_plural = _("uploads")

    file = models.FileField(
        _("File"),
        blank=True,
        upload_to='uploads/%Y/%m')
    mimetype = models.CharField(
        _("MIME type"),
        blank=True, max_length=255, editable=False)

    def handle_uploaded_files(self, request, file=None):
        #~ from django.core.files.base import ContentFile
        if not file and not 'file' in request.FILES:
            logger.debug("No 'file' has been submitted.")
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

        #~ logger.info('20121004 handle_uploaded_files() %r',uf.name)
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

        logger.info("Wrote uploaded file %s", ff.path)

    def get_file_button(self, text=None):
        if text is None:
            text = str(self)
        if self.file.name:
            url = settings.SITE.build_media_url(self.file.name)
            return E.a(text, href=url, target="_blank")
        return text

