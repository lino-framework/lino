"""Defines the Dedupable mixin used on `contacts.Partner` to assist
users in finding duplicate database records.


Overrides the :attr:`submit_insert
<lino.core.model.Model.submit_insert>` action of
:class:`lino.modlib.contacts.contacts.Partner` with
:class:`CheckedSubmitInsert`, a customized variant of the standard
:class:`SubmitInsert <lino.core.actions.SubmitInsert>` that checks for
duplicate partners and asks a user confirmation when necessary.

Also defines a virtual table :class:`SimilarPartners`, which does that
same check on existing partners and shows a slave table of partners that
are "similar" to a given master instance (and therefore are potential
duplicates).

Examples and test cases in :ref:`welfare.tested.dedupe`.

The current implementation of the detection algorithm uses the `fuzzy
<https://pypi.python.org/pypi/Fuzzy>`_ module.

Doug Hellmann about `Using Fuzzy Matching to Search by Sound with
Python <http://www.informit.com/articles/article.aspx?p=1848528>`_



.. autosummary::
   :toctree:

    mixins
    models

"""
