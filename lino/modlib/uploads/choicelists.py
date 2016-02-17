# -*- coding: UTF-8 -*-
# Copyright 2010-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Upload shortcut fields
=========================

An **upload shortcut field** is a configurable virtual field with a
user-friendly interface for managing a subset of uploaded files
related to a given database object.

Usage:

- Declare your Site's upload shortcuts from within your
  :meth:`setup_choicelists
  <lino.core.site.Site.setup_choicelists>`. For example::

    def setup_choicelists(self):
        super(Site, self).setup_choicelists()
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
from django.utils.translation import pgettext_lazy as pgettext

from lino.utils.xmlgen.html import E
from lino.utils import join_elems

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
        return rt.modules.uploads.Upload.objects.filter(
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
    required_roles = dd.required(OfficeStaff)
    verbose_name = _("Upload Area")
    verbose_name_plural = _("Upload Areas")
add = UploadAreas.add_item
add('90', _("Uploads"), 'general')


@dd.receiver(dd.pre_analyze)
def set_upload_shortcuts(sender, **kw):
    """This is the successor for `quick_upload_buttons`."""

    # remember that models might have been overridden.
    UploadType = sender.modules.uploads.UploadType

    for i in list(Shortcuts.items()):

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
                    dd.build_media_url(obj.file.name),
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


def add_shortcut(*args, **kw):
    """Declare an upload shortcut field. This is designed to be called
    from within your :meth:`setup_choicelists
    <lino.core.site.Site.setup_choicelists>`.

    """
    return Shortcuts.add_item(*args, **kw)
