============
Python dumps
============

A *database dump* is an image of the data in a database which you can
use e.g. to backup and restore your data.  While Django's
:manage:`dumpdata` command lets you make database dumps in *json* and
*xml* format, Lino extends this by letting you make a database dump in
*Python* format. This is what we call a **Python dump**.

While theoretically you might use :manage:`dumpdata` with ``--format
py`` option, this would generate a huge Python module.  And in
practice, huge Python module have several disadvantages, so you will
use the :manage:`dump2py` command.  A database dump created by
:manage:`dump2py` is a directory of Python modules with one main
module :xfile:`restore.py`.

Another important thing is that you can use such a backup for data
migrations (but that's for another chapter).

