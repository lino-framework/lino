# -*- coding: UTF-8 -*-
# Copyright 2010-2018 Luc Saffre
# License: BSD (see file COPYING for details)

"""Upload shortcut fields
=========================

An **upload shortcut field** is a configurable virtual field with a
user-friendly interface for managing a subset of uploaded files
related to a given database object.

Usage:

- Declare your Site's upload shortcuts from within your
  :attr:`workflows_module
  <lino.core.site.Site.workflows_module>`. For example::

      from lino.modlib.uploads.choicelists import add_shortcut as add
      add('contacts.Person', 'uploaded_foos', _("Foos"))
    
- Using the web interface, select :menuselection:`Configure --> Office
  --> Upload types`, create an upload type named "Foo" and set its
  `shortcut` field to "Foos".

.. autosummary::

"""

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from lino.modlib.office.roles import OfficeStaff

from lino.api import dd, rt


class Shortcut(dd.Choice):
    """Represents a shortcut field."""
    model_spec = None
    target = 'uploads.UploadsByController'

    def __init__(self, model_spec, name, verbose_name, target=None):
        if target is not None:
            self.target = target
        self.model_spec = model_spec
        value = model_spec + "." + name
        super(Shortcut, self).__init__(value, verbose_name, name)

    def get_uploads(self, **kw):
        """Return a queryset with the uploads of this shortcut."""
        return rt.models.uploads.Upload.objects.filter(
            type__shortcut=self, **kw)


class Shortcuts(dd.ChoiceList):
    """The list of upload shortcut fields which have been declared on this
Site.  See :func:`add_shortcut`.

    """
    verbose_name = _("Upload shortcut")
    verbose_name_plural = _("Upload shortcuts")
    item_class = Shortcut
    max_length = 50  # fields get created before the values are known


class UploadAreas(dd.ChoiceList):
    required_roles = dd.login_required(OfficeStaff)
    verbose_name = _("Upload Area")
    verbose_name_plural = _("Upload Areas")
add = UploadAreas.add_item
add('90', _("Uploads"), 'general')


   


def add_shortcut(*args, **kw):
    """Declare an upload shortcut field. This is designed to be called
    from within your :attr:`workflows_module
    <lino.core.site.Site.workflows_module>`.

    """
    return Shortcuts.add_item(*args, **kw)
