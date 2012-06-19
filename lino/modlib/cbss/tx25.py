# -*- coding: UTF-8 -*-
## Copyright 2011-2012 Luc Saffre
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


from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


from lino import mixins
from lino import dd
from lino.utils import Warning
from lino.utils import join_words
from lino.utils import AttrDict, IncompleteDate
from lino.tools import obj2str

from lino.utils import babel

from lino.utils.xmlgen import html as xghtml
E = xghtml.E

from lino.utils.babel import dtos



try:
    import suds
except ImportError, e:
    pass


from lino.modlib.cbss.models import NewStyleRequest,SSIN, get_client, \
  CBSSRequestDetail, CBSSRequests, cbss2gender, RequestStatus

class RetrieveTIGroupsRequest(NewStyleRequest,SSIN):
    """
    A request to the RetrieveTIGroups service (aka Tx25)
    """
    
    class Meta:
        verbose_name = _("Tx25 Request")
        verbose_name_plural = _('Tx25 Requests')
        
    wsdl_parts = ('cache','wsdl','RetrieveTIGroupsV3.wsdl')
    
    language = babel.LanguageField()
    history = models.BooleanField(
        verbose_name=_("History"),default=False,
        help_text = "Whatever this means.")
        
    def get_service_reply(self,**kwargs):
        client = get_client(self)
        meth = client.service.retrieveTI
        clientclass = meth.clientclass(kwargs)
        client = clientclass(meth.client, meth.method)
        #~ print 20120613, portSelector[0]
        #~ print '20120613b', dir(client)
        return client.succeeded(client.method.binding.input, self.response_xml.encode('utf-8'))
        
    
    def execute_newstyle(self,client,infoCustomer,simulate_response):
        si = client.factory.create('ns0:SearchInformationType')
        si.ssin = self.get_ssin()
        if self.language:
            si.language = self.language
        #~ if self.history:
            #~ si.history = 'true'
        si.history = self.history
        #~ if validate:
            #~ self.validate_newstyle(srvreq)
        if simulate_response is None:
            self.check_environment(si)
            try:
                reply = client.service.retrieveTI(infoCustomer,None,si)
            except suds.WebFault,e:
                """
                Example of a SOAP fault:
          <soapenv:Fault>
             <faultcode>soapenv:Server</faultcode>
             <faultstring>An error occurred while servicing your request.</faultstring>
             <detail>
                <v1:retrieveTIGroupsFault>
                   <informationCustomer xmlns:ns0="http://kszbcss.fgov.be/intf/RetrieveTIGroupsService/v1" xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/">
                      <ticket>2</ticket>
                      <timestampSent>2012-05-23T10:19:27.636628+01:00</timestampSent>
                      <customerIdentification>
                         <cbeNumber>0212344876</cbeNumber>
                      </customerIdentification>
                   </informationCustomer>
                   <informationCBSS>
                      <ticketCBSS>f4b9cabe-e457-4f6b-bfcc-00fe258a9b7f</ticketCBSS>
                      <timestampReceive>2012-05-23T08:19:09.029Z</timestampReceive>
                      <timestampReply>2012-05-23T08:19:09.325Z</timestampReply>
                   </informationCBSS>
                   <error>
                      <severity>FATAL</severity>
                      <reasonCode>MSG00003</reasonCode>
                      <diagnostic>Unexpected internal error occurred</diagnostic>
                      <authorCode>http://www.bcss.fgov.be/en/international/home/index.html</authorCode>
                   </error>
                </v1:retrieveTIGroupsFault>
             </detail>
          </soapenv:Fault>
                """
                
                msg = CBSS_ERROR_MESSAGE % e.fault.faultstring
                msg += unicode(e.document)
                self.status = RequestStatus.failed
                raise Warning(msg)
            self.response_xml = reply
        else:
            self.response_xml = simulate_response
            
        #~ self.response_xml = unicode(reply)
        reply = self.get_service_reply()
        self.ticket = reply.informationCBSS.ticketCBSS
        if reply.status.value == "NO_RESULT":
            msg = CBSS_ERROR_MESSAGE % reply.status.code
            keys = ('value','code','description')
            msg += '\n'.join([
                k+' : '+getattr(reply.status,k)
                    for k in keys])
            for i in reply.status.information:
                msg += "\n- %s = %s" % (i.fieldName,i.fieldValue)
            self.status = RequestStatus.warnings
            raise Warning(msg)
            
        self.status = RequestStatus.ok
        #~ self.response_xml = str(res)
        #~ self.response_xml = "20120522 %s %s" % (res.__class__,res)
        #~ print 20120523, res.informationCustomer
        #~ print self.response_xml
        return reply
        
    def Result(self,ar):
        return ar.spawn(RetrieveTIGroupsResult,master_instance=self)
        
        
  
