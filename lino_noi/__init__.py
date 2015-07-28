# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""This is the main module of the Lino framework.

.. autosummary::
   :toctree:

   settings
   lib
   fixtures.linotickets
   urls


"""

import os

execfile(os.path.join(os.path.dirname(__file__), 'project_info.py'))
__version__ = SETUP_INFO['version']

intersphinx_urls = dict(docs="http://noi.lino-framework.org")
srcref_url = 'https://github.com/lsaffre/lino-noi/blob/master/%s'

