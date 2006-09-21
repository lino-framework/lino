## Copyright 2004-2006 Luc Saffre.
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

from lino.console.application import Application, UsageError
from lino.tools.mail import readmail, openmail

class OpenMail(Application):
    name="Lino/openmail"

    copyright="""\
Copyright (c) 2002-2006 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    url="http://lino.saffre-rumma.ee/openmail.html"
    
    usage="usage: lino openmail FILE"
    description="""\
Start the user's default mail client with a ready-to-send message
whose content is previously read from FILE.

FILE describes the contents of the message using a simplified pseudo
RFC822 format.  Supported message header fields are "to", 
"subject", and the "body".  "to" is mandatory, the other fields are
optional.
"""
    
    def run(self):
        if len(self.args) != 1:
            raise UsageError("exactly 1 argument required")

        msg = readmail(self.args[0])

        self.debug("openmail() : %s",msg)

        openmail(msg)
        

def main(*args,**kw):
    OpenMail().main(*args,**kw)

if __name__ == '__main__': main() 