class RetrieveTIGroupsRequestDetail(CBSSRequestDetail):
  
    parameters = "national_id language history"
    
    result = "cbss.RetrieveTIGroupsResult"
    
    #~ def setup_handle(self,lh):
        #~ CBSSRequestDetail.setup_handle(self,lh)

class RetrieveTIGroupsRequests(CBSSRequests):
    model = RetrieveTIGroupsRequest
    detail_layout = RetrieveTIGroupsRequestDetail()
    required_user_groups = ['cbss']
        
    #~ @dd.virtualfield(dd.HtmlBox())
    #~ def result(self,row,ar):
        #~ return row.response_xml
        
class RetrieveTIGroupsRequestsByPerson(RetrieveTIGroupsRequests):
    master_key = 'person'
    
class MyRetrieveTIGroupsRequests(RetrieveTIGroupsRequests,mixins.ByUser):
    pass
    





def rn2date(rd):
    return IncompleteDate(int(rd.Century+rd.Year),int(rd.Month),int(rd.Day))
    
def datarow(group,node,since,info):
    if node.__class__.__name__.startswith('IT'):
        itnum = node.__class__.__name__[2:]
    else:
        itnum = ''
    if hasattr(node,'Type'):
        group += " " + node.Type
        group += " " + node.Status
        group += " " + node.Structure
    return AttrDict(group=group,
        type=itnum,since=rn2date(since),info=E.p(*info))
def code_label(n):
    if n.Label:
        return [n.Code,' ',E.b(n.Label)]
    return [n.Code]
    
def NameType(n):
    info = []
    s = ' '.join([ln.Label for ln in n.LastName])
    info.append(E.b(s))
    info.append(', ')
    s = ' '.join([fn.Label for fn in n.FirstName])
    info.append(s)
    return info
    
def deldate(n):
    if hasattr(n,'DelDate'):
        return [', until %s' % dtos(rn2date(n.DelDate))]
    return []
    
#~ def simpleattr(n,name):
    #~ v = getattr(n,name,None)
    #~ if v:
        #~ return [ ', '+name+' ' + unicode(v)]
    #~ return []
    
def simpletype(v):
    return [ unicode(v) ]
def addinfo(node,name,prefix=None,fmt=simpletype):
    v = getattr(node,name,None)
    if not v: return []
    if prefix is None:
        prefix = ', %s ' % name
    return [prefix] + fmt(v)
    
def DateType(n):
    return [babel.dtos(rn2date(n))]
def TribunalType(n):
    return code_label(n)
def PlaceType(n):
    return code_label(n)
def GraphicPlaceType(n):
    info = CountryType(n.Country)
    if hasattr(n.Graphic):
        info.append(', graphic:'+n.Graphic)
    return 
def ForeignJudgementType(n):
    return GraphicPlaceType(n.Place)
def BelgianJudgementType(n):
    info = []
    info += TribunalType(n.Tribunal)
    info += DateType(n.Date)
    info += PlaceType(n.Place)
    return info
def CountryType(n):
    return code_label(n)
def LieuType(n):
    info = []
    if hasattr(n,'Place1'):
        info += code_label(n.Place1)
    elif hasattr(n,'Place2'):
        info += code_label(n.Place2)
    else:
        place = n.Place3
        #~ info += GraphicPlaceType(place)
        if hasattr(place,'BelgianJudgement'):
            info += BelgianJudgementType(place.BelgianJudgement)
        else:
            info += ForeignJudgementType(place.ForeignJudgement)
    return info

