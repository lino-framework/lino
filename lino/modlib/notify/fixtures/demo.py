from lino.api import dd, rt


def objects():
    ar = rt.login('robin')
    for u in rt.models.users.User.objects.all():
        yield rt.models.notify.Notification.notify(
            ar, u, subject="Database initialized",
            body="Hello world", sent=dd.today())
