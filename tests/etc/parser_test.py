# Luc Saffre
# 2002-02-27

import re

from lino.misc.parser import SimpleParser

s1 = """
Das ist ein Versuch.
__name__ = [%s __name__]
Jawohl.
"""

s2 = "Der Wert ist [%d self.value]. Jawohl!"


class Obj:
    def __init__(self,value):
        self.value = value

if False:        

	#a = re.split(r'([^\[]*)\[([^\]])\]', s)

	#print repr(a)

	p = SimpleParser(globals(),{})
	print p.parse(s1)

	o = Obj(4)
	p = SimpleParser(o)
	print p.parse(s2)

