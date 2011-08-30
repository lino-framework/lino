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
This fixture is for one-time use in a real case, 
and maybe as starting example for future similar cases.

Usage
-----

Before loading this fixture you must set :attr:`lino.Lino.legacy_data_path` 
in your local :xfile:`settings.py`.

You must also set the encoding for mdb-export::

    export MDB_ICONV=utf-8
    export MDB_JET_CHARSET=utf-8
    
Then load the fixture using the following command::

    python manage.py initdb std all_countries all_cities be all_languages props pp2lino
    
The following variant might help to save time during testing::
    
    python manage.py initdb std few_countries pp2lino --noinput


"""

import os
import sys
#~ ENCODING = sys.stdout.encoding
#~ import csv
import codecs
import datetime

from django.conf import settings
if not settings.LINO.legacy_data_path:
    raise Exception("You must specify the name of your .mdb file in settings.LINO.legacy_data_path!")


from lino.utils import dblogger
from lino.tools import resolve_model

from lino.apps.dsbe.models import Person, City, Country, Note
from lino.modlib.users.models import User
from lino.modlib.jobs.models import Job, Contract, JobProvider, \
  ContractEnding, ExamPolicy, ContractType, Company

def get_contracttype(pk):
    if pk == 0: 
        return
    try:
        ct = ContractType.objects.get(pk=pk)
    except ContractType.DoesNotExist: 
        dblogger.warning("ContractType %r does not exist?!",pk)
        return None
    return ct
        
from lino.utils.mdbtools import Loader

from django.core.validators import validate_email, ValidationError, URLValidator
validate_url = URLValidator()
def is_valid_url(s):
    try:
        validate_url(s)
        return True
    except ValidationError:
        return False
        
def is_valid_email(s):
    try:
        validate_email(s)
        return True
    except ValidationError:
        return False
        
        
CboStatutJuridique = {
  'Personne Physique' : 3,
  'SPRL' : 2,
  'ASBL' : 9,
  'SA' : 1,
  'NV' : 1,
  'Publique' :8, 
  'BVBA' : 2,
  'SCRL' : 4,
  'SIREAS' : None,
}

CboTypeMiseEmplois = {
  1	: u"PTP",
  2	: u"Art 60§7",
  3	: u"Art 60§7 (Tok)",
  5	: u"Art 60§7 Privé (Tok)",
  6	: u"Smet",
  7	: u"Art 61",
  8	: u"Activa",
  9	: u"Stage en Entreprise",
  17	: u"CDD",
  18	: u"CDI",
  19	: u"Intérim",
  20	: u"ALE",
  21	: u"FPI",
  22	: u"SINE",
  23	: u"anlo",
  24	: u"wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
  25	: u"contrat de remplacement CDD",
}


CboTypeContrat = {
    1	: u"Tutorat",
    2	: u"PIIS 18-25 ans",
    3	: u"PIIS + 25 ans",
    4	: u"PIIS étudiant",
    5	: u"PIIS stage en entreprise - experience prof",
    6	: u"PIIS stage de détermination et d'orientation socio",
    7	: u"PIIS formation",
    8	: u"PIIS prolongation",
}


OFFSET_PERSON = 1000
OFFSET_JOBPROVIDER = 3000
"""
Both CboTypeContrat and CboTypeMiseEmplois go to Lino's ContractType table.
The following offset is added to CboTypeContrat keys. 
Must be > item count of CboTypeMiseEmplois.
"""
OFFSET_CONTRACT_TYPE_CPAS = 100 
assert OFFSET_CONTRACT_TYPE_CPAS > len(CboTypeMiseEmplois) 

"""
Both TBMiseEmplois and TBTypeDeContratCPAS go to Lino's Contract table.
The following offset is added to TBTypeDeContratCPAS keys. 
Must be > record count of TBMiseEmplois.
"""
OFFSET_CONTRACT_CPAS = 2000
        


class LinoMdbLoader(Loader):
    "Base for all Loaders in this module"
    mdb_file = settings.LINO.legacy_data_path
    if not mdb_file:
        raise Exception("You must specify the name of your .mdb file in settings.LINO.legacy_data_path!")




class CityLoader(LinoMdbLoader):
    """
    
