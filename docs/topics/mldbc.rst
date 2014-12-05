.. _mldbc:

=============================
Multilingual database content
=============================

Lino includes a facility to develop application that offer support for
multilingual database content.

For example, a Canadian company might want to print catalogs and price
offers in an English and a French version, depending on the customer's
preferred language.  The prices are the same in French and in English,
so they don't want to maintain different product tables.  They need a
Products table like this:

  +--------------+------------------+-------------+-------+----+
  | Designation  | Designation (fr) | Category    | Price | ID |
  +==============+==================+=============+=======+====+
  | Chair        | Chaise           | Accessories | 29.95 | 1  |
  +--------------+------------------+-------------+-------+----+
  | Table        | Table            | Accessories | 89.95 | 2  |
  +--------------+------------------+-------------+-------+----+
  | Monitor      | Écran            | Hardware    | 19.95 | 3  |
  +--------------+------------------+-------------+-------+----+
  | Mouse        | Souris           | Accessories |  2.95 | 4  |
  +--------------+------------------+-------------+-------+----+
  | Keyboard     | Clavier          | Accessories |  4.95 | 5  |
  +--------------+------------------+-------------+-------+----+

Now imagine that your :ref:`application <application>` is being used
both in Canada and the US.  Of course, your US customers don't want to
have a "useless" column for the French designation of their
products. With :ref:`north` you can simply set the :attr:`languages
<ad.Site.languages>` attribute to `["en"]` for US customers and to
`['en', 'fr']` for Canadian customers.

See also:

- The :doc:`/tutorials/catalog/index` tutorial
- The :attr:`languages <ad.Site.languages>` setting
