## Copyright 2005 Luc Saffre

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

raise "replaced by lino.guessenc"

import sys

## selectors = {
##     '\0xe1': ("cp850", "cp1252" ),
##     '\0x84': ("cp850",),
##     '\0x81': ("cp850",),
##     '\0xdf': ("cp1252",),
##     }


class EncodingGuesser:

    def __init__(self,encodings=('cp850','cp1252')):

        self.selectors = {}
        self.encodings = encodings
        
        for encoding in encodings:
            for i in range(127,256):
                ch = chr(i)
                try:
                    uch = ch.decode(encoding)
                except UnicodeError:
                    pass
                else:
                    if uch.isalpha():
                        if self.selectors.has_key(ch):
                            self.selectors[ch].append(encoding)
                        else:
                            self.selectors[ch] = [encoding]


    def guess(self,filename,content=None):
        if content is None:
            content = open(filename).read()
        #candidates = list(self.encodings)
        freqs = {}
        ascii = True
        for ch in content:
            o = ord(ch)
            if o > 127: # contains non-ascii
                ascii = False
                try:
                    candidates = self.selectors[ch]
                except KeyError:
                    print "TODO: no selector for " + repr(ch)
                else:
                    if len(candidates) == 1:
                        #print "found %s => encoding is %s" % (
                        #    repr(ch), candidates[0])
                        return candidates[0]
                    else:
                        pass
                        # todo: use these candidates for elimination in
                        # next non-ascii char ?

        if ascii:
            return None 
        return sys.getdefaultencoding()



## def decode(s):
##     coding = guesscoding(s)
##     print "guessed coding:", coding
##     if coding is None: return s
##     return s.decode(coding)
    
        
## def recode(s,targetcoding,errors="strict"):
##     sourcecoding = guesscoding(s)
##     print "guessed:", sourcecoding
##     if sourcecoding is None: return s
##     s = s.decode(sourcecoding)
##     s = s.encode(targetcoding,errors)
##     return s
##     return s.decode(sourcecoding).encode(targetcoding,errors)
