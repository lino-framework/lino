# Copyright 2014-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
A series of wrapper modules to encapsulate Lino's core
functionalities.  They don't define anything on their own but just
import things which are commonly used in different contexts.

One module for each of the three startup phases used when writing
application code:

- :doc:`/dev/ad` contains classes and functions that are available
  already **before** your Lino application gets initialized.  You use
  it to define your **overall application structure** (in your
  :xfile:`settings.py` files and in the :xfile:`__init__.py` files of
  your plugins).


- :doc:`/dev/dd` is for when you are **describing your database
  schema** (in your :xfile:`models.py` modules).

- :doc:`/dev/rt` contains functions and classes which are commonly
  used "at runtime", i.e. when the Lino application has been
  initialized.

  You may *import* it at the global namespace of a :xfile:`models.py`
  file, but you can *use* most of it only when the :func:`startup`
  function has been called.

Recommended usage is to import these modules as follows::

  from lino.api import ad, dd, rt, _

Another set of modules defined here are for more technical usage in
specialized context:

.. autosummary::
   :toctree:

   doctest
   shell
   selenium
"""

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
from django.utils.translation import ugettext as gettext
