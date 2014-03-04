# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""Add this to your :setting:`get_installed_apps`
if your Site should feature actions for reading electronic ID
smartcards.

When this app is installed, then you must also add the `.jar` files
required by :ref:`eidreader` into your media directory, in a
subdirectory named "eidreader".

Alternatively there is :mod:`lino.modlib.eid_jslib.beid` which overrides
:mod:`lino.modlib.beid` and does the same except that it uses
:ref:`eid_jslib` instead of :ref:`eidreader`

This app makes sense only if there is exactly one subclass of
:class:`BeIdCardHolder` among your Site's models.

.. setting:: beid.data_collector_dir

Set this to the name of an existing directory to which Lino should
write the raw data received for every card reading.

"""

import logging
logger = logging.getLogger(__name__)

import os

from lino import ad


class Plugin(ad.Plugin):  # was: use_eidreader

    site_js_snippets = ['beid/eidreader.js']
    media_name = 'eidreader'

    data_collector_dir = None

    def get_head_lines(self, site, request):
        if not site.use_java:
            return
        # p = self.build_media_url('EIDReader.jar')
        # p = self.build_media_url('eidreader.jnlp')
        p = self.build_media_url()
        p = request.build_absolute_uri(p)
        yield '<applet name="EIDReader" code="src.eidreader.EIDReader.class"'
        # yield '        archive="%s"' % p
        yield '        codebase="%s">' % p
        # seems that you may not use another size than
        # yield '        width="0" height="0">'
        # ~ yield '<param name="separate_jvm" value="true">' # 20130913
        yield '<param name="permissions" value="all-permissions">'
        # yield '<param name="jnlp_href" value="%s">' % p
        yield '<param name="jnlp_href" value="eidreader.jnlp">'
        yield '</applet>'

    def card_number_to_picture_file(self, card_number):
        #~ TODO: handle configurability of card_number_to_picture_file
        from django.conf import settings
        return os.path.join(settings.MEDIA_ROOT, 'beid',
                            card_number + '.jpg')

