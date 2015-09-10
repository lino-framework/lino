===========================
Building the Lino docs tree
===========================

When you have installed a developer's version of Lino (as explained in
:ref:`lino.dev.install`), then you should be able to build the Lino
documentation by running :cmd:`fab bd` in the root of your Lino
repository::

  $ cd ~/repositories
  $ fab bd

This uses Sphinx to read the `.rst` source files and to generate
:file:`.html` files into the :file:`docs/.build` directory.

You can then start your favourite browser on the generated files::

  $ firefox docs/.build/html/index.html

You change the :file:`.rst` files, rebuild your docs tree, and (when
you are satisfied) :doc:`pull_request`.
