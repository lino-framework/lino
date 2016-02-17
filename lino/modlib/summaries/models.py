# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""The :xfile:`models.py` module for `lino.modlib.summaries`.

"""

from __future__ import unicode_literals, print_function

from lino.api import dd, rt, _

from .mixins import UpdateSummariesByMaster, Summary


class CheckSummaries(dd.Action):
    """Web UI version of :manage:`checksummaries`. See there."""
    label = _("Update all summary data")

    def run_from_ui(self, ar, fix=None):
        for mm, summary_models in list(get_summary_models().items()):
            for sm in summary_models:
                dd.logger.info("Updating %s ...", sm._meta.verbose_name_plural)
                for master in sm.get_summary_masters():
                    sm.update_for_master(master)
                
        ar.set_response(refresh=True)

dd.inject_action('system.SiteConfig', check_summaries=CheckSummaries())


@dd.receiver(dd.pre_analyze)
def set_summary_actions(sender, **kw):
    """Installs the `update_summaries` action (an instance of
    :class:`UpdateSummariesByMaster
    <lino.modlib.summaries.mixins.UpdateSummariesByMaster>`) on every
    model for which there is at least one Summary

    """
    for mm, summary_models in list(get_summary_models().items()):
        mm.define_action(
            update_summaries=UpdateSummariesByMaster(mm, summary_models))


def get_summary_models():
    """Return a `dict` mapping each model which has at least one summary
    to a list of these summaries.

    """
    summary_masters = dict()
    for sm in rt.models_by_base(Summary, toplevel_only=True):
        mm = sm.get_summary_master_model()
        lst = summary_masters.setdefault(mm, [])
        lst.append(sm)
    return summary_masters

