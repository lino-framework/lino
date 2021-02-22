# -*- coding: UTF-8 -*-
# Copyright 2008-2021 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

import shutil
from pathlib import Path

from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage

from etgen.html import E
from lino.api import dd, rt, _
from .choicelists import UploadAreas

def safe_filename(name):
    name = name.encode('ascii', 'replace').decode('ascii')
    name = name.replace('?', '_')
    name = name.replace('/', '_')
    name = name.replace(' ', '_')
    return name


def needs_update(src, dest):
    if dest.exists() and dest.stat().st_mtime >= src.stat().st_mtime:
        return False
    return True

def make_uploaded_file(filename, src=None, upload_date=None):
    """
    Create a dummy file that looks as if a file had really been uploaded.

    """
    if src is None:
        src = Path(__file__).parent / "dummy_upload.pdf"
    if upload_date is None:
        upload_date = dd.demo_date()
    assert src.exists()
    filename = default_storage.generate_filename(safe_filename(filename))
    upload_to = Path(upload_date.strftime(dd.plugins.uploads.upload_to_tpl))
    upload_filename = default_storage.generate_filename(str(upload_to / filename))
    dest = Path(settings.MEDIA_ROOT) / upload_filename
    if needs_update(src, dest):
        print("cp {} {}".format(src, dest))
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
    return upload_filename

def demo_upload(filename, src=None, upload_date=None, **kw):
    """
    Return an upload entry that looks as if a file had really been uploaded.

    """
    kw['file'] = make_uploaded_file(filename, src, upload_date)
    return rt.models.uploads.Upload(**kw)


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
