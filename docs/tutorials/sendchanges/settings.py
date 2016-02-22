from __future__ import print_function

from lino.projects.docs.settings import *

EMAIL_TEMPLATE = """\
To: {recipients}
Subject: {subject}
{body}"""


class Site(Site):
    title = "sendchanges example"

    default_user = "robin"
    user_profiles_module = None
    # user_profiles_module = 'lino.modlib.office.roles'

    def send_email(self, subject, sender, body, recipients):
        # override for this test so that it does not actually send
        # anything.
        recipients = ', '.join(recipients)
        print(EMAIL_TEMPLATE.format(**locals()))

    def do_site_startup(self):

        super(Site, self).do_site_startup()

        from lino.utils.sendchanges import subscribe, register
        
        register('contacts.Person', '*',
                 'created_body.eml', 'updated_body.eml')
        e = register('contacts.Partner', 'name',
                     'created_body.eml', 'updated_body.eml')
        e.created_subject = "Created partner {obj}"
        e.updated_subject = "Change in partner {obj}"

        subscribe('john@example.com')
        subscribe('joe@example.com')

SITE = Site(globals())

DEBUG = True
