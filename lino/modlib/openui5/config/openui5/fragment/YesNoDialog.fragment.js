sap.ui.jsfragment("lino.fragment.YesNoDialog", {
    createContent: function (context) {

        var me = context;
        var xcallback = context.xcallback;
        var dialog = new sap.m.Dialog({
            title: xcallback['title'],
            type: 'Message',
            content: new sap.m.Text({text: "{yesno>/message}" /*context['message']*/}),
            beginButton: new sap.m.Button({
                text: xcallback['buttons']['yes'],
                press: function () {
                    sap.m.MessageToast.show('Yes pressed!');
                    jQuery.ajax({
                        url: '/callbacks/' + xcallback['id'] + '/yes',
                        type: 'GET',
                        success: function (data) {
                            sap.m.MessageToast.show(data['message']);
                            if (data['detail_handler_name'] !== undefined) {
                                // todo NAV info
                                var oView = me.getView();
                                if (data['record_deleted'] === true) {
                                    var oNavInfo = oView.oModels.record.getData().navinfo;
                                    var record_id = null;
                                    if (oNavInfo.next){
                                        record_id = oNavInfo.next;}
                                    else if (oNavInfo.prev){
                                        record_id = oNavInfo.next;}

                                    me.routeTo("detail", data['detail_handler_name'].replace('.detail', ''), {record_id:record_id});

                                }
                            }
                        },
                        error: function (e) {
                            sap.m.MessageToast.show("error: " + e);
                        }
                    });
                    dialog.close();
                }
            }),
            endButton: new sap.m.Button({
                text: xcallback['buttons']['no'],
                press: function () {
                    dialog.close();
                }
            }),
            afterClose: function () {
                dialog.destroy();
                me._yesNoDialog = undefined;
                //todo also delete yes json data binding?
            }
        });
        return dialog;
    }
});
