# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)

import os

from lino import ad


class Plugin(ad.Plugin):  # was: use_eidreader

    site_js_snippets = ['beid/eidreader.js']
    media_name = 'eidreader'

    data_collector_dir = None
    read_only_simulate = False

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