def DeliveryType(n):
    return PlaceType(n.Place)
    
def DiplomaticPostType(n):
    return code_label(n)
def ProvinceType(n):
    return code_label(n)
    
def IssuerType(n):
    info = addinfo(n,'Place',' in ',PlaceType)
    info += addinfo(n,'Province',' in ',ProvinceType)
    info += addinfo(n,'PosteDiplomatique',' by ',DiplomaticPostType)
    return info

def ResidenceType(n):
    return code_label(n)
    
def NationalNumberType(n):
    return [n.NationalNumber]
    
def PartnerType(n):
    info = addinfo(n,'NationalNumber','',NationalNumberType)
    #~ info += addinfo(n,'Name','',NameType)
    info += addinfo(n,'Name',' ',NameType)
    return info
    
def NotaryType(n):
    info = addinfo(n,'NameNotary')
    info += addinfo(n,'Place',' in ',PlaceType)
    info += addinfo(n,'Country',', ',CountryType)
    return info
    
def NotificationType(n):
    info = addinfo(n,'NotificationDate',None,DateType)
    info += addinfo(n,'Place',' in ',PlaceType)
    return info
    
def ReasonType(n):
    info = code_label(n)
    return info
    
def CessationType(n):
    return code_label(n)
    
def DeclarationType(n):
    return code_label(n)
    
def Residence(n):
    info = addinfo(n,'Residence','',ResidenceType)
    info += addinfo(n,'Fusion')
    info += addinfo(n,'Language')
    info += deldate(n)
    return info
    
    
def IT140(n):
    info = code_label(n.FamilyRole)
    info += addinfo(n,'NationalNumber',': ',NationalNumberType)
    info += addinfo(n,'Name',' ',NameType)
    info += addinfo(n,'Housing',None,HousingType)
    info += deldate(n)
    return info

def HousingType(n):
    return code_label(info)
    
    

