# Copyright 2014-2015 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Run an SMTP daemon process.

.. autosummary::
   :toctree:

   signals
   management.commands.recmail


"""


from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Mail server")
