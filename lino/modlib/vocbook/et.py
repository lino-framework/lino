# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Work in progress.

See :srcref:`docs/tickets/92`.

"""

from lino.modlib.vocbook.base import Language, Word, WordType


class EstonianWord(Word):
    pass


class Estonian(Language):

    @classmethod
    def parse_word(cls, s, **kw):
        s = s.strip()
        return cls.register_word(EstonianWord(s, **kw))
