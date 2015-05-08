# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals


from lino.utils.instantiator import Instantiator
from django.utils.translation import ugettext_lazy as _

from lino.api import dd


def objects():
    
    """
    Education levels in Belgium:
      http://www.guide-enseignement.be/infos_pages/diplomes.html

    Certificat d'études de base (CEB)
    Certificat d'enseignement secondaire du deuxième degré (C.E.S.D.D.)
    Certificat d'études de sixième année de l'enseignement secondaire professionnel (C.E.6.P.)
    Certificat de qualification (C.Q.)
    Certificat d'enseignement secondaire supérieur (C.E.S.S.)
    Certificat relatif aux connaissances de gestion de base
    Brevet d’enseignement secondaire complémentaire – section "soins infirmiers(E.P.S.C.)" 
    """

    eduLevel = Instantiator('cv.EducationLevel').build
    yield eduLevel(**dd.babel_values('name',
                                  de="Primär",
                                  fr="Primaire",
                                  en="Primary"))
    yield eduLevel(**dd.babel_values('name',
                                  de="Sekundär",
                                  fr="Secondaire",
                                  en="Secondary"))
    yield eduLevel(**dd.babel_values('name',
                                  de="Hochschule",
                                  fr="Supérieur",
                                  en="Higher"))
    yield eduLevel(**dd.babel_values('name',
                                  de="Bachelor",
                                  fr="Bachelor",
                                  en="Bachelor"))
    yield eduLevel(**dd.babel_values('name',
                                  de="Master",
                                  fr="Master",
                                  en="Master"))

    studyType = Instantiator('cv.StudyType').build
    yield studyType(**dd.babel_values('name',
                                   de=u"Schule",
                                   fr=u"École",
                                   en=u"School",
                                   ))
    yield studyType(**dd.babel_values('name',
                                   de=u"Sonderschule",
                                   fr=u"École spéciale",
                                   en=u"Special school",
                                   ))
    yield studyType(**dd.babel_values('name',
                                   de=u"Ausbildung",
                                   fr=u"Formation",
                                   en=u"Training",
                                   ))
    yield studyType(**dd.babel_values('name',
                                   de=u"Lehre",
                                   fr=u"Apprentissage",
                                   en=u"Apprenticeship",
                                   ))
    yield studyType(**dd.babel_values('name',
                                   de=u"Hochschule",
                                   fr=u"École supérieure",
                                   en=u"Highschool",
                                   ))
    yield studyType(**dd.babel_values('name',
                                   de=u"Universität",
                                   fr=u"Université",
                                   en=u"University",
                                   ))
    yield studyType(**dd.babel_values('name',
                                   de=u"Teilzeitunterricht",
                                   fr=u"Cours à temps partiel",
                                   en=u"Part-time study",
                                   ))
    yield studyType(**dd.babel_values('name',
                                   de=u"Fernkurs",
                                   fr=u"Cours à distance",
                                   en=u"Remote study",
                                   ))

    M = Instantiator('cv.StudyType', is_training=True, is_study=False).build
    yield M(**dd.str2kw('name', _("Prequalifying")))
    yield M(**dd.str2kw('name', _("Qualifying")))
    yield M(**dd.str2kw('name', _("Alpha")))

    M = Instantiator('cv.Duration').build
    yield M(**dd.str2kw('name', _("Unlimited duration")))
    yield M(**dd.str2kw('name', _("Limited duration")))
    yield M(**dd.str2kw('name', _("Clearly defined job")))
    yield M(**dd.str2kw('name', _("Replacement")))
    yield M(**dd.str2kw('name', _("Interim")))

    """
    Contrat de travail à durée indéterminée
    - Arbeidsovereenkomst voor onbepaalde tijd
    Contrat de travail à durée déterminée
    - Arbeidsovereenkomst voor bepaalde tijd
    Contrat pour un travail nettement défini
    - Arbeidsovereenkomst voor een duidelijk omschreven werk
    Contrat de remplacement
    - Vervangingsovereenkomst
    Contrat d’intérim
    Convention de premier emploi
    Contrat de travail à temps partiel
    """

    status = Instantiator('cv.Status').build
    yield status(**dd.str2kw('name', _("Worker")))
    yield status(**dd.str2kw('name', _("Employee")))
    yield status(**dd.str2kw('name', _("Freelancer")))
    yield status(**dd.str2kw('name', _("Voluntary")))
    yield status(**dd.str2kw('name', _("Student")))
    yield status(**dd.str2kw('name', _("Laboratory")))  # fr=Stage,
                                                        # de=Praktikum
    yield status(**dd.str2kw('name', _("Interim")))

    regime = Instantiator('cv.Regime').build
    yield regime(**dd.str2kw('name', _("Full-time")))
    yield regime(**dd.str2kw('name', _("Part-time")))
    yield regime(**dd.str2kw('name', _("Other")))
