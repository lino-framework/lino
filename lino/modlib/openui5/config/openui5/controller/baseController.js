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
         * Convenience method for searching up the tree of elements to find the next MVC or Dialog,
         * Needed for setting models in dialogs that are not Dependents of Views.
         * @public
         * @returns {sap.ui.core.mvc.View} The parent view
         */
        getParentViewOrDialogFragment: function (elem) {
            var v = elem
            while (v && v.getParent) {
                v = v.getParent();
                if (v instanceof sap.ui.core.mvc.View || v instanceof sap.m.Dialog) {
                    return v;
                }
            }
        },


        /**
         * Convenience method for getting the view model by name.
         * @public
         * @returns {sap.ui.model.Model} the model instance
         */
        getModel: function (model_name) {
            return this.getView().getModel(model_name);
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
         * To be overwritten.
         *  Used for ajax action requests.
         */
        getSelectedRows: function (oEvent) {
            return [];
        },

        /**
         * To be overwritten.
         * @returns record data of current row
         */
        getRecordData: function () {
            return {};
        },

        add_param_values: function (params) {
            if (this._query) { // _query is args from route matching
                jQuery.extend(params, {
                    mt: this._query['mt'],
                    mk: this._query['mk']
                })
            }
            return params
        },

        /**
         * Method that runs the ajax call for most actions.
         *
         */
// actor_id, action_name,rp,is_on_main_actor,pk, params
        runSimpleAction: function ({
                                       actor_id, action_name, sr, is_on_main_actor, submit_form_data,
                                       rp = this.getView().getId(), /*keyword args*/
                                       http_method = "GET",
                                       select_rows = true,
                                       params = {},
                                       success_callback = function(){},
})
    {
        if (typeof(sr) === "string" || typeof(sr) === "number") {
            sr = [sr]
        }
        else if (sr.length === 0) {
            // Cancel action press, nothing selected
            // Note: This might be wrong, some actions such as "Mark all as seen" might not need a SR.
            if (select_rows) {
                MessageToast.show("No row selected");
                return;
            }
        }

        if (submit_form_data) {
            jQuery.extend(true, params, this.getRecordData())
        }

        jQuery.extend(params, { //same as dict.update in python, optional  first arg for "deep update"
            "an": action_name,
            "sr": sr,
            "mt": params.mt || this._content_type,
            "mk": params.mk || this._PK            /*mk + mt are needed for inserting actions*/
        });

        let url = '/api/' + actor_id.replace(".", "/");
        if (sr.length >0) { // required to have the first sr be in the url for most actions. If not included will run action
            // on table rather than on the instance
            url += "/" + sr[0]
        }

        jQuery.ajax({
            context: this,
            url: url,
            type: http_method,
            data: jQuery.param(params),
            success: function (data) {
                success_callback(data);
                this.handleActionSuccess(data);
            },
            error: function (e) {
                MessageToast.show("error: " + e.responseText);
            }
        });
    }
,

    /**
     *  Used to open a window action's window.
     *  Requests from the server the dialog-fragment containing the layout info and shows it.
     *
     *
     */
    open_window_action: function ({
                                      actor_id, action_name, sr, is_on_main_actor, select_rows,
                                      rp = this.getView().getId(), /*keyword args*/
                                      params = {}
                                  }) {
        console.log(arguments);
        let name = actor_id + "." + action_name;
        if (!this._actions) {
            this._actions = {}
        }
        if (!this._actions[name]) {
            let control = sap.ui.controller("lino.controller.fragment");
            this._actions[name] = sap.ui.xmlfragment("lino.action." + name, control);
            this._actions[name]._linodata = {
                // an: action_name,
                actor_id: actor_id,
                callback_controller: this,
                sr: this.getSelectedRows(),
                action_name: name,
                select_rows: select_rows,
                control: control,
            };
        }
        // oView.addDependent(this._actions[nam]) // Todo attach to live cycle only?
        if (!params.data_record && action_name === "insert") {
            let action = this._actions[name];
            let ajax_params = {
                fmt: 'json',
                an: action_name,
            };
            this.add_param_values(ajax_params);
            // Get init data for insert
            jQuery.ajax({
                context: this,
                url: '/api/' + actor_id.replace(".", "/") + "/" + -99999,
                type: "GET",
                data: jQuery.param(ajax_params),
                success: function (data) {
                    let oInputModel = new JSONModel(data);
                    action.setModel(oInputModel, "record");
                    action.open();

                },
                error: function (e) {
                    MessageToast.show("error: " + e.responseText);
                }
            });

        }
        else {
            let record = params.data_record || params.field_values || {};
            this._actions[name].setModel(new JSONModel({data:record}), "record")
            this._actions[name].open();
        }
    }
,
    handleActionSuccess: function (data) {
        let oView = this.getView();
        if (data && data['success'] && data['xcallback']) {
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
        else if (data['detail_handler_name'] !== undefined && data['record_deleted'] === true) {
            this.afterRecordDelete(data)
        }

        else if (data['refresh'] || data["refresh_all"]) {
            this.refresh();
        }

        else if (data['data_record']) {
            let oModel = new JSONModel();
            oModel.setData(data['data_record']);
            oView.setModel(oModel, 'record');
        }

        else {
            MessageToast.show(data['message']);
        }

        if (data["goto_url"]){
            document.location = data["goto_url"];
        }
        else if (data["open_url"]) {
            window.open(data.open_url, 'foo', "");
        }
        console.log(data['message']);

    }
,

    /**
     * Generic function to handle button actions.
     */
    onPressAction: function (oEvent) {
        const button = oEvent.getSource();
        let args = {
            actor_id: button.data('actor_id'),
            action_name: button.data('action_name'),
            sr: this.getSelectedRows(oEvent),
            http_method: button.data('http_method'),
            submit_form_data: button.data('submit_form_data'),
            select_rows: button.data("select_rows") === "True",
        };
        MessageToast.show(button.data('action_name') + "' pressed");
        if (button.data("window_action")) {
            this.open_window_action(args);
        }
        else {
            this.runSimpleAction(args);
        }
    }
,

    /**
     * Serverside quick-search filtering for foreign key fields
     * @param oEvent
     */
    handleSuggest: function (oEvent) {
        let oInput = oEvent.getSource();
        let url = oInput.data('input_url');
        let query = oEvent.getParameter("suggestValue");
        // console.log("hs");
        if (Lino.flags['suggest']) {
            return
        }
        oInput.setFilterSuggests(true);
        this._handleSuggest({
            oEvent,
            url,
            query
        });

    }
,


    /**
     * Help button press on FK fields,
     *
     * BUG: In chrome selection doesn't work. We should change this to the normal pop-up search dialog window
     *      that is used in the input samples.
     * @param oEvent
     */
    handleValueHelp: function (oEvent) {
        let oInput = oEvent.getSource();
        oInput.setFilterSuggests(false);
        // console.log("hvh");
        Lino.wave_flag("suggest", 200);
        let url = oInput.data('input_url');
        this._handleSuggest({
            oEvent,
            url,
        });
    }
,

    _handleSuggest: function ({oEvent, url, query = "", oInput = oEvent.getSource()}) {
        let oView = this.getParentViewOrDialogFragment(oInput);
        // if (oInput.getValue() === ""){
        //     oInput.getValue(" ");
        // }

        jQuery.ajax({
            context: this,
            url: url,
            type: "GET",
            data: jQuery.param({
                start: 0,
                limit: 9999,
                query: query
            }),
            success: function (data) {
                let oInputModel = new JSONModel(data);
                oView.setModel(oInputModel, oInput.data('ext_name'));
            },
            error: function (e) {
                MessageToast.show("error: " + e.responseText);
            }
        });

        // if (query) {
        //     aFilters.push(new Filter("text", sap.ui.model.FilterOperator.StartsWith, query));
        // }
        // else {
        //     aFilters.push(new Filter("text", sap.ui.model.FilterOperator.All, ""));
        // }
        // oEvent.getSource().getBinding("suggestionItems").filter(aFilters);
        // var aFilters = [];
    }
,

    /**
     * Used in input fields (ComboElement  + ForeignKeyElement) to set the hidden value when selecting choice
     */
    suggestionItemSelected: function (evt) {

        let oItem = evt.getParameter('selectedItem'),
            sKey = oItem ? oItem.getKey() : '';

        evt.getSource().setSelectedKey(sKey);
        // console.log(evt);
    }
,

    /**
     * Event handler when a expand slave-table/summary button gets pressed
     * @param {sap.ui.base.Event} oEvent the table selectionChange event
     * @public
     *
     * Used in both detail controller and table controller
     */
    handleExpandSlave: function (oEvent) {
        var view = this.getView();
        var mk = this._PK; // wrong for grid, should be get SR,
        var mt = this._content_type;
        this.routeToAction("grid." + oEvent.getSource().data("actor_id"),
            {
                "query": {
                    mk: mk,
                    mt: mt
                }
            }, view.getId());
    }
,

})
})
;
