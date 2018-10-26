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


    let controller = baseController.extend("lino.controller.Fragment", {

        /**
         * Controller for Action Form Panels / Window actions.
         *
         * Information such as action_name and actor_id should be attached to the dialog object after INIT
         *
         * Get the dialog object with `this.getParentViewOrDialogFragment(oEvent.getSource())`.
         */

        /**
         * Should submit the action.
         * @param oEvent
         */
        onOK: function (oEvent) {
            let oDialog = this.getParentViewOrDialogFragment(oEvent.getSource());

            this.oDialog = oDialog; // Save for later when there's no events
            console.log("OK", this._linodata, this.test);
            let linodata = this.getLinoData(oDialog);
            let is_insert_action = linodata.is_insert_action !== "False";
            let call_params = {
                // mk + mt added later
                actor_id: linodata['actor_id'],
                action_name: linodata['an'],
                rp: linodata.callback_controller.getView().getId(),
                sr: linodata.sr,
                select_rows: linodata.select_rows,
                is_on_main_actor: false, //Not sure if right...
                // params: params
            };

            // Extract out only needed field names from record data
            let record_data = oDialog.getModel("record").getProperty("/data");
            call_params.params = {};

            if (is_insert_action) {
                // Inserting window.

                // collect values
                linodata.save_fields.split(" ").forEach(function (field) {
                    if (field in record_data) {
                        call_params.params[field] = record_data[field]
                    }
                    if (field + "Hidden" in record_data) {
                        call_params.params[field + "Hidden"] = record_data[field + "Hidden"]
                    }
                });


                call_params.http_method = "POST";
                linodata.callback_controller.add_param_values(call_params.params); // Only add mk + mt if a running from slave table


            } else {
                // This is a param action window,

                // collect values
                call_params.params.fv = [];
                linodata.save_fields.split(" ").forEach(function (field) {
                    if (field + "Hidden" in record_data) {
                        call_params.params.fv.push(record_data[field + "Hidden"])
                    }
                    else if (field in record_data) {
                        call_params.params.fv.push(record_data[field])
                    }
                    else {
                        call_params.params.fv.push(undefined)
                    }
                });
                if (!linodata.select_rows && linodata.sr.length === 0){
                    call_params.sr = [-99998]
                }
                call_params.http_method = "GET";
                linodata.callback_controller.add_param_values(call_params.params); // Only add mk + mt if a running from slave table


            }

            call_params.success_callback = this.success.bind(this);

            linodata.callback_controller.runSimpleAction(call_params);

        },
        onCancel: function (oEvent) {
            let oDialog = this.getParentViewOrDialogFragment(oEvent.getSource());
            oDialog.close()
        },

        /**
         * Convenince function for getting the attached linodata object which has needed data for submitting the action.
         * @param oEvent
         */
        getLinoData: function (oDialog) {
            if (!oDialog) {
                let oDialog = this.oDialog;
            }
            oDialog._linodata['an'] = oDialog.data("action_name");
            oDialog._linodata['save_fields'] = oDialog.data("save_fields");
            oDialog._linodata['is_insert_action'] = oDialog.data("is_insert_action");
            oDialog._linodata['select_rows'] = oDialog.data("select_rows") === "True";

            return oDialog._linodata;
        },

        submit: function ({action_name, actor_id, sr,}) {

        },

        /**
         * success callback from ajax call
         * Be sure to bind to correct context when running runSimpleAction
         * @param oData AJAX return data
         */
        success: function (oData) {
            this.oDialog.close();
            // this.routeToAction()
        },

        afterClose: function (oEvent) {
            let oDialog = oEvent.getSource();
            this.destroy();
            delete(oDialog._linodata.callback_controller._actions[oDialog._linodata.action_name])
            // context._yesNoDialog = undefined;
            //todo also delete yes json data binding?
        }
    });


    return controller
});

//sap.ui.getCore().byId("id")