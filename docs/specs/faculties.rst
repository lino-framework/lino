.. _noi.specs.faculties:

================================
Faculties management in Lino Noi
================================


.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_faculties
    
    doctest init:

    >>> import lino
    >>> lino.startup('lino_noi.projects.team.settings.demo')
    >>> from lino.api.doctest import *


Lino Noi has a notions of **faculties** and **competences** which
might be useful in bigger teams for assigning a ticket to a worker.

They are implemented in :mod:`lino_noi.lib.faculties`.  In the Team
demo database they are not really used.  See also :doc:`care` which
has does more usage of them.


.. contents::
  :local:


>>> rt.show(faculties.TopLevelFaculties)
... #doctest: +REPORT_UDIFF
======== =============== ================== ================== ========== ================
 No.      Designation     Designation (de)   Designation (fr)   Children   Parent faculty
-------- --------------- ------------------ ------------------ ---------- ----------------
 1        Analysis        Analysis           Analysis
 2        Code changes    Code changes       Code changes
 3        Documentation   Documentation      Documentation
 4        Testing         Testing            Testing
 5        Configuration   Configuration      Configuration
 6        Enhancement     Enhancement        Enhancement
 7        Optimization    Optimization       Optimization
 8        Offer           Offer              Offer
 **36**
======== =============== ================== ================== ========== ================
<BLANKLINE>


>>> rt.show('faculties.Competences')
... #doctest: +REPORT_UDIFF
==== ================= =============== ========== ========
 ID   User              Faculty         Affinity   Option
---- ----------------- --------------- ---------- --------
 1    Rolf Rompen       Analysis        100
 2    Rolf Rompen       Code changes    70
 3    Rolf Rompen       Documentation   71
 4    Rolf Rompen       Testing         42
 5    Rolf Rompen       Configuration   62
 6    Romain Raffault   Code changes    76
 7    Romain Raffault   Documentation   92
 8    Romain Raffault   Testing         98
 9    Romain Raffault   Configuration   68
 10   Robin Rood        Analysis        23
 11   luc               Analysis        120
 12   luc               Code changes    150
 13   luc               Documentation   75
 14   mathieu           Documentation   46
 15   Robin Rood        Testing         65
 16   mathieu           Testing         42
 17   luc               Configuration   46
 18   mathieu           Configuration   92
                                        **1338**
==== ================= =============== ========== ========
<BLANKLINE>

