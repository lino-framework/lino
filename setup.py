# -*- coding: UTF-8 -*-
## Copyright 2009-2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

#~ import os
from distutils.core import setup
#~ from distutils.core import setup, Distribution
import lino

#~ class MyDistribution(Distribution):
    
setup(name='lino',
      #~ distclass=MyDistribution,
      version=lino.__version__,
      description="A web application framework using Django and ExtJS",
      license='GPL',
      packages=['lino'],
      #~ dist_dir=os.path.join('docs','dist'),
      author='Luc Saffre',
      author_email='luc.saffre@gmail.com',
      requires=['django','dateutil'],
      url="http://lino.saffre-rumma.net",
      classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 2
Development Status :: 2 - Pre-Alpha
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: GNU General Public License (GPL)
Natural Language :: French
Natural Language :: German
Operating System :: OS Independent
Topic :: Database :: Front-Ends
Topic :: Home Automation
Topic :: Office/Business
Topic :: Software Development :: Libraries :: Application Frameworks
""".splitlines()
      )
