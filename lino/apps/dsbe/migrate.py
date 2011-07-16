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
from lino.utils import mti


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
        
    if globals_dict['SOURCE_VERSION'] == '1.1.17':
      
        from lino.modlib.jobs.models import Job, Contract, JobProvider, \
          ContractEnding, ExamPolicy, ContractType, Company
        
        
        
        def get_or_create_job(provider_id,contract_type_id):
            try:
                return Job.objects.get(provider__id=provider_id,contract_type__id=contract_type_id)
            except Job.DoesNotExist:
                if provider_id is None:
                    provider = None
                else:
                    try:
                        provider = JobProvider.objects.get(pk=provider_id)
                    except JobProvider.DoesNotExist:
                        company = Company.objects.get(pk=provider_id)
                        provider = mti.insert_child(company,JobProvider)
                        provider.save()
                job = Job(
                    provider=provider,
                    contract_type_id=contract_type_id,
                    name='%s@%s' % (contract_type_id,provider_id)
                    )
                job.save()
                return job
                
        def create_dsbe_contract(id, user_id, reminder_date, reminder_text, 
            delay_value, delay_type, reminder_done, must_build, person_id, 
            company_id, contact_id, language, type_id, applies_from, 
            applies_until, date_decided, date_issued, duration, regime, 
            schedule, hourly_rate, refund_rate, reference_person, 
            responsibilities, stages, goals, duties_asd, duties_dsbe, 
            duties_company, duties_person, user_asd_id, exam_policy_id, 
            ending_id, date_ended):
            job = get_or_create_job(company_id,type_id)
            return Contract(id=id,user_id=user_id,reminder_date=reminder_date,
              reminder_text=reminder_text,delay_value=delay_value,
              delay_type=delay_type,reminder_done=reminder_done,
              must_build=must_build,person_id=person_id,
              job=job,
              provider_id=company_id,
              contact_id=contact_id,language=language,type_id=type_id,
              applies_from=applies_from,applies_until=applies_until,date_decided=date_decided,date_issued=date_issued,duration=duration,regime=regime,schedule=schedule,hourly_rate=hourly_rate,refund_rate=refund_rate,reference_person=reference_person,responsibilities=responsibilities,stages=stages,goals=goals,duties_asd=duties_asd,duties_dsbe=duties_dsbe,duties_company=duties_company,duties_person=duties_person,user_asd_id=user_asd_id,exam_policy_id=exam_policy_id,ending_id=ending_id,date_ended=date_ended)      
              
        CONTRACTS = []
        
        def delayed_create_dsbe_contract(*args):
            CONTRACTS.append(args)
    
        def after_load():
            for args in CONTRACTS:
                create_dsbe_contract(*args)
                
        globals_dict.update(create_dsbe_contract=delayed_create_dsbe_contract)
        globals_dict.update(Contract=Contract)
        globals_dict.update(ContractEnding=ContractEnding)
        globals_dict.update(ContractType=ContractType)
        globals_dict.update(ExamPolicy=ExamPolicy)
        globals_dict.update(after_load=after_load)
        #~ globals_dict.update(create_jobs_contracttype=globals_dict['create_dsbe_contracttype'])
        #~ globals_dict.update(create_jobs_exampolicy=globals_dict['create_dsbe_exampolicy'])
        globals_dict['SOURCE_VERSION'] == '1.2.0'
        