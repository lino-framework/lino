# -*- coding: UTF-8 -*-
# Copyright 2010-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from lino.modlib.office.roles import OfficeStaff
from lino.api import dd, rt, _


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
    verbose_name = _("Upload shortcut")
    verbose_name_plural = _("Upload shortcuts")
    item_class = Shortcut
    max_length = 50  # fields get created before the values are known


class UploadAreas(dd.ChoiceList):
    required_roles = dd.login_required(OfficeStaff)
    verbose_name = _("Upload area")
    verbose_name_plural = _("Upload areas")
add = UploadAreas.add_item
add('90', _("Uploads"), 'general')



def add_shortcut(*args, **kw):
    return Shortcuts.add_item(*args, **kw)
