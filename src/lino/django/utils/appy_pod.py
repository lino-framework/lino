## Copyright 2009 Luc Saffre

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

import os
import time

from appy.pod import PodError
from appy.pod.renderer import Renderer

#docFormat = "odt"
#coOpenOfficePath = r"C:\Program Files\OpenOffice.org 3\program\soffice.exe"
coOpenOfficePath = r"C:\PROGRA~1\OPENOF~1.ORG\program\soffice.exe"

def process_pod(template,context,outfile):
    #template_name = r"c:\temp\sales\invoice.odt"
    params = context
    params['time'] = time
    #resultFile = outfile
    #tmpFolder = os.path.join(os.path.dirname(outfile), 'temp')
    #resultFile = os.path.join(tmpFolder, 'tmp.%s' % docFormat)
    try:
        renderer = Renderer(template, params, outfile, coOpenOfficePath)
        renderer.run()
    except PodError, pe:
        raise pe
    print outfile
        
#~ docFile = open(resultFile, 'rb')
#~ self.session['doc'] = docFile.read()
#~ self.session['docFormat'] = self.docFormat
#~ docFile.close()
#~ os.remove(resultFile)