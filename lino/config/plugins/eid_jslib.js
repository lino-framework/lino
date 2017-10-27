var cardReader = new be.belgium.eid.CardReader();

function noCardPresentHandler() {
  window.alert("No card present!");
}
cardReader.setNoCardPresentHandler(noCardPresentHandler);

function noReaderDetectedHandler() {
  window.alert("No reader detected!");
}
cardReader.setNoReaderDetectedHandler(noReaderDetectedHandler);

function appletNotFoundHandler() {
  window.alert("Applet not found!");
}
cardReader.setAppletNotFoundHandler(appletNotFoundHandler);

function appletExceptionHandler(e) {
  window.alert("Error reading card!\r\nException: " + e + "\r\nPlease try again.");
}
cardReader.setAppletExceptionHandler(appletExceptionHandler);

//~ function clearPicture() {
  //~ document.getElementById("encoded_picture").src = "data:image/jpeg;base64,";
//~ }

Lino.beid_read_card_processor = function() {
    var card = cardReader.read();
    if (!card) {
        //~ Lino.alert("No card returned.");
        return null;
    } 
    console.log(card.getPicture());
    return {
      cardNumber: card.cardNumber,
      validityBeginDate:card.validityBeginDate.format("{{settings.SITE.date_format_extjs}}"),
      validityEndDate: card.validityEndDate.format("{{settings.SITE.date_format_extjs}}"),
      chipNumber:card.chipNumber,
      issuingMunicipality:card.issuingMunicipality,
      nationalNumber:card.nationalNumber,
      surname:card.surname,
      firstName1:card.firstName1,
      firstName2:card.firstName2,
      firstName3:card.firstName3,
      nationality:card.nationality,
      birthLocation:card.birthLocation,
      birthDate: card.birthDate.format("{{settings.SITE.date_format_extjs}}"),
      sex:card.sex,
      nobleCondition:card.nobleCondition,
      documentType:card.documentType,
      specialStatus:card.specialStatus,
      whiteCane:card.whiteCane,
      yellowCane:card.yellowCane,
      extendedMinority:card.extendedMinority,
      street:card.street,
      streetNumber:card.streetNumber,
      boxNumber:card.boxNumber,
      zipCode:card.zipCode,
      municipality:card.municipality,
      country:card.country
      //~ comment the following line out to test whether the picture takes a lot of time
      //~ test 20121214 on my machine revealed no perceivable gain
      ,picture:base64.encode(card.getPicture())
    };
}


