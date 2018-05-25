"""A shortcut import for usage in a Django shell or a :manage:`run`
script.

Typical usage::

    >>> from lino.api.shell import *

"""
from lino import AFTER17
if AFTER17:
    import django
    django.setup()
from django.conf import settings
from lino.api import ad, dd, rt
rt.startup()
globals().update(rt.models)
