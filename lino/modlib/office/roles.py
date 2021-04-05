# Copyright 2015-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.core.roles import UserRole


class OfficeUser(UserRole):
    pass


class OfficeOperator(UserRole):
    pass


class OfficeStaff(OfficeUser, OfficeOperator):
    pass

