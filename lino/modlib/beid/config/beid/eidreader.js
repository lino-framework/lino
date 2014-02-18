
Lino.beid_read_card_processor = function() {
    var card = document.applets.EIDReader.readCard();
    if (!card) {
        //~ Lino.alert("No card returned.");
        return null;
    } 
    //~ console.log(card.getPicture());
    return { card_data: card };
}

