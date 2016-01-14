.. _noi.specs.memo:

=============
Memo commands
=============

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_memo
    
    doctest init:

    >>> from __future__ import print_function 
    >>> from __future__ import unicode_literals
    >>> from lino import startup
    >>> startup('lino_noi.projects.team.settings.demo')
    >>> from lino.api.doctest import *

The :attr:`description
<lino_noi.lib.tickets.models.Ticket.description>` of a ticket is a
formatted HTML text which can contain links, tables, headers, enumerations...

... and it can additionally contain :mod:`memo <lino.utils.memo>`
markup. Examples:

- ``[url http://www.example.com]``
- ``[url http://www.example.com example]``

- ``[ticket 1]``


>>> rt.startup()
>>> ses = rt.login(renderer=dd.plugins.extjs.renderer)
>>> print(ses.parse_memo("See also [ticket 1]."))
See also <a href="javascript:Lino.tickets.Tickets.detail.run(null,{ &quot;record_id&quot;: 1 })" title="F&#246;&#246; fails to bar when baz">#1</a>.
>>> print(ses.parse_memo("See also [url http://www.example.com]."))
See also <a href="http://www.example.com">http://www.example.com</a>.
>>> print(ses.parse_memo("See also [url http://www.example.com example]."))
See also <a href="http://www.example.com">example</a>.
