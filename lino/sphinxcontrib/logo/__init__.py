# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds some css styling to your logo so that it's widths is set to
100px.

"""

from unipath import Path


def builder_inited(app):
    mydir = Path(__file__).parent.child('static').absolute()
    app.config.html_static_path.append(mydir)
    app.config.html_logo = mydir.child('logo.png')
    app.config.html_favicon = mydir.child('favicon.ico')


def setup(app):
    app.add_stylesheet('centeredlogo.css')
    app.connect('builder-inited', builder_inited)

