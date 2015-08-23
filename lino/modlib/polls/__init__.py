# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Provides database models and functionality for managing polls.

This is the main plugin for :ref:`polly`.  It is also used in
:ref:`welfare`.

.. autosummary::
   :toctree:

    roles
    models
    choicelists
    utils
    fixtures.bible
    fixtures.feedback

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

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
        m.add_action('polls.AllPolls')
        m.add_action('polls.Questions')
        m.add_action('polls.Choices')
        m.add_action('polls.AllResponses')
        m.add_action('polls.AnswerChoices')
        m.add_action('polls.AllAnswerRemarks')
        #~ m.add_action('polls.Answers')
