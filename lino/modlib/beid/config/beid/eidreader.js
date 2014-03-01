
Lino.beid_read_card_processor = function() {
    var card = document.applets.EIDReader.readCard();
    // if (!card) {
    //     Lino.alert("Could not find any card on your reader.");
    //     return null;
    // } 
    // console.log(20140301, card);
    return { card_data: card };
}

