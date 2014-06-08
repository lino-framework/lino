.. _howto.snapshot:

======================================
How to make a snaptshot of a Lino site
======================================


::

    #!/bin/bash
    set -e
    . env/bin/activate
    if [ -d snapshot ]
      then
        rm -r snapshot
    fi
    python lino/manage.py dump2py snapshot
    if [ -f snapshot.zip ]
      then
        rm snapshot.zip
    fi
    zip -r snapshot.zip snapshot
