#!/usr/local/bin/python
# -*- coding: ISO-8859-1 -*-

## Copyright 2007 Luc Saffre.
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




# Taizé laulud eesti keeles (Taizé songbook in Estonian)
# http://yaml.org/spec/current.html
# http://pyyaml.org/

from lino.songbook import Songbook


sbk=Songbook(filename="taize-laulik",
             output_dir=r"C:\temp\laulik",
             input_encoding="latin1")

sbk.loadsongs("""
dans_nos
wait_for
lajuda 
bleibet_hier
mane_nobiscum
qui_regarde
il_signore_ti_ristora
exaudi_orationem
""")
sbk.main()

