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
                args.query = {'dt': this._selectedDevice};
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
                    return v;
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
         * Method that runs the ajax call for most actions.
         *
         * todo decide which args are for this method, move ajax into this method.
         */
// actor_id, action_name,rp,is_on_main_actor,pk, params
        runSimpleAction: function ({
                                       actor_id, action_name, sr, is_on_main_actor,
                                       rp = this.getView().getId(), /*keyword args*/
                                       http_method = "GET",
                                       params = {}
                                   }) {
           if (typeof(sr) === "string" || typeof(sr) === "number" ) {
                sr = [sr]
            }
            else if (sr.length === 0) {
                // Cancel action press, nothing selected
                // Note: This might be wrong, some actions such as "Mark all as seen" might not need a SR.
                MessageToast.show("Please select a row");
                return;
            }

            jQuery.extend(params, { //same as update in python, optinal first arg for "deep update"
                "an": action_name,
                "sr": sr,
                // "mt": this._content_type, /*Not sure if needed for simple, actions*/
                // "mk": this._PK            /*Not sure if same as PK in all cases, requires talk with luc*/
            });

            jQuery.ajax({
                context: this,
                url: '/api/' + actor_id.replace(".", "/") + "/" + params.sr[0],
                type: http_method,
                data: jQuery.param(params),
                success: this.handleActionSuccess,
                error: function (e) {
                    MessageToast.show("error: " + e.responseText);
                }
            });
        },

        handleActionSuccess: function (data) {
            if (data && data['success'] && data['xcallback']) {
                // this.xcallback = data['xcallback']; // WARNING, this is a hack to allow the jsfragment to
                let oView = this.getView();
                if (!this._yesNoDialog /*|| this._yesNoDialog.bIsDestroyed === true*/) {
                    this._yesNoDialog = sap.ui.jsfragment("lino.fragment.YesNoDialog", this);
                    oView.addDependent(this._yesNoDialog)
                }
                oView.setModel(new JSONModel(data), "yesno");
                this._yesNoDialog.open();
            }
            else if (data && data['eval_js']) {
                eval(data['eval_js']);
            }
            // sap.m.MessageToast.show(data['message']);
            else if (data['detail_handler_name'] !== undefined) {
                if (data['record_deleted'] === true) {
                    this.afterRecordDelete(data)
                }
            }

            else if(data['refresh'] || data["refresh_all"]){
                this.refresh();
            }

            else {
                MessageToast.show(data['message']);
            }

        },

        /**
         * Generic function to handle button actions.
         */
        onPressAction: function (oEvent) {
            const button = oEvent.getSource();
            MessageToast.show(button.data('action_name') + "' pressed");
            this.runSimpleAction({
                actor_id: button.data('actor_id'),
                action_name: button.data('action_name'),
                sr: this.getSelectedRows(oEvent),
                http_method: button.data('http_method'),

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

        /**
         * Event handler when a expand slave-table/summary button gets pressed
         * @param {sap.ui.base.Event} oEvent the table selectionChange event
         * @public
         *
         * Used in both detail controller and table controller
         */
        handleExpandSlave: function (oEvent) {
            var view = this.getView();
            var mk = this._PK;
            var mt = this._content_type;
            this.routeToAction("grid." + oEvent.getSource().data("actor_id"),
                {
                    "query": {
                        mk: mk,
                        mt: mt
                    }
                }, view.getId());
        },

    })
});
