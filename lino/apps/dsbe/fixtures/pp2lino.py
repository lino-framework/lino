# -*- coding: UTF-8 -*-
## Copyright 2009-2011 Luc Saffre
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

It uses `mdb-export` to extract data from the .mdb file to .csv, 
then reads these csv files. 
`mdb-export` was written by Brian Bruns and is part 
of the `mdbtools` Debian package. To install it::

  aptitude install mdbtools
  
Usage of `mdbtools` command line::

  Usage: mdb-export [options] <file> <table>
  where options are:
    -H             supress header row
    -Q             don't wrap text-like fields in quotes
    -d <delimiter> specify a column delimiter
    -R <delimiter> specify a row delimiter
    -I             INSERT statements (instead of CSV)
    -D <format>    set the date format (see strftime(3) for details)
    -S             Sanitize names (replace spaces etc. with underscore)
    -q <char>      Use <char> to wrap text-like fields. Default is ".
    -X <char>      Use <char> to escape quoted characters within a field. Default is doubling.
    
Before loading this fixture you must set :attr:`lino.Lino.legacy_data_path` 
in your local :xfile:`settings.py`.
You must also set the encoding for mdb-export::

    export MDB_ICONV=utf-8
    export MDB_JET_CHARSET=utf-8
    
Then load the fixture using a variant of the following command::

    python manage.py initdb std all_countries all_cities be all_languages props pp2lino

Thanks to Google and http://farismadi.wordpress.com/2008/07/13/encoding-of-mdb-tool/ 
for explanations on the environment variables used by `mdb-export`.

The function :func:`check_output` in this module is a copy from Python 2.7 
which we include here to make it usable in Python 2.6 too.


"""

#~ ENCODING = 'latin1' # the encoding used by the mdb file
ENCODING = 'utf8' 
#~ MDB_FILE = 'PPv5MasterCopie.mdb'
MDBTOOLS_EXPORT = 'mdb-export'

import sys
#~ ENCODING = sys.stdout.encoding
#~ import csv
import codecs

from django.conf import settings

from lino.utils import ucsv
#~ from lino.utils import dblogger
from lino.tools import resolve_model

from lino.apps.dsbe.models import Person    
from lino.modlib.users.models import User
#~ from lino.modlib.jobs.models import Job, JobProvider, Contract, ContractType
from lino.modlib.jobs.models import Job, Contract, JobProvider, \
  ContractEnding, ExamPolicy, ContractType, Company



try:
  from subprocess import check_output
except ImportError:
    import subprocess
    
    def check_output(*popenargs, **kwargs):
        r"""Run command with arguments and return its output as a byte string.

        If the exit code was non-zero it raises a CalledProcessError.  The
        CalledProcessError object will have the return code in the returncode
        attribute and output in the output attribute.

        The arguments are the same as for the Popen constructor.  Example:

        >>> check_output(["ls", "-l", "/dev/null"])
        'crw-rw-rw- 1 root root 1, 3 Oct 18  2007 /dev/null\n'

        The stdout argument is not allowed as it is used internally.
        To capture standard error in the result, use stderr=STDOUT.

        >>> check_output(["/bin/sh", "-c",
        ...               "ls -l non_existent_file ; exit 0"],
        ...              stderr=STDOUT)
        'ls: non_existent_file: No such file or directory\n'
        """
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd, output=output)
        return output


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
    

class Loader:
    table_name = None
    model = None
    
    def load(self):
        mdb_file = settings.LINO.legacy_data_path
        if not mdb_file:
            raise Exception("Must specify settings.LINO.legacy_data_path!")
        args = [MDBTOOLS_EXPORT, '-D', '%Y-%m-%d', mdb_file, self.table_name]
        s = check_output(args,executable=MDBTOOLS_EXPORT,
          env=dict(
            MDB_ICONV='utf-8',
            MDB_JET_CHARSET='utf-8'))
        #~ print ENCODING
        
        fn = self.table_name+".csv"
        fd = open(fn,'w')
        fd.write(s)
        fd.close()
        print "Wrote file", fn
        reader = ucsv.UnicodeReader(open(fn,'r'),encoding=ENCODING)
        headers = reader.next()
        if not headers == self.headers:
            raise Exception("%r != %r" % (headers,self.headers))
        n = 0
        for values in reader:
            row = {}
            for i,h in enumerate(self.headers):
                row[h] = values[i]
            n += 1
            if False:
                if int(row['IDClient']) == 967:
                    print row
                    raise Exception("20110609")
                  
            if False:
                if n < 10:
                    print n, ':', row
                else:
                    raise Exception("20110609")
            for obj in self.row2obj(row):
                yield obj

OFFSET_JOBPROVIDER = 3000

COMPANY_TYPES = {
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



class JobProviderLoader(Loader):
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
        companyType=COMPANY_TYPES.get(row['IDStatutJuridique'],None)
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
    

OFFSET_PERSON = 1000

class PersonLoader(Loader):
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
            name = 'Job%s(intern)' % contract_type_id
        else:
            name = 'Job%s@%s' % (contract_type_id,provider)
        job = Job(
            provider=provider,
            contract_type_id=contract_type_id,
            name=name
            )
        job.save()
        return job





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

class ContractArt60Loader(Loader):
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
        kw.update(applies_from=row[u'DebutContrat'])
        kw.update(applies_until=row[u'FinContrat'])
        provider_id = int(row[u'IDEndroitMiseAuTravail'])+OFFSET_JOBPROVIDER
        contract_type_id = row['IDTypeMiseEmplois']
        kw.update(job=get_or_create_job(provider_id,contract_type_id))
        #~ kw.update(provider=JobProvider.objects.get(id=))
        kw.update(person=Person.objects.get(id=int(row[u'IDClient'])+OFFSET_PERSON))
        yield self.model(**kw)

OFFSET_CONTRACT_TYPE_CPAS = 100

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

class ContractVSELoader(Loader):
    table_name = 'TBTypeDeContratCPAS'
    model = Contract
    headers = u"""
    IDTypeDeContratCPAS IDTypeContrat DateDebut DateFin ASCPAS ASISP Statut Evaluation IDClient DateSignature TypePIIS NiveauEtude
    """.split()
    
    def row2obj(self,row):
        kw = {}
        kw.update(id=int(row['IDTypeDeContratCPAS']))
        #~ ctype = int(row['IDTypeContrat']) 
        #~ if ctype:
            #~ kw.update(type=ContractType.objects.get(pk=ctype+ OFFSET_CONTRACT_TYPE_CPAS))
        kw.update(applies_from=row[u'DateDebut'])
        kw.update(applies_until=row[u'DateFin'])
        
        contract_type_id = row['IDTypeContrat']
        kw.update(job=get_or_create_job(None,contract_type_id))
        
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
    yield PersonLoader().load()
    yield JobProviderLoader().load()
    yield ContractArt60Loader().load()
    
    #~ reader = csv.reader(open(,'rb'))