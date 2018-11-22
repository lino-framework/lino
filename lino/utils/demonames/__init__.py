# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

u"""A collection of tools for generating fictive people and addresses.

This module is used by

- :mod:`lino_xl.lib.contacts.fixtures.demo`

- :mod:`lino_xl.lib.addresses.fixtures.demo2`

- :mod:`garble_persons
  <lino_xl.lib.contacts.management.commands.garble_persons>`

- :mod:`garble <lino_welfare.modlib.pcsw.management.commands.garble>`

- :xfile:`garble_tx25.py` in
  :mod:`lino_welfare.modlib.cbss.fixtures.cbss_demo`

.. autosummary::
   :toctree:

   bel
   est
   rus



"""


from .bel import LAST_NAMES_BELGIUM
from .bel import MALE_FIRST_NAMES_FRANCE
from .bel import FEMALE_FIRST_NAMES_FRANCE

from .bel import LAST_NAMES_MUSLIM
from .bel import MALE_FIRST_NAMES_MUSLIM
from .bel import FEMALE_FIRST_NAMES_MUSLIM

from .bel import LAST_NAMES_AFRICAN
from .bel import FEMALE_FIRST_NAMES_AFRICAN
from .bel import MALE_FIRST_NAMES_AFRICAN

from .bel import streets_of_liege

from .est import streets_of_tallinn
from .est import LAST_NAMES_ESTONIA
from .est import MALE_FIRST_NAMES_ESTONIA
from .est import FEMALE_FIRST_NAMES_ESTONIA

from .rus import LAST_NAMES_RUSSIA
from .rus import MALE_FIRST_NAMES_RUSSIA
from .rus import FEMALE_FIRST_NAMES_RUSSIA

