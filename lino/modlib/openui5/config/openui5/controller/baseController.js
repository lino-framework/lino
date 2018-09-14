sap.ui.define([
    "sap/ui/core/mvc/Controller",
    "sap/ui/model/json/JSONModel",
    "sap/ui/core/routing/History",
    'sap/ui/model/Filter',
    "sap/m/MessageToast"
], function (Controller, JSONModel, History, Filter, MessageToast) {
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
            if (args.base_params !== undefined) {
                // Moving base_params to a key of query, as mk and mt are querys, also maybe pvs, detail navigation also use this method
                // However when nav buttons use this method they need args to be passed to navTo
                Object.defineProperty(args, "query",
                    Object.getOwnPropertyDescriptor(args, "base_params"));
                delete args["base_params"];
            }
            if (args.query === undefined) {
                // Object.defineProperty(args, "query",
                //    {'dt':this._selectedDevice});
                args.query = {'dt':this._selectedDevice};
            }
            this.getRouter().navTo(action_id,
                args /*if 3ed arg (history) is True, oui5 will not record history for this change.*/);
        },

        /**
         * Convenience method for searching up the tree of elements to find the next MVC.
         * @public
         * @returns {sap.ui.core.mvc.View} The parent view
         */
        getParentView: function () {
            var v = this.getView();
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


        /**
         * To be OverWridden .
	 *  Usrd fot ajax action requests. 
         */
        getSelectedRows: function (oEvent) {
	    return [];
        },
	
        /**
         * Generic function to handle button actions.
         */
        onPressAction: function (oEvent) {
            var me = this;
            var button = oEvent.getSource();
            var oView = this.getView();
            var action_name = button.data('action_name');
            var action_url = button.data('action_url');
            var action_method = button.data('action_method');
            var msg = action_name + "' pressed";
            // action_url = 'tickets/Tickets/';
            var sr = this.getSelectedRows();
            if (typeof(sr) === "string"){sr = [sr]}
            var params = {"an":action_name,
                  "sr":sr};
            var url = (params.sr.length === 1) ? '/api/' + action_url + params.sr[0] : '/api/' + action_url

            MessageToast.show(msg);
            jQuery.ajax({
                url: url,
                type: action_method,
                data: jQuery.param(params),
                success: function (data) {
                    if (data && data['success'] && data['xcallback'] !== undefined) {
                        me.xcallback = data['xcallback'];
                        var oView = me.getView();
                        if (!me._yesNoDialog /*|| me._yesNoDialog.bIsDestroyed === true*/ ) {
                            me._yesNoDialog = sap.ui.jsfragment("lino.fragment.YesNoDialog", me);
                            oView.addDependent(me._yesNoDialog)
                        }
                        var oInputModel = new JSONModel(data);
                        oView.setModel(oInputModel, "yesno");
                        me._yesNoDialog.open();
                    }
                    else if (data && data['eval_js'] !== undefined) {
                        var eval_js = data['eval_js'];
                        eval(eval_js);
                    }
                    // MessageToast.show(data['message']);
                },
                error: function (e) {
                    MessageToast.show("error: " + e.responseText);
                }
            });
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
