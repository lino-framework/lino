"""
Invoke using::

  $ python manage.py run 0905.py
  
Output before the workaround:

  Company(language=u'de',is_active=True,language=u'de')

After:

  Company(name='Test',language=u'de',is_active=True)  
  
"""

from lino.core.modeltools import obj2str
from lino_welfare.modlib.pcsw.models import Company

c = Company(name="Test")
print obj2str(c)

