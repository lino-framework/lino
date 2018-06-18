sap.ui.define([
    "sap/ui/core/mvc/Controller",
    "sap/ui/model/json/JSONModel",
    "sap/ui/core/routing/History",
    'sap/ui/model/Filter',
    "sap/m/MessageToast"
], function (Controller,JSONModel, History,Filter,MessageToast) {
    "use strict";
    return Controller.extend("lino.controller.baseController", {

        /**
         * Convenience method for getting the router for navigation.
         * @public
         * @returns {sap.ui.core.routing.Router or sap.m.routing.Router}
         */
        getRouter: function () {
            return sap.ui.core.UIComponent.getRouterFor(this)
        },

        /**
         * Event callback for pressing the Back button
         * Uses the router to navigate back to the previous page
         */
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

        /**
         * Used by ui5 components to route to an actors action,
         *
         */
        routeTo: function (action, actor_id, args, history) {
            this.getRouter().navTo(action + "." + actor_id,
                args, history);
        },

        /**
         * Used by Lino.window_action, a method called by action requests that have been converted to anchors
         * Currently only used to route to grid + detail views.
         *
         */
        routeToAction: function (action_id, args, rp) {
            this.getRouter().navTo(action_id,
                args, true);
        },

        /**
         * Convenience method for searching up the tree of elements to find the next MVC.
         * @public
         * @returns {sap.ui.core.mvc.View} The parent view
         */
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