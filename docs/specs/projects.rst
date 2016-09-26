.. _noi.specs.projects:

==================
Project management
==================


.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_projects
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_noi.projects.team.settings.doctests')
    >>> from lino.api.doctest import *


This document specifies the project management functions of Lino Noi,
implemented in :mod:`lino_noi.lib.tickets`.


.. contents::
  :local:


Active projects
===============

>>> rt.show(tickets.ActiveProjects)
=========== =============== ============ =====================================================================================================
 Reference   Name            Start date   Activity overview
----------- --------------- ------------ -----------------------------------------------------------------------------------------------------
 linö        Framewörk       01/01/2009   New: **4**Talk: **3**ToDo: **2**Sticky: **3**Sleeping: **3**Ready: **2**Done: **3**Cancelled: **3**
 téam        Téam            01/01/2010   New: **3**Talk: **4**ToDo: **3**Sticky: **2**Sleeping: **3**Ready: **3**Done: **2**Cancelled: **3**
 docs        Documentatión   01/01/2009   New: **3**Talk: **3**ToDo: **3**Sticky: **4**Sleeping: **2**Ready: **3**Done: **3**Cancelled: **2**
 research    Research        01/01/1998   New: **2**Talk: **3**ToDo: **3**Sticky: **3**Sleeping: **3**Ready: **3**Done: **3**Cancelled: **3**
=========== =============== ============ =====================================================================================================
<BLANKLINE>





Choosing a project
==================

>>> base = '/choices/tickets/Tickets/project'
>>> show_choices("robin", base + '?query=')
<br/>
linö
téam
docs
research
shop

>>> show_choices("robin", base + '?query=frame')
linö
