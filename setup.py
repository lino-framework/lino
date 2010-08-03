from distutils.core import setup, Extension
import lino
setup(name='lino',
      version=lino.__version__,
      description="A web application framework using Django and ExtJS",
      license='GPL',
      packages=['lino'],
      author='Luc Saffre',
      author_email='luc.saffre@gmail.com',
      requires=['django'],
      url="http://lino.saffre-rumma.ee",
      classifiers="""\
Development Status :: 2 - Pre-Alpha
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: GNU General Public License (GPL)
Natural Language :: French
Natural Language :: German
Operating System :: OS Independent
Programming Language :: Python :: 2
Topic :: Database :: Front-Ends
Topic :: Home Automation
Topic :: Office/Business
Topic :: Software Development :: Libraries :: Application Frameworks
""".splitlines()
      )
