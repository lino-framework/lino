# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""Sets the `html_logo` and `html_favicon` for all Lino-related sites.

Using this extension currently means that you cannot set these config
settings yourself.

Also adds some css styling.

"""

from pathlib import Path


def builder_inited(app):
    """Define certain settings
    """
    mydir = (Path(__file__).parent / 'static').absolute()
    app.config.html_static_path.append(str(mydir))
    app.config.html_logo = str(mydir / 'logo_web3.png')
    app.config.html_favicon = str(mydir / 'favicon.ico')


def setup(app):
    app.add_css_file('linodocs.css')
    # app.add_stylesheet('centeredlogo.css')
    app.connect('builder-inited', builder_inited)
