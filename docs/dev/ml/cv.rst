========
Career
========

.. module:: ml.cv

The :mod:`lino.modlib.cv` plugin is for managing information about the
*career* or *curriculum vitae* of a person.

- A **Language knowledge** is when a given person knows a given language.

- A **Schooling** (fr: Éducation, de: Ausbildung) is when a given person
  has followed lessons in a given *school* for a given *period*.  There
  are two basic types of schooling: **Study** (fr: Études, de: Studium)
  and **Training** (fr: Formation, de: Lehre).

- An **Work experience** (fr: Expérience professionnelle, de:
  Berufserfahrung) is when a given person has worked in a given
  *organisation* for a given *period*.


.. contents:: 
   :local:
   :depth: 2


Models
======

.. class:: EducationLevel
.. class:: EducationLevels

    The demo database has the following education levels:

    .. django2rst::

        rt.show('cv.EducationLevels')


.. class:: TrainingType

.. class:: TrainingTypes

    The demo database has the following training types:

    .. django2rst::

        rt.show('cv.TrainingTypes')



.. class:: StudyType

    Used in :attr:`Contract.study_type` and by :attr:`jobs.Study.type`.

    .. attribute:: education_level

        Pointer to the :class:`EducationLevel`.

    .. attribute:: study_regime

        One choice from :class:`StudyRegimes`.



.. class:: StudyTypes

    The demo database has the following study types:

    .. django2rst::

        rt.show('cv.StudyTypes')




.. class:: LanguageKnowledge

    Specifies how well a certain Person knows a certain Language.

.. class:: PersonHistoryEntry
.. class:: Schooling
.. class:: Study
.. class:: Experience


