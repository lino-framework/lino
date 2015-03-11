"""A shortcut import for usage in a Django shell or a :manage:`run`
script.

Typical usage::

    >>> from lino.api.shell import *

"""
from django.conf import settings
from lino.api import ad, dd, rt
rt.startup()
globals().update(rt.modules)
