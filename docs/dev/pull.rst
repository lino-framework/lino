How to update your copy of the repositories
-------------------------------------------

Since Lino is in constant development, you will probably often do the
following::

  $ cd ~/repositories
  $ cd lino ; git pull ; cd ..

This means that you update your copy ("clone") of the Lino repository.

Note that you **don't need** to re-run ``pip install`` on these
updated repositories since you used the ``-e`` command line option of
``pip install`` (as instructed in :ref:`lino.dev.install`).

Because Lino is based on several other projects maintained by the same
author, it is recommended to always update all these projects at the
same time::

  $ cd ~/repositories
  $ cd atelier ; git pull ; cd ..
  $ cd site ; git pull  ; cd ..
  $ cd north ; git pull ; cd ..
  $ cd lino ; git pull ; cd ..

And (depending on which of the :ref:`lino.projects` you use) maybe one
or several of the following::

  $ cd cosi ; git pull ; cd ..
  $ cd welfare ; git pull ; cd ..
  $ cd voga ; git pull ; cd ..
  $ cd eidreader ; git pull ; cd ..
  $ cd davlink ; git pull ; cd ..
  
To automate this task, you can create a bash script `pull.sh` like the
following::

    for i in atelier site north lino welfare davlink eidreader
    do
        echo $i
        cd repositories/$i
        git pull
        find -name '*.pyc' -exec rm {} +
        cd ..
    done
