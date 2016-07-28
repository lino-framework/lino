import datetime
from atelier.utils import i2t
from lino.api import dd, rt


def objects():
    ar = rt.login('robin')
    now = datetime.datetime.combine(dd.today(), i2t(548))
    for u in rt.models.users.User.objects.all():
        yield rt.models.notify.Notification.create_notification(
            ar, u, subject="Database initialized",
            created=now,
            body="Hello world", sent=now)
