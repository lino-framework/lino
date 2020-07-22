# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""This plugins installs two build methods for generating
:doc:`printable documents </admin/printing>` using `weasyprint
<http://weasyprint.org/>`__.

See :doc:`/specs/weasyprint`.

"""

# trying to get rid of disturbing warnings in
# https://travis-ci.org/lino-framework/book/jobs/260560833
import warnings
warnings.filterwarnings(
    "ignore", 'There are known rendering problems')
warnings.filterwarnings(
    "ignore", '@font-face support needs Pango >= 1.38')

try:
    import imagesize
except ImportError:
    imagesize = None

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("WeasyPrint")

    header_height = 20
    """Height of header in mm. Set to `None` if you want no header."""

    footer_height = 20
    """Height of footer in mm. Set to `None` if you want no header."""

    top_right_width = None
    """Width of top-right.jpg in mm. If not given, Lino computes it based on height.
    """

    top_right_image = None
    """The first image file found in config named either top-right.jpg or top-right.png."""

    header_image = None
    """The first image file found in config named either header.jpg or header.png."""

    margin_left = 17
    margin = 10

    def get_requirements(self, site):
        yield "imagesize"

    def on_site_startup(self, site):
        if self.header_height:
            for ext in ('jpg', 'png'):
                fn = site.confdirs.find_config_file("top-right."+ext, "weasyprint")
                if fn:
                    self.top_right_image = fn
                    if self.top_right_width is None:
                        if imagesize is None:
                            site.logger.warning("imagesize is not installed")
                            continue
                        w, h = imagesize.get(fn)
                        self.top_right_width = self.header_height * w / h
                fn = site.confdirs.find_config_file("header."+ext, "weasyprint")
                if fn:
                    self.header_image = fn

        super(Plugin, self).on_site_startup(site)
