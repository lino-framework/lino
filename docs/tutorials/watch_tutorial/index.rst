.. _lino.tutorial.watch:

Watching database changes
-------------------------

.. How to test only this module:

    $ python setup.py test -s tests.DocsTests.test_watch

.. currentmodule:: lino.core.site

This tutorial explains how to implement a kind of `audit trail
<https://en.wikipedia.org/wiki/Audit_trail>`_.  using the
:mod:`lino.modlib.changes` plugin for logging changes to individual
rows of database tables.

To enable database change watching, you add :mod:`lino.modlib.changes`
to your :meth:`Site.get_installed_apps` and then register "change
watchers" for every type of change you want to watch.

You will also want to make your changes visible for users by adding
the
:class:`ChangesByOwner<lino.modlib.changes.models.ChangesByMaster>`
slave table to some detail layout.

The example in this tutorial uses the :mod:`lino.modlib.contacts`
module.  It also adds a model `Entry` as an example of a watched
model.  Imagine some journal entry to be audited.

The "master" of a change watcher is the object to which every change
should be attributed.  In this example the master is *Partner*: every
change to *Entry*, *Partner* **or** *Company* will be logged and
attributed to their *Partner* record.

We define our own subclass of `Site` for this tutorial (which is the
recommended way except for very simple examples).  Here is the
:xfile:`settings.py` file:

.. literalinclude:: settings.py

We need to redefine the default list of user profiles by overriding
:meth:`Site.setup_choicelists` because `contacts` adds a user group
"office", required to see most commands.

Here is our :xfile:`models.py` module which defines the `Entry` model
and some few startup event listeners:

.. literalinclude:: models.py

You can play with this application by cloning the latest development 
version of Lino, then ``cd`` to the :file:`/docs/tutorials/watch_tutorial` 
directory where you can run::

    $ python manage.py initdb_demo
    $ python manage.py runserver

(While you are here and comfortable with this example application, 
you might as well read another tutorial which uses this application 
to explain how to use workflows: :doc:`../workflows_tutorial/index`).

>>> from __future__ import print_function
>>> from lino.api.doctest import *

>>> from django.core.management import call_command
>>> call_command('initdb_demo', interactive=False, verbosity=0)

The :mod:`lino.modlib.changes` plugin records only changes made using
the web interface.  In a virgin database are no changes:

>>> rt.show(changes.Changes)
No data to display


We create a new person

>>> url = '/api/contacts/Companies'
>>> data = dict(an='submit_insert', name='My pub')
>>> res = post_json_dict('robin', url, data)
>>> print(res.message)
Organization "My pub" has been created.


>>> rt.show(changes.Changes, column_names="id type master object diff")
==== ============= ========== ========== =============================================================
 ID   Change Type   Master     Object     Changes
---- ------------- ---------- ---------- -------------------------------------------------------------
 1    Create        *My pub*   *My pub*   Company(id=181,name='My pub',language='en',partner_ptr=181)
==== ============= ========== ========== =============================================================
<BLANKLINE>


>>> url = '/api/contacts/Companies/181'
>>> data = "an=submit_detail&name=Our%20pub"
>>> r = test_client.put(url, data)
>>> r.status_code
200

>>> rt.show(changes.Changes, column_names="id type master object diff")
==== ============= =========== =========== =============================================================
 ID   Change Type   Master      Object      Changes
---- ------------- ----------- ----------- -------------------------------------------------------------
 2    Update        *Our pub*   *Our pub*   name : 'My pub' --> 'Our pub'
 1    Create        *Our pub*   *Our pub*   Company(id=181,name='My pub',language='en',partner_ptr=181)
==== ============= =========== =========== =============================================================
<BLANKLINE>


We add an entry:

>>> url = '/api/watch_tutorial/Entries'
>>> data = dict(an='submit_insert', subject='test', companyHidden=181)
>>> res = post_json_dict('robin', url, data)
>>> print(res.message)
Entry "Entry object" has been created.
>>> rt.show(changes.Changes, column_names="id type master object diff")
==== ============= =========== ================ =============================================================
 ID   Change Type   Master      Object           Changes
---- ------------- ----------- ---------------- -------------------------------------------------------------
 3    Create        *Our pub*   *Entry object*   Entry(id=1,user=1,subject='test',company=181)
 2    Update        *Our pub*   *Our pub*        name : 'My pub' --> 'Our pub'
 1    Create        *Our pub*   *Our pub*        Company(id=181,name='My pub',language='en',partner_ptr=181)
==== ============= =========== ================ =============================================================
<BLANKLINE>

Now we delete the entry:

>>> url = '/api/watch_tutorial/Entries/1'
>>> data = dict(an='delete_selected', sr=1)
>>> r = test_client.get(url, data)
>>> r.status_code
200
>>> res = json.loads(r.content)
>>> print(res['message'])
You are about to delete 1 Entry:
Entry object
Are you sure ?

