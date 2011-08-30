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

CboNationalite = {
  1:"BE",
  2:"Congolais(e)",
  3:"Russe",
  4:"Rwandaise",
  5:"Chilien(ne)",
  6:"FR",
  7:"Roumain(e)",
  8:"CH",
  9:"Colombien(ne)",
  11:"Uruguayen (ne)",
  12:"Marocain(ne)",
  14:u"Algérien(ne)",
  15:"Mauricien(ne)",
  16:"Togolais(e)",
  17:u"Réfugié Politique",
  18:"Turque",
  19:"Camerounai (se)",
  20:"Perouvien(ne)",
  21:"Moldave(iene)",
  23:"burundais(e)",
  24:"Sierra Leonais(e)",
  25:"Mauritanien(ne)",
  26:u"Brésilien(ne)",
  27:"Portugais(e)",
  28:"libanais(e)",
  29:"DE",
  30:"syrien(ne)",
  31:"Guinéen(ne)",
  32:u"Libérien(ne)",
  33:"tunisienne",
  34:"Nigérian(nes)",
  35:u"ouzbékistan",
  36:"bolivien(ne)",
  37:"polonais(e)",
  38:u"sénégalais(e)",
  39:"Iranien(ne)",
  40:"Iraquien(ne)",
  41:"arménie",
  42:"Italien(ne)",
  43:"angolien(ne)",
  44:"Nigerien(ne)",
  45:"Chinnoise",
  46:"burkina Faso",
  48:"laotienne",
  49:"ivoirien(ne)",
  50:u"US",
  51:"georgien(ne)",
  52:"grec",
  53:"yougoslave",
  54:u"bosnie-herzégovine",
  55:"Ukrainien(ne)",
  56:"Equatorien",
  57:"pakistannais(e)",
  58:"vietnamien(ne)",
  59:u"indonésien(ne)",
  60:"Malgache",
  62:"indien(ne)",
  63:"albanais",
  64:"Espagnol(e)",
  65:"Macedoine",
  66:"Djiboutien(ne)",
  68:"egyptien(ne)",
  69:"NL",
  70:"Kazakhstan",
  71:"Somalien(ne)",
  72:"Afghane",
  73:"Cubaine",
  74:"tchad",
  75:"Royaume-Uni",
  76:"lituanienne ",
  77:"kirghizistan",
  78:"Ethiopie",
}

