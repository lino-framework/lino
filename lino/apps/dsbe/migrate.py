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

"""
This is a real-world example of how the application developer 
can provide automatic data migrations for 
:mod:`lino.utils.dpy` dumps.

This module is used when loading a dpy dump back.
Lino writes the corresponding ``import`` statement into every dpy dump because
:mod:`lino.apps.dsbe.settings.Lino` has
:attr:`lino.Lino.migration_module` 
set to ``"lino.apps.dsbe.migrate"``

Deserves more documentation.
"""

from django.conf import settings
from lino.tools import resolve_model
from lino.utils import mti
from lino.utils import dblogger

def migrate_from_1_1_16(globals_dict):
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
    return '1.1.17'
        
def migrate_from_1_1_17(globals_dict):
  
    from lino.modlib.cal.models import migrate_reminder
    from lino.modlib.jobs.models import Job, Contract, JobProvider, \
      ContractEnding, ExamPolicy, ContractType, Company
    
    Upload = resolve_model("uploads.Upload")
    Link = resolve_model("links.Link")
    Note = resolve_model("notes.Note")
    
    
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
            if provider is None:
                name = 'Stelle%s(intern)' % contract_type_id
            else:
                name = 'Stelle%s@%s' % (contract_type_id,provider)
            job = Job(
                provider=provider,
                contract_type_id=contract_type_id,
                name=name
                )
            job.save()
            return job
            
    CONTRACTS = []
    REMINDERS = []
    UPLOADS = []
    
    def create_dsbe_contract(id, user_id, reminder_date, reminder_text, 
        delay_value, delay_type, reminder_done, must_build, person_id, 
        company_id, contact_id, language, type_id, applies_from, 
        applies_until, date_decided, date_issued, duration, regime, 
        schedule, hourly_rate, refund_rate, reference_person, 
        responsibilities, stages, goals, duties_asd, duties_dsbe, 
        duties_company, duties_person, user_asd_id, exam_policy_id, 
        ending_id, date_ended):
        job = get_or_create_job(company_id,type_id)
        obj = Contract(id=id,user_id=user_id,
          #~ reminder_date=reminder_date,
          #~ reminder_text=reminder_text,delay_value=delay_value,
          #~ delay_type=delay_type,reminder_done=reminder_done,
          must_build=must_build,person_id=person_id,
          job=job,
          provider_id=company_id,
          contact_id=contact_id,language=language,type_id=type_id,
          applies_from=applies_from,applies_until=applies_until,date_decided=date_decided,date_issued=date_issued,duration=duration,regime=regime,schedule=schedule,hourly_rate=hourly_rate,refund_rate=refund_rate,reference_person=reference_person,responsibilities=responsibilities,stages=stages,goals=goals,duties_asd=duties_asd,duties_dsbe=duties_dsbe,duties_company=duties_company,duties_person=duties_person,user_asd_id=user_asd_id,exam_policy_id=exam_policy_id,ending_id=ending_id,date_ended=date_ended)
        REMINDERS.append((obj,(reminder_date,reminder_text,delay_value,delay_type,reminder_done)))
        return obj
          
    def delayed_create_dsbe_contract(*args):
        CONTRACTS.append(args)
        
    def create_links_link(id, user_id, reminder_date, reminder_text, delay_value, delay_type, reminder_done, person_id, company_id, type_id, date, url, name):
        obj = Link(id=id,user_id=user_id,
          #~ reminder_date=reminder_date,reminder_text=reminder_text,
          #~ delay_value=delay_value,delay_type=delay_type,
          #~ reminder_done=reminder_done,
          person_id=person_id,company_id=company_id,type_id=type_id,date=date,url=url,name=name)
        REMINDERS.append((obj,(reminder_date,reminder_text,delay_value,delay_type,reminder_done)))
        return obj
        
    def create_notes_note(id, user_id, reminder_date, reminder_text, delay_value, delay_type, reminder_done, must_build, person_id, company_id, date, type_id, event_type_id, subject, body, language):
        obj = Note(id=id,user_id=user_id,
          #~ reminder_date=reminder_date,reminder_text=reminder_text,
          #~ delay_value=delay_value,delay_type=delay_type,
          #~ reminder_done=reminder_done,
          must_build=must_build,person_id=person_id,company_id=company_id,date=date,type_id=type_id,event_type_id=event_type_id,subject=subject,body=body,language=language)
        REMINDERS.append((obj,(reminder_date,reminder_text,delay_value,delay_type,reminder_done)))
        return obj
        
    def create_uploads_upload(id, user_id, owner_type_id, owner_id, reminder_date, reminder_text, delay_value, delay_type, reminder_done, file, mimetype, created, modified, description, type_id):
        obj = Upload(id=id,user_id=user_id,
          owner_type_id=owner_type_id,owner_id=owner_id,
          valid_until=reminder_date,
          #~ reminder_date=reminder_date,reminder_text=reminder_text,
          #~ delay_value=delay_value,delay_type=delay_type,
          #~ reminder_done=reminder_done,
          file=file,mimetype=mimetype,
          created=created,modified=modified,description=description,type_id=type_id)
        #~ REMINDERS.append((obj,(reminder_date,reminder_text,delay_value,delay_type,reminder_done)))
        # must relay the saving of uploads because owner is a generic foreign key 
        # which doesn't fail to save the instance but returns None for the owner if it doesn't yet 
        # exist.
        UPLOADS.append(obj)
        #~ return obj
                        

    def after_load():
        for args in CONTRACTS:
            obj = create_dsbe_contract(*args)
            obj.full_clean()
            obj.save()
        for obj,args in REMINDERS:
            migrate_reminder(obj,*args)
        for obj in UPLOADS:
            obj.save()
            
    globals_dict.update(create_dsbe_contract=delayed_create_dsbe_contract)
    globals_dict.update(Contract=Contract)
    globals_dict.update(ContractEnding=ContractEnding)
    globals_dict.update(ContractType=ContractType)
    globals_dict.update(ExamPolicy=ExamPolicy)
    globals_dict.update(create_uploads_upload=create_uploads_upload)
    globals_dict.update(create_notes_note=create_notes_note)
    globals_dict.update(create_links_link=create_links_link)
    globals_dict.update(after_load=after_load)
    #~ globals_dict.update(create_jobs_contracttype=globals_dict['create_dsbe_contracttype'])
    #~ globals_dict.update(create_jobs_exampolicy=globals_dict['create_dsbe_exampolicy'])
    return '1.2.0'
        
  
