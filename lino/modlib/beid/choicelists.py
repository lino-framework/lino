# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)


from lino.api import dd, _


class BeIdCardTypes(dd.ChoiceList):
    """
    List of Belgian identity card types:

    .. lino2rst::

       rt.show(beid.BeIdCardTypes)

    Didn't yet find any official reference document.
    
    The eID applet returns a field `documentType` which contains a
    numeric code.  For example 1 is for "Belgian citizen", 6 for "Kids
    card",...
    
    The eID viewer, when saving a card as xml file, doesn't save these
    values nowhere, it saves a string equivalent (1 becomes
    "belgian_citizen", 6 becomes "kids_card", 17 becomes
    "foreigner_f", 16 becomes "foreigner_e_plus",...
    
    Sources:
    | [1] https://securehomes.esat.kuleuven.be/~decockd/wiki/bin/view.cgi/EidForums/ForumEidCards0073
    | [2] `Enum be.fedict.commons.eid.consumer.DocumentType <http://code.google.com/p/eid-applet/source/browse/trunk/eid-applet-service/src/main/java/be/fedict/eid/applet/service/DocumentType.java>`_


    Excerpts from [1]:
    
    - Johan: A document type of 7 is used for bootstrap cards ? What
      is a bootstrap card (maybe some kind of test card?)  Danny: A
      bootstrap card was an eID card that was used in the early start
      of the eID card introduction to bootstrap the computers at the
      administration. This type is no longer issued.
    
    - Johan: A document type of 8 is used for a
      "habilitation/machtigings" card ? Is this for refugees or asylum
      seekers? Danny: A habilitation/machtigings card was aimed at
      civil servants. This type is also no longer used.
    
    """

    required_roles = dd.required(dd.SiteStaff)
    verbose_name = _("eID card type")
    verbose_name_plural = _("eID card types")

add = BeIdCardTypes.add_item
add('1', _("Belgian citizen"), "belgian_citizen")
# ,de=u"Belgischer Staatsbürger",fr=u"Citoyen belge"),
add('6', _("Kids card (< 12 year)"), "kids_card")
#,de=u"Kind unter 12 Jahren"),

#~ add('8', _("Habilitation"))
#,fr=u"Habilitation",nl=u"Machtiging")

add('11', _("Foreigner card A"), "foreigner_a")
        #~ nl=u"Bewijs van inschrijving in het vreemdelingenregister - Tijdelijk verblijf",
        #~ fr=u"Certificat d'inscription au registre des étrangers - Séjour temporaire",
        #~ de=u"Ausländerkarte A Bescheinigung der Eintragung im Ausländerregister - Vorübergehender Aufenthalt",
add('12', _("Foreigner card B"), "foreigner_b")
        #~ nl=u"Bewijs van inschrijving in het vreemdelingenregister",
        #~ fr=u"Certificat d'inscription au registre des étrangers",
        #~ de=u"Ausländerkarte B (Bescheinigung der Eintragung im Ausländerregister)",
add('13', _("Foreigner card C"), "foreigner_c")
        #~ nl=u"Identiteitskaart voor vreemdeling",
        #~ fr=u"Carte d'identité d'étranger",
        #~ de=u"C (Personalausweis für Ausländer)",
add('14', _("Foreigner card D"), "foreigner_d")
        #~ nl=u"EG - langdurig ingezetene",
        #~ fr=u"Résident de longue durée - CE",
        #~ de=u"Daueraufenthalt - EG",
add('15', _("Foreigner card E"), "foreigner_e")
        #~ nl=u"Verklaring van inschrijving",
        #~ fr=u"Attestation d’enregistrement",
        #~ de=u"Anmeldebescheinigung",
add('16', _("Foreigner card E+"), "foreigner_e_plus")
        # Document ter staving van duurzaam verblijf van een EU onderdaan
add('17', _("Foreigner card F"), "foreigner_f")
        #~ nl=u"Verblijfskaart van een familielid van een burger van de Unie",
        #~ fr=u"Carte de séjour de membre de la famille d’un citoyen de l’Union",
        #~ de=u"Aufenthaltskarte für Familienangehörige eines Unionsbürgers",
add('18', _("Foreigner card F+"), "foreigner_f_plus")

