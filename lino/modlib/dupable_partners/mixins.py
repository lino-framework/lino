from builtins import object
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

    class Meta(object):
        abstract = True

    dupable_word_model = 'dupable_partners.Word'


class DupablePerson(DupablePartner):

    class Meta(object):
        abstract = True

    def dupable_matches_required(self):
        """Two persons named *Marie-Louise Dupont* and *Marie-Louise
        Vandenmeulenbos* should *not* match.

        """
        first = self.get_dupable_words(self.first_name)
        return max(2, len(first)+1)

    def unused_find_similar_instances(self, limit, **kwargs):
        first = self.get_dupable_words(self.first_name)
        if len(first) <= 1:
            super(DupablePerson, self).find_similar_instances(limit, **kwargs)
        lst = []
        i = 0

        def matches(other):
            return True

        for o in super(DupablePerson, self).find_similar_instances(
                None, **kwargs):
            if matches(self, o):
                lst.append(o)
                i += 1
                if i >= limit:
                    break
        return lst
            
