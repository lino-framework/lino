========
Excerpts
========

.. module:: ml.excerpts

The :mod:`lino.modlib.attestations` package provides data definitions
for using "database excerpts".


.. class:: Certifiable

Any model which inherits from this mixin becomes "certifiable".

That is:

- it has a `printed_by` field and a corresponding virtual field
  `printed` which point to the excerpt that is the "definitive"
  ("Certifying") printout of this object.

- It may define a list of "certifiable" fields. These files will
  automaticaly become disabled (readonly) when the document is
  "certified".

    @classmethod
    def get_certifiable_fields(cls):
        return ''

Your database is then expected to have a certifying ExcerptType on
this model. 


Usage example::

  from lino.modlib.excerpts.mixins import Certifiable

  class MyModel(dd.UserAuthored, Certifiable, dd.Duplicable):
      ...


.. class:: CreateExcerpt

.. class:: ExcerptType

.. class:: Excerpt


