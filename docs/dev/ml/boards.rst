======
Boards
======

.. module:: ml.boards

.. class:: Board

  .. attribute:: name



.. class:: Member

  A Member is when a given :class:`ml.contacts.Person`
  belongs to a given :class:`Board`.

  .. attribute:: board

    Pointer to the :class:`Board`.

  .. attribute:: person

    Pointer to the :class:`ml.contacts.Person`.

  .. attribute:: role

    What the person is supposed to do in this board.  Pointer to the
    :class:`ml.contacts.RoleType`.
