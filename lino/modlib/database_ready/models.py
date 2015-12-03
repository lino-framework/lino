# django.db.models.signals.post_migrate

# Sent by the migrate command after it installs an application, and
# the flush command. It's not emitted for applications that lack a
# models module.

# It is important that handlers of this signal perform idempotent
# changes (e.g. no database alterations) as this may cause the flush
# management command to fail if it also ran during the migrate
# command.

from django.db.models.signals import post_migrate
from django.db import models
from lino.core.signals import database_ready


def send_database_ready(sender, **kwargs):
    raise Exception("20151203 send_database_ready")
    from django.conf import settings
    database_ready.send(settings.SITE)

post_migrate.connect(send_database_ready)


class Foo(models.Model):
    pass
    
