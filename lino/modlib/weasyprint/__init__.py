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


from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("WeasyPrint")

