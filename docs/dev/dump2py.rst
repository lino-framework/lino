============
Python dumps
============

A *database dump* is an image of the data in a database which you can
use e.g. to backup and restore your data.  While Django's
:manage:`dumpdata` command lets you make database dumps in *json* and
*xml* format, Lino extends this by letting you make a database dump in
*Python* format. This is what we call a **Python dump**.

Theoretically you might use Django's :manage:`dumpdata` with
``--format py`` option in order to create a Python dump.  For an
average production database however, this would generate a huge Python
module.  And in practice, huge Python module have several
disadvantages. So you will use the :manage:`dump2py` command.  A
database dump created by :manage:`dump2py` is a directory of Python
modules with one main module :xfile:`restore.py`.

Another important thing is that you can use such a backup for data
migrations (but that's for another chapter: :doc:`datamig`).


Manually repairing data
=======================

There are situations where you want to be a magician. For example your
users (or yourself) accidentally deleted a bunch of data from their
database and you don't have a recent backup.

In such situations you can inject data by writing a :manage:`run`
script which uses Python dumps.  Here is an example of such a script::


    from os.path import join
    from django.db.models import Count
    from django.core.exceptions import ValidationError
    
    REALLY = False  # set to True when you are sure

    p = "20150824a"  # the snapshot from where to restore

    # don't execute main(), just load create_aaa_bbb functions
    __name__ = ""
    execfile(join(p, "restore.py"))
    
    class PartnerLoader:

        def __init__(self):
            self.ignored = 0
            self.restored = 0
            self.errors = 0
            self.pklist = (85229, 84047)

        def flush_deferred_objects(self):
            pass

        def save(self, obj):
            if obj.id in self.pklist:
                if obj.__class__.objects.filter(pk=obj.pk).count() == 0:
                    try:
                        obj.full_clean()
                    except ValidationError as e:
                        self.errors += 1
                        logger.info("20150826 %s : %s", obj, e)
                        return

                    if REALLY: obj.save()
                    self.restored += 1
                    return
                else:
                    self.ignored += 1
                    return

        def report(self):
            msg = "Partners: {0} errors, {1} restored, {2} ignored"
            print msg.format(self.errors, self.restored, self.ignored)


    class MyLoader:

        def __init__(self):
            self.ignored = 0
            self.restored = 0
            self.errors = 0
            qs = debts_Budget.objects.annotate(num=Count('entry')).filter(num=0)
            self.pklist = qs.values_list('id', flat=True)
            print "Restore entries for", len(self.pklist), "budgets", [int(i) for i in self.pklist]

        def flush_deferred_objects(self):
            pass

        def save(self, obj):
            if obj.budget_id in self.pklist:
                if obj.__class__.objects.filter(pk=obj.pk).count() == 0:
                    try:
                        obj.full_clean()
                    except ValidationError as e:
                        self.errors += 1
                        print "20150826.py", obj, e
                        return

                    if REALLY: obj.save()
                    self.restored += 1
                    return
                else:
                    self.ignored += 1
                    return

        def report(self):
            msg = "Entries: {0} errors, {1} restored, {2} ignored"
            print msg.format(self.errors, self.restored, self.ignored)

    loader = PartnerLoader()
    execfile(join(p, "contacts_partner.py"))
    #execfile(join(p, "households_household.py"))
    #execfile(join(p, "contacts_company.py"))
    #execfile(join(p, "pcsw_client.py"))
    loader.report()

    loader = MyLoader()
    #execfile(join(p, "debts_actor.py"))
    #loader.report()
    execfile(join(p, "debts_entry.py"))
    loader.report()


