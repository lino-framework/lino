sap.ui.define([
    "sap/ui/core/UIComponent",
    "sap/ui/model/json/JSONModel",
    "sap/ui/model/resource/ResourceModel"
], function (UIComponent, JSONModel, ResourceModel) {
    "use strict";
    return UIComponent.extend("lino.app.Component", {

        metadata: {
//            rootView : "sap.ui.demo.wt.helloworld.view.helloworld"
            manifest: "json",
        },

        init: function () {
            // Global init for lino.app.Compnent, not sure if anything is needed.

            // call the init function of the parent
            UIComponent.prototype.init.apply(this, arguments);
            // create the views based on the url/hash
            this.getRouter().initialize();

            // set data model
//         var oData = {
//            recipient : {
//               name : "Sad World"
//            }
//         };
//         var oModel = new JSONModel(oData);
//         this.setModel(oModel);

            /*
            // set i18n model, Disabled, for simplicity.
            var i18nModel = new ResourceModel({
               bundleName : "sap.ui.demo.wt.i18n.i18n"
            });
            this.setModel(i18nModel, "i18n");
            */
            // set dialog
//         this._helloDialog = new HelloDialog(this.getRootControl());
//         },
//         openHelloDialog : function() {
//         	    this._helloDialog.open();
//         	    }
        }
    });
});