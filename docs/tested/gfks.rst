.. _lino.tested.gfks:

====================
Generic Foreign Keys
====================

This document tests some functionalities implemented by
:mod:`lino.modlib.gfks`.


.. to run only this test:

    $ python setup.py test -s tests.DocsTests.test_gfks
    
    doctest init:

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.min1.settings.doctests'
    >>> from lino.api.doctest import *



The detail view of :class:`lino.modlib.gfks.ContentTypes` has the
following fields:

>>> d = get_json_dict('robin', 'gfks/ContentTypes/9')
>>> sorted(d.keys())
[u'data', u'disable_delete', u'id', u'navinfo', u'title']
>>> sorted(d['data'].keys())
[u'app_label', u'base_classes', u'disable_editing', u'disabled_actions', u'disabled_fields', u'id', u'model', u'name']
>>> for k in sorted(d['data'].keys()):
...    print k, d['data'][k]
app_label contacts
base_classes <p />
disable_editing False
disabled_actions {}
disabled_fields {u'id': True}
id 9
model role
name Contact Person