class RowHandlers:
  
    @staticmethod
    def IT000(n,name):
        #~ group = _("National Number")
        group = name
        n = n.NationalNumber
        info = [
          E.b(n.NationalNumber),
          ' ('+unicode(cbss2gender(n.Sex))+')']
        yield datarow(group,n,n.Date,info)


    @staticmethod
    def FileOwner(fo,name):
        group = _("Residences")
        for n in fo.Residences:
            info = Residence(n)
            yield datarow(group,n,n.Date,info)
            group = ''

      
    @staticmethod
    def Names(node,name):
        #~ group = _("Names")
        group = name
        for n in node.Name:
            info = addinfo(n,'Name','',NameType)
            yield datarow(group,n,n.Date,info)
            group = ''
        

    @staticmethod
    def LegalMainAddresses(node,name):
        group = name # "Legal Main Addresses"
        for n in node.LegalMainAddress:
            info = []
            info.append(E.b(n.Address.ZipCode))
            info.append(', ')
            info.append(n.Address.Street.Label)
            info.append(' ')
            info.append(n.Address.HouseNumber)
            yield datarow(group,n,n.Date,info)
            group = ''
            

    @staticmethod
    def ResidenceAbroad(node,name):
        group = name # _("Residence Abroad")
        for n in node.ResidenceAbroad:
            info = []
            info += code_label(n.Address.PosteDiplomatique)
            info.append(', ')
            info += code_label(n.Address.Territory)
            info.append(', ')
            pd = n.Address.Address
            info += code_label(pd.Country)
            info.append(', ')
            info.append(E.b(pd.Graphic1))
            info.append(', ')
            info.append(E.b(pd.Graphic2))
            info.append(', ')
            info.append(E.b(pd.Graphic3))
            yield datarow(group,n,n.Date,info)
            group = ''
        
    @staticmethod
    def Nationalities(node,name):
        group = name # _("Nationalities")
        for n in node.Nationality:
            info = code_label(n.Nationality)
            yield datarow(group,n,n.Date,info)
            group = ''
            
    @staticmethod
    def Occupations(node,name):
        group = name # _("Occupations")
        for n in node.Occupation:
            info = code_label(n.Occupation)
            info.append(' (SC ')
            info += code_label(n.SocialCategory)
            info.append(')')
            yield datarow(group,n,n.Date,info)
            group = ''
        
    @staticmethod
    def IT100(n,name):
        group = name # _("Birth Place")
        #~ n = res.BirthPlace
        #~ info = code_label(n.Place1)
        #~ info.append(' (' + n.ActNumber + ')')
        info = []
        info += addinfo(n,'Place1',' in ',PlaceType)
        info += addinfo(n,'Place2',' in ',GraphicPlaceType)
        info += addinfo(n,'ActNumber')
        info += addinfo(n,'SuppletoryRegister')
        yield datarow(group,n,n.Date,info)
        
    @staticmethod
    def Filiations(node,name):
        group = name # _("Filiations")
        for n in node.Filiation:
            info = code_label(n.FiliationType)
            info.append(' of ')
            info.append(n.Parent1.NationalNumber.NationalNumber)
            info.append(' ')
            #~ info += name2info(n.Parent1.Name)
            info += addinfo(n.Parent1,'Name','',NameType)
            info.append(' and ')
            info.append(n.Parent2.NationalNumber.NationalNumber)
            info.append(' ')
            info += addinfo(n.Parent2,'Name','',NameType)
            #~ info += name2info(n.Parent2.Name)
            yield datarow(group,n,n.Date,info)
            group = ''
        
    @staticmethod
    def CivilStates(node,name):
        group = name # _("Civil States") # IT120
        for n in node.CivilState:
            info = code_label(n.CivilState)
            if hasattr(n,'Spouse'):
                #~ info.append(' with ')
                #~ info += name2info(n.Spouse.Name)
                info += addinfo(n.Spouse,'Name',' with ',NameType)
                info.append(' (')
                info.append(n.Spouse.NationalNumber.NationalNumber)
                info.append(')')
            info += addinfo(n,'Lieu',' in ',LieuType)
            #~ info += LieuType(n.Lieu)
            info += addinfo(n,'ActNumber')
            info += addinfo(n,'SuppletoryRegister')
            info += deldate(n)
            yield datarow(group,n,n.Date,info)
            group = ''
        
    @staticmethod
    def FamilyMembers(node,name):
        group = name # _("Family Members")
        for n in node.FamilyMember:
            info = IT140(n)
            yield datarow(group,n,n.Date,info)
            group = ''
            
    @staticmethod
    def HeadOfFamily(node,name):
        group = _("Head Of Family")
        for n in node.HeadOfFamily:
            info = []
            info += code_label(n.FamilyRole)
            info += addinfo(n,'Name',' in family headed by ',NameType)
            #~ info += name2info(n.Name)
            info.append(' (')
            info.append(n.NationalNumber.NationalNumber)
            info.append(')')
            info += deldate(n)
            yield datarow(group,n,n.Date,info)
            group = ''
        
    @staticmethod
    def DrivingLicensesOldModel(node,name):
        group = _("Driving Licenses Old Model")
        for n in node.DrivingLicense:
            info = code_label(n.TypeOfLicense)
            info.append(' number ')
            info.append(E.b(n.LicenseNumber))
            info.append(', categories ' 
              + ' '.join([cat.Label for cat in n.Categories.Category]))
            info.append(', delivered in ')
            info += code_label(n.Delivery.Place)
            yield datarow(group,n,n.Date,info)
            group = ''
        
    @staticmethod
    def IdentityCards(node,name):
        group = _("Identity Cards")
        for n in node.IdentityCard:
            info = code_label(n.TypeOfCard)
            info.append(' number ')
            info.append(E.b(n.CardNumber))
            info += addinfo(n,'ExpiryDate',', expires ',DateType)
            #~ info.append(E.b(dtos(rn2date(n.ExpiryDate))))
            info += addinfo(n,'Delivery',', delivered in ',DeliveryType)
            #~ info.append(', delivered in ')
            #~ info += code_label(n.Delivery.Place)
            yield datarow(group,n,n.Date,info)
            group = ''
        
    @staticmethod
    def LegalCohabitations(node,name):
        def CessationType(n):
            info = ['Cessation']
            info += addinfo(n,'Reason',None,ReasonType)
            info += addinfo(n,'Place',' in ',PlaceType)
            info += addinfo(n,'Notification',' in ',NotificationType)
            return info
      
        def DeclarationType(n):
            info = ['Declaration']
            info += addinfo(n,'RegistrationDate',' ',DateType)
            info += addinfo(n,'Partner',' with ',PartnerType)
            info += addinfo(n,'Place',' in ',PlaceType)
            info += addinfo(n,'Notary',' in ',NotaryType)
            return info
    
        group = name
        for n in node.LegalCohabitation:
            info = addinfo(n,'Declaration','',DeclarationType)
            info += addinfo(n,'Cessation','',CessationType)
            info += deldate(n)
            yield datarow(group,n,n.Date,info)
            group = ''
            
      
    @staticmethod
    def Passports(node,name):
        group = name # _("Passports")
        for n in node.Passport:
            info = []
            info.append('Number ')
            info.append(E.b(n.PassportIdent.PassportNumber))
            info.append(', status ')
            info += code_label(n.Status)
            info.append(', type ')
            info += code_label(n.PassportIdent.PassportType)
            info.append(', expires ')
            info.append(E.b(dtos(rn2date(n.ExpiryDate))))
            info += addinfo(n,'Issuer',', issued ',IssuerType)
            #~ info.append(', delivered by ')
            #~ info += code_label(n.Issuer.PosteDiplomatique)
            info.append(', renewal number ')
            info.append(E.b(n.RenewalNumber))
            yield datarow(group,n,n.Date,info)
            group = ''
        
    @staticmethod
    def OrganDonations(node,name):
        group = name 
        for n in node.OrganDonation:
            info = addinfo(n,'Declaration','',DeclarationType)
            info += addinfo(n,'Place',' in ',PlaceType)
            info += deldate(n)
            yield datarow(group,n,n.Date,info)
            group = ''
        
    @staticmethod
    def IT253(node,name):
        group = name # _("Creation Date")
        n = node # res.CreationDate
        info = []
        yield datarow(group,n,n.Date,info)
        
    @staticmethod
    def IT254(node,name):
        group = name # _("Last Update")
        n = node # res.LastUpdateDate
        info = []
        yield datarow(group,n,n.Date,info)
        
    
