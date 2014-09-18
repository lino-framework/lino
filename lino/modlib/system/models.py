# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models.py` module of the :mod:`lino.modlib.system` app.
"""

import logging
logger = logging.getLogger(__name__)


from django.conf import settings
from django.contrib.contenttypes import models as contenttypes
from django.utils.encoding import force_unicode

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import mixins
from lino import dd
from lino.core.dbutils import resolve_field
from lino.core import actions
from lino.utils.xmlgen.html import E
from lino.utils import join_elems

from lino.mixins.printable import BuildMethods


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

from djangosite.utils.djangotest import testcase_setup
testcase_setup.connect(my_handler)
dd.connection_created.connect(my_handler)
models.signals.post_syncdb.connect(my_handler)


#~ @dd.receiver(dd.database_connected)
#~ def my_callback(sender,**kw):
    #~ settings.SITE.clear_site_config()
#~ dd.connection_created.connect(my_callback)
#~ models.signals.post_syncdb.connect(my_callback)
#~ from djangosite.utils.djangotest import testcase_setup
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


if settings.SITE.is_installed('contenttypes'):

    class ContentTypes(dd.Table):

        """
        Deserves more documentation.
        """
        model = contenttypes.ContentType

        required = dd.required(user_level='manager')

        detail_layout = """
      id name app_label model base_classes
      system.HelpTextsByModel
      """

        @dd.displayfield(_("Base classes"))
        def base_classes(self, obj, ar):
            chunks = []

            def add(cl):
                for b in cl.__bases__:
                    add(b)
                # :
                if issubclass(cl, dd.Model) and cl is not dd.Model \
                   and cl._meta.managed:
                    if getattr(cl, '_meta', False) and not cl._meta.abstract:
                        #~ logger.info("20120205 adding(%r)",cl)
                        ct = contenttypes.ContentType.objects.get_for_model(cl)
                        chunks.append(
                            ar.obj2html(ct, unicode(cl._meta.verbose_name)))
            if obj is not None:
                #~ add(obj.model_class())
                for b in obj.model_class().__bases__:
                    add(b)
            return E.p(*join_elems(chunks, sep=', '))

    class HelpText(dd.Model):

        class Meta:
            verbose_name = _("Help Text")
            verbose_name_plural = _("Help Texts")

        content_type = models.ForeignKey(contenttypes.ContentType,
                                         verbose_name=_("Model"))
        field = models.CharField(_("Field"), max_length=200)

        help_text = dd.RichTextField(_("HelpText"),
                                     blank=True, null=True, format='plain')

        def __unicode__(self):
            return self.content_type.app_label + '.' \
                + self.content_type.model + '.' + self.field

        @dd.chooser(simple_values=True)
        def field_choices(cls, content_type):
            l = []
            if content_type is not None:
                model = content_type.model_class()
                meta = model._meta
                for f in meta.fields:
                    if not getattr(f, '_lino_babel_field', False):
                        l.append(f.name)
                for f in meta.many_to_many:
                    l.append(f.name)
                for f in meta.virtual_fields:
                    l.append(f.name)
                for a in model.get_default_table().get_actions():
                    l.append(a.action.action_name)
                l.sort()
            return l

        #~ def get_field_display(cls,fld):
            #~ return fld

        @dd.virtualfield(models.CharField(_("Verbose name"), max_length=200))
        def verbose_name(self, request):
            m = self.content_type.model_class()
            de = m.get_default_table().get_data_elem(self.field)
            if isinstance(de, models.Field):
                return "%s (%s)" % (unicode(de.verbose_name),
                                    unicode(_("database field")))
            if isinstance(de, dd.VirtualField):
                return unicode(de.return_type.verbose_name)
            if isinstance(de, actions.Action):
                return unicode(de.label)
            return str(de)

    class HelpTexts(dd.Table):
        required = dd.required(user_level='manager')
        model = HelpText
        column_names = "field verbose_name help_text id content_type"

    class HelpTextsByModel(HelpTexts):
        master_key = 'content_type'


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


SYSTEM_USER_LABEL = _("System")
OFFICE_MODULE_LABEL = _("Office")


def setup_main_menu(site, ui, profile, m):
    #~ office = m.add_menu("office",OFFICE_MODULE_LABEL)
    #~ office.add_action(MyTextFieldTemplates)
    pass


def setup_config_menu(site, ui, profile, m):
    office = m.add_menu("office", OFFICE_MODULE_LABEL)
    system = m.add_menu("system", SYSTEM_USER_LABEL)
    #~ m.add_action('links.LinkTypes')
    system.add_instance_action(site.site_config)
    if site.user_model and profile.authenticated:
        system.add_action(site.user_model)
        # system.add_action(site.modules.users.Teams)
        office.add_action(MyTextFieldTemplates)
    #~ m.add_action(site.modules.users.Users)
    if site.is_installed('contenttypes'):
        system.add_action(site.modules.system.ContentTypes)
        system.add_action(site.modules.system.HelpTexts)
        #~ m.add_action(site.modules.lino.Workflows)


def setup_explorer_menu(site, ui, profile, m):
    office = m.add_menu("office", OFFICE_MODULE_LABEL)
    system = m.add_menu("system", SYSTEM_USER_LABEL)
    if site.user_model:
        system.add_action(site.modules.users.Authorities)
        system.add_action(dd.UserGroups)
        system.add_action(dd.UserLevels)
        system.add_action(dd.UserProfiles)
        office.add_action(TextFieldTemplates)


dd.add_user_group('office', OFFICE_MODULE_LABEL)


if settings.SITE.user_model == 'auth.User':
    dd.inject_field(settings.SITE.user_model,
                    'profile', dd.UserProfiles.field())
    dd.inject_field(settings.SITE.user_model, 'language', dd.LanguageField())


@dd.receiver(dd.pre_ui_build)
def my_pre_ui_build(sender, **kw):
    self = settings.SITE
    if self.is_installed('contenttypes'):

        from django.db.utils import DatabaseError
        from django.db.models import FieldDoesNotExist
        try:

            HelpText = dd.resolve_model('system.HelpText')
            for ht in HelpText.objects.filter(help_text__isnull=False):
                #~ logger.info("20120629 %s.help_text", ht)
                try:
                    resolve_field(unicode(ht)).help_text = ht.help_text
                except FieldDoesNotExist as e:
                    #~ logger.debug("No help texts : %s",e)
                    pass
        except DatabaseError, e:
            logger.debug("No help texts : %s", e)
            pass
