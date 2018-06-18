sap.ui.define([
    "lino/controller/baseController",
    "sap/m/MessageToast",
    "sap/ui/model/json/JSONModel",
], function (baseController, MessageToast, JSONModel) {
    "use strict";
    return baseController.extend("lino.controller.dashboard", {

        onInit: function () {
            console.log("Things working....")

            var that = this;
            that.getView().byId('dashboard').getParent().setBusy(true);
            $.get("/api/main_html", function (data) {
                that.getView().byId('dashboard').setContent(data.html);
                that.getView().byId('dashboard').getParent().setBusy(false);
            });
        },
    })

});

