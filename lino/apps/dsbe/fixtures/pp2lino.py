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

    python manage.py initdb std all_countries all_languages props pp2lino
    
The following variant might help to save time during testing::
    
    python manage.py initdb std few_countries pp2lino --noinput


Notes techniques import de données PP vers Lino
-----------------------------------------------

- La table CboListeFonction (secteurs d'activité) n'est pas importée. 
  Seulement la CboDetailFonction est importée (vers 
  :class:`lino.modlib.properties.models.Property`)


"""

import os
import sys
#~ ENCODING = sys.stdout.encoding
#~ import csv
import codecs
import datetime

from django.conf import settings

from lino.utils import dblogger
from lino.utils.instantiator import Instantiator
from lino.tools import resolve_model

from lino.apps.dsbe.models import Company, Person, City, Country, Note, PersonGroup
from lino.modlib.users.models import User
from lino.modlib.jobs import models as jobs
from lino.modlib.isip import models as isip
from lino.modlib.properties import models as properties

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

# goes to jobs.ContractType
#~ CboTypeMiseEmplois = {
  #~ 1	: u"PTP",
  #~ 2	: u"Art 60§7",
  #~ 3	: u"Art 60§7 (Tok)",
  #~ 5	: u"Art 60§7 Privé (Tok)",
  #~ 6	: u"Smet",
  #~ 7	: u"Art 61",
  #~ 8	: u"Activa",
  #~ 9	: u"Stage en Entreprise",
  #~ 17	: u"CDD",
  #~ 18	: u"CDI",
  #~ 19	: u"Intérim",
  #~ 20	: u"ALE",
  #~ 21	: u"FPI",
  #~ 22	: u"SINE",
  #~ 23	: u"anlo",
  #~ 24	: u"wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
  #~ 25	: u"contrat de remplacement CDD",
#~ }


# goes to isip.ContractType
#~ CboTypeContrat = {
    #~ 1	: u"Tutorat",
    #~ 2	: u"PIIS 18-25 ans",
    #~ 3	: u"PIIS + 25 ans",
    #~ 4	: u"PIIS étudiant",
    #~ 5	: u"PIIS stage en entreprise - experience prof",
    #~ 6	: u"PIIS stage de détermination et d'orientation socio",
    #~ 7	: u"PIIS formation",
    #~ 8	: u"PIIS prolongation",
#~ }

"""
The following two dictionaries need manual work: 
replace full names by their uppercase ISO2 country code.
"""

CboNationalite = {
  1:"BE",
  2:"CG", # "Congolais(e)",
  3:'RU', # "Russe",
  4:'RW', # "Rwandaise",
  5:'CL', # "Chilien(ne)",
  6:"FR",
  7:'RO', # "Roumain(e)",
  8:"CH",
  9:"Colombien(ne)",
  11:"Uruguayen (ne)",
  12:'MA', # "Marocain(ne)",
  14:'DZ', # u"Algérien(ne)",
  15:'MU', # "Mauricien(ne)",
  16:'TG', # "Togolais(e)",
  17:u"Réfugié Politique",
  18:"Turque",
  19:'CM', # "Camerounai (se)",
  20:"Perouvien(ne)",
  21:'MD', # "Moldave(iene)",
  23:'BI', # "burundais(e)",
  24:"Sierra Leonais(e)",
  25:'MR', # "Mauritanien(ne)",
  26:'BR', # u"Brésilien(ne)",
  27:'PT', # "Portugais(e)",
  28:'LB', # "libanais(e)",
  29:"DE",
  30:'SY',# "syrien(ne)",
  31:"GN", # "Guinéen(ne)",
  32:u"Libérien(ne)",
  33:"TN",
  34:'NG', # "Nigérian(nes)",
  35:u"ouzbékistan",
  36:"bolivien(ne)",
  37:'PL', # "polonais(e)",
  38:u"sénégalais(e)",
  39:"IR", # "Iranien(ne)",
  40:'IQ', # "Iraquien(ne)",
  41:"arménie",
  42:'IT', # "Italien(ne)",
  43:'AO', # "angolien(ne)",
  44:'NE', # "Nigerien(ne)",
  45:"Chinnoise",
  46:"burkina Faso",
  48:"laotienne",
  49:"ivoirien(ne)",
  50:u"US",
  51:"georgien(ne)",
  52:"grec",
  53:'MK', # "yougoslave",
  54:u"bosnie-herzégovine",
  55:"Ukrainien(ne)",
  56:'EC', # "Equatorien",
  57:"pakistannais(e)",
  58:"vietnamien(ne)",
  59:u"indonésien(ne)",
  60:"Malgache",
  62:"indien(ne)",
  63:'AL', # "albanais",
  64:'ES', # "Espagnol(e)",
  65:"Macedoine",
  66:'DJ', # "Djiboutien(ne)",
  68:"egyptien(ne)",
  69:"NL",
  70:'KZ', # "Kazakhstan",
  71:"Somalien(ne)",
  72:"AF",
  73:'CU', # "Cubaine",
  74:'TD', # "tchad",
  75:"Royaume-Uni",
  76:'LT', # "lituanienne ",
  77:"kirghizistan",
  78:'ET', # "Ethiopie",
}

CboPays = {
  1:u"Afrique du Sud"
  ,2:'AL' # u"Albanie"
  ,3:'DZ' # u"Algérie"
  ,4:'DE' # u"Allemagne"
  ,5:u"Andorre"
  ,6:'AO' # u"Angola"
  ,7:u"Antigua-et-Barbuda"
  ,8:u"Arabie Saoudite"
  ,9:u"Argentine"
  ,10:u"Arménie"
  ,11:'AU' # u"Australie"
  ,12:'AS' # u"Autriche"
  ,13:u"Azerbaļdjan"
  ,14:u"Bahamas"
  ,15:u"Bahreļn"
  ,16:u"Bangladesh"
  ,17:u"Barbade"
  ,18:u"Beiau"
  ,19:'BE' # u"Belgique"
  ,20:u"Belize"
  ,21:u"Bénin"
  ,22:u"Bhoutan"
  ,23:u"Biélorussie"
  ,24:u"Birmanie"
  ,25:u"Bolivie"
  ,26:u"Bosnie-Herzégovine"
  ,27:u"Botswana"
  ,28:'BR' # u"Brésil"
  ,29:u"Brunei"
  ,30:u"Bulgarie"
  ,31:u"Burkina"
  ,32:'BI' # u"Burundi"
  ,33:u"Cambodge"
  ,34:'CM' # u"Cameroun"
  ,35:u"Canada"
  ,36:u"Cap-Vert"
  ,37:'CL' # u"Chili"
  ,38:'CN' # u"Chine"
  ,39:u"Chypre"
  ,40:u"Colombie"
  ,41:u"Comores"
  ,42:'CG' # u"Congo"
  ,44:u"Cook (les īles)"
  ,45:u"Corée du Nord"
  ,46:u"Corée du Sud"
  ,47:u"Costa Rica"
  ,48:'CI' # u"Cōte d'Ivoire"
  ,49:u"Croatie"
  ,50:'CU' # u"Cuba"
  ,51:'DK' # u"Danemark"
  ,52:'DJ' # u"République de Djibouti"
  ,53:'DM' # u"Dominique"
  ,54:u"Egypte"
  ,55:u"Émirats arabes unis"
  ,56:'EC' # u"Equateur"
  ,57:u"Erythrée"
  ,58:'ES' # u"Espagne"
  ,59:'EE' # u"Estonie"
  ,60:'US' # u"Etats-Unis"
  ,61:'ET' # u"Ethiopie"
  ,62:u"Fidji"
  ,63:'FI' # u"Finlande"
  ,64:'FR' # u"France"
  ,65:u"Gabon"
  ,66:u"Gambie"
  ,67:u"Géorgie"
  ,68:u"Ghana"
  ,69:u"Grčce"
  ,70:u"Grenade"
  ,71:'GT' # u"Guatemala"
  ,72:"GN" # u"Guinée"
  ,73:u"Guinée-Bissao"
  ,74:u"Guinée équatoriale"
  ,75:u"Guyana"
  ,76:u"Haļti"
  ,77:u"Honduras"
  ,78:u"Hongrie"
  ,79:u"Inde"
  ,80:u"Indonésie"
  ,81:"IR" # u"Iran"
  ,82:'IQ' # u"Iraq"
  ,83:u"Irlande"
  ,84:u"Islande"
  ,85:u"Israėl"
  ,86:'IT' # u"Italie"
  ,87:u"Jamaļque"
  ,88:u"Japon"
  ,89:u"Jordanie"
  ,90:'KZ' # u"Kazakhstan"
  ,91:u"Kenya"
  ,92:u"Kirghizistan"
  ,93:u"Kiribati"
  ,94:u"Koweļt"
  ,95:u"Laos"
  ,96:u"Lesotho"
  ,97:u"Lettonie"
  ,98:'LB' # u"Liban"
  ,99:u"Libéria"
  ,100:u"Libye"
  ,101:u"Liechtenstein"
  ,102:'LT' # u"Lituanie"
  ,103:'LU' # u"Luxembourg"
  ,104:u"Macédoine"
  ,105:u"Madagascar"
  ,106:u"Malaisie"
  ,107:u"Malawi"
  ,108:u"Maldives"
  ,109:u"Mali"
  ,110:u"Malte"
  ,111:'MA' # u"Maroc"
  ,112:u"Marshall"
  ,113:'MU' # u"Maurice"
  ,114:'MR' # u"Mauritanie"
  ,115:u"Mexique"
  ,116:u"Micronésie"
  ,117:'MD' # u"Moldavie"
  ,118:u"Monaco"
  ,119:u"Mongolie"
  ,120:u"Mozambique"
  ,121:u"Namibie"
  ,122:u"Nauru"
  ,123:u"Népal"
  ,124:u"Nicaragua"
  ,125:'NE' # u"Niger"
  ,126:'NG' # u"Nigeria"
  ,127:u"Niue"
  ,128:u"Norvčge"
  ,129:u"Nouvelle-Zélande"
  ,130:u"Oman"
  ,131:u"Ouganda"
  ,132:u"Ouzbékistan"
  ,133:u"Pakistan"
  ,134:u"Panama"
  ,135:u"Papouasie - Nouvelle Guin"
  ,136:u"Paraguay"
  ,137:'NL' # u"Pays-Bas"
  ,138:'PE' # u"Pérou"
  ,139:u"Philippines"
  ,140:'PL' # u"Pologne"
  ,141:'PT' # u"Portugal"
  ,142:u"Qatar"
  ,143:u"République centrafricaine"
  ,144:'DO' # u"République dominicaine"
  ,145:u"République tchčque"
  ,146:'RO' # u"Roumanie"
  ,147:u"Royaume-Uni"
  ,148:'RU' # u"Russie"
  ,149:'RW' # u"Rwanda"
  ,150:u"Saint-Christophe-et-Niévč"
  ,151:u"Sainte-Lucie"
  ,152:u"Vatican"
  ,153:u"Saint-Vincent-et-les Gren"
  ,154:u"Salomon"
  ,155:u"Salvador"
  ,156:u"Samoa occidentales"
  ,157:u"Sao Tomé-et-Principe"
  ,158:u"Sénégal"
  ,159:u"Seychelles"
  ,160:u"Sierra Leone"
  ,161:u"Singapour"
  ,162:u"Slovaquie"
  ,163:u"Slovénie"
  ,164:u"Somalie"
  ,165:u"Soudan"
  ,166:u"Sri Lanka"
  ,167:u"Sučde"
  ,168:u"Suisse"
  ,169:u"Suriname"
  ,170:u"Swaziland"
  ,171:'SY' # u"Syrie"
  ,172:u"Tadjikistan"
  ,173:'TZ' # u"Tanzanie"
  ,174:'TD' # u"Tchad"
  ,175:u"Thaļlande"
  ,176:'TG' # u"Togo"
  ,177:u"Tonga"
  ,178:u"Trinité-et-Tobago"
  ,179:u"TN"
  ,180:u"Turkménistan"
  ,181:u"Turquie"
  ,182:u"Tuvalu"
  ,183:u"Ukraine"
  ,184:u"Uruguay"
  ,185:u"Vanuatu"
  ,186:u"Venezuela"
  ,187:u"Viźt Nam"
  ,188:u"Yémen"
  ,189:'MK' # u"Yougoslavie"
  ,190:'ZRCD' # u"Zaļre"
  ,191:u"Zambie"
  ,192:u"Zimbabwe"
  ,193:'AF' #u"Afghanistan"
  ,194:u"Uzbekistan"
}


def k2iso(dd,k,ddname):
    if not k: return None
    k = int(k)
    if k == 0: return None
    country_id = dd.get(k)
    if country_id is None:
        dblogger.warning("Unknown %s id %s",ddname,k)
        return None
    if len(country_id) == 2:
        return country_id
    if len(country_id) == 4 and country_id == country_id.upper():
        return country_id
    dblogger.warning("Invalid %s code %s -> %r",ddname,k,country_id)
        
def nation2iso(k): return k2iso(CboNationalite,k,'CboNationalite')
def pays2iso(k):return k2iso(CboPays,k,'CboPays')


def code2user(pk,offset=0):
    if not pk: return None
    pk = int(pk) + offset
    try:
        return User.objects.get(id=pk)
    except User.DoesNotExist:
        dblogger.warning("Unkown user %r",pk)
            
def phase2group(ph):
    if not ph: return
    try:
        return PersonGroup.objects.get(name=ph)
    except PersonGroup.DoesNotExist:
        pass

#~ def get_contracttype(pk):
    #~ if pk == 0: 
        #~ return
    #~ try:
        #~ ct = ContractType.objects.get(pk=pk)
    #~ except ContractType.DoesNotExist: 
        #~ dblogger.warning("ContractType %r does not exist?!",pk)
        #~ return None
    #~ return ct
        
def get_by_id(model,pk,offset=0):
    if not pk: return None
    pk = int(pk)
    if pk == 0: return None
    try:
        return model.objects.get(pk=pk+offset)
    except model.DoesNotExist: 
        dblogger.warning("%s %r does not exist?!",model,pk)
        return None





OFFSET_USER_ISP = 100
OFFSET_PERSON = 1000
OFFSET_JOBPROVIDER = 3000
#~ """
#~ Both CboTypeContrat and CboTypeMiseEmplois go to Lino's ContractType table.
#~ The following offset is added to CboTypeContrat keys. 
#~ Must be > item count of CboTypeMiseEmplois.
#~ """
#~ OFFSET_CONTRACT_TYPE_CPAS = 100 
#~ assert OFFSET_CONTRACT_TYPE_CPAS > len(CboTypeMiseEmplois) 

#~ """
#~ Both TBMiseEmplois and TBTypeDeContratCPAS go to Lino's Contract table.
#~ The following offset is added to TBTypeDeContratCPAS keys. 
#~ Must be > record count of TBMiseEmplois.
#~ """
#~ OFFSET_CONTRACT_CPAS = 2000
        


def get_or_create_job(provider,contract_type,job_type,sector,function):
    try:
        #~ if provider_id:
        return jobs.Job.objects.get(provider=provider,
            contract_type=contract_type,
            type=job_type,
            sector=sector,
            function=function)
        #~ else:
            #~ return Job.objects.get(provider__isnull=True,contract_type__id=contract_type_id)
    except jobs.Job.DoesNotExist:
        if provider is None:
            name = '%s(interne)' % function
        else:
            name = '%s@%s' % (function,provider)
        job = jobs.Job(
            provider=provider,
            contract_type=contract_type,
            type=job_type,
            name=name,
            sector=sector,
            function=function
            )
        job.full_clean()
        job.save()
        return job





class LinoMdbLoader(Loader):
    "Base for all Loaders in this module"
    mdb_file = settings.LINO.legacy_data_path



class CityLoader(LinoMdbLoader):
    """
    Converts rows from CboCommuneCodePostal to City instances.
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
    """
    Converts rows from TBJournal to Note instances.
    """
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

class UsersSGLoader(LinoMdbLoader):
    """
    Converts rows from TBASSG to User instances.
    """
    table_name = 'TBASSG'
    model = User
    headers = u"""
    IDASSSG TitreASSSG NomASSSG PrenomASSSG CodeASSSG TelASSSG StatutASSSG
    """.split()
    
    def row2obj(self,row):
        pk = int(row['IDASSSG'])
        kw = {}
        kw.update(id=pk)
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


class UsersISPLoader(LinoMdbLoader):
    table_name = 'TBASISP'
    model = User
    headers = u"""
    IDASISP TitreASISP NomASISP PrenomASISP CodeASISP Tel StatutASISP
    """.split()
    
    def row2obj(self,row):
        pk = int(row['IDASISP'])
        kw = {}
        kw.update(id=pk+OFFSET_USER_ISP)
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






class JobProviderLoader(LinoMdbLoader):
    table_name = 'TBEndroitMiseAuTravail'
    
    model = jobs.JobProvider
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
        title=row['Titre']
        if not title in ("Monsieur","Madame"):
            kw.update(title=title)
        if row['Nom']:
            kw.update(last_name=row['Nom'])
        else:
            kw.update(last_name="?")
            
        kw.update(sex=row['Sexe'])
        
        #~ sex = row['Sexe']
        #~ if sex == "M"
            #~ kw.update(sex='M')
        #~ elif sex == "F"
            #~ kw.update(sex='F')
        #~ else:
            #~ kw.update(sex='M')            
        kw.update(first_name=row[u'Prénom'])
        kw.update(street_prefix=row[u'Rue'])
        kw.update(street=row[u'Adresse'])
        kw.update(street_no=row[u'Numero'])
        kw.update(street_box=row[u'Boite'])
        kw.update(gesdos_id=row[u'NumeroDossier'])
        kw.update(phone=row[u'Tel1'])
        kw.update(gsm=row[u'GSM1'])
        
        kw.update(birth_country_id=pays2iso(row[u'IDPays']))
        kw.update(nationality_id=nation2iso(row[u'IDNationalite']))
        kw.update(national_id=row[u'NumeroNational'])
        
        kw.update(coach1=get_by_id(User,row[u'IDASISP'],OFFSET_USER_ISP))
        kw.update(coach2=get_by_id(User,row[u'IDASSSG']))
        
        #~ kw.update(coach1=code2user(row[u'IDASISP'],OFFSET_USER_ISP))
        #~ kw.update(coach2=code2user(row[u'IDASSSG']))
            
        kw.update(group=phase2group(row[u'Phase']))
            
        city_id = row[u'IDCommuneCodePostal']
        if city_id:
            city_id = int(city_id)
            kw.update(city_id =city_id)
            
        if is_valid_email(row[u'Email']):
            kw.update(email=row[u'Email'])
        if row[u'DateNaissance']:
            kw.update(birth_date=row[u'DateNaissance'])
        if row[u'DateArrivee']:
            kw.update(coached_from=row[u'DateArrivee'])
        kw.update(remarks="""
        Tel2 : %(Tel2)s
        GSM2 : %(GSM2)s
        Remarques : %(Remarques)s
        """ % row)
        yield self.model(**kw)
        


class JobLoader(LinoMdbLoader):
    table_name = 'TbRechercheProfil'
    model = jobs.Job
    headers = u"""IDRechercheProfil 
    DateOuvertureSelection DateClotureSelection 
    DateDebutContrat 
    IDEndroitMiseAuTravail IdQualification 
    IDDetailFonction DescriptionDeFonction 
    HorairesDeTravail ProfilDemande Encadrement 
    OffreSpecifique Commentaires GestionArt60 
    StatutPoste""".split()
    def row2obj(self,row):
        kw = {}
        kw.update(id=int(row['IDTypeMiseEmplois']))
        kw.update(name=row['TypeMiseEmplois'])
        yield self.model(**kw)
    
    
SECTORS = dict()

class ListeFonctionLoader(LinoMdbLoader):
    table_name = 'CboListeFonction'
    model = jobs.Sector
    headers = u"""IdQualification Qualification Code filtre DetailFonction""".split()
    def row2obj(self,row):
        kw = {}
        kw.update(id=int(row['IdQualification']))
        kw.update(name=row['Qualification'])
        kw.update(remark=row['DetailFonction'])
        obj = self.model(**kw)
        SECTORS[row['Code']] = obj
        yield obj
    
class DetailFonctionsLoader(LinoMdbLoader):
    table_name = 'CboDetailFonction'
    model = jobs.Function
    headers = u"""IDDetailFonction DetailFonction Code Secteur""".split()
    def row2obj(self,row):
        kw = {}
        kw.update(id=int(row['IDDetailFonction']))
        kw.update(name='(' + row['Code'] + ') ' + row['DetailFonction'])
        kw.update(sector=SECTORS.get(row['Code']))
        yield self.model(**kw)
    
class JobsContractTypeLoader(LinoMdbLoader):
    table_name = 'CboTypeMiseEmplois'
    model = jobs.ContractType
    headers = u"""IDTypeMiseEmplois TypeMiseEmplois""".split()
    def row2obj(self,row):
        kw = {}
        kw.update(id=int(row['IDTypeMiseEmplois']))
        kw.update(name=row['TypeMiseEmplois'])
        yield self.model(**kw)
    
class CboSubsideLoader(LinoMdbLoader):
    table_name = 'CboSubside'
    model = jobs.JobType
    headers = u"""IDSubside TypeSubside article""".split()
    def row2obj(self,row):
        kw = {}
        kw.update(id=int(row['IDSubside']))
        kw.update(name=row['TypeSubside'])
        kw.update(remark=row['article'])
        yield self.model(**kw)
    
class IsipContractTypeLoader(LinoMdbLoader):
    table_name = 'CboTypeContrat'
    model = isip.ContractType
    headers = u"""IDTypeContrat TypeContratCPAS""".split()
    def row2obj(self,row):
        kw = {}
        kw.update(id=int(row['IDTypeContrat']))
        kw.update(name=row['TypeContratCPAS'])
        yield self.model(**kw)
    
class TBMiseEmploisLoader(LinoMdbLoader):
    table_name = 'TBMiseEmplois'
    #~ model = jobs.Contract
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
        dblogger.info("statut = %s",row['Statut'])

        kw = {}
        kw.update(id=int(row['IDMiseEmplois']))
        
        job = None
        
        function = get_by_id(jobs.Function,row['IDDetailFonction'])
        sector = get_by_id(jobs.Sector,row['IdQualification'])
        person = get_by_id(Person,row[u'IDClient'],OFFSET_PERSON)
        provider = get_by_id(jobs.JobProvider,row[u'IDEndroitMiseAuTravail'],OFFSET_JOBPROVIDER)
        ct = get_by_id(jobs.ContractType,row['IDTypeMiseEmplois'])
        if not ct:
            dblogger.warning("Ignored TBMiseEmplois %s : no contract type",kw)
        else:
            jt = get_by_id(jobs.JobType,row['IDSubside'])
            if not jt:
                dblogger.warning("Ignored TBMiseEmplois %s : no job type",kw)
            job = get_or_create_job(provider,ct,jt,sector,function)
        
        if job:
            #~ qual = get_by_id(properties.Property,row['IdQualification'])
            #~ kw.update(qual=qual)
            statut = row['Statut']
            if statut in (u'En Attente',u'En Cours',u'Terminé'):
                kw.update(applies_from=self.parsedate(row[u'DebutContrat']))
                kw.update(applies_until=self.parsedate(row[u'FinContrat']))
                kw.update(type=ct)
                kw.update(job=job)
                kw.update(provider=provider)
                kw.update(person=person)
                yield jobs.Contract(**kw)
            else:
                kw.update(statut=statut)
                dblogger.warning("Ignored TBMiseEmplois %s : unknown statut",kw)
                yield jobs.Contract(**kw)
          
        

class ContractVSELoader(LinoMdbLoader):
    table_name = 'TBTypeDeContratCPAS'
    model = isip.Contract
    headers = u"""
    IDTypeDeContratCPAS IDTypeContrat DateDebut DateFin 
    ASCPAS ASISP Statut Evaluation IDClient DateSignature 
    TypePIIS NiveauEtude
    """.split()
    
    def row2obj(self,row):
        kw = {}
        kw.update(id=int(row['IDTypeDeContratCPAS']))
        #~ ctype = int(row['IDTypeContrat']) 
        #~ if ctype:
            #~ kw.update(type=ContractType.objects.get(pk=ctype+ OFFSET_CONTRACT_TYPE_CPAS))
        kw.update(applies_from=self.parsedate(row[u'DateDebut']))
        kw.update(applies_until=self.parsedate(row[u'DateFin']))
        kw.update(person=get_by_id(Person,row[u'IDClient'],OFFSET_PERSON))
        
        ct = get_by_id(isip.ContractType,row['IDTypeContrat'])
        kw.update(type=ct)
        if not ct:
            dblogger.warning("Ignored TBTypeDeContratCPAS %s",kw)
        else:
            yield self.model(**kw)

def objects():
  
    if not settings.LINO.legacy_data_path:
        raise Exception("You must specify the name of your .mdb file in settings.LINO.legacy_data_path!")
  
    phin = Instantiator('dsbe.PersonGroup','name').build
    yield phin('1')
    yield phin('2')
    yield phin('3')
    yield phin('4')
    yield phin('4b')
    #~ User = resolve_model('users.User')
    yield User(username="root",is_staff=True,is_expert=True,is_superuser=True,first_name="Root",last_name="Superuser")
    #~ for o in PersonLoader().load(): yield o
    #~ for k,v in CboTypeMiseEmplois.items():
        #~ yield ContractType(id=k,name=v)
    #~ for k,v in CboTypeContrat.items():
        #~ yield ContractType(id=k+OFFSET_CONTRACT_TYPE_CPAS,name=v)
    yield UsersSGLoader()
    yield UsersISPLoader()
    yield CboSubsideLoader()
    yield ListeFonctionLoader()
    yield DetailFonctionsLoader()
    yield CityLoader()
    yield PersonLoader()
    yield JobProviderLoader()
    yield JobsContractTypeLoader()
    yield IsipContractTypeLoader()
    yield TBMiseEmploisLoader()
    yield ContractVSELoader()
    yield NotesLoader()
    
    #~ reader = csv.reader(open(,'rb'))