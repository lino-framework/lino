# This is needed only if Lino does not yet have a default demo
# administrator for your language.

from django.conf import settings
from lino.modlib.users.choicelists import UserProfiles


def objects():
    yield settings.SITE.user_model(username="es_demo_root", language="es",
                                   first_name="Roberto",
                                   last_name="Spanish",
                                   email=settings.SITE.demo_email,
                                   profile=UserProfiles.admin)

