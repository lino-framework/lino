# Copyright 2010-2014 Luc Saffre
# License: BSD (see file COPYING for details)

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext as _
from django.db import models
from django.conf import settings

from lino.core.model import Model


class Uploadable(Model):

    """
    Represents an uploadable file.
    """

    # file_field_class = models.FileField

    class Meta:
        abstract = True
        # verbose_name = _("upload")
        # verbose_name_plural = _("uploads")

    file = models.FileField(
        _("File"),
        blank=True,
        upload_to='uploads/%Y/%m')
    mimetype = models.CharField(
        _("MIME type"),
        blank=True,
        max_length=64, editable=False)

    def handle_uploaded_files(self, request):
        #~ from django.core.files.base import ContentFile
        if not 'file' in request.FILES:
            logger.debug("No 'file' has been submitted.")
            return
        uf = request.FILES['file']  # an UploadedFile instance
        #~ cf = ContentFile(request.FILES['file'].read())
        #~ print f
        #~ raise NotImplementedError
        #~ dir,name = os.path.split(f.name)
        #~ if name != f.name:
            #~ print "Aha: %r contains a path! (%s)" % (f.name,__file__)

        #~ name = os.path.join(settings.MEDIA_ROOT,'uploads',name)

        self.size = uf.size
        self.mimetype = uf.content_type

        """
        Certain Python versions or systems don't manage non-ascii filenames,
        so we replace any non-ascii char by "_"
        """

        #~ logger.info('20121004 handle_uploaded_files() %r',uf.name)
        name = uf.name.encode('ascii', 'replace')
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
