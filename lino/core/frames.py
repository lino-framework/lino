# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Defines classes :class:`Frame` and :class:`FrameHandle`
"""

import logging
logger = logging.getLogger(__name__)

from lino.ui import base
from lino.core import actors


class FrameHandle(base.Handle):

    def __init__(self, frame):
        #~ assert issubclass(frame,Frame)
        self.actor = frame
        base.Handle.__init__(self)

    def get_actions(self, *args, **kw):
        return self.actor.get_actions(*args, **kw)

    def __str__(self):
        return "%s on %s" % (self.__class__.__name__, self.actor)


class Frame(actors.Actor):

    _handle_class = FrameHandle
    editable = False

    @classmethod
    def get_actor_label(self):
        return self._label or self.default_action.action.label
