# Copyright 2011-2017 Luc Saffre
# License: BSD (see file COPYING for details)

import threading
user_profile_rlock = threading.RLock()
_for_user_profile = None


def with_user_profile(profile, func, *args, **kwargs):
    """Run the given callable `func` with the given user type
    activated. Optional args and kwargs are forwarded to the callable,
    and the return value is returned.

    Nott that this might be deprecated some day since we now have a
    method :meth:`lino.modlib.users.UserType.context` which returns a
    context manager so you can now write::

      with UserTypes.admin.context():
          # some code

    """
    global _for_user_profile

    with user_profile_rlock:
        old = _for_user_profile
        _for_user_profile = profile
        return func(*args, **kwargs)
        _for_user_profile = old


def get_user_profile():
    return _for_user_profile


class UserTypeContext(object):

    def __init__(self, user_type):
        self.user_type = user_type
        
    def __enter__(self):
        global _for_user_profile
        self.old = _for_user_profile
        _for_user_profile = self.user_type
        
    def __exit__(self, exc_type, exc_value, traceback):
        global _for_user_profile
        _for_user_profile = self.old
        
        
# def set_user_profile(up):
#     global _for_user_profile
#     _for_user_profile = up

# set_for_user_profile = set_user_profile