We answer "yes":

>>> url = "/callbacks/{0}/yes".format(res['xcallback']['id'])
>>> r = test_client.get(url)
>>> r.status_code
200
>>> rt.show(changes.Changes, column_names="id type master object diff")
==== ============= =========== =========== =============================================================
 ID   Change Type   Master      Object      Changes
---- ------------- ----------- ----------- -------------------------------------------------------------
 4    Delete        *Our pub*               Entry(id=1,user=1,subject='test',company=181)
 3    Create        *Our pub*               Entry(id=1,user=1,subject='test',company=181)
 2    Update        *Our pub*   *Our pub*   name : 'My pub' --> 'Our pub'
 1    Create        *Our pub*   *Our pub*   Company(id=181,name='My pub',language='en',partner_ptr=181)
==== ============= =========== =========== =============================================================
<BLANKLINE>

Note how the `object` column of the first two rows in above table is
empty. That's because the entry object has been deleted, so it does no
longer exist in the database and Lino cannot point to it. But not also
that `object` is a "nullable Generic ForeignKey", the underlying
fields `object_id` and `object_type` still contain their values:

>>> rt.show(changes.Changes, column_names="id type master object_type object_id diff")
==== ============= =========== ============== =========== =============================================================
 ID   Change Type   Master      Object type    object id   Changes
---- ------------- ----------- -------------- ----------- -------------------------------------------------------------
 4    Delete        *Our pub*   Entry          1           Entry(id=1,user=1,subject='test',company=181)
 3    Create        *Our pub*   Entry          1           Entry(id=1,user=1,subject='test',company=181)
 2    Update        *Our pub*   Organization   181         name : 'My pub' --> 'Our pub'
 1    Create        *Our pub*   Organization   181         Company(id=181,name='My pub',language='en',partner_ptr=181)
==== ============= =========== ============== =========== =============================================================
<BLANKLINE>


Until 20150626 only the
:attr:`object<lino.modlib.changes.models.Change.object>` was nullable,
not the :attr:`master<lino.modlib.changes.models.Change.master>`.  But
now you can also delete the master, and all change records will still
remain:

>>> url = '/api/contacts/Companies/181'
>>> data = dict(an='delete_selected', sr=181)
>>> r = test_client.get(url, data)
>>> r.status_code
200
>>> res = json.loads(r.content)
>>> url = "/callbacks/{0}/yes".format(res['xcallback']['id'])
>>> r = test_client.get(url)
>>> r.status_code
200
>>> rt.show(changes.Changes, column_names="id type master object diff")
==== ============= ======== ======== ==============================================================
 ID   Change Type   Master   Object   Changes
---- ------------- -------- -------- --------------------------------------------------------------
 5    Delete                          Company(id=181,name='Our pub',language='en',partner_ptr=181)
 4    Delete                          Entry(id=1,user=1,subject='test',company=181)
 3    Create                          Entry(id=1,user=1,subject='test',company=181)
 2    Update                          name : 'My pub' --> 'Our pub'
 1    Create                          Company(id=181,name='My pub',language='en',partner_ptr=181)
==== ============= ======== ======== ==============================================================
<BLANKLINE>


Of course these change records are now considered broken GFKs:


>>> rt.show(gfks.BrokenGFKs)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
================ ================= =============================================================== ========
 Database model   Database object   Message                                                         Action
---------------- ----------------- --------------------------------------------------------------- --------
 *Change*         *#1*              Invalid primary key 181 for contacts.Company in `object_id`     clear
 *Change*         *#2*              Invalid primary key 181 for contacts.Company in `object_id`     clear
 *Change*         *#3*              Invalid primary key 1 for watch_tutorial.Entry in `object_id`   clear
 *Change*         *#4*              Invalid primary key 1 for watch_tutorial.Entry in `object_id`   clear
 *Change*         *#5*              Invalid primary key 181 for contacts.Company in `object_id`     clear
 *Change*         *#1*              Invalid primary key 181 for contacts.Partner in `master_id`     clear
 *Change*         *#2*              Invalid primary key 181 for contacts.Partner in `master_id`     clear
 *Change*         *#3*              Invalid primary key 181 for contacts.Partner in `master_id`     clear
 *Change*         *#4*              Invalid primary key 181 for contacts.Partner in `master_id`     clear
 *Change*         *#5*              Invalid primary key 181 for contacts.Partner in `master_id`     clear
================ ================= =============================================================== ========
<BLANKLINE>

There open questions regarding these change records:

- Do we really never want to remove them? Do we really want a nullable
  master field? Should this option be configurable?
- How to tell :class:`lino.modlib.gfks.models.BrokenGFKs` to
  differentiate them from ?
- Should :meth:`get_broken_generic_related
  <lino.core.kernel.Kernel.get_broken_generic_related>` suggest to
  "clear" nullable GFK fields?

