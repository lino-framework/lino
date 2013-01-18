=============================
Multilingual database content
=============================

Lino provides facilities to develop application that offer 
support for multilingual database content.

For example, a Canadian company 
might want to print catalogs and price offers in an 
English and a French version, 
but don't want to maintain different product tables. 
So they need a Products table like this:

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

If your application is being used in Canada *and* the US, 
then the US clients don't want to have a useless column for the 
French designation of their products.

See also:

- The :doc:`/tutorials/babel` tutorial
- The :mod:`lino.utils.babel` module
- The :attr:`languages <lino.Lino.languages>` setting
