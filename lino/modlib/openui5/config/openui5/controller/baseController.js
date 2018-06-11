sap.ui.define([
    "sap/ui/core/mvc/Controller",
    "sap/ui/model/json/JSONModel",
    "sap/ui/core/routing/History",
    'sap/ui/model/Filter',
    "sap/m/MessageToast"
], function (Controller,JSONModel, History,Filter,MessageToast) {
    "use strict";
    return Controller.extend("lino.controller.baseController", {

        getRouter: function () {
            return sap.ui.core.UIComponent.getRouterFor(this)
        },

        onNavBack: function (oEvent) {
            var oHistory, sPreviousHash;

            oHistory = History.getInstance();
            sPreviousHash = oHistory.getPreviousHash();

            if (sPreviousHash !== undefined) {
                window.history.go(-1);
            } else {
                this.getRouter().navTo("appHome", {}, true /*no history*/);
            }
        },

        routeTo: function (action, actor_id, args, history) {
            /*
                use in app routing
            */
            this.getRouter().navTo(action + "." + actor_id,
                args, history);
        },
        routeToAction: function (action_id, args, rp) {
            /*
                used in server generated links, note the unused rp (requesting Panel).
                That might be used later for other action requests
            */
            this.getRouter().navTo(action_id,
                args, true);
        },

        getParentView: function () {
            var v = this.getView()
            while (v && v.getParent) {
                v = v.getParent();
                if (v instanceof sap.ui.core.mvc.View) {
//                    console.log(v.getMetadata()); //you have found the view
                    return v
                    break;
                }
            }
        },

        /**
         * Convenience method for getting the view model by name.
         * @public
         * @returns {sap.ui.model.Model} the model instance
         */
        getModel: function () {
            return this.getView().getModel();
        },

        /**
         * Getter for the resource bundle.
         * @public
         * @returns {sap.ui.model.resource.ResourceModel} the resourceModel of the component
         */
        getResourceBundle: function () {
            return this.getOwnerComponent().getModel("i18n").getResourceBundle();
        },

        onDelete : function () {
			var oSelected = this.byId("MAIN_PAGE").getSelectedItem();

			if (oSelected) {
				oSelected.getBindingContext().delete("$auto").then(function () {
					MessageToast.show(this._getText("deletionSuccessMessage"));
				}.bind(this), function (oError) {
					MessageBox.error(oError.message);
				});
			}
		},

        handleSuggest: function (oEvent) {
            var Input = oEvent.getSource();
            var oView = this.getView();
            var url = Input.data('input_url');
            oView.setBusy(true);
            var oInputModel = new JSONModel(jQuery.sap.getModulePath("lino.server", url));
            oView.setModel(oInputModel, "Input");
            oView.setBusy(false);

            var sTerm = oEvent.getParameter("suggestValue");
            var aFilters = [];
            if (sTerm) {
                aFilters.push(new Filter("text", sap.ui.model.FilterOperator.StartsWith, sTerm));
            }
            else {
                aFilters.push(new Filter("text", sap.ui.model.FilterOperator.All, ""));
            }

            oEvent.getSource().getBinding("suggestionItems").filter(aFilters);
        },

    })
});