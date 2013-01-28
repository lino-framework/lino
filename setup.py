import os
from setuptools import setup
#~ from distutils.core import setup
#~ from distribute.core import setup

execfile(os.path.join(os.path.dirname(__file__),'lino','version.py'))

#~ kw = {}
#~ execfile(os.path.join(os.path.dirname(__file__),'lino','pypi_info.py'),kw)
#~ del kw['__doc__']
#~ for n in """
#~ name version description 
#~ license packages author author_email 
#~ requires url classifiers
#~ """.split()

#~ print(kw)
    
#~ setup(**kw)

setup(name = 'lino',
  version = __version__,
  description = "A framework for writing desktop-like web applications using Django and ExtJS",
  license = 'GPL',
  packages = ['lino'],
  author = 'Luc Saffre',
  author_email = 'luc.saffre@gmail.com',
  requires = ['django','appy','dateutil','PyYAML','odfpy','sphinx','jinja2'],
  url = "http://www.lino-framework.org",
  test_suite = 'lino.test_apps',
  classifiers="""\
  Programming Language :: Python
  Programming Language :: Python :: 2
  Development Status :: 4 - Beta
  Environment :: Web Environment
  Framework :: Django
  Intended Audience :: Developers
  Intended Audience :: System Administrators
  License :: OSI Approved :: GNU General Public License (GPL)
  Natural Language :: English
  Natural Language :: French
  Natural Language :: German
  Operating System :: OS Independent
  Topic :: Database :: Front-Ends
  Topic :: Home Automation
  Topic :: Office/Business
  Topic :: Software Development :: Libraries :: Application Frameworks
  """.splitlines())
