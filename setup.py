# setup.py
from distutils.core import setup
import py2exe
import glob

## setup(name="lino",
## 		version='0.6.1',
## 		description="Lino Database Application Framework",
##       author="Luc Saffre",
##       author_email="luc.saffre@gmx.net",
##       url="http://lino.sourceforge.net",
## 		long_description="A collection of command-line tools",
## 		packages=['lino',
##  					 'lino.adamo',
##  					 'lino.agui',
##  					 'lino.examples',
##  					 'lino.quix',
##  					 'lino.sprl',
##  					 'lino.wxgui',
##  					 'lino.misc',
##  					 'lino.sdoc'],
## 		scripts=glob.glob("scripts\\*.py"),
## 		package_dir = {'': 'src'}
## )

from lino import __version__

setup(name="timtools",
		version=__version__,
		description="Lino TIM tools",
      author="Luc Saffre",
      author_email="luc.saffre@gmx.net",
      url="http://lino.sourceforge.net",
		long_description="A collection of command-line tools",
		console=["scripts\\pds2pdf.py",
					"scripts\\prn2pdf.py",
					"scripts\\openmail.py"]
)
