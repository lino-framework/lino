# -*- coding: UTF-8 -*-
# Copyright 2015-2018 Rumma & Ko Ltd
# License: BSD, see LICENSE for more details.
"""
Used by :xfile:`make_screenshots.py` and :xfile:`maketour.py` scripts.

Defines an :class:`Album` class and a :func:`runserver` function. An
"album" represents a directory with screenshot images and their
`index.rst` file.

Note that one :xfile:`maketour.py` file might generate several albums
during a single `runserver` process, e.g. one for each language.


`Introducing the Selenium-WebDriver API by Example
<http://www.seleniumhq.org/docs/03_webdriver.jsp#introducing-the-selenium-webdriver-api-by-example>`__

`INVOKE_SERVER` does not work at the moment. It seems that
:meth:`driver.get` does not wait if the server is just starting up and
therefore not even yet responding to connection requests. The only
workaround for this is currently to run the webserver process in a
different terminal.
"""

from __future__ import unicode_literals, absolute_import, print_function
import six
import os
import sys
import time
import subprocess
import traceback

from unipath import Path
from atelier import rstgen
from atelier.utils import unindent

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

INVOKE_SERVER = False

def runserver(settings_module, func, driver=None):

    if driver is None:
        driver = webdriver.Firefox() # service_log_path=os.path.devnull)
        # driver = webdriver.Chrome('/usr/bin/chromium-browser')

    if INVOKE_SERVER:
        env = dict()
        if False:
            env.update(LINO_BUILD_CACHE_ON_STARTUP='yes')
        env.update(os.environ)
        args = ['django-admin', 'runserver', '--noreload', '--settings',
                settings_module]
        server = subprocess.Popen(args, stdout=None, stderr=None, env=env)

        # driver.implicitly_wait(10) # seconds
        # time.sleep(10)
        # startup_time = 1
        # print("Sleeping {} seconds while server wakes up...".format(startup_time))
        # time.sleep(startup_time)
    try:
        url = "http://127.0.0.1:8000/"
        # driver.execute(Command.GET, {'url': url})
        driver.get(url)
        func(driver)
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()

    if INVOKE_SERVER:
        server.terminate()
        
    driver.quit()
    

class Album(object):
    """
    Generates one directory of screenshots images and their `index.rst`
    file.
    """
    screenshot_root = None
    screenshots = []
    title = None
    intro = None
    ref = None
    error_message = None
    
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
        if not self.driver.get_screenshot_as_file(filename):
            print("Failed to write {0}".format(filename))
            sys.exit(-1)
        print("Wrote screenshot {0} ...".format(filename))
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

        if self.error_message:
            content += "\n\n"
            if self.ref:
                content += ".. _{0}.oops:\n\n".format(self.ref)
            content += rstgen.header(2, "Not finished")
            content += "\n\n"
            content += "Oops, we had a problem when generating this document::\n"
            isep = '\n    '
            content += isep
            content += isep.join(self.error_message.splitlines())
            content += "\n\n"

        if six.PY2:
            content = content.encode('utf-8')
        index.write_file(content)

    def run(self, func):    
        try:
            func(self)
        except Exception as e:
            print(e)
            self.error_message = traceback.format_exc()
            traceback.print_exc()

        self.write_index()

