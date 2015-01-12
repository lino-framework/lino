from lino.projects.min1.settings import *

EMAIL_TEMPLATE = """\
To: {recipients}
Subject: {subject}
{body}"""


class Site(Site):
    title = "sendchanges example"

    def send_email(self, subject, sender, body, recipients):
        # override for this test so that it does not actually send
        # anything.
        recipients = ', '.join(recipients)
        print EMAIL_TEMPLATE.format(**locals())

    def do_site_startup(self):

        super(Site, self).do_site_startup()

        from lino.utils.sendchanges import subscribe, register
        
        register('contacts.Person', 'first_name last_name birth_date',
                 'created_body.eml', 'updated_body.eml')
        register('contacts.Partner', 'name',
                 'created_body.eml', 'updated_body.eml')

        subscribe('john@example.com')
        subscribe('joe@example.com')

SITE = Site(globals())
