#~ import sys
#~ print sys.argv
#~ from lino.utils import babel
#~ babel.set_language(sys.argv[0])

from lino.projects.babel_tutorial.models import Products
print Products.to_rst()