INFO Deferred City #184 (u'GANSHOREN') : {'__all__': [u'Un(e) City avec ce Country, Name et Zip code existe d\xe9j\xe0.'
]}
INFO Deferred City #270 (u'JETTE') : {'__all__': [u'Un(e) City avec ce Country, Name et Zip code existe d\xe9j\xe0.']}
INFO Deferred City #289 (u'KOEKELBERG') : {'__all__': [u'Un(e) City avec ce Country, Name et Zip code existe d\xe9j\xe0.
']}
INFO Deferred City #474 (u'SCHAERBEEK') : {'__all__': [u'Un(e) City avec ce Country, Name et Zip code existe d\xe9j\xe0.
']}
    
    """
  
  
  
    table_name = 'CboCommuneCodePostal'
    model = City
    headers = u"""
    IDCommuneCodePostal Commune CodePostal
    """.split()
    
    def row2obj(self,row):
        pk = int(row['IDCommuneCodePostal'])
        kw = {}
        kw.update(id=pk)
        kw.update(name=row['Commune'])
        kw.update(zip_code=row['CodePostal'])
        kw.update(country=Country.objects.get(pk='BE'))
        yield self.model(**kw)



class NotesLoader(LinoMdbLoader):
    table_name = 'TBJournal'
    model = Note
    headers = u"""
    IDJournal DateJournal JournalClient IDClient
    """.split()
    last_date = None
    
    def row2obj(self,row):
        pk = int(row['IDJournal'])
        kw = {}
        kw.update(id=pk)
        txt = row['JournalClient']
        if txt:
            if len(txt) > 200:
                kw.update(body=txt)
            else:
                kw.update(subject=txt)
            d = self.parsedate(row['DateJournal'])
            if d:
                self.last_date = d
            else:
                d = self.last_date
                #~ d = datetime.date.today()
                #~ dblogger.warning("TBJournal #%s : date was empty",pk)
            kw.update(date=d)
            idclient = int(row['IDClient']) + OFFSET_PERSON
            kw.update(person_id=idclient)
            #~ kw.update(person=Person.objects.get(pk=idclient))
            yield self.model(**kw)

class UsersISPLoader(LinoMdbLoader):
    table_name = 'TBASISP'
    model = User
    headers = u"""
    IDASISP TitreASISP NomASISP PrenomASISP CodeASISP Tel StatutASISP
    """.split()
    
    def row2obj(self,row):
        #~ pk = int(row['IDASISP'])
        kw = {}
        #~ kw.update(id=pk)
        kw.update(title=row['TitreASISP'])
        kw.update(first_name=row['PrenomASISP'])
        kw.update(last_name=row['NomASISP'])
        kw.update(username=row['CodeASISP'])
        kw.update(phone=row['Tel'])
        st = row['StatutASISP']
        if st == "Ouvert":
            kw.update(is_active=True)
        else:
            kw.update(is_active=False)
        yield self.model(**kw)


class UsersSGLoader(LinoMdbLoader):
    table_name = 'TBASSG'
    model = User
    headers = u"""
    IDASSSG TitreASSSG NomASSSG PrenomASSSG CodeASSSG TelASSSG StatutASSSG
    """.split()
    
    def row2obj(self,row):
        #~ pk = int(row['IDASSSG'])
        kw = {}
        #~ kw.update(id=pk)
        kw.update(title=row['TitreASSSG'])
        kw.update(first_name=row['PrenomASSSG'])
        kw.update(last_name=row['NomASSSG'])
        kw.update(username=row['CodeASSSG'])
        kw.update(phone=row['TelASSSG'])
        st = row['StatutASSSG']
        if st == "Ouvert":
            kw.update(is_active=True)
        else:
            kw.update(is_active=False)
        yield self.model(**kw)





class JobProviderLoader(LinoMdbLoader):
    table_name = 'TBEndroitMiseAuTravail'
    
    model = JobProvider
    headers = u"""
    IDEndroitMiseAuTravail EndroitMiseAuTravail IDStatutJuridique 
    NumeroInitiativeEconomieSociale 
    AdresseSiegeSocial N Bte 
    IDCommuneCodePostal NONSS Tel Fax EMail GSM Banque NCompte 
    Titre NomContact PrénomContact Fonction Tel1 Fax1 EMail1 
    Remarque Internet 
    Titre2 NomContact2 PrénomContact2 Fonction2 Tel2 GSM2 Fax2 EMail2 
    Titre3 NomContact3 PrénomContact3 Fonction3 Tel3 GSM3 Fax3 EMail3
    """.split()
    
    def row2obj(self,row):
        kw = {}
        kw.update(id=int(row['IDEndroitMiseAuTravail']) + OFFSET_JOBPROVIDER)
        kw.update(name=row['EndroitMiseAuTravail'])
        companyType=CboStatutJuridique.get(row['IDStatutJuridique'],None)
        if companyType:
            kw.update(type=CompanyType.objects.get(id=companyType))
        # see contacts/fixtures/std.py
        
        
        #~ kw.update(street_prefix=row[u'Rue'])
        kw.update(street=row[u'AdresseSiegeSocial'])
        kw.update(street_no=row[u'N'])
        kw.update(street_box=row[u'Bte'])
        kw.update(phone=row[u'Tel'])
        kw.update(gsm=row[u'GSM'])
        kw.update(fax=row[u'Fax'])
        kw.update(remarks="""
        NumeroInitiativeEconomieSociale : %(NumeroInitiativeEconomieSociale)s
        NONSS : %(NONSS)s
        """ % row)
        url = row[u'Internet']
        if url:
            if not url.startswith('http'):
                url = 'http://' + url
            if is_valid_url(url):
                kw.update(url=url)
        kw.update(remarks=row[u'Remarque'])
        if is_valid_email(row[u'EMail']):
            kw.update(email=row[u'EMail'])
        yield self.model(**kw)
    

class PersonLoader(LinoMdbLoader):
    table_name = 'TBClient'
    
    model = Person # resolve_model('contacts.Person')
    
    headers = [u'IDClient', u'DateArrivee', u'NumeroDossier', 
    u'Titre', u'Nom', u'Prénom', 
    u'Rue', u'Adresse', u'Numero', u'Boite', 
    u'IDCommuneCodePostal', u'Tel1', u'Tel2', u'GSM1', 
    u'GSM2', u'Email', u'DateNaissance', u'IDPays', u'IDNationalite', 
    u'NumeroNational', u'Conjoint', u'NEnfant', u'IBIS', u'Sexe', 
    u'Statut', u'DateFin', u'RISEQRIS', u'DateOctroi', 
    u'MontantRISEQRIS', u'Qualification', u'Phase', u'PIIS', 
    u'Tutorat', u'IDASISP', u'IDASSSG', u'Remarques', u'IDTokAns', 
    u'RPE', u'Art 35', u'DateDebutArt35', u'DateFinArt35', u'ALE', u'Update',
    u'PermisDeTravail']    
    
    def row2obj(self,row):
        kw = {}
        kw.update(id=int(row['IDClient']) + OFFSET_PERSON)
        kw.update(title=row['Titre'])
        if row['Nom']:
            kw.update(last_name=row['Nom'])
        else:
            kw.update(last_name="?")
        kw.update(first_name=row[u'Prénom'])
        kw.update(street_prefix=row[u'Rue'])
        kw.update(street=row[u'Adresse'])
        kw.update(street_no=row[u'Numero'])
        kw.update(street_box=row[u'Boite'])
        if is_valid_email(row[u'Email']):
            kw.update(email=row[u'Email'])
        if row[u'DateNaissance']:
            kw.update(birth_date=row[u'DateNaissance'])
        if row[u'DateArrivee']:
            kw.update(coached_from=row[u'DateArrivee'])
        yield self.model(**kw)
        


def get_or_create_job(provider_id,contract_type):
    if provider_id in (None,OFFSET_JOBPROVIDER):
        provider = None
    else:
        try:
            provider = JobProvider.objects.get(pk=provider_id)
        except JobProvider.DoesNotExist:
            dblogger.warning('JobProvider #%s does not exist.',provider_id)
            #~ provider = Provider(name=str(provider_id),id=provider_id)
            #~ privder.full_clean()
            #~ provider.save()
            provider = None
            #~ company = Company.objects.get(pk=provider_id)
            #~ provider = mti.insert_child(company,JobProvider)
            #~ provider.save()
    try:
        #~ if provider_id:
        return Job.objects.get(provider=provider,contract_type=contract_type)
        #~ else:
            #~ return Job.objects.get(provider__isnull=True,contract_type__id=contract_type_id)
    except Job.DoesNotExist:
        if provider is None:
            name = 'Job%s(interne)' % contract_type.id
        else:
            name = 'Job%s@%s' % (contract_type.id,provider)
        job = Job(
            provider=provider,
            contract_type=contract_type,
            name=name
            )
        job.full_clean()
        job.save()
        return job





class ContractArt60Loader(LinoMdbLoader):
    table_name = 'TBMiseEmplois'
    model = Contract
    headers = u"""
    IDMiseEmplois IDTypeMiseEmplois 
    MotifArt60 IDSubside IDETP 
    DebutContrat FinContrat TotalJourContrat 
    IDASSSG IDASISP 
    IDEndroitMiseAuTravail 
    Memo 
    IDClient 
    Durée Statut Montant DCAS DCSSS 
    IdQualification IDDetailFonction Bareme ArticleBudgetaireSPPPSalaire CoutAnnuel 
    Remarques DateCandidature
    """.split()
    
    def row2obj(self,row):
        kw = {}
        kw.update(id=int(row['IDMiseEmplois']))
        #~ ctype = 
        #~ if ctype:
            #~ kw.update(type=ContractType.objects.get(pk=ctype))
        kw.update(applies_from=self.parsedate(row[u'DebutContrat']))
        kw.update(applies_until=self.parsedate(row[u'FinContrat']))
        provider_id = row[u'IDEndroitMiseAuTravail']
        if provider_id:
            provider_id = int(provider_id) + OFFSET_JOBPROVIDER
        else:
            provider_id = None
        contract_type_id = row['IDTypeMiseEmplois']
        if contract_type_id:
            ct = get_contracttype(int(contract_type_id))
            if ct:
                job = get_or_create_job(provider_id,ct)
                if job: 
                    kw.update(job=job)
                    #~ kw.update(provider=JobProvider.objects.get(id=))
                    kw.update(person=Person.objects.get(id=int(row[u'IDClient'])+OFFSET_PERSON))
                    yield self.model(**kw)

class ContractVSELoader(LinoMdbLoader):
    table_name = 'TBTypeDeContratCPAS'
    model = Contract
    headers = u"""
    IDTypeDeContratCPAS IDTypeContrat DateDebut DateFin 
    ASCPAS ASISP Statut Evaluation IDClient DateSignature 
    TypePIIS NiveauEtude
    """.split()
    
    def row2obj(self,row):
        kw = {}
        kw.update(id=int(row['IDTypeDeContratCPAS'])+OFFSET_CONTRACT_CPAS)
        #~ ctype = int(row['IDTypeContrat']) 
        #~ if ctype:
            #~ kw.update(type=ContractType.objects.get(pk=ctype+ OFFSET_CONTRACT_TYPE_CPAS))
        kw.update(applies_from=self.parsedate(row[u'DateDebut']))
        kw.update(applies_until=self.parsedate(row[u'DateFin']))
        
        contract_type_id = row['IDTypeContrat']
        if contract_type_id:
            ct = get_contracttype(int(contract_type_id)+OFFSET_CONTRACT_TYPE_CPAS)
            if ct:
                job = get_or_create_job(None,ct)
                if job: 
                    kw.update(job=job)
                    #~ kw.update(provider=JobProvider.objects.get(id=int(row[u'IDEndroitMiseAuTravail'])+OFFSET_JOBPROVIDER))
                    kw.update(person=Person.objects.get(id=int(row[u'IDClient'])+OFFSET_PERSON))
                    yield self.model(**kw)

def objects():
    #~ User = resolve_model('users.User')
    yield User(username="root",is_staff=True,is_superuser=True,first_name="Root",last_name="Superuser")
    #~ for o in PersonLoader().load(): yield o
    for k,v in CboTypeMiseEmplois.items():
        yield ContractType(id=k,name=v)
    for k,v in CboTypeContrat.items():
        yield ContractType(id=k+OFFSET_CONTRACT_TYPE_CPAS,name=v)
    yield UsersISPLoader()
    yield UsersSGLoader()
    yield CityLoader()
    yield PersonLoader()
    yield JobProviderLoader()
    yield ContractArt60Loader()
    yield ContractVSELoader()
    yield NotesLoader()
    
    #~ reader = csv.reader(open(,'rb'))