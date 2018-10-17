# -*- coding: UTF-8 -*-
# Copyright 2011-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals
from builtins import object

from lino.api import dd, _
from lino.core.utils import resolve_fields_list

class Lockable(dd.Model):
    """
    Mixin to add row-level edit locking to any model. 

    Models with row-level edit locking are not editable in detail view
    by default.  All form fields are disabled. The user must click
    :guilabel:`Edit` in order to request an edit lock for that row.
    This will enable all fields (except those which are disabled for
    some other reason).

    Caveats: locking a row and then navigating away without changing
    anything will leave the row locked.
    """
    lockable_fields = None
    class Meta(object):
        abstract = True

    @classmethod
    def on_analyze(cls, site):
        super(Lockable, cls).on_analyze(site)
        if cls.lockable_fields is None:
            cls.lockable_fields = cls._meta.get_fields()
        else:
            resolve_fields_list(cls, 'lockable_fields')
        cls.lockable_fields = set([f.name for f in cls.lockable_fields])

    @dd.action(_("Edit"), sort_index=100, callable_from='d')
    def acquire_lock(self, ar):
        ar.get_user().get_preferences().lock_row(self)
        ar.success(refresh=True)
        
    @dd.action(_("Abort"), sort_index=100,
               auto_save=None, callable_from='d')
    def release_lock(self, ar):
        ar.get_user().get_preferences().unlock_row(self)
        ar.success(refresh=True)
        
    def after_ui_save(self, ar, cw):
        up = ar.get_user().get_preferences()
        up.unlock_row(self)
        super(Lockable, self).after_ui_save(ar, cw)

    def save_existing_instance(self, ar):
        # this is called from both SubmitDetail and SaveGridCell
        up = ar.get_user().get_preferences()
        if not up.has_row_lock(self):
            up.lock_row(self)
        super(Lockable, self).save_existing_instance(ar)
        
    def disabled_fields(self, ar):
        df = super(Lockable, self).disabled_fields(ar)
        up = ar.get_user().get_preferences()
        if up.has_row_lock(self):
            df.add('acquire_lock')
        else:
            df.add('release_lock')
            if ar.bound_action.action.window_type == "d":
                df |= self.lockable_fields
            
        # dd.logger.info("20181008 lockable_fields %s", self.lockable_fields)
        return df


