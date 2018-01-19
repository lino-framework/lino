sap.ui.define([
   "sap/ui/core/UIComponent",
   "sap/ui/model/json/JSONModel",
   "sap/ui/model/resource/ResourceModel",
   "sap/ui/demo/wt/controller/HelloDialog"
], function (UIComponent, JSONModel, ResourceModel, HelloDialog) {
   "use strict";
   return UIComponent.extend("sap.ui.demo.wt.Component", {

      metadata :{
//            rootView : "sap.ui.demo.wt.helloworld.view.helloworld"
              manifest:"json"
      },

      init : function () {
        // call the init function of the parent
         UIComponent.prototype.init.apply(this, arguments);
        // set data model
         var oData = {
            recipient : {
               name : "Sad World"
            }
         };
         var oModel = new JSONModel(oData);
         this.setModel(oModel);

         /*
         // set i18n model, Disabled, for simplicity.
         var i18nModel = new ResourceModel({
            bundleName : "sap.ui.demo.wt.i18n.i18n"
         });
         this.setModel(i18nModel, "i18n");
         */
         // set dialog
         this._helloDialog = new HelloDialog(this.getRootControl());
         },
         openHelloDialog : function() {
         	    this._helloDialog.open();
         	    }
   });
});