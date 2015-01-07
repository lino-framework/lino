# Copyright 2010-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Send an email to a configurable list of addresses when a
configurable database item has been changed.


Importing this module will add a receiver to the
:attr:`on_ui_created <lino.core.signals.on_ui_created>`,
:attr:`on_ui_updated <lino.core.signals.on_ui_updated>` and
:attr:`pre_ui_delete <lino.core.signals.pre_ui_delete>`
signals.

Typical usage (taken from :doc:`/tutorials/sendchanges/index`)::

    class Site(Site):
        title = "sendchanges example"

        def do_site_startup(self):

            super(Site, self).do_site_startup()

            from lino.utils.sendchanges import subscribe

            subscribe('contacts.Person', 'first_name last_name birth_date',
                      'created_body.eml', 'updated_body.eml')
            subscribe('contacts.Partner', 'name',
                      'created_body.eml', 'updated_body.eml')


Note that the order of subscription is important when the watched
models inherit from each other: for a given model instance, the first
matching subscription will be used.

"""

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.utils.translation import ugettext as _

from lino import rt
from lino.core.signals import receiver
from lino.core.signals import on_ui_created, on_ui_updated, pre_ui_delete
from lino.core.fields import fields_list
from lino.core.dbutils import resolve_model
from lino.core.dbutils import full_model_name as fmn

SUBSCRIPTIONS = []
EMITTERS = []


class Emitter(object):
    create_tpl = None
    update_tpl = None
    delete_tpl = None

    def __init__(self, model, watched_fields,
                 create_tpl=None, update_tpl=None, delete_tpl=None):
        self.model = resolve_model(model, strict=True)
        self.watched_fields = fields_list(self.model, watched_fields)
        if create_tpl:
            self.create_tpl = rt.get_template(create_tpl)
        if update_tpl:
            self.update_tpl = rt.get_template(update_tpl)
        if delete_tpl:
            self.delete_tpl = rt.get_template(delete_tpl)

    def __repr__(self):
        return "Emitter('{0}')".format(fmn(self.model))

    def emit_created(self, request, obj, **context):
        """Send "created" mails for the given model instance `obj`."""
        if self.create_tpl:
            subject = _("Created: {0}").format(obj)
            context.update(obj=obj)
            self.sendmails(request, subject, self.create_tpl, **context)

    def emit_updated(self, request, cw, **context):
        """Send "updated" mails for the given ChangeWatcher `cw`."""
        if not self.update_tpl:
            return
        updates = list(cw.get_updates(watched_fields=self.watched_fields))
        if len(updates) == 0:
            return
        subject = _("Updated: {0}").format(cw.watched)
        context.update(obj=cw.watched)
        context.update(old=cw.original_state)
        context.update(updates=updates)
        self.sendmails(request, subject, self.update_tpl, **context)
        
    def emit_deleted(self, request, obj, **context):
        """Send "deleted" mails for the given model instance `obj`."""
        if self.delete_tpl:
            subject = _("Deleted: {0}").format(obj)
            context.update(obj=obj)
            self.sendmails(request, subject, self.delete_tpl, **context)

    def sendmails(self, request, subject, template, **context):
        # logger.info("body template %s, template)
        context.update(request=request)
        body = template.render(**context)
        sender = request.user.email or settings.SERVER_EMAIL
        rt.send_email(subject, sender, body, SUBSCRIPTIONS)


def subscribe(addr):
    SUBSCRIPTIONS.append(addr)


def register(*args, **kwargs):
    """Register an :class:`Emitter` for the given model (`args` and
    `kwargs` see :meth:`Emitter.__init__`.

    """
    sub = Emitter(*args, **kwargs)
    EMITTERS.append(sub)
    return sub


def find_emitter(obj):
    """Return the registered subscription for the given model instance."""
    # return SUBSCRIPTIONS.get(obj.__class__)
    for e in EMITTERS:
        if isinstance(obj, e.model):
            return e


@receiver(on_ui_created)
def on_created(sender=None, request=None, **kw):
    # sender is a model instance
    s = find_emitter(sender)
    if s is not None:
        s.emit_created(request, sender)


@receiver(on_ui_updated)
def on_updated(sender=None, request=None, **kw):
    # sender is a ChangeWatcher
    s = find_emitter(sender.watched)
    if s is not None:
        s.emit_updated(request, sender)


@receiver(pre_ui_delete)
def on_deleted(sender=None, request=None, **kw):
    # sender is a model instance
    s = find_emitter(sender)
    if s is not None:
        s.emit_deleted(request, sender)

