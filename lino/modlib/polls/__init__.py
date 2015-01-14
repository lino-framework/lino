# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""The :mod:`lino.modlib.polls` package provides models and
functionality for managing Polls.

This is the main app for :ref:`polly`.
It is also used in :ref:`welfare`.

.. autosummary::
   :toctree:

    models
    utils
    fixtures.bible
    fixtures.feedback

"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("Polls")

    def setup_main_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('polls.MyPolls')
        m.add_action('polls.MyResponses')

    def setup_config_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('polls.ChoiceSets')

    def setup_explorer_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('polls.Polls')
        m.add_action('polls.Questions')
        m.add_action('polls.Choices')
        m.add_action('polls.Responses')
        m.add_action('polls.AnswerChoices')
        m.add_action('polls.AnswerRemarks')
        #~ m.add_action('polls.Answers')
