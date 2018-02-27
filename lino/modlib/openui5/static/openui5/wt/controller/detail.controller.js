sap.ui.define([
	"sap/ui/core/mvc/Controller",
	"sap/ui/model/json/JSONModel",
	"sap/ui/unified/Menu",
	"sap/ui/unified/MenuItem",
	"sap/m/MessageToast",
	"sap/ui/core/format/DateFormat"
], function(Controller, JSONModel, Menu, MenuItem, MessageToast, DateFormat) {
	"use strict";

	return Controller.extend("sap.ui.demo.wt.controller.detail", {

		onInit : function () {
			var oView = this.getView();
			this.page_no = 0;
            this.page_limit = this.visibleRowCount;
            this.pv = []; // unused,
            this._PK = null;
//            this._actor_id = this.getView().byId("MAIN_TABLE").data("actor_id");


		},

		initSampleDataModel : function() {
			var oModel = new JSONModel();

			var oDateFormat = DateFormat.getDateInstance({source: {pattern: "timestamp"}, pattern: "dd/MM/yyyy"});

			jQuery.ajax(this.getView().byId("MAIN_PAGE").data("url"), {
				dataType: "json",
				data:{limit:15,fmt:'json',an:"detail"},
				success: function (oData) {
					oModel.setData(oData);
				},
				error: function () {
					jQuery.sap.log.error("failed to load json");
				}
			});
			console.log(this.count++)

			return oModel;
		},

		getNavport: function(){
		    var vp = sap.ui.getCore().byId("__component0---MAIN_VIEW").byId('viewport');
            return vp
		},

        onNavButtonPress : function(oEvent){
            this.getNavport().back();
        },


		load_record: function(sPK){
			var oModel = new JSONModel();
            var oView = this.getView();
            this._PK = sPK;
		    MessageToast.show("Going to load item with PK of" + sPK);

		    jQuery.ajax(oView.byId("MAIN_PAGE").data("url") + sPK, {
				dataType: "json",
				data:{fmt:'json',
				      an:'detail'
				     },
				success: function (oData) {
					oModel.setData(oData);
					oView.setModel(oModel, "record");
				},
				error: function () {
					jQuery.sap.log.error("failed to load json");
				}
			});
		},

	});

});
