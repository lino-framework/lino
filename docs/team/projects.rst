=======================================
Project management using :mod:`atelier`
=======================================

(not finished)

This section introduces our minimalistic project management system
based on :mod:`atelier`.

In :mod:`atelier`, a **project** is a directory on your file system
which contains at least a :xfile:`fabfile.py`.  A project usually
corresponds to a public code repository (using Git or Mercurial). But
you can have non-public projects which have no repo at all, e.g. a
developer blog.  A project usually corresponds to a given Python
package published to PyPI.  A project can have a number of Sphinx
document trees.


Internal project name
=====================

You identify a project by its *internal project name*.  We suggest
that you create a function ``go`` in your :xfile:`~/.bash_aliases`
which might look like this::

    function go() { 
        for BASE in ~/projects ~/repositories \
            ~/repositories/lino/lino/projects
        do
          if [ -d $BASE/$1 ] 
          then
            cd $BASE/$1;
            return;
          fi
        done
        echo Oops: no $1 in $BASES
        return -1
    }


Projects don't need to be under a single top-level directory.  You can
have different base directories containing projects.  We suggest the
following naming conventions (you don't need to use these same
conventions, but our examples are based on them).

.. xfile:: ~/repositories

The :file:`~/repositories` directory is your collection of
repositories of projects for which you are not the author, but you
cloned a copy of the development repository, as explained in
:ref:`lino.dev.install`, :ref:`cosi.install`, :ref:`welfare.install`,
:ref:`faggio.install`.

.. xfile:: ~/projects

:file:`~/projects/` might be the base directory for every new project
for which you are the author.

- Move :file:`~/myblog` to :file:`~/projects/blog`.

- Here are some useful functions for your  :xfile:`~/.bash_aliases`::

    alias ci='fab ci'
    alias runserver='python manage.py runserver'
    alias pp='per_project'
    alias x='exit'

    function go() { 
        for BASE in ~/projects ~/repositories \
            ~/repositories/lino/lino/projects
        do
          if [ -d $BASE/$1 ] 
          then
            cd $BASE/$1;
            return;
          fi
        done
        echo Oops: no $1 in $BASES
        return -1
    }

    function pywhich() { 
      python -c "import $1; print $1.__file__"
    }

    function e() { 
      $EDITOR $* 
    }

- Create a :xfile:`~/.atelier/config.py` file which declares all your
  projects. For example with this content::

     add_project("/home/john/projects/myblog")
     add_project("/home/john/projects/hello")
     add_project("/home/john/repositories/lino")

   
- Play with these commands:

  - :cmd:`fab summary` displays a list of all your projects
  - :cmd:`go lino` changes to the main directory of your `lino` project
  - :cmd:`git pull` downloads the latest version of Lino
  - :cmd:`fab initdb test` (i.e. :cmd:`fab initdb` followed by
    :cmd:`fab test`)

  - :cmd:`go myblog` changes to the main directory of your developer blog
  - :cmd:`fab blog` launches your editor on today's blog entry
  - :cmd:`fab bd pd` (i.e. :cmd:`fab bd` followed by :cmd:`fab pd`)

