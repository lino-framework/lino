describe("Basic Assumptions", function() {

    it("has ExtJS loaded", function() {
        expect(Ext).toBeDefined();
        //~ expect(Ext.getVersion()).toBeTruthy();
        //~ expect(Ext.getVersion().major).toEqual(4);
        expect(Ext.version).toBeTruthy();
        expect(Ext.version).toEqual('3.3.1');
    });

    it("has loaded Lino code",function(){
        expect(Lino).toBeDefined();
    });
});

function grid_window_test(win,bp) {
    if (!bp) bp = {};
    win.default_action.run({ "base_params": bp });
    expect(Lino.current_window).toBeTruthy();
    var grid = Lino.current_window.main_item;
    expect(grid.store).toBeTruthy();
    //~ grid.refresh();
    waitsFor(
        //~ function(){ return !grid.store.isLoading(); },
        function(){ return grid.store.getCount() > 0; },
        "store has at least 1 row",
        1000
    );        
    runs(function(){
        //~ expect(grid.store.getCount()).toBeGreaterThan(3);
    });
    Lino.kill_current_window();
};
/* 
TODO: automatically generate the application-specific part to media/cache/js
*/
describe("Applications-specific", function() {
    it("can run Lino.pcsw.Clients",function(){ 
        grid_window_test(Lino.pcsw.Clients); });
    it("can run Lino.pcsw.UsersWithClients",function(){ 
        grid_window_test(Lino.pcsw.UsersWithClients); });
    it("can run Lino.pcsw.ClientsByCoach1",function(){ 
        grid_window_test(Lino.pcsw.ClientsByCoach1,{"mt":6,"mk":7}); 
    });
});
