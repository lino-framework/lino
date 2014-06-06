How to update your copy of the repositories
-------------------------------------------

Since Lino is in constant development, you will probably often do the
following::

  $ cd ~/repositories
  $ cd lino ; git pull ; cd ..

This means that you update your copy ("clone") of the Lino repository.

In fact, since Lino is based on several other projects maintained by
the same author, it is recommended to always update all these projects
at the same time::

  $ cd ~/repositories
  $ cd atelier ; git pull ; cd ..
  $ cd site ; git pull  ; cd ..
  $ cd north ; git pull ; cd ..
  $ cd lino ; git pull ; cd ..

And (depending on which of the :ref:`lino.projects` you use) maybe one
or several of the following::

  $ cd cosi ; git pull ; cd ..
  $ cd welfare ; git pull ; cd ..
  $ cd faggio ; git pull ; cd ..
  
Note: You don't need to re-run ``pip install`` on these updated
repositories since you used the ``-e`` command line option of ``pip
install`` (as instructed in :ref:`lino.dev.install`).


