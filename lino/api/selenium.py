# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre.
# License: BSD, see LICENSE for more details.
"""Used by :xfile:`make_screenshots.py` scripts.
"""

from __future__ import unicode_literals
import sys
from unipath import Path
from atelier import rstgen
from atelier.utils import unindent

            
class Application(object):
    def __init__(self, driver, root, title="Screenshots"):
        self.driver = driver
        self.screenshot_root = Path(root)
        self.screenshots = []
        self.title = title

    def checktitle(self, title):
        if self.driver.title != title:
            print "Title is {0} (expected: {1})".format(
                self.driver.title, title)
            sys.exit(-1)

    def screenshot(self, name, caption, text=''):
        filename = self.screenshot_root.child(name)
        print "Writing screenshot {0} ...".format(filename)
        if not self.driver.get_screenshot_as_file(filename):
            print "Failed to create {0}".format(filename)
            sys.exit(-1)
        text = unindent(text)
        self.screenshots.append((name, caption, text))

    def write_index(self):
        index = self.screenshot_root.child('index.rst')
        content = rstgen.header(1, self.title)
        content += "\n\n\n"
        for name, caption, text in self.screenshots:
            content += "\n\n"
            content += rstgen.header(2, caption)
            content += """

{text}

.. image:: {name}
    :alt: {caption}

""".format(**locals())

        index.write_file(content.encode('utf-8'))

