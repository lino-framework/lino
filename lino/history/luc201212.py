# -*- coding: UTF-8 -*-
# Copyright 2012 Luc Saffre
# License: BSD (see file COPYING for details)

"""
No longer used.
"""

from __future__ import unicode_literals


if False:

    from lino.history import blogger

    #
    DEMOS = blogger.ticket("lino.pr", "Demo Sites", """
  """)

    CMS = blogger.ticket("cms", "Lino as a CMS", """
  Managing Plain Web Content.
  First proof of concept of 
  :mod:`lino_xl.lib.pages`
  """)

    CHANGES = blogger.ticket("lino.dev", "Documenting code changes", """
  Now that the :mod:`lino_xl.lib.pages` has passed the proof of 
  concept phase I started a new attempt to make it easier to 
  write code change reports, and to find them back when needed.
  The current blog system isn't bad, but it has several disadvantages:

  - documenting releases is difficult 
  - no way to make dynamic queries

  """)

    blogger.ticket("lino.core", "Detail of VirtualTable ",
    """
  It seems that `detail_layout` doesn't work on `VirtualTable`.
  """)

    COSI = blogger.ticket("lino.cosi", "Simple Belgian Accounting", """
  First proof of concept of the modules 
  :mod:`lino.modlib.sales`,
  :mod:`lino.modlib.ledger`,
  :mod:`lino.modlib.finan` ...
  """)

    #
    blogger.set_date(20121221)

    blogger.entry(DEMOS, 0152, "",
    """
  The :mod:`garble <lino_welfare.modlib.pcsw.management.commands.garble>` command
  now has an option `--noinput`.

  The reason for this change is that on lino-framework.org I have a batch 
  command to run the `initdb_demo` script of all demo sites. 
  And one of these scripts also calls `garble`, causing a 
  confirmation to be asked somewhere in the middle of the process.
  """)

    DCC = blogger.entry(CHANGES, 0152, "Documenting code changes",
    """
  Wrote a new module :mod:`lino.modlib.codechanges`, 
  with a virtual table `CodeChanges`
  (:menuselection:`Explorer --> System --> Code Changes`)
  displays a list of all changes.
  """)

    #~ blogger.entry(CHANGES,1157,"Documenting code changes (continued)",
    blogger.follow(DCC, 1157,
    """
  Continued on module :mod:`lino.modlib.codechanges`.
  I abandoned a first approach which used a `changes.py` 
  file in each module because
  code changes must be documented in *one central place 
  per developer*, not per module.

  The next approach is using a package :mod:`lino.history`.
  This package is importable Python code where the developer 
  writes down what he does. The first example is 
  :srcref:`/lino/lino/history/luc201212.py`, 
  which contains a report, in Python syntax, 
  about my work in December 2012 (since yesterday).

  A first version just stored these objects in memory 
  and used the existing CodeChanges table.

  While working on this I understand that this system can also 
  be just an intermediate solution on our way to do all this 
  directly in :mod:`lino.projects.presto`.

  So the virtual table CodeChanges goes away, 
  and a fixture :mod:`lino.projects.presto.fixtures.history`
  imports the :mod:`lino.history` package and yields 
  them to the deserializer.

  """)

    blogger.set_date(20121223)

    blogger.follow(DCC, 933, """
  Continued in :mod:`lino.projects.presto.fixtures.history`.

  Side note: 
  while reading about `tags <http://mercurial.selenic.com/wiki/Tag>`_ 
  in Mercurial I noted that 
  MoinMoin produces beautiful results.
  They have even a bug tracker:
  http://moinmo.in/MoinMoinBugs


  """)

    blogger.entry(DEMOS, 1722, "demos at lino-framework.org still broken", """
  There were still a few bugs in the online demo sites.

  NameError "global name 'pages' is not defined".

  Sphinx 0.6.6 (distributed with Debian Squeeze) 
  didn't yet have a module 
  `sphinx.util.nodes` with a function 
  `split_explicit_title`. 
  This caused an ImportError. :mod:`lino.utils.restify` 
  now includes the few lines of code copied from 
  a newer Sphinx version.
  """)

    blogger.entry(CMS, 2304, "Started template inheritance", """
  The sidebar doesn't yet work. 

  The best way to solve this is probably using template inheritance.

  So in a first step I started to use it,
  as described in http://jinja.pocoo.org/docs/api/#loaders,
  by defining 
  an `Environment` instance and my own loader 
  (in :mod:`lino.core.web`).

  I also replaced Django's template engine by Jinja,
  as explained in 
  `Using an alternative template language
  <https://docs.djangoproject.com/en/dev/ref/templates/api/#using-an-alternative-template-language>`_.
  Lino used Django's template engine only for the mandatory 
  `500.html` and `404.html` templates.

  All this is really great! 
  I had never used templates because Django's 
  engine doesn't allow function calls. 
  In the beginning when I discovered Django, 
  I felt clearly that this isn't my thing.
  Cheetah had this feature, and I need it to generate `linolib.js`, 
  but I never really fell in love with Cheetah.
  I plan to replace this one also by Jinja soon.
  I did hear about Jinja, too,
  but I just didn't recognize that this was the door to a great new world.

  """)

    blogger.entry(CMS, 1037, "Sidebar", """
  As if to confirm my decision to throw away my own :mod:`lino.utils.memo`, 
  the Jinja documentation has an entry `Highlighting Active Menu Items
  <http://jinja.pocoo.org/docs/tricks/#highlighting-active-menu-items>`_
  which is a beginning of the answer to my initial issue.
  """)

    blogger.set_date(20121227)

    blogger.entry(COSI, 728, "Detail Layout for BankStatement", """
  There were no workflow buttons in the Detail Layout of 
  :class:`lino.modlib.finan.models.BankStatement`.
  """)

    blogger.entry(COSI, 805, "Preferred width of ChoiceList comboboxes", """
  :mod:`lino.ui.extjs3.ext_elems`
  now adds a hard-coded value to the preferred_width 
  of ChoiceList fields to account for the width of the trigger button.
  """)

    blogger.entry(CMS, 1330, "Miscellaneous", """
  Still experimenting with the big question on
  how to write/generate a user manual for Lino application.
  New vision for pages.Page : removed field `language`, and 
  title and body are now babel fields. 
  Only one record per ref.
  """)

    blogger.set_date(20130109)
    blogger.entry(CMS, 1607, "The next Lino production site?", """
  Started a new Lino site that runs at 
  `http://wwwbeta.lino-framework.org`_.
  But don't (for the moment) waste your time to look at it.
  My vision is to make this the first satisfying community development platform in the world.
  And I agree that rationally speaking it is pure nonsense to believe 
  that I could make something better than Googlecode, Sourceforge or Github.
  That's why I don't yet write very much about what I'm doing.
  """)
