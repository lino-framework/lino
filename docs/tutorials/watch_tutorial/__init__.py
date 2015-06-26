from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Entries")

    def setup_main_menu(self, site, profile, m):
        m = m.add_menu("entries", _("Entries"))
        m.add_action('watch_tutorial.MyEntries')
