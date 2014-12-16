.. _lino.tutorial.input_mask:

=========================
Fields with an input mask
=========================


This document describes and tests the
`mask_re` option of a :class:`lino.core.fields.CharField`.

We define a single model:

.. literalinclude:: models.py

This field is here to play with the
CharField parameters regex, mask_re and strip_chars_re.
By default it accepts all letters except Z.
