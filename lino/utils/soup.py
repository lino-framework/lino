# -*- coding: UTF-8 -*-
# Adapted copy from lxml\src\lxml\html\builder.py
# --------------------------------------------------------------------
# Modifications in this file are
# Copyright (c) 2017 Luc Saffre
# --------------------------------------------------------------------

# This document is part of the Lino test suite. To test only this
# document, run::
#
#   $ python setup.py test -s tests.UtilsTests.test_soup

"""

"""

from bs4 import BeautifulSoup

def truncate_comment(html_str, max_p_len = 240,):
    """
    :param: str: html_str: a string of html
            int: max_p_len: max length of characters in the comment if there are any pantographs.
    :return: str: a shortened version of the html. Either the first paragraph, a shortened version of the first paragraph,
    several shorter paragraphs where the total length is < max_p_len, or the whole comment if there are not paragraphs.


    Usage examples:

    >>> truncate_comment('<h1 style="color: #5e9ca0;">Styled comment <span style="color: #2b2301;">pasted from word!</span> </h1>')
    '<h1 style="color: #5e9ca0;">Styled comment <span style="color: #2b2301;">pasted from word!</span> </h1>'

    >>> truncate_comment('<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>',30)
    '<p>Lorem ipsum dolor sit amet, co...</p>'

    >>> truncate_comment('<p>Lorem ipsum dolor sit amet</p><p>consectetur adipiscing elit.</p>',30)
    '<p>Lorem ipsum dolor sit amet</p><p>...</p>'
    
    """

    soup = BeautifulSoup(html_str, "html.parser")
    ps = soup.find_all("p")
    if not ps:
        return html_str
    elif len(ps) == 1 or len(ps[0].text) >= max_p_len:
        if len(ps[0].text) > max_p_len:
            ps[0].string= (ps[0].text[:max_p_len] + "...")
        return str(ps[0])
    else:
        tl = 0
        for i, p in enumerate(ps):
            tl += len(p.text)
            if tl > max_p_len: break
        else:
            return "".join([str(p) for p in ps])

        return "".join([str(p) for p in ps[:i]]+ ["<p>...</p>"])
