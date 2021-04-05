# Copyright 2015-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""User roles for this plugin.

"""

from lino.core.roles import UserRole

class CommentsReader(UserRole):
    """
    Can read all comments. If the aplication defines AnonymousUser
    having this role, then all (non-private) comments are publicly
    visible.
    """
    pass

class CommentsUser(CommentsReader):
    """A user who can post comments.

    """

class CommentsStaff(CommentsUser):
    """A user who manages configuration of comments functionality.

    """

class PrivateCommentsReader(UserRole):
    """A user who has unfiltered access to private comments."""
    pass
