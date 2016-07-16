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
=========== =============== ============ =========================================
 Reference   Name            Start date   Activity overview
----------- --------------- ------------ -----------------------------------------
 linö        Framewörk       01/01/2009   New: **1**Sleeping: **1**Refused: **1**
 téam        Téam            01/01/2010   New: **1**Talk: **1**Ready: **1**
 docs        Documentatión   01/01/2009   Talk: **1**Sticky: **1**Done: **1**
 research    Research        01/01/1998   ToDo: **1**Ready: **1**Refused: **1**
=========== =============== ============ =========================================
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
