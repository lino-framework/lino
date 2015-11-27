.. _noi.specs.memo:

=============
Memo commands
=============

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_memo
    
    doctest init:

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_noi.projects.team.settings.demo'
    >>> from __future__ import print_function 
    >>> from __future__ import unicode_literals
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
>>> html = """See also [ticket 1]."""
>>> print(ses.parse_memo(html))
See also <a href="javascript:Lino.tickets.Tickets.detail.run(null,{ &quot;record_id&quot;: 1 })" title="F&#246;&#246; fails to bar when baz">#1</a>.
