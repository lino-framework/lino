# -*- coding: UTF-8 -*-
# Copyright 2009-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.system`.

"""
from builtins import object

import logging
logger = logging.getLogger(__name__)

from lino import AFTER18


from django.conf import settings
from django.utils.encoding import force_text

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.modlib.users.choicelists import UserProfiles
from lino.api import dd
from lino.core import actions

from lino.modlib.printing.choicelists import BuildMethods

from lino.core.roles import SiteStaff

from .choicelists import YesNo, Genders, PeriodEvents


class BuildSiteCache(dd.Action):

    """
    Rebuild the site cache.
    This action is available on :class:`About`.
    """
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


@dd.python_2_unicode_compatible
class SiteConfig(dd.Model):
    """This model should have exactly one instance,
    used to store persistent global site parameters.
    Application code sees this instance as ``settings.SITE.site_config``.

    .. attribute:: default_build_method

        The default build method to use when rendering printable documents.

        If this field is empty, Lino uses the value found in
        :attr:`lino.core.site.Site.default_build_method`.

    .. attribute:: simulate_today

        A constant user-defined date to be substituted as current
        system date.

        This should be empty except in situations such as *a
        posteriori* data entry in a prototype.

    """

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

    def __str__(self):
        return force_text(_("Site Parameters"))

    def update(self, **kw):
        """Set some field of the SiteConfig object and store it to the database.
        """
        for k, v in list(kw.items()):
            if not hasattr(self, k):
                raise Exception("SiteConfig has no attribute %r" % k)
            setattr(self, k, v)
        self.full_clean()
        self.save()

    def save(self, *args, **kw):
        #~ print "20130321 SiteConfig.save()", dd.obj2str(self,True)
        super(SiteConfig, self).save(*args, **kw)
        #~ settings.SITE.on_site_config_saved(self)
        #~ settings.SITE.clear_site_config()


def my_handler(sender, **kw):
    #~ print "20130704 Gonna clear_site_config"
    settings.SITE.clear_site_config()
    #~ kw.update(sender=sender)
    dd.database_connected.send(sender)
    #~ dd.database_connected.send(sender,**kw)

from lino.utils.djangotest import testcase_setup
testcase_setup.connect(my_handler)
dd.connection_created.connect(my_handler)
if AFTER18:
    models.signals.post_migrate.connect(my_handler)
else:
    models.signals.post_syncdb.connect(my_handler)


#~ @dd.receiver(dd.database_connected)
#~ def my_callback(sender,**kw):
    #~ settings.SITE.clear_site_config()
#~ dd.connection_created.connect(my_callback)
#~ models.signals.post_syncdb.connect(my_callback)
#~ from lino.utils.djangotest import testcase_setup
#~ testcase_setup.connect(my_callback)
#~ dd.startup.connect(my_callback)
#~ models.signals.post_save.connect(my_callback,sender=SiteConfig)
#~ NOTE : I didn't manage to get that last line working.
#~ When specifying a `sender`, the signal seems to just not get sent.
#~ Worked around this by overriding SiteConfig.save() to call directly clear_site_config()
#~ @dd.receiver(models.signals.post_save, sender=SiteConfig)
#~ def my_callback2(sender,**kw):
    #~ print "callback2"
    #~ settings.SITE.clear_site_config()
#~ models.signals.post_save.connect(my_callback2,sender=SiteConfig)
#~ from django.test.signals import setting_changed
#~ setting_changed.connect(my_callback)
#~ class SiteConfigDetail(dd.FormLayout):
    #~ about = """
    #~ versions:40x5 startup_time:30
    #~ lino.ModelsBySite:70x10
    #~ """
    #~ config = """
    #~ default_build_method
    #~ """
    #~ main = "about config"
    #~ def setup_handle(self,lh):
        #~ lh.config.label = _("Site Parameters")
        #~ lh.about.label = _("About")

class SiteConfigs(dd.Table):

    """
    The table used to present the :class:`SiteConfig` row in a Detail form.
    See also :meth:`lino.Lino.get_site_config`.
    Deserves more documentation.
    """
    model = 'system.SiteConfig'
    required_roles = dd.required(SiteStaff)
    default_action = actions.ShowDetailAction()
    #~ has_navigator = False
    hide_top_toolbar = True
    #~ can_delete = perms.never
    detail_layout = """
    default_build_method
    # lino.ModelsBySite
    """

    do_build = BuildSiteCache()


if settings.SITE.user_model == 'auth.User':
    dd.inject_field(settings.SITE.user_model,
                    'profile', UserProfiles.field())
    dd.inject_field(settings.SITE.user_model, 'language', dd.LanguageField())

