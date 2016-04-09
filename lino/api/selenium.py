# -*- coding: UTF-8 -*-
# Copyright 2015-2016 Luc Saffre.
# License: BSD, see LICENSE for more details.
"""Used by :xfile:`make_screenshots.py` scripts.
"""

from __future__ import unicode_literals, absolute_import, print_function
from builtins import object
import sys
import subprocess

from unipath import Path
from atelier import rstgen
from atelier.utils import unindent

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def runserver(settings_module, func, driver=None):
    args = ['django-admin', 'runserver', '--noreload', '--settings',
            settings_module]
    server = subprocess.Popen(args, stdout=None, stderr=None)

    # print("Started subprocess {0}".format(server.pid))

    if driver is None:
        driver = webdriver.Firefox()

    try:
        driver.get("http://127.0.0.1:8000/")
        func(driver)
    finally:
        driver.quit()
        server.terminate()


class Album(object):
    """Generates one directory of screenshots images and their `index.rst`
    file.

    """
    screenshot_root = None
    screenshots = []
    title = None
    intro = None
    ref = None

    def __init__(self, driver, root=None, title="Screenshots",
                 ref=None, intro=None):
        self.driver = driver
        self.actionChains = ActionChains(driver)

        if root is not None:
            self.screenshot_root = Path(root)
            self.screenshots = []
            self.title = title
            self.intro = intro
            self.ref = ref

    def checktitle(self, title):
        if self.driver.title != title:
            print("Title is {0} (expected: {1})".format(
                self.driver.title, title))
            sys.exit(-1)

    def screenshot(self, name, caption, before='', after=''):
        filename = self.screenshot_root.child(name)
        print("Writing screenshot {0} ...".format(filename))
        if not self.driver.get_screenshot_as_file(filename):
            print("Failed to create {0}".format(filename))
            sys.exit(-1)
        before = unindent(before)
        after = unindent(after)
        self.screenshots.append((name, caption, before, after))

    def error(self, msg):
        raise Exception(msg)
        # print(msg)
        # sys.exit(-1)

    def doubleclick(self, elem):
        self.actionChains.double_click(elem).perform()

    def hover(self, elem):
        self.actionChains.move_to_element(elem).perform()

    def stabilize(self):
        """Wait until the screen has become stable.  This measn that the
        browser has processed all Javascript, including ExtJS.onReady,
        that all AJAX requests have finised.

        This is not trivial to detect, but fortunately we need to
        check it only for Lino screens. Technically we wait until

        - a ``<div id="body">`` element must be present
        - no more loadmask is visible

        """
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(
                # (By.CLASS_NAME, "ext-el-mask-msg x-mask-loading")))
                (By.CSS_SELECTOR, ".x-mask-loading")))
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, "body")))
            
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

        for name, caption, before, after in self.screenshots:
            content += "\n\n"
            content += rstgen.header(2, caption)
            content += """

{before}

.. image:: {name}
    :alt: {caption}
    :width: 500

{after}

""".format(**locals())

        index.write_file(content.encode('utf-8'))

