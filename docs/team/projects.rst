=======================================
Project management using :mod:`atelier`
=======================================

(not finished)

This section introduces our minimalistic project management system
based on :mod:`atelier`.


- You have a directory :file:`~/repositories` with subdirectories
  :file:`lino` and maybe :file:`atelier`, :file:`welfare`, :file:`cosi`.

  This is your collection of repositories of projects for which you
  are not the author, but you cloned a copy of the development
  repository, as explained in :ref:`lino.dev.install`,
  :ref:`cosi.install`, :ref:`welfare.install`, :ref:`faggio.install`.

- Move :file:`~/myblog` to :file:`~/projects/dblog`.

- For every new project, you will create a subdirectory of
  :file:`~/projects/`.  The name of that subdirectory is your
  *internal project name*.

- Here are some useful functions for your  :xfile:`~/.bash_aliases`::

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

    alias ci='fab ci'
    alias runserver='python manage.py runserver'
    alias pp='per_project'
    alias x='exit'

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

