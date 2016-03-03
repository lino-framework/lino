===========================
The languages of a ``Site``
===========================

.. This document is part of the Lino test suite. You can test only
   this document using::

    $ python setup.py test -s tests.DocsTests.test_languages


The :attr:`languages <lino.core.site.Site.languages>` attribute of a
:class:`Site <lino.core.site.Site>` specifies the language
distribution used on this site.

- the user interface languages available on this site
- if your application uses :ref:`mldbc`, the languages for
  multi-lingual database content

Changing this setting affects your database structure if your
application uses :ref:`mldbc`, and thus might require a :ref:`data
migration <datamig>`.

This must be either `None` or an iterable of language codes, or a
string containing a space-separated series of language codes.

Examples::

  languages = "en de fr nl et".split()
  languages = ['en', 'fr']
  languages = 'en fr'

The first language in this list will be the site's default
language.




.. currentmodule:: lino.core.site

>>> from __future__ import print_function
>>> from __future__ import unicode_literals
>>> from django.utils import translation
>>> from lino.core.site import TestSite as Site
>>> from atelier.utils import list_py2


Application code usually specifies :attr:`Site.languages` as a single
string with a space-separated list of language codes.  The
:class:`Site` will analyze this string during instantiation and
convert it into a tuple of :data:`LanguageInfo` objects.

The following examples use the :class:`TestSite` class just to show
certain things which apply also to "real" Sites.

>>> SITE = Site(languages="en fr de")
>>> print(SITE.languages)  #doctest: +NORMALIZE_WHITESPACE
(LanguageInfo(django_code='en', name='en', index=0, suffix=''),
 LanguageInfo(django_code='fr', name='fr', index=1, suffix='_fr'),
 LanguageInfo(django_code='de', name='de', index=2, suffix='_de'))

>>> SITE = Site(languages="de-ch de-be")
>>> print(SITE.languages)  #doctest: +NORMALIZE_WHITESPACE
(LanguageInfo(django_code='de-ch', name='de_CH', index=0, suffix=''), LanguageInfo(django_code='de-be', name='de_BE', index=1, suffix='_de_BE'))

If we have more than one locale of a same language *on a same Site*
(e.g. 'en-us' and 'en-gb') then it is not allowed to specify just
'en'.  But otherwise it is allowed to just say "en", which will mean
"the English variant used on this Site".

>>> site = Site(languages="en-us fr de-be de")
>>> print(site.languages)  #doctest: +NORMALIZE_WHITESPACE
(LanguageInfo(django_code='en-us', name='en_US', index=0, suffix=''),
 LanguageInfo(django_code='fr', name='fr', index=1, suffix='_fr'),
 LanguageInfo(django_code='de-be', name='de_BE', index=2, suffix='_de_BE'),
 LanguageInfo(django_code='de', name='de', index=3, suffix='_de'))

>>> list_py2(list(site.language_dict))
['fr', 'de_BE', 'de', 'en_US', 'en']

>>> site.language_dict['de']
LanguageInfo(django_code='de', name='de', index=3, suffix='_de')

>>> site.language_dict['de_BE']
LanguageInfo(django_code='de-be', name='de_BE', index=2, suffix='_de_BE')

>>> site.language_dict['de'] == site.language_dict['de_BE']
False

>>> site.language_dict['en'] == site.language_dict['en_US']
True

>>> site.language_dict['en']
LanguageInfo(django_code='en-us', name='en_US', index=0, suffix='')
>>> site.language_dict['en']
LanguageInfo(django_code='en-us', name='en_US', index=0, suffix='')

>>> site.language_dict['fr']
LanguageInfo(django_code='fr', name='fr', index=1, suffix='_fr')

>>> print(site.django_settings['LANGUAGES'])  #doctest: +ELLIPSIS
[('de', 'German'), ('fr', 'French')]


