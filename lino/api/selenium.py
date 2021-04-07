# -*- coding: UTF-8 -*-
# Copyright 2015-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Defines the :class:`Tour` class and a :func:`runserver` function.

See :doc:`/dev/tours`.

"""

import os
import sys
import time
import subprocess
import traceback
# from multiprocessing import Process
from threading import Thread

# threads in Python can't be stopped or killed, but runserver needs to run
# another process in background and needs to kill it when the job is done.

from pathlib import Path
import shutil
import rstgen
import requests
from atelier.utils import unindent
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
# from django.core.management import execute_from_command_line

django_admin = shutil.which('django-admin')
runserver_cmd = [django_admin, 'runserver', '--noreload']


def runserver(func, url="http://127.0.0.1:8000/", *args, **kwargs):
    """
    Run a Django development server in background and wait until it responds to
    web requests.
    """

    server_process = None
    proc_name = "runserver " + settings.SETTINGS_MODULE

    try:
        print("Starting server {} in background...".format(proc_name))
        server_process = subprocess.Popen(runserver_cmd, shell=False, universal_newlines=True)
        Thread(target=server_process.communicate, name=proc_name).start()
        print("Waiting for server {} to respond".format(proc_name))
        while True:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    # print(response.text)
                    break
            except Exception as e:
                print(f"... not yet ready ({e})")
                time.sleep(1)

        print("OK, here we go...")
        func(*args, **kwargs)

    finally:

        if server_process is not None:
            print("Terminating server {}".format(proc_name))
            server_process.terminate()

IMAGE_DIRECTIVE = """

.. image:: {imgname}
    :alt: {caption}
    :width: {width}

"""

INTRO_TEMPLATE = """

A series of screenshots taken from the
:mod:`{settings_module}` demo project.

.. include:: /../docs/shared/include/defs.rst

"""

class Tour(object):
    """
    Generates a directory of screenshots images and their `index.rst`
    file.
    """
    screenshot_root = None
    screenshot_suffix = ".png"
    screenshots = []

    """A list of tuples `(name, desc)`, where `desc` is another
    tuple `(imgname, caption, before, after)`.
    """

    title = None
    intro = None
    ref = None
    error_message = None
    language = None
    languages = []
    server_url = "http://127.0.0.1:8000/"
    images_width = 90

    def __init__(self, main_func, output_path=None, title="Screenshots",
                 ref=None, intro=None):
        self.main_func = main_func

        if not isinstance(output_path, Path):
            raise Exception("output_path must be a pathlib.Path instance")

        if intro is None:
            intro = INTRO_TEMPLATE.format(
                settings_module=settings.SETTINGS_MODULE)

        self.screenshot_root = output_path
        self.screenshots = []
        self.title = title
        self.intro = intro
        self.ref = ref

    def set_language(self, language):
        self.language = language
        if language not in self.languages:
            self.languages.append(language)

    def checktitle(self, title):
        if self.driver.title != title:
            print("Title is {0} (expected: {1})".format(
                self.driver.title, title))
            sys.exit(-1)

    def error(self, msg):
        raise Exception(msg)
        # print(msg)
        # sys.exit(-1)

    def find_clickable(self, text):
        try:
            return self.driver.find_element(By.XPATH, '//button[text()="{}"]'.format(text))
        except NoSuchElementException:
            return self.driver.find_element(By.LINK_TEXT, text)

    def is_stale(self, elem):
        try:
            self.hover(elem)
            return False
        except StaleElementReferenceException:
            return True

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
                (By.CLASS_NAME, "ext-el-mask-msg")))
                # (By.CLASS_NAME, "ext-el-mask-msg x-mask-loading")))
                # (By.CLASS_NAME, "x-mask-loading")))
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, ".x-mask-loading")))
        # WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located(
        #         (By.ID, "body")))
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, "dashboard")))
        # time.sleep(1)

    def name2path(self, name):
        if self.language is None:
            return Path(name + self.screenshot_suffix)
        return Path(name + "_" + self.language + self.screenshot_suffix)

    def screenshot(self, name, caption, before='', after=''):
        self.stabilize()
        imgname = self.name2path(name)
        pth = self.screenshot_root / imgname
        pth.parent.mkdir(exist_ok=True)
        if not self.driver.get_screenshot_as_file(str(pth)):
            raise Exception("Failed to write {0}".format(pth))
            # sys.exit(-1)
        print("Wrote screenshot {0} ...".format(pth))
        before = unindent(before)
        after = unindent(after)
        screenshot = None
        for ss in self.screenshots:
            if ss[0] == name:
                screenshot = ss
                break
        if screenshot is None:
            screenshot = (name, [], caption, before, after)
            self.screenshots.append(screenshot)
        screenshot[1].append(imgname)

    def write_index(self):
        index = self.screenshot_root / 'index.rst'
        if len(self.screenshots) == 0:
            print("No file {} because there are no screenshots.".format(index))
            return
        if self.ref:
            content = ".. _{0}:\n\n".format(self.ref)
        else:
            content = ""
        content += rstgen.header(1, self.title)
        content += "\n\n\n"
        if self.intro:
            content += unindent(self.intro)
            content += "\n\n\n"

        for name, imgnames, caption, before, after in self.screenshots:
            content += "\n\n"
            content += rstgen.header(2, caption)
            content += "\n\n"+ before + "\n\n"
            # imgname = filename.name
            width = "{}%".format(self.images_width / len(imgnames))
            for imgname in imgnames:
                content += IMAGE_DIRECTIVE.format(**locals())
            content += "\n\n"+ after + "\n\n"

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

        index.write_text(content)

    def run_from_server(self, *args, **kwargs):
        self.driver.get(self.server_url)
        self.checktitle(settings.SITE.title)
        try:
            self.main_func(self)
        except Exception as e:
            print(e)
            self.error_message = traceback.format_exc()
            traceback.print_exc()

    def make(self, driver=None, headless=True, *args, **kwargs):
        """
        Make the tour. Open a selenium driver, start the development server in
        background, run the :attr:`main_func`, write the :file:`index.rst` files.
        """

        if driver is None:
            op = webdriver.FirefoxOptions();
            op.headless = headless
            driver = webdriver.Firefox(options=op)
            # driver.set_page_load_timeout(10)

        self.driver = driver
        self.actionChains = ActionChains(driver)

        try:
            runserver(self.run_from_server, url=self.server_url, *args, **kwargs)
        finally:
            print("Terminating browser driver", driver)
            driver.quit()

        self.write_index()
