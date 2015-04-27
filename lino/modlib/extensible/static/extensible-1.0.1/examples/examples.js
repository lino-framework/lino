/*!
 * Extensible 1.0.1
 * Copyright(c) 2010-2011 Extensible, LLC
 * licensing@ext.ensible.com
 * http://ext.ensible.com
 */
Ext.ns('Ext.ensible.sample');

Ext.ensible.sample.msg = function(title, format){
    if(!this.msgCt){
        this.msgCt = Ext.DomHelper.insertFirst(document.body, {id:'msg-div'}, true);
    }
    this.msgCt.alignTo(document, 't-t');
    var s = String.format.apply(String, Array.prototype.slice.call(arguments, 1));
    var m = Ext.DomHelper.append(this.msgCt, {html:'<div class="msg"><h3>' + title + '</h3><p>' + s + '</p></div>'}, true);

    m.slideIn('t').pause(3).ghost('t', {remove:true});
};