# -*- coding: UTF-8 -*-
# Copyright (c) 2017-2018 Rumma & Ko Ltd

"""See usage examples in :doc:`/specs/comments`.

"""

from __future__ import unicode_literals
#from builtins import str
import six

from bs4 import BeautifulSoup

def truncate_comment(html_str, max_p_len=None):
    """
    Return a shortened preview of a html string, containing at most one
    paragraph with at most `max_p_len` characters.

    :html_str: the raw string of html
    :max_p_len: max number of characters in the paragraph.

    """
    html_str = html_str.strip()  # remove leading or trailing newlines
    if not html_str.startswith('<'):
        # it's plain text without html tags
        ps = html_str.split('\n\n', 1)
        txt = ps[0]
        if max_p_len is not None and len(txt) > max_p_len:
            txt = txt[:max_p_len] + "..."
        elif len(ps) > 1:
            txt = txt + " (...)"
        return txt
    soup = BeautifulSoup(html_str, "html.parser")
    ps = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9"])
    if len(ps) > 0:
        txt = ps[0].text
        if max_p_len is not None and len(txt) > max_p_len:
            txt = txt[:max_p_len] + "..."
        elif len(ps) > 1:
            txt = txt + " (...)"
        return txt
        # ps[0].string = (txt)
        # return six.text_type(ps[0])
    return html_str
