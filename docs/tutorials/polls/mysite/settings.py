from lino.projects.std.settings import *


class Site(Site):

    title = "Cool Polls"

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'polls'

    def setup_menu(self, profile, main):
        m = main.add_menu("polls", "Polls")
        m.add_action('polls.Polls')
        m.add_action('polls.Choices')
        super(Site, self).setup_menu(profile, main)

SITE = Site(globals())

# your local settings here

DEBUG = True
