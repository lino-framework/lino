# -*- coding: UTF-8 -*-
## Copyright 2008-2011 Luc Saffre
## This file is part of the Lino-DSBE project.
## Lino-DSBE is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino-DSBE is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino-DSBE; if not, see <http://www.gnu.org/licenses/>.


#~ from django.contrib.contenttypes.models import ContentType
from lino.utils.instantiator import Instantiator, i2d
from lino.tools import resolve_model
from django.utils.translation import ugettext_lazy as _


from django.db import models
from lino.utils.babel import babel_values, babelitem

Person = resolve_model('contacts.Person')
Company = resolve_model('contacts.Company')
ExclusionType = resolve_model('dsbe.ExclusionType')

#~ from lino.modlib.properties import models as properties 

def objects():
  
    noteType = Instantiator('notes.NoteType',"name").build
    
    yield noteType(u"Beschluss")
    yield noteType(u"Konvention",remark=u"Einmaliges Dokument in Verbindung mit Arbeitsvertrag")
    #~ yield noteType(u"Externes Dokument",remark=u"Aufenthaltsgenehmigung, Arbeitsgenehmigung, Arbeitsvertrag,...")
    yield noteType(u"Brief oder Einschreiben")
    yield noteType(u"Notiz",remark=u"Kontaktversuch, Gesprächsbericht, Telefonnotiz")
    yield noteType(u"Vorladung",remark=u"Einladung zu einem persönlichen Gespräch")
    yield noteType(u"Übergabeblatt",remark=u"Übergabeblatt vom allgemeinen Sozialdienst") # (--> Datum Eintragung DSBE)
    yield noteType(u"Neuantrag")
    yield noteType(u"Antragsformular")
    yield noteType((u"Auswertungsbogen allgemein"),build_method='rtf',template=u'Auswertungsbogen_allgemein.rtf')
    yield noteType((u"Anwesenheitsbescheinigung"),build_method='rtf',template=u'Anwesenheitsbescheinigung.rtf')
    yield noteType((u"Lebenslauf"),build_method='appyrtf',template=u'cv.odt')
    
    eventType = Instantiator('notes.EventType',"name").build
    
    yield eventType(u"Eröffnungsbericht")
    yield eventType(u"Erstgespräch")
    yield eventType(u"Abschlussbericht")
    
    #~ projectType = Instantiator('projects.ProjectType',"name").build
    #~ yield projectType(u"VSE Ausbildung")
    #~ yield projectType(u"VSE Arbeitssuche")
    #~ yield projectType(u"VSE Integration")
    #~ yield projectType(u"Hausinterne Arbeitsverträge")
    #~ yield projectType(u"Externe Arbeitsverträge")
    #~ yield projectType(u"Kurse und Zusatzausbildungen")
    
    #~ yield projectType(u"Sozialhilfe")
    #~ yield projectType(u"EiEi")
    #~ yield projectType(u"Aufenthaltsgenehmigung")
    
    studyType = Instantiator('dsbe.StudyType').build
    #~ yield studyType(u"Schule")
    #~ yield studyType(u"Sonderschule")
    #~ yield studyType(u"Ausbildung")
    #~ yield studyType(u"Lehre")
    #~ yield studyType(u"Hochschule")
    #~ yield studyType(u"Universität")
    #~ yield studyType(u"Teilzeitunterricht")
    #~ yield studyType(u"Fernkurs")
    yield studyType(**babel_values('name',
          de=u"Schule",
          fr=u"École",
          en=u"School",
          ))
    yield studyType(**babel_values('name',
          de=u"Sonderschule",
          fr=u"École spéciale",
          en=u"Special school",
          ))
    yield studyType(**babel_values('name',
          de=u"Ausbildung",
          fr=u"Formation",
          en=u"Schooling",
          ))
    yield studyType(**babel_values('name',
          de=u"Lehre",
          fr=u"Apprentissage",
          en=u"Apprenticeship",
          ))
    yield studyType(**babel_values('name',
          de=u"Hochschule",
          fr=u"École supérieure",
          en=u"Highschool",
          ))
    yield studyType(**babel_values('name',
          de=u"Universität",
          fr=u"Université",
          en=u"University",
          ))
    yield studyType(**babel_values('name',
          de=u"Teilzeitunterricht",
          fr=u"Cours à temps partiel",
          en=u"Part-time study",
          ))
    yield studyType(**babel_values('name',
          de=u"Fernkurs",
          fr=u"Cours à distance",
          en=u"Remote study",
          ))
    
    

    #~ studyContent = Instantiator('dsbe.StudyContent',"name").build
    #~ yield studyContent(u"Grundschule")
    #~ yield studyContent(u"Mittlere Reife")
    #~ yield studyContent(u"Abitur")
    #~ yield studyContent(u"Schlosser")
    #~ yield studyContent(u"Schreiner")
    #~ yield studyContent(u"Biotechnologie")
    #~ yield studyContent(u"Geschichte")

    #~ license = Instantiator('dsbe.DrivingLicense',"id name").build
    #~ yield license('A',u"Motorrad")
    #~ yield license('B',u"PKW")
    #~ yield license('C',u"LKW")
    #~ yield license('CE',u"LKW über X Tonnen")
    #~ yield license('D',u"Bus")
    
    
    #~ coachingType = Instantiator('dsbe.CoachingType',"name").build
    #~ yield coachingType(u"DSBE")
    #~ yield coachingType(u"Schuldnerberatung")
    #~ yield coachingType(u"Energieberatung")
    #~ yield coachingType(u"allgemeiner Sozialdienst")
    
    
    excltype = Instantiator('dsbe.ExclusionType','name').build
    yield excltype(u"Termin nicht eingehalten")
    yield excltype(u"ONEM-Auflagen nicht erfüllt")
    
    linkType = Instantiator('links.LinkType',"name").build
    yield linkType(u"Private Website")
    yield linkType(u"Firmen-Website")
    yield linkType(u"Facebook-Profil")
    yield linkType(u"Sonstige")
    
    from lino.models import update_site_config
    
    uploadType = Instantiator('uploads.UploadType',"name").build
    yield uploadType(babelitem(de=u"Personalausweis",fr=u"Carte d'identité"))
    p = uploadType(babelitem(de=u"Aufenthaltserlaubnis",fr=u"Permis de séjour"))
    yield p
    update_site_config(residence_permit_upload_type=p)
    p = uploadType(babelitem(de=u"Arbeitserlaubnis",fr=u"Permis de travail"))
    yield p
    update_site_config(work_permit_upload_type = p)
    yield uploadType(babelitem(de=u"Vertrag",fr=u"Contrat"))
    p = uploadType(babelitem(de=u"Führerschein",fr=u"Permis de conduire"))
    yield p
    update_site_config(driving_licence_upload_type = p)
    
    
    
    exam_policy = Instantiator('jobs.ExamPolicy').build
    yield exam_policy(**babel_values('name',en='every month',de='monatlich',fr="mensuel"))
    yield exam_policy(**babel_values('name',en='every 2 months',de='zweimonatlich',fr="bimensuel"))
    yield exam_policy(**babel_values('name',en='every 3 months',de='alle 3 Monate',fr="tous les 3 mois"))
    yield exam_policy(**babel_values('name',en='other',de='andere',fr="autre"))
        
    #~ def create_dsbe_aidtype(id,name,name_fr):
        #~ return AidType(id=id,name=name,name_fr=name_fr)        
    
    aidtype = Instantiator('dsbe.AidType').build
    yield aidtype(**babel_values('name',
      de=u'Eingliederungseinkommen Kat 1 (Zusammenlebend)',
      fr=u"Revenu d'intégration cat. 1 (couple)",
      ))
    yield aidtype(**babel_values('name',
      de=u'Eingliederungseinkommen Kat 2 (Alleinlebend)',
      fr=u"Revenu d'intégration cat. 2 (célibataire)",
      ))
    yield aidtype(**babel_values('name',
      de=u'Eingliederungseinkommen Kat 3 (Familie zu Lasten)',
      fr=u"Revenu d'intégration cat. 3 (famille à charge)",
      ))
    yield aidtype(**babel_values('name',
      de=u'Ausl\xe4nderbeihilfe Kat 1 (Zusammenlebend)',
      fr=u"Aide aux immigrants cat. 1 (couple)",
      ))
    yield aidtype(**babel_values('name',
      de=u'Ausl\xe4nderbeihilfe Kat 2 (Alleinlebend)',
      fr=u"Aide aux immigrants cat. 2 (célibataire)",
      ))
    yield aidtype(**babel_values('name',
      de=u'Ausl\xe4nderbeihilfe Kat 3 (Familie zu Lasten)',
      fr=u"Aide aux immigrants cat. 3 (famille à charge)",
      ))
    yield aidtype(**babel_values('name',
      de=u'Sonstige Sozialhilfe',
      fr=u"Autre aide sociale",
      ))
    
    if False:
        M = resolve_model('dsbe.FooListing')
        yield M(title='FooListing')