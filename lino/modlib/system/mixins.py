# -*- coding: UTF-8 -*-
# Copyright 2011-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.api import dd, _, rt
from lino.core.utils import resolve_fields_list, models_by_base


class Lockable(dd.Model):
    lockable_fields = None

    locked_by = dd.ForeignKey(
        rt.settings.SITE.user_model, null=True, default=None, blank=True,
        on_delete=dd.SET_NULL)

    class Meta(object):
        abstract = True

    @staticmethod
    def get_lockables():
        return models_by_base(Lockable)

    @staticmethod
    def get_lockable_rows(user):
        for m in Lockable.get_lockables():
            for row in m.objects.filter(locked_by=user):
                yield row

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
        self.lock_row(ar)
        ar.success(refresh=True)

    def lock_row(self, ar=None, user=""):
        user = user if user else ar.get_user()

        if self.locked_by_id != None:
            msg = _("{} is being edited by another user. "
                    "Please try again later.")
            raise Warning(msg.format(self))
        self.locked_by = user
        self.save()
        rt.settings.SITE.logger.debug("%s locks %s.%s" % (user, self.__class__, self.pk))


    @dd.action(_("Abort"), sort_index=100, auto_save=None, callable_from='d')
    def release_lock(self, ar):
        self.unlock_row(ar)
        ar.success(refresh=True)

    def unlock_row(self, ar=None, user=""):
        user = user if user else ar.get_user()

        if self.locked_by == user:
            rt.settings.SITE.logger.debug(
                "%s releases lock on %s.%s", self.user, self.__class__, self.pk)
            self.locked_by = None
            self.save()
            self._disabled_fields = None  # clear cache

        elif self.locked_by is None:
            # silently ignore a request to unlock a row if it wasn't
            # locked.  This can happen e.g. when user click Save on a
            # row that wasn't locked.
            rt.settings.SITE.logger.debug(
                "%s cannot unlock %s.%s because it was not locked", self.user, self.__class__, self.pk)
            return

        else:
            # locked by another user.
            # Should we inlcude a better message?
            rt.settings.SITE.logger.debug(
                "%s cannot unlock %s.%s because it was locked by %s", self.user, self.__class__, self.pk, self.locked_by)
            return

    def has_row_lock(self, ar=None, user=""):
        user = user if user else ar.get_user()
        return self.locked_by == user

    #
    # def after_ui_save(self, ar, cw):
    #     self.unlock_row(ar)
    #     super(Lockable, self).after_ui_save(ar, cw)

    def save_existing_instance(self, ar):
        # this is called from both SubmitDetail and SaveGridCell
        if not self.has_row_lock(ar):
            self.lock_row(ar)
        super(Lockable, self).save_existing_instance(ar)
        self.unlock_row(ar)

    def disabled_fields(self, ar):
        df = super(Lockable, self).disabled_fields(ar)
        df.add("locked_by")
        if self.pk is None or self.has_row_lock(ar):
            df.add('acquire_lock')
        else:
            df.add('release_lock')
            if ar.bound_action.action.window_type != "t":
                df |= self.lockable_fields
                df.add('submit_detail')

        # dd.logger.info("20181008 lockable_fields %s", self.lockable_fields)
        return df
