.. _tested.core_utils:

Lino core utilities
===================

This document tests some functionality of :mod:`lino.core.utils`.

.. How to test only this document:

    $ python setup.py test -s tests.DocsTests.test_core_utils

    doctest init:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino.projects.docs.settings.doctests'
    >>> from lino.api.doctest import *

Get installed models which are subclass of a something
======================================================

The :func:`lino.core.utils.models_by_base` function returns a list of
models which are subclass of a given class.

>>> from lino.mixins.duplicable import Duplicable
>>> rt.models_by_base(Duplicable)
[<class 'lino.modlib.countries.models.Place'>, <class 'lino.modlib.polls.models.Choice'>, <class 'lino.modlib.polls.models.Question'>]

>>> rt.models_by_base(rt.modules.contacts.Partner)
[<class 'lino.modlib.contacts.models.Company'>, <class 'lino.modlib.contacts.models.Partner'>, <class 'lino.modlib.contacts.models.Person'>]

>>> rt.models_by_base(rt.modules.contacts.Person)
[<class 'lino.modlib.contacts.models.Person'>]

.. rubric:: Getting only top-level models

The `toplevel_only` option is used by
:mod:`lino.modlib.plausibility`. For example the
:class:`AddressOwnerChecker
<lino.modlib.addresses.mixins.AddressOwnerChecker>` needs to run only on
Partner, not also on Person, Company and Household...

>>> rt.models_by_base(rt.modules.contacts.Partner, toplevel_only=True)
[<class 'lino.modlib.contacts.models.Partner'>]

>>> rt.models_by_base(rt.modules.contacts.Person, toplevel_only=True)
[<class 'lino.modlib.contacts.models.Person'>]

