"""

mysite.py is intended to be executed from your sitecustomize.py using
a syntax similar to this::

  execfile("...path_where_lino_is_installed.../src/mysite.py")

On my system I installed `sitecustomize.py` in `s:\py-site-packages` 
which is a directory where I install site-specific pure Python
packages independently of the installed Python version.

SET PYTHONPATH=s:/py-site-packages

"""


## site.addsitedir(r"s:\py-site-packages")
## site.addsitedir(r"g:\snapshot\docutils")

## On my machine, Lino is not an installed package, but I use it
## directly from the source because I don't want to re-install it
## after each change.

import site

print __file__
site.addsitedir(r"t:\data\luc\release\lino\src")
# site.addsitedir(r"g:\snapshot\scons\src\engine")
site.addsitedir(r"g:\snapshot\Twisted-1.0.8alpha2")

