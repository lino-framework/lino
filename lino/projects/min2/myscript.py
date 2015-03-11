"""This is myscript.py, an usage example for the `run` management command.

Usage::

  $ manage.py run myscript NNN

where NNN is the id of some existing partner.

"""
import sys
from lino.api.shell import *
if len(sys.argv) != 2:
    print __doc__
    sys.exit(-1)
print contacts.Partner.objects.get(pk=sys.argv[1])
