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

            if (linodata.fv_index_order !== "") {
                // This is a param action window,
                call_params.http_method = "GET";
                oDialog._linodata['fv_index_order'].split(" ")
            } else {
                // Inserting window.
                call_params.http_method = "POST";
                call_params.sr_needed = false;
                linodata.callback_controller.add_param_values();
                call_params.params = oDialog.getModel("record").getProperty("/data");
            }

            linodata.callback_controller.runSimpleAction(call_params);

        },
        onCancel: function (oEvent) {

        },

        /**
         * Convenince function for getting the attached linodata object which has needed data for submitting the action.
         * @param oEvent
         */
        getLinoData: function (oEvent) {
            let oDialog = this.getParentViewOrDialogFragment(oEvent.getSource());
            oDialog._linodata['an'] = oDialog.data("action_name");
            oDialog._linodata['fv_index_order'] = oDialog.data("param_fields_to_submit");
            return oDialog._linodata;
        },

        submit: function ({action_name, actor_id, sr,}) {

        }
    });


    return controller
});

//sap.ui.getCore().byId("id")