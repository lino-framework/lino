## Copyright Luc Saffre 2003-2004.

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

import sys
from lino.ui import console

class ParserError(Exception):
    pass

class Status:
    """
    could be used to save/restore the status of the textobject
    """
    def __init__(self,size=10,
                 psfontname="Courier",
                 bold=False,
                 ital=False,
                 leading=14.4):
        self.ital = ital
        self.bold = bold
        self.psfontname = psfontname
        self.size = size
        self.leading = leading
        self.lpi = None
        self.underline = False


        


class Document:
    def __init__(self,pageSize=(0,0),margin=0):
        self.commands = {
            chr(12) : self.formFeed,
            chr(27)+"l" : self.setLpi,
            chr(27)+"c" : self.parse_c,
            chr(27)+"b" : self.parse_b,
            chr(27)+"u" : self.parse_u,
            chr(27)+"i" : self.parse_i,
            chr(27)+"L" : self.setPageLandscape,
            chr(27)+"I" : self.insertImage,
            }
        
        self.pageWidth,self.pageHeight = pageSize
        self.margin = margin # 5 * mm
        self.status = Status()
        #self.oldStatus = None # used by *untilEol cmds
        
        self.page = 0

        self.textobject = None
        
    def createTextObject(self):
        raise NotImplementedError
        
    def onBeginPage(self):
        raise NotImplementedError
    def onEndPage(self):
        raise NotImplementedError
    def onSetPageSize(self):
        raise NotImplementedError
    def write(self,text):
        raise NotImplementedError
    def writeln(self,text):
        raise NotImplementedError
        
    def beginPage(self):
        self.page += 1
        self.onBeginPage()
        assert self.textobject is None
        self.textobject = self.createTextObject()

    def endPage(self):
        if self.textobject is None:
            # formfeed without any preceding text generates blank page
            self.beginPage()
        self.onEndPage()
        self.textobject = None

    def endDoc(self):
        if not self.textobject is None:
            self.endPage()
        self.onEndDoc()
        

    def writechars(self,text):
        if self.textobject is None:
            #if self.page == 2:
            #    print repr(text)
            self.beginPage()

        self.write(text)
        

    def FindFirstCtrl(self,line):
        firstpos = None
        firstctrl = None
        for ctrl in self.commands.keys():
            pos = line.find(ctrl)
            if pos != -1 and (firstpos == None or pos < firstpos):
                firstctrl = ctrl
                firstpos = pos
        return (firstpos,firstctrl)
    

    def readfile(self,inputfile):
        try:
            f = file(inputfile)
            for line in f.readlines():
                #self.printLine(line.rstrip())
                self.printLine(line)
        except IOError,e:
            print e
            sys.exit(-1)


    def printLine(self,line):

        #if not self.oldStatus is None:
        #    self.restoreStatus()
        line = line.rstrip()
        (pos,ctrl) = self.FindFirstCtrl(line)
        while pos != None:
            if pos > 0:
                self.writechars(line[0:pos])

            line = line[pos+len(ctrl):]
            meth = self.commands[ctrl]
            nbytes = meth(line)
            if nbytes > 0:
                line = line[nbytes:]
            #print "len(%s) is %d" % (repr(ctrl),len(ctrl))
            (pos,ctrl) = self.FindFirstCtrl(line)

        if line == "\r\n": return
        #if len(line) == 0: return
        
        self.writechars(line)
        self.writeln()
                
        
        #self.c.drawString(self.xpos, self.ypos, line)
        #self.ypos -= self.linespacing 

##      def saveStatus(self):
##          assert self.oldStatus is None
##          self.oldStatus = self.status
##          self.status = Status(self.status.size,
##                                      self.status.psfontname,
##                                      self.status.bold,
##                                      self.status.ital,
##                                      self.status.leading
##                                      )

##      def restoreStatus(self):
##          self.status = self.oldStatus
##          self.oldStatus = None
##          self.setFont()

        
        
    def setPageLandscape(self,line):
        assert self.textobject is None, \
               'setLandscape after first text has been printed'
        if self.pageHeight > self.pageWidth:
            # only if not already
            self.pageHeight, self.pageWidth = \
                                 (self.pageWidth,self.pageHeight)
            self.onSetPageSize()
        return 0

    def onSetFont(self):
        if self.textobject is None:
            self.beginPage()

    ## methods called if ctrl sequence is found :

    def setLpi(self,line):
        par = line.split(None,1)[0]
        lpi = int(par)
        # if lpi != 6:
        # ignore 6lpi because this is the standard.
        # In a pdf file it's better to use 
        self.status.lpi = lpi
        self.onSetFont()
        return len(par)+1
        
    def parse_c(self,line):
        par = line.split(None,1)[0]
        self.setCpi(int(par))
        return len(par)+1
        
    def setCpi(self,cpi):
        "set font size in cpi (characters per inch)"
        if cpi == 10:
            self.status.size = 12
            self.status.leading = 14
        elif cpi == 12:
            self.status.size = 10
            self.status.leading = 12
        elif cpi == 15:
            self.status.size = 8
            self.status.leading = 10
        elif cpi == 17:
            self.status.size = 7
            self.status.leading = 8
        elif cpi == 20:
            self.status.size = 6
            self.status.leading = 8
        elif cpi == 5:
            self.status.size = 24
            self.status.leading = 28
        else:
            raise "%s : bad cpi size" % par
        self.onSetFont()
         
    def insertImage(self,line):
        raise NotImplementedError

    def parse_i(self,line):
        if line[0] == "0":
            self.setItalic(False)
        elif line[0] == "1":
            self.setItalic(True)
        return 1
            
    def setItalic(self,ital):
        self.status.ital = ital
        self.onSetFont()
    
    def parse_b(self,line):
        if line[0] == "0":
            self.setBold(False)
        elif line[0] == "1":
            self.setBold(True)
        else:
            raise ParserError("0 or 1 expected, but got '%s'" \
                              % line[0])
        return 1
    
    def setBold(self,bold):
        console.debug("setBold(%s)"%str(bold))
        self.status.bold = bold
        self.onSetFont()
    
    def parse_u(self,line):
        if line[0] == "0":
            self.setUnderline(False)
        elif line[0] == "1":
            self.setUnderline(True)
        else:
            raise ParserError("0 or 1 expected, but got '%s'" \
                              % line[0])
        return 1
        
    def setUnderline(self,ul):
        console.debug("setUnderline(%s)"%str(ul))
        self.status.underline = ul
        self.onSetFont()
        
    def formFeed(self,line):
        self.endPage()
        # self.beginPage()
        return 0


## def main(argv,docfactory):

##     try:
##         opts, args = getopt.getopt(argv,
##                                             "h?o:b",
##                                             ["help", "output=","batch"])

##     except getopt.GetoptError:
##         print __doc__
##         sys.exit(-1)

##     if len(args) != 1:
##         print __doc__
##         sys.exit(-1)

##     inputfile = args[0]
##     (root,ext) = os.path.splitext(inputfile)
##     outputfile = root 
##     if len(ext) == 0:
##         inputfile += ".prn"

##     #showOutput=True
##     for o, a in opts:
##         if o in ("-?", "-h", "--help"):
##             print __doc__
##             sys.exit()
##         if o in ("-o", "--output"):
##             outputfile = a
##         if o in ("-b", "--batch"):
##             #showOutput=False
##             getSystemConsole().set(batch=True)
            
##     d = docfactory(outputfile)
##     d.readfile(inputfile)
##     d.endDoc()
    
##     return d
    

        
