#coding: latin1

## Copyright Luc Saffre 2003-2005

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

from lino.adamo import *

class Languages(Table):
    def init(self):
        self.addField('id',STRING.child(width=2))
        self.addBabelField('name',STRING)
    
    class Instance(Table.Instance):
        def getLabel(self):
            return self.name

    def populate(self,sess):
        q = sess.query(Languages,'id name')
        if sess.schema.options.big:
            from lino.schemas.sprl.data import languages
            languages.populate(q)
        else:
            q.setBabelLangs('en de fr')
            q.appendRow('en',('English','Englisch','Anglais')     )
            q.appendRow('de',('German','Deutsch', 'Allemand')     )
            q.appendRow('et',('Estonian','Estnisch','Estonien')   )
            q.appendRow('fr',('French','Französisch','Français')  )
            q.appendRow('nl',('Dutch','Niederländisch','Neerlandais'))
            
    
