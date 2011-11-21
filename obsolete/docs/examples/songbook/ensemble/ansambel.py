#!/usr/local/bin/python
# -*- coding: ISO-8859-1 -*-

## Copyright 2007-2008 Luc Saffre.
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


from lino.songbook import Songbook

sbk=Songbook(
    output_dir=r"C:\temp\laulik",
    input_encoding="latin1",
    numbering=False,
    staffSize=20,
    # versesColumns=2,
    # newLines="~/ ",
    #newLines=r"\nopagebreak\\ \nopagebreak ",
    #newLines=r"\nopagebreak\\",
    newLines=r"\\",
    showTempi=False,
    geometryOptions=dict(a4paper=True,
                         heightrounded=True,
                         #twoside=True,
                         margin="10mm",
                         left="15mm",
                         #right="10mm",
                         #top="10mm",
                         #bottom="10mm",
                         #bindingoffset="5mm",
                         ),
    documentOptions={"12pt":True},
    )

sbk.loadsong("soimes_olgedel")
sbk.loadsong("coventry_carol")
sbk.loadsong("yks_roosike")
sbk.main()

