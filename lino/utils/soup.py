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

from __future__ import unicode_literals
#from builtins import str
import six

from bs4 import BeautifulSoup

def truncate_comment(html_str, max_p_len=None):
    """Return a shortened preview of a html string, containing at most one
    paragraph with at most `max_p_len` characters.

    :param: str: html_str: the raw string of html
            int: max_p_len: max number of characters in the paragraph.


    Usage examples:

    >>> print(truncate_comment('<h1 style="color: #5e9ca0;">Styled comment <span style="color: #2b2301;">pasted from word!</span> </h1>'))
    <h1 style="color: #5e9ca0;">Styled comment <span style="color: #2b2301;">pasted from word!</span> </h1>

    >>> print(truncate_comment('<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>', 30))
    <p>Lorem ipsum dolor sit amet, co...</p>

    >>> print(truncate_comment('<p>Lorem ipsum dolor sit amet</p><p>consectetur adipiscing elit.</p>', 30))
    <p>Lorem ipsum dolor sit amet (...)</p>
    
    >>> print(truncate_comment('<p>A short paragraph</p><p><ul><li>first</li><li>second</li></ul></p>'))
    <p>A short paragraph (...)</p>

    >>> html = u'<p>Ich habe Hirn, ich will hier raus! &ndash; Wie im Netz der Flachsinn regiert.</p>\\n<ul>\\n<li>Ver&ouml;ffentlicht:&nbsp;6. Mai 2017</li>\\n<li>Vorgestellt in:&nbsp;<a href="https://www.linkedin.com/pulse/feed/channel/deutsch"><span>Favoriten der Redaktion</span></a>,&nbsp;<a href="https://www.linkedin.com/pulse/feed/channel/jobs"><span>Job &amp; Karriere</span></a>,&nbsp;<a href="https://www.linkedin.com/pulse/feed/channel/verkauf"><span>Marketing &amp; Verkauf</span></a>,&nbsp;<a href="https://www.linkedin.com/pulse/feed/channel/technologie"><span>Technologie &amp; Internet</span></a>,&nbsp;<a href="https://www.linkedin.com/pulse/feed/channel/wochenendLekture"><span>Wochenend-Lekt&uuml;re</span></a></li>\\n</ul>\\n<ul>\\n<li><span><span>Gef&auml;llt mir</span></span><span>Ich habe Hirn, ich will hier raus! &ndash; Wie im Netz der Flachsinn regiert</span>\\n<p>&nbsp;</p>\\n<a href="https://www.linkedin.com/pulse/ich-habe-hirn-hier-raus-wie-im-netz-der-flachsinn-regiert-dueck"><span>806</span></a></li>\\n<li><span>Kommentar</span>\\n<p>&nbsp;</p>\\n<a href="https://www.linkedin.com/pulse/ich-habe-hirn-hier-raus-wie-im-netz-der-flachsinn-regiert-dueck#comments"><span>42</span></a></li>\\n<li><span>Teilen</span><span>Ich habe Hirn, ich will hier raus! &ndash; Wie im Netz der Flachsinn regiert teilen</span>\\n<p>&nbsp;</p>\\n<span>131</span></li>\\n</ul>\\n<p><a href="https://www.linkedin.com/in/gunterdueck"><span>Gunter Dueck</span></a> <span>Folgen</span><span>Gunter Dueck</span> Philosopher, Writer, Keynote Speaker</p>\\n<p>Das Smartphone vibriert, klingelt oder surrt. Zing! Das ist der Messenger. Eine Melodie von eBay zeigt an, dass eine Auktion in den n&auml;chsten Minuten endet. Freunde schicken Fotos, News versprechen uns "Drei Minuten, nach denen du bestimmt lange weinen musst" oder "Wenn du dieses Bild siehst, wird sich dein Leben auf der Stelle f&uuml;r immer ver&auml;ndern".</p>\\n<p>Politiker betreiben statt ihrer eigentlichen Arbeit nun simples Selbstmarketing und fordern uns auf, mal schnell unser Verhalten zu &auml;ndern &ndash; am besten nat&uuml;rlich "langfristig" und "nachhaltig". Manager fordern harsch immer mehr Extrameilen von uns ein, die alle ihre (!) Probleme beseitigen, und es gibt f&uuml;r jede Schieflage in unserem Leben Rat von allerlei Coaches und Therapeuten, es gibt Heilslehren und Globuli.</p>'
    >>> print(truncate_comment(html))
    <p>Ich habe Hirn, ich will hier raus! – Wie im Netz der Flachsinn regiert. (...)</p>

    """

    soup = BeautifulSoup(html_str, "html.parser")
    ps = soup.find_all("p")
    if len(ps) > 0:
        txt = ps[0].text
        if max_p_len is not None and len(txt) > max_p_len:
            txt = txt[:max_p_len] + "..."
        elif len(ps) > 1:
            txt = txt + " (...)"
        ps[0].string = (txt)
        return six.text_type(ps[0])
    return html_str
