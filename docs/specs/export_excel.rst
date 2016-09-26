.. _noi.specs.export_excel:

================================
Exporting to Excel from Lino Noi
================================

This just tests whether certain tables are exportable to Excel.  For
more explanations see :ref:`lino.specs.export_excel` of :ref:`book`.


.. to run only this test:

    $ python setup.py test -s tests.SpecsTests.test_export_excel
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_noi.projects.team.settings.doctests')
    >>> from lino.api.doctest import *



>>> url = "/api/clocking/Sessions?an=export_excel"
>>> res = test_client.get(url, REMOTE_USER='robin')
>>> print(res.status_code)
200

