# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

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

