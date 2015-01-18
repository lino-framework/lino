from lino.projects.std.settings import *
SITE = Site(
    globals(),
    ['lino.modlib.system', 'lino.modlib.users', 'pisa'],
    languages='en de fr')
