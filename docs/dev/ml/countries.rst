=============================
Countries (Geographic places)
=============================

.. module:: ml.countries

.. class:: Country

.. class:: Place


.. class:: CountryCity

  .. attribute:: zip_code
  .. attribute:: city

    Pointer to :class:`Place`

  .. method:: full_clean(self)

    Fills my :attr:`zip_code` from my :attr:`city`,

    If my `zip_code` is not empty and differs from that of the city.


.. class:: CountryRegionCity

    Adds a `region` field to a :class:`CountryCity`.

  

