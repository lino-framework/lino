.. _lino.tested.presto:

==================================
Miscellaneous tests in Lino Presto
==================================

.. to run only this test:
    $ python setup.py test -s tests.DocsTests.test_presto
    
    doctest init

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.presto.settings.doctests'
    >>> from lino.api.doctest import *

Test whether the bootstrap3 user interface works:

>>> url = '/bs3/products/Products'
>>> res = test_client.get(url, REMOTE_USER='robin')
>>> print res.status_code
200

