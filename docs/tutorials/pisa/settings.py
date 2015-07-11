from lino.projects.std.settings import *

SITE = Site(
    globals(),
    ['lino.modlib.printing', 
     # 'lino.modlib.system',
     'lino.modlib.users', 
     'pisa'],
    languages='en de fr')
