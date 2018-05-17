/*
*
*  This is for global shortcuts and javascript: hrefs for actions and routing
*  Currently is static, but might change to a template in needed.
*  Included in main.html
*
*/

Lino = {
    window_action: function(){
        sap.ui.getCore().byId("__component0---MAIN_VIEW").getController().routeToAction(...arguments)
    }
};