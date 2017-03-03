# Copyright 2015-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""User roles for this plugin.

"""

from lino.core.roles import UserRole

class CommentsReader(UserRole):
    """This role makes all comments readable. If the aplication defines
    AnonymousUser having this role, then all (non-private) comments
    are publicly visible.

    """
    pass

class CommentsUser(CommentsReader):
    """A user who can post comments.

    """

class CommentsStaff(CommentsUser):
    """A user who manages configuration of comments functionality.

    """


