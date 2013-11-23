# -*- coding: UTF-8 -*-
## Copyright 2009-2013 Luc Saffre
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
## along with Lino ; if not, see <http://www.gnu.org/licenses/>.

"""

Import legacy data from TIM.
:setting:`legacy_data_path` must point to the TIM data path, e.g.::

  legacy_data_path = '~/vbshared2/drives/L/backup/data/privat'

"""
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


GET_THEM_ALL = True

import os
import datetime
from decimal import Decimal
#~ from lino.utils.quantities import Duration

from dateutil import parser as dateparser

from django.conf import settings
from django.core.exceptions import ValidationError

from lino.utils import dbfreader
from lino.utils import dblogger
from north import dpy

from lino.modlib.accounts.utils import AccountTypes

from lino.core.dbutils import resolve_model, obj2str
from lino.core.dbutils import is_valid_email

from lino import dd

Activity = resolve_model('pcsw.Activity')
Country = resolve_model('countries.Country')
City = resolve_model('countries.City')
Household = resolve_model('households.Household')
Person = resolve_model("contacts.Person")
Company = resolve_model("contacts.Company")
Account = dd.resolve_model('accounts.Account')
Group = dd.resolve_model('accounts.Group')

from lino.runtime import *

if True:
    users = dd.resolve_app('users')
    tickets = dd.resolve_app('tickets')
    households = dd.resolve_app('households')
    vat = dd.resolve_app('vat')
    sales = dd.resolve_app('sales')
    ledger = dd.resolve_app('ledger')
    accounts = dd.resolve_app('accounts')
    products = dd.resolve_app('products')
    contacts = dd.resolve_app('contacts')
    finan = dd.resolve_app('finan')

def dbfmemo(s):
    s = s.replace('\r\n','\n')
    s = s.replace(u'\xec\n','')
    #~ s = s.replace(u'\r\nì',' ')
    if u'ì' in s:
        raise Exception("20121121 %r" % s)
    return s.strip()

#~ def convert_username(name):
    #~ return name.lower()

from lino.modlib.vat.models import VatClasses

def tax2vat(idtax):
    idtax = idtax.strip()
    if idtax == 'D20':
        return VatClasses.normal
    elif idtax == 'D18':
        return VatClasses.normal
    elif idtax == '0':
        return VatClasses.exempt
    elif idtax == 'IS':
        return VatClasses.normal
    elif idtax == 'XS':
        return VatClasses.normal
    else:
        return VatClasses.normal
    raise Exception("Unknown VNl->IdTax %r" % idtax)

def pcmn2type(idgen):
    if idgen[0] == '6':
        return AccountTypes.expenses
    if idgen[0] == '7':
        return AccountTypes.incomes
    if idgen[0] == '4':
        return AccountTypes.liabilities
    return AccountTypes.assets

def tim2bool(x):
    if not x.strip():
        return False
    return True

def convert_gender(v):
    if v in ('W','F'): return 'F'
    if v == 'M': return 'M'
    return None

def mton(s): # PriceField
    #~ return s.strip()
    s = s.strip()
    if s:
        if s != "GRATIS":
            return Decimal(s)
    return Decimal()

def qton(s): # QuantityField
    return s.strip()
    #~ s = s.strip()
    #~ if s:
        #~ if ':' in s: return Duration(s)
        #~ if s.endswith('%'):
            #~ return Decimal(s[:-1]) / 100
        #~ return Decimal(s)
    #~ return None

def isolang(x):
    if x == 'K' : return 'et'
    if x == 'E' : return 'en'
    if x == 'D' : return 'de'
    if x == 'F' : return 'fr'
    #~ if x == 'N' : return 'nl'

def store_date(row,obj,rowattr,objattr):
    v = row[rowattr]
    if v:
        if isinstance(v,basestring):
            v = dateparser.parse(v)
        setattr(obj,objattr,v)

def row2jnl(row):
    year = ledger.FiscalYears.from_int(2000 + int(row.iddoc[:2]))
    num = int(row.iddoc[2:])
    # if row.idjnl in ('VKR','EKR'):
    try:
        jnl = ledger.Journal.objects.get(ref=row.idjnl)
        #~ cl = sales.Invoice
        return jnl,year,num
    except ledger.Journal.DoesNotExist:
        return None,None,None
        