def migrate_from_1_2_0(globals_dict):
    return '1.2.1'
  
def migrate_from_1_2_1(globals_dict):
    """
    - rename model contacts.ContactType to contacts.RoleType
    - rename model contacts.Contact to contacts.Role 
      (and field company to parent, person to child)
    - change the id of existing users because User is now subclass of Contact
      and modify SiteConfig.next_partner_id
    """
    Role = resolve_model("contacts.Role")
    RoleType = resolve_model("contacts.RoleType")
    
    Event = resolve_model("cal.Event")
    Task = resolve_model("cal.Task")
    Person = resolve_model("contacts.Person")
    Contract = resolve_model("jobs.Contract")
    Link = resolve_model("links.Link")
    SiteConfig = resolve_model("lino.SiteConfig")
    TextFieldTemplate = resolve_model("lino.TextFieldTemplate")
    Note = resolve_model("notes.Note")
    Upload = resolve_model("uploads.Upload")
    User = resolve_model("users.User")
    PersonSearch = resolve_model("dsbe.PersonSearch")
    
    
    
    scl = list(globals_dict.get('lino_siteconfig_objects')())
    assert len(scl) == 1
    global new_next_partner_id
    new_next_partner_id = user_id_offset = scl[0].next_partner_id
    def new_user_id(old_id):
        if old_id is None: return None
        global new_next_partner_id
        i = old_id + user_id_offset
        new_next_partner_id = max(new_next_partner_id,i+1)
        return i

    def create_lino_siteconfig(id, default_build_method, site_company_id, job_office_id, propgroup_skills_id, propgroup_softskills_id, propgroup_obstacles_id, residence_permit_upload_type_id, work_permit_upload_type_id, driving_licence_upload_type_id, next_partner_id):
        next_partner_id = new_next_partner_id
        return SiteConfig(id=id,default_build_method=default_build_method,site_company_id=site_company_id,job_office_id=job_office_id,propgroup_skills_id=propgroup_skills_id,propgroup_softskills_id=propgroup_softskills_id,propgroup_obstacles_id=propgroup_obstacles_id,residence_permit_upload_type_id=residence_permit_upload_type_id,work_permit_upload_type_id=work_permit_upload_type_id,driving_licence_upload_type_id=driving_licence_upload_type_id,next_partner_id=next_partner_id)
    globals_dict.update(create_lino_siteconfig=create_lino_siteconfig)

        
    def create_users_user(id, username, first_name, last_name, email, is_staff, is_expert, is_active, is_superuser, last_login, date_joined):
        return User(id=new_user_id(id),username=username,first_name=first_name,last_name=last_name,email=email,is_staff=is_staff,is_expert=is_expert,is_active=is_active,is_superuser=is_superuser,last_login=last_login,date_joined=date_joined)
    globals_dict.update(create_users_user=create_users_user)
    
    def create_uploads_upload(id, user_id, owner_type_id, owner_id, file, mimetype, created, modified, description, type_id, valid_until):
        return Upload(id=id,user_id=new_user_id(user_id),owner_type_id=owner_type_id,owner_id=owner_id,file=file,mimetype=mimetype,created=created,modified=modified,description=description,type_id=type_id,valid_until=valid_until)
    globals_dict.update(create_uploads_upload=create_uploads_upload)
    
    def create_notes_note(id, user_id, must_build, person_id, company_id, date, type_id, event_type_id, subject, body, language):
        return Note(id=id,user_id=new_user_id(user_id),must_build=must_build,person_id=person_id,company_id=company_id,date=date,type_id=type_id,event_type_id=event_type_id,subject=subject,body=body,language=language)
    globals_dict.update(create_notes_note=create_notes_note)
    
    def create_contacts_contacttype(id, name, name_fr, name_en):
        #~ return ContactType(id=id,name=name,name_fr=name_fr,name_en=name_en)
        return RoleType(id=id,name=name,name_fr=name_fr,name_en=name_en)
    globals_dict.update(create_contacts_contacttype=create_contacts_contacttype)
    
    def create_lino_textfieldtemplate(id, user_id, name, description, text):
        return TextFieldTemplate(id=id,user_id=new_user_id(user_id),name=name,description=description,text=text)
    globals_dict.update(create_lino_textfieldtemplate=create_lino_textfieldtemplate)
    
    def create_links_link(id, user_id, person_id, company_id, type_id, date, url, name):
        return Link(id=id,user_id=new_user_id(user_id),person_id=person_id,company_id=company_id,type_id=type_id,date=date,url=url,name=name)
    globals_dict.update(create_links_link=create_links_link)
    
    def create_jobs_contract(id, user_id, must_build, person_id, provider_id, contact_id, language, job_id, type_id, applies_from, applies_until, date_decided, date_issued, duration, regime, schedule, hourly_rate, refund_rate, reference_person, responsibilities, stages, goals, duties_asd, duties_dsbe, duties_company, duties_person, user_asd_id, exam_policy_id, ending_id, date_ended):
        user_asd_id = new_user_id(user_asd_id)
        return Contract(id=id,user_id=new_user_id(user_id),must_build=must_build,person_id=person_id,provider_id=provider_id,contact_id=contact_id,language=language,job_id=job_id,type_id=type_id,applies_from=applies_from,applies_until=applies_until,date_decided=date_decided,date_issued=date_issued,duration=duration,regime=regime,schedule=schedule,hourly_rate=hourly_rate,refund_rate=refund_rate,reference_person=reference_person,responsibilities=responsibilities,stages=stages,goals=goals,duties_asd=duties_asd,duties_dsbe=duties_dsbe,duties_company=duties_company,duties_person=duties_person,user_asd_id=user_asd_id,exam_policy_id=exam_policy_id,ending_id=ending_id,date_ended=date_ended)
    globals_dict.update(create_jobs_contract=create_jobs_contract)
    
    def create_dsbe_personsearch(id, user_id, title, aged_from, aged_to, sex, only_my_persons, coached_by_id, period_from, period_until):
        user_id = new_user_id(user_id)
        coached_by_id = new_user_id(coached_by_id)
        return PersonSearch(id=id,user_id=user_id,title=title,aged_from=aged_from,aged_to=aged_to,sex=sex,only_my_persons=only_my_persons,coached_by_id=coached_by_id,period_from=period_from,period_until=period_until)
    globals_dict.update(create_dsbe_personsearch=create_dsbe_personsearch)

    def create_contacts_person(country_id, city_id, name, addr1, street_prefix, street, street_no, street_box, addr2, zip_code, region, language, email, url, phone, gsm, fax, remarks, first_name, last_name, title, sex, id, is_active, activity_id, bank_account1, bank_account2, remarks2, gesdos_id, is_cpas, is_senior, group_id, coached_from, coached_until, coach1_id, coach2_id, birth_date, birth_date_circa, birth_place, birth_country_id, civil_state, national_id, health_insurance_id, pharmacy_id, nationality_id, card_number, card_valid_from, card_valid_until, card_type, card_issuer, noble_condition, residence_type, in_belgium_since, unemployed_since, needs_residence_permit, needs_work_permit, work_permit_suspended_until, aid_type_id, income_ag, income_wg, income_kg, income_rente, income_misc, is_seeking, unavailable_until, unavailable_why, obstacles, skills, job_agents, job_office_contact_id):
        coach1_id = new_user_id(coach1_id)
        coach2_id = new_user_id(coach2_id)
        return Person(country_id=country_id,city_id=city_id,name=name,addr1=addr1,street_prefix=street_prefix,street=street,street_no=street_no,street_box=street_box,addr2=addr2,zip_code=zip_code,region=region,language=language,email=email,url=url,phone=phone,gsm=gsm,fax=fax,remarks=remarks,first_name=first_name,last_name=last_name,title=title,sex=sex,
          # Person pk is now contact_ptr_id, and FakeDeserializedObject.try_save tests this to decided whether
          # it can defer the save 
          id=id,
          contact_ptr_id=id,
          is_active=is_active,activity_id=activity_id,bank_account1=bank_account1,bank_account2=bank_account2,remarks2=remarks2,gesdos_id=gesdos_id,is_cpas=is_cpas,is_senior=is_senior,group_id=group_id,coached_from=coached_from,coached_until=coached_until,coach1_id=coach1_id,coach2_id=coach2_id,birth_date=birth_date,birth_date_circa=birth_date_circa,birth_place=birth_place,birth_country_id=birth_country_id,civil_state=civil_state,national_id=national_id,health_insurance_id=health_insurance_id,pharmacy_id=pharmacy_id,nationality_id=nationality_id,card_number=card_number,card_valid_from=card_valid_from,card_valid_until=card_valid_until,card_type=card_type,card_issuer=card_issuer,noble_condition=noble_condition,residence_type=residence_type,in_belgium_since=in_belgium_since,unemployed_since=unemployed_since,needs_residence_permit=needs_residence_permit,needs_work_permit=needs_work_permit,work_permit_suspended_until=work_permit_suspended_until,aid_type_id=aid_type_id,income_ag=income_ag,income_wg=income_wg,income_kg=income_kg,income_rente=income_rente,income_misc=income_misc,is_seeking=is_seeking,unavailable_until=unavailable_until,unavailable_why=unavailable_why,obstacles=obstacles,skills=skills,job_agents=job_agents,job_office_contact_id=job_office_contact_id)
    globals_dict.update(create_contacts_person=create_contacts_person)
    
    def create_contacts_contact(id, person_id, company_id, type_id):
        #~ return Contact(id=id,person_id=person_id,company_id=company_id,type_id=type_id)
        if not company_id: return None # field was nullable
        return Role(id=id,child_id=person_id,parent_id=company_id,type_id=type_id)
    globals_dict.update(create_contacts_contact=create_contacts_contact)
    

    def create_cal_task(id, user_id, created, modified, owner_type_id, owner_id, person_id, company_id, start_date, start_time, summary, description, access_class, sequence, alarm_value, alarm_unit, dt_alarm, due_date, due_time, done, percent, status, auto_type):
        user_id = new_user_id(user_id)
        if person_id:
            project_id=person_id
            if company_id:
                dblogger.warning("create_cal_task looses company_id %s for task #%",company_id,id)
        else:
            project_id=company_id
        return Task(id=id,user_id=user_id,created=created,modified=modified,owner_type_id=owner_type_id,owner_id=owner_id,project_id=project_id,start_date=start_date,start_time=start_time,summary=summary,description=description,access_class=access_class,sequence=sequence,alarm_value=alarm_value,alarm_unit=alarm_unit,dt_alarm=dt_alarm,due_date=due_date,due_time=due_time,done=done,percent=percent,status=status,auto_type=auto_type)
    globals_dict.update(create_cal_task=create_cal_task)

    def create_cal_event(id, user_id, created, modified, must_build, person_id, company_id, start_date, start_time, summary, description, access_class, sequence, alarm_value, alarm_unit, dt_alarm, end_date, end_time, transparent, type_id, place_id, priority, status, duration_value, duration_unit, repeat_value, repeat_unit):
        user_id = new_user_id(user_id)
        return Event(id=id,user_id=user_id,created=created,modified=modified,must_build=must_build,person_id=person_id,company_id=company_id,start_date=start_date,start_time=start_time,summary=summary,description=description,access_class=access_class,sequence=sequence,alarm_value=alarm_value,alarm_unit=alarm_unit,dt_alarm=dt_alarm,end_date=end_date,end_time=end_time,transparent=transparent,type_id=type_id,place_id=place_id,priority=priority,status=status,duration_value=duration_value,duration_unit=duration_unit,repeat_value=repeat_value,repeat_unit=repeat_unit)
    globals_dict.update(create_cal_event=create_cal_event)
  
    return '1.2.2'
  

def install(globals_dict):
    """
    Called from dpy dumps generated on a Lino/DSBE site
    (because `lino.apps.dsbe.settings.Lino.migration_module` 
    is set to :mod:`lino.apps.dsbe.migrate`).
    """
    
    # for backwards compatibility reading dumps generated by Lino before 20110827:
    settings.LINO.loading_from_dump = True 
  
    #~ from lino.modlib.cal import models as cal
    #~ cal.SKIP_AUTO_TASKS = True
    
    while True:
        funcname = 'migrate_from_' + globals_dict['SOURCE_VERSION'].replace('.','_')
        func = globals().get(funcname,None)
        if func:
            dblogger.info("Found %s()", funcname)
            globals_dict['SOURCE_VERSION'] = func(globals_dict)
            dblogger.info("--> migrating to version %s", globals_dict['SOURCE_VERSION'])
        else:
            break
    
      
        