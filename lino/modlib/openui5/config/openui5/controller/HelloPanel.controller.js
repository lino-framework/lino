sap.ui.define([
    "sap/ui/core/mvc/Controller",
    "sap/m/MessageToast"
], function (Controller, MessageToast) {
//	"use strict";

    return Controller.extend("lino.controller.HelloPanel", {
        // Name should be name of controller in the correct namespace
        onShowHello: function () {
            /* // read msg from i18n model, disabled for simplicity
             var oBundle = this.getView().getModel("i18n").getResourceBundle();
            var sRecipient = this.getView().getModel().getProperty("/recipient/name");
            var sMsg = oBundle.getText("helloMsg", [sRecipient]);
            */
            MessageToast.show("Hello World");
        }

        , onOpenDialog: function () {
            this.getOwnerComponent().openHelloDialog();
        }

    });

});
