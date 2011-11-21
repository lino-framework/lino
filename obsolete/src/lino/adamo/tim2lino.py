## Copyright 2003-2005 Luc Saffre

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


from lino.misc.memo import MemoParser

class TimMemoParser(MemoParser):
    def __init__(self,db):
        self._db = db
        cmds = {
            'url' : self.cmd_url,
            'ref' : self.cmd_ref,
            'xe' : self.cmd_ref,
            'logo' : self.cmd_logo,
            'btn' : self.cmd_btn,
            'img' : self.cmd_pic,
            'pic' : self.cmd_pic,
            }
        
        MemoParser.__init__(self,cmds)

    
    def cmd_url(self,renderer,s):
        s = s.split(None,1)
        renderer.renderLink(*s)
    ##  if len(s) == 2:
    ##      return renderLink(s[0],label=s[1])
    ##  else:
    ##      return renderLink(s[0])

    def cmd_btn(self,renderer,s):
        s = s.split(None,1)
        renderer.renderImage('buttons',*s)

    def cmd_logo(self,renderer,s):
        s = s.split(None,1)
        renderer.renderImage('logos',*s)

    def cmd_pic(self,renderer,s):
        a = s.split(None,1)
        renderer.renderPicture(*a)

    def cmd_ref(self,renderer,s):
        s = s.split(None,1)
        ref = s[0].split(':')
        if len(ref) != 2:
            raise "invalid ref %s" % repr(s)
            #renderer.write(
            #return
        if ref[0] == "MSX":
            ref[0] = "PAGES"
        elif ref[0] == "TPC":
            ref[0] = "TOPICS"
        elif ref[0] == "AUT":
            ref[0] = "AUTHORS"
        elif ref[0] == "NEW":
            ref[0] = "NEWS"
        elif ref[0] == "PUB":
            ref[0] = "PUBLICATIONS"
        #try:
        ds = self._db.getDatasource(ref[0])
        #except AttributeError,e:
            
            #return str(e)
        s[0] = renderer.uriToTable(ds._table)+"/"+ref[1]
        renderer.renderLink(*s)


    
