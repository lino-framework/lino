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
            var linodata = this.getLinoData(oEvent);

            let call_params = {
                // Are mt + mk needed, if so how to get MK?
                // mt:
                // mk:
                actor_id: linodata['actor_id'],
                action_name: linodata['an'],
                rp: linodata.callback_controller.getView().getId(),
                sr: linodata.sr,
                is_on_main_actor: false, //Not sure if right...
                // params: params
            };

            // Extract out only needed field names from record data
            let record_data = oDialog.getModel("record").getProperty("/data");
            call_params.params = {};
            linodata.save_fields.split(" ").forEach(function (field) {
                if (field in record_data) {
                    call_params.params[field] = record_data[field]
                }
                if (field + "Hidden" in record_data) {
                    call_params.params[field + "Hidden"] = record_data[field + "Hidden"]
                }
            });

            if (linodata.is_insert_action !== "") {
                // Inserting window.
                call_params.http_method = "POST";
                call_params.sr_needed = false;
                linodata.callback_controller.add_param_values();


            } else {
                // This is a param action window,
                call_params.http_method = "GET";

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
        getLinoData: function (oEvent) {
            let oDialog = this.getParentViewOrDialogFragment(oEvent.getSource());
            oDialog._linodata['an'] = oDialog.data("action_name");
            oDialog._linodata['save_fields'] = oDialog.data("save_fields");
            oDialog._linodata['is_insert_action'] = oDialog.data("is_insert_action");

            return oDialog._linodata;
        },

        submit: function ({action_name, actor_id, sr,}) {

        },

        /**
         * success callback from ajax call
         * Be sure to bind to correct context when running runSimpleAction
         * @param oData AJAX return data
         */
        success: function(oData){
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