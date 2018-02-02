sap.ui.define([
		'jquery.sap.global',
		'sap/ui/core/mvc/Controller'
	], function(jQuery, Controller) {
	"use strict";

	return Controller.extend("sap.ui.demo.wt.controller.SideNav", {

		onCollapseExpandPress: function () {
			var oSideNavigation = this.getView().byId('sideNavigation');
			var bExpanded = oSideNavigation.getExpanded();

			oSideNavigation.setExpanded(!bExpanded);
		}
	});

});

//sap.ui.getCore().byId("id")