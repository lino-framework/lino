sap.ui.define([
   "sap/ui/core/mvc/Controller",
   "sap/m/MessageToast",
   "sap/ui/model/json/JSONModel",
], function (Controller, MessageToast, JSONModel) {
   "use strict";
   return Controller.extend("lino.controller.dashboard", {

        onInit: function(){
            console.log("Things working....")

            var that=this;
            that.getView().byId('dashboard').getParent().setBusy(true);
            $.get( "/api/main_html", function( data ) {
                    that.getView().byId('dashboard').setContent(data.html);
                    that.getView().byId('dashboard').getParent().setBusy(false);
                });
            // highlights first item in menu if selected with Keyboard
//			this.byId("openMenu").attachBrowserEvent("tab keyup", function(oEvent){
//				this._bKeyboard = oEvent.type == "keyup";
//			}, this);
		},
	})

});

