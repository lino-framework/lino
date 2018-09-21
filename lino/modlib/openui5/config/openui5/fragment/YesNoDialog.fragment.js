sap.ui.jsfragment("lino.fragment.YesNoDialog", {
    createContent: function (context) {

        let dialog = new sap.m.Dialog({
            title: "{yesno>/xcallback/title}",
            type: 'Message',
            content: new sap.m.Text({text: "{yesno>/message}" /*context['message']*/}),
            beginButton: new sap.m.Button({
                text: "{yesno>/xcallback/buttons/yes}",
                press: function () {
                    sap.m.MessageToast.show('Yes pressed!');
                    jQuery.ajax({
                        context: context,
                        url: '/callbacks/' + context.getView().getModel("yesno").getProperty("/xcallback/id") + '/yes',
                        type: 'GET',
                        success: context.handleActionSuccess,
                        error: function (e) {
                            sap.m.MessageToast.show("error: " + e);
                        }
                    });
                    dialog.close();
                }
            }),
            endButton: new sap.m.Button({
                text: "{yesno>/xcallback/buttons/no}",
                press: function () {
                    dialog.close();
                }
            }),
            afterClose: function () {
                dialog.destroy();
                context._yesNoDialog = undefined;
                //todo also delete yes json data binding?
            }
        });
        return dialog;
    }
});
