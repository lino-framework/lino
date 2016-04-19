.. _lino.specs.html:

===============
Generating HTML
===============

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_html
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino.projects.polly.settings.demo')
    >>> from lino.api.doctest import *

.. contents::
   :depth: 1
   :local:


>>> from lino.utils.xmlgen.html import E

>>> txt = "foo"
>>> txt = E.b(txt)
>>> if not txt:
...    print ("oops")
oops
>>> ar = rt.login('robin', renderer=settings.SITE.kernel.default_renderer)
>>> obj = ar.user
>>> print(E.tostring(ar.obj2html(obj, txt)))
<a href="javascript:Lino.users.Users.detail.run(null,{ &quot;record_id&quot;: 1 })"><b>foo</b></a>

