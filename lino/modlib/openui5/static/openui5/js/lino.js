/*
*
*  This is for global shortcuts and javascript: hrefs for actions and routing
*  Currently is static, but might change to a template in needed.
*  Included in main.html
*
*/

Lino = {
    window_action: function () {
        sap.ui.getCore().byId("__component0---MAIN_VIEW").getController().routeToAction(...arguments);
    },

    /**
     * Generalised ajax caller for simple actions.
     * @param actor_id
     * @param action_name
     * @param rp
     * @param is_on_main_actor
     * @param pk
     * @param params
     */
    simple_action: function (actor_id, action_name, rp, is_on_main_actor, pk, params) {
        // console.log(arguments, this.flags);

        // In the case of selecting a workflow button on a table row, we need to stop the navigation.
        this.wave_flag("simple_action", 50); // if run first
        clearTimeout(Lino.timeouts['nav']); // if ran second
        // /api/tickets/TicketsBySite/2308?_dc=1537458453973&mt=36&mk=51&an=mark_opened&sr=2308
        rp = rp || "__component0---MAIN_VIEW";
        sap.ui.getCore().byId(rp).getController().runSimpleAction(
            {
                // Are mt + mk needed, if so how to get MK?
                // mt:
                // mk:
                actor_id: actor_id,
                action_name: action_name,
                rp: rp,
                sr: pk,
                is_on_main_actor: is_on_main_actor,
                params: params
            });
    },

    /**
     * Generalised ajax caller for param action, which need to open a dialog for action parameters.
     * The name of the view should be generated from actor_id and action_name.
     * @param actor_id
     * @param action_name
     * @param rp
     * @param params
     */
    param_action: function (actor_id, action_name, rp, params) {
        // In the case of selecting a workflow button on a table row, we need to stop the navigation.
        this.wave_flag("simple_action", 50); // if run first
        clearTimeout(Lino.timeouts['nav']); // if ran second
        // /api/tickets/TicketsBySite/2308?_dc=1537458453973&mt=36&mk=51&an=mark_opened&sr=2308
        rp = rp || "__component0---MAIN_VIEW";
        sap.ui.getCore().byId(rp).getController().open_window_action(
            {
                actor_id: actor_id,
                action_name: action_name,
                rp: rp,
                params: params
            });
    },

    debounce: function (func, wait, immediate) {
        var timeout;
        return function () {
            var context = this, args = arguments;
            var later = function () {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    },

    /**
     * Object for storing timeout IDs
     * Used for workflow-buttons in table-rows to prevent navigation
     */
    timeouts: {},

    /**
     * Flags that are used to temporarily notify other methods
     * Currently unused
     */

    flags: {},

    wave_flag: function (flag, duration) {
        var me = this;
        this.flags[flag] = true;
        setTimeout(function () {
                me.flags[flag] = undefined
            },
            duration)
    }
};