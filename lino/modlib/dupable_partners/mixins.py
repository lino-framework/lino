# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.mixins.dupable import Dupable


class DupablePartner(Dupable):
    """Model mixin to add to the base classes of your application's
    `contacts.Partner` model.

    Note that doing this does not yet install the `dupable_partners`
    plugin.

    """

    class Meta:
        abstract = True

    dupable_word_model = 'dupable_partners.Word'

    
