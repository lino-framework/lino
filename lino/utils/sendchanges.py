# Copyright 2010-2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Send an email to a configurable list of addresses when a
configurable database item has been changed.

This is deprecated and no longer being tested.

Importing this module will add a receiver to the
:attr:`on_ui_created <lino.core.signals.on_ui_created>`,
:attr:`on_ui_updated <lino.core.signals.on_ui_updated>` and
:attr:`pre_ui_delete <lino.core.signals.pre_ui_delete>`
signals.

Usage example::

    class Site(Site):
        title = "sendchanges example"

        def do_site_startup(self):
            super(Site, self).do_site_startup()
            from lino.utils.sendchanges import register, subscribe
            register('contacts.Person', 'first_name last_name birth_date',
                     'created_body.eml', 'updated_body.eml')
            e = register('contacts.Partner', 'name',
                         'created_body.eml', 'updated_body.eml')
            e.updated_subject = "Change in partner {master}"
            subscribe('john.doe@example.org')


TODO: Currently it will go through the global list of emiters for each
update, create, delete. It would be better to analyze the emitters at
startup and install receivers only for the needed models and events.

"""
from builtins import object

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.utils.translation import gettext as _

from lino.api import rt
from lino.core.signals import receiver
from lino.core.signals import on_ui_created, on_ui_updated, pre_ui_delete
from lino.core.fields import fields_list
from lino.core.utils import resolve_model
from lino.core.utils import full_model_name as fmn

SUBSCRIPTIONS = []
EMITTERS = []


class Emitter(object):
    """The object returned by :func:`register`.

    The instantiator takes the following arguments:

    `model` is either a class object or a string with the global name
    of a model (e.g. ``'contacts.Person'``).

    `watched_fields` is a string with a space-separated list of field
    names to watch.

    `master_field` can optionally specify a field which points to the
    "master".

    """
    created_tpl = None
    updated_tpl = None
    deleted_tpl = None
    created_subject = _("Created: {obj}")
    updated_subject = _("Updated: {obj}")
    deleted_subject = _("Deleted: {obj}")
    master_field = None

    def __init__(self, model=None, watched_fields=None,
                 created_tpl=None, updated_tpl=None, deleted_tpl=None,
                 master_field=None):
        """

        """
        if model:
            self.model = model
        if watched_fields:
            self.watched_fields = watched_fields
        self.model = resolve_model(self.model, strict=True)
        self.watched_fields = fields_list(self.model, self.watched_fields)
        if master_field:
            self.master_field = master_field

        for k in ('created_tpl', 'updated_tpl', 'deleted_tpl'):
            v = locals().get(k)
            if v:
                setattr(self, k, v)
            v = getattr(self, k)
            if v:
                setattr(self, k, rt.get_template(v))
        
        # if self.created_tpl:
        #     self.created_tpl = rt.get_template(created_tpl)
        # if updated_tpl:
        #     self.updated_tpl = rt.get_template(updated_tpl)
        # if deleted_tpl:
        #     self.deleted_tpl = rt.get_template(deleted_tpl)

    def __repr__(self):
        return "Emitter('{0}')".format(fmn(self.model))

    def register(self):
        """Register this emitter."""
        assert self not in EMITTERS
        EMITTERS.append(self)
        return self

    def get_master(self, obj):
        if self.master_field is None:
            return None
        return getattr(obj, self.master_field)

    def get_recipients(self, **kwargs):
        """Return the list of recipients. Default is to return the global
        list.

        """
        return SUBSCRIPTIONS

    def emit_created(self, request, obj, **context):
        """Send "created" mails for the given model instance `obj`."""
        if self.created_tpl:
            context.update(obj=obj)
            context.update(master=self.get_master(obj))
            subject = self.created_subject.format(**context)
            recs = self.get_recipients(**context)
            self.sendmails(request, subject, recs, self.created_tpl, **context)

    def emit_updated(self, request, cw, **context):
        """Send "updated" mails for the given ChangeWatcher `cw`."""
        if not self.updated_tpl:
            return
        updates = list(cw.get_updates(watched_fields=self.watched_fields))
        if len(updates) == 0:
            # logger.info("20150112 no updates for %s", cw)
            return
        context.update(obj=cw.watched)
        context.update(master=self.get_master(cw.watched))
        context.update(old=cw.original_state)
        context.update(updates=updates)
        subject = self.updated_subject.format(**context)
        recs = self.get_recipients(**context)
        self.sendmails(request, subject, recs, self.updated_tpl, **context)
        
    def emit_deleted(self, request, obj, **context):
        """Send "deleted" mails for the given model instance `obj`."""
        if self.deleted_tpl:
            context.update(obj=obj)
            context.update(master=self.get_master(obj))
            subject = self.deleted_subject.format(**context)
            recs = self.get_recipients(**context)
            self.sendmails(request, subject, recs, self.deleted_tpl, **context)

    def sendmails(self, request, subject, recs, template, **context):
        # logger.info("20150504 sendmails body template %s", template)
        context.update(request=request)
        body = template.render(**context)
        sender = request.user.email or settings.SERVER_EMAIL
        rt.send_email(subject, sender, body, recs)


def subscribe(addr):
    """Subscribe the given email address for getting notified about
    changes.

    """
    SUBSCRIPTIONS.append(addr)


def register(*args, **kwargs):
    """Instantiate an :class:`Emitter` for the given model. `args` and
    `kwargs` are forwarded to :meth:`Emitter.__init__`.

    """
    return Emitter(*args, **kwargs).register()


def find_emitters(obj):
    """Yield all registered emitters for the given database object."""
    # return SUBSCRIPTIONS.get(obj.__class__)
    for e in EMITTERS:
        if isinstance(obj, e.model):
            yield e


@receiver(on_ui_created)
def on_created(sender=None, request=None, **kw):
    # sender is a model instance
    for s in find_emitters(sender):
        s.emit_created(request, sender)


@receiver(on_ui_updated)
def on_updated(sender=None, watcher=None, request=None, **kw):
    # watcher is a ChangeWatcher
    for s in find_emitters(watcher.watched):
        s.emit_updated(request, watcher)


@receiver(pre_ui_delete)
def on_deleted(sender=None, request=None, **kw):
    # sender is a model instance
    for s in find_emitters(sender):
        s.emit_deleted(request, sender)

