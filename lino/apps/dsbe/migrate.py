# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

from lino.tools import resolve_model

def install(globals_dict):
    
    if globals_dict['SOURCE_VERSION'] == '1.1.16':
      
        NATIVES = []
        Person = resolve_model("contacts.Person")
        LanguageKnowledge = resolve_model("dsbe.LanguageKnowledge")


        def create_contacts_person(country_id, city_id, name, addr1, street_prefix, street, street_no, street_box, addr2, zip_code, region, language, email, url, phone, gsm, fax, remarks, first_name, last_name, title, id, is_active, activity_id, bank_account1, bank_account2, remarks2, gesdos_id, is_cpas, is_senior, group_id, coached_from, coached_until, coach1_id, coach2_id, sex, birth_date, birth_date_circa, birth_place, birth_country_id, civil_state, national_id, health_insurance_id, pharmacy_id, nationality_id, card_number, card_valid_from, card_valid_until, card_type, card_issuer, noble_condition, residence_type, in_belgium_since, unemployed_since, needs_residence_permit, needs_work_permit, work_permit_suspended_until, aid_type_id, income_ag, income_wg, income_kg, income_rente, income_misc, is_seeking, unavailable_until, unavailable_why, native_language_id, obstacles, skills, job_agents, job_office_contact_id):
            p = Person(country_id=country_id,city_id=city_id,name=name,addr1=addr1,street_prefix=street_prefix,street=street,street_no=street_no,street_box=street_box,addr2=addr2,zip_code=zip_code,region=region,language=language,email=email,url=url,phone=phone,gsm=gsm,fax=fax,remarks=remarks,first_name=first_name,last_name=last_name,title=title,id=id,is_active=is_active,activity_id=activity_id,bank_account1=bank_account1,bank_account2=bank_account2,remarks2=remarks2,gesdos_id=gesdos_id,is_cpas=is_cpas,is_senior=is_senior,group_id=group_id,coached_from=coached_from,coached_until=coached_until,coach1_id=coach1_id,coach2_id=coach2_id,sex=sex,birth_date=birth_date,birth_date_circa=birth_date_circa,birth_place=birth_place,birth_country_id=birth_country_id,civil_state=civil_state,national_id=national_id,health_insurance_id=health_insurance_id,pharmacy_id=pharmacy_id,nationality_id=nationality_id,card_number=card_number,card_valid_from=card_valid_from,card_valid_until=card_valid_until,card_type=card_type,card_issuer=card_issuer,noble_condition=noble_condition,residence_type=residence_type,in_belgium_since=in_belgium_since,unemployed_since=unemployed_since,needs_residence_permit=needs_residence_permit,needs_work_permit=needs_work_permit,work_permit_suspended_until=work_permit_suspended_until,aid_type_id=aid_type_id,income_ag=income_ag,income_wg=income_wg,income_kg=income_kg,income_rente=income_rente,income_misc=income_misc,is_seeking=is_seeking,unavailable_until=unavailable_until,unavailable_why=unavailable_why,obstacles=obstacles,skills=skills,job_agents=job_agents,job_office_contact_id=job_office_contact_id)
            if native_language_id:
                NATIVES.append((native_language_id,p))
            return p

        def after_load():
            for native_language_id,p in NATIVES:
                try:
                    lk = p.languageknowledge_set.get(language__id=native_language_id)
                except LanguageKnowledge.DoesNotExist:
                    lk = p.languageknowledge_set.create(language_id=native_language_id,native=True)
                else:
                    lk.native = True
                lk.save()
      
        globals_dict.update(create_contacts_person=create_contacts_person)
        globals_dict.update(after_load=after_load)
        globals_dict['SOURCE_VERSION'] == '1.1.17'
        