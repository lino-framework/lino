sap.ui.define([
	"sap/ui/core/mvc/Controller",
	"sap/m/MessageToast",
	"sap/ui/model/json/JSONModel",
	"sap/ui/model/Filter",
	"sap/ui/model/FilterOperator"
], function (Controller, MessageToast, JSONModel, Filter, FilterOperator) {
	"use strict";

	return Controller.extend("sap.ui.demo.wt.controller.AllTickets", {
	                          // Name should be name of controller in the correct namespace

        onInit : function () {
			var oViewModel = new JSONModel({
				currency: "EUR"
			});
			this.getView().setModel(oViewModel, "view");
		},

		/*onFilterInvoices : function (oEvent) {

			// build filter array
			var aFilter = [];
			var sQuery = oEvent.getParameter("query");
			if (sQuery) {
				aFilter.push(new Filter("ProductName", FilterOperator.Contains, sQuery));
			}

			// filter binding
			var oList = this.getView().byId("invoiceList");
			var oBinding = oList.getBinding("items");
			oBinding.filter(aFilter);
		}*/

	});

});

sap.ui.getCore().attachInit(function () {
  sap.ui.require(['sap/ui/core/library', 'sap/ui/base/DataType'], function(library, DataType){
    library.CSSSize = DataType.createType('sap.ui.core.CSSSize', {
      isValid : function(){
        return true
      },
    },
    DataType.getType('string')
    );
    new sap.m.Panel({
      headerText : "Panel 1",
      height     : "100vh",
      width      : "100vw",
      backgroundDesign: "Solid",
      expanded   : true
    }).placeAt("content");
  });
});