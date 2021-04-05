# -*- coding: UTF-8 -*-
# Copyright 2015-2016 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Defines Lino specific exceptions
"""


class ChangedAPI(Exception):
    """Protect against non-converted legacy code"""
    pass


class UnresolvedChoice(Exception):
    """Raised when some undefined choice name is encountered and
    :attr:`strict_choicelist_values
    <lino.core.site.Site.strict_choicelist_values>`.

    This can happen if an application has evolued and removed a choice
    from some choicelist. When upgrading to the new version, existing
    database content must be migrated.

    """
    pass
