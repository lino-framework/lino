# Copyright 2015-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.core.roles import UserRole

class Helper(UserRole):
    "Can help other users."
    pass

class AuthorshipTaker(UserRole):
    "Can take authorship of objects authored by others."
    pass

