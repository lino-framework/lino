=====================================
Installing Lino on a Windows computer
=====================================


.. contents:: Table of Contents
   :local:
   :depth: 2


Software prerequisites
----------------------

You'll need the following software installed on your computer:

- `Django <https://www.djangoproject.com/download/>`_. 
  Follow also the instructions 
  in Django's 
  `Quick install guide <https://docs.djangoproject.com/en/dev/intro/install/>`_
  to install Python.
  
- `Mercurial <http://mercurial.selenic.com/>`_, 
  needed because Lino is in a Mercurial repository 
  and doesn't yet provide downloadable official releases.

To test whether Python and Django are correctly installed, open a 
command prompt and type the following::

  C:\Documents and Settings\Luc> python
  >>> import django
  >>> print django.VERSION
  (1, 4, 0, 'alpha', 0)
  >>>
  
You are now in the Python shell which waits for your next command.
To exit the Python shell, type ::kbd:`Ctrl-Z` and :kbd:`ENTER`.

Some manual work
----------------

ExtJS
=====

You need to manually download and unzip `ExtJS 3 <http://www.sencha.com/products/extjs3/>`_::

    c:\Documents and Settings> md \snapshots
    c:\Documents and Settings> cd \snapshots
    c:\snapshots> wget http://extjs.cachefly.net/ext-3.3.1.zip
    c:\snapshots> unzip ext-3.3.1.zip 
  
If you don't have `wget`, you can simply paste the link to your browser and then select 
:file:`c:\\snapshots` as download location.  
ExtJS 3.3.1 should be enough, but you can download also 3.4 and later switch between 
them if things don't work as expected::

  c:\snapshots> wget http://www.sencha.com/products/extjs3/download/ext-js-3.4.0/203
  c:\snapshots> unzip ext-3.4.0.zip
  
Note that Lino didn't yet migrate to ExtJS 4.0. See :doc:`/tickets/40`

TinyMCE
=======

If you want a WYSYWIG editor for Rich Text fields, 
you'll need also `TinyMCE <http://www.tinymce.com/>`_.
TinyMCE is a platform independent web based Javascript 
HTML WYSIWYG editor control released as Open Source 
under LGPL by Moxiecode Systems AB.

If you do not want a WYSYWIG editor, 
just skip this section, but
you'll need to set
:attr:`lino.Lino.use_tinymce` to `False` in your 
local settings file (see later).

Browse to http://www.tinymce.com/download/download.php
and save the file :file:`tinymce_3.4.7.zip` 
to your directory :file:`c:\\snapshots`, then unzip it::
  
  c:\snapshots> unzip tinymce_3.4.7.zip

You'll maybe also want a language pack from
http://www.tinymce.com/i18n/index.php?ctrl=lang&act=download&pr_id=1

TODO: write detailed installation intructions.

    
Appy
====

You'll probably also want Gaëtan Delannay's :term:`appy_pod` 
so that Lino can generate .pdf, .rtf or .odt documents
when you click on a :guilabel:`Print` button::

  c:\snapshots> wget http://launchpad.net/appy/0.7/0.7.0/+download/appy0.7.0.zip
  c:\snapshots> unzip appy0.7.0.zip -d appy
  
Python dateutils
================

Lino needs Gustavo Niemeyer's python-dateutil module::

  c:\snapshots> wget http://labix.org/download/python-dateutil/python-dateutil-1.5.tar.gz
  c:\snapshots> tar -xvzf python-dateutil-1.5.tar.gz
  
This supposes that you have the ``tar`` command installed.
If you don't, you may get it 
`here <http://gnuwin32.sourceforge.net/packages/gtar.htm>`_.
  
  
Cheetah
=======

Lino needs the Cheetah templating engine, too::

  c:\snapshots> wget http://pypi.python.org/packages/source/C/Cheetah/Cheetah-2.4.4.tar.gz
  c:\snapshots> tar -xvzf Cheetah-2.4.4.tar.gz
  
PyYAML
======

Another library needed by Lino::

  c:\snapshots> wget http://pyyaml.org/download/pyyaml/PyYAML-3.10.zip
  c:\snapshots> unzip PyYAML-3.10.zip

Lino
====

Last but not least we install Lino itself::

  c:\snapshots> hg clone https://lino.googlecode.com/hg/ lino
  
  
 
Set up your Python path
-----------------------

There are several possibilities to do this, but
we suggest to create a 
path configuration file :xfile:`local.pth` 
in the :file:`c:\\Python27\\Lib\\site-packages` directory
(or any other directory that's already on your 
`Python's path <http://www.python.org/doc/current/install/index.html>`_). 
 
The file :xfile:`local.pth` is a simple text file and 
should have the following content::

  c:\snapshots\lino
  c:\snapshots\python-dateutil
  c:\snapshots\appy
  c:\snapshots\Cheetah-2.4.4
  c:\snapshots\PyYAML-3.10\lib
  c:\mypy
  
