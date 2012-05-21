# -*- coding: UTF-8 -*-
"""
Some experiments on how to explore the response to an 
IdentifyPerson request.
"""
from django.utils.translation import ugettext as _
from lino.utils.choicelists import Gender
from suds.sax.parser import Parser
PARSER = Parser()

response_string = u'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<SSDNReply xmlns="http://www.ksz-bcss.fgov.be/XSD/SSDN/Service">
  <ReplyContext>
    <ns1:ResultSummary ok="YES" xmlns:ns1="http://www.ksz-bcss.fgov.be/XSD/SSDN/Common">
      <ns1:ReturnCode>0</ns1:ReturnCode>
    </ns1:ResultSummary>
    <AuthorizedUser>
      <UserID>12345678901</UserID><Email>123@example.be</Email>
      <OrgUnit>123</OrgUnit><MatrixID>12</MatrixID><MatrixSubID>3</MatrixSubID>
    </AuthorizedUser>
    <Message>
      <Reference>IdentifyPersonRequest # 1</Reference>
      <Ticket>THTTMHHP49DGQ9V</Ticket>
      <TimeRequest>20120521T134021</TimeRequest><TimeReceive>20120521T134002</TimeReceive>
      <TimeResponse>20120521T134019</TimeResponse>
    </Message>
  </ReplyContext>
  <ServiceReply>
    <ns2:ResultSummary ok="YES" xmlns:ns2="http://www.ksz-bcss.fgov.be/XSD/SSDN/Common">
      <ns2:ReturnCode>0</ns2:ReturnCode>
    </ns2:ResultSummary>
    <ServiceId>OCMWCPASIdentifyPerson</ServiceId>
    <Version>20050930</Version>
    <ns3:IdentifyPersonReply xmlns:ns3="http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson">
      <ns3:SearchResults>
        <ns3:LimitedLegalData origin="RN_RR">
          <ns3:Basic>
            <ns3:SocialSecurityUser>38060105329</ns3:SocialSecurityUser>
            <ns3:LastName>MUSTERMANN</ns3:LastName>
            <ns3:FirstName>MAX MORITZ</ns3:FirstName>
            <ns3:BirthDate>1938-06-01</ns3:BirthDate>
            <ns3:Gender>1</ns3:Gender>
            <ns3:DiplomaticPost>
              <ns3:CountryCode>136</ns3:CountryCode>
              <ns3:Post>1418</ns3:Post>
              <ns3:AddressPlainText>WILHELM-BUSCH-STR. 15 BERLIN DEUTSCHLAND</ns3:AddressPlainText>
            </ns3:DiplomaticPost>
          </ns3:Basic>
          <ns3:Extended/>
        </ns3:LimitedLegalData>
      </ns3:SearchResults>
    </ns3:IdentifyPersonReply>
  </ServiceReply>
</SSDNReply>
'''

def gender(v):
    if v == '1':
        return Gender.male
    elif v == '2':
        return Gender.female
    return None

reply = PARSER.parse(string=response_string.encode('utf-8')).root()
print reply.childAtPath('/ReplyContext/Message/Ticket').text
print reply.childAtPath('/ServiceReply/ResultSummary/ReturnCode').text
service_reply = reply.childAtPath('/ServiceReply/IdentifyPersonReply')
results = service_reply.childAtPath('/SearchResults')
for i,person in enumerate(results):
    print person
      
    mapper = [
      # path , label, converter
      ['/Basic/SocialSecurityUser',_("National ID"),unicode],
      ['/Basic/LastName',_("Last name"),unicode],
      ['/Basic/MiddleName',_("Middle name"),unicode],
      ['/Basic/FirstName',_("First name"),unicode],
      ['/Basic/BirthDate',_("Birth Date"),unicode],
      ['/Basic/Gender',_("Gender"),gender],
    ]
    for k,lbl,cvt in mapper:
        node = person.childAtPath(k)
        if node is not None:
            v = cvt(node.text)
        else:
          v = None
        print lbl, ':', unicode(v)
        
