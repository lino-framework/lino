============
Model mixins
============

.. currentmodule:: dd


.. class:: Born

    Abstract base class that adds a `birth_date`
    field and a virtual field "Age".

  .. attribute:: birth_date


  .. attribute:: age

    Virtual field, displays the age in years.

  .. method:: get_age(self, ar, today=None)

    Return the age as a :class:`datetime.timedelta` object.

    `ar` is the requesting :class:`ActionRequest` which can be `None`
    because it is ignored.
    
    Optional keyword argument `today` should be a
    :class:`datetime.date` instance to replace the actual current
    date. This is used if you want the age at a given date in the past
    or the future.
    The default value calls :meth:`dd.Site.today`.



.. class:: Human

  Base class for all models that represent a human.  It defines the
  fields `first_name`, `middle_name, `last_name` and `gender`.

  .. attribute:: first_name

    The first name, also known as given name.

  .. attribute:: last_name

    The last name, also known as family name.

  .. attribute:: middle_name

    A space-separated list of all `middle names
    <http://en.wikipedia.org/wiki/Middle_name>`_.

  .. attribute:: gender

    The gender of this person. 
    Possible values are defined in :class:`dd.Genders`.


  .. method:: mf(self, m, f, u=None)

    Taking three parameters `m`, `f` and `u` of any type, returns one
    of them depending on whether this Person is male, female or of
    unknown gender.

    See :ref:`lino.tutorial.human` for some examples.


  .. method:: get_full_name(self, salutation=True,
                            upper=None, **salutation_options)

    Returns a one-line string composed of salutation,
    :attr:`first_name` and :attr:`last_name`.

    The optional keyword argument `salutation` can be set to
    `False` to suppress salutations.

    The optional keyword argument `upper` can be specified to
    override the Site's default value
    (:setting:`uppercase_last_name`). `True` means to convert the
    last name to uppercase as is usually done in French.

    Any other keyword arguments are forwarded to
    :func:`lino.mixins.human.get_salutation` (see there).

    See :ref:`lino.tutorial.human` for some examples.