The directory :file:`c:\\mypy` is the place where you will hold your local Python projects.
You may choose some other location, but we recommend 
a name without spaces and non-ascii characters.

Test whether Lino is installed
------------------------------

::

  c:\mypy> python
  Python 2.7.1 (r271:86832, Nov 27 2010, 18:30:46) [MSC v.1500 32 bit (Intel)] on win32
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import lino
  >>> print lino.welcome_text()
  Lino version 1.3.0 using Python 2.7.1, Django 1.4 pre-alpha SVN-16714, python-dateutil 1.5, Cheetah 2.4.4, docutils 0.7,
   PyYaml 3.08, xhtml2pdf 3.0.32, ReportLab Toolkit 2.4, appy.pod 0.6.7 (2011/06/28 09:13)
   
If things fail: contact me.


Create your local Lino project
------------------------------

To install your first Lino project from scratch, 
create the following 
files in your :file:`c:\\mypy\\mysite`:

#.  The directory must contain an empty file :file:`__init__.py`::

      touch __init__.py
      
    If your don't have a ``touch`` command, do::
    
      notepad __init__.py
      
    This will invoke the Windows notepad editor who will 
    ask you:
    
      | Cannot find  __init__.py file. 
      | Do you want to create a new file?
      
    and you answer "Yes" and exit Notepad. 
    
#.  A file :xfile:`manage.py` with the following content:
    
    .. literalinclude:: manage.py
    
    Our suggestion for an :doc:`optimized </blog/2011/0531>`

#.  And a file :xfile:`settings.py` with the following content:

    .. literalinclude:: settings.py

You will soon learn more about the :xfile:`settings.py` file,
but for the moment we guess that you want to get a quick result.
Just read on.


You want Lino? Which Lino?
--------------------------

Lino is a framework. 
In fact you don't want "just Lino",  
you'll have to decide which Lino application you want.

Soon you will probably 
write your own Lino application
or get somebody else write it for you, 
but in a first step we suggest that you choose one 
of the applications that come out of the box with Lino:

- :mod:`lino.apps.dsbe` 
  (a database for social assistants who assist 
  people in finding jobs or education).

- :mod:`lino.apps.igen` 
  (an accounting application focussed on sales) 
  
In fact you don't even need to choose. 
Just pick a random one.
As long as you are just playing around, 
it is easy to switch between these applications 
since the only difference is the line ``from lino.apps.dsbe.settings import *`` 
in your :xfile:`settings.py`.


Run the test suite
------------------

Try the following command to run Lino's unit test suite on your project::

  cd \mypy\mysite
  python manage.py test
  
Again: if things fail: contact me and send me a screenshot of the messages 
on your console window.
  
Create your database
--------------------

Go to your 
:file:`c:\\mypy\\mysite`
directory and run::

  python manage.py initdb std all_countries few_cities all_languages props demo 
  
Warning: 
The :mod:`initdb <lino.management.commands.initdb>` command 
will create the database specified in your :setting:`DATABASES` 
setting.
If such a database already exists, it will delete all data in 
that database.
We hope that you didn't specify some existing database there, didn't you?
This may sound dangerous, but it is a feature 
which facilitates testing and getting started.


Start a development web server
------------------------------

Open your :xfile:`settings.py` file and add two entries 
:attr:`extjs_root <lino.Lino.extjs_root>`
and
:attr:`extjs_root <lino.Lino.tinymce_root>`::

  class Lino(Lino):

      title = u"My first Lino site"
      csv_params = dict(delimiter=',',encoding='utf-16')
      
      extjs_root = r'c:\snapshots\ext-3.3.1'
      tinymce_root = r'c:\snapshots\tinymce\jscripts\tiny_mce'
      
Lino expects a few subdirectories of your local project directory.
It doesn't create them automatically, so you must do it yourself::

  c:\mypy\mysite> mkdir config
  c:\mypy\mysite> mkdir fixtures
  c:\mypy\mysite> mkdir media
  

Now finally we are ready to go::

  c:\mypy\mysite> python manage.py runserver
  
This should run something like::
  
  Validating models...

  0 errors found
  Django version 1.4 pre-alpha SVN-16376, using settings 'dsbe.settings'
  Development server is running at http://127.0.0.1:8000/
  Quit the server with CTRL-BREAK.
  
  
Then point a browser to http://127.0.0.1:8000/ 
and enjoy your Lino application.
Congratulations.


As the `Django docs 
<https://docs.djangoproject.com/en/dev/intro/tutorial01/#the-development-server>`_  
say: 

  You've started the Django development server, a lightweight Web server written purely in Python. We've included this with Django so you can develop things rapidly, without having to deal with configuring a production server -- such as Apache -- until you're ready for production.

  Now's a good time to note: DON'T use this server in anything resembling a production environment. 
  It's intended only for use while developing


Where to go from here
---------------------

- Now you are ready for our :doc:`/tutorials/index` section.

- You can also read the :doc:`dpytutorial` and play 
  around with some of the fixtures that come with Lino.

