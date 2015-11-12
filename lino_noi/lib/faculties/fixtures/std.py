# -*- coding: UTF-8 -*-
"""

"""
from __future__ import unicode_literals
from __future__ import print_function

from lino.api import rt, dd


def objects():
    Faculty = rt.modules.faculties.Faculty
    yield Faculty(name='Analysis')
    yield Faculty(name='Code changes')
    yield Faculty(name='Documentation')
    yield Faculty(name='Testing')
    yield Faculty(name='Configuration')
    yield Faculty(name='Enhancement')
    yield Faculty(name='Optimization')
    yield Faculty(name='Offer')
