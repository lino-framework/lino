# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.mixins.dupable import Dupable


class DupablePartner(Dupable):
    """Model mixin to add to the base classes of your application's
    `contacts.Partner` model.

    Note that using the mixin does not yet install the plugin, it just
    declares a model as being dupable. In order to activate
    verification, you must also add
    :mod:`lino.modlib.dupable_partners` to your
    :meth:`get_installed_apps
    <lino.core.site.Site.get_installed_apps>` method.

    """

    class Meta:
        abstract = True

    dupable_word_model = 'dupable_partners.Word'
