# -*- coding: UTF-8 -*-
# Copyright 2009-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from django.conf import settings
from django.utils.encoding import force_text

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.apps import apps ; get_models = apps.get_models

from lino.api import dd, rt
from lino.core import actions
from lino.core.utils import full_model_name
from lino.core.roles import SiteStaff

from lino.modlib.printing.choicelists import BuildMethods
from lino.modlib.checkdata.choicelists import Checker


# import them here to have them on rt.models.system:
from .choicelists import YesNo, Genders, PeriodEvents
from .mixins import Lockable


class BuildSiteCache(dd.Action):
    label = _("Rebuild site cache")
    url_action_name = "buildjs"

    def run_from_ui(self, ar):
        settings.SITE.kernel.default_renderer.build_site_cache(True)
        return ar.success(
            """\
Seems that it worked. Refresh your browser.
<br>
Note that other users might experience side effects because
of the unexpected .js update, but there are no known problems so far.
Please report any anomalies.""",
            alert=_("Success"))


class SiteConfigManager(models.Manager):

    def get(self, *args, **kwargs):
        return settings.SITE.site_config



class SiteConfig(dd.Model):

    class Meta(object):
        abstract = dd.is_abstract_model(__name__, 'SiteConfig')
        verbose_name = _("Site configuration")

    objects = SiteConfigManager()
    real_objects = models.Manager()

    default_build_method = BuildMethods.field(
        verbose_name=_("Default build method"),
        blank=True, null=True)

    simulate_today = models.DateField(
        _("Simulated date"), blank=True, null=True)

    site_company = dd.ForeignKey(
        "contacts.Company",
        blank=True, null=True,
        verbose_name=_("Site owner"),
        related_name='site_company_sites')


    def __str__(self):
        return force_text(_("Site Parameters"))

    def update(self, **kw):
        """
        Set some field of the SiteConfig object and store it to the
        database.
        """
        # print("20180502 update({})".format(kw))
        for k, v in kw.items():
            if not hasattr(self, k):
                raise Exception("SiteConfig has no attribute %r" % k)
            setattr(self, k, v)
        self.full_clean()
        self.save()

    def save(self, *args, **kw):
        # print("20180502 save() {}".format(dd.obj2str(self, True)))
        super(SiteConfig, self).save(*args, **kw)
        settings.SITE.clear_site_config()


def my_handler(sender, **kw):
    # print("20180502 {} my_handler calls clear_site_config()".format(
    #     settings.SITE))
    settings.SITE.clear_site_config()
    #~ kw.update(sender=sender)
    # dd.database_connected.send(sender)
    #~ dd.database_connected.send(sender,**kw)

from django.test.signals import setting_changed
from lino.core.signals import testcase_setup
setting_changed.connect(my_handler)
testcase_setup.connect(my_handler)
dd.connection_created.connect(my_handler)
models.signals.post_migrate.connect(my_handler)


class SiteConfigs(dd.Table):

    model = 'system.SiteConfig'
    required_roles = dd.login_required(SiteStaff)
    # default_action = actions.ShowDetail()
    #~ has_navigator = False
    hide_top_toolbar = True
    #~ can_delete = perms.never
    detail_layout = """
    default_build_method
    # lino.ModelsBySite
    """

    @classmethod
    def get_default_action(cls):
        return actions.ShowDetail(cls.detail_layout)



    do_build = BuildSiteCache()


# if settings.SITE.user_model == 'users.User':
#     dd.inject_field(settings.SITE.user_model,
#                     'user_type', UserTypes.field())
#     dd.inject_field(settings.SITE.user_model, 'language', dd.LanguageField())



class BleachChecker(Checker):

    verbose_name = _("Find unbleached html content")
    model = dd.Model

    def get_checkable_models(self):

        for m in super(BleachChecker, self).get_checkable_models():
            if len(m._bleached_fields):
                yield m

    def get_checkdata_problems(self, obj, fix=False):
        t = tuple(obj.fields_to_bleach())
        if len(t):
            fldnames = ', '.join([f.name for f, old, new in t])
            yield (True, _("Fields {} have unbleached content.").format(fldnames))
            if fix:
                obj.before_ui_save(None)
                obj.full_clean()
                obj.save()


BleachChecker.activate()