CboPays = {
  1:u"Afrique du Sud"
  ,2:u"Albanie"
  ,3:u"Algérie"
  ,4:'DE' # u"Allemagne"
  ,5:u"Andorre"
  ,6:u"Angola"
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
  ,28:u"Brésil"
  ,29:u"Brunei"
  ,30:u"Bulgarie"
  ,31:u"Burkina"
  ,32:u"Burundi"
  ,33:u"Cambodge"
  ,34:u"Cameroun"
  ,35:u"Canada"
  ,36:u"Cap-Vert"
  ,37:u"Chili"
  ,38:'CN' # u"Chine"
  ,39:u"Chypre"
  ,40:u"Colombie"
  ,41:u"Comores"
  ,42:u"Congo"
  ,44:u"Cook (les īles)"
  ,45:u"Corée du Nord"
  ,46:u"Corée du Sud"
  ,47:u"Costa Rica"
  ,48:u"Cōte d'Ivoire"
  ,49:u"Croatie"
  ,50:u"Cuba"
  ,51:'DK' # u"Danemark"
  ,52:u"République de Djibouti"
  ,53:u"Dominique"
  ,54:u"Egypte"
  ,55:u"Émirats arabes unis"
  ,56:u"Equateur"
  ,57:u"Erythrée"
  ,58:u"Espagne"
  ,59:u"Estonie"
  ,60:'US' # u"Etats-Unis"
  ,61:u"Ethiopie"
  ,62:u"Fidji"
  ,63:'FI' # u"Finlande"
  ,64:'FR' # u"France"
  ,65:u"Gabon"
  ,66:u"Gambie"
  ,67:u"Géorgie"
  ,68:u"Ghana"
  ,69:u"Grčce"
  ,70:u"Grenade"
  ,71:u"Guatemala"
  ,72:u"Guinée"
  ,73:u"Guinée-Bissao"
  ,74:u"Guinée équatoriale"
  ,75:u"Guyana"
  ,76:u"Haļti"
  ,77:u"Honduras"
  ,78:u"Hongrie"
  ,79:u"Inde"
  ,80:u"Indonésie"
  ,81:u"Iran"
  ,82:u"Iraq"
  ,83:u"Irlande"
  ,84:u"Islande"
  ,85:u"Israėl"
  ,86:u"Italie"
  ,87:u"Jamaļque"
  ,88:u"Japon"
  ,89:u"Jordanie"
  ,90:u"Kazakhstan"
  ,91:u"Kenya"
  ,92:u"Kirghizistan"
  ,93:u"Kiribati"
  ,94:u"Koweļt"
  ,95:u"Laos"
  ,96:u"Lesotho"
  ,97:u"Lettonie"
  ,98:u"Liban"
  ,99:u"Libéria"
  ,100:u"Libye"
  ,101:u"Liechtenstein"
  ,102:u"Lituanie"
  ,103:u"Luxembourg"
  ,104:u"Macédoine"
  ,105:u"Madagascar"
  ,106:u"Malaisie"
  ,107:u"Malawi"
  ,108:u"Maldives"
  ,109:u"Mali"
  ,110:u"Malte"
  ,111:u"Maroc"
  ,112:u"Marshall"
  ,113:u"Maurice"
  ,114:u"Mauritanie"
  ,115:u"Mexique"
  ,116:u"Micronésie"
  ,117:u"Moldavie"
  ,118:u"Monaco"
  ,119:u"Mongolie"
  ,120:u"Mozambique"
  ,121:u"Namibie"
  ,122:u"Nauru"
  ,123:u"Népal"
  ,124:u"Nicaragua"
  ,125:u"Niger"
  ,126:u"Nigeria"
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
  ,137:u"Pays-Bas"
  ,138:u"Pérou"
  ,139:u"Philippines"
  ,140:u"Pologne"
  ,141:u"Portugal"
  ,142:u"Qatar"
  ,143:u"République centrafricaine"
  ,144:u"République dominicaine"
  ,145:u"République tchčque"
  ,146:u"Roumanie"
  ,147:u"Royaume-Uni"
  ,148:'RU' # u"Russie"
  ,149:u"Rwanda"
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
  ,171:u"Syrie"
  ,172:u"Tadjikistan"
  ,173:u"Tanzanie"
  ,174:u"Tchad"
  ,175:u"Thaļlande"
  ,176:u"Togo"
  ,177:u"Tonga"
  ,178:u"Trinité-et-Tobago"
  ,179:u"Tunisie"
  ,180:u"Turkménistan"
  ,181:u"Turquie"
  ,182:u"Tuvalu"
  ,183:u"Ukraine"
  ,184:u"Uruguay"
  ,185:u"Vanuatu"
  ,186:u"Venezuela"
  ,187:u"Viźt Nam"
  ,188:u"Yémen"
  ,189:u"Yougoslavie"
  ,190:u"Zaļre"
  ,191:u"Zambie"
  ,192:u"Zimbabwe"
  ,193:u"Afghanistan"
  ,194:u"Uzbekistan"
}


def k2iso(dd,k,ddname):
    country_id = dd.get(int(k))
    if country_id is None:
        dblogger.warning("Unkown %s id %s",ddname,k)
    if len(country_id) == 2:
        return country_id
    dblogger.warning("Unkown %s code %s -> %r",ddname,k,country_id)
        
def nation2iso(k): return k2iso(CboNationalite,k,'CboNationalite')
def pays2iso(k):return k2iso(CboPays,k,'CboPays')
  


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
        #~ u = User.objects.row[u'IDASISPClient']
        #~ kw.update(coach1=u)
            
        city_id = int(row[u'IDCommuneCodePostal'])
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
        """ % row)
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