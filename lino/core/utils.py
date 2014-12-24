# Copyright 2010-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals


class Requirements(object):

    """
    Not yet used. TODO: implement requirements as a class. 
    - handle conversions (like accepting both list and string for `user_groups` ),
    - implement loosen_requirements as __or__() 
    - implement add_requirements as __and__() 
    """
    user_level = None
    user_groups = None
    states = None
    allow = None
    auth = True
    owner = None


