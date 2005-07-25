## Copyright 2004-2005 Luc Saffre.
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
import webbrowser

from lino.console.application import Application, UsageError

class OpenURL(Application):
    name="Lino openurl"
    years='2002-2005'
    author='Luc Saffre'
    usage="Usage: lino openurl URL [URL...]"
    description="""\
Starts the default browser on the specified URL(s).

"""

    
    def run(self,sess):
        if len(self.args) != 1:
            raise UsageError("no arguments specified")
        for url in self.args:
            # webbrowser.open(url,new=1)
            print url
            webbrowser.open_new(url)

consoleApplicationClass = OpenURL

if __name__ == '__main__':
    consoleApplicationClass().main() 

