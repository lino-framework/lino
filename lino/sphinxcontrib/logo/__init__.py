# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds some css styling to your logo so that it's widths is set to
100px.


Note: using this extension currently means that you cannot set the
following config settings yourself:

- html_logo, html_favicon, html_theme_options
- autodoc_member_order, autodoc_default_flags

TODO: convert builder_inited function into a configure function to be
called instead of :func:`atelier.sphinxconf.configure`.

"""

from unipath import Path


def builder_inited(app):
    """Define certain settings
    """
    mydir = Path(__file__).parent.child('static').absolute()
    app.config.html_static_path.append(mydir)
    app.config.html_logo = mydir.child('logo_web3.png')
    app.config.html_favicon = mydir.child('favicon.ico')


def setup(app):
    app.add_stylesheet('linodocs.css')
    # app.add_stylesheet('centeredlogo.css')
    app.connect('builder-inited', builder_inited)

