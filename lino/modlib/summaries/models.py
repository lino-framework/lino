# Copyright 2016-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from __future__ import unicode_literals, print_function

from django.conf import settings
# from django.db import models
from lino.api import dd, rt, _

from .mixins import UpdateSummariesByMaster, SlaveSummarized, Summarized


class CheckAllSummaries(dd.Action):
    label = _("Check all summary data")

    def run_from_ui(self, ar, fix=None):
        for sm in rt.models_by_base(Summarized, toplevel_only=True):
            dd.logger.info("Updating summary data for %s ...", sm._meta.verbose_name_plural)
            sm.check_all_summaries()

        ar.set_response(refresh=True)

dd.inject_action('system.SiteConfig', check_all_summaries=CheckAllSummaries())


@dd.receiver(dd.pre_analyze)
def set_summary_actions(sender, **kw):
    for mm, summary_models in masters_with_summaries().items():

        # remove plain Summarizable models who are their own master, so they
        # have their own check_summaries button.

        summary_models = [sm for sm in summary_models if sm is not mm]
        # if issubclass(mm, SimpleSummary):
        if len(summary_models):
            mm.define_action(
                check_summaries=UpdateSummariesByMaster(
                    mm, summary_models))

def masters_with_summaries():
    """
    Return a dict mapping each model that is a summary master to the list of
    its slave summaries.

    """
    summary_masters = dict()
    for sm in rt.models_by_base(SlaveSummarized, toplevel_only=True):
        mm = sm.get_summary_master_model()
        lst = summary_masters.setdefault(mm, [])
        lst.append(sm)
    return summary_masters


@dd.schedule_daily()
def checksummaries():
    rt.login().run(settings.SITE.site_config.check_all_summaries)
