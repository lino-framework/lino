======================================
Managing multiple virtual environments
======================================

This document explains how to easily switch Lino versions individually
on a server which hosts several Lino sites.

This document is not finshed, and there is no warranty.

For each Lino version "offered" on your server you create a new
virtualenv. We suggest to create all virtualenvs in a central root
directory named :xfile:`~/pythonenvs`.

Name your environments simply "a", "b", "c" etc. (or find other names
in alphabetical order), *do not* name them "dev", "testing" or "prod".
Because a given environment is normally first used for testing and
then for production.  And virtual environments cannot be renamed.

In the project directory of every Lino site you create a symbolic link
named :file:`env` which points to the root directory of the virtualenv
to be used by that site.

You can then easily switch between environments because Lino, Django
and Apache activates them using the symbolic link :file:`env` in their
project directory.

You can add an alias to your `.bash_aliases`::

  alias a='. env/bin/activate'

In your :xfile:`wsgy.py` file you can add something like::

    import site
    pth = '/my/project/dir/env/lib/python2.7/site-packages'
    site.addsitedir(pth)

We also recommend this line in the :xfile:`settings.py` on a
production site::

  STATIC_ROOT = SITE.project_dir.child('env', 'collectstatic').resolve()

