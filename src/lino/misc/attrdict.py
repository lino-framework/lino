## Copyright Luc Saffre 2003-2004.

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import types

class AttrDict(dict):
    def __init__(self,d=None,factory=None):
        if d is None:
            d = {}
        self.__dict__["_values"] = d
        self.__dict__["_factory"] = factory
        for m in ('values','__len__','keys','items','get'):
            self.__dict__[m] = getattr(d,m)

    def __getattr__(self,name):
        try:
            return self._values[name]
        except KeyError,e:
            if self._factory is not None:
                v = self._factory(name)
                self._values[name] = v
                return v
            raise AttributeError,e

    def __setattr__(self,name,value):
        raise "Not allowed"

    def define(self,name,value):
        assert type(name) == types.StringType
        assert name.isalnum(), "invalid attribute name %s" % name
        assert not self._values.has_key(name), \
               "duplicate key %s" % repr(name)
        self._values[name] = value

    def installto(self,d):
        d.update(self._values)

