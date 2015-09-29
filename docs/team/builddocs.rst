===========================
Building the Lino docs tree
===========================

This page explains how to build the Lino documentation tree (i.e. the
pages visible below http://www.lino-framework.org).

You need to install a developer's version of Lino as explained in
:ref:`lino.dev.install`.

The following is not necessary if you use an atelier version from after 2015-09-28:

    Before you can build the Lino docs, you must also configure
    :mod:`atelier` so that it knows about your projects.  That is, you
    must create a file :xfile:`~/.atelier/config.py` with at least one
    line of code::

      add_project('/path/to/your/lino/repository')

    More about this in `Project management using Atelier
    <http://noi.lino-framework.org/team/projects.html>`__.

And then you just run :cmd:`fab bd` in the root of your Lino repository::

  $ cd ~/repositories
  $ fab bd

This uses Sphinx to read the `.rst` source files and to generate
:file:`.html` files into the :file:`docs/.build` directory.

You can then start your favourite browser on the generated files::

  $ firefox docs/.build/html/index.html

Now you can change the :file:`.rst` files (after reading at least
`reStructuredText Primer <http://sphinx-doc.org/rest.html>`_), run
:cmd:`fab bd` again to see whether this is what you wanted, and (when
you are satisfied) :doc:`submit a pull request <pull_request>`.