def get_customer(pk):
    return contacts.Partner.objects.get(pk=pk)
    #~ try:
        #~ return sales.Customer.objects.get(pk=pk)
    #~ except sales.Customer.DoesNotExist:
        #~ obj = mti.create_child(contacts.Partner,pk,sales.Customer)
        #~ obj.save()
        #~ return sales.Customer.objects.get(pk=pk)

def ticket_state(idpns):
    if idpns == ' ':
        return tickets.TicketStates.accepted
    if idpns == 'A':
        return tickets.TicketStates.waiting
    if idpns == 'C':
        return tickets.TicketStates.closed
    if idpns == 'X':
        return tickets.TicketStates.cancelled
    return None # 20120829 tickets.TicketStates.blank_item
     
#~ def country2kw(row,kw):
    
        
def try_full_clean(i):
    while True:
        try:
            i.full_clean()
        except ValidationError as e:
            if not hasattr(e, 'message_dict'):
                raise
            for k in e.message_dict.keys():
                fld = i._meta.get_field(k)
                v = getattr(i, k)
                setattr(i, k, fld.default)
                dblogger.warning(
                    "%s : ignoring value %r for %s : %s", 
                    obj2str(i), v, k, e)
        return


class TimLoader(object):

    use_dbf_py = False
    """
    `True` means to use Ethan Furman's 
    `dbf <http://pypi.python.org/pypi/dbf/>`_ package
    to read the file,
    False means to use :mod:`lino.utils.dbfreader`.
    Set it to True when reading data from a TIM with FOXPRO DBE, 
    False when reading DBFNTX files. 
    
    """
    
    LEN_IDGEN = 6
    
    table_ext = '.FOX'
    
    archived_tables = set()
    archive_name = None
    languages = None
    codepage = 'cp850'
    #~ codepage = 'cp437'
    #etat_registered = "C"¹
    etat_registered = "¹"
    
    def __init__(self,dbpath):
        self.dbpath = dbpath
        self.VENDICT = dict()
        self.FINDICT = dict()
        self.sales_gen2art = dict()
        self.GROUPS = dict()
        self.languages = settings.SITE.resolve_languages(self.languages)
        self.must_register = []
        
    def get_user(self,idusr=None):
        return self.ROOT
        
    def par_class(self, data):
        # wer eine nationalregisternummer hat ist eine Person, selbst wenn er auch eine MWst-Nummer hat.
        prt = data.idprt
        if prt == 'O':
            return Company
        elif prt == 'P':
            return Person
        elif prt == 'F':
            return Household
        #~ dblogger.warning("Unhandled PAR->IdPrt %r",prt)


    def dc2lino(self,dc):
        if dc == "D":
            return accounts.DEBIT
        elif dc == "C":
            return accounts.CREDIT
        raise Exception("Invalid D/C value %r" % dc)

    def par_pk(self,pk):
        if pk.startswith('T'):
            return 2500 + int(pk[1:]) - 256
        else:
            return int(pk)

    def store(self,kw,**d):
        for k,v in d.items():
            if v is not None:
                if isinstance(v,basestring):
                    v = self.decode_string(v).strip()
            #~ if v:
                kw[k] = v

    def short2iso(self,s):
        if s == 'B': return 'BE'
        if s == 'D': return 'DE'
        if s == 'F': return 'FR'
        if s == 'L': return 'LU'
        if s == 'E': return 'ES'
        if s == 'I': return 'IT'
        if s == 'USA': return 'US'
        if s == 'VIE': return ''
        return s
        #~ if s == 'AU': return 'AU'
        #~ if s == 'NL': return 'NL'
        #~ raise Exception("Unknown short country code %r" % s)


    def load_dbf(self,tableName,row2obj=None):
        if row2obj is None:
            row2obj = getattr(self,'load_'+tableName[-3:].lower())
        fn = self.dbpath
        if self.archive_name is not None:
            if tableName in self.archived_tables:
                fn = os.path.join(fn,self.archive_name)
        fn = os.path.join(fn,tableName)
        fn += self.table_ext
        if self.use_dbf_py:
            dblogger.info("Loading %s...", fn)
            import dbf  # http://pypi.python.org/pypi/dbf/
            #~ table = dbf.Table(fn)
            table = dbf.Table(fn, codepage=self.codepage)
            #~ table.use_deleted = False
            table.open()
            #~ print table.structure()
            dblogger.info("Loading %d records from %s (%s)...",
                          len(table), fn, table.codepage)
            for record in table:
                if not dbf.is_deleted(record):
                    i = row2obj(record)
                    if i is not None:
                        yield settings.TIM2LINO_LOCAL(tableName, i)
            table.close()
        else:
            f = dbfreader.DBFFile(fn,codepage="cp850")
            dblogger.info("Loading %d records from %s...",len(f),fn)
            f.open()
            for dbfrow in f:
                i = row2obj(dbfrow)
                if i is not None:
                    yield settings.TIM2LINO_LOCAL(tableName,i)
            f.close()
            
        self.after_load(tableName)
            
            
    def load_gen2group(self,row,**kw):
        idgen = row.idgen.strip()
        if not idgen: return
        if len(idgen) < self.LEN_IDGEN:
            #~ dclsel = row.dclsel.strip()
            #~ kw.update(chart=accounts.Chart.objects.get(pk=1))
            kw.update(chart=self.CHART)
            kw.update(ref=idgen)
            kw.update(account_type=pcmn2type(idgen))
            self.babel2kw('libell','name',row,kw)
            #~ def names2kw(kw,*names):
                #~ names = [n.strip() for n in names]
                #~ kw.update(name=names[0])
            #~ names2kw(kw,row.libell1,row.libell2,row.libell3,row.libell4)
            """TIM accepts empty GEN->Libell fields. In that 
            case we take the ref as name.
            """
            kw.setdefault('name',idgen)
            ag = accounts.Group(**kw)
            self.GROUPS[idgen] = ag
            yield ag
        
    def load_gen2account(self,row,**kw):
        idgen = row.idgen.strip()
        if not idgen: return
        if len(idgen) == self.LEN_IDGEN:
            ag = None
            for length in range(len(idgen),0,-1):
                #~ print idgen[:length]
                ag = self.GROUPS.get(idgen[:length])
                if ag is not None:
                    break
            #~ dclsel = row.dclsel.strip()
            #~ kw.update(chart=accounts.Chart.objects.get(pk=1))
            kw.update(ref=idgen)
            kw.update(group=ag)
            kw.update(chart=self.CHART)
            kw.update(type=pcmn2type(idgen))
            self.babel2kw('libell','name',row,kw)
            #~ def names2kw(kw,*names):
                #~ names = [n.strip() for n in names]
                #~ kw.update(name=names[0])
            #~ names2kw(kw,row.libell1,row.libell2,row.libell3,row.libell4)
            obj = accounts.Account(**kw)
            #~ if idgen == "612410": 
                #~ raise Exception(20131116)
            #~ logger.info("20131116 %s",dd.obj2str(obj))
            #~ logger.info("20131116 ACCOUNT %s ",obj)
            yield obj

    def load_jnl(self, row, **kw):
        vcl = None
        kw.update(ref=row.idjnl,name=row.libell)
        kw.update(chart=self.CHART)
        kw.update(dc=self.dc2lino(row.dc))
        if row.alias == 'VEN':
            if row.idctr == 'V':
                kw.update(trade_type=vat.TradeTypes.sales)
                vcl = sales.Invoice
            elif row.idctr == 'E':
                kw.update(trade_type=vat.TradeTypes.purchases)
                vcl = ledger.AccountInvoice
        elif row.alias == 'FIN':
            idgen = row.idgen.strip()
            if idgen:
                kw.update(account=self.CHART.get_account_by_ref(idgen))
                if idgen.startswith('58'):
                    kw.update(trade_type=vat.TradeTypes.purchases)
                    vcl = finan.PaymentOrder
                elif idgen.startswith('5'):
                    vcl = finan.BankStatement
            else:
                vcl = finan.JournalEntry
        if vcl is None:
            raise Exception("Journal not recognized: %s" % row.idjnl)

        return vcl.create_journal(**kw)

    def load_fin(self, row, **kw):
        jnl, year, number = row2jnl(row)
        if jnl is None:
            raise Exception("No journal for FIN record %s" % row)
        kw.update(year=year)
        kw.update(number=number)
        #~ kw.update(id=pk)
        kw.update(date=row.date)
        kw.update(user=self.get_user())
        kw.update(balance1=mton(row.mont1))
        kw.update(balance2=mton(row.mont2))
        doc = jnl.create_voucher(**kw)
        self.FINDICT[(jnl, year, number)] = doc
        # print row.etat
        if row.etat == self.etat_registered:
            self.must_register.append(doc)
        return doc
        
    def load_fnl(self, row, **kw):
        jnl, year, number = row2jnl(row)
        if jnl is None:
            raise Exception("No journal for FNL record %s" % row)
        doc = self.FINDICT.get((jnl, year, number))
        if doc is None:
            raise Exception("FNL %r without document" %
                            list(jnl,year,number))
        kw.update(seqno=int(row.line.strip()))
        kw.update(date=row.date)
        kw.update(match=row.match.strip())
        if row.idctr == ('V'):
            kw.update(partner_id=self.par_pk(row.idcpt.strip()))
            kw.update(
                account=vat.TradeTypes.sales.get_partner_account())
        elif row.idctr == ('E'):
            kw.update(partner_id=self.par_pk(row.idcpt.strip()))
            kw.update(
                account=vat.TradeTypes.purchases.get_partner_account())
        else:
            kw.update(account=accounts.Account.objects.get(
                ref=row.idcpt.strip()))
        kw.update(amount=mton(row.mont))
        kw.update(dc=self.dc2lino(row.dc))
        return doc.add_voucher_item(**kw)


    def load_ven(self,row,**kw):
        jnl,year,number = row2jnl(row)
        if jnl is None:
            return 
        kw.update(year=year)
        kw.update(number=number)
        #~ kw.update(id=pk)
        if jnl.trade_type.name == 'sales':
            partner = get_customer(self.par_pk(row.idpar))
            kw.update(partner=partner)
            kw.update(imode=self.DIM)
            if row.idprj.strip():
                kw.update(project_id=int(row.idprj.strip()))
            kw.update(discount=mton(row.remise))
        elif jnl.trade_type.name == 'purchases':
            kw.update(partner=contacts.Partner.objects.get(
                pk=self.par_pk(row.idpar)))
            #~ partner=contacts.Partner.objects.get(pk=self.par_pk(row.idpar))
        else:
            raise Exception("Unkonwn TradeType %r" % jnl.trade_type)
        kw.update(date=row.date)
        kw.update(user=self.get_user(row.auteur))
        kw.update(total_excl=mton(row.montr))
        kw.update(total_vat=mton(row.montt))
        doc = jnl.create_voucher(**kw)
        #~ doc.partner = partner
        #~ doc.full_clean()
        #~ doc.save()
        self.VENDICT[(jnl, year, number)] = doc
        if row.etat == self.etat_registered:
            self.must_register.append(doc)
        return doc
        #~ return cl(**kw)
    
    def load_vnl(self, row, **kw):
        jnl, year, number = row2jnl(row)
        if jnl is None:
            return
        doc = self.VENDICT.get((jnl, year, number))
        if doc is None:
            raise Exception("VNL %r without document" % list(jnl,year,number))
        #~ logger.info("20131116 %s %s",row.idjnl,row.iddoc)
        #~ doc = jnl.get_document(year,number)
        #~ try:
            #~ doc = jnl.get_document(year,number)
        #~ except Exception,e:
            #~ dblogger.warning(str(e))
            #~ return 
        #~ kw.update(document=doc)
        kw.update(seqno=int(row.line.strip()))
        idart = row.idart.strip()
        if isinstance(doc,sales.Invoice):
            if row.code in ('A','F'):
                if idart != '*':
                    kw.update(product=int(idart))
            elif row.code == 'G':
                a = self.vnlg2product(row)
                if a is not None:
                    kw.update(product=a)
            kw.update(unit_price=mton(row.prixu))
            kw.update(qty=qton(row.qte))
        elif isinstance(doc,ledger.AccountInvoice):
            if row.code == 'G':
                kw.update(account=idart)
        kw.update(title=row.desig.strip())
        kw.update(vat_class=tax2vat(row.idtax))
        kw.update(total_base=mton(row.cmont))
        kw.update(total_vat=mton(row.montt))
        #~ kw.update(qty=row.idtax.strip())
        #~ kw.update(qty=row.montt.strip())
        #~ kw.update(qty=row.attrib.strip())
        #~ kw.update(date=row.date)
        return doc.add_voucher_item(**kw)
            
    def vnlg2product(self, row):
        a = row.idart.strip()
        return self.sales_gen2art.get(a)
        
    # Countries already exist after initial_data, but their short_code is 
    # needed as lookup field for Cities.
    def load_nat(self, row):
        if not row['isocode'].strip(): 
            return
        try:
            country = Country.objects.get(
                isocode=row['isocode'].strip())
        except Country.DoesNotExist:
            country = Country(isocode=row['isocode'].strip())
            country.name = row['name'].strip()
        if row['idnat'].strip():
            country.short_code = row['idnat'].strip()
        return country
        
    def load_plz(self, row):
        pk = row.pays.strip()
        if not pk:
            return
        name = row.nom.strip() or row.cp.strip()
        if not name:
            return
        
        if False: # severe
            country = Country.objects.get(isocode=self.short2iso(pk))
            #~ country = Country.objects.get(short_code=pk)
        else:
            try:
                country = Country.objects.get(isocode=self.short2iso(pk))
                #~ country = Country.objects.get(short_code=pk)
            except Country.DoesNotExist,e:
                dblogger.warning("Ignored PLZ record %s" % row)
                return
        kw = dict(
            zip_code=row['cp'].strip() or '',
            name=name,
            country=country,
        )
        return City(**kw)
            
    def load_par(self, row):
        kw = {}
        # kw.update(
        #     street2kw(join_words(
        #         row['RUE'],
        #         row['RUENUM'],
        #         row['RUEBTE'])))

        self.store(kw, id=self.par_pk(row.idpar))
        
        cl = self.par_class(row)
        if cl is Company:
            cl = Company
            self.store(
                kw,
                vat_id=row['notva'].strip(),
                prefix=row['allo'].strip(),
                name=row.firme,
            )
        elif cl is Person:
            #~ cl = Person
            # kw.update(**name2kw(self.decode_string(row.firme)))
            self.store(
                kw,
                first_name=row['vorname'].strip(),
                last_name=row.firme,
                #~ birth_date=row['gebdat'],
                bank_account1=row['compte1'].strip(),
                title=row['allo'].strip(),
            )
        else:
            dblogger.warning(
                "Ignored PAR record %s (IdPrt %r)" % (
                    row.idpar, row.idprt))
            return
        language = isolang(row['langue'])
        self.store(
            kw,
            language=language,
            remarks=dbfmemo(row['memo']),
        )

        #~ country2kw(row,kw)

        country = row['pays'].strip()
        if country:
            try:
                country = Country.objects.get(
                    short_code__exact=country)
            except Country.DoesNotExist:
                country = Country(isocode=country,
                                  name=country,
                                  short_code=country)
                country.save()
            kw.update(country=country)

        self.store(
            kw,
            phone=row['tel'].strip(),
            fax=row['fax'].strip(),
            street=row['rue'].strip(),
            street_no=row['ruenum'],
            street_box=row['ruebte'].strip(),
        )

        # kw.update(street2kw(join_words(row['RUE'],
        # row['RUENUM'],row['RUEBTE'])))

        zip_code = row['cp'].strip()
        if zip_code:
            kw.update(zip_code=zip_code)
            try:
                city = City.objects.get(
                    country=country,
                    zip_code__exact=zip_code,
                  )
                kw.update(city=city)
            except City.DoesNotExist as e:
                city = City(zip_code=zip_code,
                            name=zip_code,
                            country=country)
                city.save()
                kw.update(city=city)
                #~ dblogger.warning("%s-%s : %s",row['PAYS'],row['CP'],e)
            except City.MultipleObjectsReturned as e:
                dblogger.warning("%s-%s : %s",
                                 row['pays'],
                                 row['cp'],
                                 e)

        #~ print cl,kw
        try:
            return cl(**kw)
        except Exception as e:
            dblogger.warning("Failed to instantiate %s from %s",
                             cl, kw)
            raise

    #~ PRJPAR = dict()

    def load_prj(self, row, **kw):
        pk = int(row.idprj.strip())
        kw.update(id=pk)
        if row.parent.strip():
            kw.update(parent_id=int(row.parent))
        kw.update(name=row.name1.strip())
        if row.idpar.strip():
            kw.update(partner_id=self.par_pk(row.idpar.strip()))

        kw.update(ref=row.seq.strip())
        kw.update(user=self.get_user(None))
        desc = dbfmemo(row.abstract).strip() + '\n\n' + dbfmemo(row.body)
        #~ kw.update(summary=dbfmemo(row.abstract))
        kw.update(description=desc)
        return tickets.Project(**kw)
    
    def load_pin(self, row, **kw):
        pk = int(row.idpin)
        kw.update(id=pk)
        if row.idprj.strip():
            kw.update(project_id=int(row.idprj))
            #~ kw.update(partner_id=PRJPAR.get(int(row.idprj),None))
        if row.idpar.strip():
            kw.update(partner_id=self.par_pk(row.idpar))
        kw.update(summary=row.short.strip())
        kw.update(description=dbfmemo(row.memo))
        kw.update(state=ticket_state(row.idpns))
        kw.update(closed=row.closed)
        kw.update(created=row['date'])
        kw.update(modified=datetime.datetime.now())
        kw.update(user=self.get_user(row.idusr))
        return tickets.Ticket(**kw)
    
    def load_dls(self,row,**kw):
        if not row.iddls.strip(): 
            return
        pk = int(row.iddls)
        kw.update(id=pk)
        if row.idprj.strip():
            kw.update(project_id=int(row.idprj))
            #~ kw.update(partner_id=PRJPAR.get(int(row.idprj),None))
        if row.idpar.strip():
            kw.update(partner_id=self.par_pk(row.idpar))
        kw.update(summary=row.nb.strip())
        kw.update(description=dbfmemo(row.memo))
        kw.update(date=row.date)
        kw.update(user=self.get_user(row.idusr))
        def set_time(kw,fldname,v):
            v = v.strip()
            if not v:
                return
            if v == '24:00':
                v = '0:00'
            kw[fldname] = v
            
        set_time(kw,'start_time',row.von)
        set_time(kw,'end_time',row.bis)
        set_time(kw,'break_time',row.pause)
        #~ kw.update(start_time=row.von.strip())
        #~ kw.update(end_time=row.bis.strip())
        #~ kw.update(break_time=row.pause.strip())
        kw.update(is_private=tim2bool(row.isprivat))
        obj = tickets.Session(**kw)
        #~ if row.idpar.strip():
            #~ partner_id = self.par_pk(row.idpar)
            #~ if obj.project and obj.project.partner \
                #~ and obj.project.partner.id == partner_id:
                #~ pass
            #~ elif obj.ticket and obj.ticket.partner \
                #~ and obj.ticket.partner.id == partner_id:
                #~ pass
            #~ else:
                #~ dblogger.warning("Lost DLS->IdPar of DLS#%d" % pk)
        return obj
    
    def load_art(self,row,**kw):
        try:
            pk = int(row.idart)
        except ValueError,e:
            dblogger.warning("Ignored %s: %s",row,e)
            return
        kw.update(id=pk)
        #~ def names2kw(kw,*names):
            #~ names = [n.strip() for n in names]
            #~ kw.update(name=names[0])
        #~ names2kw(kw,row.name1,row.name2,row.name3)
        self.babel2kw('name','name',row,kw)
        return products.Product(**kw)
        
        
    def decode_string(self,v):
        return v
        #~ return v.decode(self.codepage)
        
    def babel2kw(self,tim_fld,lino_fld,row,kw):
        for i,lng in enumerate(self.languages):
            v = getattr(row,tim_fld+str(i+1),'').strip()
            if v:
                v = self.decode_string(v)
                kw[lino_fld+lng.suffix] = v
        
    def after_load(self,tableName):
        pass

    def after_gen_load(self):
        kw1 = dict()
        kw1.update(clients_account='400000')
        kw1.update(suppliers_account='440000')
        kw1.update(sales_vat_account='411000')      # vat paid
        kw1.update(purchases_vat_account='451000')  # due vat
        kw1.update(sales_account='700000')
        kw1.update(purchases_account='603000')

        sc = dict()
        for k, v in kw1.items():
            sc[k] = self.CHART.get_account_by_ref(v)
        settings.SITE.site_config.update(**sc)

    def objects(tim):
        
        self = tim
        
        self.ROOT = users.User(username='root',profile='900',last_name="Root")
        self.ROOT.set_password("1234")
        yield self.ROOT
        
        settings.SITE.loading_from_dump = True
        
        self.CHART = accounts.Chart(name="Default")
        yield self.CHART
        
        
        self.DIM = sales.InvoicingMode(name='Default')
        yield self.DIM


        #yield sales.Invoice.create_journal('sales',
        #    chart=self.CHART,name="Verkaufsrechnungen",ref="VKR")
        #yield ledger.AccountInvoice.create_journal('purchases',
        #    chart=self.CHART,name="Einkaufsrechnungen",ref="EKR")

        #~ from lino.modlib.users import models as users
        
        #~ ROOT = users.User.objects.get(username='root')
        #~ DIM = sales.InvoicingMode.objects.get(name='Default')
        

        yield tim.load_dbf('GEN',self.load_gen2group)
        yield tim.load_dbf('GEN',self.load_gen2account)
        
        yield dpy.FlushDeferredObjects
        
        self.after_gen_load()
        
        yield tim.load_dbf('JNL')
        yield tim.load_dbf('ART')
        #~ yield tim.load_dbf('NAT')
        yield tim.load_dbf('PLZ')
        yield tim.load_dbf('PAR')
        yield tim.load_dbf('PRJ')
        
        yield dpy.FlushDeferredObjects
        
        """
        We need a FlushDeferredObjects here because most Project 
        objects don't get saved at the first attempt
        """
        
        yield tim.load_dbf('VEN')
        yield tim.load_dbf('VNL')

        yield tim.load_dbf('FIN')
        yield tim.load_dbf('FNL')

        ses = settings.SITE.login('root')

        for doc in self.must_register:
            doc.register(ses)


