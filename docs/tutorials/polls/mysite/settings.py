from lino.projects.std.settings import *


class Site(Site):

    title = "Cool Polls"

    def setup_menu(self, profile, main):
        m = main.add_menu("polls", "Polls")
        m.add_action('polls.Polls')
        m.add_action('polls.Choices')

SITE = Site(globals(), 'polls')

# your local settings here

DEBUG = True
