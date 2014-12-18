# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models.py` module of the :mod:`lino.modlib.system` app.
"""

import logging
logger = logging.getLogger(__name__)


from django.conf import settings
from django.utils.encoding import force_unicode

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import mixins
from lino import dd
from lino.core import actions

from lino.mixins.printable import BuildMethods
from lino.modlib.users.mixins import UserProfiles

from .mixins import *


class BuildSiteCache(dd.Action):

    """
    Rebuild the site cache.
    This action is available on :class:`About`.
    """
    label = _("Rebuild site cache")
    url_action_name = "buildjs"

    def run_from_ui(self, ar):
        #~ rr.confirm(_("Are you sure?"))
        #~ rr.confirm(_("Are you really sure?"))
        settings.SITE.ui.default_renderer.build_site_cache(True)
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

    """
    This model should have exactly one instance,
    used to store persistent global site parameters.
    Application code sees this instance as ``settings.SITE.site_config``.
    """

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'SiteConfig')
        verbose_name = _("Site configuration")

    objects = SiteConfigManager()
    real_objects = models.Manager()

    default_build_method = BuildMethods.field(
        verbose_name=_("Default build method"),
        blank=True, null=True)

    def __unicode__(self):
        return force_unicode(_("Site Parameters"))

    def update(self, **kw):
        for k, v in kw.items():
            if not hasattr(self, k):
                raise Exception("Siteconfig has no attribute %r" % k)
            setattr(self, k, v)
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
    required = dd.required(user_level='manager')
    default_action = actions.ShowDetailAction()
    #~ has_navigator = False
    hide_top_toolbar = True
    #~ can_delete = perms.never
    detail_layout = """
    default_build_method
    # lino.ModelsBySite
    """

    do_build = BuildSiteCache()


if settings.SITE.user_model:

    class TextFieldTemplate(mixins.AutoUser):

        """A reusable block of text that can be selected from a text editor to
        be inserted into the text being edited.

        """

        class Meta:
            verbose_name = _("Text Field Template")
            verbose_name_plural = _("Text Field Templates")

        name = models.CharField(_("Designation"), max_length=200)
        description = dd.RichTextField(_("Description"),
                                       blank=True, null=True, format='plain')
            #~ blank=True,null=True,format='html')
        # team = dd.ForeignKey(
        #     'users.Team', blank=True, null=True,
        #     help_text=_("If not empty, then this template "
        #                 "is reserved to members of this team."))
        text = dd.RichTextField(_("Template Text"),
                                blank=True, null=True, format='html')

        def __unicode__(self):
            return self.name

    class TextFieldTemplates(dd.Table):
        model = TextFieldTemplate
        required = dd.required(user_groups='office', user_level='admin')
        insert_layout = dd.FormLayout("""
        name
        user #team
        """, window_size=(60, 'auto'))

        detail_layout = """
        id name user #team
        description
        text
        """

    class MyTextFieldTemplates(TextFieldTemplates, mixins.ByUser):
        required = dd.required(user_groups='office')


config = dd.plugins.system
# SYSTEM_USER_LABEL = _("System")
OFFICE_MODULE_LABEL = _("Office")


def setup_main_menu(site, ui, profile, m):
    #~ office = m.add_menu("office",OFFICE_MODULE_LABEL)
    #~ office.add_action(MyTextFieldTemplates)
    pass


def setup_config_menu(site, ui, profile, m):
    office = m.add_menu("office", OFFICE_MODULE_LABEL)
    system = m.add_menu("system", config.verbose_name)
    #~ m.add_action('links.LinkTypes')
    system.add_instance_action(site.site_config)
    if site.user_model and profile.authenticated:
        system.add_action(site.user_model)
        # system.add_action(site.modules.users.Teams)
        office.add_action(MyTextFieldTemplates)
    #~ m.add_action(site.modules.users.Users)


def setup_explorer_menu(site, ui, profile, m):
    office = m.add_menu("office", OFFICE_MODULE_LABEL)
    system = m.add_menu("system", config.verbose_name)

    if site.user_model:
        system.add_action(site.modules.users.Authorities)
        system.add_action(dd.UserGroups)
        system.add_action(dd.UserLevels)
        system.add_action(UserProfiles)
        office.add_action(TextFieldTemplates)


dd.add_user_group('office', OFFICE_MODULE_LABEL)


if settings.SITE.user_model == 'auth.User':
    dd.inject_field(settings.SITE.user_model,
                    'profile', UserProfiles.field())
    dd.inject_field(settings.SITE.user_model, 'language', dd.LanguageField())