class MyTimLoader(TimLoader):
    
    archived_tables = set('GEN ART VEN VNL'.split())
    archive_name = 'rumma'
    languages = 'et en de fr'

    def objects(self):
        
        self.PROD_617010 = products.Product(
            name="Edasimüük remondikulud",
            id=40)
        yield self.PROD_617010
        
        self.sales_gen2art['617010'] = self.PROD_617010
        
        yield super(MyTimLoader,self).objects()
        #~ for o in super(MyTimLoader,self).objects():
            #~ yield o

        if GET_THEM_ALL:
            yield self.load_dbf('PIN')
            yield self.load_dbf('DLS')

    def after_gen_load(self):
        self.PROD_617010.sales_account=accounts.Account.objects.get(ref='617010')
        self.PROD_617010.save()
        
    def load_par(self,row):
        obj = super(MyTimLoader,self).load_par(row)
        if obj is None: return 
        cl = obj.__class__
        if cl is Company:
            self.store(kw,
              national_id_et=row['regkood'].strip(),
            )
        elif cl is Household:
            self.store(kw,
              prefix=row.allo,
              name=row.firme,
            )
        elif cl is Person:
            self.store(kw,
              gender=convert_gender(row['sex']),
              national_id_et=row['regkood'].strip(),
              )
        kw.update(created=row['datcrea'])
        kw.update(modified=datetime.datetime.now())
        email = row.email.strip()
        if email and is_valid_email(email):
            kw.update(email=email)
        return obj
        
        

def objects():
    settings.SITE.startup()
    tim = MyTimLoader(settings.SITE.legacy_data_path)
    for obj in tim.objects():
        yield obj
