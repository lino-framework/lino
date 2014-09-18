# -*- coding: UTF-8 -*-
# Copyright 2012 Luc Saffre
# License: BSD (see file COPYING for details)

"""
No longer used.
"""

if False:

    #~ blogger = Blogger(username='luc')
    from lino.modlib.tickets.blogger import Blogger
    blogger = Blogger()
    blogger.set_user('luc')

    LINO = blogger.project("lino", "Lino", """
  """,
                           srcref_url_template='http://code.google.com/p/lino/source/browse%s',
                           changeset_url_template='http://code.google.com/p/lino/source/detail?r=%s')

    WELFARE = blogger.project("welfare", "Lino Welfare", """
  """,
                              srcref_url_template='http://code.google.com/p/lino-welfare/source/browse%s',
                              changeset_url_template='http://code.google.com/p/lino-welfare/source/detail?r=%s')

    blogger.set_project(LINO)

    blogger.project("lino.pr", "Public relations", """
  Long-term project. 
  This is when I work on improving the first impression.
  """, parent=LINO)
    blogger.project("lino.dev", "Development process", """
  Release cycle, documentat
  """, parent=LINO)
    blogger.project("cms", "Content management", """
  """, parent=LINO)
    blogger.project("lino.core", "Core functionality", """
  """)
    blogger.project("lino.cosi", "Lino Cosi first prototype ", """
  """)

    blogger.milestone('1.4.3', 20120328)
    blogger.milestone('1.4.5', 20120716)
    blogger.milestone('1.4.7', 20120717)
    blogger.milestone('1.4.8', 20120722)
    blogger.milestone('1.4.9', 20120729)
    blogger.milestone('1.5.3', 20121208)
