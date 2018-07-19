sap.ui.define([
    "lino/controller/baseController",
    "sap/ui/model/json/JSONModel",
    "sap/ui/unified/Menu",
    "sap/ui/unified/MenuItem",
    "sap/m/MessageToast",
    "sap/ui/core/format/DateFormat",
    'sap/m/Button',
    'sap/m/Dialog',
    'sap/m/Text'
], function (baseController, JSONModel, Menu, MenuItem, MessageToast, DateFormat, Button, Dialog, Text) {
    "use strict";

    return baseController.extend("lino.controller.detail", {

        onInit: function () {
            var oView = this.getView();
            this.page_no = 0;
            this.page_limit = this.visibleRowCount;
            this.pv = []; // unused,
            this._PK = null;
            this._actor_id = this.getView().byId("MAIN_PAGE").data("actor_id");

            var oRouter = this.getRouter();
            oRouter.getRoute("detail." + this._actor_id).attachMatched(this._onRouteMatched, this);
        },


        _onRouteMatched: function (oEvent) {
            var oArgs, oView;
            oArgs = oEvent.getParameter("arguments");
            oView = this.getView();

            this.load_record(oArgs.record_id);

        },

        /**
         * Load data for a current object.
         * @public
         * @returns {sap.ui.model.json.JSONModel}
         */
        initSampleDataModel: function () {
            var oModel = new JSONModel();

            var oDateFormat = DateFormat.getDateInstance({source: {pattern: "timestamp"}, pattern: "dd/MM/yyyy"});

            jQuery.ajax(this.getView().byId("MAIN_PAGE").data("url"), {
                dataType: "json",
                data: {limit: 15, fmt: 'json', an: "detail"},
                success: function (oData) {
                    oModel.setData(oData);
                },
                error: function () {
                    jQuery.sap.log.error("failed to load json");
                }
            });
            console.log(this.count++);

            return oModel;
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
            var url = '/api/' + action_url + this._PK;
            MessageToast.show(msg);
            jQuery.ajax({
                url: url,
                type: action_method,
                data: jQuery.param({an: action_name}),
                success: function (data) {
                    if (data && data['success'] && data['xcallback'] !== undefined) {
                        var xcallback = data['xcallback'];
                        if (!this._yesNoDialog) {
                            this._yesNoDialog = sap.ui.jsfragment("lino.fragment.YesNoDialog",
                                data);
                            oView.addDependent(this._yesNoDialog);
                        }


                        this._yesNoDialog.open();
                    }
                    else if (data && data['eval_js'] !== undefined) {
                        var eval_js = data['eval_js'];
                        // eval_js = eval_js.replace("Lino.", "me.");
                        eval(eval_js);
                    }
                    MessageToast.show(data['message']);
                },
                error: function (e) {
                    MessageToast.show("error: " + e);
                }
            });
        },

        open_window_action: function (action, options, history) {
            this.getRouter().navTo(action,
                options, history);
        },

        /***
         * Close YesNoDialog
         */
        onNoDialog: function () {
            var dialog = this.getParent();
            dialog.close();
        },

        getNavport: function () {
            var vp = sap.ui.getCore().byId("__component0---MAIN_VIEW").byId('viewport');
            return vp
        },


        load_record: function (record_id) {
            var oModel = new JSONModel();
            var oView = this.getView();
            this._PK = record_id;
            MessageToast.show("Going to load item with PK of" + record_id);
            oView.setBusy(true);
            jQuery.ajax(oView.byId("MAIN_PAGE").data("url") + record_id, {
                dataType: "json",
                data: {
                    fmt: 'json',
                    an: 'detail'
                },
                success: function (oData) {
                    oModel.setData(oData);
                    oView.setModel(oModel, "record");
                    oView.setBusy(false);
                },
                error: function () {
                    jQuery.sap.log.error("failed to load json");
                }
            });
        },

        onLoaditems: function (oEvent) {
            console.log("loaditems");
        }

    });

});
