# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from __future__ import unicode_literals, print_function

from django.conf import settings
# from django.db import models
from lino.api import dd, rt, _

from .mixins import UpdateSummariesByMaster, SimpleSummary


class CheckSummaries(dd.Action):
    label = _("Update all summary data")

    def run_from_ui(self, ar, fix=None):
        for sm in rt.models_by_base(SimpleSummary, toplevel_only=True):
            sm.objects.all().delete()
        for mm, summary_models in get_summary_models().items():
            for sm in summary_models:
                dd.logger.info("Updating %s ...", sm._meta.verbose_name_plural)
                for master in sm.get_summary_masters():
                    sm.update_for_master(master)
                
        ar.set_response(refresh=True)

dd.inject_action('system.SiteConfig', check_all_summaries=CheckSummaries())


@dd.receiver(dd.pre_analyze)
def set_summary_actions(sender, **kw):
    for mm, summary_models in get_summary_models().items():
        mm.define_action(
            check_summaries=UpdateSummariesByMaster(
                mm, summary_models))

def get_summary_models():
    summary_masters = dict()
    for sm in rt.models_by_base(SimpleSummary, toplevel_only=True):
        mm = sm.get_summary_master_model()
        lst = summary_masters.setdefault(mm, [])
        lst.append(sm)
    return summary_masters


@dd.schedule_daily()
def checksummaries():
    rt.login().run(settings.SITE.site_config.check_summaries)
