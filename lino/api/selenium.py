# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre.
# License: BSD, see LICENSE for more details.
"""Used by :xfile:`make_screenshots.py` scripts.
"""

from __future__ import unicode_literals, absolute_import
import sys
import subprocess

from unipath import Path
from atelier import rstgen
from atelier.utils import unindent
from selenium.webdriver.common.action_chains import ActionChains


def runserver(settings_module, func):
    args = ['django-admin', 'runserver', '--noreload', '--settings',
            settings_module]
    server = subprocess.Popen(args, stdout=None, stderr=None)

    # print "Started subprocess {0}".format(server.pid)

    try:
        func()
    finally:
        server.terminate()


class Album(object):
    """Generates one directory of screenshots images and their `index.rst`
    file.

    """
    def __init__(self, driver, root, title="Screenshots",
                 ref=None, intro=None):
        self.screenshot_root = Path(root)
        self.screenshots = []
        self.title = title
        self.intro = intro
        self.ref = ref
        self.driver = driver
        self.actionChains = ActionChains(driver)

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

    def doubleclick(self, elem):
        self.actionChains.double_click(elem).perform()
            
    def write_index(self):
        index = self.screenshot_root.child('index.rst')
        if self.ref:
            content = ".. _{0}:\n\n".format(self.ref)
        else:
            content = ""
        content += rstgen.header(1, self.title)
        content += "\n\n\n"
        if self.intro:
            content += unindent(self.intro)
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