class RetrieveTIGroupsResult(dd.VirtualTable):
    """
    Displays the response of an :class:`RetrieveTIGroupsRequest`
    as a table.
    """
    master = RetrieveTIGroupsRequest
    master_key = None
    label = _("Results")
    column_names = 'group:18 type:10 since:14 info:50'
    
    @dd.displayfield(_("Group"))
    def group(self,obj,ar):
        return obj.group
            
    @dd.displayfield(_("TI"))
    def type(self,obj,ar):
        return obj.type
            
    @dd.virtualfield(models.DateField(_("Since")))
    def since(self,obj,ar):
        return obj.since
            
    @dd.displayfield(_("Info"))
    def info(self,obj,ar):
        return obj.info
            
    @classmethod
    def get_data_rows(self,ar):
        rti = ar.master_instance
        if rti is None: 
            #~ print "20120606 ipr is None"
            return
        #~ if not ipr.status in (RequestStatus.ok,RequestStatus.fictive):
        #~ if not rti.status in (RequestStatus.ok,RequestStatus.warnings):
            #~ return
        reply = rti.get_service_reply()
        if reply is None:
            return
            
            
        res = reply.rrn_it_implicit
        
        for name, node in res:
            #~ print name, node.__class__
            m = getattr(RowHandlers,node.__class__.__name__,None)
            if m is None:
                yield AttrDict(
                  info="No handler for %s/%s in %s" % (name, node.__class__,rti),
                  group='Error',
                  type='',
                  date=datetime.date.today(),
                  )
            else:
                for row in m(node,name): yield row
        
        
        
            
__all__ = [
  'RetrieveTIGroupsRequest', 
  'RetrieveTIGroupsRequests',
  'RetrieveTIGroupsRequestsByPerson',
  'MyRetrieveTIGroupsRequests',
  'RetrieveTIGroupsResult',
]