Multilingual sites
==================

This is for sites who need to generate documents in different languages from a single database.

For example if you want to create a catalog in English and French, 
you will need two database fields for the description of your products.

See:

- :setting:`BABEL_LANGS`
- :func:`lino.mixins.printable.getattr_lang`
- :func:`lino.mixins.printable.add_babel_field`




.. setting:: BABEL_LANGS

  a list of additional optional languages to be supported on this site.
  "additional" means "in addition to the default language defined by LANGUAGE_CODE".
  Each database field declared as a "babel field" will have a cloned copy 
  for each "babel language".

    BABEL_LANGS = ['fr']
