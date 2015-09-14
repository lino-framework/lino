# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
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

from lino.modlib.bootstrap3.renderer import Renderer

from lino.modlib.tickets.models import Ticket


class Renderer(Renderer):
    
    def instance_handler(self, ar, obj, **kw):
        return self.get_detail_url(obj, **kw)
            
    def get_detail_url(self, obj, *args, **kw):
        if isinstance(obj, Ticket):
            return self.plugin.build_plain_url(
                'ticket', str(obj.id), *args, **kw)
        # return super(Renderer, self).get_detail_url(self, obj, *args, **kw)


