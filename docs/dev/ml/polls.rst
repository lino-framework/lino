========
Polls
========

.. module:: ml.polls

The :mod:`lino.modlib.polls` package provides data definitions for
managing Polls.

A :class:`Poll` is a collection of :class:`Questions <Question>` which
we want to ask repeatedly to different people. Each Question has a
*question text* and a :class:`ChoiceSet`, i.e. a stored ordered set of
possible choices.  A :class:`Response` is when somebody answers to a
`Poll`.  A Response contains a set of :class:`AnswerChoices
<AnswerChoice>`, each of with represents a given Choice selected by
the questioned person for a given `Question` of the `Poll`.  If the
Question is *multiple choice*, then there may be more than one
`AnswerChoice` per `Question`.  A `Response` also contains a set of
`AnswerRemarks`, each of with represents a remark written by the
responding person for a given Question of the Poll.

See also :ref:`tested.polly`.

.. contents:: 
   :local:
   :depth: 2


.. note:: 

  This is a tested document. You can test it using::

    $ python setup.py test -s tests.DocsTests.test_docs

.. 
  >>> import os
  >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
  ...   'lino.projects.polly.settings'
  >>> from lino.runtime import *


Choicelists
===========

.. class:: PollStates

    The list of possible states of a :class:`Poll`. Default is:

    .. django2rst::

       rt.show(polls.PollStates)


.. class:: ResponseStates

    The list of possible states of a :class:`Poll`. Default is:

    .. django2rst::

       rt.show(polls.ResponseStates)




Models
======

.. class:: ChoiceSet(dd.BabelNamed)

.. class:: Choice

.. class:: Poll

.. class:: Question

.. class:: Response

.. class:: AnswerChoice

.. class:: AnswerRemark

Tables
======

.. class:: AnswersByResponse

    .. attribute:: answer_buttons

    A virtual field that displays the currently selected answer(s) for
    this question, eventually (if editing is permitted) together with
    buttons to modify the selection.
