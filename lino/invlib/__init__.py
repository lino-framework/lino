# -*- coding: UTF-8 -*-
# Copyright 2016-2017 by Luc Saffre
# License: BSD, see LICENSE for more details.

"""See :doc:`/dev/invlib`.

"""

from atelier.invlib import MyCollection
from lino.invlib import tasks
ns = MyCollection.from_module(tasks)
configs = dict(demo_projects=[])
ns.configure(configs)

