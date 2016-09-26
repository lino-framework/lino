# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
#
# This file is part of Lino Noi.
#
# Lino Noi is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Noi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Noi.  If not, see
# <http://www.gnu.org/licenses/>.

from lino_noi.lib.clocking.fixtures.std import objects as parent_objects

from lino.api import rt, dd


def objects():
    yield parent_objects()

    ServiceReport = rt.modules.clocking.ServiceReport
    ExcerptType = rt.modules.excerpts.ExcerptType
    kw = dict(
        build_method='weasy2html',
        # template='service_report.weasy.html',
        # body_template='default.body.html',
        # print_recipient=False,
        primary=True, certifying=True)
    kw.update(dd.str2kw('name', ServiceReport._meta.verbose_name))
    yield ExcerptType.update_for_model(ServiceReport, **kw)
