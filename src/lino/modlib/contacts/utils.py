## Copyright 2010 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""

http://en.wikipedia.org/wiki/Dutch_name
http://www.myheritage.com/support-post-130501/dutch-belgium-german-french-surnames-with-prefix-such-as-van?lang=RU


Examples:

>>> name2kw("Saffre Luc")
{'first_name': 'Luc', 'last_name': 'Saffre'}
>>> name2kw("Van Rompuy Herman")
{'first_name': 'Herman', 'last_name': 'Van Rompuy'}
>>> name2kw("'T Jampens Jan")
{'first_name': 'Jan', 'last_name': "'T Jampens"}
>>> name2kw("Van den Bossche Marc Antoine Bernard")
{'first_name': 'Marc Antoine Bernard', 'last_name': 'Van den Bossche'}


"""

name_prefixes1 = ("HET", "'T",'VAN','DER', 'TER','VON','OF', "DE", "DU", "EL", "AL")
name_prefixes2 = ("VAN DEN","VAN DE","IN HET", "VON DER","DE LA")

def name2kw(s,**kw):
    a = s.split()
    if len(a) == 1:
        kw['last_name'] = a[0]
    elif len(a) == 2:
        kw['last_name'] = a[0]
        kw['first_name'] = a[1]
    else:
        # name consisting of more than 3 words
        a01 = a[0] + ' ' + a[1]
        if a01.upper() in name_prefixes2:
            kw['last_name'] = a01 + ' ' + a[2]
            kw['first_name'] = ' '.join(a[3:])
        elif a[0].upper() in name_prefixes1:
            kw['last_name'] = a[0] + ' ' + a[1]
            kw['first_name'] = ' '.join(a[2:])
        else:
            kw['last_name'] = a[0] 
            kw['first_name'] = ' '.join(a[1:])
    return kw


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

