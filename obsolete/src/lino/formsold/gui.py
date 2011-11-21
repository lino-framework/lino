## Copyright 2005-2006 Luc Saffre 

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import lino
from lino.console import syscon

_toolkit = None


def choose(wishlist=None):
    if wishlist is None:
        wishlist=lino.config.get('forms','wishlist')
    global _toolkit
    
    assert _toolkit is None, "cannot choose a second time"
    for tkname in wishlist.split():
        print tkname
        if tkname == "tix": 
            from lino.forms.tix.tixform import Toolkit
            _toolkit = Toolkit()
            return _toolkit
        if tkname == "wx": 
            from lino.forms.wx.wxform import Toolkit
            _toolkit = Toolkit()
            return _toolkit
        if tkname == "testkit": 
            from lino.forms.testkit import Toolkit
            _toolkit = Toolkit()
            return _toolkit
        if tkname == "console": 
            from lino.forms.console import Toolkit
            _toolkit = Toolkit()
            return _toolkit
        if tkname == "cherrypy": 
            from lino.forms.cherrygui import Toolkit
            _toolkit = Toolkit()
            return _toolkit
        
        if tkname == "htmlgen":
            from lino.console.htmlgen_toolkit import Toolkit
            #from lino.forms.cherrypy import Toolkit
            _toolkit = Toolkit()
            return _toolkit
    raise "no toolkit found"

def check():
    if _toolkit is None:
        choose()
        #GuiConsole(toolkit=_toolkit)

    
## def form(*args,**kw):
##     check()
##     global _app
##     if _app is None:
##         from lino.forms.application import BaseApplication
##         _app = BaseApplication(toolkit=_toolkit)
##         #from lino.forms.application import AutomagicApplication
##         #_app = AutomagicApplication(toolkit=_toolkit,*args,**kw)
##         #return _app._form
##     return _app.form(None,*args,**kw)
## ##     frm = _app.form(None,*args,**kw)
## ##     _app.mainForm = frm
## ##     return frm

def run(sess):
    check()
    sess.setToolkit(_toolkit)
    #print _toolkit
    #_toolkit.addSession(sess)
    _toolkit.run_forever(sess)
    #_toolkit.main(app)
    
def install():
    check()
    syscon.setToolkit(_toolkit)
    
def runApplication(app):
    check()
    syscon.setToolkit(_toolkit)
    syscon._session.app = app
    _toolkit.run_forever(syscon._session)
    

