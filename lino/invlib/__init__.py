# -*- coding: UTF-8 -*-
# Copyright 2016 by Luc Saffre
# License: BSD, see LICENSE for more details.

"""Extends :mod:`atelier.invlib` by adding a series of Lino-specific
tasks and configuration settings.

Tasks
=====

.. command:: inv initdb

    Runs :manage:`initdb_demo` on every demo project
    :attr:`config.demo_projects`.

    Note: Don't mix up :cmd:`inv initdb` (the invoke command) with
    :manage:`initdb` (the django-admin command).



Configuration settings
======================

This lists the Lino-specific settings available in your
:xfile:`tasks.py` when it uses :mod:`lino.invlib`.  See also
:class:`atelier.invlib`.

.. envvar:: demo_projects

    The list of *Django demo projects* included in this project.

    Django demo projects are used by the test suite and the Sphinx
    documentation.  Before running :command:`inv test` or
    :command:`inv bd`, they must have been initialized.  To initialize
    them, run :command:`inv initdb`.

    It is not launched automatically by :command:`inv test` or
    :command:`inv bd` because it can take some time and is not always
    necessary.


Modules
=======


.. autosummary::
   :toctree:

   ns
   tasks

"""

from atelier.invlib import MyCollection
from lino.invlib import tasks
ns = MyCollection.from_module(tasks)
configs = dict(demo_projects=[])
ns.configure(configs)

