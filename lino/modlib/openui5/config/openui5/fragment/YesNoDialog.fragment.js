sap.ui.jsfragment("lino.fragment.YesNoDialog", {
    createContent: function (data) {
        // var oButton = new sap.m.Button({
        // 	text:"Hello World",
        // 	press:oController.doSomething
        // });
        var xcallback = data['xcallback'];
        var dialog = new sap.m.Dialog({
            title: xcallback['title'],
            type: 'Message',
            content: new sap.m.Text({text: data['message']}),
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
                                me.routeTo("detail", data['detail_handler_name'].replace('.detail', ''), {});
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
            }
        });
        return dialog;
    }
});