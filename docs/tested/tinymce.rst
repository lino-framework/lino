.. _lino.tested.tinymce:

=============================
Testing `lino.modlib.tinymce`
=============================

.. to run only this test:

  $ python setup.py test -s tests.DocsTests.test_tinymce

This document tests some functionality of :mod:`lino.modlib.tinymce`.

Currently especially the behaviour of 
:class:`lino.modlib.tinymce.views.Templates`
which is designed to make usage of TinyMCE's
`external_template_list_url <http://www.tinymce.com/wiki.php/Configuration3x:external_template_list_url>`__ setting.


General stuff:

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.min2.settings.doctests'
>>> from lino.api.doctest import *

>>> url = "/tinymce/templates/notes/MyNotes/69/body"
>>> response = test_client.get(url, REMOTE_USER='robin')
>>> response.status_code
200
>>> print(response.content)
... #doctest: +NORMALIZE_WHITESPACE
var tinyMCETemplateList = [ 
[ "hello", "/tinymce/templates/notes/MyNotes/69/body/1", "Inserts 'Hello, world!'" ], 
[ "mfg", "/tinymce/templates/notes/MyNotes/69/body/2", "None" ] 
];

>>> url = "/tinymce/templates/notes/MyNotes/69/body/1"
>>> response = test_client.get(url, REMOTE_USER='robin')
>>> response.status_code
200
>>> print(response.content)
... #doctest: +NORMALIZE_WHITESPACE
<div>Hello, world!</div>

