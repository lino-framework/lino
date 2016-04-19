# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

# Test this directly using:
#
#   $ python setup.py test -s tests.UtilsTests.test_xmlgen_sepa

u"""
A set of generator tags for building SEPA documents.

Requires Python 2.7 because it needs the `default_namespace` for
`ElementTree.write`.

Usage:

>>> from lino.utils.xmlgen.sepa import E
>>> x = E.pain_001_001_02(
...   E.GrpHdr(
...     E.MsgId("SAL63023CP20130621022043"),
...     E.CreDtTm("2013-06-21T02:20:43") ,
...     E.NbOfTxs("8") ,
...     E.Grpg("MIXD") ,
...     E.InitgPty(E.Nm(u"ÖSHZ Nispert")) )
...   )
>>> print (E.tostring_pretty(x))
<pain.001.001.02 xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.02">
<GrpHdr>
<MsgId>SAL63023CP20130621022043</MsgId>
<CreDtTm>2013-06-21T02:20:43</CreDtTm>
<NbOfTxs>8</NbOfTxs>
<Grpg>MIXD</Grpg>
<InitgPty>
<Nm>&#214;SHZ Nispert</Nm>
</InitgPty>
</GrpHdr>
</pain.001.001.02>

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import os
import sys
import cgi
import datetime

from xml.etree import ElementTree as ET
from lino.utils.xmlgen import etree
from lino.utils.xmlgen import Namespace, RAW

# names have been extracted using:
# python xsdspy.py XSD/pain.001.001.02.xsd
# python xsdspy.py XSD/pain.001.001.05.xsd
# name Grpg seems to be used only in pain.001.001.02 but not in pain.001.001.05

E = Namespace("urn:iso:std:iso:20022:tech:xsd:pain.001.001.02", """
ExternalPersonIdentification1Code Rcrd GenericPersonIdentification1 PrvcOfBirth BatchBookingIndicator RltdDt Envlp UnitCcy OrgId GroupHeader48 CtryOfRes Adr Document FrDt GenericAccountIdentification1 CdtrRefInf TaxRecordPeriod1Code IntrmyAgt2Acct DlvrTo AnyBIC Ustrd CtrctId FwdgAgt PmtInfId CtrlSum AddtlRmtInf PaymentTypeInformation19 OrganisationIdentificationSchemeName1Choice ExternalPurpose1Code ExternalLocalInstrument1Code Othr InstrPrty Nb TaxTp Invcr DuePyblAmt ExternalFinancialInstitutionIdentification1Code AdrTp TaxInformation3 MobNb DbtrAcct PstlAdr PmtInf AdmstnZn ReferredDocumentInformation3 IntrmyAgt3Acct DocumentType5Code ExchangeRate1 PhoneNumber Issr Ctgy ExternalClearingSystemIdentification1Code Dt CityOfBirth FrmsCd FaxNb Prd InstrForDbtrAgt ActiveOrHistoricCurrencyAndAmount_SimpleType SvcLvl DateAndPlaceOfBirth ContactDetails2 Tax EquivalentAmount2 DlvryMtd ExternalCashAccountType1Code Mtd CertId ChequeType2Code DocumentType3Code MemoFld PstCd CtgyDtls TaxAuthorisation1 ChqInstr Max2048Text ToDt PercentageRate CdtNoteAmt IntrmyAgt1Acct DiscountAmountType1Choice EndToEndId ChqNb ActiveOrHistoricCurrencyCode InstdAmt RmtId RmtdAmt ExternalDiscountAmountType1Code ExternalAccountIdentification1Code Cd Ref RemittanceLocationMethod2Code CtctDtls AnyBICIdentifier ISODateTime CreditorReferenceType2 CountryCode ChqFr CreDtTm TaxId TtlTaxblBaseAmt PrtLctn TtlTaxAmt AmountType3Choice RmtInf Dtls Priority2Code Yr DatePeriodDetails DecimalNumber PmtTpInf TwnNm DbtrSts Ccy ChrgsAcctAgt OrganisationIdentification8 ReferredDocumentType2 Rsn CdtTrfTxInf PrvtId Dept ChequeDelivery1Code RfrdDocAmt SchmeNm TaxAmount1 TaxParty1 RefNb PlcAndNm Max140Text BldgNb BirthDt StrtNm BICFIIdentifier CashAccount24 CreditTransferTransaction6 Cdtr Authorisation1Code PaymentInstruction9 Max128Text TaxAmountAndType1 DbtrAgt SupplementaryDataEnvelope1 Strd AdjstmntAmtAndRsn CustomerCreditTransferInitiationV05 RgltryRptg CdOrPrtry Purp XchgRateInf Nm RemittanceInformation7 Titl Max35Text GenericFinancialIdentification1 NmPrfx RegulatoryReportingType1Code ActiveOrHistoricCurrencyAndAmount PersonIdentification5 Authorisation1Choice MsgId CdtrAgtAcct ChargeBearerType1Code LocalInstrument2Choice RegulatoryAuthority2 CdtrAcct TaxParty2 ExternalOrganisationIdentification1Code Max34Text BICFI InstrInf Max15NumericText FinancialInstitutionIdentification8 Max16Text RmtLctnPstlAdr PartyIdentification43 BranchAndFinancialInstitutionIdentification5 Authrty IBAN2007Identifier ChequeDeliveryMethod1Choice TaxRecord1 ExchangeRateType1Code BranchData2 SubDept ClearingSystemMemberIdentification2 StructuredRegulatoryReporting3 TaxAmountType1Choice CdtrAgt EqvtAmt UltmtDbtr Dbtr InstrForCdtrAgt Authstn ChqTp IBAN ChrgBr PoolgAdjstmntDt TaxblBaseAmt CdtDbtInd AdrLine LclInstrm DtAndPlcOfBirth Prtry AccountSchemeName1Choice BrnchId Purpose2Choice CategoryPurpose1Choice XchgRate RmtLctnMtd Number InstrId Amt TaxRecordDetails1 CtryOfBirth PersonIdentificationSchemeName1Choice PaymentMethod3Code DscntApldAmt Inf SupplementaryData1 PostalAddress6 ChrgsAcct PmtId CtrySubDvsn RegulatoryReporting3 CreditorReferenceType1Choice CreditorReferenceInformation2 EmailAdr RemittanceAmount2 RltdRmtInf RfrdDocInf PaymentIdentification1 Tp Sgntr ClearingSystemIdentification2Choice CashAccountType2Choice ISODate FinancialIdentificationSchemeName1Choice ReqdExctnDt UltmtCdtr DbtCdtRptgInd NameAndAddress10 SplmtryData Invcee DbtrAgtAcct CtgyPurp GrpHdr TaxAmt PmtMtd ReferredDocumentType1Choice Ctry ExternalServiceLevel1Code RmtLctnElctrncAdr BtchBookg Max10Text NamePrefix1Code CreditDebitCode BaseOneRate InstructionForCreditorAgent1 ExternalCategoryPurpose1Code Instruction3Code ChqMtrtyDt ClrSysId SeqNb PhneNb TaxPeriod1 CcyOfTrf RgnlClrZone ExternalTaxAmountType1Code AddressType2Code FinInstnId MmbId AccountIdentification4Choice NbOfTxs TtlAmt RegnId Party11Choice Max70Text IntrmyAgt3 IntrmyAgt2 IntrmyAgt1 Cheque7 Max4Text Max350Text InitgPty DiscountAmountAndType1 GenericOrganisationIdentification1 RemittanceLocation2 StructuredRemittanceInformation9 Rate ClrSysMmbId ServiceLevel8Choice AddtlInf DocumentAdjustment1 RateTp CstmrCdtTrfInitn FrToDt Id
FinancialInstitutionIdentification5Choice SclSctyNb ReferredDocumentAmount1Choice TaxRefNb PrvcOfBirth BatchBookingIndicator DocumentType2Code OrgId RfrdDocNb CtryOfRes Adr Document AuthrtyCtry IntrmyAgt2Acct DlvrTo Ustrd CtrctId FwdgAgt PaymentInstructionInformation1 PmtInfId TtlTaxAmt CdtrTaxTp CreditTransferTransactionInformation1 CdtTrfTxInf DtAndPlcOfBirth InstrPrty TaxTp GroupHeader1 TaxInformation2 PaymentCategoryPurpose1Code IdntyCardNb DbtrTaxId CHIPSUniversalIdentifier PstlAdr CurrencyCode CashAccountType2 IntrmyAgt3Acct Issr Max3Text PrvtId RfrdDocRltdDt PsptNb CityOfBirth FrmsCd InstrForDbtrAgt LclInstrm LocalInstrument1Choice SvcLvl GenericIdentification4 TaxTpInf TaxDt IBEI Tax DbtrAcct DlvryMtd PersonIdentification3 Purpose1Choice CdtrRef MsgId DocumentType3Code NmAndAdr AmountType2Choice MemoFld PstCd OthrId DunsIdentifier ChqInstr InstrInf PercentageRate CdtNoteAmt IntrmyAgt1Acct ChrgsAcctAgt RfrdDocTp EndToEndId ChqNb InstdAmt RmtId RmtdAmt CashAccount7 Cd PartyIdentification8 ISODateTime CountryCode ChqFr CreDtTm Grpg TtlTaxblBaseAmt PrtLctn AlnRegnNb ServiceLevel2Choice RmtInf Priority2Code DecimalNumber PmtTpInf PrtryId Ccy BkPtyId TaxIdNb ReferredDocumentType1 AccountIdentification3Choice Ctry CdtrAcct OrganisationIdentification2 ChequeDelivery1Code RfrdDocAmt NameAndAddress3 BEIIdentifier Inf Max140Text EANGLNIdentifier BldgNb BirthDt StrtNm DuePyblAmt Cdtr CmbndId Max128Text Dbtr DbtrAgt ChrgsAcct RgltryRptg RemittanceInformation1 StructuredRemittanceInformation6 Purp XchgRateInf Nm Max35Text UPIC RegulatoryReporting2 RegulatoryReportingType1Code ReferredDocumentInformation1 DateAndPlaceOfBirth BEI GenericIdentification3 AdrTp ClearingSystemMemberIdentification3Choice CdtrAgtAcct ChargeBearerType1Code CreditorReferenceInformation1 AddtlRmtInf BranchData EquivalentAmount FinancialInstitutionIdentification3 Max34Text IBEIIdentifier NameAndAddress7 Party2Choice Max15NumericText Max16Text RmtLctnPstlAdr DrvrsLicNb BranchAndFinancialInstitutionIdentification3 Authrty CtgyDesc ExternalClearingSystemMemberCode ChequeDeliveryMethod1Choice ExchangeRateType1Code CdtrTaxId Strd ExternalPurposeCode CdtrAgt Cheque5 EqvtAmt UltmtDbtr TaxblBaseAmt BICIdentifier InstrForCdtrAgt RemittanceLocationMethod1Code Authstn ChqTp IBAN ChrgBr PoolgAdjstmntDt DUNS ExternalLocalInstrumentCode ClrChanl AdrLine pain.001.001.02 CurrencyAndAmount BrnchId ServiceLevel1Code ChequeType2Code XchgRate BBAN InstrId Amt CtryOfBirth PaymentMethod3Code DscntApldAmt SimpleIdentificationInformation2 CurrencyAndAmount_SimpleType PostalAddress1 Invcr CdtrRefTp PmtId CtrySubDvsn PrtryAcct RltdRmtInf RfrdDocInf PaymentIdentification1 Tp IdTp Prtry Max256Text CertId ISODate ReqdExctnDt UltmtCdtr DbtCdtRptgInd StructuredRegulatoryReporting2 Instruction3Code AuthrtyNm Invcee DbtrAgtAcct CtgyPurp GrpHdr TaxAmt PmtMtd BIC EANGLN IBANIdentifier BtchBookg PmtInf CtrlSum BaseOneRate InstructionForCreditorAgent1 BBANIdentifier CdtrRefInf RmtLctnElctrncAdr ChqMtrtyDt ClearingChannel2Code CashAccountType4Code USCHU UPICIdentifier ExchangeRateInformation1 CcyOfTrf RgnlClrZone RgltryDtls TaxType AddressType2Code FinInstnId NbOfTxs Max70Text IntrmyAgt3 IntrmyAgt2 IntrmyAgt1 CreditorReferenceType1 PaymentTypeInformation1 RmtLctnMtd InitgPty RemittanceLocation1 Rate ClrSysMmbId RegulatoryAuthority MplyrIdNb CstmrNb RateTp TwnNm TaxDetails Id Grouping1Code
""")


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
