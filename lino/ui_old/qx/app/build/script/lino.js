(function(){

if (!window.qx) window.qx = {};

qx.$$start = new Date();
  
if (!window.qxsettings) qxsettings = {};
var settings = {"qx.application":"lino.Application","qx.revision":"exported","qx.theme":"lino.theme.Theme","qx.version":"1.4-pre"};
for (var k in settings) qxsettings[k] = settings[k];

if (!window.qxvariants) qxvariants = {};
var variants = {"qx.debug":"off"};
for (var k in variants) qxvariants[k] = variants[k];

if (!qx.$$libraries) qx.$$libraries = {};
var libinfo = {"__out__":{"sourceUri":"/media/qxapp/script"},"lino":{"resourceUri":"/media/qxapp/resource","sourceUri":"/media/qxapp/script","version":"trunk"},"qx":{"resourceUri":"/media/qxapp/resource","sourceUri":"/media/qxapp/script","version":"1.4-pre"}};
for (var k in libinfo) qx.$$libraries[k] = libinfo[k];

qx.$$resources = {};
qx.$$translations = {};
qx.$$locales = {};
qx.$$packageData = {};

qx.$$loader = {
  parts : {"boot":[0]},
  uris : [["__out__:lino.js"]],
  urisBefore : [],
  packageHashes : {"0":"61790270d40f"},
  boot : "boot",
  closureParts : {},
  bootIsInline : true,
  addNoCacheParam : false,
  
  decodeUris : function(compressedUris)
  {
    var libs = qx.$$libraries;
    var uris = [];
    for (var i=0; i<compressedUris.length; i++)
    {
      var uri = compressedUris[i].split(":");
      var euri;
      if (uri.length==2 && uri[0] in libs) {
        var prefix = libs[uri[0]].sourceUri;
        euri = prefix + "/" + uri[1];
      } else {
        euri = compressedUris[i];
      }
      if (qx.$$loader.addNoCacheParam) {
        euri += "?nocache=" + Math.random();
      }
      
      uris.push(euri);
    }
    return uris;      
  }
};  

function loadScript(uri, callback) {
  var elem = document.createElement("script");
  elem.charset = "utf-8";
  elem.src = uri;
  elem.onreadystatechange = elem.onload = function()
  {
    if (!this.readyState || this.readyState == "loaded" || this.readyState == "complete")
    {
      elem.onreadystatechange = elem.onload = null;
      callback();
    }
  };
  var head = document.getElementsByTagName("head")[0];
  head.appendChild(elem);
}

var isWebkit = /AppleWebKit\/([^ ]+)/.test(navigator.userAgent);

function loadScriptList(list, callback) {
  if (list.length == 0) {
    callback();
    return;
  }
  loadScript(list.shift(), function() {
    if (isWebkit) {
      // force asynchronous load
      // Safari fails with an "maximum recursion depth exceeded" error if it is
      // called sync.      
      window.setTimeout(function() {
        loadScriptList(list, callback);
      }, 0);
    } else {
      loadScriptList(list, callback);
    }
  });
}

var fireContentLoadedEvent = function() {
  qx.$$domReady = true;
  document.removeEventListener('DOMContentLoaded', fireContentLoadedEvent, false);
};
if (document.addEventListener) {
  document.addEventListener('DOMContentLoaded', fireContentLoadedEvent, false);
}

qx.$$loader.importPackageData = function (dataMap, callback) {
  if (dataMap["resources"]){
    var resMap = dataMap["resources"];
    for (var k in resMap) qx.$$resources[k] = resMap[k];
  }
  if (dataMap["locales"]){
    var locMap = dataMap["locales"];
    var qxlocs = qx.$$locales;
    for (var lang in locMap){
      if (!qxlocs[lang]) qxlocs[lang] = locMap[lang];
      else 
        for (var k in locMap[lang]) qxlocs[lang][k] = locMap[lang][k];
    }
  }
  if (dataMap["translations"]){
    var trMap   = dataMap["translations"];
    var qxtrans = qx.$$translations;
    for (var lang in trMap){
      if (!qxtrans[lang]) qxtrans[lang] = trMap[lang];
      else 
        for (var k in trMap[lang]) qxtrans[lang][k] = trMap[lang][k];
    }
  }
  if (callback){
    callback(dataMap);
  }
}

qx.$$loader.signalStartup = function () 
{
  qx.$$loader.scriptLoaded = true;
  if (window.qx && qx.event && qx.event.handler && qx.event.handler.Application) {
    qx.event.handler.Application.onScriptLoaded();
    qx.$$loader.applicationHandlerReady = true; 
  } else {
    qx.$$loader.applicationHandlerReady = false;
  }
}

qx.$$loader.init = function(){
  var l=qx.$$loader;
  if (l.urisBefore.length>0){
    loadScriptList(l.urisBefore, function(){
      l.initUris();
    });
  } else {
    l.initUris();
  }
}

qx.$$loader.initUris = function(){
  var l=qx.$$loader;
  var bootPackageHash=l.packageHashes[l.parts[l.boot][0]];
  if (l.bootIsInline){
    l.importPackageData(qx.$$packageData[bootPackageHash]);
    l.signalStartup();
  } else {
    loadScriptList(l.decodeUris(l.uris[l.parts[l.boot]]), function(){
      // Opera needs this extra time to parse the scripts
      window.setTimeout(function(){
        l.importPackageData(qx.$$packageData[bootPackageHash] || {});
        l.signalStartup();
      }, 0);
    });
  }
}
})();

qx.$$packageData['61790270d40f']={"locales":{"C":{"alternateQuotationEnd":"’","alternateQuotationStart":"‘","cldr_am":"AM","cldr_date_format_full":"EEEE, MMMM d, y","cldr_date_format_long":"MMMM d, y","cldr_date_format_medium":"MMM d, y","cldr_date_format_short":"M/d/yy","cldr_date_time_format_EEEd":"d EEE","cldr_date_time_format_Hm":"HH:mm","cldr_date_time_format_Hms":"HH:mm:ss","cldr_date_time_format_M":"L","cldr_date_time_format_MEd":"E, M/d","cldr_date_time_format_MMM":"LLL","cldr_date_time_format_MMMEd":"E, MMM d","cldr_date_time_format_MMMd":"MMM d","cldr_date_time_format_Md":"M/d","cldr_date_time_format_d":"d","cldr_date_time_format_hm":"h:mm a","cldr_date_time_format_hms":"h:mm:ss a","cldr_date_time_format_ms":"mm:ss","cldr_date_time_format_y":"y","cldr_date_time_format_yM":"M/y","cldr_date_time_format_yMEd":"EEE, M/d/y","cldr_date_time_format_yMMM":"MMM y","cldr_date_time_format_yMMMEd":"EEE, MMM d, y","cldr_date_time_format_yQ":"Q y","cldr_date_time_format_yQQQ":"QQQ y","cldr_day_format_abbreviated_fri":"Fri","cldr_day_format_abbreviated_mon":"Mon","cldr_day_format_abbreviated_sat":"Sat","cldr_day_format_abbreviated_sun":"Sun","cldr_day_format_abbreviated_thu":"Thu","cldr_day_format_abbreviated_tue":"Tue","cldr_day_format_abbreviated_wed":"Wed","cldr_day_format_wide_fri":"Friday","cldr_day_format_wide_mon":"Monday","cldr_day_format_wide_sat":"Saturday","cldr_day_format_wide_sun":"Sunday","cldr_day_format_wide_thu":"Thursday","cldr_day_format_wide_tue":"Tuesday","cldr_day_format_wide_wed":"Wednesday","cldr_day_stand-alone_narrow_fri":"F","cldr_day_stand-alone_narrow_mon":"M","cldr_day_stand-alone_narrow_sat":"S","cldr_day_stand-alone_narrow_sun":"S","cldr_day_stand-alone_narrow_thu":"T","cldr_day_stand-alone_narrow_tue":"T","cldr_day_stand-alone_narrow_wed":"W","cldr_month_format_abbreviated_1":"Jan","cldr_month_format_abbreviated_10":"Oct","cldr_month_format_abbreviated_11":"Nov","cldr_month_format_abbreviated_12":"Dec","cldr_month_format_abbreviated_2":"Feb","cldr_month_format_abbreviated_3":"Mar","cldr_month_format_abbreviated_4":"Apr","cldr_month_format_abbreviated_5":"May","cldr_month_format_abbreviated_6":"Jun","cldr_month_format_abbreviated_7":"Jul","cldr_month_format_abbreviated_8":"Aug","cldr_month_format_abbreviated_9":"Sep","cldr_month_format_wide_1":"January","cldr_month_format_wide_10":"October","cldr_month_format_wide_11":"November","cldr_month_format_wide_12":"December","cldr_month_format_wide_2":"February","cldr_month_format_wide_3":"March","cldr_month_format_wide_4":"April","cldr_month_format_wide_5":"May","cldr_month_format_wide_6":"June","cldr_month_format_wide_7":"July","cldr_month_format_wide_8":"August","cldr_month_format_wide_9":"September","cldr_month_stand-alone_narrow_1":"J","cldr_month_stand-alone_narrow_10":"O","cldr_month_stand-alone_narrow_11":"N","cldr_month_stand-alone_narrow_12":"D","cldr_month_stand-alone_narrow_2":"F","cldr_month_stand-alone_narrow_3":"M","cldr_month_stand-alone_narrow_4":"A","cldr_month_stand-alone_narrow_5":"M","cldr_month_stand-alone_narrow_6":"J","cldr_month_stand-alone_narrow_7":"J","cldr_month_stand-alone_narrow_8":"A","cldr_month_stand-alone_narrow_9":"S","cldr_number_decimal_separator":".","cldr_number_group_separator":",","cldr_number_percent_format":"#,##0%","cldr_pm":"PM","cldr_time_format_full":"h:mm:ss a zzzz","cldr_time_format_long":"h:mm:ss a z","cldr_time_format_medium":"h:mm:ss a","cldr_time_format_short":"h:mm a","day":"Day","dayperiod":"AM/PM","era":"Era","hour":"Hour","minute":"Minute","month":"Month","quotationEnd":"”","quotationStart":"“","second":"Second","week":"Week","weekday":"Day of the Week","year":"Year","zone":"Zone"},"en":{"alternateQuotationEnd":"’","alternateQuotationStart":"‘","cldr_am":"AM","cldr_date_format_full":"EEEE, MMMM d, y","cldr_date_format_long":"MMMM d, y","cldr_date_format_medium":"MMM d, y","cldr_date_format_short":"M/d/yy","cldr_date_time_format_EEEd":"d EEE","cldr_date_time_format_Hm":"HH:mm","cldr_date_time_format_Hms":"HH:mm:ss","cldr_date_time_format_M":"L","cldr_date_time_format_MEd":"E, M/d","cldr_date_time_format_MMM":"LLL","cldr_date_time_format_MMMEd":"E, MMM d","cldr_date_time_format_MMMd":"MMM d","cldr_date_time_format_Md":"M/d","cldr_date_time_format_d":"d","cldr_date_time_format_hm":"h:mm a","cldr_date_time_format_hms":"h:mm:ss a","cldr_date_time_format_ms":"mm:ss","cldr_date_time_format_y":"y","cldr_date_time_format_yM":"M/y","cldr_date_time_format_yMEd":"EEE, M/d/y","cldr_date_time_format_yMMM":"MMM y","cldr_date_time_format_yMMMEd":"EEE, MMM d, y","cldr_date_time_format_yQ":"Q y","cldr_date_time_format_yQQQ":"QQQ y","cldr_day_format_abbreviated_fri":"Fri","cldr_day_format_abbreviated_mon":"Mon","cldr_day_format_abbreviated_sat":"Sat","cldr_day_format_abbreviated_sun":"Sun","cldr_day_format_abbreviated_thu":"Thu","cldr_day_format_abbreviated_tue":"Tue","cldr_day_format_abbreviated_wed":"Wed","cldr_day_format_wide_fri":"Friday","cldr_day_format_wide_mon":"Monday","cldr_day_format_wide_sat":"Saturday","cldr_day_format_wide_sun":"Sunday","cldr_day_format_wide_thu":"Thursday","cldr_day_format_wide_tue":"Tuesday","cldr_day_format_wide_wed":"Wednesday","cldr_day_stand-alone_narrow_fri":"F","cldr_day_stand-alone_narrow_mon":"M","cldr_day_stand-alone_narrow_sat":"S","cldr_day_stand-alone_narrow_sun":"S","cldr_day_stand-alone_narrow_thu":"T","cldr_day_stand-alone_narrow_tue":"T","cldr_day_stand-alone_narrow_wed":"W","cldr_month_format_abbreviated_1":"Jan","cldr_month_format_abbreviated_10":"Oct","cldr_month_format_abbreviated_11":"Nov","cldr_month_format_abbreviated_12":"Dec","cldr_month_format_abbreviated_2":"Feb","cldr_month_format_abbreviated_3":"Mar","cldr_month_format_abbreviated_4":"Apr","cldr_month_format_abbreviated_5":"May","cldr_month_format_abbreviated_6":"Jun","cldr_month_format_abbreviated_7":"Jul","cldr_month_format_abbreviated_8":"Aug","cldr_month_format_abbreviated_9":"Sep","cldr_month_format_wide_1":"January","cldr_month_format_wide_10":"October","cldr_month_format_wide_11":"November","cldr_month_format_wide_12":"December","cldr_month_format_wide_2":"February","cldr_month_format_wide_3":"March","cldr_month_format_wide_4":"April","cldr_month_format_wide_5":"May","cldr_month_format_wide_6":"June","cldr_month_format_wide_7":"July","cldr_month_format_wide_8":"August","cldr_month_format_wide_9":"September","cldr_month_stand-alone_narrow_1":"J","cldr_month_stand-alone_narrow_10":"O","cldr_month_stand-alone_narrow_11":"N","cldr_month_stand-alone_narrow_12":"D","cldr_month_stand-alone_narrow_2":"F","cldr_month_stand-alone_narrow_3":"M","cldr_month_stand-alone_narrow_4":"A","cldr_month_stand-alone_narrow_5":"M","cldr_month_stand-alone_narrow_6":"J","cldr_month_stand-alone_narrow_7":"J","cldr_month_stand-alone_narrow_8":"A","cldr_month_stand-alone_narrow_9":"S","cldr_number_decimal_separator":".","cldr_number_group_separator":",","cldr_number_percent_format":"#,##0%","cldr_pm":"PM","cldr_time_format_full":"h:mm:ss a zzzz","cldr_time_format_long":"h:mm:ss a z","cldr_time_format_medium":"h:mm:ss a","cldr_time_format_short":"h:mm a","day":"Day","dayperiod":"AM/PM","era":"Era","hour":"Hour","minute":"Minute","month":"Month","quotationEnd":"”","quotationStart":"“","second":"Second","week":"Week","weekday":"Day of the Week","year":"Year","zone":"Zone"},"fr":{"alternateQuotationEnd":"›","alternateQuotationStart":"‹","cldr_am":"AM","cldr_date_format_full":"EEEE d MMMM y","cldr_date_format_long":"d MMMM y","cldr_date_format_medium":"d MMM y","cldr_date_format_short":"dd/MM/yy","cldr_date_time_format_Ed":"E d","cldr_date_time_format_Hm":"HH:mm","cldr_date_time_format_Hms":"HH:mm:ss","cldr_date_time_format_M":"L","cldr_date_time_format_MEd":"EEE d/M","cldr_date_time_format_MMM":"LLL","cldr_date_time_format_MMMEd":"E d MMM","cldr_date_time_format_MMMMEd":"EEE d MMMM","cldr_date_time_format_MMMd":"d MMM","cldr_date_time_format_MMMdd":"dd MMM","cldr_date_time_format_MMd":"d/MM","cldr_date_time_format_MMdd":"dd/MM","cldr_date_time_format_Md":"d/M","cldr_date_time_format_d":"d","cldr_date_time_format_hm":"h:mm a","cldr_date_time_format_hms":"h:mm:ss a","cldr_date_time_format_ms":"mm:ss","cldr_date_time_format_y":"y","cldr_date_time_format_yM":"M/yyyy","cldr_date_time_format_yMEd":"EEE d/M/yyyy","cldr_date_time_format_yMMM":"MMM y","cldr_date_time_format_yMMMEd":"EEE d MMM y","cldr_date_time_format_yQ":"'T'Q y","cldr_date_time_format_yQQQ":"QQQ y","cldr_date_time_format_yyMM":"MM/yy","cldr_date_time_format_yyMMM":"MMM yy","cldr_date_time_format_yyMMMEEEd":"EEE d MMM yy","cldr_date_time_format_yyMMMd":"d MMM yy","cldr_date_time_format_yyQ":"'T'Q yy","cldr_date_time_format_yyQQQQ":"QQQQ yy","cldr_date_time_format_yyyyMMMM":"MMMM y","cldr_day_format_abbreviated_fri":"ven.","cldr_day_format_abbreviated_mon":"lun.","cldr_day_format_abbreviated_sat":"sam.","cldr_day_format_abbreviated_sun":"dim.","cldr_day_format_abbreviated_thu":"jeu.","cldr_day_format_abbreviated_tue":"mar.","cldr_day_format_abbreviated_wed":"mer.","cldr_day_format_wide_fri":"vendredi","cldr_day_format_wide_mon":"lundi","cldr_day_format_wide_sat":"samedi","cldr_day_format_wide_sun":"dimanche","cldr_day_format_wide_thu":"jeudi","cldr_day_format_wide_tue":"mardi","cldr_day_format_wide_wed":"mercredi","cldr_day_stand-alone_narrow_fri":"V","cldr_day_stand-alone_narrow_mon":"L","cldr_day_stand-alone_narrow_sat":"S","cldr_day_stand-alone_narrow_sun":"D","cldr_day_stand-alone_narrow_thu":"J","cldr_day_stand-alone_narrow_tue":"M","cldr_day_stand-alone_narrow_wed":"M","cldr_month_format_abbreviated_1":"janv.","cldr_month_format_abbreviated_10":"oct.","cldr_month_format_abbreviated_11":"nov.","cldr_month_format_abbreviated_12":"déc.","cldr_month_format_abbreviated_2":"févr.","cldr_month_format_abbreviated_3":"mars","cldr_month_format_abbreviated_4":"avr.","cldr_month_format_abbreviated_5":"mai","cldr_month_format_abbreviated_6":"juin","cldr_month_format_abbreviated_7":"juil.","cldr_month_format_abbreviated_8":"août","cldr_month_format_abbreviated_9":"sept.","cldr_month_format_wide_1":"janvier","cldr_month_format_wide_10":"octobre","cldr_month_format_wide_11":"novembre","cldr_month_format_wide_12":"décembre","cldr_month_format_wide_2":"février","cldr_month_format_wide_3":"mars","cldr_month_format_wide_4":"avril","cldr_month_format_wide_5":"mai","cldr_month_format_wide_6":"juin","cldr_month_format_wide_7":"juillet","cldr_month_format_wide_8":"août","cldr_month_format_wide_9":"septembre","cldr_month_stand-alone_narrow_1":"J","cldr_month_stand-alone_narrow_10":"O","cldr_month_stand-alone_narrow_11":"N","cldr_month_stand-alone_narrow_12":"D","cldr_month_stand-alone_narrow_2":"F","cldr_month_stand-alone_narrow_3":"M","cldr_month_stand-alone_narrow_4":"A","cldr_month_stand-alone_narrow_5":"M","cldr_month_stand-alone_narrow_6":"J","cldr_month_stand-alone_narrow_7":"J","cldr_month_stand-alone_narrow_8":"A","cldr_month_stand-alone_narrow_9":"S","cldr_number_decimal_separator":",","cldr_number_group_separator":" ","cldr_number_percent_format":"#,##0 %","cldr_pm":"PM","cldr_time_format_full":"HH:mm:ss zzzz","cldr_time_format_long":"HH:mm:ss z","cldr_time_format_medium":"HH:mm:ss","cldr_time_format_short":"HH:mm","day":"jour","dayperiod":"cadran","era":"ère","hour":"heure","minute":"minute","month":"mois","quotationEnd":"»","quotationStart":"«","second":"seconde","week":"semaine","weekday":"jour de la semaine","year":"année","zone":"fuseau horaire"}},"resources":{"lino/lino-logo-2.png":[200,147,"png","lino"],"lino/lino.ico":"lino","lino/test.png":[32,32,"png","lino"],"qx/decoration/Modern/app-header.png":[110,20,"png","qx"],"qx/decoration/Modern/arrows-combined.png":[87,8,"png","qx"],"qx/decoration/Modern/arrows/down-invert.png":[8,5,"png","qx","qx/decoration/Modern/arrows-combined.png",-74,0],"qx/decoration/Modern/arrows/down-small-invert.png":[5,3,"png","qx","qx/decoration/Modern/arrows-combined.png",-69,0],"qx/decoration/Modern/arrows/down-small.png":[5,3,"png","qx","qx/decoration/Modern/arrows-combined.png",-49,0],"qx/decoration/Modern/arrows/down.png":[8,5,"png","qx","qx/decoration/Modern/arrows-combined.png",-20,0],"qx/decoration/Modern/arrows/forward.png":[10,8,"png","qx","qx/decoration/Modern/arrows-combined.png",-59,0],"qx/decoration/Modern/arrows/left-invert.png":[5,8,"png","qx","qx/decoration/Modern/arrows-combined.png",0,0],"qx/decoration/Modern/arrows/left.png":[5,8,"png","qx","qx/decoration/Modern/arrows-combined.png",-44,0],"qx/decoration/Modern/arrows/rewind.png":[10,8,"png","qx","qx/decoration/Modern/arrows-combined.png",-10,0],"qx/decoration/Modern/arrows/right-invert.png":[5,8,"png","qx","qx/decoration/Modern/arrows-combined.png",-5,0],"qx/decoration/Modern/arrows/right.png":[5,8,"png","qx","qx/decoration/Modern/arrows-combined.png",-54,0],"qx/decoration/Modern/arrows/up-invert.png":[8,5,"png","qx","qx/decoration/Modern/arrows-combined.png",-28,0],"qx/decoration/Modern/arrows/up-small.png":[5,3,"png","qx","qx/decoration/Modern/arrows-combined.png",-82,0],"qx/decoration/Modern/arrows/up.png":[8,5,"png","qx","qx/decoration/Modern/arrows-combined.png",-36,0],"qx/decoration/Modern/button-lr-combined.png":[72,52,"png","qx"],"qx/decoration/Modern/button-tb-combined.png":[4,216,"png","qx"],"qx/decoration/Modern/checkradio-combined.png":[504,14,"png","qx"],"qx/decoration/Modern/colorselector-combined.gif":[46,11,"gif","qx"],"qx/decoration/Modern/colorselector/brightness-field.png":[19,256,"png","qx"],"qx/decoration/Modern/colorselector/brightness-handle.gif":[35,11,"gif","qx","qx/decoration/Modern/colorselector-combined.gif",0,0],"qx/decoration/Modern/colorselector/huesaturation-field.jpg":[256,256,"jpeg","qx"],"qx/decoration/Modern/colorselector/huesaturation-handle.gif":[11,11,"gif","qx","qx/decoration/Modern/colorselector-combined.gif",-35,0],"qx/decoration/Modern/cursors-combined.gif":[71,20,"gif","qx"],"qx/decoration/Modern/cursors/alias.gif":[19,15,"gif","qx","qx/decoration/Modern/cursors-combined.gif",-52,0],"qx/decoration/Modern/cursors/copy.gif":[19,15,"gif","qx","qx/decoration/Modern/cursors-combined.gif",-33,0],"qx/decoration/Modern/cursors/move.gif":[13,9,"gif","qx","qx/decoration/Modern/cursors-combined.gif",-20,0],"qx/decoration/Modern/cursors/nodrop.gif":[20,20,"gif","qx","qx/decoration/Modern/cursors-combined.gif",0,0],"qx/decoration/Modern/form/button-b.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-72],"qx/decoration/Modern/form/button-bl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-204],"qx/decoration/Modern/form/button-br.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-188],"qx/decoration/Modern/form/button-c.png":[40,52,"png","qx"],"qx/decoration/Modern/form/button-checked-b.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-36],"qx/decoration/Modern/form/button-checked-bl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-84],"qx/decoration/Modern/form/button-checked-br.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-184],"qx/decoration/Modern/form/button-checked-c.png":[40,52,"png","qx"],"qx/decoration/Modern/form/button-checked-focused-b.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-156],"qx/decoration/Modern/form/button-checked-focused-bl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-208],"qx/decoration/Modern/form/button-checked-focused-br.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-160],"qx/decoration/Modern/form/button-checked-focused-c.png":[40,52,"png","qx"],"qx/decoration/Modern/form/button-checked-focused-l.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-40,0],"qx/decoration/Modern/form/button-checked-focused-r.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-32,0],"qx/decoration/Modern/form/button-checked-focused-t.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-28],"qx/decoration/Modern/form/button-checked-focused-tl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-24],"qx/decoration/Modern/form/button-checked-focused-tr.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-48],"qx/decoration/Modern/form/button-checked-focused.png":[80,60,"png","qx"],"qx/decoration/Modern/form/button-checked-l.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-16,0],"qx/decoration/Modern/form/button-checked-r.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-60,0],"qx/decoration/Modern/form/button-checked-t.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-140],"qx/decoration/Modern/form/button-checked-tl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-56],"qx/decoration/Modern/form/button-checked-tr.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-112],"qx/decoration/Modern/form/button-checked.png":[80,60,"png","qx"],"qx/decoration/Modern/form/button-disabled-b.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-40],"qx/decoration/Modern/form/button-disabled-bl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-136],"qx/decoration/Modern/form/button-disabled-br.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-16],"qx/decoration/Modern/form/button-disabled-c.png":[40,52,"png","qx"],"qx/decoration/Modern/form/button-disabled-l.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-68,0],"qx/decoration/Modern/form/button-disabled-r.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-4,0],"qx/decoration/Modern/form/button-disabled-t.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-116],"qx/decoration/Modern/form/button-disabled-tl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-168],"qx/decoration/Modern/form/button-disabled-tr.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-60],"qx/decoration/Modern/form/button-disabled.png":[80,60,"png","qx"],"qx/decoration/Modern/form/button-focused-b.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-68],"qx/decoration/Modern/form/button-focused-bl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-144],"qx/decoration/Modern/form/button-focused-br.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-8],"qx/decoration/Modern/form/button-focused-c.png":[40,52,"png","qx"],"qx/decoration/Modern/form/button-focused-l.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-24,0],"qx/decoration/Modern/form/button-focused-r.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-44,0],"qx/decoration/Modern/form/button-focused-t.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-192],"qx/decoration/Modern/form/button-focused-tl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-148],"qx/decoration/Modern/form/button-focused-tr.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-104],"qx/decoration/Modern/form/button-focused.png":[80,60,"png","qx"],"qx/decoration/Modern/form/button-hovered-b.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-108],"qx/decoration/Modern/form/button-hovered-bl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-32],"qx/decoration/Modern/form/button-hovered-br.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-128],"qx/decoration/Modern/form/button-hovered-c.png":[40,52,"png","qx"],"qx/decoration/Modern/form/button-hovered-l.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-20,0],"qx/decoration/Modern/form/button-hovered-r.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-48,0],"qx/decoration/Modern/form/button-hovered-t.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-44],"qx/decoration/Modern/form/button-hovered-tl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-76],"qx/decoration/Modern/form/button-hovered-tr.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-88],"qx/decoration/Modern/form/button-hovered.png":[80,60,"png","qx"],"qx/decoration/Modern/form/button-l.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-56,0],"qx/decoration/Modern/form/button-preselected-b.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-124],"qx/decoration/Modern/form/button-preselected-bl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-176],"qx/decoration/Modern/form/button-preselected-br.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-200],"qx/decoration/Modern/form/button-preselected-c.png":[40,52,"png","qx"],"qx/decoration/Modern/form/button-preselected-focused-b.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,0],"qx/decoration/Modern/form/button-preselected-focused-bl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-4],"qx/decoration/Modern/form/button-preselected-focused-br.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-152],"qx/decoration/Modern/form/button-preselected-focused-c.png":[40,52,"png","qx"],"qx/decoration/Modern/form/button-preselected-focused-l.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-28,0],"qx/decoration/Modern/form/button-preselected-focused-r.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-36,0],"qx/decoration/Modern/form/button-preselected-focused-t.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-196],"qx/decoration/Modern/form/button-preselected-focused-tl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-164],"qx/decoration/Modern/form/button-preselected-focused-tr.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-212],"qx/decoration/Modern/form/button-preselected-focused.png":[80,60,"png","qx"],"qx/decoration/Modern/form/button-preselected-l.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-8,0],"qx/decoration/Modern/form/button-preselected-r.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-64,0],"qx/decoration/Modern/form/button-preselected-t.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-96],"qx/decoration/Modern/form/button-preselected-tl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-80],"qx/decoration/Modern/form/button-preselected-tr.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-132],"qx/decoration/Modern/form/button-preselected.png":[80,60,"png","qx"],"qx/decoration/Modern/form/button-pressed-b.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-12],"qx/decoration/Modern/form/button-pressed-bl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-52],"qx/decoration/Modern/form/button-pressed-br.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-20],"qx/decoration/Modern/form/button-pressed-c.png":[40,52,"png","qx"],"qx/decoration/Modern/form/button-pressed-l.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-52,0],"qx/decoration/Modern/form/button-pressed-r.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",-12,0],"qx/decoration/Modern/form/button-pressed-t.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-100],"qx/decoration/Modern/form/button-pressed-tl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-172],"qx/decoration/Modern/form/button-pressed-tr.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-64],"qx/decoration/Modern/form/button-pressed.png":[80,60,"png","qx"],"qx/decoration/Modern/form/button-r.png":[4,52,"png","qx","qx/decoration/Modern/button-lr-combined.png",0,0],"qx/decoration/Modern/form/button-t.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-92],"qx/decoration/Modern/form/button-tl.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-120],"qx/decoration/Modern/form/button-tr.png":[4,4,"png","qx","qx/decoration/Modern/button-tb-combined.png",0,-180],"qx/decoration/Modern/form/button.png":[80,60,"png","qx"],"qx/decoration/Modern/form/checkbox-checked-disabled.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-126,0],"qx/decoration/Modern/form/checkbox-checked-focused-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-322,0],"qx/decoration/Modern/form/checkbox-checked-focused.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-294,0],"qx/decoration/Modern/form/checkbox-checked-hovered-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-364,0],"qx/decoration/Modern/form/checkbox-checked-hovered.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-490,0],"qx/decoration/Modern/form/checkbox-checked-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-224,0],"qx/decoration/Modern/form/checkbox-checked-pressed-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-378,0],"qx/decoration/Modern/form/checkbox-checked-pressed.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-84,0],"qx/decoration/Modern/form/checkbox-checked.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-182,0],"qx/decoration/Modern/form/checkbox-disabled.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-42,0],"qx/decoration/Modern/form/checkbox-focused-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-392,0],"qx/decoration/Modern/form/checkbox-focused.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-210,0],"qx/decoration/Modern/form/checkbox-hovered-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-14,0],"qx/decoration/Modern/form/checkbox-hovered.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-238,0],"qx/decoration/Modern/form/checkbox-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-462,0],"qx/decoration/Modern/form/checkbox-pressed-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-112,0],"qx/decoration/Modern/form/checkbox-pressed.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-448,0],"qx/decoration/Modern/form/checkbox-undetermined-disabled.png":[14,14,"png","qx"],"qx/decoration/Modern/form/checkbox-undetermined-focused-invalid.png":[14,14,"png","qx"],"qx/decoration/Modern/form/checkbox-undetermined-focused.png":[14,14,"png","qx"],"qx/decoration/Modern/form/checkbox-undetermined-hovered-invalid.png":[14,14,"png","qx"],"qx/decoration/Modern/form/checkbox-undetermined-hovered.png":[14,14,"png","qx"],"qx/decoration/Modern/form/checkbox-undetermined-invalid.png":[14,14,"png","qx"],"qx/decoration/Modern/form/checkbox-undetermined.png":[14,14,"png","qx"],"qx/decoration/Modern/form/checkbox.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-140,0],"qx/decoration/Modern/form/checked-disabled.png":[6,6,"png","qx"],"qx/decoration/Modern/form/checked.png":[6,6,"png","qx"],"qx/decoration/Modern/form/input-focused.png":[40,12,"png","qx"],"qx/decoration/Modern/form/input.png":[84,12,"png","qx"],"qx/decoration/Modern/form/radiobutton-checked-disabled.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-196,0],"qx/decoration/Modern/form/radiobutton-checked-focused-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-168,0],"qx/decoration/Modern/form/radiobutton-checked-focused.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-98,0],"qx/decoration/Modern/form/radiobutton-checked-hovered-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-308,0],"qx/decoration/Modern/form/radiobutton-checked-hovered.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-406,0],"qx/decoration/Modern/form/radiobutton-checked-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-28,0],"qx/decoration/Modern/form/radiobutton-checked-pressed-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-350,0],"qx/decoration/Modern/form/radiobutton-checked-pressed.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-266,0],"qx/decoration/Modern/form/radiobutton-checked.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-252,0],"qx/decoration/Modern/form/radiobutton-disabled.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-336,0],"qx/decoration/Modern/form/radiobutton-focused-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-476,0],"qx/decoration/Modern/form/radiobutton-focused.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-420,0],"qx/decoration/Modern/form/radiobutton-hovered-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-56,0],"qx/decoration/Modern/form/radiobutton-hovered.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",0,0],"qx/decoration/Modern/form/radiobutton-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-154,0],"qx/decoration/Modern/form/radiobutton-pressed-invalid.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-434,0],"qx/decoration/Modern/form/radiobutton-pressed.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-280,0],"qx/decoration/Modern/form/radiobutton.png":[14,14,"png","qx","qx/decoration/Modern/checkradio-combined.png",-70,0],"qx/decoration/Modern/form/tooltip-error-arrow.png":[11,14,"png","qx"],"qx/decoration/Modern/form/tooltip-error-b.png":[6,6,"png","qx","qx/decoration/Modern/tooltip-error-tb-combined.png",0,-30],"qx/decoration/Modern/form/tooltip-error-bl.png":[6,6,"png","qx","qx/decoration/Modern/tooltip-error-tb-combined.png",0,-24],"qx/decoration/Modern/form/tooltip-error-br.png":[6,6,"png","qx","qx/decoration/Modern/tooltip-error-tb-combined.png",0,0],"qx/decoration/Modern/form/tooltip-error-c.png":[40,18,"png","qx"],"qx/decoration/Modern/form/tooltip-error-l.png":[6,18,"png","qx","qx/decoration/Modern/tooltip-error-lr-combined.png",-6,0],"qx/decoration/Modern/form/tooltip-error-r.png":[6,18,"png","qx","qx/decoration/Modern/tooltip-error-lr-combined.png",0,0],"qx/decoration/Modern/form/tooltip-error-t.png":[6,6,"png","qx","qx/decoration/Modern/tooltip-error-tb-combined.png",0,-6],"qx/decoration/Modern/form/tooltip-error-tl.png":[6,6,"png","qx","qx/decoration/Modern/tooltip-error-tb-combined.png",0,-18],"qx/decoration/Modern/form/tooltip-error-tr.png":[6,6,"png","qx","qx/decoration/Modern/tooltip-error-tb-combined.png",0,-12],"qx/decoration/Modern/form/tooltip-error.png":[127,30,"png","qx"],"qx/decoration/Modern/form/undetermined-disabled.png":[6,2,"png","qx"],"qx/decoration/Modern/form/undetermined.png":[6,2,"png","qx"],"qx/decoration/Modern/group-item.png":[110,20,"png","qx"],"qx/decoration/Modern/groupbox-lr-combined.png":[8,51,"png","qx"],"qx/decoration/Modern/groupbox-tb-combined.png":[4,24,"png","qx"],"qx/decoration/Modern/groupbox/groupbox-b.png":[4,4,"png","qx","qx/decoration/Modern/groupbox-tb-combined.png",0,-12],"qx/decoration/Modern/groupbox/groupbox-bl.png":[4,4,"png","qx","qx/decoration/Modern/groupbox-tb-combined.png",0,-16],"qx/decoration/Modern/groupbox/groupbox-br.png":[4,4,"png","qx","qx/decoration/Modern/groupbox-tb-combined.png",0,-8],"qx/decoration/Modern/groupbox/groupbox-c.png":[40,51,"png","qx"],"qx/decoration/Modern/groupbox/groupbox-l.png":[4,51,"png","qx","qx/decoration/Modern/groupbox-lr-combined.png",-4,0],"qx/decoration/Modern/groupbox/groupbox-r.png":[4,51,"png","qx","qx/decoration/Modern/groupbox-lr-combined.png",0,0],"qx/decoration/Modern/groupbox/groupbox-t.png":[4,4,"png","qx","qx/decoration/Modern/groupbox-tb-combined.png",0,-4],"qx/decoration/Modern/groupbox/groupbox-tl.png":[4,4,"png","qx","qx/decoration/Modern/groupbox-tb-combined.png",0,0],"qx/decoration/Modern/groupbox/groupbox-tr.png":[4,4,"png","qx","qx/decoration/Modern/groupbox-tb-combined.png",0,-20],"qx/decoration/Modern/groupbox/groupbox.png":[255,59,"png","qx"],"qx/decoration/Modern/menu-background-combined.png":[80,49,"png","qx"],"qx/decoration/Modern/menu-checkradio-combined.gif":[64,7,"gif","qx"],"qx/decoration/Modern/menu/background.png":[40,49,"png","qx","qx/decoration/Modern/menu-background-combined.png",-40,0],"qx/decoration/Modern/menu/bar-background.png":[40,20,"png","qx","qx/decoration/Modern/menu-background-combined.png",0,0],"qx/decoration/Modern/menu/checkbox-invert.gif":[16,7,"gif","qx","qx/decoration/Modern/menu-checkradio-combined.gif",-16,0],"qx/decoration/Modern/menu/checkbox.gif":[16,7,"gif","qx","qx/decoration/Modern/menu-checkradio-combined.gif",-48,0],"qx/decoration/Modern/menu/radiobutton-invert.gif":[16,5,"gif","qx","qx/decoration/Modern/menu-checkradio-combined.gif",-32,0],"qx/decoration/Modern/menu/radiobutton.gif":[16,5,"gif","qx","qx/decoration/Modern/menu-checkradio-combined.gif",0,0],"qx/decoration/Modern/pane-lr-combined.png":[12,238,"png","qx"],"qx/decoration/Modern/pane-tb-combined.png":[6,36,"png","qx"],"qx/decoration/Modern/pane/pane-b.png":[6,6,"png","qx","qx/decoration/Modern/pane-tb-combined.png",0,-30],"qx/decoration/Modern/pane/pane-bl.png":[6,6,"png","qx","qx/decoration/Modern/pane-tb-combined.png",0,-18],"qx/decoration/Modern/pane/pane-br.png":[6,6,"png","qx","qx/decoration/Modern/pane-tb-combined.png",0,-12],"qx/decoration/Modern/pane/pane-c.png":[40,238,"png","qx"],"qx/decoration/Modern/pane/pane-l.png":[6,238,"png","qx","qx/decoration/Modern/pane-lr-combined.png",0,0],"qx/decoration/Modern/pane/pane-r.png":[6,238,"png","qx","qx/decoration/Modern/pane-lr-combined.png",-6,0],"qx/decoration/Modern/pane/pane-t.png":[6,6,"png","qx","qx/decoration/Modern/pane-tb-combined.png",0,0],"qx/decoration/Modern/pane/pane-tl.png":[6,6,"png","qx","qx/decoration/Modern/pane-tb-combined.png",0,-24],"qx/decoration/Modern/pane/pane-tr.png":[6,6,"png","qx","qx/decoration/Modern/pane-tb-combined.png",0,-6],"qx/decoration/Modern/pane/pane.png":[185,250,"png","qx"],"qx/decoration/Modern/scrollbar-combined.png":[54,12,"png","qx"],"qx/decoration/Modern/scrollbar/scrollbar-bg-horizontal.png":[76,15,"png","qx"],"qx/decoration/Modern/scrollbar/scrollbar-bg-pressed-horizontal.png":[19,10,"png","qx"],"qx/decoration/Modern/scrollbar/scrollbar-bg-pressed-vertical.png":[10,19,"png","qx"],"qx/decoration/Modern/scrollbar/scrollbar-bg-vertical.png":[15,76,"png","qx"],"qx/decoration/Modern/scrollbar/scrollbar-button-bg-horizontal.png":[12,10,"png","qx","qx/decoration/Modern/scrollbar-combined.png",-34,0],"qx/decoration/Modern/scrollbar/scrollbar-button-bg-vertical.png":[10,12,"png","qx","qx/decoration/Modern/scrollbar-combined.png",-6,0],"qx/decoration/Modern/scrollbar/scrollbar-down.png":[6,4,"png","qx","qx/decoration/Modern/scrollbar-combined.png",-28,0],"qx/decoration/Modern/scrollbar/scrollbar-left.png":[4,6,"png","qx","qx/decoration/Modern/scrollbar-combined.png",-50,0],"qx/decoration/Modern/scrollbar/scrollbar-right.png":[4,6,"png","qx","qx/decoration/Modern/scrollbar-combined.png",-46,0],"qx/decoration/Modern/scrollbar/scrollbar-up.png":[6,4,"png","qx","qx/decoration/Modern/scrollbar-combined.png",0,0],"qx/decoration/Modern/scrollbar/slider-knob-background.png":[12,10,"png","qx","qx/decoration/Modern/scrollbar-combined.png",-16,0],"qx/decoration/Modern/selection.png":[110,20,"png","qx"],"qx/decoration/Modern/shadow-lr-combined.png":[30,382,"png","qx"],"qx/decoration/Modern/shadow-small-lr-combined.png":[10,136,"png","qx"],"qx/decoration/Modern/shadow-small-tb-combined.png":[5,30,"png","qx"],"qx/decoration/Modern/shadow-tb-combined.png":[15,90,"png","qx"],"qx/decoration/Modern/shadow/shadow-b.png":[15,15,"png","qx","qx/decoration/Modern/shadow-tb-combined.png",0,-30],"qx/decoration/Modern/shadow/shadow-bl.png":[15,15,"png","qx","qx/decoration/Modern/shadow-tb-combined.png",0,-15],"qx/decoration/Modern/shadow/shadow-br.png":[15,15,"png","qx","qx/decoration/Modern/shadow-tb-combined.png",0,-45],"qx/decoration/Modern/shadow/shadow-c.png":[40,382,"png","qx"],"qx/decoration/Modern/shadow/shadow-l.png":[15,382,"png","qx","qx/decoration/Modern/shadow-lr-combined.png",0,0],"qx/decoration/Modern/shadow/shadow-r.png":[15,382,"png","qx","qx/decoration/Modern/shadow-lr-combined.png",-15,0],"qx/decoration/Modern/shadow/shadow-small-b.png":[5,5,"png","qx","qx/decoration/Modern/shadow-small-tb-combined.png",0,-20],"qx/decoration/Modern/shadow/shadow-small-bl.png":[5,5,"png","qx","qx/decoration/Modern/shadow-small-tb-combined.png",0,-15],"qx/decoration/Modern/shadow/shadow-small-br.png":[5,5,"png","qx","qx/decoration/Modern/shadow-small-tb-combined.png",0,-10],"qx/decoration/Modern/shadow/shadow-small-c.png":[40,136,"png","qx"],"qx/decoration/Modern/shadow/shadow-small-l.png":[5,136,"png","qx","qx/decoration/Modern/shadow-small-lr-combined.png",0,0],"qx/decoration/Modern/shadow/shadow-small-r.png":[5,136,"png","qx","qx/decoration/Modern/shadow-small-lr-combined.png",-5,0],"qx/decoration/Modern/shadow/shadow-small-t.png":[5,5,"png","qx","qx/decoration/Modern/shadow-small-tb-combined.png",0,-5],"qx/decoration/Modern/shadow/shadow-small-tl.png":[5,5,"png","qx","qx/decoration/Modern/shadow-small-tb-combined.png",0,0],"qx/decoration/Modern/shadow/shadow-small-tr.png":[5,5,"png","qx","qx/decoration/Modern/shadow-small-tb-combined.png",0,-25],"qx/decoration/Modern/shadow/shadow-small.png":[114,146,"png","qx"],"qx/decoration/Modern/shadow/shadow-t.png":[15,15,"png","qx","qx/decoration/Modern/shadow-tb-combined.png",0,-60],"qx/decoration/Modern/shadow/shadow-tl.png":[15,15,"png","qx","qx/decoration/Modern/shadow-tb-combined.png",0,-75],"qx/decoration/Modern/shadow/shadow-tr.png":[15,15,"png","qx","qx/decoration/Modern/shadow-tb-combined.png",0,0],"qx/decoration/Modern/shadow/shadow.png":[381,412,"png","qx"],"qx/decoration/Modern/splitpane-knobs-combined.png":[8,9,"png","qx"],"qx/decoration/Modern/splitpane/knob-horizontal.png":[1,8,"png","qx","qx/decoration/Modern/splitpane-knobs-combined.png",0,-1],"qx/decoration/Modern/splitpane/knob-vertical.png":[8,1,"png","qx","qx/decoration/Modern/splitpane-knobs-combined.png",0,0],"qx/decoration/Modern/table-combined.png":[94,18,"png","qx"],"qx/decoration/Modern/table/ascending.png":[8,5,"png","qx","qx/decoration/Modern/table-combined.png",0,0],"qx/decoration/Modern/table/boolean-false.png":[14,14,"png","qx","qx/decoration/Modern/table-combined.png",-80,0],"qx/decoration/Modern/table/boolean-true.png":[14,14,"png","qx","qx/decoration/Modern/table-combined.png",-26,0],"qx/decoration/Modern/table/descending.png":[8,5,"png","qx","qx/decoration/Modern/table-combined.png",-18,0],"qx/decoration/Modern/table/header-cell.png":[40,18,"png","qx","qx/decoration/Modern/table-combined.png",-40,0],"qx/decoration/Modern/table/select-column-order.png":[10,9,"png","qx","qx/decoration/Modern/table-combined.png",-8,0],"qx/decoration/Modern/tabview-button-bottom-active-lr-combined.png":[10,14,"png","qx"],"qx/decoration/Modern/tabview-button-bottom-active-tb-combined.png":[5,30,"png","qx"],"qx/decoration/Modern/tabview-button-bottom-inactive-b-combined.png":[3,9,"png","qx"],"qx/decoration/Modern/tabview-button-bottom-inactive-lr-combined.png":[6,15,"png","qx"],"qx/decoration/Modern/tabview-button-bottom-inactive-t-combined.png":[3,9,"png","qx"],"qx/decoration/Modern/tabview-button-left-active-lr-combined.png":[10,37,"png","qx"],"qx/decoration/Modern/tabview-button-left-active-tb-combined.png":[5,30,"png","qx"],"qx/decoration/Modern/tabview-button-left-inactive-b-combined.png":[3,9,"png","qx"],"qx/decoration/Modern/tabview-button-left-inactive-lr-combined.png":[6,39,"png","qx"],"qx/decoration/Modern/tabview-button-left-inactive-t-combined.png":[3,9,"png","qx"],"qx/decoration/Modern/tabview-button-right-active-lr-combined.png":[10,37,"png","qx"],"qx/decoration/Modern/tabview-button-right-active-tb-combined.png":[5,30,"png","qx"],"qx/decoration/Modern/tabview-button-right-inactive-b-combined.png":[3,9,"png","qx"],"qx/decoration/Modern/tabview-button-right-inactive-lr-combined.png":[6,39,"png","qx"],"qx/decoration/Modern/tabview-button-right-inactive-t-combined.png":[3,9,"png","qx"],"qx/decoration/Modern/tabview-button-top-active-lr-combined.png":[10,12,"png","qx"],"qx/decoration/Modern/tabview-button-top-active-tb-combined.png":[5,30,"png","qx"],"qx/decoration/Modern/tabview-button-top-inactive-b-combined.png":[3,9,"png","qx"],"qx/decoration/Modern/tabview-button-top-inactive-lr-combined.png":[6,15,"png","qx"],"qx/decoration/Modern/tabview-button-top-inactive-t-combined.png":[3,9,"png","qx"],"qx/decoration/Modern/tabview-pane-lr-combined.png":[60,2,"png","qx"],"qx/decoration/Modern/tabview-pane-tb-combined.png":[30,180,"png","qx"],"qx/decoration/Modern/tabview/tab-button-bottom-active-b.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-bottom-active-tb-combined.png",0,-10],"qx/decoration/Modern/tabview/tab-button-bottom-active-bl.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-bottom-active-tb-combined.png",0,-15],"qx/decoration/Modern/tabview/tab-button-bottom-active-br.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-bottom-active-tb-combined.png",0,-5],"qx/decoration/Modern/tabview/tab-button-bottom-active-c.png":[40,14,"png","qx"],"qx/decoration/Modern/tabview/tab-button-bottom-active-l.png":[5,14,"png","qx","qx/decoration/Modern/tabview-button-bottom-active-lr-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-bottom-active-r.png":[5,14,"png","qx","qx/decoration/Modern/tabview-button-bottom-active-lr-combined.png",-5,0],"qx/decoration/Modern/tabview/tab-button-bottom-active-t.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-bottom-active-tb-combined.png",0,-20],"qx/decoration/Modern/tabview/tab-button-bottom-active-tl.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-bottom-active-tb-combined.png",0,-25],"qx/decoration/Modern/tabview/tab-button-bottom-active-tr.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-bottom-active-tb-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-bottom-active.png":[49,24,"png","qx"],"qx/decoration/Modern/tabview/tab-button-bottom-inactive-b.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-bottom-inactive-b-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-bottom-inactive-bl.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-bottom-inactive-b-combined.png",0,-6],"qx/decoration/Modern/tabview/tab-button-bottom-inactive-br.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-bottom-inactive-b-combined.png",0,-3],"qx/decoration/Modern/tabview/tab-button-bottom-inactive-c.png":[40,15,"png","qx"],"qx/decoration/Modern/tabview/tab-button-bottom-inactive-l.png":[3,15,"png","qx","qx/decoration/Modern/tabview-button-bottom-inactive-lr-combined.png",-3,0],"qx/decoration/Modern/tabview/tab-button-bottom-inactive-r.png":[3,15,"png","qx","qx/decoration/Modern/tabview-button-bottom-inactive-lr-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-bottom-inactive-t.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-bottom-inactive-t-combined.png",0,-3],"qx/decoration/Modern/tabview/tab-button-bottom-inactive-tl.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-bottom-inactive-t-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-bottom-inactive-tr.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-bottom-inactive-t-combined.png",0,-6],"qx/decoration/Modern/tabview/tab-button-bottom-inactive.png":[45,21,"png","qx"],"qx/decoration/Modern/tabview/tab-button-left-active-b.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-left-active-tb-combined.png",0,-5],"qx/decoration/Modern/tabview/tab-button-left-active-bl.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-left-active-tb-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-left-active-br.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-left-active-tb-combined.png",0,-25],"qx/decoration/Modern/tabview/tab-button-left-active-c.png":[40,37,"png","qx"],"qx/decoration/Modern/tabview/tab-button-left-active-l.png":[5,37,"png","qx","qx/decoration/Modern/tabview-button-left-active-lr-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-left-active-r.png":[5,37,"png","qx","qx/decoration/Modern/tabview-button-left-active-lr-combined.png",-5,0],"qx/decoration/Modern/tabview/tab-button-left-active-t.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-left-active-tb-combined.png",0,-15],"qx/decoration/Modern/tabview/tab-button-left-active-tl.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-left-active-tb-combined.png",0,-10],"qx/decoration/Modern/tabview/tab-button-left-active-tr.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-left-active-tb-combined.png",0,-20],"qx/decoration/Modern/tabview/tab-button-left-active.png":[22,47,"png","qx"],"qx/decoration/Modern/tabview/tab-button-left-inactive-b.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-left-inactive-b-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-left-inactive-bl.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-left-inactive-b-combined.png",0,-6],"qx/decoration/Modern/tabview/tab-button-left-inactive-br.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-left-inactive-b-combined.png",0,-3],"qx/decoration/Modern/tabview/tab-button-left-inactive-c.png":[40,39,"png","qx"],"qx/decoration/Modern/tabview/tab-button-left-inactive-l.png":[3,39,"png","qx","qx/decoration/Modern/tabview-button-left-inactive-lr-combined.png",-3,0],"qx/decoration/Modern/tabview/tab-button-left-inactive-r.png":[3,39,"png","qx","qx/decoration/Modern/tabview-button-left-inactive-lr-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-left-inactive-t.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-left-inactive-t-combined.png",0,-3],"qx/decoration/Modern/tabview/tab-button-left-inactive-tl.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-left-inactive-t-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-left-inactive-tr.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-left-inactive-t-combined.png",0,-6],"qx/decoration/Modern/tabview/tab-button-left-inactive.png":[20,45,"png","qx"],"qx/decoration/Modern/tabview/tab-button-right-active-b.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-right-active-tb-combined.png",0,-25],"qx/decoration/Modern/tabview/tab-button-right-active-bl.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-right-active-tb-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-right-active-br.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-right-active-tb-combined.png",0,-20],"qx/decoration/Modern/tabview/tab-button-right-active-c.png":[40,37,"png","qx"],"qx/decoration/Modern/tabview/tab-button-right-active-l.png":[5,37,"png","qx","qx/decoration/Modern/tabview-button-right-active-lr-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-right-active-r.png":[5,37,"png","qx","qx/decoration/Modern/tabview-button-right-active-lr-combined.png",-5,0],"qx/decoration/Modern/tabview/tab-button-right-active-t.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-right-active-tb-combined.png",0,-5],"qx/decoration/Modern/tabview/tab-button-right-active-tl.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-right-active-tb-combined.png",0,-15],"qx/decoration/Modern/tabview/tab-button-right-active-tr.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-right-active-tb-combined.png",0,-10],"qx/decoration/Modern/tabview/tab-button-right-active.png":[22,47,"png","qx"],"qx/decoration/Modern/tabview/tab-button-right-inactive-b.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-right-inactive-b-combined.png",0,-3],"qx/decoration/Modern/tabview/tab-button-right-inactive-bl.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-right-inactive-b-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-right-inactive-br.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-right-inactive-b-combined.png",0,-6],"qx/decoration/Modern/tabview/tab-button-right-inactive-c.png":[40,39,"png","qx"],"qx/decoration/Modern/tabview/tab-button-right-inactive-l.png":[3,39,"png","qx","qx/decoration/Modern/tabview-button-right-inactive-lr-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-right-inactive-r.png":[3,39,"png","qx","qx/decoration/Modern/tabview-button-right-inactive-lr-combined.png",-3,0],"qx/decoration/Modern/tabview/tab-button-right-inactive-t.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-right-inactive-t-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-right-inactive-tl.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-right-inactive-t-combined.png",0,-3],"qx/decoration/Modern/tabview/tab-button-right-inactive-tr.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-right-inactive-t-combined.png",0,-6],"qx/decoration/Modern/tabview/tab-button-right-inactive.png":[20,45,"png","qx"],"qx/decoration/Modern/tabview/tab-button-top-active-b.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-top-active-tb-combined.png",0,-20],"qx/decoration/Modern/tabview/tab-button-top-active-bl.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-top-active-tb-combined.png",0,-15],"qx/decoration/Modern/tabview/tab-button-top-active-br.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-top-active-tb-combined.png",0,-10],"qx/decoration/Modern/tabview/tab-button-top-active-c.png":[40,14,"png","qx"],"qx/decoration/Modern/tabview/tab-button-top-active-l.png":[5,12,"png","qx","qx/decoration/Modern/tabview-button-top-active-lr-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-top-active-r.png":[5,12,"png","qx","qx/decoration/Modern/tabview-button-top-active-lr-combined.png",-5,0],"qx/decoration/Modern/tabview/tab-button-top-active-t.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-top-active-tb-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-top-active-tl.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-top-active-tb-combined.png",0,-25],"qx/decoration/Modern/tabview/tab-button-top-active-tr.png":[5,5,"png","qx","qx/decoration/Modern/tabview-button-top-active-tb-combined.png",0,-5],"qx/decoration/Modern/tabview/tab-button-top-active.png":[48,22,"png","qx"],"qx/decoration/Modern/tabview/tab-button-top-inactive-b.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-top-inactive-b-combined.png",0,-6],"qx/decoration/Modern/tabview/tab-button-top-inactive-bl.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-top-inactive-b-combined.png",0,-3],"qx/decoration/Modern/tabview/tab-button-top-inactive-br.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-top-inactive-b-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-top-inactive-c.png":[40,15,"png","qx"],"qx/decoration/Modern/tabview/tab-button-top-inactive-l.png":[3,15,"png","qx","qx/decoration/Modern/tabview-button-top-inactive-lr-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-top-inactive-r.png":[3,15,"png","qx","qx/decoration/Modern/tabview-button-top-inactive-lr-combined.png",-3,0],"qx/decoration/Modern/tabview/tab-button-top-inactive-t.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-top-inactive-t-combined.png",0,-3],"qx/decoration/Modern/tabview/tab-button-top-inactive-tl.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-top-inactive-t-combined.png",0,0],"qx/decoration/Modern/tabview/tab-button-top-inactive-tr.png":[3,3,"png","qx","qx/decoration/Modern/tabview-button-top-inactive-t-combined.png",0,-6],"qx/decoration/Modern/tabview/tab-button-top-inactive.png":[45,21,"png","qx"],"qx/decoration/Modern/tabview/tabview-pane-b.png":[30,30,"png","qx","qx/decoration/Modern/tabview-pane-tb-combined.png",0,-60],"qx/decoration/Modern/tabview/tabview-pane-bl.png":[30,30,"png","qx","qx/decoration/Modern/tabview-pane-tb-combined.png",0,0],"qx/decoration/Modern/tabview/tabview-pane-br.png":[30,30,"png","qx","qx/decoration/Modern/tabview-pane-tb-combined.png",0,-120],"qx/decoration/Modern/tabview/tabview-pane-c.png":[40,120,"png","qx"],"qx/decoration/Modern/tabview/tabview-pane-l.png":[30,2,"png","qx","qx/decoration/Modern/tabview-pane-lr-combined.png",0,0],"qx/decoration/Modern/tabview/tabview-pane-r.png":[30,2,"png","qx","qx/decoration/Modern/tabview-pane-lr-combined.png",-30,0],"qx/decoration/Modern/tabview/tabview-pane-t.png":[30,30,"png","qx","qx/decoration/Modern/tabview-pane-tb-combined.png",0,-150],"qx/decoration/Modern/tabview/tabview-pane-tl.png":[30,30,"png","qx","qx/decoration/Modern/tabview-pane-tb-combined.png",0,-30],"qx/decoration/Modern/tabview/tabview-pane-tr.png":[30,30,"png","qx","qx/decoration/Modern/tabview-pane-tb-combined.png",0,-90],"qx/decoration/Modern/tabview/tabview-pane.png":[185,250,"png","qx"],"qx/decoration/Modern/toolbar-combined.png":[80,130,"png","qx"],"qx/decoration/Modern/toolbar/toolbar-gradient-blue.png":[40,130,"png","qx","qx/decoration/Modern/toolbar-combined.png",-40,0],"qx/decoration/Modern/toolbar/toolbar-gradient.png":[40,130,"png","qx","qx/decoration/Modern/toolbar-combined.png",0,0],"qx/decoration/Modern/toolbar/toolbar-handle-knob.gif":[1,8,"gif","qx"],"qx/decoration/Modern/toolbar/toolbar-part.gif":[7,1,"gif","qx"],"qx/decoration/Modern/tooltip-error-lr-combined.png":[12,18,"png","qx"],"qx/decoration/Modern/tooltip-error-tb-combined.png":[6,36,"png","qx"],"qx/decoration/Modern/tree-combined.png":[32,8,"png","qx"],"qx/decoration/Modern/tree/closed-selected.png":[8,8,"png","qx","qx/decoration/Modern/tree-combined.png",-24,0],"qx/decoration/Modern/tree/closed.png":[8,8,"png","qx","qx/decoration/Modern/tree-combined.png",-16,0],"qx/decoration/Modern/tree/open-selected.png":[8,8,"png","qx","qx/decoration/Modern/tree-combined.png",-8,0],"qx/decoration/Modern/tree/open.png":[8,8,"png","qx","qx/decoration/Modern/tree-combined.png",0,0],"qx/decoration/Modern/window-captionbar-buttons-combined.png":[108,9,"png","qx"],"qx/decoration/Modern/window-captionbar-lr-active-combined.png":[12,9,"png","qx"],"qx/decoration/Modern/window-captionbar-lr-inactive-combined.png":[12,9,"png","qx"],"qx/decoration/Modern/window-captionbar-tb-active-combined.png":[6,36,"png","qx"],"qx/decoration/Modern/window-captionbar-tb-inactive-combined.png":[6,36,"png","qx"],"qx/decoration/Modern/window-statusbar-lr-combined.png":[8,7,"png","qx"],"qx/decoration/Modern/window-statusbar-tb-combined.png":[4,24,"png","qx"],"qx/decoration/Modern/window/captionbar-active-b.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-active-combined.png",0,-18],"qx/decoration/Modern/window/captionbar-active-bl.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-active-combined.png",0,-24],"qx/decoration/Modern/window/captionbar-active-br.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-active-combined.png",0,-12],"qx/decoration/Modern/window/captionbar-active-c.png":[40,9,"png","qx"],"qx/decoration/Modern/window/captionbar-active-l.png":[6,9,"png","qx","qx/decoration/Modern/window-captionbar-lr-active-combined.png",-6,0],"qx/decoration/Modern/window/captionbar-active-r.png":[6,9,"png","qx","qx/decoration/Modern/window-captionbar-lr-active-combined.png",0,0],"qx/decoration/Modern/window/captionbar-active-t.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-active-combined.png",0,-6],"qx/decoration/Modern/window/captionbar-active-tl.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-active-combined.png",0,0],"qx/decoration/Modern/window/captionbar-active-tr.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-active-combined.png",0,-30],"qx/decoration/Modern/window/captionbar-active.png":[69,21,"png","qx"],"qx/decoration/Modern/window/captionbar-inactive-b.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-inactive-combined.png",0,-24],"qx/decoration/Modern/window/captionbar-inactive-bl.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-inactive-combined.png",0,-6],"qx/decoration/Modern/window/captionbar-inactive-br.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-inactive-combined.png",0,-30],"qx/decoration/Modern/window/captionbar-inactive-c.png":[40,9,"png","qx"],"qx/decoration/Modern/window/captionbar-inactive-l.png":[6,9,"png","qx","qx/decoration/Modern/window-captionbar-lr-inactive-combined.png",0,0],"qx/decoration/Modern/window/captionbar-inactive-r.png":[6,9,"png","qx","qx/decoration/Modern/window-captionbar-lr-inactive-combined.png",-6,0],"qx/decoration/Modern/window/captionbar-inactive-t.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-inactive-combined.png",0,0],"qx/decoration/Modern/window/captionbar-inactive-tl.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-inactive-combined.png",0,-12],"qx/decoration/Modern/window/captionbar-inactive-tr.png":[6,6,"png","qx","qx/decoration/Modern/window-captionbar-tb-inactive-combined.png",0,-18],"qx/decoration/Modern/window/captionbar-inactive.png":[69,21,"png","qx"],"qx/decoration/Modern/window/close-active-hovered.png":[9,9,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-27,0],"qx/decoration/Modern/window/close-active.png":[9,9,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-9,0],"qx/decoration/Modern/window/close-inactive.png":[9,9,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-90,0],"qx/decoration/Modern/window/maximize-active-hovered.png":[9,9,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-18,0],"qx/decoration/Modern/window/maximize-active.png":[9,9,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-81,0],"qx/decoration/Modern/window/maximize-inactive.png":[9,9,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-54,0],"qx/decoration/Modern/window/minimize-active-hovered.png":[9,9,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-63,0],"qx/decoration/Modern/window/minimize-active.png":[9,9,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-72,0],"qx/decoration/Modern/window/minimize-inactive.png":[9,9,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-36,0],"qx/decoration/Modern/window/restore-active-hovered.png":[9,8,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",0,0],"qx/decoration/Modern/window/restore-active.png":[9,8,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-99,0],"qx/decoration/Modern/window/restore-inactive.png":[9,8,"png","qx","qx/decoration/Modern/window-captionbar-buttons-combined.png",-45,0],"qx/decoration/Modern/window/statusbar-b.png":[4,4,"png","qx","qx/decoration/Modern/window-statusbar-tb-combined.png",0,-16],"qx/decoration/Modern/window/statusbar-bl.png":[4,4,"png","qx","qx/decoration/Modern/window-statusbar-tb-combined.png",0,-20],"qx/decoration/Modern/window/statusbar-br.png":[4,4,"png","qx","qx/decoration/Modern/window-statusbar-tb-combined.png",0,-4],"qx/decoration/Modern/window/statusbar-c.png":[40,7,"png","qx"],"qx/decoration/Modern/window/statusbar-l.png":[4,7,"png","qx","qx/decoration/Modern/window-statusbar-lr-combined.png",-4,0],"qx/decoration/Modern/window/statusbar-r.png":[4,7,"png","qx","qx/decoration/Modern/window-statusbar-lr-combined.png",0,0],"qx/decoration/Modern/window/statusbar-t.png":[4,4,"png","qx","qx/decoration/Modern/window-statusbar-tb-combined.png",0,0],"qx/decoration/Modern/window/statusbar-tl.png":[4,4,"png","qx","qx/decoration/Modern/window-statusbar-tb-combined.png",0,-8],"qx/decoration/Modern/window/statusbar-tr.png":[4,4,"png","qx","qx/decoration/Modern/window-statusbar-tb-combined.png",0,-12],"qx/decoration/Modern/window/statusbar.png":[369,15,"png","qx"],"qx/icon/Tango/16/actions/dialog-cancel.png":[16,16,"png","qx"],"qx/icon/Tango/16/actions/dialog-ok.png":[16,16,"png","qx"],"qx/icon/Tango/16/actions/view-refresh.png":[16,16,"png","qx"],"qx/icon/Tango/16/actions/window-close.png":[16,16,"png","qx"],"qx/icon/Tango/16/apps/office-calendar.png":[16,16,"png","qx"],"qx/icon/Tango/16/apps/utilities-color-chooser.png":[16,16,"png","qx"],"qx/icon/Tango/16/mimetypes/office-document.png":[16,16,"png","qx"],"qx/icon/Tango/16/places/folder-open.png":[16,16,"png","qx"],"qx/icon/Tango/16/places/folder.png":[16,16,"png","qx"],"qx/icon/Tango/22/mimetypes/office-document.png":[22,22,"png","qx"],"qx/icon/Tango/22/places/folder-open.png":[22,22,"png","qx"],"qx/icon/Tango/22/places/folder.png":[22,22,"png","qx"],"qx/icon/Tango/32/mimetypes/office-document.png":[32,32,"png","qx"],"qx/icon/Tango/32/places/folder-open.png":[32,32,"png","qx"],"qx/icon/Tango/32/places/folder.png":[32,32,"png","qx"],"qx/static/blank.gif":[1,1,"gif","qx"]},"translations":{"C":{},"en":{},"fr":{"%1 of %2 rows":"ligne %1 de %2","%1 rows":"%1 lignes","one of one row":"ligne une de une","one row":"une ligne"}}};
(function(){var m="toString",k=".",j="default",h="Object",g='"',f="Array",e="()",d="String",c="Function",b=".prototype",L="function",K="Boolean",J="Error",I="constructor",H="warn",G="hasOwnProperty",F="string",E="toLocaleString",D="RegExp",C='\", "',t="info",u="BROKEN_IE",r="isPrototypeOf",s="Date",p="",q="qx.Bootstrap",n="]",o="Class",v="error",w="[Class ",y="valueOf",x="Number",A="count",z="debug",B="ES5";
if(!window.qx){window.qx={};
}qx.Bootstrap={genericToString:function(){return w+this.classname+n;
},createNamespace:function(name,M){var O=name.split(k);
var parent=window;
var N=O[0];

for(var i=0,P=O.length-1;i<P;i++,N=O[i]){if(!parent[N]){parent=parent[N]={};
}else{parent=parent[N];
}}parent[N]=M;
return N;
},setDisplayName:function(Q,R,name){Q.displayName=R+k+name+e;
},setDisplayNames:function(S,T){for(var name in S){var U=S[name];

if(U instanceof Function){U.displayName=T+k+name+e;
}}},define:function(name,V){if(!V){var V={statics:{}};
}var bb;
var Y=null;
qx.Bootstrap.setDisplayNames(V.statics,name);

if(V.members||V.extend){qx.Bootstrap.setDisplayNames(V.members,name+b);
bb=V.construct||new Function;

if(V.extend){this.extendClass(bb,bb,V.extend,name,ba);
}var W=V.statics||{};
for(var i=0,bc=qx.Bootstrap.getKeys(W),l=bc.length;i<l;i++){var bd=bc[i];
bb[bd]=W[bd];
}Y=bb.prototype;
var X=V.members||{};
for(var i=0,bc=qx.Bootstrap.getKeys(X),l=bc.length;i<l;i++){var bd=bc[i];
Y[bd]=X[bd];
}}else{bb=V.statics||{};
}var ba=this.createNamespace(name,bb);
bb.name=bb.classname=name;
bb.basename=ba;
bb.$$type=o;
if(!bb.hasOwnProperty(m)){bb.toString=this.genericToString;
}if(V.defer){V.defer(bb,Y);
}qx.Bootstrap.$$registry[name]=V.statics;
return bb;
}};
qx.Bootstrap.define(q,{statics:{LOADSTART:qx.$$start||new Date(),createNamespace:qx.Bootstrap.createNamespace,define:qx.Bootstrap.define,setDisplayName:qx.Bootstrap.setDisplayName,setDisplayNames:qx.Bootstrap.setDisplayNames,genericToString:qx.Bootstrap.genericToString,extendClass:function(be,bf,bg,name,bh){var bk=bg.prototype;
var bj=new Function;
bj.prototype=bk;
var bi=new bj;
be.prototype=bi;
bi.name=bi.classname=name;
bi.basename=bh;
bf.base=be.superclass=bg;
bf.self=be.constructor=bi.constructor=be;
},getByName:function(name){return qx.Bootstrap.$$registry[name];
},$$registry:{},objectGetLength:({"count":function(bl){return bl.__count__;
},"default":function(bm){var length=0;

for(var bn in bm){length++;
}return length;
}})[(({}).__count__==0)?A:j],objectMergeWith:function(bo,bp,bq){if(bq===undefined){bq=true;
}
for(var br in bp){if(bq||bo[br]===undefined){bo[br]=bp[br];
}}return bo;
},__a:[r,G,E,m,y,I],getKeys:({"ES5":Object.keys,"BROKEN_IE":function(bs){var bt=[];
var bv=Object.prototype.hasOwnProperty;

for(var bw in bs){if(bv.call(bs,bw)){bt.push(bw);
}}var bu=qx.Bootstrap.__a;

for(var i=0,a=bu,l=a.length;i<l;i++){if(bv.call(bs,a[i])){bt.push(a[i]);
}}return bt;
},"default":function(bx){var by=[];
var bz=Object.prototype.hasOwnProperty;

for(var bA in bx){if(bz.call(bx,bA)){by.push(bA);
}}return by;
}})[typeof (Object.keys)==
L?B:
(function(){for(var bB in {toString:1}){return bB;
}})()!==m?u:j],getKeysAsString:function(bC){var bD=qx.Bootstrap.getKeys(bC);

if(bD.length==0){return p;
}return g+bD.join(C)+g;
},__b:{"[object String]":d,"[object Array]":f,"[object Object]":h,"[object RegExp]":D,"[object Number]":x,"[object Boolean]":K,"[object Date]":s,"[object Function]":c,"[object Error]":J},bind:function(bE,self,bF){var bG=Array.prototype.slice.call(arguments,2,arguments.length);
return function(){var bH=Array.prototype.slice.call(arguments,0,arguments.length);
return bE.apply(self,bG.concat(bH));
};
},firstUp:function(bI){return bI.charAt(0).toUpperCase()+bI.substr(1);
},firstLow:function(bJ){return bJ.charAt(0).toLowerCase()+bJ.substr(1);
},getClass:function(bK){var bL=Object.prototype.toString.call(bK);
return (qx.Bootstrap.__b[bL]||bL.slice(8,-1));
},isString:function(bM){return (bM!==null&&(typeof bM===F||qx.Bootstrap.getClass(bM)==d||bM instanceof String||(!!bM&&!!bM.$$isString)));
},isArray:function(bN){return (bN!==null&&(bN instanceof Array||(bN&&qx.data&&qx.data.IListData&&qx.Bootstrap.hasInterface(bN.constructor,qx.data.IListData))||qx.Bootstrap.getClass(bN)==f||(!!bN&&!!bN.$$isArray)));
},isObject:function(bO){return (bO!==undefined&&bO!==null&&qx.Bootstrap.getClass(bO)==h);
},isFunction:function(bP){return qx.Bootstrap.getClass(bP)==c;
},classIsDefined:function(name){return qx.Bootstrap.getByName(name)!==undefined;
},getPropertyDefinition:function(bQ,name){while(bQ){if(bQ.$$properties&&bQ.$$properties[name]){return bQ.$$properties[name];
}bQ=bQ.superclass;
}return null;
},hasProperty:function(bR,name){return !!qx.Bootstrap.getPropertyDefinition(bR,name);
},getEventType:function(bS,name){var bS=bS.constructor;

while(bS.superclass){if(bS.$$events&&bS.$$events[name]!==undefined){return bS.$$events[name];
}bS=bS.superclass;
}return null;
},supportsEvent:function(bT,name){return !!qx.Bootstrap.getEventType(bT,name);
},getByInterface:function(bU,bV){var bW,i,l;

while(bU){if(bU.$$implements){bW=bU.$$flatImplements;

for(i=0,l=bW.length;i<l;i++){if(bW[i]===bV){return bU;
}}}bU=bU.superclass;
}return null;
},hasInterface:function(bX,bY){return !!qx.Bootstrap.getByInterface(bX,bY);
},getMixins:function(ca){var cb=[];

while(ca){if(ca.$$includes){cb.push.apply(cb,ca.$$flatIncludes);
}ca=ca.superclass;
}return cb;
},$$logs:[],debug:function(cc,cd){qx.Bootstrap.$$logs.push([z,arguments]);
},info:function(ce,cf){qx.Bootstrap.$$logs.push([t,arguments]);
},warn:function(cg,ch){qx.Bootstrap.$$logs.push([H,arguments]);
},error:function(ci,cj){qx.Bootstrap.$$logs.push([v,arguments]);
},trace:function(ck){}}});
})();
(function(){var g="qx.Mixin",f=".prototype",e="constructor",d="[Mixin ",c="]",b="destruct",a="Mixin";
qx.Bootstrap.define(g,{statics:{define:function(name,h){if(h){if(h.include&&!(h.include instanceof Array)){h.include=[h.include];
}{};
var k=h.statics?h.statics:{};
qx.Bootstrap.setDisplayNames(k,name);

for(var j in k){if(k[j] instanceof Function){k[j].$$mixin=k;
}}if(h.construct){k.$$constructor=h.construct;
qx.Bootstrap.setDisplayName(h.construct,name,e);
}
if(h.include){k.$$includes=h.include;
}
if(h.properties){k.$$properties=h.properties;
}
if(h.members){k.$$members=h.members;
qx.Bootstrap.setDisplayNames(h.members,name+f);
}
for(var j in k.$$members){if(k.$$members[j] instanceof Function){k.$$members[j].$$mixin=k;
}}
if(h.events){k.$$events=h.events;
}
if(h.destruct){k.$$destructor=h.destruct;
qx.Bootstrap.setDisplayName(h.destruct,name,b);
}}else{var k={};
}k.$$type=a;
k.name=name;
k.toString=this.genericToString;
k.basename=qx.Bootstrap.createNamespace(name,k);
this.$$registry[name]=k;
return k;
},checkCompatibility:function(m){var p=this.flatten(m);
var q=p.length;

if(q<2){return true;
}var t={};
var s={};
var r={};
var o;

for(var i=0;i<q;i++){o=p[i];

for(var n in o.events){if(r[n]){throw new Error('Conflict between mixin "'+o.name+'" and "'+r[n]+'" in member "'+n+'"!');
}r[n]=o.name;
}
for(var n in o.properties){if(t[n]){throw new Error('Conflict between mixin "'+o.name+'" and "'+t[n]+'" in property "'+n+'"!');
}t[n]=o.name;
}
for(var n in o.members){if(s[n]){throw new Error('Conflict between mixin "'+o.name+'" and "'+s[n]+'" in member "'+n+'"!');
}s[n]=o.name;
}}return true;
},isCompatible:function(u,v){var w=qx.Bootstrap.getMixins(v);
w.push(u);
return qx.Mixin.checkCompatibility(w);
},getByName:function(name){return this.$$registry[name];
},isDefined:function(name){return this.getByName(name)!==undefined;
},getTotalNumber:function(){return qx.Bootstrap.objectGetLength(this.$$registry);
},flatten:function(x){if(!x){return [];
}var y=x.concat();

for(var i=0,l=x.length;i<l;i++){if(x[i].$$includes){y.push.apply(y,this.flatten(x[i].$$includes));
}}return y;
},genericToString:function(){return d+this.name+c;
},$$registry:{},__c:null,__d:function(){}}});
})();
(function(){var h="qx.allowUrlSettings",g="&",f="qx.core.Setting",e="qx.allowUrlVariants",d="qx.propertyDebugLevel",c="qxsetting",b=":",a=".";
qx.Bootstrap.define(f,{statics:{__e:{},define:function(j,k){if(k===undefined){throw new Error('Default value of setting "'+j+'" must be defined!');
}
if(!this.__e[j]){this.__e[j]={};
}else if(this.__e[j].defaultValue!==undefined){throw new Error('Setting "'+j+'" is already defined!');
}this.__e[j].defaultValue=k;
},get:function(l){var m=this.__e[l];

if(m===undefined){throw new Error('Setting "'+l+'" is not defined.');
}
if(m.value!==undefined){return m.value;
}return m.defaultValue;
},set:function(n,o){if((n.split(a)).length<2){throw new Error('Malformed settings key "'+n+'". Must be following the schema "namespace.key".');
}
if(!this.__e[n]){this.__e[n]={};
}this.__e[n].value=o;
},__f:function(){if(window.qxsettings){for(var p in window.qxsettings){this.set(p,window.qxsettings[p]);
}window.qxsettings=undefined;

try{delete window.qxsettings;
}catch(q){}this.__g();
}},__g:function(){if(this.get(h)!=true){return;
}var s=document.location.search.slice(1).split(g);

for(var i=0;i<s.length;i++){var r=s[i].split(b);

if(r.length!=3||r[0]!=c){continue;
}this.set(r[1],decodeURIComponent(r[2]));
}}},defer:function(t){t.define(h,false);
t.define(e,false);
t.define(d,0);
t.__f();
}});
})();
(function(){var h="function",g="Boolean",f="qx.Interface",e="]",d="toggle",c="Interface",b="is",a="[Interface ";
qx.Bootstrap.define(f,{statics:{define:function(name,j){if(j){if(j.extend&&!(j.extend instanceof Array)){j.extend=[j.extend];
}{};
var k=j.statics?j.statics:{};
if(j.extend){k.$$extends=j.extend;
}
if(j.properties){k.$$properties=j.properties;
}
if(j.members){k.$$members=j.members;
}
if(j.events){k.$$events=j.events;
}}else{var k={};
}k.$$type=c;
k.name=name;
k.toString=this.genericToString;
k.basename=qx.Bootstrap.createNamespace(name,k);
qx.Interface.$$registry[name]=k;
return k;
},getByName:function(name){return this.$$registry[name];
},isDefined:function(name){return this.getByName(name)!==undefined;
},getTotalNumber:function(){return qx.Bootstrap.objectGetLength(this.$$registry);
},flatten:function(m){if(!m){return [];
}var n=m.concat();

for(var i=0,l=m.length;i<l;i++){if(m[i].$$extends){n.push.apply(n,this.flatten(m[i].$$extends));
}}return n;
},__h:function(o,p,q,r){var v=q.$$members;

if(v){for(var u in v){if(qx.Bootstrap.isFunction(v[u])){var t=this.__i(p,u);
var s=t||qx.Bootstrap.isFunction(o[u]);

if(!s){throw new Error('Implementation of method "'+u+'" is missing in class "'+p.classname+'" required by interface "'+q.name+'"');
}var w=r===true&&!t&&!qx.Bootstrap.hasInterface(p,q);

if(w){o[u]=this.__l(q,o[u],u,v[u]);
}}else{if(typeof o[u]===undefined){if(typeof o[u]!==h){throw new Error('Implementation of member "'+u+'" is missing in class "'+p.classname+'" required by interface "'+q.name+'"');
}}}}}},__i:function(x,y){var C=y.match(/^(is|toggle|get|set|reset)(.*)$/);

if(!C){return false;
}var z=qx.Bootstrap.firstLow(C[2]);
var A=qx.Bootstrap.getPropertyDefinition(x,z);

if(!A){return false;
}var B=C[0]==b||C[0]==d;

if(B){return qx.Bootstrap.getPropertyDefinition(x,z).check==g;
}return true;
},__j:function(D,E){if(E.$$properties){for(var F in E.$$properties){if(!qx.Bootstrap.getPropertyDefinition(D,F)){throw new Error('The property "'+F+'" is not supported by Class "'+D.classname+'"!');
}}}},__k:function(G,H){if(H.$$events){for(var I in H.$$events){if(!qx.Bootstrap.supportsEvent(G,I)){throw new Error('The event "'+I+'" is not supported by Class "'+G.classname+'"!');
}}}},assertObject:function(J,K){var M=J.constructor;
this.__h(J,M,K,false);
this.__j(M,K);
this.__k(M,K);
var L=K.$$extends;

if(L){for(var i=0,l=L.length;i<l;i++){this.assertObject(J,L[i]);
}}},assert:function(N,O,P){this.__h(N.prototype,N,O,P);
this.__j(N,O);
this.__k(N,O);
var Q=O.$$extends;

if(Q){for(var i=0,l=Q.length;i<l;i++){this.assert(N,Q[i],P);
}}},genericToString:function(){return a+this.name+e;
},$$registry:{},__l:function(){},__m:null,__n:function(){}}});
})();
(function(){var d="qx.core.Aspect",c="before",b="*",a="static";
qx.Bootstrap.define(d,{statics:{__o:[],wrap:function(e,f,g){var m=[];
var h=[];
var l=this.__o;
var k;

for(var i=0;i<l.length;i++){k=l[i];

if((k.type==null||g==k.type||k.type==b)&&(k.name==null||e.match(k.name))){k.pos==-1?m.push(k.fcn):h.push(k.fcn);
}}
if(m.length===0&&h.length===0){return f;
}var j=function(){for(var i=0;i<m.length;i++){m[i].call(this,e,f,g,arguments);
}var n=f.apply(this,arguments);

for(var i=0;i<h.length;i++){h[i].call(this,e,f,g,arguments,n);
}return n;
};

if(g!==a){j.self=f.self;
j.base=f.base;
}f.wrapper=j;
j.original=f;
return j;
},addAdvice:function(o,p,q,name){this.__o.push({fcn:o,pos:p===c?-1:1,type:q,name:name});
}}});
})();
(function(){var g="emulated",f="native",e='"',d="qx.lang.Core",c="\\\\",b="\\\"",a="[object Error]";
qx.Bootstrap.define(d,{statics:{errorToString:{"native":Error.prototype.toString,"emulated":function(){return this.message;
}}[(!Error.prototype.toString||Error.prototype.toString()==a)?g:f],arrayIndexOf:{"native":Array.prototype.indexOf,"emulated":function(h,j){if(j==null){j=0;
}else if(j<0){j=Math.max(0,this.length+j);
}
for(var i=j;i<this.length;i++){if(this[i]===h){return i;
}}return -1;
}}[Array.prototype.indexOf?f:g],arrayLastIndexOf:{"native":Array.prototype.lastIndexOf,"emulated":function(k,m){if(m==null){m=this.length-1;
}else if(m<0){m=Math.max(0,this.length+m);
}
for(var i=m;i>=0;i--){if(this[i]===k){return i;
}}return -1;
}}[Array.prototype.lastIndexOf?f:g],arrayForEach:{"native":Array.prototype.forEach,"emulated":function(n,o){var l=this.length;

for(var i=0;i<l;i++){var p=this[i];

if(p!==undefined){n.call(o||window,p,i,this);
}}}}[Array.prototype.forEach?f:g],arrayFilter:{"native":Array.prototype.filter,"emulated":function(q,r){var s=[];
var l=this.length;

for(var i=0;i<l;i++){var t=this[i];

if(t!==undefined){if(q.call(r||window,t,i,this)){s.push(this[i]);
}}}return s;
}}[Array.prototype.filter?f:g],arrayMap:{"native":Array.prototype.map,"emulated":function(u,v){var w=[];
var l=this.length;

for(var i=0;i<l;i++){var x=this[i];

if(x!==undefined){w[i]=u.call(v||window,x,i,this);
}}return w;
}}[Array.prototype.map?f:g],arraySome:{"native":Array.prototype.some,"emulated":function(y,z){var l=this.length;

for(var i=0;i<l;i++){var A=this[i];

if(A!==undefined){if(y.call(z||window,A,i,this)){return true;
}}}return false;
}}[Array.prototype.some?f:g],arrayEvery:{"native":Array.prototype.every,"emulated":function(B,C){var l=this.length;

for(var i=0;i<l;i++){var D=this[i];

if(D!==undefined){if(!B.call(C||window,D,i,this)){return false;
}}}return true;
}}[Array.prototype.every?f:g],stringQuote:{"native":String.prototype.quote,"emulated":function(){return e+this.replace(/\\/g,c).replace(/\"/g,b)+e;
}}[String.prototype.quote?f:g]}});
Error.prototype.toString=qx.lang.Core.errorToString;
Array.prototype.indexOf=qx.lang.Core.arrayIndexOf;
Array.prototype.lastIndexOf=qx.lang.Core.arrayLastIndexOf;
Array.prototype.forEach=qx.lang.Core.arrayForEach;
Array.prototype.filter=qx.lang.Core.arrayFilter;
Array.prototype.map=qx.lang.Core.arrayMap;
Array.prototype.some=qx.lang.Core.arraySome;
Array.prototype.every=qx.lang.Core.arrayEvery;
String.prototype.quote=qx.lang.Core.stringQuote;
})();
(function(){var s="gecko",r="1.9.0.0",q=".",p="[object Opera]",o="function",n="[^\\.0-9]",m="525.26",l="",k="mshtml",j="AppleWebKit/",d="unknown",i="9.6.0",g="4.0",c="Gecko",b="opera",f="webkit",e="0.0.0",h="8.0",a="qx.bom.client.Engine";
qx.Bootstrap.define(a,{statics:{NAME:"",FULLVERSION:"0.0.0",VERSION:0.0,OPERA:false,WEBKIT:false,GECKO:false,MSHTML:false,UNKNOWN_ENGINE:false,UNKNOWN_VERSION:false,DOCUMENT_MODE:null,__p:function(){var t=d;
var x=e;
var w=window.navigator.userAgent;
var z=false;
var v=false;

if(window.opera&&Object.prototype.toString.call(window.opera)==p){t=b;
this.OPERA=true;
if(/Opera[\s\/]([0-9]+)\.([0-9])([0-9]*)/.test(w)){x=RegExp.$1+q+RegExp.$2;

if(RegExp.$3!=l){x+=q+RegExp.$3;
}}else{v=true;
x=i;
}}else if(window.navigator.userAgent.indexOf(j)!=-1){t=f;
this.WEBKIT=true;

if(/AppleWebKit\/([^ ]+)/.test(w)){x=RegExp.$1;
var y=RegExp(n).exec(x);

if(y){x=x.slice(0,y.index);
}}else{v=true;
x=m;
}}else if(window.controllers&&window.navigator.product===c){t=s;
this.GECKO=true;
if(/rv\:([^\);]+)(\)|;)/.test(w)){x=RegExp.$1;
}else{v=true;
x=r;
}}else if(window.navigator.cpuClass&&/MSIE\s+([^\);]+)(\)|;)/.test(w)){t=k;
x=RegExp.$1;

if(document.documentMode){this.DOCUMENT_MODE=document.documentMode;
}if(x<8&&/Trident\/([^\);]+)(\)|;)/.test(w)){if(RegExp.$1===g){x=h;
}}this.MSHTML=true;
}else{var u=window.qxFail;

if(u&&typeof u===o){var t=u();

if(t.NAME&&t.FULLVERSION){t=t.NAME;
this[t.toUpperCase()]=true;
x=t.FULLVERSION;
}}else{z=true;
v=true;
x=r;
t=s;
this.GECKO=true;
qx.Bootstrap.warn("Unsupported client: "+w+"! Assumed gecko version 1.9.0.0 (Firefox 3.0).");
}}this.UNKNOWN_ENGINE=z;
this.UNKNOWN_VERSION=v;
this.NAME=t;
this.FULLVERSION=x;
this.VERSION=parseFloat(x);
}},defer:function(A){A.__p();
}});
})();
(function(){var x="off",w="on",u="|",t="default",s="object",r="&",q="qx.aspects",p="qx.mobile.nativescroll",o="qx.mobile.emulatetouch",n="$",e="qx.allowUrlVariants",m="qx.debug",h="qx.client",c="qx.dynlocale",b="webkit",g="qxvariant",f="opera",j=":",a="qx.core.Variant",k="mshtml",d="gecko";
qx.Bootstrap.define(a,{statics:{__q:{},__r:{},compilerIsSet:function(){return true;
},define:function(y,z,A){{};

if(!this.__q[y]){this.__q[y]={};
}else{}this.__q[y].allowedValues=z;
this.__q[y].defaultValue=A;
},get:function(B){var C=this.__q[B];
{};

if(C.value!==undefined){return C.value;
}return C.defaultValue;
},__s:function(){if(window.qxvariants){for(var D in qxvariants){{};

if(!this.__q[D]){this.__q[D]={};
}this.__q[D].value=qxvariants[D];
}window.qxvariants=undefined;

try{delete window.qxvariants;
}catch(E){}this.__t(this.__q);
}},__t:function(){if(qx.core.Setting.get(e)!=true){return;
}var F=document.location.search.slice(1).split(r);

for(var i=0;i<F.length;i++){var G=F[i].split(j);

if(G.length!=3||G[0]!=g){continue;
}var H=G[1];

if(!this.__q[H]){this.__q[H]={};
}this.__q[H].value=decodeURIComponent(G[2]);
}},select:function(I,J){{};

for(var K in J){if(this.isSet(I,K)){return J[K];
}}
if(J[t]!==undefined){return J[t];
}{};
},isSet:function(L,M){var N=L+n+M;

if(this.__r[N]!==undefined){return this.__r[N];
}var P=false;
if(M.indexOf(u)<0){P=this.get(L)===M;
}else{var O=M.split(u);

for(var i=0,l=O.length;i<l;i++){if(this.get(L)===O[i]){P=true;
break;
}}}this.__r[N]=P;
return P;
},__u:function(v){return typeof v===s&&v!==null&&v instanceof Array;
},__v:function(v){return typeof v===s&&v!==null&&!(v instanceof Array);
},__w:function(Q,R){for(var i=0,l=Q.length;i<l;i++){if(Q[i]==R){return true;
}}return false;
}},defer:function(S){S.define(h,[d,k,f,b],qx.bom.client.Engine.NAME);
S.define(m,[w,x],w);
S.define(q,[w,x],x);
S.define(c,[w,x],w);
S.define(o,[w,x],x);
S.define(p,[w,x],x);
S.__s();
}});
})();
(function(){var m=';',k='return this.',j="boolean",h="string",g='!==undefined)',f='else if(this.',e='if(this.',d='else ',c=' of an instance of ',b=' is not (yet) ready!");',bi="init",bh='qx.lang.Type.isString(value) && qx.util.ColorUtil.isValidPropertyValue(value)',bg='value !== null && qx.theme.manager.Font.getInstance().isDynamic(value)',bf=" of class ",be='qx.core.Assert.assertInstance(value, Date, msg) || true',bd='value !== null && value.nodeType !== undefined',bc='var inherit=prop.$$inherit;',bb='value !== null && value.nodeType === 9 && value.documentElement',ba='return init;',Y='value !== null && value.$$type === "Mixin"',t='qx.core.Assert.assertMap(value, msg) || true',u='var init=this.',r='return value;',s='qx.core.Assert.assertNumber(value, msg) || true',p='qx.core.Assert.assertPositiveInteger(value, msg) || true',q="': ",n="Error in property ",o='if(init==qx.core.Property.$$inherit)init=null;',x='qx.core.Assert.assertInteger(value, msg) || true',y="rv:1.8.1",G='value !== null && value.$$type === "Interface"',E="set",O='value !== null && value.$$type === "Theme"',J='qx.core.Assert.assertInstance(value, RegExp, msg) || true',U='value !== null && value.type !== undefined',S='value !== null && value.document',A=" in method ",X='qx.core.Assert.assertInstance(value, Error, msg) || true',W='throw new Error("Property ',V='qx.core.Assert.assertBoolean(value, msg) || true',z='return null;',C='qx.core.Assert.assertObject(value, msg) || true',D="setRuntime",F='value !== null && value.nodeType === 1 && value.attributes',H=" with incoming value '",K="setThemed",P='qx.core.Assert.assertString(value, msg) || true',T="inherit",v='value !== null && value.$$type === "Class"',w='qx.core.Assert.assertFunction(value, msg) || true',B='value !== null && qx.theme.manager.Decoration.getInstance().isValidPropertyValue(value)',N='qx.core.Assert.assertArray(value, msg) || true',M='qx.core.Assert.assertPositiveNumber(value, msg) || true',L="object",R="MSIE 6.0",Q='if(init==qx.core.Property.$$inherit)throw new Error("Inheritable property ',I="qx.core.Property";
qx.Bootstrap.define(I,{statics:{__x:{"Boolean":V,"String":P,"Number":s,"Integer":x,"PositiveNumber":M,"PositiveInteger":p,"Error":X,"RegExp":J,"Object":C,"Array":N,"Map":t,"Function":w,"Date":be,"Node":bd,"Element":F,"Document":bb,"Window":S,"Event":U,"Class":v,"Mixin":Y,"Interface":G,"Theme":O,"Color":bh,"Decorator":B,"Font":bg},__y:{"Node":true,"Element":true,"Document":true,"Window":true,"Event":true},$$inherit:T,$$store:{runtime:{},user:{},theme:{},inherit:{},init:{},useinit:{}},$$method:{get:{},set:{},reset:{},init:{},refresh:{},setRuntime:{},resetRuntime:{},setThemed:{},resetThemed:{}},$$allowedKeys:{name:h,dereference:j,inheritable:j,nullable:j,themeable:j,refine:j,init:null,apply:h,event:h,check:null,transform:h,deferredInit:j,validate:null},$$allowedGroupKeys:{name:h,group:L,mode:h,themeable:j},$$inheritable:{},__z:function(bj){var bk=this.__A(bj);

if(!bk.length){var bl=qx.lang.Function.empty;
}else{bl=this.__B(bk);
}bj.prototype.$$refreshInheritables=bl;
},__A:function(bm){var bo=[];

while(bm){var bn=bm.$$properties;

if(bn){for(var name in this.$$inheritable){if(bn[name]&&bn[name].inheritable){bo.push(name);
}}}bm=bm.superclass;
}return bo;
},__B:function(bp){var bt=this.$$store.inherit;
var bs=this.$$store.init;
var br=this.$$method.refresh;
var bq=["var parent = this.getLayoutParent();","if (!parent) return;"];

for(var i=0,l=bp.length;i<l;i++){var name=bp[i];
bq.push("var value = parent.",bt[name],";","if (value===undefined) value = parent.",bs[name],";","this.",br[name],"(value);");
}return new Function(bq.join(""));
},attachRefreshInheritables:function(bu){bu.prototype.$$refreshInheritables=function(){qx.core.Property.__z(bu);
return this.$$refreshInheritables();
};
},attachMethods:function(bv,name,bw){bw.group?this.__C(bv,bw,name):this.__D(bv,bw,name);
},__C:function(bx,by,name){var bF=qx.Bootstrap.firstUp(name);
var bE=bx.prototype;
var bG=by.themeable===true;
{};
var bH=[];
var bB=[];

if(bG){var bz=[];
var bD=[];
}var bC="var a=arguments[0] instanceof Array?arguments[0]:arguments;";
bH.push(bC);

if(bG){bz.push(bC);
}
if(by.mode=="shorthand"){var bA="a=qx.lang.Array.fromShortHand(qx.lang.Array.fromArguments(a));";
bH.push(bA);

if(bG){bz.push(bA);
}}
for(var i=0,a=by.group,l=a.length;i<l;i++){{};
bH.push("this.",this.$$method.set[a[i]],"(a[",i,"]);");
bB.push("this.",this.$$method.reset[a[i]],"();");

if(bG){{};
bz.push("this.",this.$$method.setThemed[a[i]],"(a[",i,"]);");
bD.push("this.",this.$$method.resetThemed[a[i]],"();");
}}this.$$method.set[name]="set"+bF;
bE[this.$$method.set[name]]=new Function(bH.join(""));
this.$$method.reset[name]="reset"+bF;
bE[this.$$method.reset[name]]=new Function(bB.join(""));

if(bG){this.$$method.setThemed[name]="setThemed"+bF;
bE[this.$$method.setThemed[name]]=new Function(bz.join(""));
this.$$method.resetThemed[name]="resetThemed"+bF;
bE[this.$$method.resetThemed[name]]=new Function(bD.join(""));
}},__D:function(bI,bJ,name){var bL=qx.Bootstrap.firstUp(name);
var bN=bI.prototype;
{};
if(bJ.dereference===undefined&&typeof bJ.check==="string"){bJ.dereference=this.__E(bJ.check);
}var bM=this.$$method;
var bK=this.$$store;
bK.runtime[name]="$$runtime_"+name;
bK.user[name]="$$user_"+name;
bK.theme[name]="$$theme_"+name;
bK.init[name]="$$init_"+name;
bK.inherit[name]="$$inherit_"+name;
bK.useinit[name]="$$useinit_"+name;
bM.get[name]="get"+bL;
bN[bM.get[name]]=function(){return qx.core.Property.executeOptimizedGetter(this,bI,name,"get");
};
bM.set[name]="set"+bL;
bN[bM.set[name]]=function(bO){return qx.core.Property.executeOptimizedSetter(this,bI,name,"set",arguments);
};
bM.reset[name]="reset"+bL;
bN[bM.reset[name]]=function(){return qx.core.Property.executeOptimizedSetter(this,bI,name,"reset");
};

if(bJ.inheritable||bJ.apply||bJ.event||bJ.deferredInit){bM.init[name]="init"+bL;
bN[bM.init[name]]=function(bP){return qx.core.Property.executeOptimizedSetter(this,bI,name,"init",arguments);
};
}
if(bJ.inheritable){bM.refresh[name]="refresh"+bL;
bN[bM.refresh[name]]=function(bQ){return qx.core.Property.executeOptimizedSetter(this,bI,name,"refresh",arguments);
};
}bM.setRuntime[name]="setRuntime"+bL;
bN[bM.setRuntime[name]]=function(bR){return qx.core.Property.executeOptimizedSetter(this,bI,name,"setRuntime",arguments);
};
bM.resetRuntime[name]="resetRuntime"+bL;
bN[bM.resetRuntime[name]]=function(){return qx.core.Property.executeOptimizedSetter(this,bI,name,"resetRuntime");
};

if(bJ.themeable){bM.setThemed[name]="setThemed"+bL;
bN[bM.setThemed[name]]=function(bS){return qx.core.Property.executeOptimizedSetter(this,bI,name,"setThemed",arguments);
};
bM.resetThemed[name]="resetThemed"+bL;
bN[bM.resetThemed[name]]=function(){return qx.core.Property.executeOptimizedSetter(this,bI,name,"resetThemed");
};
}
if(bJ.check==="Boolean"){bN["toggle"+bL]=new Function("return this."+bM.set[name]+"(!this."+bM.get[name]+"())");
bN["is"+bL]=new Function("return this."+bM.get[name]+"()");
}},__E:function(bT){return !!this.__y[bT];
},__F:function(bU){return this.__y[bU]||qx.Bootstrap.classIsDefined(bU)||(qx.Interface&&qx.Interface.isDefined(bU));
},__G:{0:'Could not change or apply init value after constructing phase!',1:'Requires exactly one argument!',2:'Undefined value is not allowed!',3:'Does not allow any arguments!',4:'Null value is not allowed!',5:'Is invalid!'},error:function(bV,bW,bX,bY,ca){var cb=bV.constructor.classname;
var cc=n+bX+bf+cb+A+this.$$method[bY][bX]+H+ca+q;
throw new Error(cc+(this.__G[bW]||"Unknown reason: "+bW));
},__H:function(cd,ce,name,cf,cg,ch){var ci=this.$$method[cf][name];
{ce[ci]=new Function("value",cg.join(""));
};
if(qx.core.Variant.isSet("qx.aspects","on")){ce[ci]=qx.core.Aspect.wrap(cd.classname+"."+ci,ce[ci],"property");
}qx.Bootstrap.setDisplayName(ce[ci],cd.classname+".prototype",ci);
if(ch===undefined){return cd[ci]();
}else{return cd[ci](ch[0]);
}},executeOptimizedGetter:function(cj,ck,name,cl){var cn=ck.$$properties[name];
var cp=ck.prototype;
var cm=[];
var co=this.$$store;
cm.push(e,co.runtime[name],g);
cm.push(k,co.runtime[name],m);

if(cn.inheritable){cm.push(f,co.inherit[name],g);
cm.push(k,co.inherit[name],m);
cm.push(d);
}cm.push(e,co.user[name],g);
cm.push(k,co.user[name],m);

if(cn.themeable){cm.push(f,co.theme[name],g);
cm.push(k,co.theme[name],m);
}
if(cn.deferredInit&&cn.init===undefined){cm.push(f,co.init[name],g);
cm.push(k,co.init[name],m);
}cm.push(d);

if(cn.init!==undefined){if(cn.inheritable){cm.push(u,co.init[name],m);

if(cn.nullable){cm.push(o);
}else if(cn.init!==undefined){cm.push(k,co.init[name],m);
}else{cm.push(Q,name,c,ck.classname,b);
}cm.push(ba);
}else{cm.push(k,co.init[name],m);
}}else if(cn.inheritable||cn.nullable){cm.push(z);
}else{cm.push(W,name,c,ck.classname,b);
}return this.__H(cj,cp,name,cl,cm);
},executeOptimizedSetter:function(cq,cr,name,cs,ct){var cy=cr.$$properties[name];
var cx=cr.prototype;
var cv=[];
var cu=cs===E||cs===K||cs===D||(cs===bi&&cy.init===undefined);
var cw=cy.apply||cy.event||cy.inheritable;
var cz=this.__I(cs,name);
this.__J(cv,cy,name,cs,cu);

if(cu){this.__K(cv,cr,cy,name);
}
if(cw){this.__L(cv,cu,cz,cs);
}
if(cy.inheritable){cv.push(bc);
}{};

if(!cw){this.__N(cv,name,cs,cu);
}else{this.__O(cv,cy,name,cs,cu);
}
if(cy.inheritable){this.__P(cv,cy,name,cs);
}else if(cw){this.__Q(cv,cy,name,cs);
}
if(cw){this.__R(cv,cy,name);
if(cy.inheritable&&cx._getChildren){this.__S(cv,name);
}}if(cu){cv.push(r);
}return this.__H(cq,cx,name,cs,cv,ct);
},__I:function(cA,name){if(cA==="setRuntime"||cA==="resetRuntime"){var cB=this.$$store.runtime[name];
}else if(cA==="setThemed"||cA==="resetThemed"){cB=this.$$store.theme[name];
}else if(cA==="init"){cB=this.$$store.init[name];
}else{cB=this.$$store.user[name];
}return cB;
},__J:function(cC,cD,name,cE,cF){{if(!cD.nullable||cD.check||cD.inheritable){cC.push('var prop=qx.core.Property;');
}if(cE==="set"){cC.push('if(value===undefined)prop.error(this,2,"',name,'","',cE,'",value);');
}};
},__K:function(cG,cH,cI,name){if(cI.transform){cG.push('value=this.',cI.transform,'(value);');
}if(cI.validate){if(typeof cI.validate==="string"){cG.push('this.',cI.validate,'(value);');
}else if(cI.validate instanceof Function){cG.push(cH.classname,'.$$properties.',name);
cG.push('.validate.call(this, value);');
}}},__L:function(cJ,cK,cL,cM){var cN=(cM==="reset"||cM==="resetThemed"||cM==="resetRuntime");

if(cK){cJ.push('if(this.',cL,'===value)return value;');
}else if(cN){cJ.push('if(this.',cL,'===undefined)return;');
}},__M:undefined,__N:function(cO,name,cP,cQ){if(cP==="setRuntime"){cO.push('this.',this.$$store.runtime[name],'=value;');
}else if(cP==="resetRuntime"){cO.push('if(this.',this.$$store.runtime[name],'!==undefined)');
cO.push('delete this.',this.$$store.runtime[name],';');
}else if(cP==="set"){cO.push('this.',this.$$store.user[name],'=value;');
}else if(cP==="reset"){cO.push('if(this.',this.$$store.user[name],'!==undefined)');
cO.push('delete this.',this.$$store.user[name],';');
}else if(cP==="setThemed"){cO.push('this.',this.$$store.theme[name],'=value;');
}else if(cP==="resetThemed"){cO.push('if(this.',this.$$store.theme[name],'!==undefined)');
cO.push('delete this.',this.$$store.theme[name],';');
}else if(cP==="init"&&cQ){cO.push('this.',this.$$store.init[name],'=value;');
}},__O:function(cR,cS,name,cT,cU){if(cS.inheritable){cR.push('var computed, old=this.',this.$$store.inherit[name],';');
}else{cR.push('var computed, old;');
}cR.push('if(this.',this.$$store.runtime[name],'!==undefined){');

if(cT==="setRuntime"){cR.push('computed=this.',this.$$store.runtime[name],'=value;');
}else if(cT==="resetRuntime"){cR.push('delete this.',this.$$store.runtime[name],';');
cR.push('if(this.',this.$$store.user[name],'!==undefined)');
cR.push('computed=this.',this.$$store.user[name],';');
cR.push('else if(this.',this.$$store.theme[name],'!==undefined)');
cR.push('computed=this.',this.$$store.theme[name],';');
cR.push('else if(this.',this.$$store.init[name],'!==undefined){');
cR.push('computed=this.',this.$$store.init[name],';');
cR.push('this.',this.$$store.useinit[name],'=true;');
cR.push('}');
}else{cR.push('old=computed=this.',this.$$store.runtime[name],';');
if(cT==="set"){cR.push('this.',this.$$store.user[name],'=value;');
}else if(cT==="reset"){cR.push('delete this.',this.$$store.user[name],';');
}else if(cT==="setThemed"){cR.push('this.',this.$$store.theme[name],'=value;');
}else if(cT==="resetThemed"){cR.push('delete this.',this.$$store.theme[name],';');
}else if(cT==="init"&&cU){cR.push('this.',this.$$store.init[name],'=value;');
}}cR.push('}');
cR.push('else if(this.',this.$$store.user[name],'!==undefined){');

if(cT==="set"){if(!cS.inheritable){cR.push('old=this.',this.$$store.user[name],';');
}cR.push('computed=this.',this.$$store.user[name],'=value;');
}else if(cT==="reset"){if(!cS.inheritable){cR.push('old=this.',this.$$store.user[name],';');
}cR.push('delete this.',this.$$store.user[name],';');
cR.push('if(this.',this.$$store.runtime[name],'!==undefined)');
cR.push('computed=this.',this.$$store.runtime[name],';');
cR.push('if(this.',this.$$store.theme[name],'!==undefined)');
cR.push('computed=this.',this.$$store.theme[name],';');
cR.push('else if(this.',this.$$store.init[name],'!==undefined){');
cR.push('computed=this.',this.$$store.init[name],';');
cR.push('this.',this.$$store.useinit[name],'=true;');
cR.push('}');
}else{if(cT==="setRuntime"){cR.push('computed=this.',this.$$store.runtime[name],'=value;');
}else if(cS.inheritable){cR.push('computed=this.',this.$$store.user[name],';');
}else{cR.push('old=computed=this.',this.$$store.user[name],';');
}if(cT==="setThemed"){cR.push('this.',this.$$store.theme[name],'=value;');
}else if(cT==="resetThemed"){cR.push('delete this.',this.$$store.theme[name],';');
}else if(cT==="init"&&cU){cR.push('this.',this.$$store.init[name],'=value;');
}}cR.push('}');
if(cS.themeable){cR.push('else if(this.',this.$$store.theme[name],'!==undefined){');

if(!cS.inheritable){cR.push('old=this.',this.$$store.theme[name],';');
}
if(cT==="setRuntime"){cR.push('computed=this.',this.$$store.runtime[name],'=value;');
}else if(cT==="set"){cR.push('computed=this.',this.$$store.user[name],'=value;');
}else if(cT==="setThemed"){cR.push('computed=this.',this.$$store.theme[name],'=value;');
}else if(cT==="resetThemed"){cR.push('delete this.',this.$$store.theme[name],';');
cR.push('if(this.',this.$$store.init[name],'!==undefined){');
cR.push('computed=this.',this.$$store.init[name],';');
cR.push('this.',this.$$store.useinit[name],'=true;');
cR.push('}');
}else if(cT==="init"){if(cU){cR.push('this.',this.$$store.init[name],'=value;');
}cR.push('computed=this.',this.$$store.theme[name],';');
}else if(cT==="refresh"){cR.push('computed=this.',this.$$store.theme[name],';');
}cR.push('}');
}cR.push('else if(this.',this.$$store.useinit[name],'){');

if(!cS.inheritable){cR.push('old=this.',this.$$store.init[name],';');
}
if(cT==="init"){if(cU){cR.push('computed=this.',this.$$store.init[name],'=value;');
}else{cR.push('computed=this.',this.$$store.init[name],';');
}}else if(cT==="set"||cT==="setRuntime"||cT==="setThemed"||cT==="refresh"){cR.push('delete this.',this.$$store.useinit[name],';');

if(cT==="setRuntime"){cR.push('computed=this.',this.$$store.runtime[name],'=value;');
}else if(cT==="set"){cR.push('computed=this.',this.$$store.user[name],'=value;');
}else if(cT==="setThemed"){cR.push('computed=this.',this.$$store.theme[name],'=value;');
}else if(cT==="refresh"){cR.push('computed=this.',this.$$store.init[name],';');
}}cR.push('}');
if(cT==="set"||cT==="setRuntime"||cT==="setThemed"||cT==="init"){cR.push('else{');

if(cT==="setRuntime"){cR.push('computed=this.',this.$$store.runtime[name],'=value;');
}else if(cT==="set"){cR.push('computed=this.',this.$$store.user[name],'=value;');
}else if(cT==="setThemed"){cR.push('computed=this.',this.$$store.theme[name],'=value;');
}else if(cT==="init"){if(cU){cR.push('computed=this.',this.$$store.init[name],'=value;');
}else{cR.push('computed=this.',this.$$store.init[name],';');
}cR.push('this.',this.$$store.useinit[name],'=true;');
}cR.push('}');
}},__P:function(cV,cW,name,cX){cV.push('if(computed===undefined||computed===inherit){');

if(cX==="refresh"){cV.push('computed=value;');
}else{cV.push('var pa=this.getLayoutParent();if(pa)computed=pa.',this.$$store.inherit[name],';');
}cV.push('if((computed===undefined||computed===inherit)&&');
cV.push('this.',this.$$store.init[name],'!==undefined&&');
cV.push('this.',this.$$store.init[name],'!==inherit){');
cV.push('computed=this.',this.$$store.init[name],';');
cV.push('this.',this.$$store.useinit[name],'=true;');
cV.push('}else{');
cV.push('delete this.',this.$$store.useinit[name],';}');
cV.push('}');
cV.push('if(old===computed)return value;');
cV.push('if(computed===inherit){');
cV.push('computed=undefined;delete this.',this.$$store.inherit[name],';');
cV.push('}');
cV.push('else if(computed===undefined)');
cV.push('delete this.',this.$$store.inherit[name],';');
cV.push('else this.',this.$$store.inherit[name],'=computed;');
cV.push('var backup=computed;');
if(cW.init!==undefined&&cX!=="init"){cV.push('if(old===undefined)old=this.',this.$$store.init[name],";");
}else{cV.push('if(old===undefined)old=null;');
}cV.push('if(computed===undefined||computed==inherit)computed=null;');
},__Q:function(cY,da,name,db){if(db!=="set"&&db!=="setRuntime"&&db!=="setThemed"){cY.push('if(computed===undefined)computed=null;');
}cY.push('if(old===computed)return value;');
if(da.init!==undefined&&db!=="init"){cY.push('if(old===undefined)old=this.',this.$$store.init[name],";");
}else{cY.push('if(old===undefined)old=null;');
}},__R:function(dc,dd,name){if(dd.apply){dc.push('this.',dd.apply,'(computed, old, "',name,'");');
}if(dd.event){dc.push("var reg=qx.event.Registration;","if(reg.hasListener(this, '",dd.event,"')){","reg.fireEvent(this, '",dd.event,"', qx.event.type.Data, [computed, old]",")}");
}},__S:function(de,name){de.push('var a=this._getChildren();if(a)for(var i=0,l=a.length;i<l;i++){');
de.push('if(a[i].',this.$$method.refresh[name],')a[i].',this.$$method.refresh[name],'(backup);');
de.push('}');
}},defer:function(df){var dh=navigator.userAgent.indexOf(R)!=-1;
var dg=navigator.userAgent.indexOf(y)!=-1;
if(dh||dg){df.__E=df.__F;
}}});
})();
(function(){var p="qx.aspects",o="on",n=".",m="static",k="[Class ",j="]",h="$$init_",g="constructor",f="member",e=".prototype",b="extend",d="qx.Class",c="qx.event.type.Data";
qx.Bootstrap.define(d,{statics:{define:function(name,q){if(!q){var q={};
}if(q.include&&!(q.include instanceof Array)){q.include=[q.include];
}if(q.implement&&!(q.implement instanceof Array)){q.implement=[q.implement];
}var r=false;

if(!q.hasOwnProperty(b)&&!q.type){q.type=m;
r=true;
}{};
var s=this.__X(name,q.type,q.extend,q.statics,q.construct,q.destruct,q.include);
if(q.extend){if(q.properties){this.__ba(s,q.properties,true);
}if(q.members){this.__bc(s,q.members,true,true,false);
}if(q.events){this.__Y(s,q.events,true);
}if(q.include){for(var i=0,l=q.include.length;i<l;i++){this.__bg(s,q.include[i],false);
}}}if(q.settings){for(var t in q.settings){qx.core.Setting.define(t,q.settings[t]);
}}if(q.variants){for(var t in q.variants){qx.core.Variant.define(t,q.variants[t].allowedValues,q.variants[t].defaultValue);
}}if(q.implement){for(var i=0,l=q.implement.length;i<l;i++){this.__be(s,q.implement[i]);
}}{};
if(q.defer){q.defer.self=s;
q.defer(s,s.prototype,{add:function(name,u){var v={};
v[name]=u;
qx.Class.__ba(s,v,true);
}});
}return s;
},undefine:function(name){delete this.$$registry[name];
var w=name.split(n);
var y=[window];

for(var i=0;i<w.length;i++){y.push(y[i][w[i]]);
}for(var i=y.length-1;i>=1;i--){var x=y[i];
var parent=y[i-1];

if(qx.Bootstrap.isFunction(x)||qx.Bootstrap.objectGetLength(x)===0){delete parent[w[i-1]];
}else{break;
}}},isDefined:qx.Bootstrap.classIsDefined,getTotalNumber:function(){return qx.Bootstrap.objectGetLength(this.$$registry);
},getByName:qx.Bootstrap.getByName,include:function(z,A){{};
qx.Class.__bg(z,A,false);
},patch:function(B,C){{};
qx.Class.__bg(B,C,true);
},isSubClassOf:function(D,E){if(!D){return false;
}
if(D==E){return true;
}
if(D.prototype instanceof E){return true;
}return false;
},getPropertyDefinition:qx.Bootstrap.getPropertyDefinition,getProperties:function(F){var G=[];

while(F){if(F.$$properties){G.push.apply(G,qx.Bootstrap.getKeys(F.$$properties));
}F=F.superclass;
}return G;
},getByProperty:function(H,name){while(H){if(H.$$properties&&H.$$properties[name]){return H;
}H=H.superclass;
}return null;
},hasProperty:qx.Bootstrap.hasProperty,getEventType:qx.Bootstrap.getEventType,supportsEvent:qx.Bootstrap.supportsEvent,hasOwnMixin:function(I,J){return I.$$includes&&I.$$includes.indexOf(J)!==-1;
},getByMixin:function(K,L){var M,i,l;

while(K){if(K.$$includes){M=K.$$flatIncludes;

for(i=0,l=M.length;i<l;i++){if(M[i]===L){return K;
}}}K=K.superclass;
}return null;
},getMixins:qx.Bootstrap.getMixins,hasMixin:function(N,O){return !!this.getByMixin(N,O);
},hasOwnInterface:function(P,Q){return P.$$implements&&P.$$implements.indexOf(Q)!==-1;
},getByInterface:qx.Bootstrap.getByInterface,getInterfaces:function(R){var S=[];

while(R){if(R.$$implements){S.push.apply(S,R.$$flatImplements);
}R=R.superclass;
}return S;
},hasInterface:qx.Bootstrap.hasInterface,implementsInterface:function(T,U){var V=T.constructor;

if(this.hasInterface(V,U)){return true;
}
try{qx.Interface.assertObject(T,U);
return true;
}catch(W){}
try{qx.Interface.assert(V,U,false);
return true;
}catch(X){}return false;
},getInstance:function(){if(!this.$$instance){this.$$allowconstruct=true;
this.$$instance=new this;
delete this.$$allowconstruct;
}return this.$$instance;
},genericToString:function(){return k+this.classname+j;
},$$registry:qx.Bootstrap.$$registry,__T:null,__U:null,__V:function(){},__W:function(){},__X:function(name,Y,ba,bb,bc,bd,be){var bh;

if(!ba&&qx.core.Variant.isSet("qx.aspects","off")){bh=bb||{};
qx.Bootstrap.setDisplayNames(bh,name);
}else{var bh={};

if(ba){if(!bc){bc=this.__bh();
}
if(this.__bj(ba,be)){bh=this.__bk(bc,name,Y);
}else{bh=bc;
}if(Y==="singleton"){bh.getInstance=this.getInstance;
}qx.Bootstrap.setDisplayName(bc,name,"constructor");
}if(bb){qx.Bootstrap.setDisplayNames(bb,name);
var bi;

for(var i=0,a=qx.Bootstrap.getKeys(bb),l=a.length;i<l;i++){bi=a[i];
var bf=bb[bi];

if(qx.core.Variant.isSet("qx.aspects","on")){if(bf instanceof Function){bf=qx.core.Aspect.wrap(name+"."+bi,bf,"static");
}bh[bi]=bf;
}else{bh[bi]=bf;
}}}}var bg=qx.Bootstrap.createNamespace(name,bh);
bh.name=bh.classname=name;
bh.basename=bg;
bh.$$type="Class";

if(Y){bh.$$classtype=Y;
}if(!bh.hasOwnProperty("toString")){bh.toString=this.genericToString;
}
if(ba){qx.Bootstrap.extendClass(bh,bc,ba,name,bg);
if(bd){if(qx.core.Variant.isSet("qx.aspects","on")){bd=qx.core.Aspect.wrap(name,bd,"destructor");
}bh.$$destructor=bd;
qx.Bootstrap.setDisplayName(bd,name,"destruct");
}}this.$$registry[name]=bh;
return bh;
},__Y:function(bj,bk,bl){var bm,bm;
{};

if(bj.$$events){for(var bm in bk){bj.$$events[bm]=bk[bm];
}}else{bj.$$events=bk;
}},__ba:function(bn,bo,bp){var bq;

if(bp===undefined){bp=false;
}var br=bn.prototype;

for(var name in bo){bq=bo[name];
{};
bq.name=name;
if(!bq.refine){if(bn.$$properties===undefined){bn.$$properties={};
}bn.$$properties[name]=bq;
}if(bq.init!==undefined){bn.prototype[h+name]=bq.init;
}if(bq.event!==undefined){var event={};
event[bq.event]=c;
this.__Y(bn,event,bp);
}if(bq.inheritable){qx.core.Property.$$inheritable[name]=true;

if(!br.$$refreshInheritables){qx.core.Property.attachRefreshInheritables(bn);
}}
if(!bq.refine){qx.core.Property.attachMethods(bn,name,bq);
}}},__bb:null,__bc:function(bs,bt,bu,bv,bw){var bx=bs.prototype;
var bz,by;
qx.Bootstrap.setDisplayNames(bt,bs.classname+e);

for(var i=0,a=qx.Bootstrap.getKeys(bt),l=a.length;i<l;i++){bz=a[i];
by=bt[bz];
{};
if(bv!==false&&by instanceof Function&&by.$$type==null){if(bw==true){by=this.__bd(by,bx[bz]);
}else{if(bx[bz]){by.base=bx[bz];
}by.self=bs;
}
if(qx.core.Variant.isSet(p,o)){by=qx.core.Aspect.wrap(bs.classname+n+bz,by,f);
}}bx[bz]=by;
}},__bd:function(bA,bB){if(bB){return function(){var bD=bA.base;
bA.base=bB;
var bC=bA.apply(this,arguments);
bA.base=bD;
return bC;
};
}else{return bA;
}},__be:function(bE,bF){{};
var bG=qx.Interface.flatten([bF]);

if(bE.$$implements){bE.$$implements.push(bF);
bE.$$flatImplements.push.apply(bE.$$flatImplements,bG);
}else{bE.$$implements=[bF];
bE.$$flatImplements=bG;
}},__bf:function(bH){var name=bH.classname;
var bI=this.__bk(bH,name,bH.$$classtype);
for(var i=0,a=qx.Bootstrap.getKeys(bH),l=a.length;i<l;i++){bJ=a[i];
bI[bJ]=bH[bJ];
}bI.prototype=bH.prototype;
var bL=bH.prototype;

for(var i=0,a=qx.Bootstrap.getKeys(bL),l=a.length;i<l;i++){bJ=a[i];
var bM=bL[bJ];
if(bM&&bM.self==bH){bM.self=bI;
}}for(var bJ in this.$$registry){var bK=this.$$registry[bJ];

if(!bK){continue;
}
if(bK.base==bH){bK.base=bI;
}
if(bK.superclass==bH){bK.superclass=bI;
}
if(bK.$$original){if(bK.$$original.base==bH){bK.$$original.base=bI;
}
if(bK.$$original.superclass==bH){bK.$$original.superclass=bI;
}}}qx.Bootstrap.createNamespace(name,bI);
this.$$registry[name]=bI;
return bI;
},__bg:function(bN,bO,bP){{};

if(this.hasMixin(bN,bO)){return;
}var bS=bN.$$original;

if(bO.$$constructor&&!bS){bN=this.__bf(bN);
}var bR=qx.Mixin.flatten([bO]);
var bQ;

for(var i=0,l=bR.length;i<l;i++){bQ=bR[i];
if(bQ.$$events){this.__Y(bN,bQ.$$events,bP);
}if(bQ.$$properties){this.__ba(bN,bQ.$$properties,bP);
}if(bQ.$$members){this.__bc(bN,bQ.$$members,bP,bP,bP);
}}if(bN.$$includes){bN.$$includes.push(bO);
bN.$$flatIncludes.push.apply(bN.$$flatIncludes,bR);
}else{bN.$$includes=[bO];
bN.$$flatIncludes=bR;
}},__bh:function(){function bT(){bT.base.apply(this,arguments);
}return bT;
},__bi:function(){return function(){};
},__bj:function(bU,bV){{};
if(bU&&bU.$$includes){var bW=bU.$$flatIncludes;

for(var i=0,l=bW.length;i<l;i++){if(bW[i].$$constructor){return true;
}}}if(bV){var bX=qx.Mixin.flatten(bV);

for(var i=0,l=bX.length;i<l;i++){if(bX[i].$$constructor){return true;
}}}return false;
},__bk:function(bY,name,ca){var cc=function(){var cf=cc;
{};
var ce=cf.$$original.apply(this,arguments);
if(cf.$$includes){var cd=cf.$$flatIncludes;

for(var i=0,l=cd.length;i<l;i++){if(cd[i].$$constructor){cd[i].$$constructor.apply(this,arguments);
}}}{};
return ce;
};

if(qx.core.Variant.isSet(p,o)){var cb=qx.core.Aspect.wrap(name,cc,g);
cc.$$original=bY;
cc.constructor=cb;
cc=cb;
}cc.$$original=bY;
bY.wrapper=cc;
return cc;
}},defer:function(){if(qx.core.Variant.isSet(p,o)){for(var cg in qx.Bootstrap.$$registry){var ch=qx.Bootstrap.$$registry[cg];

for(var ci in ch){if(ch[ci] instanceof Function){ch[ci]=qx.core.Aspect.wrap(cg+n+ci,ch[ci],m);
}}}}}});
})();
(function(){var a="qx.lang.RingBuffer";
qx.Class.define(a,{extend:Object,construct:function(b){this.setMaxEntries(b||50);
},members:{__bl:0,__bm:0,__bn:false,__bo:0,__bp:null,__bq:null,setMaxEntries:function(c){this.__bq=c;
this.clear();
},getMaxEntries:function(){return this.__bq;
},addEntry:function(d){this.__bp[this.__bl]=d;
this.__bl=this.__br(this.__bl,1);
var e=this.getMaxEntries();

if(this.__bm<e){this.__bm++;
}if(this.__bn&&(this.__bo<e)){this.__bo++;
}},mark:function(){this.__bn=true;
this.__bo=0;
},clearMark:function(){this.__bn=false;
},getAllEntries:function(){return this.getEntries(this.getMaxEntries(),false);
},getEntries:function(f,g){if(f>this.__bm){f=this.__bm;
}if(g&&this.__bn&&(f>this.__bo)){f=this.__bo;
}
if(f>0){var i=this.__br(this.__bl,-1);
var h=this.__br(i,-f+1);
var j;

if(h<=i){j=this.__bp.slice(h,i+1);
}else{j=this.__bp.slice(h,this.__bm).concat(this.__bp.slice(0,i+1));
}}else{j=[];
}return j;
},clear:function(){this.__bp=new Array(this.getMaxEntries());
this.__bm=0;
this.__bo=0;
this.__bl=0;
},__br:function(k,l){var m=this.getMaxEntries();
var n=(k+l)%m;
if(n<0){n+=m;
}return n;
}}});
})();
(function(){var a="qx.log.appender.RingBuffer";
qx.Class.define(a,{extend:qx.lang.RingBuffer,construct:function(b){this.setMaxMessages(b||50);
},members:{setMaxMessages:function(c){this.setMaxEntries(c);
},getMaxMessages:function(){return this.getMaxEntries();
},process:function(d){this.addEntry(d);
},getAllLogEvents:function(){return this.getAllEntries();
},retrieveLogEvents:function(e,f){return this.getEntries(e,f);
},clearHistory:function(){this.clear();
}}});
})();
(function(){var g="mshtml",f="qx.client",e="[object Array]",d="qx.lang.Array",c="qx",b="number",a="string";
qx.Class.define(d,{statics:{toArray:function(h,j){return this.cast(h,Array,j);
},cast:function(k,m,n){if(k.constructor===m){return k;
}
if(qx.Class.hasInterface(k,qx.data.IListData)){var k=k.toArray();
}var o=new m;
if(qx.core.Variant.isSet(f,g)){if(k.item){for(var i=n||0,l=k.length;i<l;i++){o.push(k[i]);
}return o;
}}if(Object.prototype.toString.call(k)===e&&n==null){o.push.apply(o,k);
}else{o.push.apply(o,Array.prototype.slice.call(k,n||0));
}return o;
},fromArguments:function(p,q){return Array.prototype.slice.call(p,q||0);
},fromCollection:function(r){if(qx.core.Variant.isSet(f,g)){if(r.item){var s=[];

for(var i=0,l=r.length;i<l;i++){s[i]=r[i];
}return s;
}}return Array.prototype.slice.call(r,0);
},fromShortHand:function(t){var v=t.length;
var u=qx.lang.Array.clone(t);
switch(v){case 1:u[1]=u[2]=u[3]=u[0];
break;
case 2:u[2]=u[0];
case 3:u[3]=u[1];
}return u;
},clone:function(w){return w.concat();
},insertAt:function(x,y,i){x.splice(i,0,y);
return x;
},insertBefore:function(z,A,B){var i=z.indexOf(B);

if(i==-1){z.push(A);
}else{z.splice(i,0,A);
}return z;
},insertAfter:function(C,D,E){var i=C.indexOf(E);

if(i==-1||i==(C.length-1)){C.push(D);
}else{C.splice(i+1,0,D);
}return C;
},removeAt:function(F,i){return F.splice(i,1)[0];
},removeAll:function(G){G.length=0;
return this;
},append:function(H,I){{};
Array.prototype.push.apply(H,I);
return H;
},exclude:function(J,K){{};

for(var i=0,M=K.length,L;i<M;i++){L=J.indexOf(K[i]);

if(L!=-1){J.splice(L,1);
}}return J;
},remove:function(N,O){var i=N.indexOf(O);

if(i!=-1){N.splice(i,1);
return O;
}},contains:function(P,Q){return P.indexOf(Q)!==-1;
},equals:function(R,S){var length=R.length;

if(length!==S.length){return false;
}
for(var i=0;i<length;i++){if(R[i]!==S[i]){return false;
}}return true;
},sum:function(T){var U=0;

for(var i=0,l=T.length;i<l;i++){U+=T[i];
}return U;
},max:function(V){{};
var i,X=V.length,W=V[0];

for(i=1;i<X;i++){if(V[i]>W){W=V[i];
}}return W===undefined?null:W;
},min:function(Y){{};
var i,bb=Y.length,ba=Y[0];

for(i=1;i<bb;i++){if(Y[i]<ba){ba=Y[i];
}}return ba===undefined?null:ba;
},unique:function(bc){var bm=[],be={},bh={},bj={};
var bi,bd=0;
var bn=c+qx.lang.Date.now();
var bf=false,bl=false,bo=false;
for(var i=0,bk=bc.length;i<bk;i++){bi=bc[i];
if(bi===null){if(!bf){bf=true;
bm.push(bi);
}}else if(bi===undefined){}else if(bi===false){if(!bl){bl=true;
bm.push(bi);
}}else if(bi===true){if(!bo){bo=true;
bm.push(bi);
}}else if(typeof bi===a){if(!be[bi]){be[bi]=1;
bm.push(bi);
}}else if(typeof bi===b){if(!bh[bi]){bh[bi]=1;
bm.push(bi);
}}else{bg=bi[bn];

if(bg==null){bg=bi[bn]=bd++;
}
if(!bj[bg]){bj[bg]=bi;
bm.push(bi);
}}}for(var bg in bj){try{delete bj[bg][bn];
}catch(bp){try{bj[bg][bn]=null;
}catch(bq){throw new Error("Cannot clean-up map entry doneObjects["+bg+"]["+bn+"]");
}}}return bm;
}}});
})();
(function(){var f="()",e=".",d=".prototype.",c='anonymous()',b="qx.lang.Function",a=".constructor()";
qx.Class.define(b,{statics:{getCaller:function(g){return g.caller?g.caller.callee:g.callee.caller;
},getName:function(h){if(h.displayName){return h.displayName;
}
if(h.$$original||h.wrapper||h.classname){return h.classname+a;
}
if(h.$$mixin){for(var j in h.$$mixin.$$members){if(h.$$mixin.$$members[j]==h){return h.$$mixin.name+d+j+f;
}}for(var j in h.$$mixin){if(h.$$mixin[j]==h){return h.$$mixin.name+e+j+f;
}}}
if(h.self){var k=h.self.constructor;

if(k){for(var j in k.prototype){if(k.prototype[j]==h){return k.classname+d+j+f;
}}for(var j in k){if(k[j]==h){return k.classname+e+j+f;
}}}}var i=h.toString().match(/function\s*(\w*)\s*\(.*/);

if(i&&i.length>=1&&i[1]){return i[1]+f;
}return c;
},globalEval:function(l){if(window.execScript){return window.execScript(l);
}else{return eval.call(window,l);
}},empty:function(){},returnTrue:function(){return true;
},returnFalse:function(){return false;
},returnNull:function(){return null;
},returnThis:function(){return this;
},returnZero:function(){return 0;
},create:function(m,n){{};
if(!n){return m;
}if(!(n.self||n.args||n.delay!=null||n.periodical!=null||n.attempt)){return m;
}return function(event){{};
var p=qx.lang.Array.fromArguments(arguments);
if(n.args){p=n.args.concat(p);
}
if(n.delay||n.periodical){var o=qx.event.GlobalError.observeMethod(function(){return m.apply(n.self||this,p);
});

if(n.delay){return window.setTimeout(o,n.delay);
}
if(n.periodical){return window.setInterval(o,n.periodical);
}}else if(n.attempt){var q=false;

try{q=m.apply(n.self||this,p);
}catch(r){}return q;
}else{return m.apply(n.self||this,p);
}};
},bind:function(s,self,t){return this.create(s,{self:self,args:arguments.length>2?qx.lang.Array.fromArguments(arguments,2):null});
},curry:function(u,v){return this.create(u,{args:arguments.length>1?qx.lang.Array.fromArguments(arguments,1):null});
},listener:function(w,self,x){if(arguments.length<3){return function(event){return w.call(self||this,event||window.event);
};
}else{var y=qx.lang.Array.fromArguments(arguments,2);
return function(event){var z=[event||window.event];
z.push.apply(z,y);
w.apply(self||this,z);
};
}},attempt:function(A,self,B){return this.create(A,{self:self,attempt:true,args:arguments.length>2?qx.lang.Array.fromArguments(arguments,2):null})();
},delay:function(C,D,self,E){return this.create(C,{delay:D,self:self,args:arguments.length>3?qx.lang.Array.fromArguments(arguments,3):null})();
},periodical:function(F,G,self,H){return this.create(F,{periodical:G,self:self,args:arguments.length>3?qx.lang.Array.fromArguments(arguments,3):null})();
}}});
})();
(function(){var m=":",l="qx.client",k="Error created at",j="anonymous",h="...",g="qx.dev.StackTrace",f="",e="\n",d="?",c="/source/class/",a="of linked script",b=".";
qx.Class.define(g,{statics:{getStackTrace:qx.core.Variant.select(l,{"gecko":function(){try{throw new Error();
}catch(A){var u=this.getStackTraceFromError(A);
qx.lang.Array.removeAt(u,0);
var s=this.getStackTraceFromCaller(arguments);
var q=s.length>u.length?s:u;

for(var i=0;i<Math.min(s.length,u.length);i++){var r=s[i];

if(r.indexOf(j)>=0){continue;
}var y=r.split(m);

if(y.length!=2){continue;
}var w=y[0];
var p=y[1];
var o=u[i];
var z=o.split(m);
var v=z[0];
var n=z[1];

if(qx.Class.getByName(v)){var t=v;
}else{t=w;
}var x=t+m;

if(p){x+=p+m;
}x+=n;
q[i]=x;
}return q;
}},"mshtml|webkit":function(){return this.getStackTraceFromCaller(arguments);
},"opera":function(){var B;

try{B.bar();
}catch(D){var C=this.getStackTraceFromError(D);
qx.lang.Array.removeAt(C,0);
return C;
}return [];
}}),getStackTraceFromCaller:qx.core.Variant.select(l,{"opera":function(E){return [];
},"default":function(F){var K=[];
var J=qx.lang.Function.getCaller(F);
var G={};

while(J){var H=qx.lang.Function.getName(J);
K.push(H);

try{J=J.caller;
}catch(L){break;
}
if(!J){break;
}var I=qx.core.ObjectRegistry.toHashCode(J);

if(G[I]){K.push(h);
break;
}G[I]=J;
}return K;
}}),getStackTraceFromError:qx.core.Variant.select(l,{"gecko":function(M){if(!M.stack){return [];
}var S=/@(.+):(\d+)$/gm;
var N;
var O=[];

while((N=S.exec(M.stack))!=null){var P=N[1];
var R=N[2];
var Q=this.__bs(P);
O.push(Q+m+R);
}return O;
},"webkit":function(T){if(T.stack){var bb=/at (.*)/gm;
var ba=/\((.*?)(:[^\/].*)\)/;
var X=/(.*?)(:[^\/].*)/;
var U;
var V=[];

while((U=bb.exec(T.stack))!=null){var W=ba.exec(U[1]);

if(!W){W=X.exec(U[1]);
}
if(W){var Y=this.__bs(W[1]);
V.push(Y+W[2]);
}else{V.push(U[1]);
}}return V;
}else if(T.sourceURL&&T.line){return [this.__bs(T.sourceURL)+m+T.line];
}else{return [];
}},"opera":function(bc){if(bc.stacktrace){var be=bc.stacktrace;

if(be.indexOf(k)>=0){be=be.split(k)[0];
}if(be.indexOf(a)>=0){var bo=/Line\ (\d+?)\ of\ linked\ script\ (.*?)$/gm;
var bf;
var bg=[];

while((bf=bo.exec(be))!=null){var bn=bf[1];
var bi=bf[2];
var bm=this.__bs(bi);
bg.push(bm+m+bn);
}}else{var bo=/line\ (\d+?),\ column\ (\d+?)\ in\ (?:.*?)\ in\ (.*?):[^\/]/gm;
var bf;
var bg=[];

while((bf=bo.exec(be))!=null){var bn=bf[1];
var bh=bf[2];
var bi=bf[3];
var bm=this.__bs(bi);
bg.push(bm+m+bn+m+bh);
}}return bg;
}else if(bc.message.indexOf("Backtrace:")>=0){var bg=[];
var bj=qx.lang.String.trim(bc.message.split("Backtrace:")[1]);
var bk=bj.split(e);

for(var i=0;i<bk.length;i++){var bd=bk[i].match(/\s*Line ([0-9]+) of.* (\S.*)/);

if(bd&&bd.length>=2){var bn=bd[1];
var bl=this.__bs(bd[2]);
bg.push(bl+m+bn);
}}return bg;
}else{return [];
}},"default":function(){return [];
}}),__bs:function(bp){var bt=c;
var bq=bp.indexOf(bt);
var bs=bp.indexOf(d);

if(bs>=0){bp=bp.substring(0,bs);
}var br=(bq==-1)?bp:bp.substring(bq+bt.length).replace(/\//g,b).replace(/\.js$/,f);
return br;
}}});
})();
(function(){var k="",j="g",h="0",g='\\$1',f="%",e='-',d="qx.lang.String",c=' ',b='\n',a="undefined";
qx.Class.define(d,{statics:{camelCase:function(l){return l.replace(/\-([a-z])/g,function(m,n){return n.toUpperCase();
});
},hyphenate:function(o){return o.replace(/[A-Z]/g,function(p){return (e+p.charAt(0).toLowerCase());
});
},capitalize:function(q){return q.replace(/\b[a-z]/g,function(r){return r.toUpperCase();
});
},clean:function(s){return this.trim(s.replace(/\s+/g,c));
},trimLeft:function(t){return t.replace(/^\s+/,k);
},trimRight:function(u){return u.replace(/\s+$/,k);
},trim:function(v){return v.replace(/^\s+|\s+$/g,k);
},startsWith:function(w,x){return w.indexOf(x)===0;
},endsWith:function(y,z){return y.substring(y.length-z.length,y.length)===z;
},repeat:function(A,B){return A.length>0?new Array(B+1).join(A):k;
},pad:function(C,length,D){var E=length-C.length;

if(E>0){if(typeof D===a){D=h;
}return this.repeat(D,E)+C;
}else{return C;
}},firstUp:qx.Bootstrap.firstUp,firstLow:qx.Bootstrap.firstLow,contains:function(F,G){return F.indexOf(G)!=-1;
},format:function(H,I){var J=H;

for(var i=0;i<I.length;i++){J=J.replace(new RegExp(f+(i+1),j),I[i]+k);
}return J;
},escapeRegexpChars:function(K){return K.replace(/([.*+?^${}()|[\]\/\\])/g,g);
},toArray:function(L){return L.split(/\B|\b/g);
},stripTags:function(M){return M.replace(/<\/?[^>]+>/gi,k);
},stripScripts:function(N,O){var Q=k;
var P=N.replace(/<script[^>]*>([\s\S]*?)<\/script>/gi,function(){Q+=arguments[1]+b;
return k;
});

if(O===true){qx.lang.Function.globalEval(Q);
}return P;
}}});
})();
(function(){var k="node",j="error",h="...(+",g="array",f=")",e="info",d="instance",c="string",b="null",a="class",H="number",G="stringify",F="]",E="date",D="unknown",C="function",B="boolean",A="debug",z="map",y="undefined",s="qx.log.Logger",t="[",q="#",r="warn",o="document",p="{...(",m="text[",n="[...(",u="\n",v=")}",x=")]",w="object";
qx.Class.define(s,{statics:{__bt:A,setLevel:function(I){this.__bt=I;
},getLevel:function(){return this.__bt;
},setTreshold:function(J){this.__bw.setMaxMessages(J);
},getTreshold:function(){return this.__bw.getMaxMessages();
},__bu:{},__bv:0,register:function(K){if(K.$$id){return;
}var M=this.__bv++;
this.__bu[M]=K;
K.$$id=M;
var L=this.__bx;
var N=this.__bw.getAllLogEvents();

for(var i=0,l=N.length;i<l;i++){if(L[N[i].level]>=L[this.__bt]){K.process(N[i]);
}}},unregister:function(O){var P=O.$$id;

if(P==null){return;
}delete this.__bu[P];
delete O.$$id;
},debug:function(Q,R){qx.log.Logger.__by(A,arguments);
},info:function(S,T){qx.log.Logger.__by(e,arguments);
},warn:function(U,V){qx.log.Logger.__by(r,arguments);
},error:function(W,X){qx.log.Logger.__by(j,arguments);
},trace:function(Y){qx.log.Logger.__by(e,[Y,qx.dev.StackTrace.getStackTrace().join(u)]);
},deprecatedMethodWarning:function(ba,bb){var bc;
{};
},deprecatedClassWarning:function(bd,be){var bf;
{};
},deprecatedEventWarning:function(bg,event,bh){var bi;
{};
},deprecatedMixinWarning:function(bj,bk){var bl;
{};
},deprecatedConstantWarning:function(bm,bn,bo){var self,bp;
{};
},deprecateMethodOverriding:function(bq,br,bs,bt){var bu;
{};
},clear:function(){this.__bw.clearHistory();
},__bw:new qx.log.appender.RingBuffer(50),__bx:{debug:0,info:1,warn:2,error:3},__by:function(bv,bw){var bB=this.__bx;

if(bB[bv]<bB[this.__bt]){return;
}var by=bw.length<2?null:bw[0];
var bA=by?1:0;
var bx=[];

for(var i=bA,l=bw.length;i<l;i++){bx.push(this.__bA(bw[i],true));
}var bC=new Date;
var bD={time:bC,offset:bC-qx.Bootstrap.LOADSTART,level:bv,items:bx,win:window};
if(by){if(by.$$hash!==undefined){bD.object=by.$$hash;
}else if(by.$$type){bD.clazz=by;
}}this.__bw.process(bD);
var bE=this.__bu;

for(var bz in bE){bE[bz].process(bD);
}},__bz:function(bF){if(bF===undefined){return y;
}else if(bF===null){return b;
}
if(bF.$$type){return a;
}var bG=typeof bF;

if(bG===C||bG==c||bG===H||bG===B){return bG;
}else if(bG===w){if(bF.nodeType){return k;
}else if(bF.classname){return d;
}else if(bF instanceof Array){return g;
}else if(bF instanceof Error){return j;
}else if(bF instanceof Date){return E;
}else{return z;
}}
if(bF.toString){return G;
}return D;
},__bA:function(bH,bI){var bP=this.__bz(bH);
var bL=D;
var bK=[];

switch(bP){case b:case y:bL=bP;
break;
case c:case H:case B:case E:bL=bH;
break;
case k:if(bH.nodeType===9){bL=o;
}else if(bH.nodeType===3){bL=m+bH.nodeValue+F;
}else if(bH.nodeType===1){bL=bH.nodeName.toLowerCase();

if(bH.id){bL+=q+bH.id;
}}else{bL=k;
}break;
case C:bL=qx.lang.Function.getName(bH)||bP;
break;
case d:bL=bH.basename+t+bH.$$hash+F;
break;
case a:case G:bL=bH.toString();
break;
case j:bK=qx.dev.StackTrace.getStackTraceFromError(bH);
bL=bH.toString();
break;
case g:if(bI){bL=[];

for(var i=0,l=bH.length;i<l;i++){if(bL.length>20){bL.push(h+(l-i)+f);
break;
}bL.push(this.__bA(bH[i],false));
}}else{bL=n+bH.length+x;
}break;
case z:if(bI){var bJ;
var bO=[];

for(var bN in bH){bO.push(bN);
}bO.sort();
bL=[];

for(var i=0,l=bO.length;i<l;i++){if(bL.length>20){bL.push(h+(l-i)+f);
break;
}bN=bO[i];
bJ=this.__bA(bH[bN],false);
bJ.key=bN;
bL.push(bJ);
}}else{var bM=0;

for(var bN in bH){bM++;
}bL=p+bM+v;
}break;
}return {type:bP,text:bL,trace:bK};
}},defer:function(bQ){var bR=qx.Bootstrap.$$logs;

for(var i=0;i<bR.length;i++){bQ.__by(bR[i][0],bR[i][1]);
}qx.Bootstrap.debug=bQ.debug;
qx.Bootstrap.info=bQ.info;
qx.Bootstrap.warn=bQ.warn;
qx.Bootstrap.error=bQ.error;
qx.Bootstrap.trace=bQ.trace;
}});
})();
(function(){var e="$$hash",d="",c="qx.core.ObjectRegistry";
qx.Class.define(c,{statics:{inShutDown:false,__bB:{},__bC:0,__bD:[],register:function(f){var j=this.__bB;

if(!j){return;
}var h=f.$$hash;

if(h==null){var g=this.__bD;

if(g.length>0){h=g.pop();
}else{h=(this.__bC++)+d;
}f.$$hash=h;
}{};
j[h]=f;
},unregister:function(k){var m=k.$$hash;

if(m==null){return;
}var n=this.__bB;

if(n&&n[m]){delete n[m];
this.__bD.push(m);
}try{delete k.$$hash;
}catch(o){if(k.removeAttribute){k.removeAttribute(e);
}}},toHashCode:function(p){{};
var r=p.$$hash;

if(r!=null){return r;
}var q=this.__bD;

if(q.length>0){r=q.pop();
}else{r=(this.__bC++)+d;
}return p.$$hash=r;
},clearHashCode:function(s){{};
var t=s.$$hash;

if(t!=null){this.__bD.push(t);
try{delete s.$$hash;
}catch(u){if(s.removeAttribute){s.removeAttribute(e);
}}}},fromHashCode:function(v){return this.__bB[v]||null;
},shutdown:function(){this.inShutDown=true;
var x=this.__bB;
var z=[];

for(var y in x){z.push(y);
}z.sort(function(a,b){return parseInt(b,10)-parseInt(a,10);
});
var w,i=0,l=z.length;

while(true){try{for(;i<l;i++){y=z[i];
w=x[y];

if(w&&w.dispose){w.dispose();
}}}catch(A){qx.Bootstrap.error(this,"Could not dispose object "+w.toString()+": "+A);

if(i!==l){i++;
continue;
}}break;
}qx.Bootstrap.debug(this,"Disposed "+l+" objects");
delete this.__bB;
},getRegistry:function(){return this.__bB;
}}});
})();
(function(){var j="on",i="qx.client",h="gecko",g="function",f="HTMLEvents",d="mousedown",c="qx.bom.Event",b="return;",a="mouseover";
qx.Class.define(c,{statics:{addNativeListener:function(k,l,m,n){if(k.addEventListener){k.addEventListener(l,m,!!n);
}else if(k.attachEvent){k.attachEvent(j+l,m);
}},removeNativeListener:function(o,p,q,r){if(o.removeEventListener){o.removeEventListener(p,q,!!r);
}else if(o.detachEvent){try{o.detachEvent(j+p,q);
}catch(e){if(e.number!==-2146828218){throw e;
}}}},getTarget:function(e){return e.target||e.srcElement;
},getRelatedTarget:function(e){if(e.relatedTarget!==undefined){if(qx.core.Variant.isSet(i,h)){try{e.relatedTarget&&e.relatedTarget.nodeType;
}catch(e){return null;
}}return e.relatedTarget;
}else if(e.fromElement!==undefined&&e.type===a){return e.fromElement;
}else if(e.toElement!==undefined){return e.toElement;
}else{return null;
}},preventDefault:function(e){if(e.preventDefault){if(qx.core.Variant.isSet(i,h)&&qx.bom.client.Engine.VERSION>=1.9&&e.type==d&&e.button==2){return;
}e.preventDefault();
if(qx.core.Variant.isSet(i,h)&&qx.bom.client.Engine.VERSION<1.9){try{e.keyCode=0;
}catch(s){}}}else{try{e.keyCode=0;
}catch(t){}e.returnValue=false;
}},stopPropagation:function(e){if(e.stopPropagation){e.stopPropagation();
}else{e.cancelBubble=true;
}},fire:function(u,v){if(document.createEvent){var w=document.createEvent(f);
w.initEvent(v,true,true);
return !u.dispatchEvent(w);
}else{var w=document.createEventObject();
return u.fireEvent(j+v,w);
}},supportsEvent:qx.core.Variant.select(i,{"webkit":function(x,y){return x.hasOwnProperty(j+y);
},"default":function(z,A){var B=j+A;
var C=(B in z);

if(!C){C=typeof z[B]==g;

if(!C&&z.setAttribute){z.setAttribute(B,b);
C=typeof z[B]==g;
z.removeAttribute(B);
}}return C;
}})}});
})();
(function(){var r="|bubble",q="|capture",p="|",o="",n="_",m="unload",k="UNKNOWN_",j="__bJ",h="c",g="DOM_",c="__bI",f="WIN_",e="QX_",b="qx.event.Manager",a="capture",d="DOCUMENT_";
qx.Class.define(b,{extend:Object,construct:function(s,t){this.__bE=s;
this.__bF=qx.core.ObjectRegistry.toHashCode(s);
this.__bG=t;
if(s.qx!==qx){var self=this;
qx.bom.Event.addNativeListener(s,m,qx.event.GlobalError.observeMethod(function(){qx.bom.Event.removeNativeListener(s,m,arguments.callee);
self.dispose();
}));
}this.__bH={};
this.__bI={};
this.__bJ={};
this.__bK={};
},statics:{__bL:0,getNextUniqueId:function(){return (this.__bL++)+o;
}},members:{__bG:null,__bH:null,__bJ:null,__bM:null,__bI:null,__bK:null,__bE:null,__bF:null,getWindow:function(){return this.__bE;
},getWindowId:function(){return this.__bF;
},getHandler:function(u){var v=this.__bI[u.classname];

if(v){return v;
}return this.__bI[u.classname]=new u(this);
},getDispatcher:function(w){var x=this.__bJ[w.classname];

if(x){return x;
}return this.__bJ[w.classname]=new w(this,this.__bG);
},getListeners:function(y,z,A){var B=y.$$hash||qx.core.ObjectRegistry.toHashCode(y);
var D=this.__bH[B];

if(!D){return null;
}var E=z+(A?q:r);
var C=D[E];
return C?C.concat():null;
},serializeListeners:function(F){var M=F.$$hash||qx.core.ObjectRegistry.toHashCode(F);
var O=this.__bH[M];
var K=[];

if(O){var I,N,G,J,L;

for(var H in O){I=H.indexOf(p);
N=H.substring(0,I);
G=H.charAt(I+1)==h;
J=O[H];

for(var i=0,l=J.length;i<l;i++){L=J[i];
K.push({self:L.context,handler:L.handler,type:N,capture:G});
}}}return K;
},toggleAttachedEvents:function(P,Q){var V=P.$$hash||qx.core.ObjectRegistry.toHashCode(P);
var X=this.__bH[V];

if(X){var S,W,R,T;

for(var U in X){S=U.indexOf(p);
W=U.substring(0,S);
R=U.charCodeAt(S+1)===99;
T=X[U];

if(Q){this.__bN(P,W,R);
}else{this.__bO(P,W,R);
}}}},hasListener:function(Y,ba,bb){{};
var bc=Y.$$hash||qx.core.ObjectRegistry.toHashCode(Y);
var be=this.__bH[bc];

if(!be){return false;
}var bf=ba+(bb?q:r);
var bd=be[bf];
return !!(bd&&bd.length>0);
},importListeners:function(bg,bh){{};
var bn=bg.$$hash||qx.core.ObjectRegistry.toHashCode(bg);
var bo=this.__bH[bn]={};
var bk=qx.event.Manager;

for(var bi in bh){var bl=bh[bi];
var bm=bl.type+(bl.capture?q:r);
var bj=bo[bm];

if(!bj){bj=bo[bm]=[];
this.__bN(bg,bl.type,bl.capture);
}bj.push({handler:bl.listener,context:bl.self,unique:bl.unique||(bk.__bL++)+o});
}},addListener:function(bp,bq,br,self,bs){var bw;
{};
var bx=bp.$$hash||qx.core.ObjectRegistry.toHashCode(bp);
var bz=this.__bH[bx];

if(!bz){bz=this.__bH[bx]={};
}var bv=bq+(bs?q:r);
var bu=bz[bv];

if(!bu){bu=bz[bv]=[];
}if(bu.length===0){this.__bN(bp,bq,bs);
}var by=(qx.event.Manager.__bL++)+o;
var bt={handler:br,context:self,unique:by};
bu.push(bt);
return bv+p+by;
},findHandler:function(bA,bB){var bN=false,bF=false,bO=false,bC=false;
var bL;

if(bA.nodeType===1){bN=true;
bL=g+bA.tagName.toLowerCase()+n+bB;
}else if(bA.nodeType===9){bC=true;
bL=d+bB;
}else if(bA==this.__bE){bF=true;
bL=f+bB;
}else if(bA.classname){bO=true;
bL=e+bA.classname+n+bB;
}else{bL=k+bA+n+bB;
}var bH=this.__bK;

if(bH[bL]){return bH[bL];
}var bK=this.__bG.getHandlers();
var bG=qx.event.IEventHandler;
var bI,bJ,bE,bD;

for(var i=0,l=bK.length;i<l;i++){bI=bK[i];
bE=bI.SUPPORTED_TYPES;

if(bE&&!bE[bB]){continue;
}bD=bI.TARGET_CHECK;

if(bD){var bM=false;

if(bN&&((bD&bG.TARGET_DOMNODE)!=0)){bM=true;
}else if(bF&&((bD&bG.TARGET_WINDOW)!=0)){bM=true;
}else if(bO&&((bD&bG.TARGET_OBJECT)!=0)){bM=true;
}else if(bC&&((bD&bG.TARGET_DOCUMENT)!=0)){bM=true;
}
if(!bM){continue;
}}bJ=this.getHandler(bK[i]);

if(bI.IGNORE_CAN_HANDLE||bJ.canHandleEvent(bA,bB)){bH[bL]=bJ;
return bJ;
}}return null;
},__bN:function(bP,bQ,bR){var bS=this.findHandler(bP,bQ);

if(bS){bS.registerEvent(bP,bQ,bR);
return;
}{};
},removeListener:function(bT,bU,bV,self,bW){var cb;
{};
var cc=bT.$$hash||qx.core.ObjectRegistry.toHashCode(bT);
var cd=this.__bH[cc];

if(!cd){return false;
}var bX=bU+(bW?q:r);
var bY=cd[bX];

if(!bY){return false;
}var ca;

for(var i=0,l=bY.length;i<l;i++){ca=bY[i];

if(ca.handler===bV&&ca.context===self){qx.lang.Array.removeAt(bY,i);

if(bY.length==0){this.__bO(bT,bU,bW);
}return true;
}}return false;
},removeListenerById:function(ce,cf){var cl;
{};
var cj=cf.split(p);
var co=cj[0];
var cg=cj[1].charCodeAt(0)==99;
var cn=cj[2];
var cm=ce.$$hash||qx.core.ObjectRegistry.toHashCode(ce);
var cp=this.__bH[cm];

if(!cp){return false;
}var ck=co+(cg?q:r);
var ci=cp[ck];

if(!ci){return false;
}var ch;

for(var i=0,l=ci.length;i<l;i++){ch=ci[i];

if(ch.unique===cn){qx.lang.Array.removeAt(ci,i);

if(ci.length==0){this.__bO(ce,co,cg);
}return true;
}}return false;
},removeAllListeners:function(cq){var cu=cq.$$hash||qx.core.ObjectRegistry.toHashCode(cq);
var cw=this.__bH[cu];

if(!cw){return false;
}var cs,cv,cr;

for(var ct in cw){if(cw[ct].length>0){cs=ct.split(p);
cv=cs[0];
cr=cs[1]===a;
this.__bO(cq,cv,cr);
}}delete this.__bH[cu];
return true;
},deleteAllListeners:function(cx){delete this.__bH[cx];
},__bO:function(cy,cz,cA){var cB=this.findHandler(cy,cz);

if(cB){cB.unregisterEvent(cy,cz,cA);
return;
}{};
},dispatchEvent:function(cC,event){var cH;
{};
var cI=event.getType();

if(!event.getBubbles()&&!this.hasListener(cC,cI)){qx.event.Pool.getInstance().poolObject(event);
return true;
}
if(!event.getTarget()){event.setTarget(cC);
}var cG=this.__bG.getDispatchers();
var cF;
var cE=false;

for(var i=0,l=cG.length;i<l;i++){cF=this.getDispatcher(cG[i]);
if(cF.canDispatchEvent(cC,event,cI)){cF.dispatchEvent(cC,event,cI);
cE=true;
break;
}}
if(!cE){{};
return true;
}var cD=event.getDefaultPrevented();
qx.event.Pool.getInstance().poolObject(event);
return !cD;
},dispose:function(){this.__bG.removeManager(this);
qx.util.DisposeUtil.disposeMap(this,c);
qx.util.DisposeUtil.disposeMap(this,j);
this.__bH=this.__bE=this.__bM=null;
this.__bG=this.__bK=null;
}}});
})();
(function(){var d="qx.dom.Node",c="qx.client",b="";
qx.Class.define(d,{statics:{ELEMENT:1,ATTRIBUTE:2,TEXT:3,CDATA_SECTION:4,ENTITY_REFERENCE:5,ENTITY:6,PROCESSING_INSTRUCTION:7,COMMENT:8,DOCUMENT:9,DOCUMENT_TYPE:10,DOCUMENT_FRAGMENT:11,NOTATION:12,getDocument:function(e){return e.nodeType===
this.DOCUMENT?e:
e.ownerDocument||e.document;
},getWindow:qx.core.Variant.select(c,{"mshtml":function(f){if(f.nodeType==null){return f;
}if(f.nodeType!==this.DOCUMENT){f=f.ownerDocument;
}return f.parentWindow;
},"default":function(g){if(g.nodeType==null){return g;
}if(g.nodeType!==this.DOCUMENT){g=g.ownerDocument;
}return g.defaultView;
}}),getDocumentElement:function(h){return this.getDocument(h).documentElement;
},getBodyElement:function(j){return this.getDocument(j).body;
},isNode:function(k){return !!(k&&k.nodeType!=null);
},isElement:function(l){return !!(l&&l.nodeType===this.ELEMENT);
},isDocument:function(m){return !!(m&&m.nodeType===this.DOCUMENT);
},isText:function(n){return !!(n&&n.nodeType===this.TEXT);
},isWindow:function(o){return !!(o&&o.history&&o.location&&o.document);
},isNodeName:function(p,q){if(!q||!p||!p.nodeName){return false;
}return q.toLowerCase()==qx.dom.Node.getName(p);
},getName:function(r){if(!r||!r.nodeName){return null;
}return r.nodeName.toLowerCase();
},getText:function(s){if(!s||!s.nodeType){return null;
}
switch(s.nodeType){case 1:var i,a=[],t=s.childNodes,length=t.length;

for(i=0;i<length;i++){a[i]=this.getText(t[i]);
}return a.join(b);
case 2:return s.nodeValue;
break;
case 3:return s.nodeValue;
break;
}return null;
},isBlockNode:function(u){if(!qx.dom.Node.isElement(u)){return false;
}u=qx.dom.Node.getName(u);
return /^(body|form|textarea|fieldset|ul|ol|dl|dt|dd|li|div|hr|p|h[1-6]|quote|pre|table|thead|tbody|tfoot|tr|td|th|iframe|address|blockquote)$/.test(u);
}}});
})();
(function(){var c="qx.event.Registration";
qx.Class.define(c,{statics:{__bP:{},getManager:function(d){if(d==null){{};
d=window;
}else if(d.nodeType){d=qx.dom.Node.getWindow(d);
}else if(!qx.dom.Node.isWindow(d)){d=window;
}var f=d.$$hash||qx.core.ObjectRegistry.toHashCode(d);
var e=this.__bP[f];

if(!e){e=new qx.event.Manager(d,this);
this.__bP[f]=e;
}return e;
},removeManager:function(g){var h=g.getWindowId();
delete this.__bP[h];
},addListener:function(i,j,k,self,l){return this.getManager(i).addListener(i,j,k,self,l);
},removeListener:function(m,n,o,self,p){return this.getManager(m).removeListener(m,n,o,self,p);
},removeListenerById:function(q,r){return this.getManager(q).removeListenerById(q,r);
},removeAllListeners:function(s){return this.getManager(s).removeAllListeners(s);
},deleteAllListeners:function(t){var u=t.$$hash;

if(u){this.getManager(t).deleteAllListeners(u);
}},hasListener:function(v,w,x){return this.getManager(v).hasListener(v,w,x);
},serializeListeners:function(y){return this.getManager(y).serializeListeners(y);
},createEvent:function(z,A,B){{};
if(A==null){A=qx.event.type.Event;
}var C=qx.event.Pool.getInstance().getObject(A);
B?C.init.apply(C,B):C.init();
if(z){C.setType(z);
}return C;
},dispatchEvent:function(D,event){return this.getManager(D).dispatchEvent(D,event);
},fireEvent:function(E,F,G,H){var I;
{};
var J=this.createEvent(F,G||null,H);
return this.getManager(E).dispatchEvent(E,J);
},fireNonBubblingEvent:function(K,L,M,N){{};
var O=this.getManager(K);

if(!O.hasListener(K,L,false)){return true;
}var P=this.createEvent(L,M||null,N);
return O.dispatchEvent(K,P);
},PRIORITY_FIRST:-32000,PRIORITY_NORMAL:0,PRIORITY_LAST:32000,__bQ:[],addHandler:function(Q){{};
this.__bQ.push(Q);
this.__bQ.sort(function(a,b){return a.PRIORITY-b.PRIORITY;
});
},getHandlers:function(){return this.__bQ;
},__bR:[],addDispatcher:function(R,S){{};
this.__bR.push(R);
this.__bR.sort(function(a,b){return a.PRIORITY-b.PRIORITY;
});
},getDispatchers:function(){return this.__bR;
}}});
})();
(function(){var f="qx.lang.Type",e="Error",d="RegExp",c="Date",b="Number",a="Boolean";
qx.Class.define(f,{statics:{getClass:qx.Bootstrap.getClass,isString:qx.Bootstrap.isString,isArray:qx.Bootstrap.isArray,isObject:qx.Bootstrap.isObject,isFunction:qx.Bootstrap.isFunction,isRegExp:function(g){return this.getClass(g)==d;
},isNumber:function(h){return (h!==null&&(this.getClass(h)==b||h instanceof Number));
},isBoolean:function(i){return (i!==null&&(this.getClass(i)==a||i instanceof Boolean));
},isDate:function(j){return (j!==null&&(this.getClass(j)==c||j instanceof Date));
},isError:function(k){return (k!==null&&(this.getClass(k)==e||k instanceof Error));
}}});
})();
(function(){var c="",b=": ",a="qx.type.BaseError";
qx.Class.define(a,{extend:Error,construct:function(d,e){Error.call(this,e);
this.__bS=d||c;
this.message=e||qx.type.BaseError.DEFAULTMESSAGE;
},statics:{DEFAULTMESSAGE:"error"},members:{__bS:null,message:null,getComment:function(){return this.__bS;
},toString:function(){return this.__bS+(this.message?b+this.message:c);
}}});
})();
(function(){var a="qx.core.AssertionError";
qx.Class.define(a,{extend:qx.type.BaseError,construct:function(b,c){qx.type.BaseError.call(this,b,c);
this.__bT=qx.dev.StackTrace.getStackTrace();
},members:{__bT:null,getStackTrace:function(){return this.__bT;
}}});
})();
(function(){var p="",o="!",n="'!",m="'",k="Expected '",j="' (rgb(",h=",",g=")), but found value '",f="Event (",d="Expected value to be the CSS color '",bw="' but found ",bv="The value '",bu=" != ",bt="qx.core.Object",bs="Expected value to be an array but found ",br=") was fired.",bq="Expected value to be an integer >= 0 but found ",bp="' to be not equal with '",bo="' to '",bn="qx.ui.core.Widget",w="Called assertTrue with '",x="Expected value to be a map but found ",u="The function did not raise an exception!",v="Expected value to be undefined but found ",s="Expected value to be a DOM element but found  '",t="Expected value to be a regular expression but found ",q="' to implement the interface '",r="Expected value to be null but found ",E="Invalid argument 'type'",F="Called assert with 'false'",R="Assertion error! ",N="null",ba="' but found '",U="' must must be a key of the map '",bj="The String '",bf="Expected value to be a string but found ",J="Expected value not to be undefined but found undefined!",bm="qx.util.ColorUtil",bl=": ",bk="The raised exception does not have the expected type! ",I=") not fired.",L="qx.core.Assert",M="Expected value to be typeof object but found ",P="' (identical) but found '",S="' must have any of the values defined in the array '",V="Expected value to be a number but found ",bc="Called assertFalse with '",bh="]",y="Expected value to be a qooxdoo object but found ",z="' arguments.",K="Expected value '%1' to be in the range '%2'..'%3'!",Y="Array[",X="' does not match the regular expression '",W="' to be not identical with '",be="' arguments but found '",bd="', which cannot be converted to a CSS color!",T="Expected object '",bb="qx.core.AssertionError",a="Expected value to be a boolean but found ",bg="Expected value not to be null but found null!",A="))!",B="Expected value to be a qooxdoo widget but found ",O="Expected value to be typeof '",b="Expected value to be typeof function but found ",c="Expected value to be an integer but found ",H="Called fail().",C="The parameter 're' must be a string or a regular expression.",D="Expected value to be a number >= 0 but found ",G="Expected value to be instanceof '",Q="Wrong number of arguments given. Expected '",bi="object";
qx.Class.define(L,{statics:{__bU:true,__bV:function(bx,by){var bC=p;

for(var i=1,l=arguments.length;i<l;i++){bC=bC+this.__bW(arguments[i]);
}var bB=p;

if(bC){bB=bx+bl+bC;
}else{bB=bx;
}var bA=R+bB;

if(this.__bU){qx.Bootstrap.error(bA);
}
if(qx.Class.isDefined(bb)){var bz=new qx.core.AssertionError(bx,bC);

if(this.__bU){qx.Bootstrap.error("Stack trace: \n"+bz.getStackTrace());
}throw bz;
}else{throw new Error(bA);
}},__bW:function(bD){var bE;

if(bD===null){bE=N;
}else if(qx.lang.Type.isArray(bD)&&bD.length>10){bE=Y+bD.length+bh;
}else if((bD instanceof Object)&&(bD.toString==null)){bE=qx.lang.Json.stringify(bD,null,2);
}else{try{bE=bD.toString();
}catch(e){bE=p;
}}return bE;
},assert:function(bF,bG){bF==true||this.__bV(bG||p,F);
},fail:function(bH,bI){var bJ=bI?p:H;
this.__bV(bH||p,bJ);
},assertTrue:function(bK,bL){(bK===true)||this.__bV(bL||p,w,bK,m);
},assertFalse:function(bM,bN){(bM===false)||this.__bV(bN||p,bc,bM,m);
},assertEquals:function(bO,bP,bQ){bO==bP||this.__bV(bQ||p,k,bO,ba,bP,n);
},assertNotEquals:function(bR,bS,bT){bR!=bS||this.__bV(bT||p,k,bR,bp,bS,n);
},assertIdentical:function(bU,bV,bW){bU===bV||this.__bV(bW||p,k,bU,P,bV,n);
},assertNotIdentical:function(bX,bY,ca){bX!==bY||this.__bV(ca||p,k,bX,W,bY,n);
},assertNotUndefined:function(cb,cc){cb!==undefined||this.__bV(cc||p,J);
},assertUndefined:function(cd,ce){cd===undefined||this.__bV(ce||p,v,cd,o);
},assertNotNull:function(cf,cg){cf!==null||this.__bV(cg||p,bg);
},assertNull:function(ch,ci){ch===null||this.__bV(ci||p,r,ch,o);
},assertJsonEquals:function(cj,ck,cl){this.assertEquals(qx.lang.Json.stringify(cj),qx.lang.Json.stringify(ck),cl);
},assertMatch:function(cm,cn,co){this.assertString(cm);
this.assert(qx.lang.Type.isRegExp(cn)||qx.lang.Type.isString(cn),C);
cm.search(cn)>=0||this.__bV(co||p,bj,cm,X,cn.toString(),n);
},assertArgumentsCount:function(cp,cq,cr,cs){var ct=cp.length;
(ct>=cq&&ct<=cr)||this.__bV(cs||p,Q,cq,bo,cr,be,arguments.length,z);
},assertEventFired:function(cu,event,cv,cw,cx){var cz=false;
var cy=function(e){if(cw){cw.call(cu,e);
}cz=true;
};
var cA;

try{cA=cu.addListener(event,cy,cu);
cv.call();
}catch(cB){throw cB;
}finally{try{cu.removeListenerById(cA);
}catch(cC){}}cz===true||this.__bV(cx||p,f,event,I);
},assertEventNotFired:function(cD,event,cE,cF){var cH=false;
var cG=function(e){cH=true;
};
var cI=cD.addListener(event,cG,cD);
cE.call();
cH===false||this.__bV(cF||p,f,event,br);
cD.removeListenerById(cI);
},assertException:function(cJ,cK,cL,cM){var cK=cK||Error;
var cN;

try{this.__bU=false;
cJ();
}catch(cO){cN=cO;
}finally{this.__bU=true;
}
if(cN==null){this.__bV(cM||p,u);
}cN instanceof cK||this.__bV(cM||p,bk,cK,bu,cN);

if(cL){this.assertMatch(cN.toString(),cL,cM);
}},assertInArray:function(cP,cQ,cR){cQ.indexOf(cP)!==-1||this.__bV(cR||p,bv,cP,S,cQ,m);
},assertArrayEquals:function(cS,cT,cU){this.assertArray(cS,cU);
this.assertArray(cT,cU);
this.assertEquals(cS.length,cT.length,cU);

for(var i=0;i<cS.length;i++){this.assertIdentical(cS[i],cT[i],cU);
}},assertKeyInMap:function(cV,cW,cX){cW[cV]!==undefined||this.__bV(cX||p,bv,cV,U,cW,m);
},assertFunction:function(cY,da){qx.lang.Type.isFunction(cY)||this.__bV(da||p,b,cY,o);
},assertString:function(db,dc){qx.lang.Type.isString(db)||this.__bV(dc||p,bf,db,o);
},assertBoolean:function(dd,de){qx.lang.Type.isBoolean(dd)||this.__bV(de||p,a,dd,o);
},assertNumber:function(df,dg){(qx.lang.Type.isNumber(df)&&isFinite(df))||this.__bV(dg||p,V,df,o);
},assertPositiveNumber:function(dh,di){(qx.lang.Type.isNumber(dh)&&isFinite(dh)&&dh>=0)||this.__bV(di||p,D,dh,o);
},assertInteger:function(dj,dk){(qx.lang.Type.isNumber(dj)&&isFinite(dj)&&dj%1===0)||this.__bV(dk||p,c,dj,o);
},assertPositiveInteger:function(dl,dm){var dn=(qx.lang.Type.isNumber(dl)&&isFinite(dl)&&dl%1===0&&dl>=0);
dn||this.__bV(dm||p,bq,dl,o);
},assertInRange:function(dp,dq,dr,ds){(dp>=dq&&dp<=dr)||this.__bV(ds||p,qx.lang.String.format(K,[dp,dq,dr]));
},assertObject:function(dt,du){var dv=dt!==null&&(qx.lang.Type.isObject(dt)||typeof dt===bi);
dv||this.__bV(du||p,M,(dt),o);
},assertArray:function(dw,dx){qx.lang.Type.isArray(dw)||this.__bV(dx||p,bs,dw,o);
},assertMap:function(dy,dz){qx.lang.Type.isObject(dy)||this.__bV(dz||p,x,dy,o);
},assertRegExp:function(dA,dB){qx.lang.Type.isRegExp(dA)||this.__bV(dB||p,t,dA,o);
},assertType:function(dC,dD,dE){this.assertString(dD,E);
typeof (dC)===dD||this.__bV(dE||p,O,dD,bw,dC,o);
},assertInstance:function(dF,dG,dH){var dI=dG.classname||dG+p;
dF instanceof dG||this.__bV(dH||p,G,dI,bw,dF,o);
},assertInterface:function(dJ,dK,dL){qx.Class.implementsInterface(dJ,dK)||this.__bV(dL||p,T,dJ,q,dK,n);
},assertCssColor:function(dM,dN,dO){var dP=qx.Class.getByName(bm);

if(!dP){throw new Error("qx.util.ColorUtil not available! Your code must have a dependency on 'qx.util.ColorUtil'");
}var dR=dP.stringToRgb(dM);

try{var dQ=dP.stringToRgb(dN);
}catch(dT){this.__bV(dO||p,d,dM,j,dR.join(h),g,dN,bd);
}var dS=dR[0]==dQ[0]&&dR[1]==dQ[1]&&dR[2]==dQ[2];
dS||this.__bV(dO||p,d,dR,j,dR.join(h),g,dN,j,dQ.join(h),A);
},assertElement:function(dU,dV){!!(dU&&dU.nodeType===1)||this.__bV(dV||p,s,dU,n);
},assertQxObject:function(dW,dX){this.__bX(dW,bt)||this.__bV(dX||p,y,dW,o);
},assertQxWidget:function(dY,ea){this.__bX(dY,bn)||this.__bV(ea||p,B,dY,o);
},__bX:function(eb,ec){if(!eb){return false;
}var ed=eb.constructor;

while(ed){if(ed.classname===ec){return true;
}ed=ed.superclass;
}return false;
}}});
})();
(function(){var p='',o='"',m=':',l=']',h='null',g=': ',f='object',e='function',d=',',b='\n',ba='\\u',Y=',\n',X='0000',W='string',V="Cannot stringify a recursive object.",U='0',T='-',S='}',R='String',Q='Boolean',x='\\\\',y='\\f',u='\\t',w='{\n',s='[]',t="qx.lang.JsonImpl",q='Z',r='\\n',z='Object',A='{}',H='@',F='.',K='(',J='Array',M='T',L='\\r',C='{',P='JSON.parse',O=' ',N='[',B='Number',D=')',E='[\n',G='\\"',I='\\b';
qx.Class.define(t,{extend:Object,construct:function(){this.stringify=qx.lang.Function.bind(this.stringify,this);
this.parse=qx.lang.Function.bind(this.parse,this);
},members:{__bY:null,__ca:null,__cb:null,__cc:null,stringify:function(bb,bc,bd){this.__bY=p;
this.__ca=p;
this.__cc=[];

if(qx.lang.Type.isNumber(bd)){var bd=Math.min(10,Math.floor(bd));

for(var i=0;i<bd;i+=1){this.__ca+=O;
}}else if(qx.lang.Type.isString(bd)){if(bd.length>10){bd=bd.slice(0,10);
}this.__ca=bd;
}if(bc&&(qx.lang.Type.isFunction(bc)||qx.lang.Type.isArray(bc))){this.__cb=bc;
}else{this.__cb=null;
}return this.__cd(p,{'':bb});
},__cd:function(be,bf){var bi=this.__bY,bg,bj=bf[be];
if(bj&&qx.lang.Type.isFunction(bj.toJSON)){bj=bj.toJSON(be);
}else if(qx.lang.Type.isDate(bj)){bj=this.dateToJSON(bj);
}if(typeof this.__cb===e){bj=this.__cb.call(bf,be,bj);
}
if(bj===null){return h;
}
if(bj===undefined){return undefined;
}switch(qx.lang.Type.getClass(bj)){case R:return this.__ce(bj);
case B:return isFinite(bj)?String(bj):h;
case Q:return String(bj);
case J:this.__bY+=this.__ca;
bg=[];

if(this.__cc.indexOf(bj)!==-1){throw new TypeError(V);
}this.__cc.push(bj);
var length=bj.length;

for(var i=0;i<length;i+=1){bg[i]=this.__cd(i,bj)||h;
}this.__cc.pop();
if(bg.length===0){var bh=s;
}else if(this.__bY){bh=E+this.__bY+bg.join(Y+this.__bY)+b+bi+l;
}else{bh=N+bg.join(d)+l;
}this.__bY=bi;
return bh;
case z:this.__bY+=this.__ca;
bg=[];

if(this.__cc.indexOf(bj)!==-1){throw new TypeError(V);
}this.__cc.push(bj);
if(this.__cb&&typeof this.__cb===f){var length=this.__cb.length;

for(var i=0;i<length;i+=1){var k=this.__cb[i];

if(typeof k===W){var v=this.__cd(k,bj);

if(v){bg.push(this.__ce(k)+(this.__bY?g:m)+v);
}}}}else{for(var k in bj){if(Object.hasOwnProperty.call(bj,k)){var v=this.__cd(k,bj);

if(v){bg.push(this.__ce(k)+(this.__bY?g:m)+v);
}}}}this.__cc.pop();
if(bg.length===0){var bh=A;
}else if(this.__bY){bh=w+this.__bY+bg.join(Y+this.__bY)+b+bi+S;
}else{bh=C+bg.join(d)+S;
}this.__bY=bi;
return bh;
}},dateToJSON:function(bk){var bl=function(n){return n<10?U+n:n;
};
var bm=function(n){var bn=bl(n);
return n<100?U+bn:bn;
};
return isFinite(bk.valueOf())?bk.getUTCFullYear()+T+bl(bk.getUTCMonth()+1)+T+bl(bk.getUTCDate())+M+bl(bk.getUTCHours())+m+bl(bk.getUTCMinutes())+m+bl(bk.getUTCSeconds())+F+bm(bk.getUTCMilliseconds())+q:null;
},__ce:function(bo){var bp={'\b':I,'\t':u,'\n':r,'\f':y,'\r':L,'"':G,'\\':x};
var bq=/[\\\"\x00-\x1f\x7f-\x9f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g;
bq.lastIndex=0;

if(bq.test(bo)){return o+
bo.replace(bq,function(a){var c=bp[a];
return typeof c===W?c:ba+(X+a.charCodeAt(0).toString(16)).slice(-4);
})+o;
}else{return o+bo+o;
}},parse:function(br,bs){var bt=/[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g;
bt.lastIndex=0;
if(bt.test(br)){br=br.replace(bt,function(a){return ba+(X+a.charCodeAt(0).toString(16)).slice(-4);
});
}if(/^[\],:{}\s]*$/.test(br.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g,H).replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,l).replace(/(?:^|:|,)(?:\s*\[)+/g,p))){var j=eval(K+br+D);
return typeof bs===e?this.__cf({'':j},p,bs):j;
}throw new SyntaxError(P);
},__cf:function(bu,bv,bw){var bx=bu[bv];

if(bx&&typeof bx===f){for(var k in bx){if(Object.hasOwnProperty.call(bx,k)){var v=this.__cf(bx,k,bw);

if(v!==undefined){bx[k]=v;
}else{delete bx[k];
}}}}return bw.call(bu,bv,bx);
}}});
})();
(function(){var c="qx.event.type.Data",b="qx.event.type.Event",a="qx.data.IListData";
qx.Interface.define(a,{events:{"change":c,"changeLength":b},members:{getItem:function(d){},setItem:function(e,f){},splice:function(g,h,i){},contains:function(j){},getLength:function(){},toArray:function(){}}});
})();
(function(){var b="GlobalError: ",a="qx.core.GlobalError";
qx.Bootstrap.define(a,{extend:Error,construct:function(c,d){{};
this.__cg=b+(c&&c.message?c.message:c);
Error.call(this,this.__cg);
this.__ch=d;
this.__ci=c;
},members:{__ci:null,__ch:null,__cg:null,toString:function(){return this.__cg;
},getArguments:function(){return this.__ch;
},getSourceException:function(){return this.__ci;
}},destruct:function(){this.__ci=null;
this.__ch=null;
this.__cg=null;
}});
})();
(function(){var c="qx.globalErrorHandling",b="on",a="qx.event.GlobalError";
qx.Bootstrap.define(a,{statics:{setErrorHandler:function(d,e){this.__cj=d||null;
this.__ck=e||window;

if(qx.core.Setting.get(c)===b){if(d&&window.onerror){var f=qx.Bootstrap.bind(this.__cm,this);

if(this.__cl==null){this.__cl=window.onerror;
}var self=this;
window.onerror=function(g,h,i){self.__cl(g,h,i);
f(g,h,i);
};
}
if(d&&!window.onerror){window.onerror=qx.Bootstrap.bind(this.__cm,this);
}if(this.__cj==null){if(this.__cl!=null){window.onerror=this.__cl;
this.__cl=null;
}else{window.onerror=null;
}}}},__cm:function(j,k,l){if(this.__cj){this.handleError(new qx.core.WindowError(j,k,l));
return true;
}},observeMethod:function(m){if(qx.core.Setting.get(c)===b){var self=this;
return function(){if(!self.__cj){return m.apply(this,arguments);
}
try{return m.apply(this,arguments);
}catch(n){self.handleError(new qx.core.GlobalError(n,arguments));
}};
}else{return m;
}},handleError:function(o){if(this.__cj){this.__cj.call(this.__ck,o);
}}},defer:function(p){qx.core.Setting.define(c,b);
p.setErrorHandler(null,null);
}});
})();
(function(){var a="qx.data.MBinding";
qx.Mixin.define(a,{members:{bind:function(b,c,d,e){return qx.data.SingleValueBinding.bind(this,b,c,d,e);
},removeBinding:function(f){qx.data.SingleValueBinding.removeBindingFromObject(this,f);
},removeAllBindings:function(){qx.data.SingleValueBinding.removeAllBindingsForObject(this);
},getBindings:function(){return qx.data.SingleValueBinding.getAllBindingsForObject(this);
}}});
})();
(function(){var q="set",p="get",o="reset",n="MSIE 6.0",m="info",k="qx.core.Object",j="error",h="warn",g="]",f="debug",b="[",d="$$user_",c="rv:1.8.1",a="Object";
qx.Class.define(k,{extend:Object,include:[qx.data.MBinding],construct:function(){qx.core.ObjectRegistry.register(this);
},statics:{$$type:a},members:{toHashCode:function(){return this.$$hash;
},toString:function(){return this.classname+b+this.$$hash+g;
},base:function(r,s){{};

if(arguments.length===1){return r.callee.base.call(this);
}else{return r.callee.base.apply(this,Array.prototype.slice.call(arguments,1));
}},self:function(t){return t.callee.self;
},clone:function(){var v=this.constructor;
var u=new v;
var x=qx.Class.getProperties(v);
var w=qx.core.Property.$$store.user;
var y=qx.core.Property.$$method.set;
var name;
for(var i=0,l=x.length;i<l;i++){name=x[i];

if(this.hasOwnProperty(w[name])){u[y[name]](this[w[name]]);
}}return u;
},set:function(z,A){var C=qx.core.Property.$$method.set;

if(qx.Bootstrap.isString(z)){if(!this[C[z]]){if(this[q+qx.Bootstrap.firstUp(z)]!=undefined){this[q+qx.Bootstrap.firstUp(z)](A);
return this;
}{};
}return this[C[z]](A);
}else{for(var B in z){if(!this[C[B]]){if(this[q+qx.Bootstrap.firstUp(B)]!=undefined){this[q+qx.Bootstrap.firstUp(B)](z[B]);
continue;
}{};
}this[C[B]](z[B]);
}return this;
}},get:function(D){var E=qx.core.Property.$$method.get;

if(!this[E[D]]){if(this[p+qx.Bootstrap.firstUp(D)]!=undefined){return this[p+qx.Bootstrap.firstUp(D)]();
}{};
}return this[E[D]]();
},reset:function(F){var G=qx.core.Property.$$method.reset;

if(!this[G[F]]){if(this[o+qx.Bootstrap.firstUp(F)]!=undefined){this[o+qx.Bootstrap.firstUp(F)]();
return;
}{};
}this[G[F]]();
},__cn:qx.event.Registration,addListener:function(H,I,self,J){if(!this.$$disposed){return this.__cn.addListener(this,H,I,self,J);
}return null;
},addListenerOnce:function(K,L,self,M){var N=function(e){this.removeListener(K,N,this,M);
L.call(self||this,e);
};
return this.addListener(K,N,this,M);
},removeListener:function(O,P,self,Q){if(!this.$$disposed){return this.__cn.removeListener(this,O,P,self,Q);
}return false;
},removeListenerById:function(R){if(!this.$$disposed){return this.__cn.removeListenerById(this,R);
}return false;
},hasListener:function(S,T){return this.__cn.hasListener(this,S,T);
},dispatchEvent:function(U){if(!this.$$disposed){return this.__cn.dispatchEvent(this,U);
}return true;
},fireEvent:function(V,W,X){if(!this.$$disposed){return this.__cn.fireEvent(this,V,W,X);
}return true;
},fireNonBubblingEvent:function(Y,ba,bb){if(!this.$$disposed){return this.__cn.fireNonBubblingEvent(this,Y,ba,bb);
}return true;
},fireDataEvent:function(bc,bd,be,bf){if(!this.$$disposed){if(be===undefined){be=null;
}return this.__cn.fireNonBubblingEvent(this,bc,qx.event.type.Data,[bd,be,!!bf]);
}return true;
},__co:null,setUserData:function(bg,bh){if(!this.__co){this.__co={};
}this.__co[bg]=bh;
},getUserData:function(bi){if(!this.__co){return null;
}var bj=this.__co[bi];
return bj===undefined?null:bj;
},__cp:qx.log.Logger,debug:function(bk){this.__cq(f,arguments);
},info:function(bl){this.__cq(m,arguments);
},warn:function(bm){this.__cq(h,arguments);
},error:function(bn){this.__cq(j,arguments);
},trace:function(){this.__cp.trace(this);
},__cq:function(bo,bp){var bq=qx.lang.Array.fromArguments(bp);
bq.unshift(this);
this.__cp[bo].apply(this.__cp,bq);
},isDisposed:function(){return this.$$disposed||false;
},dispose:function(){var bv,bt,bs,bw;
if(this.$$disposed){return;
}this.$$disposed=true;
this.$$instance=null;
this.$$allowconstruct=null;
{};
var bu=this.constructor;
var br;

while(bu.superclass){if(bu.$$destructor){bu.$$destructor.call(this);
}if(bu.$$includes){br=bu.$$flatIncludes;

for(var i=0,l=br.length;i<l;i++){if(br[i].$$destructor){br[i].$$destructor.call(this);
}}}bu=bu.superclass;
}if(this.__cr){this.__cr();
}{};
},__cr:null,__cs:function(){var bx=qx.Class.getProperties(this.constructor);

for(var i=0,l=bx.length;i<l;i++){delete this[d+bx[i]];
}},_disposeObjects:function(by){qx.util.DisposeUtil.disposeObjects(this,arguments);
},_disposeSingletonObjects:function(bz){qx.util.DisposeUtil.disposeObjects(this,arguments,true);
},_disposeArray:function(bA){qx.util.DisposeUtil.disposeArray(this,bA);
},_disposeMap:function(bB){qx.util.DisposeUtil.disposeMap(this,bB);
}},settings:{"qx.disposerDebugLevel":0},defer:function(bC,bD){{};
var bF=navigator.userAgent.indexOf(n)!=-1;
var bE=navigator.userAgent.indexOf(c)!=-1;
if(bF||bE){bD.__cr=bD.__cs;
}},destruct:function(){if(!qx.core.ObjectRegistry.inShutDown){qx.event.Registration.removeAllListeners(this);
}else{qx.event.Registration.deleteAllListeners(this);
}qx.core.ObjectRegistry.unregister(this);
this.__co=null;
var bI=this.constructor;
var bM;
var bN=qx.core.Property.$$store;
var bK=bN.user;
var bL=bN.theme;
var bG=bN.inherit;
var bJ=bN.useinit;
var bH=bN.init;

while(bI){bM=bI.$$properties;

if(bM){for(var name in bM){if(bM[name].dereference){this[bK[name]]=this[bL[name]]=this[bG[name]]=this[bJ[name]]=this[bH[name]]=undefined;
}}}bI=bI.superclass;
}}});
})();
(function(){var a="qx.lang.Json";
qx.Class.define(a,{statics:{JSON:(qx.lang.Type.getClass(window.JSON)=="JSON"&&JSON.parse('{"x":1}').x===1)?window.JSON:new qx.lang.JsonImpl(),stringify:null,parse:null},defer:function(b){b.stringify=b.JSON.stringify;
b.parse=b.JSON.parse;
}});
})();
(function(){var a="qx.event.IEventHandler";
qx.Interface.define(a,{statics:{TARGET_DOMNODE:1,TARGET_WINDOW:2,TARGET_OBJECT:4,TARGET_DOCUMENT:8},members:{canHandleEvent:function(b,c){},registerEvent:function(d,e,f){},unregisterEvent:function(g,h,i){}}});
})();
(function(){var m="ready",l="qx.client",k="mshtml",j="load",i="unload",h="qx.event.handler.Application",g="complete",f="qx.application",d="gecko|opera|webkit",c="left",a="DOMContentLoaded",b="shutdown";
qx.Class.define(h,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(n){qx.core.Object.call(this);
this._window=n.getWindow();
this.__ct=false;
this.__cu=false;
this._initObserver();
qx.event.handler.Application.$$instance=this;
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{ready:1,shutdown:1},TARGET_CHECK:qx.event.IEventHandler.TARGET_WINDOW,IGNORE_CAN_HANDLE:true,onScriptLoaded:function(){var o=qx.event.handler.Application.$$instance;

if(o){o.__cx();
}}},members:{canHandleEvent:function(p,q){},registerEvent:function(r,s,t){},unregisterEvent:function(u,v,w){},__cv:null,__ct:null,__cu:null,__cw:null,__cx:function(){if(!this.__cv&&this.__ct&&qx.$$loader.scriptLoaded){try{var x=qx.core.Setting.get(f);

if(!qx.Class.getByName(x)){return;
}}catch(e){}if(qx.core.Variant.isSet(l,k)){if(qx.event.Registration.hasListener(this._window,m)){this.__cv=true;
qx.event.Registration.fireEvent(this._window,m);
}}else{this.__cv=true;
qx.event.Registration.fireEvent(this._window,m);
}}},isApplicationReady:function(){return this.__cv;
},_initObserver:function(){if(qx.$$domReady||document.readyState==g||document.readyState==m){this.__ct=true;
this.__cx();
}else{this._onNativeLoadWrapped=qx.lang.Function.bind(this._onNativeLoad,this);

if(qx.core.Variant.isSet(l,d)){qx.bom.Event.addNativeListener(this._window,a,this._onNativeLoadWrapped);
}else if(qx.core.Variant.isSet(l,k)){var self=this;
var y=function(){try{document.documentElement.doScroll(c);

if(document.body){self._onNativeLoadWrapped();
}}catch(z){window.setTimeout(y,100);
}};
y();
}qx.bom.Event.addNativeListener(this._window,j,this._onNativeLoadWrapped);
}this._onNativeUnloadWrapped=qx.lang.Function.bind(this._onNativeUnload,this);
qx.bom.Event.addNativeListener(this._window,i,this._onNativeUnloadWrapped);
},_stopObserver:function(){if(this._onNativeLoadWrapped){qx.bom.Event.removeNativeListener(this._window,j,this._onNativeLoadWrapped);
}qx.bom.Event.removeNativeListener(this._window,i,this._onNativeUnloadWrapped);
this._onNativeLoadWrapped=null;
this._onNativeUnloadWrapped=null;
},_onNativeLoad:qx.event.GlobalError.observeMethod(function(){this.__ct=true;
this.__cx();
}),_onNativeUnload:qx.event.GlobalError.observeMethod(function(){if(!this.__cw){this.__cw=true;

try{qx.event.Registration.fireEvent(this._window,b);
}catch(e){throw e;
}finally{qx.core.ObjectRegistry.shutdown();
}}})},destruct:function(){this._stopObserver();
this._window=null;
},defer:function(A){qx.event.Registration.addHandler(A);
}});
})();
(function(){var a="qx.event.IEventDispatcher";
qx.Interface.define(a,{members:{canDispatchEvent:function(b,event,c){this.assertInstance(event,qx.event.type.Event);
this.assertString(c);
},dispatchEvent:function(d,event,e){this.assertInstance(event,qx.event.type.Event);
this.assertString(e);
}}});
})();
(function(){var a="qx.event.dispatch.Direct";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.event.IEventDispatcher,construct:function(b){this._manager=b;
},statics:{PRIORITY:qx.event.Registration.PRIORITY_LAST},members:{canDispatchEvent:function(c,event,d){return !event.getBubbles();
},dispatchEvent:function(e,event,f){var j,g;
{};
event.setEventPhase(qx.event.type.Event.AT_TARGET);
var k=this._manager.getListeners(e,f,false);

if(k){for(var i=0,l=k.length;i<l;i++){var h=k[i].context||e;
k[i].handler.call(h,event);
}}}},defer:function(m){qx.event.Registration.addDispatcher(m);
}});
})();
(function(){var b="qx.util.ObjectPool",a="Integer";
qx.Class.define(b,{extend:qx.core.Object,construct:function(c){qx.core.Object.call(this);
this.__cH={};

if(c!=null){this.setSize(c);
}},properties:{size:{check:a,init:Infinity}},members:{__cH:null,getObject:function(d){if(this.$$disposed){return new d;
}
if(!d){throw new Error("Class needs to be defined!");
}var e=null;
var f=this.__cH[d.classname];

if(f){e=f.pop();
}
if(e){e.$$pooled=false;
}else{e=new d;
}return e;
},poolObject:function(g){if(!this.__cH){return;
}var h=g.classname;
var j=this.__cH[h];

if(g.$$pooled){throw new Error("Object is already pooled: "+g);
}
if(!j){this.__cH[h]=j=[];
}if(j.length>this.getSize()){if(g.destroy){g.destroy();
}else{g.dispose();
}return;
}g.$$pooled=true;
j.push(g);
}},destruct:function(){var n=this.__cH;
var k,m,i,l;

for(k in n){m=n[k];

for(i=0,l=m.length;i<l;i++){m[i].dispose();
}}delete this.__cH;
}});
})();
(function(){var b="singleton",a="qx.event.Pool";
qx.Class.define(a,{extend:qx.util.ObjectPool,type:b,construct:function(){qx.util.ObjectPool.call(this,30);
}});
})();
(function(){var a="qx.event.type.Event";
qx.Class.define(a,{extend:qx.core.Object,statics:{CAPTURING_PHASE:1,AT_TARGET:2,BUBBLING_PHASE:3},members:{init:function(b,c){{};
this._type=null;
this._target=null;
this._currentTarget=null;
this._relatedTarget=null;
this._originalTarget=null;
this._stopPropagation=false;
this._preventDefault=false;
this._bubbles=!!b;
this._cancelable=!!c;
this._timeStamp=(new Date()).getTime();
this._eventPhase=null;
return this;
},clone:function(d){if(d){var e=d;
}else{var e=qx.event.Pool.getInstance().getObject(this.constructor);
}e._type=this._type;
e._target=this._target;
e._currentTarget=this._currentTarget;
e._relatedTarget=this._relatedTarget;
e._originalTarget=this._originalTarget;
e._stopPropagation=this._stopPropagation;
e._bubbles=this._bubbles;
e._preventDefault=this._preventDefault;
e._cancelable=this._cancelable;
return e;
},stop:function(){if(this._bubbles){this.stopPropagation();
}
if(this._cancelable){this.preventDefault();
}},stopPropagation:function(){{};
this._stopPropagation=true;
},getPropagationStopped:function(){return !!this._stopPropagation;
},preventDefault:function(){{};
this._preventDefault=true;
},getDefaultPrevented:function(){return !!this._preventDefault;
},getType:function(){return this._type;
},setType:function(f){this._type=f;
},getEventPhase:function(){return this._eventPhase;
},setEventPhase:function(g){this._eventPhase=g;
},getTimeStamp:function(){return this._timeStamp;
},getTarget:function(){return this._target;
},setTarget:function(h){this._target=h;
},getCurrentTarget:function(){return this._currentTarget||this._target;
},setCurrentTarget:function(i){this._currentTarget=i;
},getRelatedTarget:function(){return this._relatedTarget;
},setRelatedTarget:function(j){this._relatedTarget=j;
},getOriginalTarget:function(){return this._originalTarget;
},setOriginalTarget:function(k){this._originalTarget=k;
},getBubbles:function(){return this._bubbles;
},setBubbles:function(l){this._bubbles=l;
},isCancelable:function(){return this._cancelable;
},setCancelable:function(m){this._cancelable=m;
}},destruct:function(){this._target=this._currentTarget=this._relatedTarget=this._originalTarget=null;
}});
})();
(function(){var a="qx.event.type.Native";
qx.Class.define(a,{extend:qx.event.type.Event,members:{init:function(b,c,d,e,f){qx.event.type.Event.prototype.init.call(this,e,f);
this._target=c||qx.bom.Event.getTarget(b);
this._relatedTarget=d||qx.bom.Event.getRelatedTarget(b);

if(b.timeStamp){this._timeStamp=b.timeStamp;
}this._native=b;
this._returnValue=null;
return this;
},clone:function(g){var h=qx.event.type.Event.prototype.clone.call(this,g);
var i={};
h._native=this._cloneNativeEvent(this._native,i);
h._returnValue=this._returnValue;
return h;
},_cloneNativeEvent:function(j,k){k.preventDefault=qx.lang.Function.empty;
return k;
},preventDefault:function(){qx.event.type.Event.prototype.preventDefault.call(this);
qx.bom.Event.preventDefault(this._native);
},getNativeEvent:function(){return this._native;
},setReturnValue:function(l){this._returnValue=l;
},getReturnValue:function(){return this._returnValue;
}},destruct:function(){this._native=this._returnValue=null;
}});
})();
(function(){var a="qx.event.handler.Window";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(b){qx.core.Object.call(this);
this._manager=b;
this._window=b.getWindow();
this._initWindowObserver();
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{error:1,load:1,beforeunload:1,unload:1,resize:1,scroll:1,beforeshutdown:1},TARGET_CHECK:qx.event.IEventHandler.TARGET_WINDOW,IGNORE_CAN_HANDLE:true},members:{canHandleEvent:function(c,d){},registerEvent:function(f,g,h){},unregisterEvent:function(i,j,k){},_initWindowObserver:function(){this._onNativeWrapper=qx.lang.Function.listener(this._onNative,this);
var m=qx.event.handler.Window.SUPPORTED_TYPES;

for(var l in m){qx.bom.Event.addNativeListener(this._window,l,this._onNativeWrapper);
}},_stopWindowObserver:function(){var o=qx.event.handler.Window.SUPPORTED_TYPES;

for(var n in o){qx.bom.Event.removeNativeListener(this._window,n,this._onNativeWrapper);
}},_onNative:qx.event.GlobalError.observeMethod(function(e){if(this.isDisposed()){return;
}var q=this._window;

try{var t=q.document;
}catch(e){return ;
}var r=t.documentElement;
var p=qx.bom.Event.getTarget(e);

if(p==null||p===q||p===t||p===r){var event=qx.event.Registration.createEvent(e.type,qx.event.type.Native,[e,q]);
qx.event.Registration.dispatchEvent(q,event);
var s=event.getReturnValue();

if(s!=null){e.returnValue=s;
return s;
}}})},destruct:function(){this._stopWindowObserver();
this._manager=this._window=null;
},defer:function(u){qx.event.Registration.addHandler(u);
}});
})();
(function(){var f="ready",d="qx.application",c="beforeunload",b="qx.core.Init",a="shutdown";
qx.Class.define(b,{statics:{getApplication:function(){return this.__cy||null;
},ready:function(){if(this.__cy){return;
}
if(qx.bom.client.Engine.UNKNOWN_ENGINE){qx.log.Logger.warn("Could not detect engine!");
}
if(qx.bom.client.Engine.UNKNOWN_VERSION){qx.log.Logger.warn("Could not detect the version of the engine!");
}
if(qx.bom.client.Platform.UNKNOWN_PLATFORM){qx.log.Logger.warn("Could not detect platform!");
}
if(qx.bom.client.System.UNKNOWN_SYSTEM){qx.log.Logger.warn("Could not detect system!");
}qx.log.Logger.debug(this,"Load runtime: "+(new Date-qx.Bootstrap.LOADSTART)+"ms");
var h=qx.core.Setting.get(d);
var i=qx.Class.getByName(h);

if(i){this.__cy=new i;
var g=new Date;
this.__cy.main();
qx.log.Logger.debug(this,"Main runtime: "+(new Date-g)+"ms");
var g=new Date;
this.__cy.finalize();
qx.log.Logger.debug(this,"Finalize runtime: "+(new Date-g)+"ms");
}else{qx.log.Logger.warn("Missing application class: "+h);
}},__cz:function(e){var j=this.__cy;

if(j){e.setReturnValue(j.close());
}},__cA:function(){var k=this.__cy;

if(k){k.terminate();
}}},defer:function(l){qx.event.Registration.addListener(window,f,l.ready,l);
qx.event.Registration.addListener(window,a,l.__cA,l);
qx.event.Registration.addListener(window,c,l.__cz,l);
}});
})();
(function(){var a="qx.application.IApplication";
qx.Interface.define(a,{members:{main:function(){},finalize:function(){},close:function(){},terminate:function(){}}});
})();
(function(){var a="qx.locale.MTranslation";
qx.Mixin.define(a,{members:{tr:function(b,c){var d=qx.locale.Manager;

if(d){return d.tr.apply(d,arguments);
}throw new Error("To enable localization please include qx.locale.Manager into your build!");
},trn:function(e,f,g,h){var i=qx.locale.Manager;

if(i){return i.trn.apply(i,arguments);
}throw new Error("To enable localization please include qx.locale.Manager into your build!");
},trc:function(j,k,l){var m=qx.locale.Manager;

if(m){return m.trc.apply(m,arguments);
}throw new Error("To enable localization please include qx.locale.Manager into your build!");
},marktr:function(n){var o=qx.locale.Manager;

if(o){return o.marktr.apply(o,arguments);
}throw new Error("To enable localization please include qx.locale.Manager into your build!");
}}});
})();
(function(){var b="abstract",a="qx.application.AbstractGui";
qx.Class.define(a,{type:b,extend:qx.core.Object,implement:[qx.application.IApplication],include:qx.locale.MTranslation,members:{__cB:null,_createRootWidget:function(){throw new Error("Abstract method call");
},getRoot:function(){return this.__cB;
},main:function(){qx.theme.manager.Meta.getInstance().initialize();
qx.ui.tooltip.Manager.getInstance();
this.__cB=this._createRootWidget();
},finalize:function(){this.render();
},render:function(){qx.ui.core.queue.Manager.flush();
},close:function(c){},terminate:function(){}},destruct:function(){this.__cB=null;
}});
})();
(function(){var a="qx.application.Standalone";
qx.Class.define(a,{extend:qx.application.AbstractGui,members:{_createRootWidget:function(){return new qx.ui.root.Application(document);
}}});
})();
(function(){var h='execute',g="lino.Application",f="Cities",d="Countries",c="Qooxdoo!",a='http://qooxdoo.org';
qx.Class.define(g,{extend:qx.application.Standalone,members:{main:function(){qx.application.Standalone.prototype.main.call(this);
{};
this.setupMainMenu();
},showWindow:function(k){k.open();
this.getRoot().add(k,{left:50,top:10});
},setupMainMenu:function(){var l=new qx.ui.toolbar.ToolBar();
this.getRoot().add(l,{left:0,top:0,right:0});
var n=new qx.ui.toolbar.MenuButton(d);
l.add(n);
var m=new qx.ui.menu.Menu();
n.setMenu(m);
var b=new qx.ui.menu.Button(f);
m.add(b);
b.addListener(h,function(){this.showWindow(new lino.CountriesCitiesTable(this));
},this);
var b=new qx.ui.menu.Button(c);
m.add(b);
b.addListener(h,function(){window.location.href=a;
},this);
},loadMenu:function(o){var s=new qx.ui.toolbar.ToolBar();
this.getRoot().add(s,{left:0,top:0,right:0});
for(var i=0;i<o.length;i++){var q=o[i];

if(q.menu){var p=new qx.ui.toolbar.MenuButton(q.text);
s.add(p);
var m=new qx.ui.menu.Menu();

for(var j=0;j<q.menu.items.length;j++){var r=q.menu.items[j];
var b=new qx.ui.menu.Button(r.text);

if(r.href){b.href=r.href;
b.addListener(h,function(e){window.location=e.getTarget().href;
});
}else{b.addListener(h,r.handler,this);
}m.add(b);
}p.setMenu(m);
}}}}});
})();
(function(){var a="qx.event.type.Data";
qx.Class.define(a,{extend:qx.event.type.Event,members:{__cC:null,__cD:null,init:function(b,c,d){qx.event.type.Event.prototype.init.call(this,false,d);
this.__cC=b;
this.__cD=c;
return this;
},clone:function(e){var f=qx.event.type.Event.prototype.clone.call(this,e);
f.__cC=this.__cC;
f.__cD=this.__cD;
return f;
},getData:function(){return this.__cC;
},getOldData:function(){return this.__cD;
}},destruct:function(){this.__cC=this.__cD=null;
}});
})();
(function(){var b="",a="qx.core.WindowError";
qx.Bootstrap.define(a,{extend:Error,construct:function(c,d,e){Error.call(this,c);
this.__cE=c;
this.__cF=d||b;
this.__cG=e===undefined?-1:e;
},members:{__cE:null,__cF:null,__cG:null,toString:function(){return this.__cE;
},getUri:function(){return this.__cF;
},getLineNumber:function(){return this.__cG;
}}});
})();
(function(){var a="qx.lang.Date";
qx.Class.define(a,{statics:{now:function(){return +new Date;
}}});
})();
(function(){var a="qx.util.DisposeUtil";
qx.Class.define(a,{statics:{disposeObjects:function(b,c,d){var name;

for(var i=0,l=c.length;i<l;i++){name=c[i];

if(b[name]==null||!b.hasOwnProperty(name)){continue;
}
if(!qx.core.ObjectRegistry.inShutDown){if(b[name].dispose){if(!d&&b[name].constructor.$$instance){throw new Error("The object stored in key "+name+" is a singleton! Please use disposeSingleton instead.");
}else{b[name].dispose();
}}else{throw new Error("Has no disposable object under key: "+name+"!");
}}b[name]=null;
}},disposeArray:function(e,f){var h=e[f];

if(!h){return;
}if(qx.core.ObjectRegistry.inShutDown){e[f]=null;
return;
}try{var g;

for(var i=h.length-1;i>=0;i--){g=h[i];

if(g){g.dispose();
}}}catch(j){throw new Error("The array field: "+f+" of object: "+e+" has non disposable entries: "+j);
}h.length=0;
e[f]=null;
},disposeMap:function(k,m){var o=k[m];

if(!o){return;
}if(qx.core.ObjectRegistry.inShutDown){k[m]=null;
return;
}try{var n;

for(var p in o){n=o[p];

if(o.hasOwnProperty(p)&&n){n.dispose();
}}}catch(q){throw new Error("The map field: "+m+" of object: "+k+" has non disposable entries: "+q);
}k[m]=null;
},disposeTriggeredBy:function(r,s){var t=s.dispose;
s.dispose=function(){t.call(s);
r.dispose();
};
}}});
})();
(function(){var m="get",l="",k="[",h="last",g="change",f="]",d=".",c="Number",b="String",a="set",E="deepBinding",D="item",C="reset",B="' (",A="Boolean",z=").",y=") to the object '",x="Integer",w=" of object ",v="qx.data.SingleValueBinding",t="Binding property ",u="PositiveNumber",r="Binding from '",s="PositiveInteger",p="Binding does not exist!",q="Date",n=" not possible: No event available. ";
qx.Class.define(v,{statics:{DEBUG_ON:false,__cI:{},bind:function(F,G,H,I,J){var T=this.__cK(F,G,H,I,J);
var O=G.split(d);
var L=this.__cQ(O);
var S=[];
var P=[];
var Q=[];
var M=[];
var N=F;
for(var i=0;i<O.length;i++){if(L[i]!==l){M.push(g);
}else{M.push(this.__cL(N,O[i]));
}S[i]=N;
if(i==O.length-1){if(L[i]!==l){var W=L[i]===h?N.length-1:L[i];
var K=N.getItem(W);
this.__cP(K,H,I,J,F);
Q[i]=this.__cR(N,M[i],H,I,J,L[i]);
}else{if(O[i]!=null&&N[m+qx.lang.String.firstUp(O[i])]!=null){var K=N[m+qx.lang.String.firstUp(O[i])]();
this.__cP(K,H,I,J,F);
}Q[i]=this.__cR(N,M[i],H,I,J);
}}else{var U={index:i,propertyNames:O,sources:S,listenerIds:Q,arrayIndexValues:L,targetObject:H,targetPropertyChain:I,options:J,listeners:P};
var R=qx.lang.Function.bind(this.__cJ,this,U);
P.push(R);
Q[i]=N.addListener(M[i],R);
}if(N[m+qx.lang.String.firstUp(O[i])]==null){N=null;
}else if(L[i]!==l){N=N[m+qx.lang.String.firstUp(O[i])](L[i]);
}else{N=N[m+qx.lang.String.firstUp(O[i])]();
}
if(!N){break;
}}var V={type:E,listenerIds:Q,sources:S,targetListenerIds:T.listenerIds,targets:T.targets};
this.__cS(V,F,G,H,I);
return V;
},__cJ:function(X){if(X.options&&X.options.onUpdate){X.options.onUpdate(X.sources[X.index],X.targetObject);
}for(var j=X.index+1;j<X.propertyNames.length;j++){var bc=X.sources[j];
X.sources[j]=null;

if(!bc){continue;
}bc.removeListenerById(X.listenerIds[j]);
}var bc=X.sources[X.index];
for(var j=X.index+1;j<X.propertyNames.length;j++){if(X.arrayIndexValues[j-1]!==l){bc=bc[m+qx.lang.String.firstUp(X.propertyNames[j-1])](X.arrayIndexValues[j-1]);
}else{bc=bc[m+qx.lang.String.firstUp(X.propertyNames[j-1])]();
}X.sources[j]=bc;
if(!bc){this.__cM(X.targetObject,X.targetPropertyChain);
break;
}if(j==X.propertyNames.length-1){if(qx.Class.implementsInterface(bc,qx.data.IListData)){var bd=X.arrayIndexValues[j]===h?bc.length-1:X.arrayIndexValues[j];
var ba=bc.getItem(bd);
this.__cP(ba,X.targetObject,X.targetPropertyChain,X.options,X.sources[X.index]);
X.listenerIds[j]=this.__cR(bc,g,X.targetObject,X.targetPropertyChain,X.options,X.arrayIndexValues[j]);
}else{if(X.propertyNames[j]!=null&&bc[m+qx.lang.String.firstUp(X.propertyNames[j])]!=null){var ba=bc[m+qx.lang.String.firstUp(X.propertyNames[j])]();
this.__cP(ba,X.targetObject,X.targetPropertyChain,X.options,X.sources[X.index]);
}var bb=this.__cL(bc,X.propertyNames[j]);
X.listenerIds[j]=this.__cR(bc,bb,X.targetObject,X.targetPropertyChain,X.options);
}}else{if(X.listeners[j]==null){var Y=qx.lang.Function.bind(this.__cJ,this,X);
X.listeners.push(Y);
}if(qx.Class.implementsInterface(bc,qx.data.IListData)){var bb=g;
}else{var bb=this.__cL(bc,X.propertyNames[j]);
}X.listenerIds[j]=bc.addListener(bb,X.listeners[j]);
}}},__cK:function(be,bf,bg,bh,bi){var bm=bh.split(d);
var bk=this.__cQ(bm);
var br=[];
var bq=[];
var bo=[];
var bn=[];
var bl=bg;
for(var i=0;i<bm.length-1;i++){if(bk[i]!==l){bn.push(g);
}else{try{bn.push(this.__cL(bl,bm[i]));
}catch(e){break;
}}br[i]=bl;
var bp=function(){for(var j=i+1;j<bm.length-1;j++){var bu=br[j];
br[j]=null;

if(!bu){continue;
}bu.removeListenerById(bo[j]);
}var bu=br[i];
for(var j=i+1;j<bm.length-1;j++){var bs=qx.lang.String.firstUp(bm[j-1]);
if(bk[j-1]!==l){var bv=bk[j-1]===h?bu.getLength()-1:bk[j-1];
bu=bu[m+bs](bv);
}else{bu=bu[m+bs]();
}br[j]=bu;
if(bq[j]==null){bq.push(bp);
}if(qx.Class.implementsInterface(bu,qx.data.IListData)){var bt=g;
}else{try{var bt=qx.data.SingleValueBinding.__cL(bu,bm[j]);
}catch(e){break;
}}bo[j]=bu.addListener(bt,bq[j]);
}qx.data.SingleValueBinding.updateTarget(be,bf,bg,bh,bi);
};
bq.push(bp);
bo[i]=bl.addListener(bn[i],bp);
var bj=qx.lang.String.firstUp(bm[i]);
if(bl[m+bj]==null){bl=null;
}else if(bk[i]!==l){bl=bl[m+bj](bk[i]);
}else{bl=bl[m+bj]();
}
if(!bl){break;
}}return {listenerIds:bo,targets:br};
},updateTarget:function(bw,bx,by,bz,bA){var bB=this.getValueFromObject(bw,bx);
bB=qx.data.SingleValueBinding.__cT(bB,by,bz,bA);
this.__cN(by,bz,bB);
},getValueFromObject:function(o,bC){var bG=this.__cO(o,bC);
var bE;

if(bG!=null){var bI=bC.substring(bC.lastIndexOf(d)+1,bC.length);
if(bI.charAt(bI.length-1)==f){var bD=bI.substring(bI.lastIndexOf(k)+1,bI.length-1);
var bF=bI.substring(0,bI.lastIndexOf(k));
var bH=bG[m+qx.lang.String.firstUp(bF)]();

if(bD==h){bD=bH.length-1;
}
if(bH!=null){bE=bH.getItem(bD);
}}else{bE=bG[m+qx.lang.String.firstUp(bI)]();
}}return bE;
},__cL:function(bJ,bK){var bL=this.__cU(bJ,bK);
if(bL==null){if(qx.Class.supportsEvent(bJ.constructor,bK)){bL=bK;
}else if(qx.Class.supportsEvent(bJ.constructor,g+qx.lang.String.firstUp(bK))){bL=g+qx.lang.String.firstUp(bK);
}else{throw new qx.core.AssertionError(t+bK+w+bJ+n);
}}return bL;
},__cM:function(bM,bN){var bO=this.__cO(bM,bN);

if(bO!=null){var bP=bN.substring(bN.lastIndexOf(d)+1,bN.length);
if(bP.charAt(bP.length-1)==f){this.__cN(bM,bN,null);
return;
}if(bO[C+qx.lang.String.firstUp(bP)]!=undefined){bO[C+qx.lang.String.firstUp(bP)]();
}else{bO[a+qx.lang.String.firstUp(bP)](null);
}}},__cN:function(bQ,bR,bS){var bW=this.__cO(bQ,bR);

if(bW!=null){var bX=bR.substring(bR.lastIndexOf(d)+1,bR.length);
if(bX.charAt(bX.length-1)==f){var bT=bX.substring(bX.lastIndexOf(k)+1,bX.length-1);
var bV=bX.substring(0,bX.lastIndexOf(k));
var bU=bQ;

if(!qx.Class.implementsInterface(bU,qx.data.IListData)){bU=bW[m+qx.lang.String.firstUp(bV)]();
}
if(bT==h){bT=bU.length-1;
}
if(bU!=null){bU.setItem(bT,bS);
}}else{bW[a+qx.lang.String.firstUp(bX)](bS);
}}},__cO:function(bY,ca){var cd=ca.split(d);
var ce=bY;
for(var i=0;i<cd.length-1;i++){try{var cc=cd[i];
if(cc.indexOf(f)==cc.length-1){var cb=cc.substring(cc.indexOf(k)+1,cc.length-1);
cc=cc.substring(0,cc.indexOf(k));
}if(cc!=l){ce=ce[m+qx.lang.String.firstUp(cc)]();
}if(cb!=null){if(cb==h){cb=ce.length-1;
}ce=ce.getItem(cb);
cb=null;
}}catch(cf){return null;
}}return ce;
},__cP:function(cg,ch,ci,cj,ck){cg=this.__cT(cg,ch,ci,cj);
if(cg===undefined){this.__cM(ch,ci);
}if(cg!==undefined){try{this.__cN(ch,ci,cg);
if(cj&&cj.onUpdate){cj.onUpdate(ck,ch,cg);
}}catch(e){if(!(e instanceof qx.core.ValidationError)){throw e;
}
if(cj&&cj.onSetFail){cj.onSetFail(e);
}else{qx.log.Logger.warn("Failed so set value "+cg+" on "+ch+". Error message: "+e);
}}}},__cQ:function(cl){var cm=[];
for(var i=0;i<cl.length;i++){var name=cl[i];
if(qx.lang.String.endsWith(name,f)){var cn=name.substring(name.indexOf(k)+1,name.indexOf(f));
if(name.indexOf(f)!=name.length-1){throw new Error("Please use only one array at a time: "+name+" does not work.");
}
if(cn!==h){if(cn==l||isNaN(parseInt(cn,10))){throw new Error("No number or 'last' value hast been given"+" in a array binding: "+name+" does not work.");
}}if(name.indexOf(k)!=0){cl[i]=name.substring(0,name.indexOf(k));
cm[i]=l;
cm[i+1]=cn;
cl.splice(i+1,0,D);
i++;
}else{cm[i]=cn;
cl.splice(i,1,D);
}}else{cm[i]=l;
}}return cm;
},__cR:function(co,cp,cq,cr,cs,ct){var cu;
{};
var cw=function(cx,e){if(cx!==l){if(cx===h){cx=co.length-1;
}var cA=co.getItem(cx);
if(cA===undefined){qx.data.SingleValueBinding.__cM(cq,cr);
}var cy=e.getData().start;
var cz=e.getData().end;

if(cx<cy||cx>cz){return;
}}else{var cA=e.getData();
}if(qx.data.SingleValueBinding.DEBUG_ON){qx.log.Logger.debug("Binding executed from "+co+" by "+cp+" to "+cq+" ("+cr+")");
qx.log.Logger.debug("Data before conversion: "+cA);
}cA=qx.data.SingleValueBinding.__cT(cA,cq,cr,cs);
if(qx.data.SingleValueBinding.DEBUG_ON){qx.log.Logger.debug("Data after conversion: "+cA);
}try{if(cA!==undefined){qx.data.SingleValueBinding.__cN(cq,cr,cA);
}else{qx.data.SingleValueBinding.__cM(cq,cr);
}if(cs&&cs.onUpdate){cs.onUpdate(co,cq,cA);
}}catch(e){if(!(e instanceof qx.core.ValidationError)){throw e;
}
if(cs&&cs.onSetFail){cs.onSetFail(e);
}else{qx.log.Logger.warn("Failed so set value "+cA+" on "+cq+". Error message: "+e);
}}};
if(!ct){ct=l;
}cw=qx.lang.Function.bind(cw,co,ct);
var cv=co.addListener(cp,cw);
return cv;
},__cS:function(cB,cC,cD,cE,cF){if(this.__cI[cC.toHashCode()]===undefined){this.__cI[cC.toHashCode()]=[];
}this.__cI[cC.toHashCode()].push([cB,cC,cD,cE,cF]);
},__cT:function(cG,cH,cI,cJ){if(cJ&&cJ.converter){var cL;

if(cH.getModel){cL=cH.getModel();
}return cJ.converter(cG,cL);
}else{var cN=this.__cO(cH,cI);
var cO=cI.substring(cI.lastIndexOf(d)+1,cI.length);
if(cN==null){return cG;
}var cM=qx.Class.getPropertyDefinition(cN.constructor,cO);
var cK=cM==null?l:cM.check;
return this.__cV(cG,cK);
}},__cU:function(cP,cQ){var cR=qx.Class.getPropertyDefinition(cP.constructor,cQ);

if(cR==null){return null;
}return cR.event;
},__cV:function(cS,cT){var cU=qx.lang.Type.getClass(cS);
if((cU==c||cU==b)&&(cT==x||cT==s)){cS=parseInt(cS,10);
}if((cU==A||cU==c||cU==q)&&cT==b){cS=cS+l;
}if((cU==c||cU==b)&&(cT==c||cT==u)){cS=parseFloat(cS);
}return cS;
},removeBindingFromObject:function(cV,cW){if(cW.type==E){for(var i=0;i<cW.sources.length;i++){if(cW.sources[i]){cW.sources[i].removeListenerById(cW.listenerIds[i]);
}}for(var i=0;i<cW.targets.length;i++){if(cW.targets[i]){cW.targets[i].removeListenerById(cW.targetListenerIds[i]);
}}}else{cV.removeListenerById(cW);
}var cX=this.__cI[cV.toHashCode()];
if(cX!=undefined){for(var i=0;i<cX.length;i++){if(cX[i][0]==cW){qx.lang.Array.remove(cX,cX[i]);
return;
}}}throw new Error("Binding could not be found!");
},removeAllBindingsForObject:function(cY){{};
var da=this.__cI[cY.toHashCode()];

if(da!=undefined){for(var i=da.length-1;i>=0;i--){this.removeBindingFromObject(cY,da[i][0]);
}}},getAllBindingsForObject:function(db){if(this.__cI[db.toHashCode()]===undefined){this.__cI[db.toHashCode()]=[];
}return this.__cI[db.toHashCode()];
},removeAllBindings:function(){for(var dd in this.__cI){var dc=qx.core.ObjectRegistry.fromHashCode(dd);
if(dc==null){delete this.__cI[dd];
continue;
}this.removeAllBindingsForObject(dc);
}this.__cI={};
},getAllBindings:function(){return this.__cI;
},showBindingInLog:function(de,df){var dh;
for(var i=0;i<this.__cI[de.toHashCode()].length;i++){if(this.__cI[de.toHashCode()][i][0]==df){dh=this.__cI[de.toHashCode()][i];
break;
}}
if(dh===undefined){var dg=p;
}else{var dg=r+dh[1]+B+dh[2]+y+dh[3]+B+dh[4]+z;
}qx.log.Logger.debug(dg);
},showAllBindingsInLog:function(){for(var dj in this.__cI){var di=qx.core.ObjectRegistry.fromHashCode(dj);

for(var i=0;i<this.__cI[dj].length;i++){this.showBindingInLog(di,this.__cI[dj][i][0]);
}}}}});
})();
(function(){var a="qx.core.ValidationError";
qx.Class.define(a,{extend:qx.type.BaseError});
})();
(function(){var a="qx.event.handler.Object";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.event.IEventHandler,statics:{PRIORITY:qx.event.Registration.PRIORITY_LAST,SUPPORTED_TYPES:null,TARGET_CHECK:qx.event.IEventHandler.TARGET_OBJECT,IGNORE_CAN_HANDLE:false},members:{canHandleEvent:function(b,c){return qx.Class.supportsEvent(b.constructor,c);
},registerEvent:function(d,e,f){},unregisterEvent:function(g,h,i){}},defer:function(j){qx.event.Registration.addHandler(j);
}});
})();
(function(){var k="indexOf",j="lastIndexOf",h="slice",g="concat",f="join",e="toLocaleUpperCase",d="shift",c="substr",b="filter",a="unshift",I="match",H="quote",G="qx.lang.Generics",F="localeCompare",E="sort",D="some",C="charAt",B="split",A="substring",z="pop",t="toUpperCase",u="replace",q="push",r="charCodeAt",o="every",p="reverse",m="search",n="forEach",v="map",w="toLowerCase",y="splice",x="toLocaleLowerCase";
qx.Class.define(G,{statics:{__cW:{"Array":[f,p,E,q,z,d,a,y,g,h,k,j,n,v,b,D,o],"String":[H,A,w,t,C,r,k,j,x,e,F,I,m,u,B,c,g,h]},__cX:function(J,K){return function(s){return J.prototype[K].apply(s,Array.prototype.slice.call(arguments,1));
};
},__cY:function(){var L=qx.lang.Generics.__cW;

for(var P in L){var N=window[P];
var M=L[P];

for(var i=0,l=M.length;i<l;i++){var O=M[i];

if(!N[O]){N[O]=qx.lang.Generics.__cX(N,O);
}}}}},defer:function(Q){Q.__cY();
}});
})();
(function(){var n="iPod",m="Win32",l="",k="Win64",j="Linux",i="BSD",h="Macintosh",g="iPhone",f="Windows",e="qx.bom.client.Platform",b="iPad",d="X11",c="MacIntel",a="MacPPC";
qx.Class.define(e,{statics:{NAME:"",WIN:false,MAC:false,UNIX:false,UNKNOWN_PLATFORM:false,__da:function(){var o=navigator.platform;
if(o==null||o===l){o=navigator.userAgent;
}
if(o.indexOf(f)!=-1||o.indexOf(m)!=-1||o.indexOf(k)!=-1){this.WIN=true;
this.NAME="win";
}else if(o.indexOf(h)!=-1||o.indexOf(a)!=-1||o.indexOf(c)!=-1||o.indexOf(n)!=-1||o.indexOf(g)!=-1||o.indexOf(b)!=-1){this.MAC=true;
this.NAME="mac";
}else if(o.indexOf(d)!=-1||o.indexOf(j)!=-1||o.indexOf(i)!=-1){this.UNIX=true;
this.NAME="unix";
}else{this.UNKNOWN_PLATFORM=true;
this.WIN=true;
this.NAME="win";
}}},defer:function(p){p.__da();
}});
})();
(function(){var j="win98",i="osx2",h="osx0",g="osx4",f="win95",e="win2000",d="osx1",c="osx5",b="osx3",a="Windows NT 5.01",I=")",H="winxp",G="freebsd",F="sunos",E="SV1",D="|",C="nintendods",B="winnt4",A="wince",z="winme",q="os9",r="\.",o="osx",p="linux",m="netbsd",n="winvista",k="openbsd",l="(",s="win2003",t="iPad",v="symbian",u="win7",x="g",w="qx.bom.client.System",y=" Mobile/";
qx.Bootstrap.define(w,{statics:{NAME:"",SP1:false,SP2:false,WIN95:false,WIN98:false,WINME:false,WINNT4:false,WIN2000:false,WINXP:false,WIN2003:false,WINVISTA:false,WIN7:false,WINCE:false,LINUX:false,SUNOS:false,FREEBSD:false,NETBSD:false,OPENBSD:false,OSX:false,OS9:false,SYMBIAN:false,NINTENDODS:false,PSP:false,IPHONE:false,IPAD:false,UNKNOWN_SYSTEM:false,__db:{"Windows NT 6.1":u,"Windows NT 6.0":n,"Windows NT 5.2":s,"Windows NT 5.1":H,"Windows NT 5.0":e,"Windows 2000":e,"Windows NT 4.0":B,"Win 9x 4.90":z,"Windows CE":A,"Windows 98":j,"Win98":j,"Windows 95":f,"Win95":f,"Linux":p,"FreeBSD":G,"NetBSD":m,"OpenBSD":k,"SunOS":F,"Symbian System":v,"Nitro":C,"PSP":"sonypsp","Mac OS X 10_5":c,"Mac OS X 10.5":c,"Mac OS X 10_4":g,"Mac OS X 10.4":g,"Mac OS X 10_3":b,"Mac OS X 10.3":b,"Mac OS X 10_2":i,"Mac OS X 10.2":i,"Mac OS X 10_1":d,"Mac OS X 10.1":d,"Mac OS X 10_0":h,"Mac OS X 10.0":h,"Mac OS X":o,"Mac OS 9":q},__dc:function(){var L=navigator.userAgent;
var K=[];

for(var J in this.__db){K.push(J);
}var M=new RegExp(l+K.join(D).replace(/\./g,r)+I,x);

if(!M.test(L)){this.UNKNOWN_SYSTEM=true;

if(!qx.bom.client.Platform.UNKNOWN_PLATFORM){if(qx.bom.client.Platform.UNIX){this.NAME="linux";
this.LINUX=true;
}else if(qx.bom.client.Platform.MAC){this.NAME="osx5";
this.OSX=true;
}else{this.NAME="winxp";
this.WINXP=true;
}}else{this.NAME="winxp";
this.WINXP=true;
}return;
}
if(qx.bom.client.Engine.WEBKIT&&RegExp(y).test(navigator.userAgent)){if(RegExp(t).test(navigator.userAgent)){this.IPAD=true;
this.NAME="ipad";
}else{this.IPHONE=true;
this.NAME="iphone";
}}else{this.NAME=this.__db[RegExp.$1];
this[this.NAME.toUpperCase()]=true;

if(qx.bom.client.Platform.WIN){if(L.indexOf(a)!==-1){this.SP1=true;
}else if(qx.bom.client.Engine.MSHTML&&L.indexOf(E)!==-1){this.SP2=true;
}}}}},defer:function(N){N.__dc();
}});
})();
(function(){var f="_applyTheme",e="qx.theme",d="qx.theme.manager.Meta",c="qx.theme.Modern",b="Theme",a="singleton";
qx.Class.define(d,{type:a,extend:qx.core.Object,properties:{theme:{check:b,nullable:true,apply:f}},members:{_applyTheme:function(g,h){var k=null;
var n=null;
var q=null;
var r=null;
var m=null;

if(g){k=g.meta.color||null;
n=g.meta.decoration||null;
q=g.meta.font||null;
r=g.meta.icon||null;
m=g.meta.appearance||null;
}var o=qx.theme.manager.Color.getInstance();
var p=qx.theme.manager.Decoration.getInstance();
var i=qx.theme.manager.Font.getInstance();
var l=qx.theme.manager.Icon.getInstance();
var j=qx.theme.manager.Appearance.getInstance();
o.setTheme(k);
p.setTheme(n);
i.setTheme(q);
l.setTheme(r);
j.setTheme(m);
},initialize:function(){var t=qx.core.Setting;
var s,u;
s=t.get(e);

if(s){u=qx.Theme.getByName(s);

if(!u){throw new Error("The theme to use is not available: "+s);
}this.setTheme(u);
}}},settings:{"qx.theme":c}});
})();
(function(){var b="qx.util.ValueManager",a="abstract";
qx.Class.define(b,{type:a,extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this._dynamic={};
},members:{_dynamic:null,resolveDynamic:function(c){return this._dynamic[c];
},isDynamic:function(d){return !!this._dynamic[d];
},resolve:function(e){if(e&&this._dynamic[e]){return this._dynamic[e];
}return e;
},_setDynamic:function(f){this._dynamic=f;
},_getDynamic:function(){return this._dynamic;
}},destruct:function(){this._dynamic=null;
}});
})();
(function(){var f="_applyTheme",e="qx.theme.manager.Color",d="Theme",c="changeTheme",b="string",a="singleton";
qx.Class.define(e,{type:a,extend:qx.util.ValueManager,properties:{theme:{check:d,nullable:true,apply:f,event:c}},members:{_applyTheme:function(g){var h={};

if(g){var i=g.colors;
var j=qx.util.ColorUtil;
var k;

for(var l in i){k=i[l];

if(typeof k===b){if(!j.isCssString(k)){throw new Error("Could not parse color: "+k);
}}else if(k instanceof Array){k=j.rgbToRgbString(k);
}else{throw new Error("Could not parse color: "+k);
}h[l]=k;
}}this._setDynamic(h);
},resolve:function(m){var p=this._dynamic;
var n=p[m];

if(n){return n;
}var o=this.getTheme();

if(o!==null&&o.colors[m]){return p[m]=o.colors[m];
}return m;
},isDynamic:function(q){var s=this._dynamic;

if(q&&(s[q]!==undefined)){return true;
}var r=this.getTheme();

if(r!==null&&q&&(r.colors[q]!==undefined)){s[q]=r.colors[q];
return true;
}return false;
}}});
})();
(function(){var h=",",e="rgb(",d=")",c="qx.theme.manager.Color",a="qx.util.ColorUtil";
qx.Class.define(a,{statics:{REGEXP:{hex3:/^#([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})$/,hex6:/^#([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})$/,rgb:/^rgb\(\s*([0-9]{1,3}\.{0,1}[0-9]*)\s*,\s*([0-9]{1,3}\.{0,1}[0-9]*)\s*,\s*([0-9]{1,3}\.{0,1}[0-9]*)\s*\)$/,rgba:/^rgba\(\s*([0-9]{1,3}\.{0,1}[0-9]*)\s*,\s*([0-9]{1,3}\.{0,1}[0-9]*)\s*,\s*([0-9]{1,3}\.{0,1}[0-9]*)\s*,\s*([0-9]{1,3}\.{0,1}[0-9]*)\s*\)$/},SYSTEM:{activeborder:true,activecaption:true,appworkspace:true,background:true,buttonface:true,buttonhighlight:true,buttonshadow:true,buttontext:true,captiontext:true,graytext:true,highlight:true,highlighttext:true,inactiveborder:true,inactivecaption:true,inactivecaptiontext:true,infobackground:true,infotext:true,menu:true,menutext:true,scrollbar:true,threeddarkshadow:true,threedface:true,threedhighlight:true,threedlightshadow:true,threedshadow:true,window:true,windowframe:true,windowtext:true},NAMED:{black:[0,0,0],silver:[192,192,192],gray:[128,128,128],white:[255,255,255],maroon:[128,0,0],red:[255,0,0],purple:[128,0,128],fuchsia:[255,0,255],green:[0,128,0],lime:[0,255,0],olive:[128,128,0],yellow:[255,255,0],navy:[0,0,128],blue:[0,0,255],teal:[0,128,128],aqua:[0,255,255],transparent:[-1,-1,-1],magenta:[255,0,255],orange:[255,165,0],brown:[165,42,42]},isNamedColor:function(j){return this.NAMED[j]!==undefined;
},isSystemColor:function(k){return this.SYSTEM[k]!==undefined;
},supportsThemes:function(){return qx.Class.isDefined(c);
},isThemedColor:function(l){if(!this.supportsThemes()){return false;
}return qx.theme.manager.Color.getInstance().isDynamic(l);
},stringToRgb:function(m){if(this.supportsThemes()&&this.isThemedColor(m)){var m=qx.theme.manager.Color.getInstance().resolveDynamic(m);
}
if(this.isNamedColor(m)){return this.NAMED[m];
}else if(this.isSystemColor(m)){throw new Error("Could not convert system colors to RGB: "+m);
}else if(this.isRgbString(m)){return this.__dd();
}else if(this.isHex3String(m)){return this.__df();
}else if(this.isHex6String(m)){return this.__dg();
}throw new Error("Could not parse color: "+m);
},cssStringToRgb:function(n){if(this.isNamedColor(n)){return this.NAMED[n];
}else if(this.isSystemColor(n)){throw new Error("Could not convert system colors to RGB: "+n);
}else if(this.isRgbString(n)){return this.__dd();
}else if(this.isRgbaString(n)){return this.__de();
}else if(this.isHex3String(n)){return this.__df();
}else if(this.isHex6String(n)){return this.__dg();
}throw new Error("Could not parse color: "+n);
},stringToRgbString:function(o){return this.rgbToRgbString(this.stringToRgb(o));
},rgbToRgbString:function(s){return e+s[0]+h+s[1]+h+s[2]+d;
},rgbToHexString:function(u){return (qx.lang.String.pad(u[0].toString(16).toUpperCase(),2)+qx.lang.String.pad(u[1].toString(16).toUpperCase(),2)+qx.lang.String.pad(u[2].toString(16).toUpperCase(),2));
},isValidPropertyValue:function(v){return this.isThemedColor(v)||this.isNamedColor(v)||this.isHex3String(v)||this.isHex6String(v)||this.isRgbString(v);
},isCssString:function(w){return this.isSystemColor(w)||this.isNamedColor(w)||this.isHex3String(w)||this.isHex6String(w)||this.isRgbString(w);
},isHex3String:function(x){return this.REGEXP.hex3.test(x);
},isHex6String:function(y){return this.REGEXP.hex6.test(y);
},isRgbString:function(z){return this.REGEXP.rgb.test(z);
},isRgbaString:function(A){return this.REGEXP.rgba.test(A);
},__dd:function(){var D=parseInt(RegExp.$1,10);
var C=parseInt(RegExp.$2,10);
var B=parseInt(RegExp.$3,10);
return [D,C,B];
},__de:function(){var G=parseInt(RegExp.$1,10);
var F=parseInt(RegExp.$2,10);
var E=parseInt(RegExp.$3,10);
return [G,F,E];
},__df:function(){var J=parseInt(RegExp.$1,16)*17;
var I=parseInt(RegExp.$2,16)*17;
var H=parseInt(RegExp.$3,16)*17;
return [J,I,H];
},__dg:function(){var M=(parseInt(RegExp.$1,16)*16)+parseInt(RegExp.$2,16);
var L=(parseInt(RegExp.$3,16)*16)+parseInt(RegExp.$4,16);
var K=(parseInt(RegExp.$5,16)*16)+parseInt(RegExp.$6,16);
return [M,L,K];
},hex3StringToRgb:function(N){if(this.isHex3String(N)){return this.__df(N);
}throw new Error("Invalid hex3 value: "+N);
},hex6StringToRgb:function(O){if(this.isHex6String(O)){return this.__dg(O);
}throw new Error("Invalid hex6 value: "+O);
},hexStringToRgb:function(P){if(this.isHex3String(P)){return this.__df(P);
}
if(this.isHex6String(P)){return this.__dg(P);
}throw new Error("Invalid hex value: "+P);
},rgbToHsb:function(Q){var S,T,V;
var bc=Q[0];
var Y=Q[1];
var R=Q[2];
var bb=(bc>Y)?bc:Y;

if(R>bb){bb=R;
}var U=(bc<Y)?bc:Y;

if(R<U){U=R;
}V=bb/255.0;

if(bb!=0){T=(bb-U)/bb;
}else{T=0;
}
if(T==0){S=0;
}else{var X=(bb-bc)/(bb-U);
var ba=(bb-Y)/(bb-U);
var W=(bb-R)/(bb-U);

if(bc==bb){S=W-ba;
}else if(Y==bb){S=2.0+X-W;
}else{S=4.0+ba-X;
}S=S/6.0;

if(S<0){S=S+1.0;
}}return [Math.round(S*360),Math.round(T*100),Math.round(V*100)];
},hsbToRgb:function(bd){var i,f,p,q,t;
var be=bd[0]/360;
var bf=bd[1]/100;
var bg=bd[2]/100;

if(be>=1.0){be%=1.0;
}
if(bf>1.0){bf=1.0;
}
if(bg>1.0){bg=1.0;
}var bh=Math.floor(255*bg);
var bi={};

if(bf==0.0){bi.red=bi.green=bi.blue=bh;
}else{be*=6.0;
i=Math.floor(be);
f=be-i;
p=Math.floor(bh*(1.0-bf));
q=Math.floor(bh*(1.0-(bf*f)));
t=Math.floor(bh*(1.0-(bf*(1.0-f))));

switch(i){case 0:bi.red=bh;
bi.green=t;
bi.blue=p;
break;
case 1:bi.red=q;
bi.green=bh;
bi.blue=p;
break;
case 2:bi.red=p;
bi.green=bh;
bi.blue=t;
break;
case 3:bi.red=p;
bi.green=q;
bi.blue=bh;
break;
case 4:bi.red=t;
bi.green=p;
bi.blue=bh;
break;
case 5:bi.red=bh;
bi.green=p;
bi.blue=q;
break;
}}return [bi.red,bi.green,bi.blue];
},randomColor:function(){var r=Math.round(Math.random()*255);
var g=Math.round(Math.random()*255);
var b=Math.round(Math.random()*255);
return this.rgbToRgbString([r,g,b]);
}}});
})();
(function(){var m="object",l="__dh",k="_applyTheme",j="",h="_",g="qx.ui.decoration.",f="qx.theme.manager.Decoration",e=".",d="Theme",c="changeTheme",a="string",b="singleton";
qx.Class.define(f,{type:b,extend:qx.core.Object,properties:{theme:{check:d,nullable:true,apply:k,event:c}},members:{__dh:null,resolve:function(n){if(!n){return null;
}
if(typeof n===m){return n;
}var s=this.getTheme();

if(!s){return null;
}var p=this.__dh;

if(!p){p=this.__dh={};
}var o=p[n];

if(o){return o;
}var v=s.decorations[n];

if(!v){return null;
}if(!v.style){v.style={};
}var q=v;

while(q.include){q=s.decorations[q.include];
if(!v.decorator&&q.decorator){v.decorator=q.decorator;
}if(q.style){for(var u in q.style){if(v.style[u]==undefined){v.style[u]=q.style[u];
}}}}var r=v.decorator;

if(r==null){throw new Error("Missing definition of which decorator to use in entry: "+n+"!");
}if(r instanceof Array){var t=r.concat([]);

for(var i=0;i<t.length;i++){t[i]=t[i].basename.replace(e,j);
}var name=g+t.join(h);

if(!qx.Class.getByName(name)){qx.Class.define(name,{extend:qx.ui.decoration.DynamicDecorator,include:r});
}r=qx.Class.getByName(name);
}return p[n]=(new r).set(v.style);
},isValidPropertyValue:function(w){if(typeof w===a){return this.isDynamic(w);
}else if(typeof w===m){var x=w.constructor;
return qx.Class.hasInterface(x,qx.ui.decoration.IDecorator);
}return false;
},isDynamic:function(y){if(!y){return false;
}var z=this.getTheme();

if(!z){return false;
}return !!z.decorations[y];
},_applyTheme:function(A,B){var D=qx.util.AliasManager.getInstance();

if(B){for(var C in B.aliases){D.remove(C);
}}
if(A){for(var C in A.aliases){D.add(C,A.aliases[C]);
}}
if(!A){this.__dh={};
}}},destruct:function(){this._disposeMap(l);
}});
})();
(function(){var a="qx.ui.decoration.IDecorator";
qx.Interface.define(a,{members:{getMarkup:function(){},resize:function(b,c,d){},tint:function(e,f){},getInsets:function(){}}});
})();
(function(){var i="Number",h="_applyInsets",g="abstract",f="insetRight",e="insetTop",d="insetBottom",c="qx.ui.decoration.Abstract",b="shorthand",a="insetLeft";
qx.Class.define(c,{extend:qx.core.Object,implement:[qx.ui.decoration.IDecorator],type:g,properties:{insetLeft:{check:i,nullable:true,apply:h},insetRight:{check:i,nullable:true,apply:h},insetBottom:{check:i,nullable:true,apply:h},insetTop:{check:i,nullable:true,apply:h},insets:{group:[e,f,d,a],mode:b}},members:{__lh:null,_getDefaultInsets:function(){throw new Error("Abstract method called.");
},_isInitialized:function(){throw new Error("Abstract method called.");
},_resetInsets:function(){this.__lh=null;
},getInsets:function(){if(this.__lh){return this.__lh;
}var j=this._getDefaultInsets();
return this.__lh={left:this.getInsetLeft()==null?j.left:this.getInsetLeft(),right:this.getInsetRight()==null?j.right:this.getInsetRight(),bottom:this.getInsetBottom()==null?j.bottom:this.getInsetBottom(),top:this.getInsetTop()==null?j.top:this.getInsetTop()};
},_applyInsets:function(){{};
this.__lh=null;
}},destruct:function(){this.__lh=null;
}});
})();
(function(){var o="px",n="top",m="_tint",l="abstract",k='<div style="',j="",h="_getDefaultInsetsFor",g="bottom",f="qx.ui.decoration.DynamicDecorator",e="left",b="right",d="_resize",c="_style",a='"></div>';
qx.Class.define(f,{extend:qx.ui.decoration.Abstract,type:l,members:{getMarkup:function(){if(this._markup){return this._markup;
}var p={};

for(var name in this){if(name.indexOf(c)==0&&this[name] instanceof Function){this[name](p);
}}if(!this._generateMarkup){var q=[k];
q.push(qx.bom.element.Style.compile(p));
q.push(a);
q=q.join(j);
}else{var q=this._generateMarkup(p);
}return this._markup=q;
},resize:function(r,s,t){var v={};

for(var name in this){if(name.indexOf(d)==0&&this[name] instanceof Function){var u=this[name](r,s,t);

if(v.left==undefined){v.left=u.left;
v.top=u.top;
}
if(v.width==undefined){v.width=u.width;
v.height=u.height;
}
if(u.elementToApplyDimensions){v.elementToApplyDimensions=u.elementToApplyDimensions;
}v.left=u.left<v.left?u.left:v.left;
v.top=u.top<v.top?u.top:v.top;
v.width=u.width>v.width?u.width:v.width;
v.height=u.height>v.height?u.height:v.height;
}}if(v.left!=undefined){r.style.left=v.left+o;
r.style.top=v.top+o;
}if(v.width!=undefined){if(v.width<0){v.width=0;
}
if(v.height<0){v.height=0;
}
if(v.elementToApplyDimensions){r=v.elementToApplyDimensions;
}r.style.width=v.width+o;
r.style.height=v.height+o;
}},tint:function(w,x){for(var name in this){if(name.indexOf(m)==0&&this[name] instanceof Function){this[name](w,x,w.style);
}}},_isInitialized:function(){return !!this._markup;
},_getDefaultInsets:function(){var B=[n,b,g,e];
var z={};

for(var name in this){if(name.indexOf(h)==0&&this[name] instanceof Function){var A=this[name]();

for(var i=0;i<B.length;i++){var y=B[i];
if(z[y]==undefined){z[y]=A[y];
}if(A[y]<z[y]){z[y]=A[y];
}}}}if(z[n]!=undefined){return z;
}return {top:0,right:0,bottom:0,left:0};
}}});
})();
(function(){var q="qx.client",p="",o="boxSizing",n="box-sizing",m=":",k="border-box",j="qx.bom.element.BoxSizing",h="KhtmlBoxSizing",g="-moz-box-sizing",f="WebkitBoxSizing",c=";",e="-khtml-box-sizing",d="content-box",b="-webkit-box-sizing",a="MozBoxSizing";
qx.Class.define(j,{statics:{__eP:qx.core.Variant.select(q,{"mshtml":null,"webkit":[o,h,f],"gecko":[a],"opera":[o]}),__eQ:qx.core.Variant.select(q,{"mshtml":null,"webkit":[n,e,b],"gecko":[g],"opera":[n]}),__eR:{tags:{button:true,select:true},types:{search:true,button:true,submit:true,reset:true,checkbox:true,radio:true}},__eS:function(r){var s=this.__eR;
return s.tags[r.tagName.toLowerCase()]||s.types[r.type];
},compile:qx.core.Variant.select(q,{"mshtml":function(t){{};
},"default":function(u){var w=this.__eQ;
var v=p;

if(w){for(var i=0,l=w.length;i<l;i++){v+=w[i]+m+u+c;
}}return v;
}}),get:qx.core.Variant.select(q,{"mshtml":function(x){if(qx.bom.Document.isStandardMode(qx.dom.Node.getDocument(x))){if(!this.__eS(x)){return d;
}}return k;
},"default":function(y){var A=this.__eP;
var z;

if(A){for(var i=0,l=A.length;i<l;i++){z=qx.bom.element.Style.get(y,A[i],null,false);

if(z!=null&&z!==p){return z;
}}}return p;
}}),set:qx.core.Variant.select(q,{"mshtml":function(B,C){{};
},"default":function(D,E){var F=this.__eP;

if(F){for(var i=0,l=F.length;i<l;i++){D.style[F[i]]=E;
}}}}),reset:function(G){this.set(G,p);
}}});
})();
(function(){var k="",j="qx.client",i="hidden",h="-moz-scrollbars-none",g="overflow",f=";",e="overflowY",d=":",b="overflowX",a="overflow:",y="none",x="scroll",w="borderLeftStyle",v="borderRightStyle",u="div",r="borderRightWidth",q="overflow-y",p="borderLeftWidth",o="-moz-scrollbars-vertical",n="100px",l="qx.bom.element.Overflow",m="overflow-x";
qx.Class.define(l,{statics:{__eT:null,getScrollbarWidth:function(){if(this.__eT!==null){return this.__eT;
}var z=qx.bom.element.Style;
var B=function(F,G){return parseInt(z.get(F,G),10)||0;
};
var C=function(H){return (z.get(H,v)==y?0:B(H,r));
};
var A=function(I){return (z.get(I,w)==y?0:B(I,p));
};
var E=qx.core.Variant.select(j,{"mshtml":function(J){if(z.get(J,e)==i||J.clientWidth==0){return C(J);
}return Math.max(0,J.offsetWidth-J.clientLeft-J.clientWidth);
},"default":function(K){if(K.clientWidth==0){var L=z.get(K,g);
var M=(L==x||L==o?16:0);
return Math.max(0,C(K)+M);
}return Math.max(0,(K.offsetWidth-K.clientWidth-A(K)));
}});
var D=function(N){return E(N)-C(N);
};
var t=document.createElement(u);
var s=t.style;
s.height=s.width=n;
s.overflow=x;
document.body.appendChild(t);
var c=D(t);
this.__eT=c?c:16;
document.body.removeChild(t);
return this.__eT;
},_compile:qx.core.Variant.select(j,{"gecko":qx.bom.client.Engine.VERSION<
1.8?
function(O,P){if(P==i){P=h;
}return a+P+f;
}:
function(Q,R){return Q+d+R+f;
},"opera":qx.bom.client.Engine.VERSION<
9.5?
function(S,T){return a+T+f;
}:
function(U,V){return U+d+V+f;
},"default":function(W,X){return W+d+X+f;
}}),compileX:function(Y){return this._compile(m,Y);
},compileY:function(ba){return this._compile(q,ba);
},getX:qx.core.Variant.select(j,{"gecko":qx.bom.client.Engine.VERSION<
1.8?
function(bb,bc){var bd=qx.bom.element.Style.get(bb,g,bc,false);

if(bd===h){bd=i;
}return bd;
}:
function(be,bf){return qx.bom.element.Style.get(be,b,bf,false);
},"opera":qx.bom.client.Engine.VERSION<
9.5?
function(bg,bh){return qx.bom.element.Style.get(bg,g,bh,false);
}:
function(bi,bj){return qx.bom.element.Style.get(bi,b,bj,false);
},"default":function(bk,bl){return qx.bom.element.Style.get(bk,b,bl,false);
}}),setX:qx.core.Variant.select(j,{"gecko":qx.bom.client.Engine.VERSION<
1.8?
function(bm,bn){if(bn==i){bn=h;
}bm.style.overflow=bn;
}:
function(bo,bp){bo.style.overflowX=bp;
},"opera":qx.bom.client.Engine.VERSION<
9.5?
function(bq,br){bq.style.overflow=br;
}:
function(bs,bt){bs.style.overflowX=bt;
},"default":function(bu,bv){bu.style.overflowX=bv;
}}),resetX:qx.core.Variant.select(j,{"gecko":qx.bom.client.Engine.VERSION<
1.8?
function(bw){bw.style.overflow=k;
}:
function(bx){bx.style.overflowX=k;
},"opera":qx.bom.client.Engine.VERSION<
9.5?
function(by,bz){by.style.overflow=k;
}:
function(bA,bB){bA.style.overflowX=k;
},"default":function(bC){bC.style.overflowX=k;
}}),getY:qx.core.Variant.select(j,{"gecko":qx.bom.client.Engine.VERSION<
1.8?
function(bD,bE){var bF=qx.bom.element.Style.get(bD,g,bE,false);

if(bF===h){bF=i;
}return bF;
}:
function(bG,bH){return qx.bom.element.Style.get(bG,e,bH,false);
},"opera":qx.bom.client.Engine.VERSION<
9.5?
function(bI,bJ){return qx.bom.element.Style.get(bI,g,bJ,false);
}:
function(bK,bL){return qx.bom.element.Style.get(bK,e,bL,false);
},"default":function(bM,bN){return qx.bom.element.Style.get(bM,e,bN,false);
}}),setY:qx.core.Variant.select(j,{"gecko":qx.bom.client.Engine.VERSION<
1.8?
function(bO,bP){if(bP===i){bP=h;
}bO.style.overflow=bP;
}:
function(bQ,bR){bQ.style.overflowY=bR;
},"opera":qx.bom.client.Engine.VERSION<
9.5?
function(bS,bT){bS.style.overflow=bT;
}:
function(bU,bV){bU.style.overflowY=bV;
},"default":function(bW,bX){bW.style.overflowY=bX;
}}),resetY:qx.core.Variant.select(j,{"gecko":qx.bom.client.Engine.VERSION<
1.8?
function(bY){bY.style.overflow=k;
}:
function(ca){ca.style.overflowY=k;
},"opera":qx.bom.client.Engine.VERSION<
9.5?
function(cb,cc){cb.style.overflow=k;
}:
function(cd,ce){cd.style.overflowY=k;
},"default":function(cf){cf.style.overflowY=k;
}})}});
})();
(function(){var k="n-resize",j="e-resize",i="nw-resize",h="ne-resize",g="",f="cursor:",e="qx.client",d=";",c="qx.bom.element.Cursor",b="cursor",a="hand";
qx.Class.define(c,{statics:{__eU:qx.core.Variant.select(e,{"mshtml":{"cursor":a,"ew-resize":j,"ns-resize":k,"nesw-resize":h,"nwse-resize":i},"opera":{"col-resize":j,"row-resize":k,"ew-resize":j,"ns-resize":k,"nesw-resize":h,"nwse-resize":i},"default":{}}),compile:function(l){return f+(this.__eU[l]||l)+d;
},get:function(m,n){return qx.bom.element.Style.get(m,b,n,false);
},set:function(o,p){o.style.cursor=this.__eU[p]||p;
},reset:function(q){q.style.cursor=g;
}}});
})();
(function(){var o="auto",n="px",m=",",l="clip:auto;",k="rect(",j=");",i="",h=")",g="qx.bom.element.Clip",f="string",c="clip:rect(",e=" ",d="clip",b="rect(auto,auto,auto,auto)",a="rect(auto, auto, auto, auto)";
qx.Class.define(g,{statics:{compile:function(p){if(!p){return l;
}var u=p.left;
var top=p.top;
var t=p.width;
var s=p.height;
var q,r;

if(u==null){q=(t==null?o:t+n);
u=o;
}else{q=(t==null?o:u+t+n);
u=u+n;
}
if(top==null){r=(s==null?o:s+n);
top=o;
}else{r=(s==null?o:top+s+n);
top=top+n;
}return c+top+m+q+m+r+m+u+j;
},get:function(v,w){var y=qx.bom.element.Style.get(v,d,w,false);
var E,top,C,B;
var x,z;

if(typeof y===f&&y!==o&&y!==i){y=qx.lang.String.trim(y);
if(/\((.*)\)/.test(y)){var D=RegExp.$1;
if(/,/.test(D)){var A=D.split(m);
}else{var A=D.split(e);
}top=qx.lang.String.trim(A[0]);
x=qx.lang.String.trim(A[1]);
z=qx.lang.String.trim(A[2]);
E=qx.lang.String.trim(A[3]);
if(E===o){E=null;
}
if(top===o){top=null;
}
if(x===o){x=null;
}
if(z===o){z=null;
}if(top!=null){top=parseInt(top,10);
}
if(x!=null){x=parseInt(x,10);
}
if(z!=null){z=parseInt(z,10);
}
if(E!=null){E=parseInt(E,10);
}if(x!=null&&E!=null){C=x-E;
}else if(x!=null){C=x;
}
if(z!=null&&top!=null){B=z-top;
}else if(z!=null){B=z;
}}else{throw new Error("Could not parse clip string: "+y);
}}return {left:E||null,top:top||null,width:C||null,height:B||null};
},set:function(F,G){if(!G){F.style.clip=b;
return;
}var L=G.left;
var top=G.top;
var K=G.width;
var J=G.height;
var H,I;

if(L==null){H=(K==null?o:K+n);
L=o;
}else{H=(K==null?o:L+K+n);
L=L+n;
}
if(top==null){I=(J==null?o:J+n);
top=o;
}else{I=(J==null?o:top+J+n);
top=top+n;
}F.style.clip=k+top+m+H+m+I+m+L+h;
},reset:function(M){M.style.clip=a;
}}});
})();
(function(){var m="",l="qx.client",k=";",j="opacity:",i="opacity",h="filter",g="MozOpacity",f=");",e=")",d="zoom:1;filter:alpha(opacity=",a="qx.bom.element.Opacity",c="alpha(opacity=",b="-moz-opacity:";
qx.Class.define(a,{statics:{SUPPORT_CSS3_OPACITY:false,compile:qx.core.Variant.select(l,{"mshtml":function(n){if(n>=1){n=1;
}
if(n<0.00001){n=0;
}
if(qx.bom.element.Opacity.SUPPORT_CSS3_OPACITY){return j+n+k;
}else{return d+(n*100)+f;
}},"gecko":function(o){if(o>=1){o=0.999999;
}
if(!qx.bom.element.Opacity.SUPPORT_CSS3_OPACITY){return b+o+k;
}else{return j+o+k;
}},"default":function(p){if(p>=1){return m;
}return j+p+k;
}}),set:qx.core.Variant.select(l,{"mshtml":function(q,r){if(qx.bom.element.Opacity.SUPPORT_CSS3_OPACITY){if(r>=1){r=m;
}q.style.opacity=r;
}else{var s=qx.bom.element.Style.get(q,h,qx.bom.element.Style.COMPUTED_MODE,false);

if(r>=1){r=1;
}
if(r<0.00001){r=0;
}if(!q.currentStyle||!q.currentStyle.hasLayout){q.style.zoom=1;
}q.style.filter=s.replace(/alpha\([^\)]*\)/gi,m)+c+r*100+e;
}},"gecko":function(t,u){if(u>=1){u=0.999999;
}
if(!qx.bom.element.Opacity.SUPPORT_CSS3_OPACITY){t.style.MozOpacity=u;
}else{t.style.opacity=u;
}},"default":function(v,w){if(w>=1){w=m;
}v.style.opacity=w;
}}),reset:qx.core.Variant.select(l,{"mshtml":function(x){if(qx.bom.element.Opacity.SUPPORT_CSS3_OPACITY){x.style.opacity=m;
}else{var y=qx.bom.element.Style.get(x,h,qx.bom.element.Style.COMPUTED_MODE,false);
x.style.filter=y.replace(/alpha\([^\)]*\)/gi,m);
}},"gecko":function(z){if(!qx.bom.element.Opacity.SUPPORT_CSS3_OPACITY){z.style.MozOpacity=m;
}else{z.style.opacity=m;
}},"default":function(A){A.style.opacity=m;
}}),get:qx.core.Variant.select(l,{"mshtml":function(B,C){if(qx.bom.element.Opacity.SUPPORT_CSS3_OPACITY){var D=qx.bom.element.Style.get(B,i,C,false);

if(D!=null){return parseFloat(D);
}return 1.0;
}else{var E=qx.bom.element.Style.get(B,h,C,false);

if(E){var D=E.match(/alpha\(opacity=(.*)\)/);

if(D&&D[1]){return parseFloat(D[1])/100;
}}return 1.0;
}},"gecko":function(F,G){var H=qx.bom.element.Style.get(F,!qx.bom.element.Opacity.SUPPORT_CSS3_OPACITY?g:i,G,false);

if(H==0.999999){H=1.0;
}
if(H!=null){return parseFloat(H);
}return 1.0;
},"default":function(I,J){var K=qx.bom.element.Style.get(I,i,J,false);

if(K!=null){return parseFloat(K);
}return 1.0;
}})},defer:function(L){L.SUPPORT_CSS3_OPACITY=(typeof document.documentElement.style.opacity=="string");
}});
})();
(function(){var m="",k="qx.client",h="userSelect",g="style",f="MozUserModify",e="px",d="float",c="borderImage",b="styleFloat",a="appearance",F="pixelHeight",E='Ms',D=":",C="cssFloat",B="pixelTop",A="pixelLeft",z='O',y="qx.bom.element.Style",x='Khtml',w='string',t="pixelRight",u='Moz',r="pixelWidth",s="pixelBottom",p=";",q="textOverflow",n="userModify",o='Webkit',v="WebkitUserModify";
qx.Class.define(y,{statics:{__eV:function(){var G=[a,h,q,c];
var K={};
var H=document.documentElement.style;
var L=[u,o,x,z,E];

for(var i=0,l=G.length;i<l;i++){var M=G[i];
var I=M;

if(H[M]){K[I]=M;
continue;
}M=qx.lang.String.firstUp(M);

for(var j=0,N=L.length;j<N;j++){var J=L[j]+M;

if(typeof H[J]==w){K[I]=J;
break;
}}}this.__eW=K;
this.__eW[n]=qx.core.Variant.select(k,{"gecko":f,"webkit":v,"default":h});
this.__eX={};

for(var I in K){this.__eX[I]=this.__fc(K[I]);
}this.__eW[d]=qx.core.Variant.select(k,{"mshtml":b,"default":C});
},__eY:{width:r,height:F,left:A,right:t,top:B,bottom:s},__fa:{clip:qx.bom.element.Clip,cursor:qx.bom.element.Cursor,opacity:qx.bom.element.Opacity,boxSizing:qx.bom.element.BoxSizing,overflowX:{set:qx.lang.Function.bind(qx.bom.element.Overflow.setX,qx.bom.element.Overflow),get:qx.lang.Function.bind(qx.bom.element.Overflow.getX,qx.bom.element.Overflow),reset:qx.lang.Function.bind(qx.bom.element.Overflow.resetX,qx.bom.element.Overflow),compile:qx.lang.Function.bind(qx.bom.element.Overflow.compileX,qx.bom.element.Overflow)},overflowY:{set:qx.lang.Function.bind(qx.bom.element.Overflow.setY,qx.bom.element.Overflow),get:qx.lang.Function.bind(qx.bom.element.Overflow.getY,qx.bom.element.Overflow),reset:qx.lang.Function.bind(qx.bom.element.Overflow.resetY,qx.bom.element.Overflow),compile:qx.lang.Function.bind(qx.bom.element.Overflow.compileY,qx.bom.element.Overflow)}},compile:function(O){var Q=[];
var S=this.__fa;
var R=this.__eX;
var name,P;

for(name in O){P=O[name];

if(P==null){continue;
}name=R[name]||name;
if(S[name]){Q.push(S[name].compile(P));
}else{Q.push(this.__fc(name),D,P,p);
}}return Q.join(m);
},__fb:{},__fc:function(T){var U=this.__fb;
var V=U[T];

if(!V){V=U[T]=qx.lang.String.hyphenate(T);
}return V;
},setCss:qx.core.Variant.select(k,{"mshtml":function(W,X){W.style.cssText=X;
},"default":function(Y,ba){Y.setAttribute(g,ba);
}}),getCss:qx.core.Variant.select(k,{"mshtml":function(bb){return bb.style.cssText.toLowerCase();
},"default":function(bc){return bc.getAttribute(g);
}}),isPropertySupported:function(bd){return (this.__fa[bd]||this.__eW[bd]||bd in document.documentElement.style);
},COMPUTED_MODE:1,CASCADED_MODE:2,LOCAL_MODE:3,set:function(be,name,bf,bg){{};
name=this.__eW[name]||name;
if(bg!==false&&this.__fa[name]){return this.__fa[name].set(be,bf);
}else{be.style[name]=bf!==null?bf:m;
}},setStyles:function(bh,bi,bj){{};
var bm=this.__eW;
var bo=this.__fa;
var bk=bh.style;

for(var bn in bi){var bl=bi[bn];
var name=bm[bn]||bn;

if(bl===undefined){if(bj!==false&&bo[name]){bo[name].reset(bh);
}else{bk[name]=m;
}}else{if(bj!==false&&bo[name]){bo[name].set(bh,bl);
}else{bk[name]=bl!==null?bl:m;
}}}},reset:function(bp,name,bq){name=this.__eW[name]||name;
if(bq!==false&&this.__fa[name]){return this.__fa[name].reset(bp);
}else{bp.style[name]=m;
}},get:qx.core.Variant.select(k,{"mshtml":function(br,name,bs,bt){name=this.__eW[name]||name;
if(bt!==false&&this.__fa[name]){return this.__fa[name].get(br,bs);
}if(!br.currentStyle){return br.style[name]||m;
}switch(bs){case this.LOCAL_MODE:return br.style[name]||m;
case this.CASCADED_MODE:return br.currentStyle[name]||m;
default:var bx=br.currentStyle[name]||m;
if(/^-?[\.\d]+(px)?$/i.test(bx)){return bx;
}var bw=this.__eY[name];

if(bw){var bu=br.style[name];
br.style[name]=bx||0;
var bv=br.style[bw]+e;
br.style[name]=bu;
return bv;
}if(/^-?[\.\d]+(em|pt|%)?$/i.test(bx)){throw new Error("Untranslated computed property value: "+name+". Only pixel values work well across different clients.");
}return bx;
}},"default":function(by,name,bz,bA){name=this.__eW[name]||name;
if(bA!==false&&this.__fa[name]){return this.__fa[name].get(by,bz);
}switch(bz){case this.LOCAL_MODE:return by.style[name]||m;
case this.CASCADED_MODE:if(by.currentStyle){return by.currentStyle[name]||m;
}throw new Error("Cascaded styles are not supported in this browser!");
default:var bB=qx.dom.Node.getDocument(by);
var bC=bB.defaultView.getComputedStyle(by,null);
return bC?bC[name]:m;
}}})},defer:function(bD){bD.__eV();
}});
})();
(function(){var f="CSS1Compat",e="position:absolute;width:0;height:0;width:1",d="qx.bom.Document",c="1px",b="qx.client",a="div";
qx.Class.define(d,{statics:{isQuirksMode:qx.core.Variant.select(b,{"mshtml":function(g){if(qx.bom.client.Engine.VERSION>=8){return (g||window).document.documentMode===5;
}else{return (g||window).document.compatMode!==f;
}},"webkit":function(h){if(document.compatMode===undefined){var i=(h||window).document.createElement(a);
i.style.cssText=e;
return i.style.width===c?true:false;
}else{return (h||window).document.compatMode!==f;
}},"default":function(j){return (j||window).document.compatMode!==f;
}}),isStandardMode:function(k){return !this.isQuirksMode(k);
},getWidth:function(l){var m=(l||window).document;
var n=qx.bom.Viewport.getWidth(l);
var scroll=this.isStandardMode(l)?m.documentElement.scrollWidth:m.body.scrollWidth;
return Math.max(scroll,n);
},getHeight:function(o){var p=(o||window).document;
var q=qx.bom.Viewport.getHeight(o);
var scroll=this.isStandardMode(o)?p.documentElement.scrollHeight:p.body.scrollHeight;
return Math.max(scroll,q);
}}});
})();
(function(){var b="qx.client",a="qx.bom.Viewport";
qx.Class.define(a,{statics:{getWidth:qx.core.Variant.select(b,{"opera":function(c){if(qx.bom.client.Engine.VERSION<9.5){return (c||window).document.body.clientWidth;
}else{var d=(c||window).document;
return qx.bom.Document.isStandardMode(c)?d.documentElement.clientWidth:d.body.clientWidth;
}},"webkit":function(e){if(qx.bom.client.Engine.VERSION<523.15){return (e||window).innerWidth;
}else{var f=(e||window).document;
return qx.bom.Document.isStandardMode(e)?f.documentElement.clientWidth:f.body.clientWidth;
}},"default":function(g){var h=(g||window).document;
return qx.bom.Document.isStandardMode(g)?h.documentElement.clientWidth:h.body.clientWidth;
}}),getHeight:qx.core.Variant.select(b,{"opera":function(i){if(qx.bom.client.Engine.VERSION<9.5){return (i||window).document.body.clientHeight;
}else{var j=(i||window).document;
return qx.bom.Document.isStandardMode(i)?j.documentElement.clientHeight:j.body.clientHeight;
}},"webkit":function(k){if(qx.bom.client.Engine.VERSION<523.15){return (k||window).innerHeight;
}else{var l=(k||window).document;
return qx.bom.Document.isStandardMode(k)?l.documentElement.clientHeight:l.body.clientHeight;
}},"default":function(m){var n=(m||window).document;
return qx.bom.Document.isStandardMode(m)?n.documentElement.clientHeight:n.body.clientHeight;
}}),getScrollLeft:qx.core.Variant.select(b,{"mshtml":function(o){var p=(o||window).document;
return p.documentElement.scrollLeft||p.body.scrollLeft;
},"default":function(q){return (q||window).pageXOffset;
}}),getScrollTop:qx.core.Variant.select(b,{"mshtml":function(r){var s=(r||window).document;
return s.documentElement.scrollTop||s.body.scrollTop;
},"default":function(t){return (t||window).pageYOffset;
}}),getOrientation:function(u){var v=(u||window).orientation;

if(v==null){v=this.getWidth(u)>this.getHeight(u)?90:0;
}return v;
},isLandscape:function(w){return Math.abs(this.getOrientation(w))==90;
},isPortrait:function(x){var y=this.getOrientation(x);
return (y==0||y==180);
}}});
})();
(function(){var j="/",i="0",h="qx/static",g="http://",f="https://",e="file://",d="qx.util.AliasManager",c="singleton",b=".",a="static";
qx.Class.define(d,{type:c,extend:qx.util.ValueManager,construct:function(){qx.util.ValueManager.call(this);
this.__di={};
this.add(a,h);
},members:{__di:null,_preprocess:function(k){var n=this._getDynamic();

if(n[k]===false){return k;
}else if(n[k]===undefined){if(k.charAt(0)===j||k.charAt(0)===b||k.indexOf(g)===0||k.indexOf(f)===i||k.indexOf(e)===0){n[k]=false;
return k;
}
if(this.__di[k]){return this.__di[k];
}var m=k.substring(0,k.indexOf(j));
var l=this.__di[m];

if(l!==undefined){n[k]=l+k.substring(m.length);
}}return k;
},add:function(o,p){this.__di[o]=p;
var r=this._getDynamic();
for(var q in r){if(q.substring(0,q.indexOf(j))===o){r[q]=p+q.substring(o.length);
}}},remove:function(s){delete this.__di[s];
},resolve:function(t){var u=this._getDynamic();

if(t!=null){t=this._preprocess(t);
}return u[t]||t;
},getAliases:function(){var v={};

for(var w in this.__di){v[w]=this.__di[w];
}return v;
}},destruct:function(){this.__di=null;
}});
})();
(function(){var e="qx.theme.manager.Font",d="Theme",c="changeTheme",b="_applyTheme",a="singleton";
qx.Class.define(e,{type:a,extend:qx.util.ValueManager,properties:{theme:{check:d,nullable:true,apply:b,event:c}},members:{resolveDynamic:function(f){var g=this._dynamic;
return f instanceof qx.bom.Font?f:g[f];
},resolve:function(h){var k=this._dynamic;
var i=k[h];

if(i){return i;
}var j=this.getTheme();

if(j!==null&&j.fonts[h]){return k[h]=(new qx.bom.Font).set(j.fonts[h]);
}return h;
},isDynamic:function(l){var n=this._dynamic;

if(l&&(l instanceof qx.bom.Font||n[l]!==undefined)){return true;
}var m=this.getTheme();

if(m!==null&&l&&m.fonts[l]){n[l]=(new qx.bom.Font).set(m.fonts[l]);
return true;
}return false;
},__dj:function(o,p){if(o[p].include){var q=o[o[p].include];
o[p].include=null;
delete o[p].include;
o[p]=qx.lang.Object.mergeWith(o[p],q,false);
this.__dj(o,p);
}},_applyTheme:function(r){var s=this._getDynamic();

for(var v in s){if(s[v].themed){s[v].dispose();
delete s[v];
}}
if(r){var t=r.fonts;
var u=qx.bom.Font;

for(var v in t){if(t[v].include&&t[t[v].include]){this.__dj(t,v);
}s[v]=(new u).set(t[v]);
s[v].themed=true;
}}this._setDynamic(s);
}}});
})();
(function(){var k="",j="underline",h="Boolean",g="px",f='"',e="italic",d="normal",c="bold",b="_applyItalic",a="_applyBold",z="Integer",y="_applyFamily",x="_applyLineHeight",w="Array",v="line-through",u="overline",t="Color",s="qx.bom.Font",r="Number",q="_applyDecoration",o=" ",p="_applySize",m=",",n="_applyColor";
qx.Class.define(s,{extend:qx.core.Object,construct:function(A,B){qx.core.Object.call(this);

if(A!==undefined){this.setSize(A);
}
if(B!==undefined){this.setFamily(B);
}},statics:{fromString:function(C){var G=new qx.bom.Font();
var E=C.split(/\s+/);
var name=[];
var F;

for(var i=0;i<E.length;i++){switch(F=E[i]){case c:G.setBold(true);
break;
case e:G.setItalic(true);
break;
case j:G.setDecoration(j);
break;
default:var D=parseInt(F,10);

if(D==F||qx.lang.String.contains(F,g)){G.setSize(D);
}else{name.push(F);
}break;
}}
if(name.length>0){G.setFamily(name);
}return G;
},fromConfig:function(H){var I=new qx.bom.Font;
I.set(H);
return I;
},__dk:{fontFamily:k,fontSize:k,fontWeight:k,fontStyle:k,textDecoration:k,lineHeight:1.2,textColor:k},getDefaultStyles:function(){return this.__dk;
}},properties:{size:{check:z,nullable:true,apply:p},lineHeight:{check:r,nullable:true,apply:x},family:{check:w,nullable:true,apply:y},bold:{check:h,nullable:true,apply:a},italic:{check:h,nullable:true,apply:b},decoration:{check:[j,v,u],nullable:true,apply:q},color:{check:t,nullable:true,apply:n}},members:{__dl:null,__dm:null,__dn:null,__do:null,__dp:null,__dq:null,__tR:null,_applySize:function(J,K){this.__dl=J===null?null:J+g;
},_applyLineHeight:function(L,M){this.__dq=L===null?null:L;
},_applyFamily:function(N,O){var P=k;

for(var i=0,l=N.length;i<l;i++){if(N[i].indexOf(o)>0){P+=f+N[i]+f;
}else{P+=N[i];
}
if(i!==l-1){P+=m;
}}this.__dm=P;
},_applyBold:function(Q,R){this.__dn=Q===null?null:Q?c:d;
},_applyItalic:function(S,T){this.__do=S===null?null:S?e:d;
},_applyDecoration:function(U,V){this.__dp=U===null?null:U;
},_applyColor:function(W,X){this.__tR=W===null?null:W;
},getStyles:function(){return {fontFamily:this.__dm,fontSize:this.__dl,fontWeight:this.__dn,fontStyle:this.__do,textDecoration:this.__dp,lineHeight:this.__dq,textColor:this.__tR};
}}});
})();
(function(){var h="qx.bom.client.Feature",g="CSS1Compat",f="label",d="http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul",c="input",b="pointerEvents",a="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==";
qx.Bootstrap.define(h,{statics:{STANDARD_MODE:false,QUIRKS_MODE:false,CONTENT_BOX:false,BORDER_BOX:false,SVG:false,CANVAS:!!window.CanvasRenderingContext2D,VML:false,XPATH:!!document.evaluate,AIR:navigator.userAgent.indexOf("adobeair")!==-1,GEARS:!!(window.google&&window.google.gears),SSL:window.location.protocol==="https:",ECMA_OBJECT_COUNT:(({}).__count__==0),CSS_POINTER_EVENTS:false,XUL:false,CSS_TEXT_OVERFLOW:("textOverflow" in document.documentElement.style||"OTextOverflow" in document.documentElement.style),HTML5_CLASSLIST:!!(document.documentElement.classList&&qx.Bootstrap.getClass(document.documentElement.classList)==="DOMTokenList"),TOUCH:("ontouchstart" in window),PLACEHOLDER:false,DATA_URL:false,CSS_BORDER_RADIUS:("borderRadius" in document.documentElement.style||"MozBorderRadius" in document.documentElement.style||"WebkitBorderRadius" in document.documentElement.style),CSS_BOX_SHADOW:("BoxShadow" in document.documentElement.style||"MozBoxShadow" in document.documentElement.style||"WebkitBoxShadow" in document.documentElement.style),CSS_GRADIENTS:(function(){var j;

try{j=document.createElement("div");
}catch(l){j=document.createElement();
}var k=["-webkit-gradient(linear,0% 0%,100% 100%,from(white), to(red))","-moz-linear-gradient(0deg, white 0%, red 100%)","-o-linear-gradient(0deg, white 0%, red 100%)","linear-gradient(0deg, white 0%, red 100%)"];

for(var i=0;i<k.length;i++){try{j.style["background"]=k[i];

if(j.style["background"].indexOf("gradient")!=-1){return true;
}}catch(m){}}return false;
})(),WEB_WORKER:window.Worker!=null,GEO_LOCATION:navigator.geolocation!=null,AUDIO:window.Audio!=null,VIDEO:window.Video!=null,LOCAL_STORAGE:window.LocalStorage!=null,SESSION_STORAGE:window.SessionStorage!=null,__dr:function(){this.QUIRKS_MODE=this.__ds();
this.STANDARD_MODE=!this.QUIRKS_MODE;
this.CONTENT_BOX=!qx.bom.client.Engine.MSHTML||this.STANDARD_MODE;
this.BORDER_BOX=!this.CONTENT_BOX;
this.SVG=document.implementation&&document.implementation.hasFeature&&(document.implementation.hasFeature("org.w3c.dom.svg","1.0")||document.implementation.hasFeature("http://www.w3.org/TR/SVG11/feature#BasicStructure","1.1"));
this.VML=qx.bom.client.Engine.MSHTML;

try{document.createElementNS(d,f);
this.XUL=true;
}catch(e){this.XUL=false;
}var i=document.createElement(c);
this.PLACEHOLDER="placeholder" in i;
if(b in document.documentElement.style){if(qx.bom.client.Engine.OPERA){this.CSS_POINTER_EVENTS=false;
}else{this.CSS_POINTER_EVENTS=true;
}}var n=new Image();
n.onload=n.onerror=function(){if(n.width==1&&n.height==1){qx.bom.client.Feature.DATA_URL=true;
}};
n.src=a;
},__ds:function(){if(qx.bom.client.Engine.MSHTML&&qx.bom.client.Engine.VERSION>=8){return qx.bom.client.Engine.DOCUMENT_MODE===5;
}else{return document.compatMode!==g;
}}},defer:function(o){o.__dr();
}});
})();
(function(){var a="qx.lang.Object";
qx.Class.define(a,{statics:{empty:function(b){{};

for(var c in b){if(b.hasOwnProperty(c)){delete b[c];
}}},isEmpty:(qx.bom.client.Feature.ECMA_OBJECT_COUNT)?
function(d){{};
return d.__count__===0;
}:
function(e){{};

for(var f in e){return false;
}return true;
},hasMinLength:(qx.bom.client.Feature.ECMA_OBJECT_COUNT)?
function(g,h){{};
return g.__count__>=h;
}:
function(j,k){{};

if(k<=0){return true;
}var length=0;

for(var m in j){if((++length)>=k){return true;
}}return false;
},getLength:qx.Bootstrap.objectGetLength,getKeys:qx.Bootstrap.getKeys,getKeysAsString:qx.Bootstrap.getKeysAsString,getValues:function(n){{};
var p=[];
var o=this.getKeys(n);

for(var i=0,l=o.length;i<l;i++){p.push(n[o[i]]);
}return p;
},mergeWith:qx.Bootstrap.objectMergeWith,carefullyMergeWith:function(q,r){{};
return qx.lang.Object.mergeWith(q,r,false);
},merge:function(s,t){{};
var u=arguments.length;

for(var i=1;i<u;i++){qx.lang.Object.mergeWith(s,arguments[i]);
}return s;
},clone:function(v){{};
var w={};

for(var x in v){w[x]=v[x];
}return w;
},invert:function(y){{};
var z={};

for(var A in y){z[y[A].toString()]=A;
}return z;
},getKeyFromValue:function(B,C){{};

for(var D in B){if(B.hasOwnProperty(D)&&B[D]===C){return D;
}}return null;
},contains:function(E,F){{};
return this.getKeyFromValue(E,F)!==null;
},select:function(G,H){{};
return H[G];
},fromArray:function(I){{};
var J={};

for(var i=0,l=I.length;i<l;i++){{};
J[I[i].toString()]=true;
}return J;
}}});
})();
(function(){var e="qx.theme.manager.Icon",d="Theme",c="changeTheme",b="_applyTheme",a="singleton";
qx.Class.define(e,{type:a,extend:qx.core.Object,properties:{theme:{check:d,nullable:true,apply:b,event:c}},members:{_applyTheme:function(f,g){var i=qx.util.AliasManager.getInstance();

if(g){for(var h in g.aliases){i.remove(h);
}}
if(f){for(var h in f.aliases){i.add(h,f.aliases[h]);
}}}}});
})();
(function(){var h="string",g="_applyTheme",f="qx.theme.manager.Appearance",e=":",d="Theme",c="changeTheme",b="/",a="singleton";
qx.Class.define(f,{type:a,extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__dt={};
this.__du={};
},properties:{theme:{check:d,nullable:true,event:c,apply:g}},members:{__dv:{},__dt:null,__du:null,_applyTheme:function(j,k){this.__du={};
this.__dt={};
},__dw:function(l,m,n){var s=m.appearances;
var v=s[l];

if(!v){var w=b;
var p=[];
var u=l.split(w);
var t;

while(!v&&u.length>0){p.unshift(u.pop());
var q=u.join(w);
v=s[q];

if(v){t=v.alias||v;

if(typeof t===h){var r=t+w+p.join(w);
return this.__dw(r,m,n);
}}}for(var i=0;i<p.length-1;i++){p.shift();
var q=p.join(w);
var o=this.__dw(q,m);

if(o){return o;
}}if(n!=null){return this.__dw(n,m);
}return null;
}else if(typeof v===h){return this.__dw(v,m,n);
}else if(v.include&&!v.style){return this.__dw(v.include,m,n);
}return l;
},styleFrom:function(x,y,z,A){if(!z){z=this.getTheme();
}var F=this.__du;
var B=F[x];

if(!B){B=F[x]=this.__dw(x,z,A);
}var L=z.appearances[B];

if(!L){this.warn("Missing appearance: "+x);
return null;
}if(!L.style){return null;
}var M=B;

if(y){var N=L.$$bits;

if(!N){N=L.$$bits={};
L.$$length=0;
}var D=0;

for(var H in y){if(!y[H]){continue;
}
if(N[H]==null){N[H]=1<<L.$$length++;
}D+=N[H];
}if(D>0){M+=e+D;
}}var E=this.__dt;

if(E[M]!==undefined){return E[M];
}if(!y){y=this.__dv;
}var J;
if(L.include||L.base){var C;

if(L.include){C=this.styleFrom(L.include,y,z,A);
}var G=L.style(y,C);
J={};
if(L.base){var I=this.styleFrom(B,y,L.base,A);

if(L.include){for(var K in I){if(!C.hasOwnProperty(K)&&!G.hasOwnProperty(K)){J[K]=I[K];
}}}else{for(var K in I){if(!G.hasOwnProperty(K)){J[K]=I[K];
}}}}if(L.include){for(var K in C){if(!G.hasOwnProperty(K)){J[K]=C[K];
}}}for(var K in G){J[K]=G[K];
}}else{J=L.style(y);
}return E[M]=J||null;
}},destruct:function(){this.__dt=this.__du=null;
}});
})();
(function(){var p="other",o="widgets",n="fonts",m="appearances",k="qx.Theme",j="]",h="[Theme ",g="colors",f="decorations",e="Theme",b="meta",d="borders",c="icons";
qx.Bootstrap.define(k,{statics:{define:function(name,q){if(!q){var q={};
}q.include=this.__dx(q.include);
q.patch=this.__dx(q.patch);
{};
var r={$$type:e,name:name,title:q.title,toString:this.genericToString};
if(q.extend){r.supertheme=q.extend;
}r.basename=qx.Bootstrap.createNamespace(name,r);
this.__dA(r,q);
this.__dy(r,q);
this.$$registry[name]=r;
for(var i=0,a=q.include,l=a.length;i<l;i++){this.include(r,a[i]);
}
for(var i=0,a=q.patch,l=a.length;i<l;i++){this.patch(r,a[i]);
}},__dx:function(s){if(!s){return [];
}
if(qx.Bootstrap.isArray(s)){return s;
}else{return [s];
}},__dy:function(t,u){var v=u.aliases||{};

if(u.extend&&u.extend.aliases){qx.Bootstrap.objectMergeWith(v,u.extend.aliases,false);
}t.aliases=v;
},getAll:function(){return this.$$registry;
},getByName:function(name){return this.$$registry[name];
},isDefined:function(name){return this.getByName(name)!==undefined;
},getTotalNumber:function(){return qx.Bootstrap.objectGetLength(this.$$registry);
},genericToString:function(){return h+this.name+j;
},__dz:function(w){for(var i=0,x=this.__dB,l=x.length;i<l;i++){if(w[x[i]]){return x[i];
}}},__dA:function(y,z){var C=this.__dz(z);
if(z.extend&&!C){C=z.extend.type;
}y.type=C||p;
if(!C){return;
}var E=function(){};
if(z.extend){E.prototype=new z.extend.$$clazz;
}var D=E.prototype;
var B=z[C];
for(var A in B){D[A]=B[A];
if(D[A].base){{};
D[A].base=z.extend;
}}y.$$clazz=E;
y[C]=new E;
},$$registry:{},__dB:[g,d,f,n,c,o,m,b],__dC:null,__dD:null,__dE:function(){},patch:function(F,G){var I=this.__dz(G);

if(I!==this.__dz(F)){throw new Error("The mixins '"+F.name+"' are not compatible '"+G.name+"'!");
}var H=G[I];
var J=F.$$clazz.prototype;

for(var K in H){J[K]=H[K];
}},include:function(L,M){var O=M.type;

if(O!==L.type){throw new Error("The mixins '"+L.name+"' are not compatible '"+M.name+"'!");
}var N=M[O];
var P=L.$$clazz.prototype;

for(var Q in N){if(P[Q]!==undefined){continue;
}P[Q]=N[Q];
}}}});
})();
(function(){var p="Boolean",o="focusout",n="interval",m="mouseover",l="mouseout",k="mousemove",j="widget",i="qx.ui.tooltip.ToolTip",h="__dI",g="__dG",c="_applyCurrent",f="qx.ui.tooltip.Manager",d="__dF",b="tooltip-error",a="singleton";
qx.Class.define(f,{type:a,extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
qx.event.Registration.addListener(document.body,m,this.__dP,this,true);
this.__dF=new qx.event.Timer();
this.__dF.addListener(n,this.__dM,this);
this.__dG=new qx.event.Timer();
this.__dG.addListener(n,this.__dN,this);
this.__dH={left:0,top:0};
},properties:{current:{check:i,nullable:true,apply:c},showInvalidToolTips:{check:p,init:true},showToolTips:{check:p,init:true}},members:{__dH:null,__dG:null,__dF:null,__dI:null,__dJ:null,__dK:function(){if(!this.__dI){this.__dI=new qx.ui.tooltip.ToolTip().set({rich:true});
}return this.__dI;
},__dL:function(){if(!this.__dJ){this.__dJ=new qx.ui.tooltip.ToolTip().set({appearance:b});
this.__dJ.syncAppearance();
}return this.__dJ;
},_applyCurrent:function(q,r){if(r&&qx.ui.core.Widget.contains(r,q)){return;
}if(r){if(!r.isDisposed()){r.exclude();
}this.__dF.stop();
this.__dG.stop();
}var t=qx.event.Registration;
var s=document.body;
if(q){this.__dF.startWith(q.getShowTimeout());
t.addListener(s,l,this.__dQ,this,true);
t.addListener(s,o,this.__dR,this,true);
t.addListener(s,k,this.__dO,this,true);
}else{t.removeListener(s,l,this.__dQ,this,true);
t.removeListener(s,o,this.__dR,this,true);
t.removeListener(s,k,this.__dO,this,true);
}},__dM:function(e){var u=this.getCurrent();

if(u&&!u.isDisposed()){this.__dG.startWith(u.getHideTimeout());

if(u.getPlaceMethod()==j){u.placeToWidget(u.getOpener());
}else{u.placeToPoint(this.__dH);
}u.show();
}this.__dF.stop();
},__dN:function(e){var v=this.getCurrent();

if(v&&!v.isDisposed()){v.exclude();
}this.__dG.stop();
this.resetCurrent();
},__dO:function(e){var w=this.__dH;
w.left=e.getDocumentLeft();
w.top=e.getDocumentTop();
},__dP:function(e){var z=qx.ui.core.Widget.getWidgetByElement(e.getTarget());

if(!z){return;
}var A,B,y,x;
while(z!=null){A=z.getToolTip();
B=z.getToolTipText()||null;
y=z.getToolTipIcon()||null;

if(qx.Class.hasInterface(z.constructor,qx.ui.form.IForm)&&!z.isValid()){x=z.getInvalidMessage();
}
if(A||B||y||x){break;
}z=z.getLayoutParent();
}if(!z||
!z.getEnabled()||
z.isBlockToolTip()||
(!x&&!this.getShowToolTips())||(x&&!this.getShowInvalidToolTips())){return;
}
if(x){A=this.__dL().set({label:x});
}
if(!A){A=this.__dK().set({label:B,icon:y});
}this.setCurrent(A);
A.setOpener(z);
},__dQ:function(e){var C=qx.ui.core.Widget.getWidgetByElement(e.getTarget());

if(!C){return;
}var D=qx.ui.core.Widget.getWidgetByElement(e.getRelatedTarget());

if(!D){return;
}var E=this.getCurrent();
if(E&&(D==E||qx.ui.core.Widget.contains(E,D))){return;
}if(D&&C&&qx.ui.core.Widget.contains(C,D)){return;
}if(E&&!D){this.setCurrent(null);
}else{this.resetCurrent();
}},__dR:function(e){var F=qx.ui.core.Widget.getWidgetByElement(e.getTarget());

if(!F){return;
}var G=this.getCurrent();
if(G&&G==F.getToolTip()){this.setCurrent(null);
}}},destruct:function(){qx.event.Registration.removeListener(document.body,m,this.__dP,this,true);
this._disposeObjects(d,g,h);
this.__dH=null;
}});
})();
(function(){var h="interval",g="qx.event.Timer",f="_applyInterval",d="_applyEnabled",c="Boolean",b="qx.event.type.Event",a="Integer";
qx.Class.define(g,{extend:qx.core.Object,construct:function(i){qx.core.Object.call(this);
this.setEnabled(false);

if(i!=null){this.setInterval(i);
}var self=this;
this.__dS=function(){self._oninterval.call(self);
};
},events:{"interval":b},statics:{once:function(j,k,l){var m=new qx.event.Timer(l);
m.__dT=j;
m.addListener(h,function(e){m.stop();
j.call(k,e);
m.dispose();
k=null;
},k);
m.start();
return m;
}},properties:{enabled:{init:true,check:c,apply:d},interval:{check:a,init:1000,apply:f}},members:{__dU:null,__dS:null,_applyInterval:function(n,o){if(this.getEnabled()){this.restart();
}},_applyEnabled:function(p,q){if(q){window.clearInterval(this.__dU);
this.__dU=null;
}else if(p){this.__dU=window.setInterval(this.__dS,this.getInterval());
}},start:function(){this.setEnabled(true);
},startWith:function(r){this.setInterval(r);
this.start();
},stop:function(){this.setEnabled(false);
},restart:function(){this.stop();
this.start();
},restartWith:function(s){this.stop();
this.startWith(s);
},_oninterval:qx.event.GlobalError.observeMethod(function(){if(this.$$disposed){return;
}
if(this.getEnabled()){this.fireEvent(h);
}})},destruct:function(){if(this.__dU){window.clearInterval(this.__dU);
}this.__dU=this.__dS=null;
}});
})();
(function(){var j="Integer",i="interval",h="keep-align",g="disappear",f="best-fit",e="mouse",d="bottom-left",c="direct",b="Boolean",a="bottom-right",x="widget",w="qx.ui.core.MPlacement",v="left-top",u="offsetRight",t="shorthand",s="offsetLeft",r="top-left",q="appear",p="offsetBottom",o="top-right",m="offsetTop",n="right-bottom",k="right-top",l="left-bottom";
qx.Mixin.define(w,{statics:{__dV:null,setVisibleElement:function(y){this.__dV=y;
},getVisibleElement:function(){return this.__dV;
}},properties:{position:{check:[r,o,d,a,v,l,k,n],init:d,themeable:true},placeMethod:{check:[x,e],init:e,themeable:true},domMove:{check:b,init:false},placementModeX:{check:[c,h,f],init:h,themeable:true},placementModeY:{check:[c,h,f],init:h,themeable:true},offsetLeft:{check:j,init:0,themeable:true},offsetTop:{check:j,init:0,themeable:true},offsetRight:{check:j,init:0,themeable:true},offsetBottom:{check:j,init:0,themeable:true},offset:{group:[m,u,p,s],mode:t,themeable:true}},members:{__dW:null,__dX:null,__dY:null,getLayoutLocation:function(z){var C,B,D,top;
B=z.getBounds();
D=B.left;
top=B.top;
var E=B;
z=z.getLayoutParent();

while(z&&!z.isRootWidget()){B=z.getBounds();
D+=B.left;
top+=B.top;
C=z.getInsets();
D+=C.left;
top+=C.top;
z=z.getLayoutParent();
}if(z.isRootWidget()){var A=z.getContainerLocation();

if(A){D+=A.left;
top+=A.top;
}}return {left:D,top:top,right:D+E.width,bottom:top+E.height};
},moveTo:function(F,top){var H=qx.ui.core.MPlacement.getVisibleElement();
if(H){var J=this.getBounds();
var G=H.getContentLocation();
if(J&&G){var K=top+J.height;
var I=F+J.width;
if((I>G.left&&F<G.right)&&(K>G.top&&top<G.bottom)){F=Math.max(G.left-J.width,0);
}}}
if(this.getDomMove()){this.setDomPosition(F,top);
}else{this.setLayoutProperties({left:F,top:top});
}},placeToWidget:function(L,M){if(M){this.__ea();
this.__dW=qx.lang.Function.bind(this.placeToWidget,this,L,false);
qx.event.Idle.getInstance().addListener(i,this.__dW);
this.__dY=function(){this.__ea();
};
this.addListener(g,this.__dY,this);
}var N=L.getContainerLocation()||this.getLayoutLocation(L);
this.__ec(N);
},__ea:function(){if(this.__dW){qx.event.Idle.getInstance().removeListener(i,this.__dW);
this.__dW=null;
}
if(this.__dY){this.removeListener(g,this.__dY,this);
this.__dY=null;
}},placeToMouse:function(event){var P=event.getDocumentLeft();
var top=event.getDocumentTop();
var O={left:P,top:top,right:P,bottom:top};
this.__ec(O);
},placeToElement:function(Q,R){var location=qx.bom.element.Location.get(Q);
var S={left:location.left,top:location.top,right:location.left+Q.offsetWidth,bottom:location.top+Q.offsetHeight};
if(R){this.__dW=qx.lang.Function.bind(this.placeToElement,this,Q,false);
qx.event.Idle.getInstance().addListener(i,this.__dW);
this.addListener(g,function(){if(this.__dW){qx.event.Idle.getInstance().removeListener(i,this.__dW);
this.__dW=null;
}},this);
}this.__ec(S);
},placeToPoint:function(T){var U={left:T.left,top:T.top,right:T.left,bottom:T.top};
this.__ec(U);
},_getPlacementOffsets:function(){return {left:this.getOffsetLeft(),top:this.getOffsetTop(),right:this.getOffsetRight(),bottom:this.getOffsetBottom()};
},__eb:function(V){var W=null;

if(this._computePlacementSize){var W=this._computePlacementSize();
}else if(this.isVisible()){var W=this.getBounds();
}
if(W==null){this.addListenerOnce(q,function(){this.__eb(V);
},this);
}else{V.call(this,W);
}},__ec:function(X){this.__eb(function(Y){var ba=qx.util.placement.Placement.compute(Y,this.getLayoutParent().getBounds(),X,this._getPlacementOffsets(),this.getPosition(),this.getPlacementModeX(),this.getPlacementModeY());
this.moveTo(ba.left,ba.top);
});
}},destruct:function(){this.__ea();
}});
})();
(function(){var a="qx.ui.core.MChildrenHandling";
qx.Mixin.define(a,{members:{getChildren:function(){return this._getChildren();
},hasChildren:function(){return this._hasChildren();
},indexOf:function(b){return this._indexOf(b);
},add:function(c,d){this._add(c,d);
},addAt:function(e,f,g){this._addAt(e,f,g);
},addBefore:function(h,i,j){this._addBefore(h,i,j);
},addAfter:function(k,l,m){this._addAfter(k,l,m);
},remove:function(n){this._remove(n);
},removeAt:function(o){return this._removeAt(o);
},removeAll:function(){return this._removeAll();
}},statics:{remap:function(p){p.getChildren=p._getChildren;
p.hasChildren=p._hasChildren;
p.indexOf=p._indexOf;
p.add=p._add;
p.addAt=p._addAt;
p.addBefore=p._addBefore;
p.addAfter=p._addAfter;
p.remove=p._remove;
p.removeAt=p._removeAt;
p.removeAll=p._removeAll;
}}});
})();
(function(){var a="qx.ui.core.MLayoutHandling";
qx.Mixin.define(a,{members:{setLayout:function(b){return this._setLayout(b);
},getLayout:function(){return this._getLayout();
}},statics:{remap:function(c){c.getLayout=c._getLayout;
c.setLayout=c._setLayout;
}}});
})();
(function(){var j="Integer",i="_applyDimension",h="Boolean",g="_applyStretching",f="_applyMargin",e="shorthand",d="_applyAlign",c="allowShrinkY",b="bottom",a="baseline",x="marginBottom",w="qx.ui.core.LayoutItem",v="center",u="marginTop",t="allowGrowX",s="middle",r="marginLeft",q="allowShrinkX",p="top",o="right",m="marginRight",n="abstract",k="allowGrowY",l="left";
qx.Class.define(w,{type:n,extend:qx.core.Object,properties:{minWidth:{check:j,nullable:true,apply:i,init:null,themeable:true},width:{check:j,nullable:true,apply:i,init:null,themeable:true},maxWidth:{check:j,nullable:true,apply:i,init:null,themeable:true},minHeight:{check:j,nullable:true,apply:i,init:null,themeable:true},height:{check:j,nullable:true,apply:i,init:null,themeable:true},maxHeight:{check:j,nullable:true,apply:i,init:null,themeable:true},allowGrowX:{check:h,apply:g,init:true,themeable:true},allowShrinkX:{check:h,apply:g,init:true,themeable:true},allowGrowY:{check:h,apply:g,init:true,themeable:true},allowShrinkY:{check:h,apply:g,init:true,themeable:true},allowStretchX:{group:[t,q],mode:e,themeable:true},allowStretchY:{group:[k,c],mode:e,themeable:true},marginTop:{check:j,init:0,apply:f,themeable:true},marginRight:{check:j,init:0,apply:f,themeable:true},marginBottom:{check:j,init:0,apply:f,themeable:true},marginLeft:{check:j,init:0,apply:f,themeable:true},margin:{group:[u,m,x,r],mode:e,themeable:true},alignX:{check:[l,v,o],nullable:true,apply:d,themeable:true},alignY:{check:[p,s,b,a],nullable:true,apply:d,themeable:true}},members:{__ed:null,__ee:null,__ef:null,__eg:null,__eh:null,__ei:null,__ej:null,getBounds:function(){return this.__ei||this.__ee||null;
},clearSeparators:function(){},renderSeparator:function(y,z){},renderLayout:function(A,top,B,C){var D;
{};
var E=null;

if(this.getHeight()==null&&this._hasHeightForWidth()){var E=this._getHeightForWidth(B);
}
if(E!=null&&E!==this.__ed){this.__ed=E;
qx.ui.core.queue.Layout.add(this);
return null;
}var G=this.__ee;

if(!G){G=this.__ee={};
}var F={};

if(A!==G.left||top!==G.top){F.position=true;
G.left=A;
G.top=top;
}
if(B!==G.width||C!==G.height){F.size=true;
G.width=B;
G.height=C;
}if(this.__ef){F.local=true;
delete this.__ef;
}
if(this.__eh){F.margin=true;
delete this.__eh;
}return F;
},isExcluded:function(){return false;
},hasValidLayout:function(){return !this.__ef;
},scheduleLayoutUpdate:function(){qx.ui.core.queue.Layout.add(this);
},invalidateLayoutCache:function(){this.__ef=true;
this.__eg=null;
},getSizeHint:function(H){var I=this.__eg;

if(I){return I;
}
if(H===false){return null;
}I=this.__eg=this._computeSizeHint();
if(this._hasHeightForWidth()&&this.__ed&&this.getHeight()==null){I.height=this.__ed;
}if(I.minWidth>I.width){I.width=I.minWidth;
}
if(I.maxWidth<I.width){I.width=I.maxWidth;
}
if(!this.getAllowGrowX()){I.maxWidth=I.width;
}
if(!this.getAllowShrinkX()){I.minWidth=I.width;
}if(I.minHeight>I.height){I.height=I.minHeight;
}
if(I.maxHeight<I.height){I.height=I.maxHeight;
}
if(!this.getAllowGrowY()){I.maxHeight=I.height;
}
if(!this.getAllowShrinkY()){I.minHeight=I.height;
}return I;
},_computeSizeHint:function(){var N=this.getMinWidth()||0;
var K=this.getMinHeight()||0;
var O=this.getWidth()||N;
var M=this.getHeight()||K;
var J=this.getMaxWidth()||Infinity;
var L=this.getMaxHeight()||Infinity;
return {minWidth:N,width:O,maxWidth:J,minHeight:K,height:M,maxHeight:L};
},_hasHeightForWidth:function(){var P=this._getLayout();

if(P){return P.hasHeightForWidth();
}return false;
},_getHeightForWidth:function(Q){var R=this._getLayout();

if(R&&R.hasHeightForWidth()){return R.getHeightForWidth(Q);
}return null;
},_getLayout:function(){return null;
},_applyMargin:function(){this.__eh=true;
var parent=this.$$parent;

if(parent){parent.updateLayoutProperties();
}},_applyAlign:function(){var parent=this.$$parent;

if(parent){parent.updateLayoutProperties();
}},_applyDimension:function(){qx.ui.core.queue.Layout.add(this);
},_applyStretching:function(){qx.ui.core.queue.Layout.add(this);
},hasUserBounds:function(){return !!this.__ei;
},setUserBounds:function(S,top,T,U){this.__ei={left:S,top:top,width:T,height:U};
qx.ui.core.queue.Layout.add(this);
},resetUserBounds:function(){delete this.__ei;
qx.ui.core.queue.Layout.add(this);
},__ek:{},setLayoutProperties:function(V){if(V==null){return;
}var W=this.__ej;

if(!W){W=this.__ej={};
}var parent=this.getLayoutParent();

if(parent){parent.updateLayoutProperties(V);
}for(var X in V){if(V[X]==null){delete W[X];
}else{W[X]=V[X];
}}},getLayoutProperties:function(){return this.__ej||this.__ek;
},clearLayoutProperties:function(){delete this.__ej;
},updateLayoutProperties:function(Y){var ba=this._getLayout();

if(ba){var bb;
{};
ba.invalidateChildrenCache();
}qx.ui.core.queue.Layout.add(this);
},getApplicationRoot:function(){return qx.core.Init.getApplication().getRoot();
},getLayoutParent:function(){return this.$$parent||null;
},setLayoutParent:function(parent){if(this.$$parent===parent){return;
}this.$$parent=parent||null;
qx.ui.core.queue.Visibility.add(this);
},isRootWidget:function(){return false;
},_getRoot:function(){var parent=this;

while(parent){if(parent.isRootWidget()){return parent;
}parent=parent.$$parent;
}return null;
},clone:function(){var bc=qx.core.Object.prototype.clone.call(this);
var bd=this.__ej;

if(bd){bc.__ej=qx.lang.Object.clone(bd);
}return bc;
}},destruct:function(){this.$$parent=this.$$subparent=this.__ej=this.__ee=this.__ei=this.__eg=null;
}});
})();
(function(){var b="qx.ui.core.DecoratorFactory",a="$$nopool$$";
qx.Class.define(b,{extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__el={};
},statics:{MAX_SIZE:15,__em:a},members:{__el:null,getDecoratorElement:function(c){var h=qx.ui.core.DecoratorFactory;

if(qx.lang.Type.isString(c)){var f=c;
var e=qx.theme.manager.Decoration.getInstance().resolve(c);
}else{var f=h.__em;
e=c;
}var g=this.__el;

if(g[f]&&g[f].length>0){var d=g[f].pop();
}else{var d=this._createDecoratorElement(e,f);
}d.$$pooled=false;
return d;
},poolDecorator:function(i){if(!i||i.$$pooled||i.isDisposed()){return;
}var l=qx.ui.core.DecoratorFactory;
var j=i.getId();

if(j==l.__em){i.dispose();
return;
}var k=this.__el;

if(!k[j]){k[j]=[];
}
if(k[j].length>l.MAX_SIZE){i.dispose();
}else{i.$$pooled=true;
k[j].push(i);
}},_createDecoratorElement:function(m,n){var o=new qx.html.Decorator(m,n);
{};
return o;
},toString:function(){return qx.core.Object.prototype.toString.call(this);
}},destruct:function(){if(!qx.core.ObjectRegistry.inShutDown){var q=this.__el;

for(var p in q){qx.util.DisposeUtil.disposeArray(q,p);
}}this.__el=null;
}});
})();
(function(){var bW="px",bV="Boolean",bU="qx.event.type.Drag",bT="qx.event.type.Mouse",bS="visible",bR="qx.event.type.Focus",bQ="on",bP="Integer",bO="qx.event.type.Touch",bN="excluded",bx="qx.event.type.Data",bw="_applyPadding",bv="qx.event.type.Event",bu="hidden",bt="contextmenu",bs="String",br="tabIndex",bq="focused",bp="changeVisibility",bo="mshtml",ce="hovered",cf="qx.event.type.KeySequence",cc="qx.client",cd="absolute",ca="backgroundColor",cb="drag",bX="div",bY="disabled",cg="move",ch="dragstart",bG="qx.dynlocale",bF="dragchange",bI="dragend",bH="resize",bK="Decorator",bJ="zIndex",bM="opacity",bL="default",bE="Color",bD="changeToolTipText",c="beforeContextmenuOpen",d="_applyNativeContextMenu",f="_applyBackgroundColor",g="_applyFocusable",h="changeShadow",j="__es",k="qx.event.type.KeyInput",m="createChildControl",n="__ey",o="Font",cl="_applyShadow",ck="_applyEnabled",cj="_applySelectable",ci="Number",cp="_applyKeepActive",co="__er",cn="_applyVisibility",cm="repeat",cr="qxDraggable",cq="syncAppearance",N="paddingLeft",O="_applyDroppable",L="__eA",M="#",R="qx.event.type.MouseWheel",S="_applyCursor",P="_applyDraggable",Q="changeTextColor",J="$$widget",K="changeContextMenu",w="paddingTop",v="changeSelectable",y="hideFocus",x="none",s="outline",r="_applyAppearance",u="_applyOpacity",t="url(",q=")",p="qx.ui.core.Widget",X="_applyFont",Y="cursor",ba="qxDroppable",bb="__en",T="__ew",U="changeZIndex",V="changeEnabled",W="changeFont",bc="_applyDecorator",bd="_applyZIndex",G="_applyTextColor",F="qx.ui.menu.Menu",E="__eo",D="_applyToolTipText",C="true",B="widget",A="changeDecorator",z="_applyTabIndex",I="changeAppearance",H="shorthand",be="/",bf="",bg="_applyContextMenu",bh="paddingBottom",bi="changeNativeContextMenu",bj="undefined",bk="qx.ui.tooltip.ToolTip",bl="qxKeepActive",bm="_applyKeepFocus",bn="paddingRight",bB="changeBackgroundColor",bA="changeLocale",bz="qxKeepFocus",by="__et",bC="qx/static/blank.gif";
qx.Class.define(p,{extend:qx.ui.core.LayoutItem,include:[qx.locale.MTranslation],construct:function(){qx.ui.core.LayoutItem.call(this);
this.__en=this._createContainerElement();
this.__eo=this.__ez();
this.__en.add(this.__eo);
this.initFocusable();
this.initSelectable();
this.initNativeContextMenu();
},events:{appear:bv,disappear:bv,createChildControl:bx,resize:bx,move:bx,syncAppearance:bx,mousemove:bT,mouseover:bT,mouseout:bT,mousedown:bT,mouseup:bT,click:bT,dblclick:bT,contextmenu:bT,beforeContextmenuOpen:bx,mousewheel:R,touchstart:bO,touchend:bO,touchmove:bO,touchcancel:bO,tap:bO,swipe:bO,keyup:cf,keydown:cf,keypress:cf,keyinput:k,focus:bR,blur:bR,focusin:bR,focusout:bR,activate:bR,deactivate:bR,capture:bv,losecapture:bv,drop:bU,dragleave:bU,dragover:bU,drag:bU,dragstart:bU,dragend:bU,dragchange:bU,droprequest:bU},properties:{paddingTop:{check:bP,init:0,apply:bw,themeable:true},paddingRight:{check:bP,init:0,apply:bw,themeable:true},paddingBottom:{check:bP,init:0,apply:bw,themeable:true},paddingLeft:{check:bP,init:0,apply:bw,themeable:true},padding:{group:[w,bn,bh,N],mode:H,themeable:true},zIndex:{nullable:true,init:null,apply:bd,event:U,check:bP,themeable:true},decorator:{nullable:true,init:null,apply:bc,event:A,check:bK,themeable:true},shadow:{nullable:true,init:null,apply:cl,event:h,check:bK,themeable:true},backgroundColor:{nullable:true,check:bE,apply:f,event:bB,themeable:true},textColor:{nullable:true,check:bE,apply:G,event:Q,themeable:true,inheritable:true},font:{nullable:true,apply:X,check:o,event:W,themeable:true,inheritable:true,dereference:true},opacity:{check:ci,apply:u,themeable:true,nullable:true,init:null},cursor:{check:bs,apply:S,themeable:true,inheritable:true,nullable:true,init:null},toolTip:{check:bk,nullable:true},toolTipText:{check:bs,nullable:true,event:bD,apply:D},toolTipIcon:{check:bs,nullable:true,event:bD},blockToolTip:{check:bV,init:false},visibility:{check:[bS,bu,bN],init:bS,apply:cn,event:bp},enabled:{init:true,check:bV,inheritable:true,apply:ck,event:V},anonymous:{init:false,check:bV},tabIndex:{check:bP,nullable:true,apply:z},focusable:{check:bV,init:false,apply:g},keepFocus:{check:bV,init:false,apply:bm},keepActive:{check:bV,init:false,apply:cp},draggable:{check:bV,init:false,apply:P},droppable:{check:bV,init:false,apply:O},selectable:{check:bV,init:false,event:v,apply:cj},contextMenu:{check:F,apply:bg,nullable:true,event:K},nativeContextMenu:{check:bV,init:false,themeable:true,event:bi,apply:d},appearance:{check:bs,init:B,apply:r,event:I}},statics:{DEBUG:false,getWidgetByElement:function(cs,ct){while(cs){var cu=cs.$$widget;
if(cu!=null){var cv=qx.core.ObjectRegistry.fromHashCode(cu);
if(!ct||!cv.getAnonymous()){return cv;
}}try{cs=cs.parentNode;
}catch(e){return null;
}}return null;
},contains:function(parent,cw){while(cw){if(parent==cw){return true;
}cw=cw.getLayoutParent();
}return false;
},__ep:new qx.ui.core.DecoratorFactory(),__eq:new qx.ui.core.DecoratorFactory()},members:{__en:null,__eo:null,__er:null,__es:null,__et:null,__eu:null,__ev:null,__ew:null,_getLayout:function(){return this.__ew;
},_setLayout:function(cx){{};

if(this.__ew){this.__ew.connectToWidget(null);
}
if(cx){cx.connectToWidget(this);
}this.__ew=cx;
qx.ui.core.queue.Layout.add(this);
},setLayoutParent:function(parent){if(this.$$parent===parent){return;
}var cy=this.getContainerElement();

if(this.$$parent&&!this.$$parent.$$disposed){this.$$parent.getContentElement().remove(cy);
}this.$$parent=parent||null;

if(parent&&!parent.$$disposed){this.$$parent.getContentElement().add(cy);
}this.$$refreshInheritables();
qx.ui.core.queue.Visibility.add(this);
},_updateInsets:null,__ex:function(a,b){if(a==b){return false;
}
if(a==null||b==null){return true;
}var cz=qx.theme.manager.Decoration.getInstance();
var cB=cz.resolve(a).getInsets();
var cA=cz.resolve(b).getInsets();

if(cB.top!=cA.top||cB.right!=cA.right||cB.bottom!=cA.bottom||cB.left!=cA.left){return true;
}return false;
},renderLayout:function(cC,top,cD,cE){var cN=qx.ui.core.LayoutItem.prototype.renderLayout.call(this,cC,top,cD,cE);
if(!cN){return null;
}var cG=this.getContainerElement();
var content=this.getContentElement();
var cK=cN.size||this._updateInsets;
var cO=bW;
var cL={};
if(cN.position){cL.left=cC+cO;
cL.top=top+cO;
}if(cN.size){cL.width=cD+cO;
cL.height=cE+cO;
}
if(cN.position||cN.size){cG.setStyles(cL);
}
if(cK||cN.local||cN.margin){var cF=this.getInsets();
var innerWidth=cD-cF.left-cF.right;
var innerHeight=cE-cF.top-cF.bottom;
innerWidth=innerWidth<0?0:innerWidth;
innerHeight=innerHeight<0?0:innerHeight;
}var cI={};

if(this._updateInsets){cI.left=cF.left+cO;
cI.top=cF.top+cO;
}
if(cK){cI.width=innerWidth+cO;
cI.height=innerHeight+cO;
}
if(cK||this._updateInsets){content.setStyles(cI);
}
if(cN.size){var cM=this.__et;

if(cM){cM.setStyles({width:cD+bW,height:cE+bW});
}}
if(cN.size||this._updateInsets){if(this.__er){this.__er.resize(cD,cE);
}}
if(cN.size){if(this.__es){var cF=this.__es.getInsets();
var cJ=cD+cF.left+cF.right;
var cH=cE+cF.top+cF.bottom;
this.__es.resize(cJ,cH);
}}
if(cK||cN.local||cN.margin){if(this.__ew&&this.hasLayoutChildren()){this.__ew.renderLayout(innerWidth,innerHeight);
}else if(this.hasLayoutChildren()){throw new Error("At least one child in control "+this._findTopControl()+" requires a layout, but no one was defined!");
}}if(cN.position&&this.hasListener(cg)){this.fireDataEvent(cg,this.getBounds());
}
if(cN.size&&this.hasListener(bH)){this.fireDataEvent(bH,this.getBounds());
}delete this._updateInsets;
return cN;
},__ey:null,clearSeparators:function(){var cQ=this.__ey;

if(!cQ){return;
}var cR=qx.ui.core.Widget.__ep;
var content=this.getContentElement();
var cP;

for(var i=0,l=cQ.length;i<l;i++){cP=cQ[i];
cR.poolDecorator(cP);
content.remove(cP);
}cQ.length=0;
},renderSeparator:function(cS,cT){var cU=qx.ui.core.Widget.__ep.getDecoratorElement(cS);
this.getContentElement().add(cU);
cU.resize(cT.width,cT.height);
cU.setStyles({left:cT.left+bW,top:cT.top+bW});
if(!this.__ey){this.__ey=[cU];
}else{this.__ey.push(cU);
}},_computeSizeHint:function(){var dc=this.getWidth();
var db=this.getMinWidth();
var cW=this.getMaxWidth();
var da=this.getHeight();
var cX=this.getMinHeight();
var cY=this.getMaxHeight();
{};
var dd=this._getContentHint();
var cV=this.getInsets();
var df=cV.left+cV.right;
var de=cV.top+cV.bottom;

if(dc==null){dc=dd.width+df;
}
if(da==null){da=dd.height+de;
}
if(db==null){db=df;

if(dd.minWidth!=null){db+=dd.minWidth;
}}
if(cX==null){cX=de;

if(dd.minHeight!=null){cX+=dd.minHeight;
}}
if(cW==null){if(dd.maxWidth==null){cW=Infinity;
}else{cW=dd.maxWidth+df;
}}
if(cY==null){if(dd.maxHeight==null){cY=Infinity;
}else{cY=dd.maxHeight+de;
}}return {width:dc,minWidth:db,maxWidth:cW,height:da,minHeight:cX,maxHeight:cY};
},invalidateLayoutCache:function(){qx.ui.core.LayoutItem.prototype.invalidateLayoutCache.call(this);

if(this.__ew){this.__ew.invalidateLayoutCache();
}},_getContentHint:function(){var dh=this.__ew;

if(dh){if(this.hasLayoutChildren()){var dg;
var di=dh.getSizeHint();
{};
return di;
}else{return {width:0,height:0};
}}else{return {width:100,height:50};
}},_getHeightForWidth:function(dj){var dn=this.getInsets();
var dr=dn.left+dn.right;
var dq=dn.top+dn.bottom;
var dp=dj-dr;
var dl=this._getLayout();

if(dl&&dl.hasHeightForWidth()){var dk=dl.getHeightForWidth(dj);
}else{dk=this._getContentHeightForWidth(dp);
}var dm=dk+dq;
return dm;
},_getContentHeightForWidth:function(ds){throw new Error("Abstract method call: _getContentHeightForWidth()!");
},getInsets:function(){var top=this.getPaddingTop();
var du=this.getPaddingRight();
var dw=this.getPaddingBottom();
var dv=this.getPaddingLeft();

if(this.__er){var dt=this.__er.getInsets();
{};
top+=dt.top;
du+=dt.right;
dw+=dt.bottom;
dv+=dt.left;
}return {"top":top,"right":du,"bottom":dw,"left":dv};
},getInnerSize:function(){var dy=this.getBounds();

if(!dy){return null;
}var dx=this.getInsets();
return {width:dy.width-dx.left-dx.right,height:dy.height-dx.top-dx.bottom};
},show:function(){this.setVisibility(bS);
},hide:function(){this.setVisibility(bu);
},exclude:function(){this.setVisibility(bN);
},isVisible:function(){return this.getVisibility()===bS;
},isHidden:function(){return this.getVisibility()!==bS;
},isExcluded:function(){return this.getVisibility()===bN;
},isSeeable:function(){var dA=this.getContainerElement().getDomElement();

if(dA){return dA.offsetWidth>0;
}var dz=this;

do{if(!dz.isVisible()){return false;
}
if(dz.isRootWidget()){return true;
}dz=dz.getLayoutParent();
}while(dz);
return false;
},_createContainerElement:function(){var dC={"$$widget":this.toHashCode()};
{};
var dB={zIndex:0,position:cd};
return new qx.html.Element(bX,dB,dC);
},__ez:function(){var dD=this._createContentElement();
{};
dD.setStyles({"position":cd,"zIndex":10});
return dD;
},_createContentElement:function(){return new qx.html.Element(bX,{overflowX:bu,overflowY:bu});
},getContainerElement:function(){return this.__en;
},getContentElement:function(){return this.__eo;
},getDecoratorElement:function(){return this.__er||null;
},getShadowElement:function(){return this.__es||null;
},__eA:null,getLayoutChildren:function(){var dF=this.__eA;

if(!dF){return this.__eB;
}var dG;

for(var i=0,l=dF.length;i<l;i++){var dE=dF[i];

if(dE.hasUserBounds()||dE.isExcluded()){if(dG==null){dG=dF.concat();
}qx.lang.Array.remove(dG,dE);
}}return dG||dF;
},scheduleLayoutUpdate:function(){qx.ui.core.queue.Layout.add(this);
},invalidateLayoutChildren:function(){var dH=this.__ew;

if(dH){dH.invalidateChildrenCache();
}qx.ui.core.queue.Layout.add(this);
},hasLayoutChildren:function(){var dI=this.__eA;

if(!dI){return false;
}var dJ;

for(var i=0,l=dI.length;i<l;i++){dJ=dI[i];

if(!dJ.hasUserBounds()&&!dJ.isExcluded()){return true;
}}return false;
},getChildrenContainer:function(){return this;
},__eB:[],_getChildren:function(){return this.__eA||this.__eB;
},_indexOf:function(dK){var dL=this.__eA;

if(!dL){return -1;
}return dL.indexOf(dK);
},_hasChildren:function(){var dM=this.__eA;
return dM!=null&&(!!dM[0]);
},addChildrenToQueue:function(dN){var dO=this.__eA;

if(!dO){return;
}var dP;

for(var i=0,l=dO.length;i<l;i++){dP=dO[i];
dN[dP.$$hash]=dP;
dP.addChildrenToQueue(dN);
}},_add:function(dQ,dR){if(dQ.getLayoutParent()==this){qx.lang.Array.remove(this.__eA,dQ);
}
if(this.__eA){this.__eA.push(dQ);
}else{this.__eA=[dQ];
}this.__eC(dQ,dR);
},_addAt:function(dS,dT,dU){if(!this.__eA){this.__eA=[];
}if(dS.getLayoutParent()==this){qx.lang.Array.remove(this.__eA,dS);
}var dV=this.__eA[dT];

if(dV===dS){dS.setLayoutProperties(dU);
}
if(dV){qx.lang.Array.insertBefore(this.__eA,dS,dV);
}else{this.__eA.push(dS);
}this.__eC(dS,dU);
},_addBefore:function(dW,dX,dY){{};

if(dW==dX){return;
}
if(!this.__eA){this.__eA=[];
}if(dW.getLayoutParent()==this){qx.lang.Array.remove(this.__eA,dW);
}qx.lang.Array.insertBefore(this.__eA,dW,dX);
this.__eC(dW,dY);
},_addAfter:function(ea,eb,ec){{};

if(ea==eb){return;
}
if(!this.__eA){this.__eA=[];
}if(ea.getLayoutParent()==this){qx.lang.Array.remove(this.__eA,ea);
}qx.lang.Array.insertAfter(this.__eA,ea,eb);
this.__eC(ea,ec);
},_remove:function(ed){if(!this.__eA){throw new Error("This widget has no children!");
}qx.lang.Array.remove(this.__eA,ed);
this.__eD(ed);
},_removeAt:function(ee){if(!this.__eA){throw new Error("This widget has no children!");
}var ef=this.__eA[ee];
qx.lang.Array.removeAt(this.__eA,ee);
this.__eD(ef);
return ef;
},_removeAll:function(){if(!this.__eA){return [];
}var eg=this.__eA.concat();
this.__eA.length=0;

for(var i=eg.length-1;i>=0;i--){this.__eD(eg[i]);
}qx.ui.core.queue.Layout.add(this);
return eg;
},_afterAddChild:null,_afterRemoveChild:null,__eC:function(eh,ei){{};
var parent=eh.getLayoutParent();

if(parent&&parent!=this){parent._remove(eh);
}eh.setLayoutParent(this);
if(ei){eh.setLayoutProperties(ei);
}else{this.updateLayoutProperties();
}if(this._afterAddChild){this._afterAddChild(eh);
}},__eD:function(ej){{};

if(ej.getLayoutParent()!==this){throw new Error("Remove Error: "+ej+" is not a child of this widget!");
}ej.setLayoutParent(null);
if(this.__ew){this.__ew.invalidateChildrenCache();
}qx.ui.core.queue.Layout.add(this);
if(this._afterRemoveChild){this._afterRemoveChild(ej);
}},capture:function(ek){this.getContainerElement().capture(ek);
},releaseCapture:function(){this.getContainerElement().releaseCapture();
},_applyPadding:function(em,en,name){this._updateInsets=true;
qx.ui.core.queue.Layout.add(this);
},_createProtectorElement:function(){if(this.__et){return;
}var eo=this.__et=new qx.html.Element;
{};
eo.setStyles({position:cd,top:0,left:0,zIndex:7});
var ep=this.getBounds();

if(ep){this.__et.setStyles({width:ep.width+bW,height:ep.height+bW});
}if(qx.core.Variant.isSet(cc,bo)){eo.setStyles({backgroundImage:t+qx.util.ResourceManager.getInstance().toUri(bC)+q,backgroundRepeat:cm});
}this.getContainerElement().add(eo);
},_applyDecorator:function(eq,er){{};
var eu=qx.ui.core.Widget.__ep;
var es=this.getContainerElement();
if(!this.__et&&!qx.bom.client.Feature.CSS_POINTER_EVENTS){this._createProtectorElement();
}if(er){es.remove(this.__er);
eu.poolDecorator(this.__er);
}if(eq){var et=this.__er=eu.getDecoratorElement(eq);
et.setStyle(bJ,5);
es.add(et);
}else{delete this.__er;
}this._applyBackgroundColor(this.getBackgroundColor());
if(this.__ex(er,eq)){this._updateInsets=true;
qx.ui.core.queue.Layout.add(this);
}else if(eq){var ev=this.getBounds();

if(ev){et.resize(ev.width,ev.height);
this.__et&&
this.__et.setStyles({width:ev.width+bW,height:ev.height+bW});
}}},_applyShadow:function(ew,ex){var eE=qx.ui.core.Widget.__eq;
var ez=this.getContainerElement();
if(ex){ez.remove(this.__es);
eE.poolDecorator(this.__es);
}if(ew){var eB=this.__es=eE.getDecoratorElement(ew);
ez.add(eB);
var eD=eB.getInsets();
eB.setStyles({left:(-eD.left)+bW,top:(-eD.top)+bW});
var eC=this.getBounds();

if(eC){var eA=eC.width+eD.left+eD.right;
var ey=eC.height+eD.top+eD.bottom;
eB.resize(eA,ey);
}eB.tint(null);
}else{delete this.__es;
}},_applyToolTipText:function(eF,eG){if(qx.core.Variant.isSet(bG,bQ)){if(this.__ev){return;
}var eH=qx.locale.Manager.getInstance();
this.__ev=eH.addListener(bA,function(){var eI=this.getToolTipText();

if(eI&&eI.translate){this.setToolTipText(eI.translate());
}},this);
}},_applyTextColor:function(eJ,eK){},_applyZIndex:function(eL,eM){this.getContainerElement().setStyle(bJ,eL==null?0:eL);
},_applyVisibility:function(eN,eO){var eP=this.getContainerElement();

if(eN===bS){eP.show();
}else{eP.hide();
}var parent=this.$$parent;

if(parent&&(eO==null||eN==null||eO===bN||eN===bN)){parent.invalidateLayoutChildren();
}qx.ui.core.queue.Visibility.add(this);
},_applyOpacity:function(eQ,eR){this.getContainerElement().setStyle(bM,eQ==1?null:eQ);
if(qx.core.Variant.isSet(cc,bo)&&qx.bom.element.Decoration.isAlphaImageLoaderEnabled()){if(!qx.Class.isSubClassOf(this.getContentElement().constructor,qx.html.Image)){var eS=(eQ==1||eQ==null)?null:0.99;
this.getContentElement().setStyle(bM,eS);
}}},_applyCursor:function(eT,eU){if(eT==null&&!this.isSelectable()){eT=bL;
}this.getContainerElement().setStyle(Y,eT,qx.bom.client.Engine.OPERA);
},_applyBackgroundColor:function(eV,eW){var eX=this.getBackgroundColor();
var fa=this.getContainerElement();

if(this.__er){this.__er.tint(eX);
fa.setStyle(ca,null);
}else{var eY=qx.theme.manager.Color.getInstance().resolve(eX);
fa.setStyle(ca,eY);
}},_applyFont:function(fb,fc){},__eE:null,$$stateChanges:null,_forwardStates:null,hasState:function(fd){var fe=this.__eE;
return !!fe&&!!fe[fd];
},addState:function(ff){var fg=this.__eE;

if(!fg){fg=this.__eE={};
}
if(fg[ff]){return;
}this.__eE[ff]=true;
if(ff===ce){this.syncAppearance();
}else if(!qx.ui.core.queue.Visibility.isVisible(this)){this.$$stateChanges=true;
}else{qx.ui.core.queue.Appearance.add(this);
}var forward=this._forwardStates;
var fj=this.__eH;

if(forward&&forward[ff]&&fj){var fh;

for(var fi in fj){fh=fj[fi];

if(fh instanceof qx.ui.core.Widget){fj[fi].addState(ff);
}}}},removeState:function(fk){var fl=this.__eE;

if(!fl||!fl[fk]){return;
}delete this.__eE[fk];
if(fk===ce){this.syncAppearance();
}else if(!qx.ui.core.queue.Visibility.isVisible(this)){this.$$stateChanges=true;
}else{qx.ui.core.queue.Appearance.add(this);
}var forward=this._forwardStates;
var fo=this.__eH;

if(forward&&forward[fk]&&fo){for(var fn in fo){var fm=fo[fn];

if(fm instanceof qx.ui.core.Widget){fm.removeState(fk);
}}}},replaceState:function(fp,fq){var fr=this.__eE;

if(!fr){fr=this.__eE={};
}
if(!fr[fq]){fr[fq]=true;
}
if(fr[fp]){delete fr[fp];
}
if(!qx.ui.core.queue.Visibility.isVisible(this)){this.$$stateChanges=true;
}else{qx.ui.core.queue.Appearance.add(this);
}var forward=this._forwardStates;
var fu=this.__eH;

if(forward&&forward[fq]&&fu){for(var ft in fu){var fs=fu[ft];

if(fs instanceof qx.ui.core.Widget){fs.replaceState(fp,fq);
}}}},__eF:null,__eG:null,syncAppearance:function(){var fz=this.__eE;
var fy=this.__eF;
var fA=qx.theme.manager.Appearance.getInstance();
var fw=qx.core.Property.$$method.setThemed;
var fE=qx.core.Property.$$method.resetThemed;
if(this.__eG){delete this.__eG;
if(fy){var fv=fA.styleFrom(fy,fz,null,this.getAppearance());
fy=null;
}}if(!fy){var fx=this;
var fD=[];

do{fD.push(fx.$$subcontrol||fx.getAppearance());
}while(fx=fx.$$subparent);
fy=fD.reverse().join(be).replace(/#[0-9]+/g,bf);
this.__eF=fy;
}var fB=fA.styleFrom(fy,fz,null,this.getAppearance());

if(fB){var fC;

if(fv){for(var fC in fv){if(fB[fC]===undefined){this[fE[fC]]();
}}}{};
for(var fC in fB){fB[fC]===undefined?this[fE[fC]]():this[fw[fC]](fB[fC]);
}}else if(fv){for(var fC in fv){this[fE[fC]]();
}}this.fireDataEvent(cq,this.__eE);
},_applyAppearance:function(fF,fG){this.updateAppearance();
},checkAppearanceNeeds:function(){if(!this.__eu){qx.ui.core.queue.Appearance.add(this);
this.__eu=true;
}else if(this.$$stateChanges){qx.ui.core.queue.Appearance.add(this);
delete this.$$stateChanges;
}},updateAppearance:function(){this.__eG=true;
qx.ui.core.queue.Appearance.add(this);
var fJ=this.__eH;

if(fJ){var fH;

for(var fI in fJ){fH=fJ[fI];

if(fH instanceof qx.ui.core.Widget){fH.updateAppearance();
}}}},syncWidget:function(){},getEventTarget:function(){var fK=this;

while(fK.getAnonymous()){fK=fK.getLayoutParent();

if(!fK){return null;
}}return fK;
},getFocusTarget:function(){var fL=this;

if(!fL.getEnabled()){return null;
}
while(fL.getAnonymous()||!fL.getFocusable()){fL=fL.getLayoutParent();

if(!fL||!fL.getEnabled()){return null;
}}return fL;
},getFocusElement:function(){return this.getContainerElement();
},isTabable:function(){return (!!this.getContainerElement().getDomElement())&&this.isFocusable();
},_applyFocusable:function(fM,fN){var fO=this.getFocusElement();
if(fM){var fP=this.getTabIndex();

if(fP==null){fP=1;
}fO.setAttribute(br,fP);
if(qx.core.Variant.isSet(cc,bo)){fO.setAttribute(y,C);
}else{fO.setStyle(s,x);
}}else{if(fO.isNativelyFocusable()){fO.setAttribute(br,-1);
}else if(fN){fO.setAttribute(br,null);
}}},_applyKeepFocus:function(fQ){var fR=this.getFocusElement();
fR.setAttribute(bz,fQ?bQ:null);
},_applyKeepActive:function(fS){var fT=this.getContainerElement();
fT.setAttribute(bl,fS?bQ:null);
},_applyTabIndex:function(fU){if(fU==null){fU=1;
}else if(fU<1||fU>32000){throw new Error("TabIndex property must be between 1 and 32000");
}
if(this.getFocusable()&&fU!=null){this.getFocusElement().setAttribute(br,fU);
}},_applySelectable:function(fV,fW){if(fW!==null){this._applyCursor(this.getCursor());
}this.getContentElement().setSelectable(fV);
},_applyEnabled:function(fX,fY){if(fX===false){this.addState(bY);
this.removeState(ce);
if(this.isFocusable()){this.removeState(bq);
this._applyFocusable(false,true);
}if(this.isDraggable()){this._applyDraggable(false,true);
}if(this.isDroppable()){this._applyDroppable(false,true);
}}else{this.removeState(bY);
if(this.isFocusable()){this._applyFocusable(true,false);
}if(this.isDraggable()){this._applyDraggable(true,false);
}if(this.isDroppable()){this._applyDroppable(true,false);
}}},_applyNativeContextMenu:function(ga,gb,name){},_applyContextMenu:function(gc,gd){if(gd){gd.removeState(bt);

if(gd.getOpener()==this){gd.resetOpener();
}
if(!gc){this.removeListener(bt,this._onContextMenuOpen);
gd.removeListener(bp,this._onBeforeContextMenuOpen,this);
}}
if(gc){gc.setOpener(this);
gc.addState(bt);

if(!gd){this.addListener(bt,this._onContextMenuOpen);
gc.addListener(bp,this._onBeforeContextMenuOpen,this);
}}},_onContextMenuOpen:function(e){this.getContextMenu().openAtMouse(e);
e.stop();
},_onBeforeContextMenuOpen:function(e){if(e.getData()==bS&&this.hasListener(c)){this.fireDataEvent(c,e);
}},_onStopEvent:function(e){e.stopPropagation();
},_applyDraggable:function(ge,gf){if(!this.isEnabled()&&ge===true){ge=false;
}qx.ui.core.DragDropCursor.getInstance();
if(ge){this.addListener(ch,this._onDragStart);
this.addListener(cb,this._onDrag);
this.addListener(bI,this._onDragEnd);
this.addListener(bF,this._onDragChange);
}else{this.removeListener(ch,this._onDragStart);
this.removeListener(cb,this._onDrag);
this.removeListener(bI,this._onDragEnd);
this.removeListener(bF,this._onDragChange);
}this.getContainerElement().setAttribute(cr,ge?bQ:null);
},_applyDroppable:function(gg,gh){if(!this.isEnabled()&&gg===true){gg=false;
}this.getContainerElement().setAttribute(ba,gg?bQ:null);
},_onDragStart:function(e){qx.ui.core.DragDropCursor.getInstance().placeToMouse(e);
this.getApplicationRoot().setGlobalCursor(bL);
},_onDrag:function(e){qx.ui.core.DragDropCursor.getInstance().placeToMouse(e);
},_onDragEnd:function(e){qx.ui.core.DragDropCursor.getInstance().moveTo(-1000,-1000);
this.getApplicationRoot().resetGlobalCursor();
},_onDragChange:function(e){var gi=qx.ui.core.DragDropCursor.getInstance();
var gj=e.getCurrentAction();
gj?gi.setAction(gj):gi.resetAction();
},visualizeFocus:function(){this.addState(bq);
},visualizeBlur:function(){this.removeState(bq);
},scrollChildIntoView:function(gk,gl,gm,gn){gn=typeof gn==bj?true:gn;
var go=qx.ui.core.queue.Layout;
var parent;
if(gn){gn=!go.isScheduled(gk);
parent=gk.getLayoutParent();
if(gn&&parent){gn=!go.isScheduled(parent);
if(gn){parent.getChildren().forEach(function(gp){gn=gn&&!go.isScheduled(gp);
});
}}}this.scrollChildIntoViewX(gk,gl,gn);
this.scrollChildIntoViewY(gk,gm,gn);
},scrollChildIntoViewX:function(gq,gr,gs){this.getContentElement().scrollChildIntoViewX(gq.getContainerElement(),gr,gs);
},scrollChildIntoViewY:function(gt,gu,gv){this.getContentElement().scrollChildIntoViewY(gt.getContainerElement(),gu,gv);
},focus:function(){if(this.isFocusable()){this.getFocusElement().focus();
}else{throw new Error("Widget is not focusable!");
}},blur:function(){if(this.isFocusable()){this.getFocusElement().blur();
}else{throw new Error("Widget is not focusable!");
}},activate:function(){this.getContainerElement().activate();
},deactivate:function(){this.getContainerElement().deactivate();
},tabFocus:function(){this.getFocusElement().focus();
},hasChildControl:function(gw){if(!this.__eH){return false;
}return !!this.__eH[gw];
},__eH:null,_getCreatedChildControls:function(){return this.__eH;
},getChildControl:function(gx,gy){if(!this.__eH){if(gy){return null;
}this.__eH={};
}var gz=this.__eH[gx];

if(gz){return gz;
}
if(gy===true){return null;
}return this._createChildControl(gx);
},_showChildControl:function(gA){var gB=this.getChildControl(gA);
gB.show();
return gB;
},_excludeChildControl:function(gC){var gD=this.getChildControl(gC,true);

if(gD){gD.exclude();
}},_isChildControlVisible:function(gE){var gF=this.getChildControl(gE,true);

if(gF){return gF.isVisible();
}return false;
},_createChildControl:function(gG){if(!this.__eH){this.__eH={};
}else if(this.__eH[gG]){throw new Error("Child control '"+gG+"' already created!");
}var gK=gG.indexOf(M);

if(gK==-1){var gH=this._createChildControlImpl(gG);
}else{var gH=this._createChildControlImpl(gG.substring(0,gK),gG.substring(gK+1,gG.length));
}
if(!gH){throw new Error("Unsupported control: "+gG);
}gH.$$subcontrol=gG;
gH.$$subparent=this;
var gI=this.__eE;
var forward=this._forwardStates;

if(gI&&forward&&gH instanceof qx.ui.core.Widget){for(var gJ in gI){if(forward[gJ]){gH.addState(gJ);
}}}this.fireDataEvent(m,gH);
return this.__eH[gG]=gH;
},_createChildControlImpl:function(gL,gM){return null;
},_disposeChildControls:function(){var gQ=this.__eH;

if(!gQ){return;
}var gO=qx.ui.core.Widget;

for(var gP in gQ){var gN=gQ[gP];

if(!gO.contains(this,gN)){gN.destroy();
}else{gN.dispose();
}}delete this.__eH;
},_findTopControl:function(){var gR=this;

while(gR){if(!gR.$$subparent){return gR;
}gR=gR.$$subparent;
}return null;
},getContainerLocation:function(gS){var gT=this.getContainerElement().getDomElement();
return gT?qx.bom.element.Location.get(gT,gS):null;
},getContentLocation:function(gU){var gV=this.getContentElement().getDomElement();
return gV?qx.bom.element.Location.get(gV,gU):null;
},setDomLeft:function(gW){var gX=this.getContainerElement().getDomElement();

if(gX){gX.style.left=gW+bW;
}else{throw new Error("DOM element is not yet created!");
}},setDomTop:function(gY){var ha=this.getContainerElement().getDomElement();

if(ha){ha.style.top=gY+bW;
}else{throw new Error("DOM element is not yet created!");
}},setDomPosition:function(hb,top){var hc=this.getContainerElement().getDomElement();

if(hc){hc.style.left=hb+bW;
hc.style.top=top+bW;
}else{throw new Error("DOM element is not yet created!");
}},destroy:function(){if(this.$$disposed){return;
}var parent=this.$$parent;

if(parent){parent._remove(this);
}qx.ui.core.queue.Dispose.add(this);
},clone:function(){var hd=qx.ui.core.LayoutItem.prototype.clone.call(this);

if(this.getChildren){var he=this.getChildren();

for(var i=0,l=he.length;i<l;i++){hd.add(he[i].clone());
}}return hd;
}},destruct:function(){if(!qx.core.ObjectRegistry.inShutDown){if(qx.core.Variant.isSet(bG,bQ)){if(this.__ev){qx.locale.Manager.getInstance().removeListenerById(this.__ev);
}}this.getContainerElement().setAttribute(J,null,true);
this._disposeChildControls();
qx.ui.core.queue.Appearance.remove(this);
qx.ui.core.queue.Layout.remove(this);
qx.ui.core.queue.Visibility.remove(this);
qx.ui.core.queue.Widget.remove(this);
}if(!qx.core.ObjectRegistry.inShutDown){var hg=qx.ui.core.Widget;
var hf=this.getContainerElement();

if(this.__er){hf.remove(this.__er);
hg.__ep.poolDecorator(this.__er);
}
if(this.__es){hf.remove(this.__es);
hg.__eq.poolDecorator(this.__es);
}this.clearSeparators();
this.__er=this.__es=this.__ey=null;
}else{this._disposeArray(n);
this._disposeObjects(co,j);
}this._disposeArray(L);
this.__eE=this.__eH=null;
this._disposeObjects(T,bb,E,by);
}});
})();
(function(){var d="qx.event.type.Data",c="qx.ui.container.Composite",b="addChildWidget",a="removeChildWidget";
qx.Class.define(c,{extend:qx.ui.core.Widget,include:[qx.ui.core.MChildrenHandling,qx.ui.core.MLayoutHandling],construct:function(e){qx.ui.core.Widget.call(this);

if(e!=null){this._setLayout(e);
}},events:{addChildWidget:d,removeChildWidget:d},members:{_afterAddChild:function(f){this.fireNonBubblingEvent(b,qx.event.type.Data,[f]);
},_afterRemoveChild:function(g){this.fireNonBubblingEvent(a,qx.event.type.Data,[g]);
}},defer:function(h,i){qx.ui.core.MChildrenHandling.remap(i);
qx.ui.core.MLayoutHandling.remap(i);
}});
})();
(function(){var e="qx.ui.popup.Popup",d="visible",c="excluded",b="popup",a="Boolean";
qx.Class.define(e,{extend:qx.ui.container.Composite,include:qx.ui.core.MPlacement,construct:function(f){qx.ui.container.Composite.call(this,f);
qx.core.Init.getApplication().getRoot().add(this);
this.initVisibility();
},properties:{appearance:{refine:true,init:b},visibility:{refine:true,init:c},autoHide:{check:a,init:true}},members:{_applyVisibility:function(g,h){qx.ui.container.Composite.prototype._applyVisibility.call(this,g,h);
var i=qx.ui.popup.Manager.getInstance();
g===d?i.add(this):i.remove(this);
}},destruct:function(){qx.ui.popup.Manager.getInstance().remove(this);
}});
})();
(function(){var l="atom",k="Integer",j="String",i="_applyRich",h="qx.ui.tooltip.ToolTip",g="_applyIcon",f="tooltip",d="qx.ui.core.Widget",c="mouseover",b="Boolean",a="_applyLabel";
qx.Class.define(h,{extend:qx.ui.popup.Popup,construct:function(m,n){qx.ui.popup.Popup.call(this);
this.setLayout(new qx.ui.layout.Grow);
this._createChildControl(l);
if(m!=null){this.setLabel(m);
}
if(n!=null){this.setIcon(n);
}this.addListener(c,this._onMouseOver,this);
},properties:{appearance:{refine:true,init:f},showTimeout:{check:k,init:700,themeable:true},hideTimeout:{check:k,init:4000,themeable:true},label:{check:j,nullable:true,apply:a},icon:{check:j,nullable:true,apply:g,themeable:true},rich:{check:b,init:false,apply:i},opener:{check:d,nullable:true}},members:{_createChildControlImpl:function(o,p){var q;

switch(o){case l:q=new qx.ui.basic.Atom;
this._add(q);
break;
}return q||qx.ui.popup.Popup.prototype._createChildControlImpl.call(this,o);
},_onMouseOver:function(e){this.hide();
},_applyIcon:function(r,s){var t=this.getChildControl(l);
r==null?t.resetIcon():t.setIcon(r);
},_applyLabel:function(u,v){var w=this.getChildControl(l);
u==null?w.resetLabel():w.setLabel(u);
},_applyRich:function(x,y){var z=this.getChildControl(l);
z.setRich(x);
}}});
})();
(function(){var f="interval",e="Number",d="_applyTimeoutInterval",c="qx.event.type.Event",b="qx.event.Idle",a="singleton";
qx.Class.define(b,{extend:qx.core.Object,type:a,construct:function(){qx.core.Object.call(this);
var g=new qx.event.Timer(this.getTimeoutInterval());
g.addListener(f,this._onInterval,this);
g.start();
this.__eI=g;
},events:{"interval":c},properties:{timeoutInterval:{check:e,init:100,apply:d}},members:{__eI:null,_applyTimeoutInterval:function(h){this.__eI.setInterval(h);
},_onInterval:function(){this.fireEvent(f);
}},destruct:function(){if(this.__eI){this.__eI.stop();
}this.__eI=null;
}});
})();
(function(){var j="borderTopWidth",i="borderLeftWidth",h="marginTop",g="marginLeft",f="scroll",e="qx.client",d="border-box",c="borderBottomWidth",b="borderRightWidth",a="auto",y="padding",x="qx.bom.element.Location",w="paddingLeft",v="static",u="marginBottom",t="visible",s="BODY",r="paddingBottom",q="paddingTop",p="marginRight",n="position",o="margin",l="overflow",m="paddingRight",k="border";
qx.Class.define(x,{statics:{__eJ:function(z,A){return qx.bom.element.Style.get(z,A,qx.bom.element.Style.COMPUTED_MODE,false);
},__eK:function(B,C){return parseInt(qx.bom.element.Style.get(B,C,qx.bom.element.Style.COMPUTED_MODE,false),10)||0;
},__eL:function(D){var G=0,top=0;
if(D.getBoundingClientRect&&!qx.bom.client.Engine.OPERA){var F=qx.dom.Node.getWindow(D);
G-=qx.bom.Viewport.getScrollLeft(F);
top-=qx.bom.Viewport.getScrollTop(F);
}else{var E=qx.dom.Node.getDocument(D).body;
D=D.parentNode;
while(D&&D!=E){G+=D.scrollLeft;
top+=D.scrollTop;
D=D.parentNode;
}}return {left:G,top:top};
},__eM:qx.core.Variant.select(e,{"mshtml":function(H){var J=qx.dom.Node.getDocument(H);
var I=J.body;
var K=0;
var top=0;
K-=I.clientLeft+J.documentElement.clientLeft;
top-=I.clientTop+J.documentElement.clientTop;

if(qx.bom.client.Feature.STANDARD_MODE){K+=this.__eK(I,i);
top+=this.__eK(I,j);
}return {left:K,top:top};
},"webkit":function(L){var N=qx.dom.Node.getDocument(L);
var M=N.body;
var O=M.offsetLeft;
var top=M.offsetTop;
if(qx.bom.client.Engine.VERSION<530.17){O+=this.__eK(M,i);
top+=this.__eK(M,j);
}return {left:O,top:top};
},"gecko":function(P){var Q=qx.dom.Node.getDocument(P).body;
var R=Q.offsetLeft;
var top=Q.offsetTop;
if(qx.bom.client.Engine.VERSION<1.9){R+=this.__eK(Q,g);
top+=this.__eK(Q,h);
}if(qx.bom.element.BoxSizing.get(Q)!==d){R+=this.__eK(Q,i);
top+=this.__eK(Q,j);
}return {left:R,top:top};
},"default":function(S){var T=qx.dom.Node.getDocument(S).body;
var U=T.offsetLeft;
var top=T.offsetTop;
return {left:U,top:top};
}}),__eN:qx.core.Variant.select(e,{"mshtml|webkit":function(V){var X=qx.dom.Node.getDocument(V);
if(V.getBoundingClientRect){var Y=V.getBoundingClientRect();
var ba=Y.left;
var top=Y.top;
}else{var ba=V.offsetLeft;
var top=V.offsetTop;
V=V.offsetParent;
var W=X.body;
while(V&&V!=W){ba+=V.offsetLeft;
top+=V.offsetTop;
ba+=this.__eK(V,i);
top+=this.__eK(V,j);
V=V.offsetParent;
}}return {left:ba,top:top};
},"gecko":function(bb){if(bb.getBoundingClientRect){var be=bb.getBoundingClientRect();
var bf=Math.round(be.left);
var top=Math.round(be.top);
}else{var bf=0;
var top=0;
var bc=qx.dom.Node.getDocument(bb).body;
var bd=qx.bom.element.BoxSizing;

if(bd.get(bb)!==d){bf-=this.__eK(bb,i);
top-=this.__eK(bb,j);
}
while(bb&&bb!==bc){bf+=bb.offsetLeft;
top+=bb.offsetTop;
if(bd.get(bb)!==d){bf+=this.__eK(bb,i);
top+=this.__eK(bb,j);
}if(bb.parentNode&&this.__eJ(bb.parentNode,l)!=t){bf+=this.__eK(bb.parentNode,i);
top+=this.__eK(bb.parentNode,j);
}bb=bb.offsetParent;
}}return {left:bf,top:top};
},"default":function(bg){var bi=0;
var top=0;
var bh=qx.dom.Node.getDocument(bg).body;
while(bg&&bg!==bh){bi+=bg.offsetLeft;
top+=bg.offsetTop;
bg=bg.offsetParent;
}return {left:bi,top:top};
}}),get:function(bj,bk){if(bj.tagName==s){var location=this.__eO(bj);
var br=location.left;
var top=location.top;
}else{var bl=this.__eM(bj);
var bq=this.__eN(bj);
var scroll=this.__eL(bj);
var br=bq.left+bl.left-scroll.left;
var top=bq.top+bl.top-scroll.top;
}var bm=br+bj.offsetWidth;
var bn=top+bj.offsetHeight;

if(bk){if(bk==y||bk==f){var bo=qx.bom.element.Overflow.getX(bj);

if(bo==f||bo==a){bm+=bj.scrollWidth-bj.offsetWidth+this.__eK(bj,i)+this.__eK(bj,b);
}var bp=qx.bom.element.Overflow.getY(bj);

if(bp==f||bp==a){bn+=bj.scrollHeight-bj.offsetHeight+this.__eK(bj,j)+this.__eK(bj,c);
}}
switch(bk){case y:br+=this.__eK(bj,w);
top+=this.__eK(bj,q);
bm-=this.__eK(bj,m);
bn-=this.__eK(bj,r);
case f:br-=bj.scrollLeft;
top-=bj.scrollTop;
bm-=bj.scrollLeft;
bn-=bj.scrollTop;
case k:br+=this.__eK(bj,i);
top+=this.__eK(bj,j);
bm-=this.__eK(bj,b);
bn-=this.__eK(bj,c);
break;
case o:br-=this.__eK(bj,g);
top-=this.__eK(bj,h);
bm+=this.__eK(bj,p);
bn+=this.__eK(bj,u);
break;
}}return {left:br,top:top,right:bm,bottom:bn};
},__eO:qx.core.Variant.select(e,{"default":function(bs){var top=bs.offsetTop+this.__eK(bs,h);
var bt=bs.offsetLeft+this.__eK(bs,g);
return {left:bt,top:top};
},"mshtml":function(bu){var top=bu.offsetTop;
var bv=bu.offsetLeft;

if(!((qx.bom.client.Engine.VERSION<8||qx.bom.client.Engine.DOCUMENT_MODE<8)&&!qx.bom.client.Feature.QUIRKS_MODE)){top+=this.__eK(bu,h);
bv+=this.__eK(bu,g);
}return {left:bv,top:top};
},"gecko":function(bw){var top=bw.offsetTop+this.__eK(bw,h)+this.__eK(bw,i);
var bx=bw.offsetLeft+this.__eK(bw,g)+this.__eK(bw,j);
return {left:bx,top:top};
}}),getLeft:function(by,bz){return this.get(by,bz).left;
},getTop:function(bA,bB){return this.get(bA,bB).top;
},getRight:function(bC,bD){return this.get(bC,bD).right;
},getBottom:function(bE,bF){return this.get(bE,bF).bottom;
},getRelative:function(bG,bH,bI,bJ){var bL=this.get(bG,bI);
var bK=this.get(bH,bJ);
return {left:bL.left-bK.left,top:bL.top-bK.top,right:bL.right-bK.right,bottom:bL.bottom-bK.bottom};
},getPosition:function(bM){return this.getRelative(bM,this.getOffsetParent(bM));
},getOffsetParent:function(bN){var bP=bN.offsetParent||document.body;
var bO=qx.bom.element.Style;

while(bP&&(!/^body|html$/i.test(bP.tagName)&&bO.get(bP,n)===v)){bP=bP.offsetParent;
}return bP;
}}});
})();
(function(){var o="top",n="right",m="bottom",l="left",k="align-start",j="qx.util.placement.AbstractAxis",i="edge-start",h="align-end",g="edge-end",f="-",c="best-fit",e='__fd',d="qx.util.placement.Placement",b="keep-align",a="direct";
qx.Class.define(d,{extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__fd=new qx.util.placement.DirectAxis();
},properties:{axisX:{check:j},axisY:{check:j},edge:{check:[o,n,m,l],init:o},align:{check:[o,n,m,l],init:n}},statics:{__fe:null,compute:function(p,q,r,s,t,u,v){this.__fe=this.__fe||new qx.util.placement.Placement();
var y=t.split(f);
var x=y[0];
var w=y[1];
this.__fe.set({axisX:this.__fi(u),axisY:this.__fi(v),edge:x,align:w});
return this.__fe.compute(p,q,r,s);
},__ff:null,__fg:null,__fh:null,__fi:function(z){switch(z){case a:this.__ff=this.__ff||new qx.util.placement.DirectAxis();
return this.__ff;
case b:this.__fg=this.__fg||new qx.util.placement.KeepAlignAxis();
return this.__fg;
case c:this.__fh=this.__fh||new qx.util.placement.BestFitAxis();
return this.__fh;
default:throw new Error("Invalid 'mode' argument!'");
}}},members:{__fd:null,compute:function(A,B,C,D){{};
var E=this.getAxisX()||this.__fd;
var G=E.computeStart(A.width,{start:C.left,end:C.right},{start:D.left,end:D.right},B.width,this.__fj());
var F=this.getAxisY()||this.__fd;
var top=F.computeStart(A.height,{start:C.top,end:C.bottom},{start:D.top,end:D.bottom},B.height,this.__fk());
return {left:G,top:top};
},__fj:function(){var I=this.getEdge();
var H=this.getAlign();

if(I==l){return i;
}else if(I==n){return g;
}else if(H==l){return k;
}else if(H==n){return h;
}},__fk:function(){var K=this.getEdge();
var J=this.getAlign();

if(K==o){return i;
}else if(K==m){return g;
}else if(J==o){return k;
}else if(J==m){return h;
}}},destruct:function(){this._disposeObjects(e);
}});
})();
(function(){var e="edge-start",d="align-start",c="align-end",b="edge-end",a="qx.util.placement.AbstractAxis";
qx.Class.define(a,{extend:qx.core.Object,members:{computeStart:function(f,g,h,i,j){throw new Error("abstract method call!");
},_moveToEdgeAndAlign:function(k,l,m,n){switch(n){case e:return l.start-m.end-k;
case b:return l.end+m.start;
case d:return l.start+m.start;
case c:return l.end-m.end-k;
}},_isInRange:function(o,p,q){return o>=0&&o+p<=q;
}}});
})();
(function(){var a="qx.util.placement.DirectAxis";
qx.Class.define(a,{extend:qx.util.placement.AbstractAxis,members:{computeStart:function(b,c,d,e,f){return this._moveToEdgeAndAlign(b,c,d,f);
}}});
})();
(function(){var c="qx.util.placement.KeepAlignAxis",b="edge-start",a="edge-end";
qx.Class.define(c,{extend:qx.util.placement.AbstractAxis,members:{computeStart:function(d,e,f,g,h){var i=this._moveToEdgeAndAlign(d,e,f,h);
var j,k;

if(this._isInRange(i,d,g)){return i;
}
if(h==b||h==a){j=e.start-f.end;
k=e.end+f.start;
}else{j=e.end-f.end;
k=e.start+f.start;
}
if(j>g-k){i=j-d;
}else{i=k;
}return i;
}}});
})();
(function(){var a="qx.util.placement.BestFitAxis";
qx.Class.define(a,{extend:qx.util.placement.AbstractAxis,members:{computeStart:function(b,c,d,e,f){var g=this._moveToEdgeAndAlign(b,c,d,f);

if(this._isInRange(g,b,e)){return g;
}
if(g<0){g=Math.min(0,e-b);
}
if(g+b>e){g=Math.max(0,e-b);
}return g;
}}});
})();
(function(){var b="qx.ui.core.queue.Layout",a="layout";
qx.Class.define(b,{statics:{__fl:{},remove:function(c){delete this.__fl[c.$$hash];
},add:function(d){this.__fl[d.$$hash]=d;
qx.ui.core.queue.Manager.scheduleFlush(a);
},isScheduled:function(e){return !!this.__fl[e.$$hash];
},flush:function(){var f=this.__fo();
for(var i=f.length-1;i>=0;i--){var g=f[i];
if(g.hasValidLayout()){continue;
}if(g.isRootWidget()&&!g.hasUserBounds()){var j=g.getSizeHint();
g.renderLayout(0,0,j.width,j.height);
}else{var h=g.getBounds();
g.renderLayout(h.left,h.top,h.width,h.height);
}}},getNestingLevel:function(k){var l=this.__fn;
var n=0;
var parent=k;
while(true){if(l[parent.$$hash]!=null){n+=l[parent.$$hash];
break;
}
if(!parent.$$parent){break;
}parent=parent.$$parent;
n+=1;
}var m=n;

while(k&&k!==parent){l[k.$$hash]=m--;
k=k.$$parent;
}return n;
},__fm:function(){var t=qx.ui.core.queue.Visibility;
this.__fn={};
var s=[];
var r=this.__fl;
var o,q;

for(var p in r){o=r[p];

if(t.isVisible(o)){q=this.getNestingLevel(o);
if(!s[q]){s[q]={};
}s[q][p]=o;
delete r[p];
}}return s;
},__fo:function(){var x=[];
var z=this.__fm();

for(var w=z.length-1;w>=0;w--){if(!z[w]){continue;
}
for(var v in z[w]){var u=z[w][v];
if(w==0||u.isRootWidget()||u.hasUserBounds()){x.push(u);
u.invalidateLayoutCache();
continue;
}var B=u.getSizeHint(false);

if(B){u.invalidateLayoutCache();
var y=u.getSizeHint();
var A=(!u.getBounds()||B.minWidth!==y.minWidth||B.width!==y.width||B.maxWidth!==y.maxWidth||B.minHeight!==y.minHeight||B.height!==y.height||B.maxHeight!==y.maxHeight);
}else{A=true;
}
if(A){var parent=u.getLayoutParent();

if(!z[w-1]){z[w-1]={};
}z[w-1][parent.$$hash]=parent;
}else{x.push(u);
}}}return x;
}}});
})();
(function(){var b="qx.util.DeferredCallManager",a="singleton";
qx.Class.define(b,{extend:qx.core.Object,type:a,construct:function(){this.__fp={};
this.__fq=qx.lang.Function.bind(this.__fu,this);
this.__fr=false;
},members:{__fs:null,__ft:null,__fp:null,__fr:null,__fq:null,schedule:function(c){if(this.__fs==null){this.__fs=window.setTimeout(this.__fq,0);
}var d=c.toHashCode();
if(this.__ft&&this.__ft[d]){return;
}this.__fp[d]=c;
this.__fr=true;
},cancel:function(e){var f=e.toHashCode();
if(this.__ft&&this.__ft[f]){this.__ft[f]=null;
return;
}delete this.__fp[f];
if(qx.lang.Object.isEmpty(this.__fp)&&this.__fs!=null){window.clearTimeout(this.__fs);
this.__fs=null;
}},__fu:qx.event.GlobalError.observeMethod(function(){this.__fs=null;
while(this.__fr){this.__ft=qx.lang.Object.clone(this.__fp);
this.__fp={};
this.__fr=false;

for(var h in this.__ft){var g=this.__ft[h];

if(g){this.__ft[h]=null;
g.call();
}}}this.__ft=null;
})},destruct:function(){if(this.__fs!=null){window.clearTimeout(this.__fs);
}this.__fq=this.__fp=null;
}});
})();
(function(){var a="qx.util.DeferredCall";
qx.Class.define(a,{extend:qx.core.Object,construct:function(b,c){qx.core.Object.call(this);
this.__fv=b;
this.__fw=c||null;
this.__fx=qx.util.DeferredCallManager.getInstance();
},members:{__fv:null,__fw:null,__fx:null,cancel:function(){this.__fx.cancel(this);
},schedule:function(){this.__fx.schedule(this);
},call:function(){this.__fw?this.__fv.apply(this.__fw):this.__fv();
}},destruct:function(d,e){this.cancel();
this.__fw=this.__fv=this.__fx=null;
}});
})();
(function(){var m="element",k="qx.client",j="qxSelectable",h="off",g="on",f="text",d="div",c="",b="mshtml",a="none",G="scroll",F="qx.html.Element",E="|capture|",D="activate",C="blur",B="deactivate",A="capture",z="userSelect",w="chrome",v="-moz-none",t="visible",u="releaseCapture",r="|bubble|",s="tabIndex",p="__fU",q="focus",n="MozUserSelect",o="hidden";
qx.Class.define(F,{extend:qx.core.Object,construct:function(H,I,J){qx.core.Object.call(this);
this.__fy=H||d;
this.__fz=I||null;
this.__fA=J||null;
},statics:{DEBUG:false,_modified:{},_visibility:{},_scroll:{},_actions:[],__fB:{},_scheduleFlush:function(K){qx.html.Element.__gg.schedule();
},flush:function(){var V;
{};
var N=this.__fC();
var M=N.getFocus();

if(M&&this.__fG(M)){N.blur(M);
}var bd=N.getActive();

if(bd&&this.__fG(bd)){qx.bom.Element.deactivate(bd);
}var Q=this.__fE();

if(Q&&this.__fG(Q)){qx.bom.Element.releaseCapture(Q);
}var W=[];
var X=this._modified;

for(var U in X){V=X[U];
if(V.__fY()){if(V.__fH&&qx.dom.Hierarchy.isRendered(V.__fH)){W.push(V);
}else{{};
V.__fX();
}delete X[U];
}}
for(var i=0,l=W.length;i<l;i++){V=W[i];
{};
V.__fX();
}var S=this._visibility;

for(var U in S){V=S[U];
var Y=V.__fH;

if(!Y){delete S[U];
continue;
}{};
if(!V.$$disposed){Y.style.display=V.__fK?c:a;
if(qx.core.Variant.isSet(k,b)){if(!(document.documentMode>=8)){Y.style.visibility=V.__fK?t:o;
}}}delete S[U];
}var scroll=this._scroll;

for(var U in scroll){V=scroll[U];
var be=V.__fH;

if(be&&be.offsetWidth){var P=true;
if(V.__fN!=null){V.__fH.scrollLeft=V.__fN;
delete V.__fN;
}if(V.__fO!=null){V.__fH.scrollTop=V.__fO;
delete V.__fO;
}var ba=V.__fL;

if(ba!=null){var T=ba.element.getDomElement();

if(T&&T.offsetWidth){qx.bom.element.Scroll.intoViewX(T,be,ba.align);
delete V.__fL;
}else{P=false;
}}var bb=V.__fM;

if(bb!=null){var T=bb.element.getDomElement();

if(T&&T.offsetWidth){qx.bom.element.Scroll.intoViewY(T,be,bb.align);
delete V.__fM;
}else{P=false;
}}if(P){delete scroll[U];
}}}var O={"releaseCapture":1,"blur":1,"deactivate":1};
for(var i=0;i<this._actions.length;i++){var bc=this._actions[i];
var Y=bc.element.__fH;

if(!Y||!O[bc.type]&&!bc.element.__fY()){continue;
}var R=bc.args;
R.unshift(Y);
qx.bom.Element[bc.type].apply(qx.bom.Element,R);
}this._actions=[];
for(var U in this.__fB){var L=this.__fB[U];
var be=L.element.__fH;

if(be){qx.bom.Selection.set(be,L.start,L.end);
delete this.__fB[U];
}}qx.event.handler.Appear.refresh();
},__fC:function(){if(!this.__fD){var bf=qx.event.Registration.getManager(window);
this.__fD=bf.getHandler(qx.event.handler.Focus);
}return this.__fD;
},__fE:function(){if(!this.__fF){var bg=qx.event.Registration.getManager(window);
this.__fF=bg.getDispatcher(qx.event.dispatch.MouseCapture);
}return this.__fF.getCaptureElement();
},__fG:function(bh){var bi=qx.core.ObjectRegistry.fromHashCode(bh.$$element);
return bi&&!bi.__fY();
}},members:{__fy:null,__fH:null,__fI:false,__fJ:true,__fK:true,__fL:null,__fM:null,__fN:null,__fO:null,__fP:null,__fQ:null,__fR:null,__fz:null,__fA:null,__fS:null,__fT:null,__fU:null,__fV:null,__fW:null,_scheduleChildrenUpdate:function(){if(this.__fV){return;
}this.__fV=true;
qx.html.Element._modified[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
},_createDomElement:function(){return qx.bom.Element.create(this.__fy);
},__fX:function(){{};
var length;
var bj=this.__fU;

if(bj){length=bj.length;
var bk;

for(var i=0;i<length;i++){bk=bj[i];

if(bk.__fK&&bk.__fJ&&!bk.__fH){bk.__fX();
}}}
if(!this.__fH){this.__fH=this._createDomElement();
this.__fH.$$element=this.$$hash;
this._copyData(false);

if(bj&&length>0){this._insertChildren();
}}else{this._syncData();

if(this.__fV){this._syncChildren();
}}delete this.__fV;
},_insertChildren:function(){var bl=this.__fU;
var length=bl.length;
var bn;

if(length>2){var bm=document.createDocumentFragment();

for(var i=0;i<length;i++){bn=bl[i];

if(bn.__fH&&bn.__fJ){bm.appendChild(bn.__fH);
}}this.__fH.appendChild(bm);
}else{var bm=this.__fH;

for(var i=0;i<length;i++){bn=bl[i];

if(bn.__fH&&bn.__fJ){bm.appendChild(bn.__fH);
}}}},_syncChildren:function(){var bs;
var bx=qx.core.ObjectRegistry;
var bo=this.__fU;
var bv=bo.length;
var bp;
var bt;
var br=this.__fH;
var bu=br.childNodes;
var bq=0;
var bw;
{};
for(var i=bu.length-1;i>=0;i--){bw=bu[i];
bt=bx.fromHashCode(bw.$$element);

if(!bt||!bt.__fJ||bt.__fW!==this){br.removeChild(bw);
{};
}}for(var i=0;i<bv;i++){bp=bo[i];
if(bp.__fJ){bt=bp.__fH;
bw=bu[bq];

if(!bt){continue;
}if(bt!=bw){if(bw){br.insertBefore(bt,bw);
}else{br.appendChild(bt);
}{};
}bq++;
}}{};
},_copyData:function(by){var bC=this.__fH;
var bB=this.__fA;

if(bB){var bz=qx.bom.element.Attribute;

for(var bD in bB){bz.set(bC,bD,bB[bD]);
}}var bB=this.__fz;

if(bB){var bA=qx.bom.element.Style;

if(by){bA.setStyles(bC,bB);
}else{bA.setCss(bC,bA.compile(bB));
}}var bB=this.__fS;

if(bB){for(var bD in bB){this._applyProperty(bD,bB[bD]);
}}var bB=this.__fT;

if(bB){qx.event.Registration.getManager(bC).importListeners(bC,bB);
delete this.__fT;
}},_syncData:function(){var bI=this.__fH;
var bH=qx.bom.element.Attribute;
var bF=qx.bom.element.Style;
var bG=this.__fQ;

if(bG){var bL=this.__fA;

if(bL){var bJ;

for(var bK in bG){bJ=bL[bK];

if(bJ!==undefined){bH.set(bI,bK,bJ);
}else{bH.reset(bI,bK);
}}}this.__fQ=null;
}var bG=this.__fP;

if(bG){var bL=this.__fz;

if(bL){var bE={};

for(var bK in bG){bE[bK]=bL[bK];
}bF.setStyles(bI,bE);
}this.__fP=null;
}var bG=this.__fR;

if(bG){var bL=this.__fS;

if(bL){var bJ;

for(var bK in bG){this._applyProperty(bK,bL[bK]);
}}this.__fR=null;
}},__fY:function(){var bM=this;
while(bM){if(bM.__fI){return true;
}
if(!bM.__fJ||!bM.__fK){return false;
}bM=bM.__fW;
}return false;
},__ga:function(bN){if(bN.__fW===this){throw new Error("Child is already in: "+bN);
}
if(bN.__fI){throw new Error("Root elements could not be inserted into other ones.");
}if(bN.__fW){bN.__fW.remove(bN);
}bN.__fW=this;
if(!this.__fU){this.__fU=[];
}if(this.__fH){this._scheduleChildrenUpdate();
}},__gb:function(bO){if(bO.__fW!==this){throw new Error("Has no child: "+bO);
}if(this.__fH){this._scheduleChildrenUpdate();
}delete bO.__fW;
},__gc:function(bP){if(bP.__fW!==this){throw new Error("Has no child: "+bP);
}if(this.__fH){this._scheduleChildrenUpdate();
}},getChildren:function(){return this.__fU||null;
},getChild:function(bQ){var bR=this.__fU;
return bR&&bR[bQ]||null;
},hasChildren:function(){var bS=this.__fU;
return bS&&bS[0]!==undefined;
},indexOf:function(bT){var bU=this.__fU;
return bU?bU.indexOf(bT):-1;
},hasChild:function(bV){var bW=this.__fU;
return bW&&bW.indexOf(bV)!==-1;
},add:function(bX){if(arguments[1]){for(var i=0,l=arguments.length;i<l;i++){this.__ga(arguments[i]);
}this.__fU.push.apply(this.__fU,arguments);
}else{this.__ga(bX);
this.__fU.push(bX);
}return this;
},addAt:function(bY,ca){this.__ga(bY);
qx.lang.Array.insertAt(this.__fU,bY,ca);
return this;
},remove:function(cb){var cc=this.__fU;

if(!cc){return;
}
if(arguments[1]){var cd;

for(var i=0,l=arguments.length;i<l;i++){cd=arguments[i];
this.__gb(cd);
qx.lang.Array.remove(cc,cd);
}}else{this.__gb(cb);
qx.lang.Array.remove(cc,cb);
}return this;
},removeAt:function(ce){var cf=this.__fU;

if(!cf){throw new Error("Has no children!");
}var cg=cf[ce];

if(!cg){throw new Error("Has no child at this position!");
}this.__gb(cg);
qx.lang.Array.removeAt(this.__fU,ce);
return this;
},removeAll:function(){var ch=this.__fU;

if(ch){for(var i=0,l=ch.length;i<l;i++){this.__gb(ch[i]);
}ch.length=0;
}return this;
},getParent:function(){return this.__fW||null;
},insertInto:function(parent,ci){parent.__ga(this);

if(ci==null){parent.__fU.push(this);
}else{qx.lang.Array.insertAt(this.__fU,this,ci);
}return this;
},insertBefore:function(cj){var parent=cj.__fW;
parent.__ga(this);
qx.lang.Array.insertBefore(parent.__fU,this,cj);
return this;
},insertAfter:function(ck){var parent=ck.__fW;
parent.__ga(this);
qx.lang.Array.insertAfter(parent.__fU,this,ck);
return this;
},moveTo:function(cl){var parent=this.__fW;
parent.__gc(this);
var cm=parent.__fU.indexOf(this);

if(cm===cl){throw new Error("Could not move to same index!");
}else if(cm<cl){cl--;
}qx.lang.Array.removeAt(parent.__fU,cm);
qx.lang.Array.insertAt(parent.__fU,this,cl);
return this;
},moveBefore:function(cn){var parent=this.__fW;
return this.moveTo(parent.__fU.indexOf(cn));
},moveAfter:function(co){var parent=this.__fW;
return this.moveTo(parent.__fU.indexOf(co)+1);
},free:function(){var parent=this.__fW;

if(!parent){throw new Error("Has no parent to remove from.");
}
if(!parent.__fU){return;
}parent.__gb(this);
qx.lang.Array.remove(parent.__fU,this);
return this;
},getDomElement:function(){return this.__fH||null;
},getNodeName:function(){return this.__fy;
},setNodeName:function(name){this.__fy=name;
},setRoot:function(cp){this.__fI=cp;
},useMarkup:function(cq){if(this.__fH){throw new Error("Could not overwrite existing element!");
}if(qx.core.Variant.isSet(k,b)){var cr=document.createElement(d);
}else{var cr=qx.bom.Element.getHelperElement();
}cr.innerHTML=cq;
this.useElement(cr.firstChild);
return this.__fH;
},useElement:function(cs){if(this.__fH){throw new Error("Could not overwrite existing element!");
}this.__fH=cs;
this.__fH.$$element=this.$$hash;
this._copyData(true);
},isFocusable:function(){var cu=this.getAttribute(s);

if(cu>=1){return true;
}var ct=qx.event.handler.Focus.FOCUSABLE_ELEMENTS;

if(cu>=0&&ct[this.__fy]){return true;
}return false;
},setSelectable:qx.core.Variant.select(k,{"webkit":function(cv){this.setAttribute(j,cv?g:h);
if(qx.bom.client.Browser.NAME!==w){this.setStyle(z,cv?f:a);
}},"gecko":function(cw){this.setAttribute(j,cw?g:h);
this.setStyle(n,cw?f:v);
},"default":function(cx){this.setAttribute(j,cx?g:h);
}}),isNativelyFocusable:function(){return !!qx.event.handler.Focus.FOCUSABLE_ELEMENTS[this.__fy];
},include:function(){if(this.__fJ){return;
}delete this.__fJ;

if(this.__fW){this.__fW._scheduleChildrenUpdate();
}return this;
},exclude:function(){if(!this.__fJ){return;
}this.__fJ=false;

if(this.__fW){this.__fW._scheduleChildrenUpdate();
}return this;
},isIncluded:function(){return this.__fJ===true;
},show:function(){if(this.__fK){return;
}
if(this.__fH){qx.html.Element._visibility[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}if(this.__fW){this.__fW._scheduleChildrenUpdate();
}delete this.__fK;
},hide:function(){if(!this.__fK){return;
}
if(this.__fH){qx.html.Element._visibility[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}this.__fK=false;
},isVisible:function(){return this.__fK===true;
},scrollChildIntoViewX:function(cy,cz,cA){var cB=this.__fH;
var cC=cy.getDomElement();

if(cA!==false&&cB&&cB.offsetWidth&&cC&&cC.offsetWidth){qx.bom.element.Scroll.intoViewX(cC,cB,cz);
}else{this.__fL={element:cy,align:cz};
qx.html.Element._scroll[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}delete this.__fN;
},scrollChildIntoViewY:function(cD,cE,cF){var cG=this.__fH;
var cH=cD.getDomElement();

if(cF!==false&&cG&&cG.offsetWidth&&cH&&cH.offsetWidth){qx.bom.element.Scroll.intoViewY(cH,cG,cE);
}else{this.__fM={element:cD,align:cE};
qx.html.Element._scroll[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}delete this.__fO;
},scrollToX:function(x,cI){var cJ=this.__fH;

if(cI!==true&&cJ&&cJ.offsetWidth){cJ.scrollLeft=x;
delete this.__fN;
}else{this.__fN=x;
qx.html.Element._scroll[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}delete this.__fL;
},getScrollX:function(){var cK=this.__fH;

if(cK){return cK.scrollLeft;
}return this.__fN||0;
},scrollToY:function(y,cL){var cM=this.__fH;

if(cL!==true&&cM&&cM.offsetWidth){cM.scrollTop=y;
delete this.__fO;
}else{this.__fO=y;
qx.html.Element._scroll[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}delete this.__fM;
},getScrollY:function(){var cN=this.__fH;

if(cN){return cN.scrollTop;
}return this.__fO||0;
},disableScrolling:function(){this.enableScrolling();
this.scrollToX(0);
this.scrollToY(0);
this.addListener(G,this.__ge,this);
},enableScrolling:function(){this.removeListener(G,this.__ge,this);
},__gd:null,__ge:function(e){if(!this.__gd){this.__gd=true;
this.__fH.scrollTop=0;
this.__fH.scrollLeft=0;
delete this.__gd;
}},getTextSelection:function(){var cO=this.__fH;

if(cO){return qx.bom.Selection.get(cO);
}return null;
},getTextSelectionLength:function(){var cP=this.__fH;

if(cP){return qx.bom.Selection.getLength(cP);
}return null;
},getTextSelectionStart:function(){var cQ=this.__fH;

if(cQ){return qx.bom.Selection.getStart(cQ);
}return null;
},getTextSelectionEnd:function(){var cR=this.__fH;

if(cR){return qx.bom.Selection.getEnd(cR);
}return null;
},setTextSelection:function(cS,cT){var cU=this.__fH;

if(cU){qx.bom.Selection.set(cU,cS,cT);
return;
}qx.html.Element.__fB[this.toHashCode()]={element:this,start:cS,end:cT};
qx.html.Element._scheduleFlush(m);
},clearTextSelection:function(){var cV=this.__fH;

if(cV){qx.bom.Selection.clear(cV);
}delete qx.html.Element.__fB[this.toHashCode()];
},__gf:function(cW,cX){var cY=qx.html.Element._actions;
cY.push({type:cW,element:this,args:cX||[]});
qx.html.Element._scheduleFlush(m);
},focus:function(){this.__gf(q);
},blur:function(){this.__gf(C);
},activate:function(){this.__gf(D);
},deactivate:function(){this.__gf(B);
},capture:function(da){this.__gf(A,[da!==false]);
},releaseCapture:function(){this.__gf(u);
},setStyle:function(dc,dd,de){if(!this.__fz){this.__fz={};
}
if(this.__fz[dc]==dd){return;
}
if(dd==null){delete this.__fz[dc];
}else{this.__fz[dc]=dd;
}if(this.__fH){if(de){qx.bom.element.Style.set(this.__fH,dc,dd);
return this;
}if(!this.__fP){this.__fP={};
}this.__fP[dc]=true;
qx.html.Element._modified[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}return this;
},setStyles:function(df,dg){var dh=qx.bom.element.Style;

if(!this.__fz){this.__fz={};
}
if(this.__fH){if(!this.__fP){this.__fP={};
}
for(var dj in df){var di=df[dj];

if(this.__fz[dj]==di){continue;
}
if(di==null){delete this.__fz[dj];
}else{this.__fz[dj]=di;
}if(dg){dh.set(this.__fH,dj,di);
continue;
}this.__fP[dj]=true;
}qx.html.Element._modified[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}else{for(var dj in df){var di=df[dj];

if(this.__fz[dj]==di){continue;
}
if(di==null){delete this.__fz[dj];
}else{this.__fz[dj]=di;
}}}return this;
},removeStyle:function(dk,dl){this.setStyle(dk,null,dl);
},getStyle:function(dm){return this.__fz?this.__fz[dm]:null;
},getAllStyles:function(){return this.__fz||null;
},setAttribute:function(dn,dp,dq){if(!this.__fA){this.__fA={};
}
if(this.__fA[dn]==dp){return;
}
if(dp==null){delete this.__fA[dn];
}else{this.__fA[dn]=dp;
}if(this.__fH){if(dq){qx.bom.element.Attribute.set(this.__fH,dn,dp);
return this;
}if(!this.__fQ){this.__fQ={};
}this.__fQ[dn]=true;
qx.html.Element._modified[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}return this;
},setAttributes:function(dr,ds){for(var dt in dr){this.setAttribute(dt,dr[dt],ds);
}return this;
},removeAttribute:function(du,dv){this.setAttribute(du,null,dv);
},getAttribute:function(dw){return this.__fA?this.__fA[dw]:null;
},_applyProperty:function(name,dx){},_setProperty:function(dy,dz,dA){if(!this.__fS){this.__fS={};
}
if(this.__fS[dy]==dz){return;
}
if(dz==null){delete this.__fS[dy];
}else{this.__fS[dy]=dz;
}if(this.__fH){if(dA){this._applyProperty(dy,dz);
return this;
}if(!this.__fR){this.__fR={};
}this.__fR[dy]=true;
qx.html.Element._modified[this.$$hash]=this;
qx.html.Element._scheduleFlush(m);
}return this;
},_removeProperty:function(dB,dC){this._setProperty(dB,null,dC);
},_getProperty:function(dD){var dE=this.__fS;

if(!dE){return null;
}var dF=dE[dD];
return dF==null?null:dF;
},addListener:function(dG,dH,self,dI){var dJ;

if(this.$$disposed){return null;
}{};

if(this.__fH){return qx.event.Registration.addListener(this.__fH,dG,dH,self,dI);
}
if(!this.__fT){this.__fT={};
}
if(dI==null){dI=false;
}var dK=qx.event.Manager.getNextUniqueId();
var dL=dG+(dI?E:r)+dK;
this.__fT[dL]={type:dG,listener:dH,self:self,capture:dI,unique:dK};
return dL;
},removeListener:function(dM,dN,self,dO){var dP;

if(this.$$disposed){return null;
}{};

if(this.__fH){qx.event.Registration.removeListener(this.__fH,dM,dN,self,dO);
}else{var dR=this.__fT;
var dQ;

if(dO==null){dO=false;
}
for(var dS in dR){dQ=dR[dS];
if(dQ.listener===dN&&dQ.self===self&&dQ.capture===dO&&dQ.type===dM){delete dR[dS];
break;
}}}return this;
},removeListenerById:function(dT){if(this.$$disposed){return null;
}
if(this.__fH){qx.event.Registration.removeListenerById(this.__fH,dT);
}else{delete this.__fT[dT];
}return this;
},hasListener:function(dU,dV){if(this.$$disposed){return false;
}
if(this.__fH){return qx.event.Registration.hasListener(this.__fH,dU,dV);
}var dX=this.__fT;
var dW;

if(dV==null){dV=false;
}
for(var dY in dX){dW=dX[dY];
if(dW.capture===dV&&dW.type===dU){return true;
}}return false;
}},defer:function(ea){ea.__gg=new qx.util.DeferredCall(ea.flush,ea);
},destruct:function(){var eb=this.__fH;

if(eb){qx.event.Registration.getManager(eb).removeAllListeners(eb);
eb.$$element=c;
}
if(!qx.core.ObjectRegistry.inShutDown){var parent=this.__fW;

if(parent&&!parent.$$disposed){parent.remove(this);
}}this._disposeArray(p);
this.__fA=this.__fz=this.__fT=this.__fS=this.__fQ=this.__fP=this.__fR=this.__fH=this.__fW=this.__fL=this.__fM=null;
}});
})();
(function(){var a="qx.event.handler.UserAction";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(b){qx.core.Object.call(this);
this.__gh=b;
this.__gi=b.getWindow();
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{useraction:1},TARGET_CHECK:qx.event.IEventHandler.TARGET_WINDOW,IGNORE_CAN_HANDLE:true},members:{__gh:null,__gi:null,canHandleEvent:function(c,d){},registerEvent:function(e,f,g){},unregisterEvent:function(h,i,j){}},destruct:function(){this.__gh=this.__gi=null;
},defer:function(k){qx.event.Registration.addHandler(k);
}});
})();
(function(){var d='ie',c="qx.ui.core.queue.Manager",b="useraction",a="touchend";
qx.Class.define(c,{statics:{__gj:false,__gk:{},__gl:0,MAX_RETRIES:10,scheduleFlush:function(f){var self=qx.ui.core.queue.Manager;
self.__gk[f]=true;

if(!self.__gj){self.__gq.schedule();
self.__gj=true;
}},flush:function(){if(qx.ui.core.queue.Manager.PAUSE){return;
}var self=qx.ui.core.queue.Manager;
if(self.__gm){return;
}self.__gm=true;
self.__gq.cancel();
var g=self.__gk;
self.__gn(function(){while(g.visibility||g.widget||g.appearance||g.layout||g.element){if(g.widget){delete g.widget;
qx.ui.core.queue.Widget.flush();
}
if(g.visibility){delete g.visibility;
qx.ui.core.queue.Visibility.flush();
}
if(g.appearance){delete g.appearance;
qx.ui.core.queue.Appearance.flush();
}if(g.widget||g.visibility||g.appearance){continue;
}
if(g.layout){delete g.layout;
qx.ui.core.queue.Layout.flush();
}if(g.widget||g.visibility||g.appearance||g.layout){continue;
}
if(g.element){delete g.element;
qx.html.Element.flush();
}}},function(){self.__gj=false;
});
self.__gn(function(){if(g.dispose){delete g.dispose;
qx.ui.core.queue.Dispose.flush();
}},function(){self.__gm=false;
});
self.__gl=0;
},__gn:function(h,i){var self=qx.ui.core.queue.Manager;

try{h();
}catch(e){{};
self.__gj=false;
self.__gm=false;
self.__gl+=1;
if(qx.bom.client.Browser.NAME==d&&qx.bom.client.Browser.VERSION<=7){i();
}
if(self.__gl<=self.MAX_RETRIES){self.scheduleFlush();
}else{throw new Error("Fatal Error: Flush terminated "+(self.__gl-1)+" times in a row"+" due to exceptions in user code. The application has to be reloaded!");
}throw e;
}finally{i();
}},__go:function(e){var j=qx.ui.core.queue.Manager;
if(e.getData()==a){j.PAUSE=true;

if(j.__gp){window.clearTimeout(j.__gp);
}j.__gp=window.setTimeout(function(){j.PAUSE=false;
j.__gp=null;
j.flush();
},500);
}else{j.flush();
}}},defer:function(k){k.__gq=new qx.util.DeferredCall(k.flush);
qx.html.Element._scheduleFlush=k.scheduleFlush;
qx.event.Registration.addListener(window,b,qx.bom.client.Feature.TOUCH?k.__go:k.flush);
}});
})();
(function(){var d="-",c="qx.event.handler.Element",b="load",a="iframe";
qx.Class.define(c,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(e){qx.core.Object.call(this);
this._manager=e;
this._registeredEvents={};
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{abort:true,load:true,scroll:true,select:true,selectstart:true,reset:true,submit:true},CANCELABLE:{selectstart:true},TARGET_CHECK:qx.event.IEventHandler.TARGET_DOMNODE,IGNORE_CAN_HANDLE:false},members:{canHandleEvent:function(f,g){if(g===b){return f.tagName.toLowerCase()!==a;
}else{return true;
}},registerEvent:function(h,i,j){var m=qx.core.ObjectRegistry.toHashCode(h);
var k=m+d+i;
var l=qx.lang.Function.listener(this._onNative,this,k);
qx.bom.Event.addNativeListener(h,i,l);
this._registeredEvents[k]={element:h,type:i,listener:l};
},unregisterEvent:function(n,o,p){var s=this._registeredEvents;

if(!s){return;
}var t=qx.core.ObjectRegistry.toHashCode(n);
var q=t+d+o;
var r=this._registeredEvents[q];

if(r){qx.bom.Event.removeNativeListener(n,o,r.listener);
}delete this._registeredEvents[q];
},_onNative:qx.event.GlobalError.observeMethod(function(u,v){var x=this._registeredEvents;

if(!x){return;
}var w=x[v];
var y=this.constructor.CANCELABLE[w.type];
qx.event.Registration.fireNonBubblingEvent(w.element,w.type,qx.event.type.Native,[u,undefined,undefined,undefined,y]);
})},destruct:function(){var z;
var A=this._registeredEvents;

for(var B in A){z=A[B];
qx.bom.Event.removeNativeListener(z.element,z.type,z.listener);
}this._manager=this._registeredEvents=null;
},defer:function(C){qx.event.Registration.addHandler(C);
}});
})();
(function(){var e="orientationchange",d="resize",c="landscape",b="portrait",a="qx.event.handler.Orientation";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(f){qx.core.Object.call(this);
this.__gr=f;
this.__gs=f.getWindow();
this._initObserver();
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{orientationchange:1},TARGET_CHECK:qx.event.IEventHandler.TARGET_WINDOW,IGNORE_CAN_HANDLE:true},members:{__gr:null,__gs:null,__gt:null,__gu:null,__gv:null,canHandleEvent:function(g,h){},registerEvent:function(i,j,k){},unregisterEvent:function(l,m,n){},_initObserver:function(){this.__gv=qx.lang.Function.listener(this._onNative,this);
this.__gt=qx.bom.Event.supportsEvent(this.__gs,e)?e:d;
var Event=qx.bom.Event;
Event.addNativeListener(this.__gs,this.__gt,this.__gv);
},_stopObserver:function(){var Event=qx.bom.Event;
Event.removeNativeListener(this.__gs,this.__gt,this.__gv);
},_onNative:qx.event.GlobalError.observeMethod(function(o){var q=qx.bom.Viewport;
var p=q.getOrientation();

if(this.__gu!=p){this.__gu=p;
var r=q.isLandscape()?c:b;
qx.event.Registration.fireEvent(this.__gs,e,qx.event.type.Orientation,[p,r]);
}})},destruct:function(){this._stopObserver();
this.__gr=this.__gs=null;
},defer:function(s){qx.event.Registration.addHandler(s);
}});
})();
(function(){var t="qx.mobile.emulatetouch",s="touchend",r="touchstart",q="touchmove",p="mousemove",o="touchcancel",n="mouseup",m="mousedown",l="qx.client",k="mshtml",d="qx.event.handler.Touch",j="useraction",h="swipe",c="qx.mobile.nativescroll",b="webkit",g="off",f="tap",i="x",a="y";
qx.Class.define(d,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(u){qx.core.Object.call(this);
this.__gw=u;
this.__gx=u.getWindow();
this.__gy=this.__gx.document;
this._initTouchObserver();
this._initMouseObserver();
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{touchstart:1,touchmove:1,touchend:1,touchcancel:1,tap:1,swipe:1},TARGET_CHECK:qx.event.IEventHandler.TARGET_DOMNODE+qx.event.IEventHandler.TARGET_DOCUMENT,IGNORE_CAN_HANDLE:true,MOUSE_TO_TOUCH_MAPPING:{"mousedown":"touchstart","mousemove":"touchmove","mouseup":"touchend"},SWIPE_DIRECTION:{x:["left","right"],y:["up","down"]},TAP_MAX_DISTANCE:10,SWIPE_MIN_DISTANCE:11,SWIPE_MIN_VELOCITY:0},members:{__gz:null,__gA:null,__gw:null,__gx:null,__gy:null,__gB:null,__gC:null,__gD:null,__gE:null,__gF:false,__gG:null,canHandleEvent:function(v,w){},registerEvent:function(x,y,z){},unregisterEvent:function(A,B,C){},__gH:function(D){var E=qx.bom.Event.getTarget(D);
if(qx.core.Variant.isSet(l,b)){if(E&&E.nodeType==3){E=E.parentNode;
}}return E;
},__gI:function(F,G,H,I){if(!H){H=this.__gH(F);
}var G=G||F.type;

if(H&&H.nodeType){qx.event.Registration.fireEvent(H,G,I||qx.event.type.Touch,[F,H,null,true,true]);
}qx.event.Registration.fireEvent(this.__gx,j,qx.event.type.Data,[G]);
},__gJ:function(J,K,L){if(!L){L=this.__gH(J);
}var K=K||J.type;

if(K==r){this.__gK(J,L);
}else if(K==q){this.__gL(J,L);
}else if(K==s){this.__gM(J,L);
}},__gK:function(M,N){var O=M.changedTouches[0];
this.__gB=O.screenX;
this.__gC=O.screenY;
this.__gD=new Date().getTime();
this.__gE=M.changedTouches.length===1;
},__gL:function(P,Q){if(this.__gE&&P.changedTouches.length>1){this.__gE=false;
}},__gM:function(R,S){if(this.__gE){var T=R.changedTouches[0];
var V={x:T.screenX-this.__gB,y:T.screenY-this.__gC};
var W=qx.event.handler.Touch;

if(this.__gG==S&&Math.abs(V.x)<=W.TAP_MAX_DISTANCE&&Math.abs(V.y)<=W.TAP_MAX_DISTANCE){this.__gI(R,f,S,qx.event.type.Tap);
}else{var U=this.__gN(R,S,V);

if(U){R.swipe=U;
this.__gI(R,h,S,qx.event.type.Swipe);
}}}},__gN:function(X,Y,ba){var be=qx.event.handler.Touch;
var bf=new Date().getTime()-this.__gD;
var bh=(Math.abs(ba.x)>=Math.abs(ba.y))?i:a;
var bb=ba[bh];
var bc=be.SWIPE_DIRECTION[bh][bb<0?0:1];
var bg=(bf!==0)?bb/bf:0;
var bd=null;

if(Math.abs(bg)>=be.SWIPE_MIN_VELOCITY&&Math.abs(bb)>=be.SWIPE_MIN_DISTANCE){bd={startTime:this.__gD,duration:bf,axis:bh,direction:bc,distance:bb,velocity:bg};
}return bd;
},__gO:qx.core.Variant.select(t,{"on":function(bi){var bj=bi.type;
var bl=qx.event.handler.Touch.MOUSE_TO_TOUCH_MAPPING;

if(bl[bj]){bj=bl[bj];
if(bj==r&&this.__gP(bi)){this.__gF=true;
}else if(bj==s){this.__gF=false;
}var bm=this.__gQ(bi);
var bk=(bj==s?[]:[bm]);
bi.touches=bk;
bi.targetTouches=bk;
bi.changedTouches=[bm];
}return bj;
},"default":qx.lang.Function.empty}),__gP:qx.core.Variant.select(t,{"on":function(bn){if(qx.core.Variant.isSet(l,k)){var bo=1;
}else{var bo=0;
}return bn.button==bo;
},"default":qx.lang.Function.empty}),__gQ:qx.core.Variant.select(t,{"on":function(bp){var bq=this.__gH(bp);
return {clientX:bp.clientX,clientY:bp.clientY,screenX:bp.screenX,screenY:bp.screenY,pageX:bp.pageX,pageY:bp.pageY,identifier:1,target:bq};
},"default":qx.lang.Function.empty}),_initTouchObserver:function(){this.__gz=qx.lang.Function.listener(this._onTouchEvent,this);
var Event=qx.bom.Event;
Event.addNativeListener(this.__gy,r,this.__gz);
Event.addNativeListener(this.__gy,q,this.__gz);
Event.addNativeListener(this.__gy,s,this.__gz);
Event.addNativeListener(this.__gy,o,this.__gz);
},_initMouseObserver:qx.core.Variant.select(t,{"on":function(){if(!qx.bom.client.Feature.TOUCH){this.__gA=qx.lang.Function.listener(this._onMouseEvent,this);
var Event=qx.bom.Event;
Event.addNativeListener(this.__gy,m,this.__gA);
Event.addNativeListener(this.__gy,p,this.__gA);
Event.addNativeListener(this.__gy,n,this.__gA);
}},"default":qx.lang.Function.empty}),_stopTouchObserver:function(){var Event=qx.bom.Event;
Event.removeNativeListener(this.__gy,r,this.__gz);
Event.removeNativeListener(this.__gy,q,this.__gz);
Event.removeNativeListener(this.__gy,s,this.__gz);
Event.removeNativeListener(this.__gy,o,this.__gz);
},_stopMouseObserver:qx.core.Variant.select(t,{"on":function(){if(!qx.bom.client.Feature.TOUCH){var Event=qx.bom.Event;
Event.removeNativeListener(this.__gy,m,this.__gA);
Event.removeNativeListener(this.__gy,p,this.__gA);
Event.removeNativeListener(this.__gy,n,this.__gA);
}},"default":qx.lang.Function.empty}),_onTouchEvent:qx.event.GlobalError.observeMethod(function(br){this._commonTouchEventHandler(br);
}),_onMouseEvent:qx.core.Variant.select(t,{"on":qx.event.GlobalError.observeMethod(function(bs){if(!qx.bom.client.Feature.TOUCH){if(bs.type==p&&!this.__gF){return;
}var bt=this.__gO(bs);
this._commonTouchEventHandler(bs,bt);
}}),"default":qx.lang.Function.empty}),_commonTouchEventHandler:function(bu,bv){var bv=bv||bu.type;

if(bv==r){this.__gG=this.__gH(bu);
}this.__gI(bu,bv);
this.__gJ(bu,bv);
}},destruct:function(){this._stopTouchObserver();
this._stopMouseObserver();
this.__gw=this.__gx=this.__gy=this.__gG=null;
},defer:function(bw){qx.event.Registration.addHandler(bw);
if(qx.bom.client.Feature.TOUCH){if(qx.core.Variant.isSet(c,g)){document.addEventListener(q,function(e){e.preventDefault();
});
}qx.event.Registration.getManager(document).getHandler(bw);
}}});
})();
(function(){var a="qx.event.handler.Capture";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.event.IEventHandler,statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{capture:true,losecapture:true},TARGET_CHECK:qx.event.IEventHandler.TARGET_DOMNODE,IGNORE_CAN_HANDLE:true},members:{canHandleEvent:function(b,c){},registerEvent:function(d,e,f){},unregisterEvent:function(g,h,i){}},defer:function(j){qx.event.Registration.addHandler(j);
}});
})();
(function(){var p="mouseup",o="click",n="qx.client",m="mousedown",l="contextmenu",k="mousewheel",j="dblclick",h="mouseover",g="mouseout",f="mousemove",c="on",e="useraction",d="DOMMouseScroll",b="gecko|webkit",a="qx.event.handler.Mouse";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(q){qx.core.Object.call(this);
this.__gR=q;
this.__gS=q.getWindow();
this.__gT=this.__gS.document;
this._initButtonObserver();
this._initMoveObserver();
this._initWheelObserver();
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{mousemove:1,mouseover:1,mouseout:1,mousedown:1,mouseup:1,click:1,dblclick:1,contextmenu:1,mousewheel:1},TARGET_CHECK:qx.event.IEventHandler.TARGET_DOMNODE+qx.event.IEventHandler.TARGET_DOCUMENT+qx.event.IEventHandler.TARGET_WINDOW,IGNORE_CAN_HANDLE:true},members:{__gU:null,__gV:null,__gW:null,__gX:null,__gY:null,__gR:null,__gS:null,__gT:null,canHandleEvent:function(r,s){},registerEvent:qx.bom.client.System.IPHONE||
qx.bom.client.System.IPAD?
function(t,u,v){t[c+u]=qx.lang.Function.returnNull;
}:qx.lang.Function.returnNull,unregisterEvent:qx.bom.client.System.IPHONE||
qx.bom.client.System.IPAD?
function(w,x,y){w[c+x]=undefined;
}:qx.lang.Function.returnNull,__ha:function(z,A,B){if(!B){B=qx.bom.Event.getTarget(z);
}if(B&&B.nodeType){qx.event.Registration.fireEvent(B,A||z.type,A==k?qx.event.type.MouseWheel:qx.event.type.Mouse,[z,B,null,true,true]);
}qx.event.Registration.fireEvent(this.__gS,e,qx.event.type.Data,[A||z.type]);
},__hb:function(){var D=[this.__gS,this.__gT,this.__gT.body];
var E=this.__gS;
var C=d;

for(var i=0;i<D.length;i++){if(qx.bom.Event.supportsEvent(D[i],k)){C=k;
E=D[i];
break;
}}return {type:C,target:E};
},_initButtonObserver:function(){this.__gU=qx.lang.Function.listener(this._onButtonEvent,this);
var Event=qx.bom.Event;
Event.addNativeListener(this.__gT,m,this.__gU);
Event.addNativeListener(this.__gT,p,this.__gU);
Event.addNativeListener(this.__gT,o,this.__gU);
Event.addNativeListener(this.__gT,j,this.__gU);
Event.addNativeListener(this.__gT,l,this.__gU);
},_initMoveObserver:function(){this.__gV=qx.lang.Function.listener(this._onMoveEvent,this);
var Event=qx.bom.Event;
Event.addNativeListener(this.__gT,f,this.__gV);
Event.addNativeListener(this.__gT,h,this.__gV);
Event.addNativeListener(this.__gT,g,this.__gV);
},_initWheelObserver:function(){this.__gW=qx.lang.Function.listener(this._onWheelEvent,this);
var F=this.__hb();
qx.bom.Event.addNativeListener(F.target,F.type,this.__gW);
},_stopButtonObserver:function(){var Event=qx.bom.Event;
Event.removeNativeListener(this.__gT,m,this.__gU);
Event.removeNativeListener(this.__gT,p,this.__gU);
Event.removeNativeListener(this.__gT,o,this.__gU);
Event.removeNativeListener(this.__gT,j,this.__gU);
Event.removeNativeListener(this.__gT,l,this.__gU);
},_stopMoveObserver:function(){var Event=qx.bom.Event;
Event.removeNativeListener(this.__gT,f,this.__gV);
Event.removeNativeListener(this.__gT,h,this.__gV);
Event.removeNativeListener(this.__gT,g,this.__gV);
},_stopWheelObserver:function(){var G=this.__hb();
qx.bom.Event.removeNativeListener(G.target,G.type,this.__gW);
},_onMoveEvent:qx.event.GlobalError.observeMethod(function(H){this.__ha(H);
}),_onButtonEvent:qx.event.GlobalError.observeMethod(function(I){var J=I.type;
var K=qx.bom.Event.getTarget(I);
if(qx.core.Variant.isSet(n,b)){if(K&&K.nodeType==3){K=K.parentNode;
}}
if(this.__hc){this.__hc(I,J,K);
}
if(this.__he){this.__he(I,J,K);
}this.__ha(I,J,K);

if(this.__hd){this.__hd(I,J,K);
}
if(this.__hf){this.__hf(I,J,K);
}this.__gX=J;
}),_onWheelEvent:qx.event.GlobalError.observeMethod(function(L){this.__ha(L,k);
}),__hc:qx.core.Variant.select(n,{"webkit":function(M,N,O){if(qx.bom.client.Engine.VERSION<530){if(N==l){this.__ha(M,p,O);
}}},"default":null}),__hd:qx.core.Variant.select(n,{"opera":function(P,Q,R){if(Q==p&&P.button==2){this.__ha(P,l,R);
}},"default":null}),__he:qx.core.Variant.select(n,{"mshtml":function(S,T,U){if(S.target!==undefined){return;
}
if(T==p&&this.__gX==o){this.__ha(S,m,U);
}else if(T==j){this.__ha(S,o,U);
}},"default":null}),__hf:qx.core.Variant.select(n,{"mshtml":null,"default":function(V,W,X){switch(W){case m:this.__gY=X;
break;
case p:if(X!==this.__gY){var Y=qx.dom.Hierarchy.getCommonParent(X,this.__gY);
this.__ha(V,o,Y);
}}}})},destruct:function(){this._stopButtonObserver();
this._stopMoveObserver();
this._stopWheelObserver();
this.__gR=this.__gS=this.__gT=this.__gY=null;
},defer:function(ba){qx.event.Registration.addHandler(ba);
}});
})();
(function(){var m="keydown",l="qx.client",k="keypress",j="NumLock",i="keyup",h="Enter",g="0",f="9",e="-",d="PageUp",bu="+",bt="PrintScreen",bs="gecko",br="A",bq="Space",bp="Left",bo="F5",bn="Down",bm="Up",bl="F11",t="F6",u="useraction",r="F3",s="keyinput",p="Insert",q="F8",n="End",o="/",B="Delete",C="*",O="cmd",K="F1",W="F4",R="Home",bh="F2",bc="F12",G="PageDown",bk="F7",bj="Win",bi="F9",F="F10",I="Right",J="Z",M="text",P="Escape",S="webkit",Y="5",be="3",v="Meta",w="7",H="CapsLock",V="input",U="Control",T="Tab",bb="Shift",ba="Pause",Q="Unidentified",X="qx.event.handler.Keyboard",a="mshtml|webkit",bd="6",x="off",y="Apps",L="4",b="Alt",c="mshtml",E="2",z="Scroll",A="1",D="8",N="Backspace",bg="autoComplete",bf=",";
qx.Class.define(X,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(bv){qx.core.Object.call(this);
this.__hg=bv;
this.__hh=bv.getWindow();
if(qx.core.Variant.isSet(l,bs)){this.__hi=this.__hh;
}else{this.__hi=this.__hh.document.documentElement;
}this.__hj={};
this._initKeyObserver();
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{keyup:1,keydown:1,keypress:1,keyinput:1},TARGET_CHECK:qx.event.IEventHandler.TARGET_DOMNODE,IGNORE_CAN_HANDLE:true,isValidKeyIdentifier:function(bw){if(this._identifierToKeyCodeMap[bw]){return true;
}
if(bw.length!=1){return false;
}
if(bw>=g&&bw<=f){return true;
}
if(bw>=br&&bw<=J){return true;
}
switch(bw){case bu:case e:case C:case o:return true;
default:return false;
}},isPrintableKeyIdentifier:function(bx){if(bx===bq){return true;
}else{return this._identifierToKeyCodeMap[bx]?false:true;
}}},members:{__hk:null,__hg:null,__hh:null,__hi:null,__hj:null,__hl:null,__hm:null,__hn:null,canHandleEvent:function(by,bz){},registerEvent:function(bA,bB,bC){},unregisterEvent:function(bD,bE,bF){},_fireInputEvent:function(bG,bH){var bI=this.__ho();
if(bI&&bI.offsetWidth!=0){var event=qx.event.Registration.createEvent(s,qx.event.type.KeyInput,[bG,bI,bH]);
this.__hg.dispatchEvent(bI,event);
}if(this.__hh){qx.event.Registration.fireEvent(this.__hh,u,qx.event.type.Data,[s]);
}},_fireSequenceEvent:function(bJ,bK,bL){var bM=this.__ho();
var bN=bJ.keyCode;
var event=qx.event.Registration.createEvent(bK,qx.event.type.KeySequence,[bJ,bM,bL]);
this.__hg.dispatchEvent(bM,event);
if(qx.core.Variant.isSet(l,a)){if(bK==m&&event.getDefaultPrevented()){if(!this._isNonPrintableKeyCode(bN)&&!this._emulateKeyPress[bN]){this._fireSequenceEvent(bJ,k,bL);
}}}if(this.__hh){qx.event.Registration.fireEvent(this.__hh,u,qx.event.type.Data,[bK]);
}},__ho:function(){var bO=this.__hg.getHandler(qx.event.handler.Focus);
var bP=bO.getActive();
if(!bP||bP.offsetWidth==0){bP=bO.getFocus();
}if(!bP||bP.offsetWidth==0){bP=this.__hg.getWindow().document.body;
}return bP;
},_initKeyObserver:function(){this.__hk=qx.lang.Function.listener(this.__hp,this);
this.__hn=qx.lang.Function.listener(this.__hr,this);
var Event=qx.bom.Event;
Event.addNativeListener(this.__hi,i,this.__hk);
Event.addNativeListener(this.__hi,m,this.__hk);
Event.addNativeListener(this.__hi,k,this.__hn);
},_stopKeyObserver:function(){var Event=qx.bom.Event;
Event.removeNativeListener(this.__hi,i,this.__hk);
Event.removeNativeListener(this.__hi,m,this.__hk);
Event.removeNativeListener(this.__hi,k,this.__hn);

for(var bR in (this.__hm||{})){var bQ=this.__hm[bR];
Event.removeNativeListener(bQ.target,k,bQ.callback);
}delete (this.__hm);
},__hp:qx.event.GlobalError.observeMethod(qx.core.Variant.select(l,{"mshtml":function(bS){bS=window.event||bS;
var bV=bS.keyCode;
var bT=0;
var bU=bS.type;
if(!(this.__hj[bV]==m&&bU==m)){this._idealKeyHandler(bV,bT,bU,bS);
}if(bU==m){if(this._isNonPrintableKeyCode(bV)||this._emulateKeyPress[bV]){this._idealKeyHandler(bV,bT,k,bS);
}}this.__hj[bV]=bU;
},"gecko":function(bW){var cb=this._keyCodeFix[bW.keyCode]||bW.keyCode;
var bY=0;
var ca=bW.type;
if(qx.bom.client.Platform.WIN){var bX=cb?this._keyCodeToIdentifier(cb):this._charCodeToIdentifier(bY);

if(!(this.__hj[bX]==m&&ca==m)){this._idealKeyHandler(cb,bY,ca,bW);
}this.__hj[bX]=ca;
}else{this._idealKeyHandler(cb,bY,ca,bW);
}this.__hq(bW.target,ca,cb);
},"webkit":function(cc){var cf=0;
var cd=0;
var ce=cc.type;
if(qx.bom.client.Engine.VERSION<525.13){if(ce==i||ce==m){cf=this._charCode2KeyCode[cc.charCode]||cc.keyCode;
}else{if(this._charCode2KeyCode[cc.charCode]){cf=this._charCode2KeyCode[cc.charCode];
}else{cd=cc.charCode;
}}this._idealKeyHandler(cf,cd,ce,cc);
}else{cf=cc.keyCode;
this._idealKeyHandler(cf,cd,ce,cc);
if(ce==m){if(this._isNonPrintableKeyCode(cf)||this._emulateKeyPress[cf]){this._idealKeyHandler(cf,cd,k,cc);
}}this.__hj[cf]=ce;
}},"opera":function(cg){this.__hl=cg.keyCode;
this._idealKeyHandler(cg.keyCode,0,cg.type,cg);
}})),__hq:qx.core.Variant.select(l,{"gecko":function(ch,ci,cj){if(ci===m&&(cj==33||cj==34||cj==38||cj==40)&&ch.type==M&&ch.tagName.toLowerCase()===V&&ch.getAttribute(bg)!==x){if(!this.__hm){this.__hm={};
}var cl=qx.core.ObjectRegistry.toHashCode(ch);

if(this.__hm[cl]){return;
}var self=this;
this.__hm[cl]={target:ch,callback:function(cm){qx.bom.Event.stopPropagation(cm);
self.__hr(cm);
}};
var ck=qx.event.GlobalError.observeMethod(this.__hm[cl].callback);
qx.bom.Event.addNativeListener(ch,k,ck);
}},"default":null}),__hr:qx.event.GlobalError.observeMethod(qx.core.Variant.select(l,{"mshtml":function(cn){cn=window.event||cn;

if(this._charCode2KeyCode[cn.keyCode]){this._idealKeyHandler(this._charCode2KeyCode[cn.keyCode],0,cn.type,cn);
}else{this._idealKeyHandler(0,cn.keyCode,cn.type,cn);
}},"gecko":function(co){var cr=this._keyCodeFix[co.keyCode]||co.keyCode;
var cp=co.charCode;
var cq=co.type;
this._idealKeyHandler(cr,cp,cq,co);
},"webkit":function(cs){if(qx.bom.client.Engine.VERSION<525.13){var cv=0;
var ct=0;
var cu=cs.type;

if(cu==i||cu==m){cv=this._charCode2KeyCode[cs.charCode]||cs.keyCode;
}else{if(this._charCode2KeyCode[cs.charCode]){cv=this._charCode2KeyCode[cs.charCode];
}else{ct=cs.charCode;
}}this._idealKeyHandler(cv,ct,cu,cs);
}else{if(this._charCode2KeyCode[cs.keyCode]){this._idealKeyHandler(this._charCode2KeyCode[cs.keyCode],0,cs.type,cs);
}else{this._idealKeyHandler(0,cs.keyCode,cs.type,cs);
}}},"opera":function(cw){var cy=cw.keyCode;
var cx=cw.type;
if(cy!=this.__hl){this._idealKeyHandler(0,this.__hl,cx,cw);
}else{if(this._keyCodeToIdentifierMap[cw.keyCode]){this._idealKeyHandler(cw.keyCode,0,cw.type,cw);
}else{this._idealKeyHandler(0,cw.keyCode,cw.type,cw);
}}}})),_idealKeyHandler:function(cz,cA,cB,cC){var cD;
if(cz||(!cz&&!cA)){cD=this._keyCodeToIdentifier(cz);
this._fireSequenceEvent(cC,cB,cD);
}else{cD=this._charCodeToIdentifier(cA);
this._fireSequenceEvent(cC,k,cD);
this._fireInputEvent(cC,cA);
}},_specialCharCodeMap:{8:N,9:T,13:h,27:P,32:bq},_emulateKeyPress:qx.core.Variant.select(l,{"mshtml":{8:true,9:true},"webkit":{8:true,9:true,27:true},"default":{}}),_keyCodeToIdentifierMap:{16:bb,17:U,18:b,20:H,224:v,37:bp,38:bm,39:I,40:bn,33:d,34:G,35:n,36:R,45:p,46:B,112:K,113:bh,114:r,115:W,116:bo,117:t,118:bk,119:q,120:bi,121:F,122:bl,123:bc,144:j,44:bt,145:z,19:ba,91:qx.bom.client.Platform.MAC?O:bj,92:bj,93:qx.bom.client.Platform.MAC?O:y},_numpadToCharCode:{96:g.charCodeAt(0),97:A.charCodeAt(0),98:E.charCodeAt(0),99:be.charCodeAt(0),100:L.charCodeAt(0),101:Y.charCodeAt(0),102:bd.charCodeAt(0),103:w.charCodeAt(0),104:D.charCodeAt(0),105:f.charCodeAt(0),106:C.charCodeAt(0),107:bu.charCodeAt(0),109:e.charCodeAt(0),110:bf.charCodeAt(0),111:o.charCodeAt(0)},_charCodeA:br.charCodeAt(0),_charCodeZ:J.charCodeAt(0),_charCode0:g.charCodeAt(0),_charCode9:f.charCodeAt(0),_isNonPrintableKeyCode:function(cE){return this._keyCodeToIdentifierMap[cE]?true:false;
},_isIdentifiableKeyCode:function(cF){if(cF>=this._charCodeA&&cF<=this._charCodeZ){return true;
}if(cF>=this._charCode0&&cF<=this._charCode9){return true;
}if(this._specialCharCodeMap[cF]){return true;
}if(this._numpadToCharCode[cF]){return true;
}if(this._isNonPrintableKeyCode(cF)){return true;
}return false;
},_keyCodeToIdentifier:function(cG){if(this._isIdentifiableKeyCode(cG)){var cH=this._numpadToCharCode[cG];

if(cH){return String.fromCharCode(cH);
}return (this._keyCodeToIdentifierMap[cG]||this._specialCharCodeMap[cG]||String.fromCharCode(cG));
}else{return Q;
}},_charCodeToIdentifier:function(cI){return this._specialCharCodeMap[cI]||String.fromCharCode(cI).toUpperCase();
},_identifierToKeyCode:function(cJ){return qx.event.handler.Keyboard._identifierToKeyCodeMap[cJ]||cJ.charCodeAt(0);
}},destruct:function(){this._stopKeyObserver();
this.__hl=this.__hg=this.__hh=this.__hi=this.__hj=null;
},defer:function(cK,cL){qx.event.Registration.addHandler(cK);
if(!cK._identifierToKeyCodeMap){cK._identifierToKeyCodeMap={};

for(var cM in cL._keyCodeToIdentifierMap){cK._identifierToKeyCodeMap[cL._keyCodeToIdentifierMap[cM]]=parseInt(cM,10);
}
for(var cM in cL._specialCharCodeMap){cK._identifierToKeyCodeMap[cL._specialCharCodeMap[cM]]=parseInt(cM,10);
}}
if(qx.core.Variant.isSet(l,c)){cL._charCode2KeyCode={13:13,27:27};
}else if(qx.core.Variant.isSet(l,bs)){cL._keyCodeFix={12:cL._identifierToKeyCode(j)};
}else if(qx.core.Variant.isSet(l,S)){if(qx.bom.client.Engine.VERSION<525.13){cL._charCode2KeyCode={63289:cL._identifierToKeyCode(j),63276:cL._identifierToKeyCode(d),63277:cL._identifierToKeyCode(G),63275:cL._identifierToKeyCode(n),63273:cL._identifierToKeyCode(R),63234:cL._identifierToKeyCode(bp),63232:cL._identifierToKeyCode(bm),63235:cL._identifierToKeyCode(I),63233:cL._identifierToKeyCode(bn),63272:cL._identifierToKeyCode(B),63302:cL._identifierToKeyCode(p),63236:cL._identifierToKeyCode(K),63237:cL._identifierToKeyCode(bh),63238:cL._identifierToKeyCode(r),63239:cL._identifierToKeyCode(W),63240:cL._identifierToKeyCode(bo),63241:cL._identifierToKeyCode(t),63242:cL._identifierToKeyCode(bk),63243:cL._identifierToKeyCode(q),63244:cL._identifierToKeyCode(bi),63245:cL._identifierToKeyCode(F),63246:cL._identifierToKeyCode(bl),63247:cL._identifierToKeyCode(bc),63248:cL._identifierToKeyCode(bt),3:cL._identifierToKeyCode(h),12:cL._identifierToKeyCode(j),13:cL._identifierToKeyCode(h)};
}else{cL._charCode2KeyCode={13:13,27:27};
}}}});
})();
(function(){var k="alias",j="copy",i="blur",h="mouseout",g="keydown",f="Ctrl",d="Shift",c="mousemove",b="move",a="mouseover",A="Alt",z="keyup",y="mouseup",x="dragend",w="on",v="mousedown",u="qxDraggable",t="drag",s="drop",r="qxDroppable",p="qx.event.handler.DragDrop",q="droprequest",n="dragstart",o="dragchange",l="dragleave",m="dragover";
qx.Class.define(p,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(B){qx.core.Object.call(this);
this.__hs=B;
this.__ht=B.getWindow().document.documentElement;
this.__hs.addListener(this.__ht,v,this._onMouseDown,this);
this.__hF();
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{dragstart:1,dragend:1,dragover:1,dragleave:1,drop:1,drag:1,dragchange:1,droprequest:1},IGNORE_CAN_HANDLE:true},members:{__hs:null,__ht:null,__hu:null,__hv:null,__hw:null,__hx:null,__hy:null,__hz:null,__hA:null,__hB:null,__hC:false,__hD:0,__hE:0,canHandleEvent:function(C,D){},registerEvent:function(E,F,G){},unregisterEvent:function(H,I,J){},addType:function(K){this.__hw[K]=true;
},addAction:function(L){this.__hx[L]=true;
},supportsType:function(M){return !!this.__hw[M];
},supportsAction:function(N){return !!this.__hx[N];
},getData:function(O){if(!this.__hM||!this.__hu){throw new Error("This method must not be used outside the drop event listener!");
}
if(!this.__hw[O]){throw new Error("Unsupported data type: "+O+"!");
}
if(!this.__hz[O]){this.__hA=O;
this.__hH(q,this.__hv,this.__hu,false);
}
if(!this.__hz[O]){throw new Error("Please use a droprequest listener to the drag source to fill the manager with data!");
}return this.__hz[O]||null;
},getCurrentAction:function(){return this.__hB;
},addData:function(P,Q){this.__hz[P]=Q;
},getCurrentType:function(){return this.__hA;
},isSessionActive:function(){return this.__hC;
},__hF:function(){this.__hw={};
this.__hx={};
this.__hy={};
this.__hz={};
},__hG:function(){if(this.__hv==null){return;
}var T=this.__hx;
var R=this.__hy;
var S=null;

if(this.__hM){if(R.Shift&&R.Ctrl&&T.alias){S=k;
}else if(R.Shift&&R.Alt&&T.copy){S=j;
}else if(R.Shift&&T.move){S=b;
}else if(R.Alt&&T.alias){S=k;
}else if(R.Ctrl&&T.copy){S=j;
}else if(T.move){S=b;
}else if(T.copy){S=j;
}else if(T.alias){S=k;
}}
if(S!=this.__hB){this.__hB=S;
this.__hH(o,this.__hv,this.__hu,false);
}},__hH:function(U,V,W,X,Y){var bb=qx.event.Registration;
var ba=bb.createEvent(U,qx.event.type.Drag,[X,Y]);

if(V!==W){ba.setRelatedTarget(W);
}return bb.dispatchEvent(V,ba);
},__hI:function(bc){while(bc&&bc.nodeType==1){if(bc.getAttribute(u)==w){return bc;
}bc=bc.parentNode;
}return null;
},__hJ:function(bd){while(bd&&bd.nodeType==1){if(bd.getAttribute(r)==w){return bd;
}bd=bd.parentNode;
}return null;
},__hK:function(){this.__hv=null;
this.__hs.removeListener(this.__ht,c,this._onMouseMove,this,true);
this.__hs.removeListener(this.__ht,y,this._onMouseUp,this,true);
qx.event.Registration.removeListener(window,i,this._onWindowBlur,this);
this.__hF();
},__hL:function(){if(this.__hC){this.__hs.removeListener(this.__ht,a,this._onMouseOver,this,true);
this.__hs.removeListener(this.__ht,h,this._onMouseOut,this,true);
this.__hs.removeListener(this.__ht,g,this._onKeyDown,this,true);
this.__hs.removeListener(this.__ht,z,this._onKeyUp,this,true);
this.__hH(x,this.__hv,this.__hu,false);
this.__hC=false;
}this.__hM=false;
this.__hu=null;
this.__hK();
},__hM:false,_onWindowBlur:function(e){this.__hL();
},_onKeyDown:function(e){var be=e.getKeyIdentifier();

switch(be){case A:case f:case d:if(!this.__hy[be]){this.__hy[be]=true;
this.__hG();
}}},_onKeyUp:function(e){var bf=e.getKeyIdentifier();

switch(bf){case A:case f:case d:if(this.__hy[bf]){this.__hy[bf]=false;
this.__hG();
}}},_onMouseDown:function(e){if(this.__hC){return;
}var bg=this.__hI(e.getTarget());

if(bg){this.__hD=e.getDocumentLeft();
this.__hE=e.getDocumentTop();
this.__hv=bg;
this.__hs.addListener(this.__ht,c,this._onMouseMove,this,true);
this.__hs.addListener(this.__ht,y,this._onMouseUp,this,true);
qx.event.Registration.addListener(window,i,this._onWindowBlur,this);
}},_onMouseUp:function(e){if(this.__hM){this.__hH(s,this.__hu,this.__hv,false,e);
}if(this.__hC){e.stopPropagation();
}this.__hL();
},_onMouseMove:function(e){if(this.__hC){if(!this.__hH(t,this.__hv,this.__hu,true,e)){this.__hL();
}}else{if(Math.abs(e.getDocumentLeft()-this.__hD)>3||Math.abs(e.getDocumentTop()-this.__hE)>3){if(this.__hH(n,this.__hv,this.__hu,true,e)){this.__hC=true;
this.__hs.addListener(this.__ht,a,this._onMouseOver,this,true);
this.__hs.addListener(this.__ht,h,this._onMouseOut,this,true);
this.__hs.addListener(this.__ht,g,this._onKeyDown,this,true);
this.__hs.addListener(this.__ht,z,this._onKeyUp,this,true);
var bh=this.__hy;
bh.Ctrl=e.isCtrlPressed();
bh.Shift=e.isShiftPressed();
bh.Alt=e.isAltPressed();
this.__hG();
}else{this.__hH(x,this.__hv,this.__hu,false);
this.__hK();
}}}},_onMouseOver:function(e){var bi=e.getTarget();
var bj=this.__hJ(bi);

if(bj&&bj!=this.__hu){this.__hM=this.__hH(m,bj,this.__hv,true,e);
this.__hu=bj;
this.__hG();
}},_onMouseOut:function(e){var bl=this.__hJ(e.getTarget());
var bk=this.__hJ(e.getRelatedTarget());

if(bl&&bl!==bk&&bl==this.__hu){this.__hH(l,this.__hu,bk,false,e);
this.__hu=null;
this.__hM=false;
qx.event.Timer.once(this.__hG,this,0);
}}},destruct:function(){this.__hv=this.__hu=this.__hs=this.__ht=this.__hw=this.__hx=this.__hy=this.__hz=null;
},defer:function(bm){qx.event.Registration.addHandler(bm);
}});
})();
(function(){var c="qx.event.handler.Appear",b="disappear",a="appear";
qx.Class.define(c,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(d){qx.core.Object.call(this);
this.__hN=d;
this.__hO={};
qx.event.handler.Appear.__hP[this.$$hash]=this;
},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{appear:true,disappear:true},TARGET_CHECK:qx.event.IEventHandler.TARGET_DOMNODE,IGNORE_CAN_HANDLE:true,__hP:{},refresh:function(){var e=this.__hP;

for(var f in e){e[f].refresh();
}}},members:{__hN:null,__hO:null,canHandleEvent:function(g,h){},registerEvent:function(i,j,k){var l=qx.core.ObjectRegistry.toHashCode(i)+j;
var m=this.__hO;

if(m&&!m[l]){m[l]=i;
i.$$displayed=i.offsetWidth>0;
}},unregisterEvent:function(n,o,p){var q=qx.core.ObjectRegistry.toHashCode(n)+o;
var r=this.__hO;

if(!r){return;
}
if(r[q]){delete r[q];
}},refresh:function(){var v=this.__hO;
var w;

for(var u in v){w=v[u];
var s=w.offsetWidth>0;

if((!!w.$$displayed)!==s){w.$$displayed=s;
var t=qx.event.Registration.createEvent(s?a:b);
this.__hN.dispatchEvent(w,t);
}}}},destruct:function(){this.__hN=this.__hO=null;
delete qx.event.handler.Appear.__hP[this.$$hash];
},defer:function(x){qx.event.Registration.addHandler(x);
}});
})();
(function(){var b="abstract",a="qx.event.dispatch.AbstractBubbling";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.event.IEventDispatcher,type:b,construct:function(c){this._manager=c;
},members:{_getParent:function(d){throw new Error("Missing implementation");
},canDispatchEvent:function(e,event,f){return event.getBubbles();
},dispatchEvent:function(g,event,h){var parent=g;
var s=this._manager;
var p,w;
var n;
var r,u;
var t;
var v=[];
p=s.getListeners(g,h,true);
w=s.getListeners(g,h,false);

if(p){v.push(p);
}
if(w){v.push(w);
}var parent=this._getParent(g);
var l=[];
var k=[];
var m=[];
var q=[];
while(parent!=null){p=s.getListeners(parent,h,true);

if(p){m.push(p);
q.push(parent);
}w=s.getListeners(parent,h,false);

if(w){l.push(w);
k.push(parent);
}parent=this._getParent(parent);
}event.setEventPhase(qx.event.type.Event.CAPTURING_PHASE);

for(var i=m.length-1;i>=0;i--){t=q[i];
event.setCurrentTarget(t);
n=m[i];

for(var j=0,o=n.length;j<o;j++){r=n[j];
u=r.context||t;
r.handler.call(u,event);
}
if(event.getPropagationStopped()){return;
}}event.setEventPhase(qx.event.type.Event.AT_TARGET);
event.setCurrentTarget(g);

for(var i=0,x=v.length;i<x;i++){n=v[i];

for(var j=0,o=n.length;j<o;j++){r=n[j];
u=r.context||g;
r.handler.call(u,event);
}
if(event.getPropagationStopped()){return;
}}event.setEventPhase(qx.event.type.Event.BUBBLING_PHASE);

for(var i=0,x=l.length;i<x;i++){t=k[i];
event.setCurrentTarget(t);
n=l[i];

for(var j=0,o=n.length;j<o;j++){r=n[j];
u=r.context||t;
r.handler.call(u,event);
}
if(event.getPropagationStopped()){return;
}}}}});
})();
(function(){var a="qx.event.dispatch.DomBubbling";
qx.Class.define(a,{extend:qx.event.dispatch.AbstractBubbling,statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL},members:{_getParent:function(b){return b.parentNode;
},canDispatchEvent:function(c,event,d){return c.nodeType!==undefined&&event.getBubbles();
}},defer:function(e){qx.event.Registration.addDispatcher(e);
}});
})();
(function(){var q="mshtml",p="",o="qx.client",n=" ",m=">",k="<",h="='",g="none",f="<INPUT TYPE='RADIO' NAME='RADIOTEST' VALUE='Second Choice'>",d="qx.bom.Element",a="' ",c="div",b="></";
qx.Class.define(d,{statics:{__hQ:{"onload":true,"onpropertychange":true,"oninput":true,"onchange":true,"name":true,"type":true,"checked":true,"disabled":true},__hR:{},__hS:{},allowCreationWithMarkup:function(r){if(!r){r=window;
}var s=r.location.href;

if(qx.bom.Element.__hS[s]==undefined){try{r.document.createElement(f);
qx.bom.Element.__hS[s]=true;
}catch(e){qx.bom.Element.__hS[s]=false;
}}return qx.bom.Element.__hS[s];
},getHelperElement:function(t){if(!t){t=window;
}var v=t.location.href;

if(!qx.bom.Element.__hR[v]){var u=qx.bom.Element.__hR[v]=t.document.createElement(c);
if(qx.bom.client.Engine.WEBKIT){u.style.display=g;
t.document.body.appendChild(u);
}}return qx.bom.Element.__hR[v];
},create:function(name,w,x){if(!x){x=window;
}
if(!name){throw new Error("The tag name is missing!");
}var z=this.__hQ;
var y=p;

for(var B in w){if(z[B]){y+=B+h+w[B]+a;
}}var C;
if(y!=p){if(qx.bom.Element.allowCreationWithMarkup(x)){C=x.document.createElement(k+name+n+y+m);
}else{var A=qx.bom.Element.getHelperElement(x);
A.innerHTML=k+name+n+y+b+name+m;
C=A.firstChild;
}}else{C=x.document.createElement(name);
}
for(var B in w){if(!z[B]){qx.bom.element.Attribute.set(C,B,w[B]);
}}return C;
},empty:function(D){return D.innerHTML=p;
},addListener:function(E,F,G,self,H){return qx.event.Registration.addListener(E,F,G,self,H);
},removeListener:function(I,J,K,self,L){return qx.event.Registration.removeListener(I,J,K,self,L);
},removeListenerById:function(M,N){return qx.event.Registration.removeListenerById(M,N);
},hasListener:function(O,P,Q){return qx.event.Registration.hasListener(O,P,Q);
},focus:function(R){qx.event.Registration.getManager(R).getHandler(qx.event.handler.Focus).focus(R);
},blur:function(S){qx.event.Registration.getManager(S).getHandler(qx.event.handler.Focus).blur(S);
},activate:function(T){qx.event.Registration.getManager(T).getHandler(qx.event.handler.Focus).activate(T);
},deactivate:function(U){qx.event.Registration.getManager(U).getHandler(qx.event.handler.Focus).deactivate(U);
},capture:function(V,W){qx.event.Registration.getManager(V).getDispatcher(qx.event.dispatch.MouseCapture).activateCapture(V,W);
},releaseCapture:function(X){qx.event.Registration.getManager(X).getDispatcher(qx.event.dispatch.MouseCapture).releaseCapture(X);
},matchesSelector:function(Y,ba){if(ba){return qx.bom.Selector.query(ba,Y.parentNode).length>0;
}else{return false;
}},clone:function(bb,bc){var bf;

if(bc||(qx.core.Variant.isSet(o,q)&&!qx.xml.Document.isXmlDocument(bb))){var bj=qx.event.Registration.getManager(bb);
var bd=qx.dom.Hierarchy.getDescendants(bb);
bd.push(bb);
}if(qx.core.Variant.isSet(o,q)){for(var i=0,l=bd.length;i<l;i++){bj.toggleAttachedEvents(bd[i],false);
}}var bf=bb.cloneNode(true);
if(qx.core.Variant.isSet(o,q)){for(var i=0,l=bd.length;i<l;i++){bj.toggleAttachedEvents(bd[i],true);
}}if(bc===true){var bm=qx.dom.Hierarchy.getDescendants(bf);
bm.push(bf);
var be,bh,bl,bg;

for(var i=0,bk=bd.length;i<bk;i++){bl=bd[i];
be=bj.serializeListeners(bl);

if(be.length>0){bh=bm[i];

for(var j=0,bi=be.length;j<bi;j++){bg=be[j];
bj.addListener(bh,bg.type,bg.handler,bg.self,bg.capture);
}}}}return bf;
}}});
})();
(function(){var c="landscape",b="qx.event.type.Orientation",a="portrait";
qx.Class.define(b,{extend:qx.event.type.Event,members:{__hT:null,__hU:null,init:function(d,e){qx.event.type.Event.prototype.init.call(this,false,false);
this.__hT=d;
this.__hU=e;
return this;
},clone:function(f){var g=qx.event.type.Event.prototype.clone.call(this,f);
g.__hT=this.__hT;
g.__hU=this.__hU;
return g;
},getOrientation:function(){return this.__hT;
},isLandscape:function(){return this.__hU==c;
},isPortrait:function(){return this.__hU==a;
}}});
})();
(function(){var a="qx.event.type.Dom";
qx.Class.define(a,{extend:qx.event.type.Native,statics:{SHIFT_MASK:1,CTRL_MASK:2,ALT_MASK:4,META_MASK:8},members:{_cloneNativeEvent:function(b,c){var c=qx.event.type.Native.prototype._cloneNativeEvent.call(this,b,c);
c.shiftKey=b.shiftKey;
c.ctrlKey=b.ctrlKey;
c.altKey=b.altKey;
c.metaKey=b.metaKey;
return c;
},getModifiers:function(){var e=0;
var d=this._native;

if(d.shiftKey){e|=qx.event.type.Dom.SHIFT_MASK;
}
if(d.ctrlKey){e|=qx.event.type.Dom.CTRL_MASK;
}
if(d.altKey){e|=qx.event.type.Dom.ALT_MASK;
}
if(d.metaKey){e|=qx.event.type.Dom.META_MASK;
}return e;
},isCtrlPressed:function(){return this._native.ctrlKey;
},isShiftPressed:function(){return this._native.shiftKey;
},isAltPressed:function(){return this._native.altKey;
},isMetaPressed:function(){return this._native.metaKey;
},isCtrlOrCommandPressed:function(){if(qx.bom.client.Platform.MAC){return this._native.metaKey;
}else{return this._native.ctrlKey;
}}}});
})();
(function(){var c="touchcancel",b="qx.event.type.Touch",a="touchend";
qx.Class.define(b,{extend:qx.event.type.Dom,members:{_cloneNativeEvent:function(d,e){var e=qx.event.type.Dom.prototype._cloneNativeEvent.call(this,d,e);
e.pageX=d.pageX;
e.pageY=d.pageY;
e.layerX=d.layerX;
e.layerY=d.layerY;
e.scale=d.scale;
e.rotation=d.rotation;
e.srcElement=d.srcElement;
e.targetTouches=[];

for(var i=0;i<d.targetTouches.length;i++){e.targetTouches[i]=d.targetTouches[i];
}e.changedTouches=[];

for(var i=0;i<d.changedTouches.length;i++){e.changedTouches[i]=d.changedTouches[i];
}e.touches=[];

for(var i=0;i<d.touches.length;i++){e.touches[i]=d.touches[i];
}return e;
},stop:function(){this.stopPropagation();
},getAllTouches:function(){return this._native.touches;
},getTargetTouches:function(){return this._native.targetTouches;
},getChangedTargetTouches:function(){return this._native.changedTouches;
},isMultiTouch:function(){return this.__hW().length>1;
},getScale:function(){return this._native.scale;
},getRotation:function(){return this._native.rotation;
},getDocumentLeft:function(f){return this.__hV(f).pageX;
},getDocumentTop:function(g){return this.__hV(g).pageY;
},getScreenLeft:function(h){return this.__hV(h).screenX;
},getScreenTop:function(j){return this.__hV(j).screenY;
},getViewportLeft:function(k){return this.__hV(k).clientX;
},getViewportTop:function(l){return this.__hV(l).clientY;
},getIdentifier:function(m){return this.__hV(m).identifier;
},__hV:function(n){n=n==null?0:n;
return this.__hW()[n];
},__hW:function(){var o=(this._isTouchEnd()?this.getChangedTargetTouches():this.getTargetTouches());
return o;
},_isTouchEnd:function(){return (this.getType()==a||this.getType()==c);
}}});
})();
(function(){var a="qx.event.type.Tap";
qx.Class.define(a,{extend:qx.event.type.Touch,members:{_isTouchEnd:function(){return true;
}}});
})();
(function(){var a="qx.event.type.Swipe";
qx.Class.define(a,{extend:qx.event.type.Touch,members:{_cloneNativeEvent:function(b,c){var c=qx.event.type.Touch.prototype._cloneNativeEvent.call(this,b,c);
c.swipe=b.swipe;
return c;
},_isTouchEnd:function(){return true;
},getStartTime:function(){return this._native.swipe.startTime;
},getDuration:function(){return this._native.swipe.duration;
},getAxis:function(){return this._native.swipe.axis;
},getDirection:function(){return this._native.swipe.direction;
},getVelocity:function(){return this._native.swipe.velocity;
},getDistance:function(){return this._native.swipe.distance;
}}});
})();
(function(){var h="left",g="right",f="middle",e="none",d="click",c="contextmenu",b="qx.event.type.Mouse",a="qx.client";
qx.Class.define(b,{extend:qx.event.type.Dom,members:{_cloneNativeEvent:function(i,j){var j=qx.event.type.Dom.prototype._cloneNativeEvent.call(this,i,j);
j.button=i.button;
j.clientX=i.clientX;
j.clientY=i.clientY;
j.pageX=i.pageX;
j.pageY=i.pageY;
j.screenX=i.screenX;
j.screenY=i.screenY;
j.wheelDelta=i.wheelDelta;
j.detail=i.detail;
j.srcElement=i.srcElement;
j.target=i.target;
return j;
},__hX:{0:h,2:g,1:f},__hY:{1:h,2:g,4:f},stop:function(){this.stopPropagation();
},getButton:function(){switch(this._type){case c:return g;
case d:if(this.__ia){return this.__ia();
}default:if(this._native.target!==undefined){return this.__hX[this._native.button]||e;
}else{return this.__hY[this._native.button]||e;
}}},__ia:qx.core.Variant.select(a,{"mshtml":function(){return h;
},"default":null}),isLeftPressed:function(){return this.getButton()===h;
},isMiddlePressed:function(){return this.getButton()===f;
},isRightPressed:function(){return this.getButton()===g;
},getRelatedTarget:function(){return this._relatedTarget;
},getViewportLeft:function(){return this._native.clientX;
},getViewportTop:function(){return this._native.clientY;
},getDocumentLeft:function(){if(this._native.pageX!==undefined){return this._native.pageX;
}else{var k=qx.dom.Node.getWindow(this._native.srcElement);
return this._native.clientX+qx.bom.Viewport.getScrollLeft(k);
}},getDocumentTop:function(){if(this._native.pageY!==undefined){return this._native.pageY;
}else{var l=qx.dom.Node.getWindow(this._native.srcElement);
return this._native.clientY+qx.bom.Viewport.getScrollTop(l);
}},getScreenLeft:function(){return this._native.screenX;
},getScreenTop:function(){return this._native.screenY;
}}});
})();
(function(){var c="qx.client",b="chrome",a="qx.event.type.MouseWheel";
qx.Class.define(a,{extend:qx.event.type.Mouse,members:{stop:function(){this.stopPropagation();
this.preventDefault();
},getWheelDelta:qx.core.Variant.select(c,{"default":function(){return -(this._native.wheelDelta/40);
},"gecko":function(){return this._native.detail;
},"webkit":function(){if(qx.bom.client.Browser.NAME==b){if(qx.bom.client.Platform.MAC){return -(this._native.wheelDelta/60);
}else{return -(this._native.wheelDelta/120);
}}else{if(qx.bom.client.Platform.WIN){var d=120;
if(qx.bom.client.Engine.VERSION==533.16){d=1200;
}}else{d=40;
if(qx.bom.client.Engine.VERSION==533.16||qx.bom.client.Engine.VERSION==533.17||qx.bom.client.Engine.VERSION==533.18){d=1200;
}}return -(this._native.wheelDelta/d);
}}})}});
})();
(function(){var j="qx.client",i="ie",h="msie",g="android",f="operamini",e="mobile chrome",d=")(/| )([0-9]+\.[0-9])",c="iemobile",b="opera mobi",a="Mobile Safari",x="operamobile",w="mobile safari",v="IEMobile|Maxthon|MSIE",u="qx.bom.client.Browser",t="opera mini",s="(",r="opera",q="mshtml",p="Opera Mini|Opera Mobi|Opera",o="AdobeAIR|Titanium|Fluid|Chrome|Android|Epiphany|Konqueror|iCab|OmniWeb|Maxthon|Pre|Mobile Safari|Safari",m="webkit",n="5.0",k="prism|Fennec|Camino|Kmeleon|Galeon|Netscape|SeaMonkey|Firefox",l="Mobile/";
qx.Bootstrap.define(u,{statics:{UNKNOWN:true,NAME:"unknown",TITLE:"unknown 0.0",VERSION:0.0,FULLVERSION:"0.0.0",__ib:function(y){var z=navigator.userAgent;
var B=new RegExp(s+y+d);
var C=z.match(B);

if(!C){return;
}var name=C[1].toLowerCase();
var A=C[3];
if(z.match(/Version(\/| )([0-9]+\.[0-9])/)){A=RegExp.$2;
}
if(qx.core.Variant.isSet(j,m)){if(name===g){name=e;
}else if(z.indexOf(a)!==-1||z.indexOf(l)!==-1){name=w;
}}else if(qx.core.Variant.isSet(j,q)){if(name===h){name=i;
if(qx.bom.client.System.WINCE&&name===i){name=c;
A=n;
}}}else if(qx.core.Variant.isSet(j,r)){if(name===b){name=x;
}else if(name===t){name=f;
}}this.NAME=name;
this.FULLVERSION=A;
this.VERSION=parseFloat(A,10);
this.TITLE=name+" "+this.VERSION;
this.UNKNOWN=false;
}},defer:qx.core.Variant.select(j,{"webkit":function(D){D.__ib(o);
},"gecko":function(E){E.__ib(k);
},"mshtml":function(F){F.__ib(v);
},"opera":function(G){G.__ib(p);
}})});
})();
(function(){var f="qx.client",e="qx.dom.Hierarchy",d="previousSibling",c="*",b="nextSibling",a="parentNode";
qx.Class.define(e,{statics:{getNodeIndex:function(g){var h=0;

while(g&&(g=g.previousSibling)){h++;
}return h;
},getElementIndex:function(i){var j=0;
var k=qx.dom.Node.ELEMENT;

while(i&&(i=i.previousSibling)){if(i.nodeType==k){j++;
}}return j;
},getNextElementSibling:function(l){while(l&&(l=l.nextSibling)&&!qx.dom.Node.isElement(l)){continue;
}return l||null;
},getPreviousElementSibling:function(m){while(m&&(m=m.previousSibling)&&!qx.dom.Node.isElement(m)){continue;
}return m||null;
},contains:qx.core.Variant.select(f,{"webkit|mshtml|opera":function(n,o){if(qx.dom.Node.isDocument(n)){var p=qx.dom.Node.getDocument(o);
return n&&p==n;
}else if(qx.dom.Node.isDocument(o)){return false;
}else{return n.contains(o);
}},"gecko":function(q,r){return !!(q.compareDocumentPosition(r)&16);
},"default":function(s,t){while(t){if(s==t){return true;
}t=t.parentNode;
}return false;
}}),isRendered:qx.core.Variant.select(f,{"mshtml":function(u){if(!u.parentNode||!u.offsetParent){return false;
}var v=u.ownerDocument||u.document;
return v.body.contains(u);
},"gecko":function(w){var x=w.ownerDocument||w.document;
return !!(x.compareDocumentPosition(w)&16);
},"default":function(y){if(!y.parentNode||!y.offsetParent){return false;
}var z=y.ownerDocument||y.document;
return z.body.contains(y);
}}),isDescendantOf:function(A,B){return this.contains(B,A);
},getCommonParent:qx.core.Variant.select(f,{"mshtml|opera":function(C,D){if(C===D){return C;
}
while(C&&qx.dom.Node.isElement(C)){if(C.contains(D)){return C;
}C=C.parentNode;
}return null;
},"default":function(E,F){if(E===F){return E;
}var G={};
var J=qx.core.ObjectRegistry;
var I,H;

while(E||F){if(E){I=J.toHashCode(E);

if(G[I]){return G[I];
}G[I]=E;
E=E.parentNode;
}
if(F){H=J.toHashCode(F);

if(G[H]){return G[H];
}G[H]=F;
F=F.parentNode;
}}return null;
}}),getAncestors:function(K){return this._recursivelyCollect(K,a);
},getChildElements:function(L){L=L.firstChild;

if(!L){return [];
}var M=this.getNextSiblings(L);

if(L.nodeType===1){M.unshift(L);
}return M;
},getDescendants:function(N){return qx.lang.Array.fromCollection(N.getElementsByTagName(c));
},getFirstDescendant:function(O){O=O.firstChild;

while(O&&O.nodeType!=1){O=O.nextSibling;
}return O;
},getLastDescendant:function(P){P=P.lastChild;

while(P&&P.nodeType!=1){P=P.previousSibling;
}return P;
},getPreviousSiblings:function(Q){return this._recursivelyCollect(Q,d);
},getNextSiblings:function(R){return this._recursivelyCollect(R,b);
},_recursivelyCollect:function(S,T){var U=[];

while(S=S[T]){if(S.nodeType==1){U.push(S);
}}return U;
},getSiblings:function(V){return this.getPreviousSiblings(V).reverse().concat(this.getNextSiblings(V));
},isEmpty:function(W){W=W.firstChild;

while(W){if(W.nodeType===qx.dom.Node.ELEMENT||W.nodeType===qx.dom.Node.TEXT){return false;
}W=W.nextSibling;
}return true;
},cleanWhitespace:function(X){var Y=X.firstChild;

while(Y){var ba=Y.nextSibling;

if(Y.nodeType==3&&!/\S/.test(Y.nodeValue)){X.removeChild(Y);
}Y=ba;
}}}});
})();
(function(){var a="qx.event.type.KeyInput";
qx.Class.define(a,{extend:qx.event.type.Dom,members:{init:function(b,c,d){qx.event.type.Dom.prototype.init.call(this,b,c,null,true,true);
this._charCode=d;
return this;
},clone:function(e){var f=qx.event.type.Dom.prototype.clone.call(this,e);
f._charCode=this._charCode;
return f;
},getCharCode:function(){return this._charCode;
},getChar:function(){return String.fromCharCode(this._charCode);
}}});
})();
(function(){var a="qx.event.type.KeySequence";
qx.Class.define(a,{extend:qx.event.type.Dom,members:{init:function(b,c,d){qx.event.type.Dom.prototype.init.call(this,b,c,null,true,true);
this._keyCode=b.keyCode;
this._identifier=d;
return this;
},clone:function(e){var f=qx.event.type.Dom.prototype.clone.call(this,e);
f._keyCode=this._keyCode;
f._identifier=this._identifier;
return f;
},getKeyIdentifier:function(){return this._identifier;
},getKeyCode:function(){return this._keyCode;
},isPrintable:function(){return qx.event.handler.Keyboard.isPrintableKeyIdentifier(this._identifier);
}}});
})();
(function(){var j="qx.client",i="mousedown",h="mouseup",g="blur",f="focus",e="on",d="selectstart",c="DOMFocusOut",b="focusin",a="focusout",z="DOMFocusIn",y="draggesture",x="qx.event.handler.Focus",w="_applyFocus",v="deactivate",u="textarea",t="_applyActive",s='character',r="input",q="qxSelectable",o="tabIndex",p="off",m="activate",n="mshtml",k="qxKeepFocus",l="qxKeepActive";
qx.Class.define(x,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(A){qx.core.Object.call(this);
this._manager=A;
this._window=A.getWindow();
this._document=this._window.document;
this._root=this._document.documentElement;
this._body=this._document.body;
this._initObserver();
},properties:{active:{apply:t,nullable:true},focus:{apply:w,nullable:true}},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{focus:1,blur:1,focusin:1,focusout:1,activate:1,deactivate:1},IGNORE_CAN_HANDLE:true,FOCUSABLE_ELEMENTS:qx.core.Variant.select("qx.client",{"mshtml|gecko":{a:1,body:1,button:1,frame:1,iframe:1,img:1,input:1,object:1,select:1,textarea:1},"opera|webkit":{button:1,input:1,select:1,textarea:1}})},members:{__ic:null,__id:null,__ie:null,__if:null,__ig:null,__ih:null,__ii:null,__ij:null,__ik:null,__il:null,canHandleEvent:function(B,C){},registerEvent:function(D,E,F){},unregisterEvent:function(G,H,I){},focus:function(J){if(qx.core.Variant.isSet(j,n)){window.setTimeout(function(){try{J.focus();
var K=qx.bom.Selection.get(J);

if(K.length==0){var L=J.createTextRange();
L.moveStart(s,J.value.length);
L.collapse();
L.select();
}}catch(M){}},0);
}else{try{J.focus();
}catch(N){}}this.setFocus(J);
this.setActive(J);
},activate:function(O){this.setActive(O);
},blur:function(P){try{P.blur();
}catch(Q){}
if(this.getActive()===P){this.resetActive();
}
if(this.getFocus()===P){this.resetFocus();
}},deactivate:function(R){if(this.getActive()===R){this.resetActive();
}},tryActivate:function(S){var T=this.__iA(S);

if(T){this.setActive(T);
}},__im:function(U,V,W,X){var ba=qx.event.Registration;
var Y=ba.createEvent(W,qx.event.type.Focus,[U,V,X]);
ba.dispatchEvent(U,Y);
},_windowFocused:true,__in:function(){if(this._windowFocused){this._windowFocused=false;
this.__im(this._window,null,g,false);
}},__io:function(){if(!this._windowFocused){this._windowFocused=true;
this.__im(this._window,null,f,false);
}},_initObserver:qx.core.Variant.select(j,{"gecko":function(){this.__ic=qx.lang.Function.listener(this.__iu,this);
this.__id=qx.lang.Function.listener(this.__iv,this);
this.__ie=qx.lang.Function.listener(this.__it,this);
this.__if=qx.lang.Function.listener(this.__is,this);
this.__ig=qx.lang.Function.listener(this.__ip,this);
qx.bom.Event.addNativeListener(this._document,i,this.__ic,true);
qx.bom.Event.addNativeListener(this._document,h,this.__id,true);
qx.bom.Event.addNativeListener(this._window,f,this.__ie,true);
qx.bom.Event.addNativeListener(this._window,g,this.__if,true);
qx.bom.Event.addNativeListener(this._window,y,this.__ig,true);
},"mshtml":function(){this.__ic=qx.lang.Function.listener(this.__iu,this);
this.__id=qx.lang.Function.listener(this.__iv,this);
this.__ii=qx.lang.Function.listener(this.__iq,this);
this.__ij=qx.lang.Function.listener(this.__ir,this);
this.__ih=qx.lang.Function.listener(this.__ix,this);
qx.bom.Event.addNativeListener(this._document,i,this.__ic);
qx.bom.Event.addNativeListener(this._document,h,this.__id);
qx.bom.Event.addNativeListener(this._document,b,this.__ii);
qx.bom.Event.addNativeListener(this._document,a,this.__ij);
qx.bom.Event.addNativeListener(this._document,d,this.__ih);
},"webkit":function(){this.__ic=qx.lang.Function.listener(this.__iu,this);
this.__id=qx.lang.Function.listener(this.__iv,this);
this.__ij=qx.lang.Function.listener(this.__ir,this);
this.__ie=qx.lang.Function.listener(this.__it,this);
this.__if=qx.lang.Function.listener(this.__is,this);
this.__ih=qx.lang.Function.listener(this.__ix,this);
qx.bom.Event.addNativeListener(this._document,i,this.__ic,true);
qx.bom.Event.addNativeListener(this._document,h,this.__id,true);
qx.bom.Event.addNativeListener(this._document,d,this.__ih,false);
qx.bom.Event.addNativeListener(this._window,c,this.__ij,true);
qx.bom.Event.addNativeListener(this._window,f,this.__ie,true);
qx.bom.Event.addNativeListener(this._window,g,this.__if,true);
},"opera":function(){this.__ic=qx.lang.Function.listener(this.__iu,this);
this.__id=qx.lang.Function.listener(this.__iv,this);
this.__ii=qx.lang.Function.listener(this.__iq,this);
this.__ij=qx.lang.Function.listener(this.__ir,this);
qx.bom.Event.addNativeListener(this._document,i,this.__ic,true);
qx.bom.Event.addNativeListener(this._document,h,this.__id,true);
qx.bom.Event.addNativeListener(this._window,z,this.__ii,true);
qx.bom.Event.addNativeListener(this._window,c,this.__ij,true);
}}),_stopObserver:qx.core.Variant.select(j,{"gecko":function(){qx.bom.Event.removeNativeListener(this._document,i,this.__ic,true);
qx.bom.Event.removeNativeListener(this._document,h,this.__id,true);
qx.bom.Event.removeNativeListener(this._window,f,this.__ie,true);
qx.bom.Event.removeNativeListener(this._window,g,this.__if,true);
qx.bom.Event.removeNativeListener(this._window,y,this.__ig,true);
},"mshtml":function(){qx.bom.Event.removeNativeListener(this._document,i,this.__ic);
qx.bom.Event.removeNativeListener(this._document,h,this.__id);
qx.bom.Event.removeNativeListener(this._document,b,this.__ii);
qx.bom.Event.removeNativeListener(this._document,a,this.__ij);
qx.bom.Event.removeNativeListener(this._document,d,this.__ih);
},"webkit":function(){qx.bom.Event.removeNativeListener(this._document,i,this.__ic,true);
qx.bom.Event.removeNativeListener(this._document,h,this.__id,true);
qx.bom.Event.removeNativeListener(this._document,d,this.__ih,false);
qx.bom.Event.removeNativeListener(this._window,c,this.__ij,true);
qx.bom.Event.removeNativeListener(this._window,f,this.__ie,true);
qx.bom.Event.removeNativeListener(this._window,g,this.__if,true);
},"opera":function(){qx.bom.Event.removeNativeListener(this._document,i,this.__ic,true);
qx.bom.Event.removeNativeListener(this._document,h,this.__id,true);
qx.bom.Event.removeNativeListener(this._window,z,this.__ii,true);
qx.bom.Event.removeNativeListener(this._window,c,this.__ij,true);
}}),__ip:qx.event.GlobalError.observeMethod(qx.core.Variant.select(j,{"gecko":function(bb){var bc=qx.bom.Event.getTarget(bb);

if(!this.__iB(bc)){qx.bom.Event.preventDefault(bb);
}},"default":null})),__iq:qx.event.GlobalError.observeMethod(qx.core.Variant.select(j,{"mshtml":function(bd){this.__io();
var bf=qx.bom.Event.getTarget(bd);
var be=this.__iz(bf);

if(be){this.setFocus(be);
}this.tryActivate(bf);
},"opera":function(bg){var bh=qx.bom.Event.getTarget(bg);

if(bh==this._document||bh==this._window){this.__io();

if(this.__ik){this.setFocus(this.__ik);
delete this.__ik;
}
if(this.__il){this.setActive(this.__il);
delete this.__il;
}}else{this.setFocus(bh);
this.tryActivate(bh);
if(!this.__iB(bh)){bh.selectionStart=0;
bh.selectionEnd=0;
}}},"default":null})),__ir:qx.event.GlobalError.observeMethod(qx.core.Variant.select(j,{"mshtml":function(bi){if(!bi.toElement){this.__in();
this.resetFocus();
this.resetActive();
}},"webkit":function(bj){var bk=qx.bom.Event.getTarget(bj);

if(bk===this.getFocus()){this.resetFocus();
}
if(bk===this.getActive()){this.resetActive();
}},"opera":function(bl){var bm=qx.bom.Event.getTarget(bl);

if(bm==this._document){this.__in();
this.__ik=this.getFocus();
this.__il=this.getActive();
this.resetFocus();
this.resetActive();
}else{if(bm===this.getFocus()){this.resetFocus();
}
if(bm===this.getActive()){this.resetActive();
}}},"default":null})),__is:qx.event.GlobalError.observeMethod(qx.core.Variant.select(j,{"gecko":function(bn){var bo=qx.bom.Event.getTarget(bn);

if(bo===this._window||bo===this._document){this.__in();
this.resetActive();
this.resetFocus();
}},"webkit":function(bp){var bq=qx.bom.Event.getTarget(bp);

if(bq===this._window||bq===this._document){this.__in();
this.__ik=this.getFocus();
this.__il=this.getActive();
this.resetActive();
this.resetFocus();
}},"default":null})),__it:qx.event.GlobalError.observeMethod(qx.core.Variant.select(j,{"gecko":function(br){var bs=qx.bom.Event.getTarget(br);

if(bs===this._window||bs===this._document){this.__io();
bs=this._body;
}this.setFocus(bs);
this.tryActivate(bs);
},"webkit":function(bt){var bu=qx.bom.Event.getTarget(bt);

if(bu===this._window||bu===this._document){this.__io();

if(this.__ik){this.setFocus(this.__ik);
delete this.__ik;
}
if(this.__il){this.setActive(this.__il);
delete this.__il;
}}else{this.setFocus(bu);
this.tryActivate(bu);
}},"default":null})),__iu:qx.event.GlobalError.observeMethod(qx.core.Variant.select(j,{"gecko":function(bv){var bx=qx.bom.Event.getTarget(bv);
var bw=this.__iz(bx);

if(!bw){qx.bom.Event.preventDefault(bv);
}else if(bw===this._body){this.setFocus(bw);
}},"mshtml":function(by){var bB=qx.bom.Event.getTarget(by);
var bz=this.__iz(bB);

if(bz){if(!this.__iB(bB)){bB.unselectable=e;
try{document.selection.empty();
}catch(bC){}try{var bA=qx.bom.Viewport.getScrollTop();
bz.focus();
window.document.documentElement.scrollTop=bA;
}catch(bD){}}}else{qx.bom.Event.preventDefault(by);
if(!this.__iB(bB)){bB.unselectable=e;
}}},"webkit":function(bE){this.__tS(bE);
},"opera":function(bF){if(qx.bom.client.Browser.VERSION>=11){this.__tS(bF);
}else{var bI=qx.bom.Event.getTarget(bF);
var bG=this.__iz(bI);

if(!this.__iB(bI)){qx.bom.Event.preventDefault(bF);
if(bG){var bH=this.getFocus();

if(bH&&bH.selectionEnd){bH.selectionStart=0;
bH.selectionEnd=0;
bH.blur();
}if(bG){this.setFocus(bG);
}}}else if(bG){this.setFocus(bG);
}}},"default":null})),__tS:function(bJ){var bL=qx.bom.Event.getTarget(bJ);
var bK=this.__iz(bL);
if(bK){this.setFocus(bK);
}else{qx.bom.Event.preventDefault(bJ);
}},__iv:qx.event.GlobalError.observeMethod(qx.core.Variant.select(j,{"mshtml":function(bM){var bN=qx.bom.Event.getTarget(bM);

if(bN.unselectable){bN.unselectable=p;
}this.tryActivate(this.__iw(bN));
},"gecko":function(bO){var bP=qx.bom.Event.getTarget(bO);

while(bP&&bP.offsetWidth===undefined){bP=bP.parentNode;
}
if(bP){this.tryActivate(bP);
}},"webkit|opera":function(bQ){var bR=qx.bom.Event.getTarget(bQ);
this.tryActivate(this.__iw(bR));
},"default":null})),__iw:qx.event.GlobalError.observeMethod(qx.core.Variant.select(j,{"mshtml|webkit":function(bS){var bT=this.getFocus();

if(bT&&bS!=bT&&(bT.nodeName.toLowerCase()===r||bT.nodeName.toLowerCase()===u)){bS=bT;
}return bS;
},"default":function(bU){return bU;
}})),__ix:qx.event.GlobalError.observeMethod(qx.core.Variant.select(j,{"mshtml|webkit":function(bV){var bW=qx.bom.Event.getTarget(bV);

if(!this.__iB(bW)){qx.bom.Event.preventDefault(bV);
}},"default":null})),__iy:function(bX){var bY=qx.bom.element.Attribute.get(bX,o);

if(bY>=1){return true;
}var ca=qx.event.handler.Focus.FOCUSABLE_ELEMENTS;

if(bY>=0&&ca[bX.tagName]){return true;
}return false;
},__iz:function(cb){while(cb&&cb.nodeType===1){if(cb.getAttribute(k)==e){return null;
}
if(this.__iy(cb)){return cb;
}cb=cb.parentNode;
}return this._body;
},__iA:function(cc){var cd=cc;

while(cc&&cc.nodeType===1){if(cc.getAttribute(l)==e){return null;
}cc=cc.parentNode;
}return cd;
},__iB:function(ce){while(ce&&ce.nodeType===1){var cf=ce.getAttribute(q);

if(cf!=null){return cf===e;
}ce=ce.parentNode;
}return true;
},_applyActive:function(cg,ch){if(ch){this.__im(ch,cg,v,true);
}
if(cg){this.__im(cg,ch,m,true);
}},_applyFocus:function(ci,cj){if(cj){this.__im(cj,ci,a,true);
}
if(ci){this.__im(ci,cj,b,true);
}if(cj){this.__im(cj,ci,g,false);
}
if(ci){this.__im(ci,cj,f,false);
}}},destruct:function(){this._stopObserver();
this._manager=this._window=this._document=this._root=this._body=this.__iC=null;
},defer:function(ck){qx.event.Registration.addHandler(ck);
var cl=ck.FOCUSABLE_ELEMENTS;

for(var cm in cl){cl[cm.toUpperCase()]=1;
}}});
})();
(function(){var k="qx.client",j="character",i="EndToEnd",h="input",g="textarea",f="StartToStart",e='character',d="qx.bom.Selection",c="button",b="#text",a="body";
qx.Class.define(d,{statics:{getSelectionObject:qx.core.Variant.select(k,{"mshtml":function(l){return l.selection;
},"default":function(m){return qx.dom.Node.getWindow(m).getSelection();
}}),get:qx.core.Variant.select(k,{"mshtml":function(n){var o=qx.bom.Range.get(qx.dom.Node.getDocument(n));
return o.text;
},"default":function(p){if(this.__iD(p)){return p.value.substring(p.selectionStart,p.selectionEnd);
}else{return this.getSelectionObject(qx.dom.Node.getDocument(p)).toString();
}}}),getLength:qx.core.Variant.select(k,{"mshtml":function(q){var s=this.get(q);
var r=qx.util.StringSplit.split(s,/\r\n/);
return s.length-(r.length-1);
},"opera":function(t){var y,w,u;

if(this.__iD(t)){var x=t.selectionStart;
var v=t.selectionEnd;
y=t.value.substring(x,v);
w=v-x;
}else{y=qx.bom.Selection.get(t);
w=y.length;
}u=qx.util.StringSplit.split(y,/\r\n/);
return w-(u.length-1);
},"default":function(z){if(this.__iD(z)){return z.selectionEnd-z.selectionStart;
}else{return this.get(z).length;
}}}),getStart:qx.core.Variant.select(k,{"mshtml":function(A){if(this.__iD(A)){var F=qx.bom.Range.get();
if(!A.contains(F.parentElement())){return -1;
}var G=qx.bom.Range.get(A);
var E=A.value.length;
G.moveToBookmark(F.getBookmark());
G.moveEnd(e,E);
return E-G.text.length;
}else{var G=qx.bom.Range.get(A);
var C=G.parentElement();
var H=qx.bom.Range.get();
H.moveToElementText(C);
var B=qx.bom.Range.get(qx.dom.Node.getBodyElement(A));
B.setEndPoint(f,G);
B.setEndPoint(i,H);
if(H.compareEndPoints(f,B)==0){return 0;
}var D;
var I=0;

while(true){D=B.moveStart(j,-1);
if(H.compareEndPoints(f,B)==0){break;
}if(D==0){break;
}else{I++;
}}return ++I;
}},"gecko|webkit":function(J){if(this.__iD(J)){return J.selectionStart;
}else{var L=qx.dom.Node.getDocument(J);
var K=this.getSelectionObject(L);
if(K.anchorOffset<K.focusOffset){return K.anchorOffset;
}else{return K.focusOffset;
}}},"default":function(M){if(this.__iD(M)){return M.selectionStart;
}else{return qx.bom.Selection.getSelectionObject(qx.dom.Node.getDocument(M)).anchorOffset;
}}}),getEnd:qx.core.Variant.select(k,{"mshtml":function(N){if(this.__iD(N)){var S=qx.bom.Range.get();
if(!N.contains(S.parentElement())){return -1;
}var T=qx.bom.Range.get(N);
var R=N.value.length;
T.moveToBookmark(S.getBookmark());
T.moveStart(e,-R);
return T.text.length;
}else{var T=qx.bom.Range.get(N);
var P=T.parentElement();
var U=qx.bom.Range.get();
U.moveToElementText(P);
var R=U.text.length;
var O=qx.bom.Range.get(qx.dom.Node.getBodyElement(N));
O.setEndPoint(i,T);
O.setEndPoint(f,U);
if(U.compareEndPoints(i,O)==0){return R-1;
}var Q;
var V=0;

while(true){Q=O.moveEnd(j,1);
if(U.compareEndPoints(i,O)==0){break;
}if(Q==0){break;
}else{V++;
}}return R-(++V);
}},"gecko|webkit":function(W){if(this.__iD(W)){return W.selectionEnd;
}else{var Y=qx.dom.Node.getDocument(W);
var X=this.getSelectionObject(Y);
if(X.focusOffset>X.anchorOffset){return X.focusOffset;
}else{return X.anchorOffset;
}}},"default":function(ba){if(this.__iD(ba)){return ba.selectionEnd;
}else{return qx.bom.Selection.getSelectionObject(qx.dom.Node.getDocument(ba)).focusOffset;
}}}),__iD:function(bb){return qx.dom.Node.isElement(bb)&&(bb.nodeName.toLowerCase()==h||bb.nodeName.toLowerCase()==g);
},set:qx.core.Variant.select(k,{"mshtml":function(bc,bd,be){var bf;
if(qx.dom.Node.isDocument(bc)){bc=bc.body;
}
if(qx.dom.Node.isElement(bc)||qx.dom.Node.isText(bc)){switch(bc.nodeName.toLowerCase()){case h:case g:case c:if(be===undefined){be=bc.value.length;
}
if(bd>=0&&bd<=bc.value.length&&be>=0&&be<=bc.value.length){bf=qx.bom.Range.get(bc);
bf.collapse(true);
bf.moveStart(j,bd);
bf.moveEnd(j,be-bd);
bf.select();
return true;
}break;
case b:if(be===undefined){be=bc.nodeValue.length;
}
if(bd>=0&&bd<=bc.nodeValue.length&&be>=0&&be<=bc.nodeValue.length){bf=qx.bom.Range.get(qx.dom.Node.getBodyElement(bc));
bf.moveToElementText(bc.parentNode);
bf.collapse(true);
bf.moveStart(j,bd);
bf.moveEnd(j,be-bd);
bf.select();
return true;
}break;
default:if(be===undefined){be=bc.childNodes.length-1;
}if(bc.childNodes[bd]&&bc.childNodes[be]){bf=qx.bom.Range.get(qx.dom.Node.getBodyElement(bc));
bf.moveToElementText(bc.childNodes[bd]);
bf.collapse(true);
var bg=qx.bom.Range.get(qx.dom.Node.getBodyElement(bc));
bg.moveToElementText(bc.childNodes[be]);
bf.setEndPoint(i,bg);
bf.select();
return true;
}}}return false;
},"default":function(bh,bi,bj){var bn=bh.nodeName.toLowerCase();

if(qx.dom.Node.isElement(bh)&&(bn==h||bn==g)){if(bj===undefined){bj=bh.value.length;
}if(bi>=0&&bi<=bh.value.length&&bj>=0&&bj<=bh.value.length){bh.focus();
bh.select();
bh.setSelectionRange(bi,bj);
return true;
}}else{var bl=false;
var bm=qx.dom.Node.getWindow(bh).getSelection();
var bk=qx.bom.Range.get(bh);
if(qx.dom.Node.isText(bh)){if(bj===undefined){bj=bh.length;
}
if(bi>=0&&bi<bh.length&&bj>=0&&bj<=bh.length){bl=true;
}}else if(qx.dom.Node.isElement(bh)){if(bj===undefined){bj=bh.childNodes.length-1;
}
if(bi>=0&&bh.childNodes[bi]&&bj>=0&&bh.childNodes[bj]){bl=true;
}}else if(qx.dom.Node.isDocument(bh)){bh=bh.body;

if(bj===undefined){bj=bh.childNodes.length-1;
}
if(bi>=0&&bh.childNodes[bi]&&bj>=0&&bh.childNodes[bj]){bl=true;
}}
if(bl){if(!bm.isCollapsed){bm.collapseToStart();
}bk.setStart(bh,bi);
if(qx.dom.Node.isText(bh)){bk.setEnd(bh,bj);
}else{bk.setEndAfter(bh.childNodes[bj]);
}if(bm.rangeCount>0){bm.removeAllRanges();
}bm.addRange(bk);
return true;
}}return false;
}}),setAll:function(bo){return qx.bom.Selection.set(bo,0);
},clear:qx.core.Variant.select(k,{"mshtml":function(bp){var bq=qx.bom.Selection.getSelectionObject(qx.dom.Node.getDocument(bp));
var br=qx.bom.Range.get(bp);
var parent=br.parentElement();
var bs=qx.bom.Range.get(qx.dom.Node.getDocument(bp));
if(parent==bs.parentElement()&&parent==bp){bq.empty();
}},"default":function(bt){var bv=qx.bom.Selection.getSelectionObject(qx.dom.Node.getDocument(bt));
var bx=bt.nodeName.toLowerCase();
if(qx.dom.Node.isElement(bt)&&(bx==h||bx==g)){bt.setSelectionRange(0,0);
qx.bom.Element.blur(bt);
}else if(qx.dom.Node.isDocument(bt)||bx==a){bv.collapse(bt.body?bt.body:bt,0);
}else{var bw=qx.bom.Range.get(bt);

if(!bw.collapsed){var by;
var bu=bw.commonAncestorContainer;
if(qx.dom.Node.isElement(bt)&&qx.dom.Node.isText(bu)){by=bu.parentNode;
}else{by=bu;
}
if(by==bt){bv.collapse(bt,0);
}}}}})}});
})();
(function(){var l="button",k="qx.bom.Range",j="text",i="password",h="file",g="submit",f="reset",e="textarea",d="input",c="hidden",a="qx.client",b="body";
qx.Class.define(k,{statics:{get:qx.core.Variant.select(a,{"mshtml":function(m){if(qx.dom.Node.isElement(m)){switch(m.nodeName.toLowerCase()){case d:switch(m.type){case j:case i:case c:case l:case f:case h:case g:return m.createTextRange();
break;
default:return qx.bom.Selection.getSelectionObject(qx.dom.Node.getDocument(m)).createRange();
}break;
case e:case b:case l:return m.createTextRange();
break;
default:return qx.bom.Selection.getSelectionObject(qx.dom.Node.getDocument(m)).createRange();
}}else{if(m==null){m=window;
}return qx.bom.Selection.getSelectionObject(qx.dom.Node.getDocument(m)).createRange();
}},"default":function(n){var o=qx.dom.Node.getDocument(n);
var p=qx.bom.Selection.getSelectionObject(o);

if(p.rangeCount>0){return p.getRangeAt(0);
}else{return o.createRange();
}}})}});
})();
(function(){var j="",h="m",g="g",f="^",e="qx.util.StringSplit",d="i",c="$(?!\\s)",b="[object RegExp]",a="y";
qx.Class.define(e,{statics:{split:function(k,l,m){if(Object.prototype.toString.call(l)!==b){return String.prototype.split.call(k,l,m);
}var t=[],n=0,r=(l.ignoreCase?d:j)+(l.multiline?h:j)+(l.sticky?a:j),l=RegExp(l.source,r+g),q,u,o,p,s=/()??/.exec(j)[1]===undefined;
k=k+j;

if(!s){q=RegExp(f+l.source+c,r);
}if(m===undefined||+m<0){m=Infinity;
}else{m=Math.floor(+m);

if(!m){return [];
}}
while(u=l.exec(k)){o=u.index+u[0].length;

if(o>n){t.push(k.slice(n,u.index));
if(!s&&u.length>1){u[0].replace(q,function(){for(var i=1;i<arguments.length-2;i++){if(arguments[i]===undefined){u[i]=undefined;
}}});
}
if(u.length>1&&u.index<k.length){Array.prototype.push.apply(t,u.slice(1));
}p=u[0].length;
n=o;

if(t.length>=m){break;
}}
if(l.lastIndex===u.index){l.lastIndex++;
}}
if(n===k.length){if(p||!l.test(j)){t.push(j);
}}else{t.push(k.slice(n));
}return t.length>m?t.slice(0,m):t;
}}});
})();
(function(){var a="qx.event.type.Focus";
qx.Class.define(a,{extend:qx.event.type.Event,members:{init:function(b,c,d){qx.event.type.Event.prototype.init.call(this,d,false);
this._target=b;
this._relatedTarget=c;
return this;
}}});
})();
(function(){var j="",i="undefined",h="qx.client",g="readOnly",f="accessKey",e="qx.bom.element.Attribute",d="rowSpan",c="vAlign",b="className",a="textContent",y="'",x="htmlFor",w="longDesc",v="cellSpacing",u="frameBorder",t="='",s="useMap",r="innerText",q="innerHTML",p="tabIndex",n="dateTime",o="maxLength",l="mshtml",m="cellPadding",k="colSpan";
qx.Class.define(e,{statics:{__iE:{names:{"class":b,"for":x,html:q,text:qx.core.Variant.isSet(h,l)?r:a,colspan:k,rowspan:d,valign:c,datetime:n,accesskey:f,tabindex:p,maxlength:o,readonly:g,longdesc:w,cellpadding:m,cellspacing:v,frameborder:u,usemap:s},runtime:{"html":1,"text":1},bools:{compact:1,nowrap:1,ismap:1,declare:1,noshade:1,checked:1,disabled:1,readOnly:1,multiple:1,selected:1,noresize:1,defer:1,allowTransparency:1},property:{$$html:1,$$widget:1,disabled:1,checked:1,readOnly:1,multiple:1,selected:1,value:1,maxLength:1,className:1,innerHTML:1,innerText:1,textContent:1,htmlFor:1,tabIndex:1},qxProperties:{$$widget:1,$$html:1},propertyDefault:{disabled:false,checked:false,readOnly:false,multiple:false,selected:false,value:j,className:j,innerHTML:j,innerText:j,textContent:j,htmlFor:j,tabIndex:0,maxLength:qx.core.Variant.select(h,{"mshtml":2147483647,"webkit":524288,"default":-1})},removeableProperties:{disabled:1,multiple:1,maxLength:1},original:{href:1,src:1,type:1}},compile:function(z){var A=[];
var C=this.__iE.runtime;

for(var B in z){if(!C[B]){A.push(B,t,z[B],y);
}}return A.join(j);
},get:qx.core.Variant.select(h,{"mshtml":function(D,name){var F=this.__iE;
var E;
name=F.names[name]||name;
if(F.original[name]){E=D.getAttribute(name,2);
}else if(F.property[name]){E=D[name];

if(typeof F.propertyDefault[name]!==i&&E==F.propertyDefault[name]){if(typeof F.bools[name]===i){return null;
}else{return E;
}}}else{E=D.getAttribute(name);
}if(F.bools[name]){return !!E;
}return E;
},"default":function(G,name){var I=this.__iE;
var H;
name=I.names[name]||name;
if(I.property[name]){H=G[name];

if(typeof I.propertyDefault[name]!==i&&H==I.propertyDefault[name]){if(typeof I.bools[name]===i){return null;
}else{return H;
}}}else{H=G.getAttribute(name);
}if(I.bools[name]){return !!H;
}return H;
}}),set:function(J,name,K){if(typeof K===i){return;
}var L=this.__iE;
name=L.names[name]||name;
if(L.bools[name]){K=!!K;
}if(L.property[name]&&(!(J[name]===undefined)||L.qxProperties[name])){if(K==null){if(L.removeableProperties[name]){J.removeAttribute(name);
return;
}else if(typeof L.propertyDefault[name]!==i){K=L.propertyDefault[name];
}}J[name]=K;
}else{if(K===true){J.setAttribute(name,name);
}else if(K===false||K===null){J.removeAttribute(name);
}else{J.setAttribute(name,K);
}}},reset:function(M,name){this.set(M,name,null);
}}});
})();
(function(){var a="qx.event.type.Drag";
qx.Class.define(a,{extend:qx.event.type.Event,members:{init:function(b,c){qx.event.type.Event.prototype.init.call(this,true,b);

if(c){this._native=c.getNativeEvent()||null;
this._originalTarget=c.getTarget()||null;
}else{this._native=null;
this._originalTarget=null;
}return this;
},clone:function(d){var e=qx.event.type.Event.prototype.clone.call(this,d);
e._native=this._native;
return e;
},getDocumentLeft:function(){if(this._native==null){return 0;
}
if(this._native.pageX!==undefined){return this._native.pageX;
}else{var f=qx.dom.Node.getWindow(this._native.srcElement);
return this._native.clientX+qx.bom.Viewport.getScrollLeft(f);
}},getDocumentTop:function(){if(this._native==null){return 0;
}
if(this._native.pageY!==undefined){return this._native.pageY;
}else{var g=qx.dom.Node.getWindow(this._native.srcElement);
return this._native.clientY+qx.bom.Viewport.getScrollTop(g);
}},getManager:function(){return qx.event.Registration.getManager(this.getTarget()).getHandler(qx.event.handler.DragDrop);
},addType:function(h){this.getManager().addType(h);
},addAction:function(i){this.getManager().addAction(i);
},supportsType:function(j){return this.getManager().supportsType(j);
},supportsAction:function(k){return this.getManager().supportsAction(k);
},addData:function(l,m){this.getManager().addData(l,m);
},getData:function(n){return this.getManager().getData(n);
},getCurrentType:function(){return this.getManager().getCurrentType();
},getCurrentAction:function(){return this.getManager().getCurrentAction();
}}});
})();
(function(){var h="losecapture",g="qx.client",f="blur",e="focus",d="click",c="qx.event.dispatch.MouseCapture",b="capture",a="scroll";
qx.Class.define(c,{extend:qx.event.dispatch.AbstractBubbling,construct:function(i,j){qx.event.dispatch.AbstractBubbling.call(this,i);
this.__iF=i.getWindow();
this.__iG=j;
i.addListener(this.__iF,f,this.releaseCapture,this);
i.addListener(this.__iF,e,this.releaseCapture,this);
i.addListener(this.__iF,a,this.releaseCapture,this);
},statics:{PRIORITY:qx.event.Registration.PRIORITY_FIRST},members:{__iG:null,__iH:null,__iI:true,__iF:null,_getParent:function(k){return k.parentNode;
},canDispatchEvent:function(l,event,m){return (this.__iH&&this.__iJ[m]);
},dispatchEvent:function(n,event,o){if(o==d){event.stopPropagation();
this.releaseCapture();
return;
}
if(this.__iI||!qx.dom.Hierarchy.contains(this.__iH,n)){n=this.__iH;
}qx.event.dispatch.AbstractBubbling.prototype.dispatchEvent.call(this,n,event,o);
},__iJ:{"mouseup":1,"mousedown":1,"click":1,"dblclick":1,"mousemove":1,"mouseout":1,"mouseover":1},activateCapture:function(p,q){var q=q!==false;

if(this.__iH===p&&this.__iI==q){return;
}
if(this.__iH){this.releaseCapture();
}this.nativeSetCapture(p,q);

if(this.hasNativeCapture){var self=this;
qx.bom.Event.addNativeListener(p,h,function(){qx.bom.Event.removeNativeListener(p,h,arguments.callee);
self.releaseCapture();
});
}this.__iI=q;
this.__iH=p;
this.__iG.fireEvent(p,b,qx.event.type.Event,[true,false]);
},getCaptureElement:function(){return this.__iH;
},releaseCapture:function(){var r=this.__iH;

if(!r){return;
}this.__iH=null;
this.__iG.fireEvent(r,h,qx.event.type.Event,[true,false]);
this.nativeReleaseCapture(r);
},hasNativeCapture:qx.bom.client.Engine.MSHTML,nativeSetCapture:qx.core.Variant.select(g,{"mshtml":function(s,t){s.setCapture(t!==false);
},"default":qx.lang.Function.empty}),nativeReleaseCapture:qx.core.Variant.select(g,{"mshtml":function(u){u.releaseCapture();
},"default":qx.lang.Function.empty})},destruct:function(){this.__iH=this.__iF=this.__iG=null;
},defer:function(v){qx.event.Registration.addDispatcher(v);
}});
})();
(function(){var c="qx.bom.Selector";
qx.Class.define(c,{statics:{query:null,matches:null}});
(function(){var o=/((?:\((?:\([^()]+\)|[^()]+)+\)|\[(?:\[[^\[\]]*\]|['"][^'"]*['"]|[^\[\]'"]+)+\]|\\.|[^ >+~,(\[\\]+)+|[>+~])(\s*,\s*)?((?:.|\r|\n)*)/g,v=0,r=Object.prototype.toString,p=false,x=true;
[0,0].sort(function(){x=false;
return 0;
});
var g=function(z,A,B,C){B=B||[];
A=A||document;
var L=A;

if(A.nodeType!==1&&A.nodeType!==9){return [];
}
if(!z||typeof z!=="string"){return B;
}var m,F,D,H,J,G,M,i,N=true,E=g.isXML(A),I=[],K=z;
do{o.exec("");
m=o.exec(K);

if(m){K=m[3];
I.push(m[1]);

if(m[2]){H=m[3];
break;
}}}while(m);

if(I.length>1&&q.exec(z)){if(I.length===2&&k.relative[I[0]]){F=h(I[0]+I[1],A);
}else{F=k.relative[I[0]]?[A]:g(I.shift(),A);

while(I.length){z=I.shift();

if(k.relative[z]){z+=I.shift();
}F=h(z,F);
}}}else{if(!C&&I.length>1&&A.nodeType===9&&!E&&k.match.ID.test(I[0])&&!k.match.ID.test(I[I.length-1])){J=g.find(I.shift(),A,E);
A=J.expr?g.filter(J.expr,J.set)[0]:J.set[0];
}
if(A){J=C?
{expr:I.pop(),set:f(C)}:g.find(I.pop(),I.length===1&&(I[0]==="~"||I[0]==="+")&&A.parentNode?A.parentNode:A,E);
F=J.expr?g.filter(J.expr,J.set):J.set;

if(I.length>0){D=f(F);
}else{N=false;
}
while(I.length){G=I.pop();
M=G;

if(!k.relative[G]){G="";
}else{M=I.pop();
}
if(M==null){M=A;
}k.relative[G](D,M,E);
}}else{D=I=[];
}}
if(!D){D=F;
}
if(!D){g.error(G||z);
}
if(r.call(D)==="[object Array]"){if(!N){B.push.apply(B,D);
}else if(A&&A.nodeType===1){for(i=0;D[i]!=null;i++){if(D[i]&&(D[i]===true||D[i].nodeType===1&&g.contains(A,D[i]))){B.push(F[i]);
}}}else{for(i=0;D[i]!=null;i++){if(D[i]&&D[i].nodeType===1){B.push(F[i]);
}}}}else{f(D,B);
}
if(H){g(H,L,B,C);
g.uniqueSort(B);
}return B;
};
g.uniqueSort=function(O){if(s){p=x;
O.sort(s);

if(p){for(var i=1;i<O.length;i++){if(O[i]===O[i-1]){O.splice(i--,1);
}}}}return O;
};
g.matches=function(P,Q){return g(P,null,null,Q);
};
g.matchesSelector=function(R,S){return g(S,null,null,[R]).length>0;
};
g.find=function(T,U,V){var W;

if(!T){return [];
}
for(var i=0,l=k.order.length;i<l;i++){var Y,X=k.order[i];

if((Y=k.leftMatch[X].exec(T))){var ba=Y[1];
Y.splice(1,1);

if(ba.substr(ba.length-1)!=="\\"){Y[1]=(Y[1]||"").replace(/\\/g,"");
W=k.find[X](Y,U,V);

if(W!=null){T=T.replace(k.match[X],"");
break;
}}}}
if(!W){W=U.getElementsByTagName("*");
}return {set:W,expr:T};
};
g.filter=function(bb,bc,bd,be){var br,bq,bf=bb,bk=[],bg=bc,bh=bc&&bc[0]&&g.isXML(bc[0]);

while(bb&&bc.length){for(var bo in k.filter){if((br=k.leftMatch[bo].exec(bb))!=null&&br[2]){var bn,bj,bi=k.filter[bo],bs=br[1];
bq=false;
br.splice(1,1);

if(bs.substr(bs.length-1)==="\\"){continue;
}
if(bg===bk){bk=[];
}
if(k.preFilter[bo]){br=k.preFilter[bo](br,bg,bd,bk,be,bh);

if(!br){bq=bn=true;
}else if(br===true){continue;
}}
if(br){for(var i=0;(bj=bg[i])!=null;i++){if(bj){bn=bi(bj,br,i,bg);
var bm=be^!!bn;

if(bd&&bn!=null){if(bm){bq=true;
}else{bg[i]=false;
}}else if(bm){bk.push(bj);
bq=true;
}}}}
if(bn!==undefined){if(!bd){bg=bk;
}bb=bb.replace(k.match[bo],"");

if(!bq){return [];
}break;
}}}if(bb===bf){if(bq==null){g.error(bb);
}else{break;
}}bf=bb;
}return bg;
};
g.error=function(bt){throw "Syntax error, unrecognized expression: "+bt;
};
var k=g.selectors={order:["ID","NAME","TAG"],match:{ID:/#((?:[\w\u00c0-\uFFFF\-]|\\.)+)/,CLASS:/\.((?:[\w\u00c0-\uFFFF\-]|\\.)+)/,NAME:/\[name=['"]*((?:[\w\u00c0-\uFFFF\-]|\\.)+)['"]*\]/,ATTR:/\[\s*((?:[\w\u00c0-\uFFFF\-]|\\.)+)\s*(?:(\S?=)\s*(['"]*)(.*?)\3|)\s*\]/,TAG:/^((?:[\w\u00c0-\uFFFF\*\-]|\\.)+)/,CHILD:/:(only|nth|last|first)-child(?:\((even|odd|[\dn+\-]*)\))?/,POS:/:(nth|eq|gt|lt|first|last|even|odd)(?:\((\d*)\))?(?=[^\-]|$)/,PSEUDO:/:((?:[\w\u00c0-\uFFFF\-]|\\.)+)(?:\((['"]?)((?:\([^\)]+\)|[^\(\)]*)+)\2\))?/},leftMatch:{},attrMap:{"class":"className","for":"htmlFor"},attrHandle:{href:function(bu){return bu.getAttribute("href");
}},relative:{"+":function(bv,bw){var bx=typeof bw==="string",bz=bx&&!/\W/.test(bw),bA=bx&&!bz;

if(bz){bw=bw.toLowerCase();
}
for(var i=0,l=bv.length,by;i<l;i++){if((by=bv[i])){while((by=by.previousSibling)&&by.nodeType!==1){}bv[i]=bA||by&&by.nodeName.toLowerCase()===bw?by||false:by===bw;
}}
if(bA){g.filter(bw,bv,true);
}},">":function(bB,bC){var bE,bD=typeof bC==="string",i=0,l=bB.length;

if(bD&&!/\W/.test(bC)){bC=bC.toLowerCase();

for(;i<l;i++){bE=bB[i];

if(bE){var parent=bE.parentNode;
bB[i]=parent.nodeName.toLowerCase()===bC?parent:false;
}}}else{for(;i<l;i++){bE=bB[i];

if(bE){bB[i]=bD?bE.parentNode:bE.parentNode===bC;
}}
if(bD){g.filter(bC,bB,true);
}}},"":function(bF,bG,bH){var bK,bI=v++,bJ=w;

if(typeof bG==="string"&&!/\W/.test(bG)){bG=bG.toLowerCase();
bK=bG;
bJ=y;
}bJ("parentNode",bG,bI,bF,bK,bH);
},"~":function(bL,bM,bN){var bQ,bO=v++,bP=w;

if(typeof bM==="string"&&!/\W/.test(bM)){bM=bM.toLowerCase();
bQ=bM;
bP=y;
}bP("previousSibling",bM,bO,bL,bQ,bN);
}},find:{ID:function(bR,bS,bT){if(typeof bS.getElementById!=="undefined"&&!bT){var m=bS.getElementById(bR[1]);
return m&&m.parentNode?[m]:[];
}},NAME:function(bU,bV){if(typeof bV.getElementsByName!=="undefined"){var bX=[],bW=bV.getElementsByName(bU[1]);

for(var i=0,l=bW.length;i<l;i++){if(bW[i].getAttribute("name")===bU[1]){bX.push(bW[i]);
}}return bX.length===0?null:bX;
}},TAG:function(bY,ca){return ca.getElementsByTagName(bY[1]);
}},preFilter:{CLASS:function(cb,cc,cd,ce,cf,cg){cb=" "+cb[1].replace(/\\/g,"")+" ";

if(cg){return cb;
}
for(var i=0,ch;(ch=cc[i])!=null;i++){if(ch){if(cf^(ch.className&&(" "+ch.className+" ").replace(/[\t\n]/g," ").indexOf(cb)>=0)){if(!cd){ce.push(ch);
}}else if(cd){cc[i]=false;
}}}return false;
},ID:function(ci){return ci[1].replace(/\\/g,"");
},TAG:function(cj,ck){return cj[1].toLowerCase();
},CHILD:function(cl){if(cl[1]==="nth"){var cm=/(-?)(\d*)n((?:\+|-)?\d*)/.exec(cl[2]==="even"&&"2n"||cl[2]==="odd"&&"2n+1"||!/\D/.test(cl[2])&&"0n+"+cl[2]||cl[2]);
cl[2]=(cm[1]+(cm[2]||1))-0;
cl[3]=cm[3]-0;
}cl[0]=v++;
return cl;
},ATTR:function(cn,co,cp,cq,cr,cs){var name=cn[1].replace(/\\/g,"");

if(!cs&&k.attrMap[name]){cn[1]=k.attrMap[name];
}
if(cn[2]==="~="){cn[4]=" "+cn[4]+" ";
}return cn;
},PSEUDO:function(ct,cu,cv,cw,cx){if(ct[1]==="not"){if((o.exec(ct[3])||"").length>1||/^\w/.test(ct[3])){ct[3]=g(ct[3],null,null,cu);
}else{var cy=g.filter(ct[3],cu,cv,true^cx);

if(!cv){cw.push.apply(cw,cy);
}return false;
}}else if(k.match.POS.test(ct[0])||k.match.CHILD.test(ct[0])){return true;
}return ct;
},POS:function(cz){cz.unshift(true);
return cz;
}},filters:{enabled:function(cA){return cA.disabled===false&&cA.type!=="hidden";
},disabled:function(cB){return cB.disabled===true;
},checked:function(cC){return cC.checked===true;
},selected:function(cD){cD.parentNode.selectedIndex;
return cD.selected===true;
},parent:function(cE){return !!cE.firstChild;
},empty:function(cF){return !cF.firstChild;
},has:function(cG,i,cH){return !!g(cH[3],cG).length;
},header:function(cI){return (/h\d/i).test(cI.nodeName);
},text:function(cJ){return "text"===cJ.type;
},radio:function(cK){return "radio"===cK.type;
},checkbox:function(cL){return "checkbox"===cL.type;
},file:function(cM){return "file"===cM.type;
},password:function(cN){return "password"===cN.type;
},submit:function(cO){return "submit"===cO.type;
},image:function(cP){return "image"===cP.type;
},reset:function(cQ){return "reset"===cQ.type;
},button:function(cR){return "button"===cR.type||cR.nodeName.toLowerCase()==="button";
},input:function(cS){return (/input|select|textarea|button/i).test(cS.nodeName);
}},setFilters:{first:function(cT,i){return i===0;
},last:function(cU,i,cV,cW){return i===cW.length-1;
},even:function(cX,i){return i%2===0;
},odd:function(cY,i){return i%2===1;
},lt:function(da,i,db){return i<db[3]-0;
},gt:function(dc,i,dd){return i>dd[3]-0;
},nth:function(de,i,df){return df[3]-0===i;
},eq:function(dg,i,dh){return dh[3]-0===i;
}},filter:{PSEUDO:function(di,dj,i,dk){var name=dj[1],dl=k.filters[name];

if(dl){return dl(di,i,dj,dk);
}else if(name==="contains"){return (di.textContent||di.innerText||g.getText([di])||"").indexOf(dj[3])>=0;
}else if(name==="not"){var dm=dj[3];

for(var j=0,l=dm.length;j<l;j++){if(dm[j]===di){return false;
}}return true;
}else{g.error("Syntax error, unrecognized expression: "+name);
}},CHILD:function(dn,dp){var dv=dp[1],dq=dn;

switch(dv){case "only":case "first":while((dq=dq.previousSibling)){if(dq.nodeType===1){return false;
}}
if(dv==="first"){return true;
}dq=dn;
case "last":while((dq=dq.nextSibling)){if(dq.nodeType===1){return false;
}}return true;
case "nth":var dw=dp[2],ds=dp[3];

if(dw===1&&ds===0){return true;
}var du=dp[0],parent=dn.parentNode;

if(parent&&(parent.sizcache!==du||!dn.nodeIndex)){var dr=0;

for(dq=parent.firstChild;dq;dq=dq.nextSibling){if(dq.nodeType===1){dq.nodeIndex=++dr;
}}parent.sizcache=du;
}var dt=dn.nodeIndex-ds;

if(dw===0){return dt===0;
}else{return (dt%dw===0&&dt/dw>=0);
}}},ID:function(dx,dy){return dx.nodeType===1&&dx.getAttribute("id")===dy;
},TAG:function(dz,dA){return (dA==="*"&&dz.nodeType===1)||dz.nodeName.toLowerCase()===dA;
},CLASS:function(dB,dC){return (" "+(dB.className||dB.getAttribute("class"))+" ").indexOf(dC)>-1;
},ATTR:function(dD,dE){var name=dE[1],dI=k.attrHandle[name]?k.attrHandle[name](dD):dD[name]!=null?dD[name]:dD.getAttribute(name),dH=dI+"",dG=dE[2],dF=dE[4];
return dI==null?dG==="!=":dG==="="?dH===dF:dG==="*="?dH.indexOf(dF)>=0:dG==="~="?(" "+dH+" ").indexOf(dF)>=0:!dF?dH&&dI!==false:dG==="!="?dH!==dF:dG==="^="?dH.indexOf(dF)===0:dG==="$="?dH.substr(dH.length-dF.length)===dF:dG==="|="?dH===dF||dH.substr(0,dF.length+1)===dF+"-":false;
},POS:function(dJ,dK,i,dL){var name=dK[2],dM=k.setFilters[name];

if(dM){return dM(dJ,i,dK,dL);
}}}};
var q=k.match.POS,d=function(dN,dO){return "\\"+(dO-0+1);
};

for(var u in k.match){k.match[u]=new RegExp(k.match[u].source+(/(?![^\[]*\])(?![^\(]*\))/.source));
k.leftMatch[u]=new RegExp(/(^(?:.|\r|\n)*?)/.source+k.match[u].source.replace(/\\(\d+)/g,d));
}var f=function(dP,dQ){dP=Array.prototype.slice.call(dP,0);

if(dQ){dQ.push.apply(dQ,dP);
return dQ;
}return dP;
};
try{Array.prototype.slice.call(document.documentElement.childNodes,0)[0].nodeType;
}catch(e){f=function(dR,dS){var i=0,dT=dS||[];

if(r.call(dR)==="[object Array]"){Array.prototype.push.apply(dT,dR);
}else{if(typeof dR.length==="number"){for(var l=dR.length;i<l;i++){dT.push(dR[i]);
}}else{for(;dR[i];i++){dT.push(dR[i]);
}}}return dT;
};
}var s,n;

if(document.documentElement.compareDocumentPosition){s=function(a,b){if(a===b){p=true;
return 0;
}
if(!a.compareDocumentPosition||!b.compareDocumentPosition){return a.compareDocumentPosition?-1:1;
}return a.compareDocumentPosition(b)&4?-1:1;
};
}else{s=function(a,b){var dY,dW,ea=[],eb=[],dV=a.parentNode,dX=b.parentNode,dU=dV;
if(a===b){p=true;
return 0;
}else if(dV===dX){return n(a,b);
}else if(!dV){return -1;
}else if(!dX){return 1;
}while(dU){ea.unshift(dU);
dU=dU.parentNode;
}dU=dX;

while(dU){eb.unshift(dU);
dU=dU.parentNode;
}dY=ea.length;
dW=eb.length;
for(var i=0;i<dY&&i<dW;i++){if(ea[i]!==eb[i]){return n(ea[i],eb[i]);
}}return i===dY?n(a,eb[i],-1):n(ea[i],b,1);
};
n=function(a,b,ec){if(a===b){return ec;
}var ed=a.nextSibling;

while(ed){if(ed===b){return -1;
}ed=ed.nextSibling;
}return 1;
};
}g.getText=function(ee){var eg="",ef;

for(var i=0;ee[i];i++){ef=ee[i];
if(ef.nodeType===3||ef.nodeType===4){eg+=ef.nodeValue;
}else if(ef.nodeType!==8){eg+=g.getText(ef.childNodes);
}}return eg;
};
(function(){var ej=document.createElement("div"),ei="script"+(new Date()).getTime(),eh=document.documentElement;
ej.innerHTML="<a name='"+ei+"'/>";
eh.insertBefore(ej,eh.firstChild);
if(document.getElementById(ei)){k.find.ID=function(ek,el,em){if(typeof el.getElementById!=="undefined"&&!em){var m=el.getElementById(ek[1]);
return m?m.id===ek[1]||typeof m.getAttributeNode!=="undefined"&&m.getAttributeNode("id").nodeValue===ek[1]?[m]:undefined:[];
}};
k.filter.ID=function(en,eo){var ep=typeof en.getAttributeNode!=="undefined"&&en.getAttributeNode("id");
return en.nodeType===1&&ep&&ep.nodeValue===eo;
};
}eh.removeChild(ej);
eh=ej=null;
})();
(function(){var eq=document.createElement("div");
eq.appendChild(document.createComment(""));
if(eq.getElementsByTagName("*").length>0){k.find.TAG=function(er,es){var eu=es.getElementsByTagName(er[1]);
if(er[1]==="*"){var et=[];

for(var i=0;eu[i];i++){if(eu[i].nodeType===1){et.push(eu[i]);
}}eu=et;
}return eu;
};
}eq.innerHTML="<a href='#'></a>";

if(eq.firstChild&&typeof eq.firstChild.getAttribute!=="undefined"&&eq.firstChild.getAttribute("href")!=="#"){k.attrHandle.href=function(ev){return ev.getAttribute("href",2);
};
}eq=null;
})();

if(document.querySelectorAll){(function(){var ex=g,ew=document.createElement("div"),ey="__sizzle__";
ew.innerHTML="<p class='TEST'></p>";
if(ew.querySelectorAll&&ew.querySelectorAll(".TEST").length===0){return;
}g=function(eA,eB,eC,eD){eB=eB||document;
eA=eA.replace(/\=\s*([^'"\]]*)\s*\]/g,"='$1']");
if(!eD&&!g.isXML(eB)){if(eB.nodeType===9){try{return f(eB.querySelectorAll(eA),eC);
}catch(eG){}}else if(eB.nodeType===1&&eB.nodeName.toLowerCase()!=="object"){var eE=eB.getAttribute("id"),eF=eE||ey;

if(!eE){eB.setAttribute("id",eF);
}
try{return f(eB.querySelectorAll("#"+eF+" "+eA),eC);
}catch(eH){}finally{if(!eE){eB.removeAttribute("id");
}}}}return ex(eA,eB,eC,eD);
};

for(var ez in ex){g[ez]=ex[ez];
}ew=null;
})();
}(function(){var eK=document.documentElement,eI=eK.matchesSelector||eK.mozMatchesSelector||eK.webkitMatchesSelector||eK.msMatchesSelector,eJ=false;

try{eI.call(document.documentElement,"[test!='']:sizzle");
}catch(eL){eJ=true;
}
if(eI){g.matchesSelector=function(eM,eN){eN=eN.replace(/\=\s*([^'"\]]*)\s*\]/g,"='$1']");

if(!g.isXML(eM)){try{if(eJ||!k.match.PSEUDO.test(eN)&&!/!=/.test(eN)){return eI.call(eM,eN);
}}catch(e){}}return g(eN,null,null,[eM]).length>0;
};
}})();
(function(){var eO=document.createElement("div");
eO.innerHTML="<div class='test e'></div><div class='test'></div>";
if(!eO.getElementsByClassName||eO.getElementsByClassName("e").length===0){return;
}eO.lastChild.className="e";

if(eO.getElementsByClassName("e").length===1){return;
}k.order.splice(1,0,"CLASS");
k.find.CLASS=function(eP,eQ,eR){if(typeof eQ.getElementsByClassName!=="undefined"&&!eR){return eQ.getElementsByClassName(eP[1]);
}};
eO=null;
})();
function y(eS,eT,eU,eV,eW,eX){for(var i=0,l=eV.length;i<l;i++){var fa=eV[i];

if(fa){var eY=false;
fa=fa[eS];

while(fa){if(fa.sizcache===eU){eY=eV[fa.sizset];
break;
}
if(fa.nodeType===1&&!eX){fa.sizcache=eU;
fa.sizset=i;
}
if(fa.nodeName.toLowerCase()===eT){eY=fa;
break;
}fa=fa[eS];
}eV[i]=eY;
}}}function w(fb,fc,fd,fe,ff,fg){for(var i=0,l=fe.length;i<l;i++){var fi=fe[i];

if(fi){var fh=false;
fi=fi[fb];

while(fi){if(fi.sizcache===fd){fh=fe[fi.sizset];
break;
}
if(fi.nodeType===1){if(!fg){fi.sizcache=fd;
fi.sizset=i;
}
if(typeof fc!=="string"){if(fi===fc){fh=true;
break;
}}else if(g.filter(fc,[fi]).length>0){fh=fi;
break;
}}fi=fi[fb];
}fe[i]=fh;
}}}
if(document.documentElement.contains){g.contains=function(a,b){return a!==b&&(a.contains?a.contains(b):true);
};
}else if(document.documentElement.compareDocumentPosition){g.contains=function(a,b){return !!(a.compareDocumentPosition(b)&16);
};
}else{g.contains=function(){return false;
};
}g.isXML=function(fj){var fk=(fj?fj.ownerDocument||fj:0).documentElement;
return fk?fk.nodeName!=="HTML":false;
};
var h=function(fl,fm){var fq,fo=[],fn="",fp=fm.nodeType?[fm]:fm;
while((fq=k.match.PSEUDO.exec(fl))){fn+=fq[0];
fl=fl.replace(k.match.PSEUDO,"");
}fl=k.relative[fl]?fl+"*":fl;

for(var i=0,l=fp.length;i<l;i++){g(fl,fp[i],fo);
}return g.filter(fn,fo);
};
var t=qx.bom.Selector;
t.query=function(fr,fs){return g(fr,fs);
};
t.matches=function(ft,fu){return g(ft,null,null,fu);
};
})();
})();
(function(){var r="qx.client",q="MSXML2.DOMDocument.3.0",p="",o="mshtml",n='<\?xml version="1.0" encoding="utf-8"?>\n<',m="qx.xml.Document",k=" />",j="SelectionLanguage",h="'",g="MSXML2.XMLHTTP.3.0",c="MSXML2.XMLHTTP.6.0",f=" xmlns='",e="text/xml",b="XPath",a="MSXML2.DOMDocument.6.0",d="HTML";
qx.Class.define(m,{statics:{DOMDOC:null,XMLHTTP:null,isXmlDocument:function(s){if(s.nodeType===9){return s.documentElement.nodeName!==d;
}else if(s.ownerDocument){return this.isXmlDocument(s.ownerDocument);
}else{return false;
}},create:qx.core.Variant.select(r,{"mshtml":function(t,u){var v=new ActiveXObject(this.DOMDOC);
if(this.DOMDOC==q){v.setProperty(j,b);
}
if(u){var w=n;
w+=u;

if(t){w+=f+t+h;
}w+=k;
v.loadXML(w);
}return v;
},"default":function(x,y){return document.implementation.createDocument(x||p,y||p,null);
}}),fromString:qx.core.Variant.select(r,{"mshtml":function(z){var A=qx.xml.Document.create();
A.loadXML(z);
return A;
},"default":function(B){var C=new DOMParser();
return C.parseFromString(B,e);
}})},defer:function(D){if(qx.core.Variant.isSet(r,o)){var E=[a,q];
var F=[c,g];

for(var i=0,l=E.length;i<l;i++){try{new ActiveXObject(E[i]);
new ActiveXObject(F[i]);
}catch(G){continue;
}D.DOMDOC=E[i];
D.XMLHTTP=F[i];
break;
}}}});
})();
(function(){var k="visible",j="scroll",i="borderBottomWidth",h="borderTopWidth",g="left",f="borderLeftWidth",e="bottom",d="top",c="right",b="qx.bom.element.Scroll",a="borderRightWidth";
qx.Class.define(b,{statics:{intoViewX:function(l,stop,m){var parent=l.parentNode;
var r=qx.dom.Node.getDocument(l);
var n=r.body;
var z,x,u;
var B,s,C;
var v,D,G;
var E,p,y,o;
var t,F,w;
var q=m===g;
var A=m===c;
stop=stop?stop.parentNode:r;
while(parent&&parent!=stop){if(parent.scrollWidth>parent.clientWidth&&(parent===n||qx.bom.element.Overflow.getY(parent)!=k)){if(parent===n){x=parent.scrollLeft;
u=x+qx.bom.Viewport.getWidth();
B=qx.bom.Viewport.getWidth();
s=parent.clientWidth;
C=parent.scrollWidth;
v=0;
D=0;
G=0;
}else{z=qx.bom.element.Location.get(parent);
x=z.left;
u=z.right;
B=parent.offsetWidth;
s=parent.clientWidth;
C=parent.scrollWidth;
v=parseInt(qx.bom.element.Style.get(parent,f),10)||0;
D=parseInt(qx.bom.element.Style.get(parent,a),10)||0;
G=B-s-v-D;
}E=qx.bom.element.Location.get(l);
p=E.left;
y=E.right;
o=l.offsetWidth;
t=p-x-v;
F=y-u+D;
w=0;
if(q){w=t;
}else if(A){w=F+G;
}else if(t<0||o>s){w=t;
}else if(F>0){w=F+G;
}parent.scrollLeft+=w;
qx.event.Registration.fireNonBubblingEvent(parent,j);
}
if(parent===n){break;
}parent=parent.parentNode;
}},intoViewY:function(H,stop,I){var parent=H.parentNode;
var O=qx.dom.Node.getDocument(H);
var J=O.body;
var W,K,S;
var Y,V,Q;
var M,N,L;
var bb,bc,X,R;
var U,P,bd;
var ba=I===d;
var T=I===e;
stop=stop?stop.parentNode:O;
while(parent&&parent!=stop){if(parent.scrollHeight>parent.clientHeight&&(parent===J||qx.bom.element.Overflow.getY(parent)!=k)){if(parent===J){K=parent.scrollTop;
S=K+qx.bom.Viewport.getHeight();
Y=qx.bom.Viewport.getHeight();
V=parent.clientHeight;
Q=parent.scrollHeight;
M=0;
N=0;
L=0;
}else{W=qx.bom.element.Location.get(parent);
K=W.top;
S=W.bottom;
Y=parent.offsetHeight;
V=parent.clientHeight;
Q=parent.scrollHeight;
M=parseInt(qx.bom.element.Style.get(parent,h),10)||0;
N=parseInt(qx.bom.element.Style.get(parent,i),10)||0;
L=Y-V-M-N;
}bb=qx.bom.element.Location.get(H);
bc=bb.top;
X=bb.bottom;
R=H.offsetHeight;
U=bc-K-M;
P=X-S+N;
bd=0;
if(ba){bd=U;
}else if(T){bd=P+L;
}else if(U<0||R>V){bd=U;
}else if(P>0){bd=P+L;
}parent.scrollTop+=bd;
qx.event.Registration.fireNonBubblingEvent(parent,j);
}
if(parent===J){break;
}parent=parent.parentNode;
}},intoView:function(be,stop,bf,bg){this.intoViewX(be,stop,bf);
this.intoViewY(be,stop,bg);
}}});
})();
(function(){var b="qx.ui.core.queue.Widget",a="widget";
qx.Class.define(b,{statics:{__iK:{},remove:function(c){delete this.__iK[c.$$hash];
},add:function(d){var e=this.__iK;

if(e[d.$$hash]){return;
}e[d.$$hash]=d;
qx.ui.core.queue.Manager.scheduleFlush(a);
},flush:function(){var f=this.__iK;
var h;

for(var g in f){h=f[g];
delete f[g];
h.syncWidget();
}for(var g in f){return;
}this.__iK={};
}}});
})();
(function(){var b="qx.ui.core.queue.Visibility",a="visibility";
qx.Class.define(b,{statics:{__iL:{},__iM:{},remove:function(c){var d=c.$$hash;
delete this.__iM[d];
delete this.__iL[d];
},isVisible:function(e){return this.__iM[e.$$hash]||false;
},__iN:function(f){var h=this.__iM;
var g=f.$$hash;
var i;
if(f.isExcluded()){i=false;
}else{var parent=f.$$parent;

if(parent){i=this.__iN(parent);
}else{i=f.isRootWidget();
}}return h[g]=i;
},add:function(j){var k=this.__iL;

if(k[j.$$hash]){return;
}k[j.$$hash]=j;
qx.ui.core.queue.Manager.scheduleFlush(a);
},flush:function(){var l=this.__iL;
var p=this.__iM;
for(var m in l){if(p[m]!=null){l[m].addChildrenToQueue(l);
}}var o={};

for(var m in l){o[m]=p[m];
p[m]=null;
}for(var m in l){var n=l[m];
delete l[m];
if(p[m]==null){this.__iN(n);
}if(p[m]&&p[m]!=o[m]){n.checkAppearanceNeeds();
}}this.__iL={};
}}});
})();
(function(){var b="appearance",a="qx.ui.core.queue.Appearance";
qx.Class.define(a,{statics:{__iO:{},remove:function(c){delete this.__iO[c.$$hash];
},add:function(d){var e=this.__iO;

if(e[d.$$hash]){return;
}e[d.$$hash]=d;
qx.ui.core.queue.Manager.scheduleFlush(b);
},has:function(f){return !!this.__iO[f.$$hash];
},flush:function(){var j=qx.ui.core.queue.Visibility;
var g=this.__iO;
var i;

for(var h in g){i=g[h];
delete g[h];
if(j.isVisible(i)){i.syncAppearance();
}else{i.$$stateChanges=true;
}}}}});
})();
(function(){var b="dispose",a="qx.ui.core.queue.Dispose";
qx.Class.define(a,{statics:{__iP:{},add:function(c){var d=this.__iP;

if(d[c.$$hash]){return;
}d[c.$$hash]=c;
qx.ui.core.queue.Manager.scheduleFlush(b);
},flush:function(){var e=this.__iP;

for(var g in e){var f=e[g];
delete e[g];
f.dispose();
}for(var g in e){return;
}this.__iP={};
}}});
})();
(function(){var c="none",b="qx.html.Decorator",a="absolute";
qx.Class.define(b,{extend:qx.html.Element,construct:function(d,e){var f={position:a,top:0,left:0};

if(qx.bom.client.Feature.CSS_POINTER_EVENTS){f.pointerEvents=c;
}qx.html.Element.call(this,null,f);
this.__iQ=d;
this.__iR=e||d.toHashCode();
this.useMarkup(d.getMarkup());
},members:{__iR:null,__iQ:null,getId:function(){return this.__iR;
},getDecorator:function(){return this.__iQ;
},resize:function(g,h){this.__iQ.resize(this.getDomElement(),g,h);
},tint:function(i){this.__iQ.tint(this.getDomElement(),i);
},getInsets:function(){return this.__iQ.getInsets();
}},destruct:function(){this.__iQ=null;
}});
})();
(function(){var f="blur",e="focus",d="input",c="load",b="qx.ui.core.EventHandler",a="activate";
qx.Class.define(b,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(){qx.core.Object.call(this);
this.__iS=qx.event.Registration.getManager(window);
},statics:{PRIORITY:qx.event.Registration.PRIORITY_FIRST,SUPPORTED_TYPES:{mousemove:1,mouseover:1,mouseout:1,mousedown:1,mouseup:1,click:1,dblclick:1,contextmenu:1,mousewheel:1,keyup:1,keydown:1,keypress:1,keyinput:1,capture:1,losecapture:1,focusin:1,focusout:1,focus:1,blur:1,activate:1,deactivate:1,appear:1,disappear:1,dragstart:1,dragend:1,dragover:1,dragleave:1,drop:1,drag:1,dragchange:1,droprequest:1,touchstart:1,touchend:1,touchmove:1,touchcancel:1,tap:1,swipe:1},IGNORE_CAN_HANDLE:false},members:{__iS:null,__iT:{focusin:1,focusout:1,focus:1,blur:1},__iU:{mouseover:1,mouseout:1,appear:1,disappear:1},canHandleEvent:function(g,h){return g instanceof qx.ui.core.Widget;
},_dispatchEvent:function(j){var p=j.getTarget();
var o=qx.ui.core.Widget.getWidgetByElement(p);
var q=false;

while(o&&o.isAnonymous()){var q=true;
o=o.getLayoutParent();
}if(o&&q&&j.getType()==a){o.getContainerElement().activate();
}if(this.__iT[j.getType()]){o=o&&o.getFocusTarget();
if(!o){return;
}}if(j.getRelatedTarget){var x=j.getRelatedTarget();
var w=qx.ui.core.Widget.getWidgetByElement(x);

while(w&&w.isAnonymous()){w=w.getLayoutParent();
}
if(w){if(this.__iT[j.getType()]){w=w.getFocusTarget();
}if(w===o){return;
}}}var s=j.getCurrentTarget();
var u=qx.ui.core.Widget.getWidgetByElement(s);

if(!u||u.isAnonymous()){return;
}if(this.__iT[j.getType()]){u=u.getFocusTarget();
}var v=j.getType();

if(!u||!(u.isEnabled()||this.__iU[v])){return;
}var k=j.getEventPhase()==qx.event.type.Event.CAPTURING_PHASE;
var r=this.__iS.getListeners(u,v,k);

if(!r||r.length===0){return;
}var m=qx.event.Pool.getInstance().getObject(j.constructor);
j.clone(m);
m.setTarget(o);
m.setRelatedTarget(w||null);
m.setCurrentTarget(u);
var y=j.getOriginalTarget();

if(y){var n=qx.ui.core.Widget.getWidgetByElement(y);

while(n&&n.isAnonymous()){n=n.getLayoutParent();
}m.setOriginalTarget(n);
}else{m.setOriginalTarget(p);
}for(var i=0,l=r.length;i<l;i++){var t=r[i].context||u;
r[i].handler.call(t,m);
}if(m.getPropagationStopped()){j.stopPropagation();
}
if(m.getDefaultPrevented()){j.preventDefault();
}qx.event.Pool.getInstance().poolObject(m);
},registerEvent:function(z,A,B){var C;

if(A===e||A===f){C=z.getFocusElement();
}else if(A===c||A===d){C=z.getContentElement();
}else{C=z.getContainerElement();
}
if(C){C.addListener(A,this._dispatchEvent,this,B);
}},unregisterEvent:function(D,E,F){var G;

if(E===e||E===f){G=D.getFocusElement();
}else if(E===c||E===d){G=D.getContentElement();
}else{G=D.getContainerElement();
}
if(G){G.removeListener(E,this._dispatchEvent,this,F);
}}},destruct:function(){this.__iS=null;
},defer:function(H){qx.event.Registration.addHandler(H);
}});
})();
(function(){var p="",o="/",n="mshtml",m="qx.client",l="data",k="//",j=",",i="?",h="string",g="type",c=";",f="Falling back for",e="encoding",b="qx.util.ResourceManager",a="singleton",d="data:image/";
qx.Class.define(b,{extend:qx.core.Object,type:a,construct:function(){qx.core.Object.call(this);
},statics:{__iV:qx.$$resources||{},__iW:{}},members:{has:function(q){return !!this.self(arguments).__iV[q];
},getData:function(r){return this.self(arguments).__iV[r]||null;
},getImageWidth:function(s){var t=this.self(arguments).__iV[s];
return t?t[0]:null;
},getImageHeight:function(u){var v=this.self(arguments).__iV[u];
return v?v[1]:null;
},getImageFormat:function(w){var x=this.self(arguments).__iV[w];
return x?x[2]:null;
},isClippedImage:function(y){var A=this.self(arguments).__iV[y];
var z=A&&A.length>4;

if(z){var C=A[4];
var B=this.self(arguments).__iV[C];
z=B[2];
}return z;
},toUri:function(D){if(D==null){return D;
}var E=this.self(arguments).__iV[D];

if(!E){return D;
}
if(typeof E===h){var G=E;
}else{var G=E[3];
if(!G){return D;
}}var F=p;

if(qx.core.Variant.isSet(m,n)&&qx.bom.client.Feature.SSL){F=this.self(arguments).__iW[G];
}return F+qx.$$libraries[G].resourceUri+o+D;
},toDataUri:function(H){var J=this.constructor.__iV[H];
var K=this.constructor.__iV[J[4]];
var L;

if(K){var I=K[4][H];
L=d+I[g]+c+I[e]+j+I[l];
}else{console.log(f,H);
L=this.toUri(H);
}return L;
}},defer:function(M){if(qx.core.Variant.isSet(m,n)){if(qx.bom.client.Feature.SSL){for(var Q in qx.$$libraries){var O;

if(qx.$$libraries[Q].resourceUri){O=qx.$$libraries[Q].resourceUri;
}else{M.__iW[Q]=p;
continue;
}if(O.match(/^\/\//)!=null){M.__iW[Q]=window.location.protocol;
}else if(O.match(/^\//)!=null){M.__iW[Q]=window.location.protocol+k+window.location.host;
}else if(O.match(/^\.\//)!=null){var N=document.URL;
M.__iW[Q]=N.substring(0,N.lastIndexOf(o)+1);
}else if(O.match(/^http/)!=null){M.__iW[Q]=p;
}else{var R=window.location.href.indexOf(i);
var P;

if(R==-1){P=window.location.href;
}else{P=window.location.href.substring(0,R);
}M.__iW[Q]=P.substring(0,P.lastIndexOf(o)+1);
}}}}}});
})();
(function(){var c="qx.bom.client.Locale",b="-",a="";
qx.Class.define(c,{statics:{LOCALE:"",VARIANT:"",__iX:function(){var d=(navigator.userLanguage||navigator.language).toLowerCase();
var f=a;
var e=d.indexOf(b);

if(e!=-1){f=d.substr(e+1);
d=d.substr(0,e);
}this.LOCALE=d;
this.VARIANT=f;
}},defer:function(g){g.__iX();
}});
})();
(function(){var t="",s='indexOf',r='slice',q='concat',p='toLocaleLowerCase',o="qx.type.BaseString",n='match',m='toLocaleUpperCase',k='search',j='replace',c='toLowerCase',h='charCodeAt',f='split',b='substring',a='lastIndexOf',e='substr',d='toUpperCase',g='charAt';
qx.Class.define(o,{extend:Object,construct:function(u){var u=u||t;
this.__iY=u;
this.length=u.length;
},members:{$$isString:true,length:0,__iY:null,toString:function(){return this.__iY;
},charAt:null,valueOf:null,charCodeAt:null,concat:null,indexOf:null,lastIndexOf:null,match:null,replace:null,search:null,slice:null,split:null,substr:null,substring:null,toLowerCase:null,toUpperCase:null,toHashCode:function(){return qx.core.ObjectRegistry.toHashCode(this);
},toLocaleLowerCase:null,toLocaleUpperCase:null,base:function(v,w){return qx.core.Object.prototype.base.apply(this,arguments);
}},defer:function(x,y){{};
var z=[g,h,q,s,a,n,j,k,r,f,e,b,c,d,p,m];
y.valueOf=y.toString;

if(new x(t).valueOf()==null){delete y.valueOf;
}
for(var i=0,l=z.length;i<l;i++){y[z[i]]=String.prototype[z[i]];
}}});
})();
(function(){var a="qx.locale.LocalizedString";
qx.Class.define(a,{extend:qx.type.BaseString,construct:function(b,c,d){qx.type.BaseString.call(this,b);
this.__ja=c;
this.__jb=d;
},members:{__ja:null,__jb:null,translate:function(){return qx.locale.Manager.getInstance().translate(this.__ja,this.__jb);
}}});
})();
(function(){var k="_",j="",h="_applyLocale",g="changeLocale",f="C",e="qx.dynlocale",d="on",c="qx.locale.Manager",b="String",a="singleton";
qx.Class.define(c,{type:a,extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__jc=qx.$$translations||{};
this.__jd=qx.$$locales||{};
var n=qx.bom.client.Locale;
var l=n.LOCALE;
var m=n.VARIANT;

if(m!==j){l+=k+m;
}this.__je=l;
this.setLocale(l||this.__jf);
},statics:{tr:function(o,p){var q=qx.lang.Array.fromArguments(arguments);
q.splice(0,1);
return qx.locale.Manager.getInstance().translate(o,q);
},trn:function(r,s,t,u){var v=qx.lang.Array.fromArguments(arguments);
v.splice(0,3);
if(t!=1){return qx.locale.Manager.getInstance().translate(s,v);
}else{return qx.locale.Manager.getInstance().translate(r,v);
}},trc:function(w,x,y){var z=qx.lang.Array.fromArguments(arguments);
z.splice(0,2);
return qx.locale.Manager.getInstance().translate(x,z);
},marktr:function(A){return A;
}},properties:{locale:{check:b,nullable:true,apply:h,event:g}},members:{__jf:f,__jg:null,__jh:null,__jc:null,__jd:null,__je:null,getLanguage:function(){return this.__jh;
},getTerritory:function(){return this.getLocale().split(k)[1]||j;
},getAvailableLocales:function(){var C=[];

for(var B in this.__jd){if(B!=this.__jf){C.push(B);
}}return C;
},__ji:function(D){var F;
var E=D.indexOf(k);

if(E==-1){F=D;
}else{F=D.substring(0,E);
}return F;
},_applyLocale:function(G,H){{};
this.__jg=G;
this.__jh=this.__ji(G);
},addTranslation:function(I,J){var K=this.__jc;

if(K[I]){for(var L in J){K[I][L]=J[L];
}}else{K[I]=J;
}},addLocale:function(M,N){var O=this.__jd;

if(O[M]){for(var P in N){O[M][P]=N[P];
}}else{O[M]=N;
}},translate:function(Q,R,S){var T=this.__jc;
return this.__jj(T,Q,R,S);
},localize:function(U,V,W){var X=this.__jd;
return this.__jj(X,U,V,W);
},__jj:function(Y,ba,bb,bc){var bd;

if(!Y){return ba;
}
if(bc){var bf=this.__ji(bc);
}else{bc=this.__jg;
bf=this.__jh;
}if(!bd&&Y[bc]){bd=Y[bc][ba];
}if(!bd&&Y[bf]){bd=Y[bf][ba];
}if(!bd&&Y[this.__jf]){bd=Y[this.__jf][ba];
}
if(!bd){bd=ba;
}
if(bb.length>0){var be=[];

for(var i=0;i<bb.length;i++){var bg=bb[i];

if(bg&&bg.translate){be[i]=bg.translate();
}else{be[i]=bg;
}}bd=qx.lang.String.format(bd,be);
}
if(qx.core.Variant.isSet(e,d)){bd=new qx.locale.LocalizedString(bd,ba,bb);
}return bd;
}},destruct:function(){this.__jc=this.__jd=null;
}});
})();
(function(){var k="px",j="qx.client",i="div",h="img",g="",f="no-repeat",d="scale-x",c="mshtml",b="scale",a="b64",H="scale-y",G="qx/icon",F="repeat",E=".png",D="crop",C="progid:DXImageTransform.Microsoft.AlphaImageLoader(src='",B='<div style="',A="repeat-y",z='<img src="',y="qx.bom.element.Decoration",r="', sizingMethod='",s="png",p="')",q='"></div>',n='"/>',o='" style="',l="none",m="webkit",t=" ",u="repeat-x",w="DXImageTransform.Microsoft.AlphaImageLoader",v="qx/static/blank.gif",x="absolute";
qx.Class.define(y,{statics:{DEBUG:false,__jk:{},__jl:qx.core.Variant.isSet(j,c)&&qx.bom.client.Engine.VERSION<9,__jm:qx.core.Variant.select(j,{"mshtml":{"scale-x":true,"scale-y":true,"scale":true,"no-repeat":true},"default":null}),__jn:{"scale-x":h,"scale-y":h,"scale":h,"repeat":i,"no-repeat":i,"repeat-x":i,"repeat-y":i},update:function(I,J,K,L){var N=this.getTagName(K,J);

if(N!=I.tagName.toLowerCase()){throw new Error("Image modification not possible because elements could not be replaced at runtime anymore!");
}var O=this.getAttributes(J,K,L);

if(N===h){I.src=O.src||qx.util.ResourceManager.getInstance().toUri(v);
}if(I.style.backgroundPosition!=g&&O.style.backgroundPosition===undefined){O.style.backgroundPosition=null;
}if(I.style.clip!=g&&O.style.clip===undefined){O.style.clip=null;
}var M=qx.bom.element.Style;
M.setStyles(I,O.style);
if(this.__jl){try{I.filters[w].apply();
}catch(e){}}},create:function(P,Q,R){var S=this.getTagName(Q,P);
var U=this.getAttributes(P,Q,R);
var T=qx.bom.element.Style.compile(U.style);

if(S===h){return z+U.src+o+T+n;
}else{return B+T+q;
}},getTagName:function(V,W){if(qx.core.Variant.isSet(j,c)){if(W&&this.__jl&&this.__jm[V]&&qx.lang.String.endsWith(W,E)){return i;
}}return this.__jn[V];
},getAttributes:function(X,Y,ba){if(!ba){ba={};
}
if(!ba.position){ba.position=x;
}
if(qx.core.Variant.isSet(j,c)){ba.fontSize=0;
ba.lineHeight=0;
}else if(qx.core.Variant.isSet(j,m)){ba.WebkitUserDrag=l;
}var bc=qx.util.ResourceManager.getInstance().getImageFormat(X)||qx.io.ImageLoader.getFormat(X);
{};
var bb;
if(this.__jl&&this.__jm[Y]&&bc===s){bb=this.__jq(ba,Y,X);
}else{if(Y===b){bb=this.__jr(ba,Y,X);
}else if(Y===d||Y===H){bb=this.__js(ba,Y,X);
}else{bb=this.__jv(ba,Y,X);
}}return bb;
},__jo:function(bd,be,bf){if(bd.width==null&&be!=null){bd.width=be+k;
}
if(bd.height==null&&bf!=null){bd.height=bf+k;
}return bd;
},__jp:function(bh){var bi=qx.util.ResourceManager.getInstance().getImageWidth(bh)||qx.io.ImageLoader.getWidth(bh);
var bj=qx.util.ResourceManager.getInstance().getImageHeight(bh)||qx.io.ImageLoader.getHeight(bh);
return {width:bi,height:bj};
},__jq:function(bk,bl,bm){var bp=this.__jp(bm);
bk=this.__jo(bk,bp.width,bp.height);
var bo=bl==f?D:b;
var bn=C+qx.util.ResourceManager.getInstance().toUri(bm)+r+bo+p;
bk.filter=bn;
bk.backgroundImage=bk.backgroundRepeat=g;
return {style:bk};
},__jr:function(bq,br,bs){var bt=qx.util.ResourceManager.getInstance().toUri(bs);
var bu=this.__jp(bs);
bq=this.__jo(bq,bu.width,bu.height);
return {src:bt,style:bq};
},__js:function(bv,bw,bx){var by=qx.util.ResourceManager.getInstance();
var bB=by.isClippedImage(bx);
var bD=this.__jp(bx);
var bz;

if(bB){var bC=by.getData(bx);
var bA=bC[4];

if(bB==a){bz=by.toDataUri(bx);
}else{bz=by.toUri(bA);
}
if(bw===d){bv=this.__jt(bv,bC,bD.height);
}else{bv=this.__ju(bv,bC,bD.width);
}return {src:bz,style:bv};
}else{{};

if(bw==d){bv.height=bD.height==null?null:bD.height+k;
}else if(bw==H){bv.width=bD.width==null?null:bD.width+k;
}bz=by.toUri(bx);
return {src:bz,style:bv};
}},__jt:function(bE,bF,bG){var bH=qx.util.ResourceManager.getInstance().getImageHeight(bF[4]);
bE.clip={top:-bF[6],height:bG};
bE.height=bH+k;
if(bE.top!=null){bE.top=(parseInt(bE.top,10)+bF[6])+k;
}else if(bE.bottom!=null){bE.bottom=(parseInt(bE.bottom,10)+bG-bH-bF[6])+k;
}return bE;
},__ju:function(bI,bJ,bK){var bL=qx.util.ResourceManager.getInstance().getImageWidth(bJ[4]);
bI.clip={left:-bJ[5],width:bK};
bI.width=bL+k;
if(bI.left!=null){bI.left=(parseInt(bI.left,10)+bJ[5])+k;
}else if(bI.right!=null){bI.right=(parseInt(bI.right,10)+bK-bL-bJ[5])+k;
}return bI;
},__jv:function(bM,bN,bO){var bR=qx.util.ResourceManager.getInstance();
var bW=bR.isClippedImage(bO);
var bY=this.__jp(bO);
if(bW&&bN!==F){var bX=bR.getData(bO);
var bV=bX[4];

if(bW==a){var bU=bR.toDataUri(bO);
var bT=bS=0;
}else{var bU=bR.toUri(bV);
var bT=bX[5];
var bS=bX[6];
}var bP=qx.bom.element.Background.getStyles(bU,bN,bT,bS);

for(var bQ in bP){bM[bQ]=bP[bQ];
}
if(bY.width!=null&&bM.width==null&&(bN==A||bN===f)){bM.width=bY.width+k;
}
if(bY.height!=null&&bM.height==null&&(bN==u||bN===f)){bM.height=bY.height+k;
}return {style:bM};
}else{{};
bM=this.__jo(bM,bY.width,bY.height);
bM=this.__jw(bM,bO,bN);
return {style:bM};
}},__jw:function(ca,cb,cc){var top=null;
var cg=null;

if(ca.backgroundPosition){var cd=ca.backgroundPosition.split(t);
cg=parseInt(cd[0],10);

if(isNaN(cg)){cg=cd[0];
}top=parseInt(cd[1],10);

if(isNaN(top)){top=cd[1];
}}var cf=qx.bom.element.Background.getStyles(cb,cc,cg,top);

for(var ce in cf){ca[ce]=cf[ce];
}if(ca.filter){ca.filter=g;
}return ca;
},__jx:function(ch){if(this.DEBUG&&qx.util.ResourceManager.getInstance().has(ch)&&ch.indexOf(G)==-1){if(!this.__jk[ch]){qx.log.Logger.debug("Potential clipped image candidate: "+ch);
this.__jk[ch]=true;
}}},isAlphaImageLoaderEnabled:qx.core.Variant.select(j,{"mshtml":function(){return qx.bom.element.Decoration.__jl;
},"default":function(){return false;
}})}});
})();
(function(){var c="qx.client",b="load",a="qx.io.ImageLoader";
qx.Bootstrap.define(a,{statics:{__jy:{},__jz:{width:null,height:null},__jA:/\.(png|gif|jpg|jpeg|bmp)\b/i,isLoaded:function(d){var e=this.__jy[d];
return !!(e&&e.loaded);
},isFailed:function(f){var g=this.__jy[f];
return !!(g&&g.failed);
},isLoading:function(h){var j=this.__jy[h];
return !!(j&&j.loading);
},getFormat:function(k){var m=this.__jy[k];
return m?m.format:null;
},getSize:function(n){var o=this.__jy[n];
return o?
{width:o.width,height:o.height}:this.__jz;
},getWidth:function(p){var q=this.__jy[p];
return q?q.width:null;
},getHeight:function(r){var s=this.__jy[r];
return s?s.height:null;
},load:function(t,u,v){var w=this.__jy[t];

if(!w){w=this.__jy[t]={};
}if(u&&!v){v=window;
}if(w.loaded||w.loading||w.failed){if(u){if(w.loading){w.callbacks.push(u,v);
}else{u.call(v,t,w);
}}}else{w.loading=true;
w.callbacks=[];

if(u){w.callbacks.push(u,v);
}var y=new Image();
var x=qx.lang.Function.listener(this.__jB,this,y,t);
y.onload=x;
y.onerror=x;
y.src=t;
w.element=y;
}},abort:function(z){var A=this.__jy[z];

if(A&&!A.loaded){A.aborted=true;
var C=A.callbacks;
var B=A.element;
B.onload=B.onerror=null;
delete A.callbacks;
delete A.element;
delete A.loading;

for(var i=0,l=C.length;i<l;i+=2){C[i].call(C[i+1],z,A);
}}this.__jy[z]=null;
},__jB:qx.event.GlobalError.observeMethod(function(event,D,E){var F=this.__jy[E];
if(event.type===b){F.loaded=true;
F.width=this.__jC(D);
F.height=this.__jD(D);
var G=this.__jA.exec(E);

if(G!=null){F.format=G[1];
}}else{F.failed=true;
}D.onload=D.onerror=null;
var H=F.callbacks;
delete F.loading;
delete F.callbacks;
delete F.element;
for(var i=0,l=H.length;i<l;i+=2){H[i].call(H[i+1],E,F);
}}),__jC:qx.core.Variant.select(c,{"gecko":function(I){return I.naturalWidth;
},"default":function(J){return J.width;
}}),__jD:qx.core.Variant.select(c,{"gecko":function(K){return K.naturalHeight;
},"default":function(L){return L.height;
}})}});
})();
(function(){var r="number",q="0",p="px",o=";",n="'",m="')",l="background-image:url(",k=");",j="",i=")",c="background-repeat:",h="data:",f=" ",b="qx.bom.element.Background",a="url(",e="background-position:",d="base64",g="url('";
qx.Class.define(b,{statics:{__jE:[l,null,k,e,null,o,c,null,o],__jF:{backgroundImage:null,backgroundPosition:null,backgroundRepeat:null},__jG:function(s,top){var t=qx.bom.client.Engine;

if(t.GECKO&&t.VERSION<1.9&&s==top&&typeof s==r){top+=0.01;
}
if(s){var u=(typeof s==r)?s+p:s;
}else{u=q;
}
if(top){var v=(typeof top==r)?top+p:top;
}else{v=q;
}return u+f+v;
},__tT:function(w){var String=qx.lang.String;
var x=w.substr(0,50);
return String.startsWith(x,h)&&String.contains(x,d);
},compile:function(y,z,A,top){var B=this.__jG(A,top);
var C=qx.util.ResourceManager.getInstance().toUri(y);

if(this.__tT(C)){C=n+C+n;
}var D=this.__jE;
D[1]=C;
D[4]=B;
D[7]=z;
return D.join(j);
},getStyles:function(E,F,G,top){if(!E){return this.__jF;
}var H=this.__jG(G,top);
var J=qx.util.ResourceManager.getInstance().toUri(E);
var K;

if(this.__tT(J)){K=g+J+m;
}else{K=a+J+i;
}var I={backgroundPosition:H,backgroundImage:K};

if(F!=null){I.backgroundRepeat=F;
}return I;
},set:function(L,M,N,O,top){var P=this.getStyles(M,N,O,top);

for(var Q in P){L.style[Q]=P[Q];
}}}});
})();
(function(){var k="source",j="scale",i="no-repeat",h="qx.client",g="",f="mshtml",e="webkit",d="backgroundImage",c="div",b="qx.html.Image",a="qx/static/blank.gif";
qx.Class.define(b,{extend:qx.html.Element,members:{tagNameHint:null,_applyProperty:function(name,l){qx.html.Element.prototype._applyProperty.call(this,name,l);

if(name===k){var p=this.getDomElement();
var m=this.getAllStyles();

if(this.getNodeName()==c&&this.getStyle(d)){m.backgroundPosition=null;
m.backgroundRepeat=null;
}var n=this._getProperty(k);
var o=this._getProperty(j);
var q=o?j:i;
if(n!=null){n=n||null;
qx.bom.element.Decoration.update(p,n,q,m);
}}},_removeProperty:function(r,s){if(r==k){this._setProperty(r,g,s);
}else{this._setProperty(r,null,s);
}},_createDomElement:function(){var u=this._getProperty(j);
var v=u?j:i;

if(qx.core.Variant.isSet(h,f)){var t=this._getProperty(k);

if(this.tagNameHint!=null){this.setNodeName(this.tagNameHint);
}else{this.setNodeName(qx.bom.element.Decoration.getTagName(v,t));
}}else{this.setNodeName(qx.bom.element.Decoration.getTagName(v));
}return qx.html.Element.prototype._createDomElement.call(this);
},_copyData:function(w){return qx.html.Element.prototype._copyData.call(this,true);
},setSource:function(x){this._setProperty(k,x);
return this;
},getSource:function(){return this._getProperty(k);
},resetSource:function(){if(qx.core.Variant.isSet(h,e)){this._setProperty(k,qx.util.ResourceManager.getInstance().toUri(a));
}else{this._removeProperty(k,true);
}return this;
},setScale:function(y){this._setProperty(j,y);
return this;
},getScale:function(){return this._getProperty(j);
}}});
})();
(function(){var j="nonScaled",i="scaled",h="alphaScaled",g=".png",f="qx.client",e="div",d="replacement",c="qx.event.type.Event",b="hidden",a="Boolean",y="px",x="scale",w="changeSource",v="qx.ui.basic.Image",u="loaded",t="-disabled.$1",s="loadingFailed",r="String",q="_applySource",p="img",n="image",o="mshtml",l="_applyScale",m="__jH",k="no-repeat";
qx.Class.define(v,{extend:qx.ui.core.Widget,construct:function(z){this.__jH={};
qx.ui.core.Widget.call(this);

if(z){this.setSource(z);
}},properties:{source:{check:r,init:null,nullable:true,event:w,apply:q,themeable:true},scale:{check:a,init:false,themeable:true,apply:l},appearance:{refine:true,init:n},allowShrinkX:{refine:true,init:false},allowShrinkY:{refine:true,init:false},allowGrowX:{refine:true,init:false},allowGrowY:{refine:true,init:false}},events:{loadingFailed:c,loaded:c},members:{__jI:null,__jJ:null,__jK:null,__jH:null,getContentElement:function(){return this.__jO();
},_createContentElement:function(){return this.__jO();
},_getContentHint:function(){return {width:this.__jI||0,height:this.__jJ||0};
},_applyEnabled:function(A,B){qx.ui.core.Widget.prototype._applyEnabled.call(this,A,B);

if(this.getSource()){this._styleSource();
}},_applySource:function(C){this._styleSource();
},_applyScale:function(D){this._styleSource();
},__jL:function(E){this.__jK=E;
},__jM:function(){if(this.__jK==null){var G=this.getSource();
var F=false;

if(G!=null){F=qx.lang.String.endsWith(G,g);
}
if(this.getScale()&&F&&qx.bom.element.Decoration.isAlphaImageLoaderEnabled()){this.__jK=h;
}else if(this.getScale()){this.__jK=i;
}else{this.__jK=j;
}}return this.__jK;
},__jN:function(H){var I;
var J;

if(H==h){I=true;
J=e;
}else if(H==j){I=false;
J=e;
}else{I=true;
J=p;
}var K=new qx.html.Image(J);
K.setScale(I);
K.setStyles({"overflowX":b,"overflowY":b});
return K;
},__jO:function(){var L=this.__jM();

if(this.__jH[L]==null){this.__jH[L]=this.__jN(L);
}return this.__jH[L];
},_styleSource:function(){var M=qx.util.AliasManager.getInstance().resolve(this.getSource());

if(!M){this.getContentElement().resetSource();
return;
}this.__jP(M);

if(qx.core.Variant.isSet(f,o)){var N=this.getScale()?x:k;
this.getContentElement().tagNameHint=qx.bom.element.Decoration.getTagName(N,M);
}if(qx.util.ResourceManager.getInstance().has(M)){this.__jR(this.getContentElement(),M);
}else if(qx.io.ImageLoader.isLoaded(M)){this.__jS(this.getContentElement(),M);
}else{this.__jT(this.getContentElement(),M);
}},__jP:qx.core.Variant.select(f,{"mshtml":function(O){var Q=qx.bom.element.Decoration.isAlphaImageLoaderEnabled();
var P=qx.lang.String.endsWith(O,g);

if(Q&&P){if(this.getScale()&&this.__jM()!=h){this.__jL(h);
}else if(!this.getScale()&&this.__jM()!=j){this.__jL(j);
}}else{if(this.getScale()&&this.__jM()!=i){this.__jL(i);
}else if(!this.getScale()&&this.__jM()!=j){this.__jL(j);
}}this.__jQ(this.__jO());
},"default":function(R){if(this.getScale()&&this.__jM()!=i){this.__jL(i);
}else if(!this.getScale()&&this.__jM(j)){this.__jL(j);
}this.__jQ(this.__jO());
}}),__jQ:function(S){var V=this.getContainerElement();
var W=V.getChild(0);

if(W!=S){if(W!=null){var Y=y;
var T={};
var U=this.getInnerSize();

if(U!=null){T.width=U.width+Y;
T.height=U.height+Y;
}var X=this.getInsets();
T.left=X.left+Y;
T.top=X.top+Y;
T.zIndex=10;
S.setStyles(T,true);
S.setSelectable(this.getSelectable());
}V.removeAt(0);
V.addAt(S,0);
}},__jR:function(ba,bb){var bd=qx.util.ResourceManager.getInstance();
if(!this.getEnabled()){var bc=bb.replace(/\.([a-z]+)$/,t);

if(bd.has(bc)){bb=bc;
this.addState(d);
}else{this.removeState(d);
}}if(ba.getSource()===bb){return;
}ba.setSource(bb);
this.__jV(bd.getImageWidth(bb),bd.getImageHeight(bb));
},__jS:function(be,bf){var bh=qx.io.ImageLoader;
be.setSource(bf);
var bg=bh.getWidth(bf);
var bi=bh.getHeight(bf);
this.__jV(bg,bi);
},__jT:function(bj,bk){var self;
var bl=qx.io.ImageLoader;
{};
if(!bl.isFailed(bk)){bl.load(bk,this.__jU,this);
}else{if(bj!=null){bj.resetSource();
}}},__jU:function(bm,bn){if(this.$$disposed===true){return;
}if(bm!==qx.util.AliasManager.getInstance().resolve(this.getSource())){return;
}if(bn.failed){this.warn("Image could not be loaded: "+bm);
this.fireEvent(s);
}else{this.fireEvent(u);
}this._styleSource();
},__jV:function(bo,bp){if(bo!==this.__jI||bp!==this.__jJ){this.__jI=bo;
this.__jJ=bp;
qx.ui.core.queue.Layout.add(this);
}}},destruct:function(){this._disposeMap(m);
}});
})();
(function(){var g="dragdrop-cursor",f="_applyAction",e="alias",d="qx.ui.core.DragDropCursor",c="move",b="singleton",a="copy";
qx.Class.define(d,{extend:qx.ui.basic.Image,include:qx.ui.core.MPlacement,type:b,construct:function(){qx.ui.basic.Image.call(this);
this.setZIndex(1e8);
this.setDomMove(true);
var h=this.getApplicationRoot();
h.add(this,{left:-1000,top:-1000});
},properties:{appearance:{refine:true,init:g},action:{check:[e,a,c],apply:f,nullable:true}},members:{_applyAction:function(i,j){if(j){this.removeState(j);
}
if(i){this.addState(i);
}}}});
})();
(function(){var f="mousedown",d="blur",c="__jW",b="singleton",a="qx.ui.popup.Manager";
qx.Class.define(a,{type:b,extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__jW=[];
qx.event.Registration.addListener(document.documentElement,f,this.__jY,this,true);
qx.bom.Element.addListener(window,d,this.hideAll,this);
},members:{__jW:null,add:function(g){{};
this.__jW.push(g);
this.__jX();
},remove:function(h){{};

if(this.__jW){qx.lang.Array.remove(this.__jW,h);
this.__jX();
}},hideAll:function(){var j;
var k=this.__jW;

if(k){for(var i=0,l=k.length;i<l;i++){var j=k[i];
j.getAutoHide()&&j.exclude();
}}},__jX:function(){var m=1e7;

for(var i=0;i<this.__jW.length;i++){this.__jW[i].setZIndex(m++);
}},__jY:function(e){var o=qx.ui.core.Widget.getWidgetByElement(e.getTarget());
var p=this.__jW;

for(var i=0;i<p.length;i++){var n=p[i];

if(!n.getAutoHide()||o==n||qx.ui.core.Widget.contains(n,o)){continue;
}n.exclude();
}}},destruct:function(){qx.event.Registration.removeListener(document.documentElement,f,this.__jY,this,true);
this._disposeArray(c);
}});
})();
(function(){var b="abstract",a="qx.ui.layout.Abstract";
qx.Class.define(a,{type:b,extend:qx.core.Object,members:{__ka:null,_invalidChildrenCache:null,__kb:null,invalidateLayoutCache:function(){this.__ka=null;
},renderLayout:function(c,d){this.warn("Missing renderLayout() implementation!");
},getSizeHint:function(){if(this.__ka){return this.__ka;
}return this.__ka=this._computeSizeHint();
},hasHeightForWidth:function(){return false;
},getHeightForWidth:function(e){this.warn("Missing getHeightForWidth() implementation!");
return null;
},_computeSizeHint:function(){return null;
},invalidateChildrenCache:function(){this._invalidChildrenCache=true;
},verifyLayoutProperty:null,_clearSeparators:function(){var f=this.__kb;

if(f instanceof qx.ui.core.LayoutItem){f.clearSeparators();
}},_renderSeparator:function(g,h){this.__kb.renderSeparator(g,h);
},connectToWidget:function(i){if(i&&this.__kb){throw new Error("It is not possible to manually set the connected widget.");
}this.__kb=i;
this.invalidateChildrenCache();
},_getWidget:function(){return this.__kb;
},_applyLayoutChange:function(){if(this.__kb){this.__kb.scheduleLayoutUpdate();
}},_getLayoutChildren:function(){return this.__kb.getLayoutChildren();
}},destruct:function(){this.__kb=this.__ka=null;
}});
})();
(function(){var a="qx.ui.layout.Grow";
qx.Class.define(a,{extend:qx.ui.layout.Abstract,members:{verifyLayoutProperty:null,renderLayout:function(b,c){var g=this._getLayoutChildren();
var f,h,e,d;
for(var i=0,l=g.length;i<l;i++){f=g[i];
h=f.getSizeHint();
e=b;

if(e<h.minWidth){e=h.minWidth;
}else if(e>h.maxWidth){e=h.maxWidth;
}d=c;

if(d<h.minHeight){d=h.minHeight;
}else if(d>h.maxHeight){d=h.maxHeight;
}f.renderLayout(0,0,e,d);
}},_computeSizeHint:function(){var q=this._getLayoutChildren();
var o,s;
var r=0,p=0;
var n=0,k=0;
var j=Infinity,m=Infinity;
for(var i=0,l=q.length;i<l;i++){o=q[i];
s=o.getSizeHint();
r=Math.max(r,s.width);
p=Math.max(p,s.height);
n=Math.max(n,s.minWidth);
k=Math.max(k,s.minHeight);
j=Math.min(j,s.maxWidth);
m=Math.min(m,s.maxHeight);
}return {width:r,height:p,minWidth:n,minHeight:k,maxWidth:j,maxHeight:m};
}}});
})();
(function(){var j="label",i="icon",h="Boolean",g="both",f="String",e="left",d="changeGap",c="changeShow",b="bottom",a="_applyCenter",y="changeIcon",x="qx.ui.basic.Atom",w="changeLabel",v="Integer",u="_applyIconPosition",t="bottom-left",s="top-left",r="top",q="right",p="_applyRich",n="_applyIcon",o="_applyShow",l="_applyLabel",m="_applyGap",k="atom";
qx.Class.define(x,{extend:qx.ui.core.Widget,construct:function(z,A){{};
qx.ui.core.Widget.call(this);
this._setLayout(new qx.ui.layout.Atom());

if(z!=null){this.setLabel(z);
}
if(A!=null){this.setIcon(A);
}},properties:{appearance:{refine:true,init:k},label:{apply:l,nullable:true,check:f,event:w},rich:{check:h,init:false,apply:p},icon:{check:f,apply:n,nullable:true,themeable:true,event:y},gap:{check:v,nullable:false,event:d,apply:m,themeable:true,init:4},show:{init:g,check:[g,j,i],themeable:true,inheritable:true,apply:o,event:c},iconPosition:{init:e,check:[r,q,b,e,s,t],themeable:true,apply:u},center:{init:false,check:h,themeable:true,apply:a}},members:{_createChildControlImpl:function(B,C){var D;

switch(B){case j:D=new qx.ui.basic.Label(this.getLabel());
D.setAnonymous(true);
D.setRich(this.getRich());
this._add(D);

if(this.getLabel()==null||this.getShow()===i){D.exclude();
}break;
case i:D=new qx.ui.basic.Image(this.getIcon());
D.setAnonymous(true);
this._addAt(D,0);

if(this.getIcon()==null||this.getShow()===j){D.exclude();
}break;
}return D||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,B);
},_forwardStates:{focused:true,hovered:true},_handleLabel:function(){if(this.getLabel()==null||this.getShow()===i){this._excludeChildControl(j);
}else{this._showChildControl(j);
}},_handleIcon:function(){if(this.getIcon()==null||this.getShow()===j){this._excludeChildControl(i);
}else{this._showChildControl(i);
}},_applyLabel:function(E,F){var G=this.getChildControl(j,true);

if(G){G.setValue(E);
}this._handleLabel();
},_applyRich:function(H,I){var J=this.getChildControl(j,true);

if(J){J.setRich(H);
}},_applyIcon:function(K,L){var M=this.getChildControl(i,true);

if(M){M.setSource(K);
}this._handleIcon();
},_applyGap:function(N,O){this._getLayout().setGap(N);
},_applyShow:function(P,Q){this._handleLabel();
this._handleIcon();
},_applyIconPosition:function(R,S){this._getLayout().setIconPosition(R);
},_applyCenter:function(T,U){this._getLayout().setCenter(T);
},_applySelectable:function(V,W){qx.ui.core.Widget.prototype._applySelectable.call(this,V,W);
var X=this.getChildControl(j,true);

if(X){this.getChildControl(j).setSelectable(V);
}}}});
})();
(function(){var m="bottom",l="top",k="_applyLayoutChange",j="top-left",h="bottom-left",g="left",f="right",e="middle",d="center",c="qx.ui.layout.Atom",a="Integer",b="Boolean";
qx.Class.define(c,{extend:qx.ui.layout.Abstract,properties:{gap:{check:a,init:4,apply:k},iconPosition:{check:[g,l,f,m,j,h],init:g,apply:k},center:{check:b,init:false,apply:k}},members:{verifyLayoutProperty:null,renderLayout:function(n,o){var x=qx.ui.layout.Util;
var q=this.getIconPosition();
var t=this._getLayoutChildren();
var length=t.length;
var I,top,H,r;
var C,w;
var A=this.getGap();
var F=this.getCenter();
if(q===m||q===f){var y=length-1;
var u=-1;
var s=-1;
}else{var y=0;
var u=length;
var s=1;
}if(q==l||q==m){if(F){var B=0;

for(var i=y;i!=u;i+=s){r=t[i].getSizeHint().height;

if(r>0){B+=r;

if(i!=y){B+=A;
}}}top=Math.round((o-B)/2);
}else{top=0;
}
for(var i=y;i!=u;i+=s){C=t[i];
w=C.getSizeHint();
H=Math.min(w.maxWidth,Math.max(n,w.minWidth));
r=w.height;
I=x.computeHorizontalAlignOffset(d,H,n);
C.renderLayout(I,top,H,r);
if(r>0){top+=r+A;
}}}else{var v=n;
var p=null;
var E=0;

for(var i=y;i!=u;i+=s){C=t[i];
H=C.getSizeHint().width;

if(H>0){if(!p&&C instanceof qx.ui.basic.Label){p=C;
}else{v-=H;
}E++;
}}
if(E>1){var D=(E-1)*A;
v-=D;
}
if(p){var w=p.getSizeHint();
var z=Math.max(w.minWidth,Math.min(v,w.maxWidth));
v-=z;
}
if(F&&v>0){I=Math.round(v/2);
}else{I=0;
}
for(var i=y;i!=u;i+=s){C=t[i];
w=C.getSizeHint();
r=Math.min(w.maxHeight,Math.max(o,w.minHeight));

if(C===p){H=z;
}else{H=w.width;
}var G=e;

if(q==j){G=l;
}else if(q==h){G=m;
}top=x.computeVerticalAlignOffset(G,w.height,o);
C.renderLayout(I,top,H,r);
if(H>0){I+=H+A;
}}}},_computeSizeHint:function(){var T=this._getLayoutChildren();
var length=T.length;
var L,R;
if(length===1){var L=T[0].getSizeHint();
R={width:L.width,height:L.height,minWidth:L.minWidth,minHeight:L.minHeight};
}else{var P=0,Q=0;
var M=0,O=0;
var N=this.getIconPosition();
var S=this.getGap();

if(N===l||N===m){var J=0;

for(var i=0;i<length;i++){L=T[i].getSizeHint();
Q=Math.max(Q,L.width);
P=Math.max(P,L.minWidth);
if(L.height>0){O+=L.height;
M+=L.minHeight;
J++;
}}
if(J>1){var K=(J-1)*S;
O+=K;
M+=K;
}}else{var J=0;

for(var i=0;i<length;i++){L=T[i].getSizeHint();
O=Math.max(O,L.height);
M=Math.max(M,L.minHeight);
if(L.width>0){Q+=L.width;
P+=L.minWidth;
J++;
}}
if(J>1){var K=(J-1)*S;
Q+=K;
P+=K;
}}R={minWidth:P,width:Q,minHeight:M,height:O};
}return R;
}}});
})();
(function(){var g="middle",f="qx.ui.layout.Util",e="left",d="center",c="top",b="bottom",a="right";
qx.Class.define(f,{statics:{PERCENT_VALUE:/[0-9]+(?:\.[0-9]+)?%/,computeFlexOffsets:function(h,j,k){var n,r,m,s;
var o=j>k;
var t=Math.abs(j-k);
var u,p;
var q={};

for(r in h){n=h[r];
q[r]={potential:o?n.max-n.value:n.value-n.min,flex:o?n.flex:1/n.flex,offset:0};
}while(t!=0){s=Infinity;
m=0;

for(r in q){n=q[r];

if(n.potential>0){m+=n.flex;
s=Math.min(s,n.potential/n.flex);
}}if(m==0){break;
}s=Math.min(t,s*m)/m;
u=0;

for(r in q){n=q[r];

if(n.potential>0){p=Math.min(t,n.potential,Math.ceil(s*n.flex));
u+=p-s*n.flex;

if(u>=1){u-=1;
p-=1;
}n.potential-=p;

if(o){n.offset+=p;
}else{n.offset-=p;
}t-=p;
}}}return q;
},computeHorizontalAlignOffset:function(v,w,x,y,z){if(y==null){y=0;
}
if(z==null){z=0;
}var A=0;

switch(v){case e:A=y;
break;
case a:A=x-w-z;
break;
case d:A=Math.round((x-w)/2);
if(A<y){A=y;
}else if(A<z){A=Math.max(y,x-w-z);
}break;
}return A;
},computeVerticalAlignOffset:function(B,C,D,E,F){if(E==null){E=0;
}
if(F==null){F=0;
}var G=0;

switch(B){case c:G=E;
break;
case b:G=D-C-F;
break;
case g:G=Math.round((D-C)/2);
if(G<E){G=E;
}else if(G<F){G=Math.max(E,D-C-F);
}break;
}return G;
},collapseMargins:function(H){var I=0,K=0;

for(var i=0,l=arguments.length;i<l;i++){var J=arguments[i];

if(J<0){K=Math.min(K,J);
}else if(J>0){I=Math.max(I,J);
}}return I+K;
},computeHorizontalGaps:function(L,M,N){if(M==null){M=0;
}var O=0;

if(N){O+=L[0].getMarginLeft();

for(var i=1,l=L.length;i<l;i+=1){O+=this.collapseMargins(M,L[i-1].getMarginRight(),L[i].getMarginLeft());
}O+=L[l-1].getMarginRight();
}else{for(var i=1,l=L.length;i<l;i+=1){O+=L[i].getMarginLeft()+L[i].getMarginRight();
}O+=(M*(l-1));
}return O;
},computeVerticalGaps:function(P,Q,R){if(Q==null){Q=0;
}var S=0;

if(R){S+=P[0].getMarginTop();

for(var i=1,l=P.length;i<l;i+=1){S+=this.collapseMargins(Q,P[i-1].getMarginBottom(),P[i].getMarginTop());
}S+=P[l-1].getMarginBottom();
}else{for(var i=1,l=P.length;i<l;i+=1){S+=P[i].getMarginTop()+P[i].getMarginBottom();
}S+=(Q*(l-1));
}return S;
},computeHorizontalSeparatorGaps:function(T,U,V){var Y=qx.theme.manager.Decoration.getInstance().resolve(V);
var X=Y.getInsets();
var W=X.left+X.right;
var ba=0;

for(var i=0,l=T.length;i<l;i++){var bb=T[i];
ba+=bb.getMarginLeft()+bb.getMarginRight();
}ba+=(U+W+U)*(l-1);
return ba;
},computeVerticalSeparatorGaps:function(bc,bd,be){var bh=qx.theme.manager.Decoration.getInstance().resolve(be);
var bg=bh.getInsets();
var bf=bg.top+bg.bottom;
var bi=0;

for(var i=0,l=bc.length;i<l;i++){var bj=bc[i];
bi+=bj.getMarginTop()+bj.getMarginBottom();
}bi+=(bd+bf+bd)*(l-1);
return bi;
},arrangeIdeals:function(bk,bl,bm,bn,bo,bp){if(bl<bk||bo<bn){if(bl<bk&&bo<bn){bl=bk;
bo=bn;
}else if(bl<bk){bo-=(bk-bl);
bl=bk;
if(bo<bn){bo=bn;
}}else if(bo<bn){bl-=(bn-bo);
bo=bn;
if(bl<bk){bl=bk;
}}}
if(bl>bm||bo>bp){if(bl>bm&&bo>bp){bl=bm;
bo=bp;
}else if(bl>bm){bo+=(bl-bm);
bl=bm;
if(bo>bp){bo=bp;
}}else if(bo>bp){bl+=(bo-bp);
bo=bp;
if(bl>bm){bl=bm;
}}}return {begin:bl,end:bo};
}}});
})();
(function(){var b="qx.event.type.Data",a="qx.ui.form.IStringForm";
qx.Interface.define(a,{events:{"changeValue":b},members:{setValue:function(c){return arguments.length==1;
},resetValue:function(){},getValue:function(){}}});
})();
(function(){var k="qx.dynlocale",j="Boolean",i="color",h="changeLocale",g="enabled",f="on",d="_applyTextAlign",c="qx.ui.core.Widget",b="nowrap",a="changeTextAlign",C="_applyWrap",B="A",A="changeContent",z="qx.ui.basic.Label",y="whiteSpace",x="_applyValue",w="center",v="_applyBuddy",u="String",t="textAlign",r="right",s="changeRich",p="normal",q="_applyRich",n="click",o="label",l="left",m="changeValue";
qx.Class.define(z,{extend:qx.ui.core.Widget,implement:[qx.ui.form.IStringForm],construct:function(D){qx.ui.core.Widget.call(this);

if(D!=null){this.setValue(D);
}
if(qx.core.Variant.isSet(k,f)){qx.locale.Manager.getInstance().addListener(h,this._onChangeLocale,this);
}},properties:{rich:{check:j,init:false,event:s,apply:q},wrap:{check:j,init:true,apply:C},value:{check:u,apply:x,event:m,nullable:true},buddy:{check:c,apply:v,nullable:true,init:null,dereference:true},textAlign:{check:[l,w,r],nullable:true,themeable:true,apply:d,event:a},appearance:{refine:true,init:o},selectable:{refine:true,init:false},allowGrowX:{refine:true,init:false},allowGrowY:{refine:true,init:false},allowShrinkY:{refine:true,init:false}},members:{__kc:null,__kd:null,__ke:null,__kf:null,_getContentHint:function(){if(this.__kd){this.__kg=this.__kh();
delete this.__kd;
}return {width:this.__kg.width,height:this.__kg.height};
},_hasHeightForWidth:function(){return this.getRich()&&this.getWrap();
},_applySelectable:function(E){if(!qx.bom.client.Feature.CSS_TEXT_OVERFLOW&&qx.bom.client.Feature.XUL){if(E&&!this.isRich()){{};
return;
}}qx.ui.core.Widget.prototype._applySelectable.call(this,E);
},_getContentHeightForWidth:function(F){if(!this.getRich()&&!this.getWrap()){return null;
}return this.__kh(F).height;
},_createContentElement:function(){return new qx.html.Label;
},_applyTextAlign:function(G,H){this.getContentElement().setStyle(t,G);
},_applyTextColor:function(I,J){if(I){this.getContentElement().setStyle(i,qx.theme.manager.Color.getInstance().resolve(I));
}else{this.getContentElement().removeStyle(i);
}},__kg:{width:0,height:0},_applyFont:function(K,L){var M;

if(K){this.__kc=qx.theme.manager.Font.getInstance().resolve(K);
M=this.__kc.getStyles();
}else{this.__kc=null;
M=qx.bom.Font.getDefaultStyles();
}this.getContentElement().setStyles(M);
this.__kd=true;
qx.ui.core.queue.Layout.add(this);
},__kh:function(N){var R=qx.bom.Label;
var P=this.getFont();
var O=P?this.__kc.getStyles():qx.bom.Font.getDefaultStyles();
var content=this.getValue()||B;
var Q=this.getRich();
return Q?R.getHtmlSize(content,O,N):R.getTextSize(content,O);
},_applyBuddy:function(S,T){if(T!=null){T.removeBinding(this.__ke);
this.__ke=null;
this.removeListenerById(this.__kf);
this.__kf=null;
}
if(S!=null){this.__ke=S.bind(g,this,g);
this.__kf=this.addListener(n,function(){if(S.isFocusable()){S.focus.apply(S);
}},this);
}},_applyRich:function(U){this.getContentElement().setRich(U);
this.__kd=true;
qx.ui.core.queue.Layout.add(this);
},_applyWrap:function(V,W){if(V&&!this.isRich()){{};
}
if(this.isRich()){var X=V?p:b;
this.getContentElement().setStyle(y,X);
}},_onChangeLocale:qx.core.Variant.select(k,{"on":function(e){var content=this.getValue();

if(content&&content.translate){this.setValue(content.translate());
}},"off":null}),_applyValue:function(Y,ba){this.getContentElement().setValue(Y);
this.__kd=true;
qx.ui.core.queue.Layout.add(this);
this.fireDataEvent(A,Y,ba);
}},destruct:function(){if(qx.core.Variant.isSet(k,f)){qx.locale.Manager.getInstance().removeListener(h,this._onChangeLocale,this);
}if(this.__ke!=null){var bb=this.getBuddy();

if(bb!=null&&!bb.isDisposed()){bb.removeBinding(this.__ke);
}}this.__kc=this.__ke=null;
}});
})();
(function(){var b="value",a="qx.html.Label";
qx.Class.define(a,{extend:qx.html.Element,members:{__ki:null,_applyProperty:function(name,c){qx.html.Element.prototype._applyProperty.call(this,name,c);

if(name==b){var d=this.getDomElement();
qx.bom.Label.setValue(d,c);
}},_createDomElement:function(){var f=this.__ki;
var e=qx.bom.Label.create(this._content,f);
return e;
},_copyData:function(g){return qx.html.Element.prototype._copyData.call(this,true);
},setRich:function(h){var i=this.getDomElement();

if(i){throw new Error("The label mode cannot be modified after initial creation");
}h=!!h;

if(this.__ki==h){return;
}this.__ki=h;
return this;
},setValue:function(j){this._setProperty(b,j);
return this;
},getValue:function(){return this._getProperty(b);
}}});
})();
(function(){var j="div",i="inherit",h="text",g="qx.client",f="value",e="",d="hidden",c="http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul",b="nowrap",a="auto",z="0",y="ellipsis",x="normal",w="label",v="px",u="crop",t="gecko",s="end",r="100%",q="visible",o="qx.bom.Label",p="opera",m="mshtml",n="block",k="-1000px",l="absolute";
qx.Class.define(o,{statics:{__kj:{fontFamily:1,fontSize:1,fontWeight:1,fontStyle:1,lineHeight:1},__kk:function(){var A=this.__km(false);
document.body.insertBefore(A,document.body.firstChild);
return this._textElement=A;
},__kl:function(){var B=this.__km(true);
document.body.insertBefore(B,document.body.firstChild);
return this._htmlElement=B;
},__km:function(C){var D=qx.bom.Element.create(j);
var E=D.style;
E.width=E.height=a;
E.left=E.top=k;
E.visibility=d;
E.position=l;
E.overflow=q;

if(C){E.whiteSpace=x;
}else{E.whiteSpace=b;

if(!qx.bom.client.Feature.CSS_TEXT_OVERFLOW&&qx.bom.client.Feature.XUL){var F=document.createElementNS(c,w);
var E=F.style;
E.padding=z;

for(var G in this.__kj){E[G]=i;
}D.appendChild(F);
}}return D;
},__kn:function(H){var I={};

if(H){I.whiteSpace=x;
}else if(!qx.bom.client.Feature.CSS_TEXT_OVERFLOW&&qx.bom.client.Feature.XUL){I.display=n;
}else{I.overflow=d;
I.whiteSpace=b;
I.textOverflow=y;
if(qx.core.Variant.isSet(g,p)){I.OTextOverflow=y;
}}return I;
},create:function(content,J,K){if(!K){K=window;
}
if(J){var L=K.document.createElement(j);
L.useHtml=true;
}else if(!qx.bom.client.Feature.CSS_TEXT_OVERFLOW&&qx.bom.client.Feature.XUL){var L=K.document.createElement(j);
var N=K.document.createElementNS(c,w);
var M=N.style;
M.cursor=i;
M.color=i;
M.overflow=d;
M.maxWidth=r;
M.padding=z;
for(var O in this.__kj){N.style[O]=i;
}N.setAttribute(u,s);
L.appendChild(N);
}else{var L=K.document.createElement(j);
qx.bom.element.Style.setStyles(L,this.__kn(J));
}
if(content){this.setValue(L,content);
}return L;
},setValue:function(P,Q){Q=Q||e;

if(P.useHtml){P.innerHTML=Q;
}else if(!qx.bom.client.Feature.CSS_TEXT_OVERFLOW&&qx.bom.client.Feature.XUL){P.firstChild.setAttribute(f,Q);
}else{qx.bom.element.Attribute.set(P,h,Q);
}},getValue:function(R){if(R.useHtml){return R.innerHTML;
}else if(!qx.bom.client.Feature.CSS_TEXT_OVERFLOW&&qx.bom.client.Feature.XUL){return R.firstChild.getAttribute(f)||e;
}else{return qx.bom.element.Attribute.get(R,h);
}},getHtmlSize:function(content,S,T){var U=this._htmlElement||this.__kl();
U.style.width=T!==undefined?T+v:a;
U.innerHTML=content;
return this.__ko(U,S);
},getTextSize:function(V,W){var X=this._textElement||this.__kk();

if(!qx.bom.client.Feature.CSS_TEXT_OVERFLOW&&qx.bom.client.Feature.XUL){X.firstChild.setAttribute(f,V);
}else{qx.bom.element.Attribute.set(X,h,V);
}return this.__ko(X,W);
},__ko:function(Y,ba){var bb=this.__kj;

if(!ba){ba={};
}
for(var bc in bb){Y.style[bc]=ba[bc]||e;
}var bd=qx.bom.element.Dimension.getSize(Y);

if(qx.core.Variant.isSet(g,t)){if(!qx.bom.client.Platform.WIN){bd.width++;
}}if(qx.core.Variant.isSet(g,m)&&qx.bom.client.Engine.VERSION>=9){bd.width++;
}return bd;
}}});
})();
(function(){var i="0px",h="qx.client",g="mshtml",f="qx.bom.element.Dimension",e="paddingRight",d="paddingLeft",c="opera",b="paddingTop",a="paddingBottom";
qx.Class.define(f,{statics:{getWidth:qx.core.Variant.select(h,{"gecko":function(j){if(j.getBoundingClientRect){var k=j.getBoundingClientRect();
return Math.round(k.right)-Math.round(k.left);
}else{return j.offsetWidth;
}},"default":function(l){return l.offsetWidth;
}}),getHeight:qx.core.Variant.select(h,{"gecko":function(m){if(m.getBoundingClientRect){var n=m.getBoundingClientRect();
return Math.round(n.bottom)-Math.round(n.top);
}else{return m.offsetHeight;
}},"default":function(o){return o.offsetHeight;
}}),getSize:function(p){return {width:this.getWidth(p),height:this.getHeight(p)};
},__kp:{visible:true,hidden:true},getContentWidth:function(q){var s=qx.bom.element.Style;
var t=qx.bom.element.Overflow.getX(q);
var u=parseInt(s.get(q,d)||i,10);
var x=parseInt(s.get(q,e)||i,10);

if(this.__kp[t]){var w=q.clientWidth;

if(qx.core.Variant.isSet(h,c)){w=w-u-x;
}else{if(qx.dom.Node.isBlockNode(q)){w=w-u-x;
}}return w;
}else{if(q.clientWidth>=q.scrollWidth){return Math.max(q.clientWidth,q.scrollWidth)-u-x;
}else{var v=q.scrollWidth-u;
var r=qx.bom.client.Engine;

if(r.NAME===g&&r.VERSION==6){v-=x;
}return v;
}}},getContentHeight:function(y){var A=qx.bom.element.Style;
var C=qx.bom.element.Overflow.getY(y);
var D=parseInt(A.get(y,b)||i,10);
var B=parseInt(A.get(y,a)||i,10);

if(this.__kp[C]){return y.clientHeight-D-B;
}else{if(y.clientHeight>=y.scrollHeight){return Math.max(y.clientHeight,y.scrollHeight)-D-B;
}else{var E=y.scrollHeight-D;
var z=qx.bom.client.Engine;

if(z.NAME===g&&z.VERSION==6){E-=B;
}return E;
}}},getContentSize:function(F){return {width:this.getContentWidth(F),height:this.getContentHeight(F)};
}}});
})();
(function(){var b="qx.event.type.Data",a="qx.ui.form.IForm";
qx.Interface.define(a,{events:{"changeEnabled":b,"changeValid":b,"changeInvalidMessage":b,"changeRequired":b},members:{setEnabled:function(c){return arguments.length==1;
},getEnabled:function(){},setRequired:function(d){return arguments.length==1;
},getRequired:function(){},setValid:function(e){return arguments.length==1;
},getValid:function(){},setInvalidMessage:function(f){return arguments.length==1;
},getInvalidMessage:function(){},setRequiredInvalidMessage:function(g){return arguments.length==1;
},getRequiredInvalidMessage:function(){}}});
})();
(function(){var i="qx.ui.window.Window",h="changeModal",g="changeVisibility",f="changeActive",d="_applyActiveWindow",c="__kr",b="__kq",a="qx.ui.window.MDesktop";
qx.Mixin.define(a,{properties:{activeWindow:{check:i,apply:d,init:null,nullable:true}},members:{__kq:null,__kr:null,getWindowManager:function(){if(!this.__kr){this.setWindowManager(new qx.ui.window.Window.DEFAULT_MANAGER_CLASS());
}return this.__kr;
},supportsMaximize:function(){return true;
},setWindowManager:function(j){if(this.__kr){this.__kr.setDesktop(null);
}j.setDesktop(this);
this.__kr=j;
},_onChangeActive:function(e){if(e.getData()){this.setActiveWindow(e.getTarget());
}else if(this.getActiveWindow()==e.getTarget()){this.setActiveWindow(null);
}},_applyActiveWindow:function(k,l){this.getWindowManager().changeActiveWindow(k,l);
this.getWindowManager().updateStack();
},_onChangeModal:function(e){this.getWindowManager().updateStack();
},_onChangeVisibility:function(){this.getWindowManager().updateStack();
},_afterAddChild:function(m){if(qx.Class.isDefined(i)&&m instanceof qx.ui.window.Window){this._addWindow(m);
}},_addWindow:function(n){if(!qx.lang.Array.contains(this.getWindows(),n)){this.getWindows().push(n);
n.addListener(f,this._onChangeActive,this);
n.addListener(h,this._onChangeModal,this);
n.addListener(g,this._onChangeVisibility,this);
}
if(n.getActive()){this.setActiveWindow(n);
}this.getWindowManager().updateStack();
},_afterRemoveChild:function(o){if(qx.Class.isDefined(i)&&o instanceof qx.ui.window.Window){this._removeWindow(o);
}},_removeWindow:function(p){qx.lang.Array.remove(this.getWindows(),p);
p.removeListener(f,this._onChangeActive,this);
p.removeListener(h,this._onChangeModal,this);
p.removeListener(g,this._onChangeVisibility,this);
this.getWindowManager().updateStack();
},getWindows:function(){if(!this.__kq){this.__kq=[];
}return this.__kq;
}},destruct:function(){this._disposeArray(b);
this._disposeObjects(c);
}});
})();
(function(){var f="_applyBlockerColor",e="__ks",d="Number",c="qx.ui.core.MBlocker",b="_applyBlockerOpacity",a="Color";
qx.Mixin.define(c,{construct:function(){this.__ks=new qx.ui.core.Blocker(this);
},properties:{blockerColor:{check:a,init:null,nullable:true,apply:f,themeable:true},blockerOpacity:{check:d,init:1,apply:b,themeable:true}},members:{__ks:null,_applyBlockerColor:function(g,h){this.__ks.setColor(g);
},_applyBlockerOpacity:function(i,j){this.__ks.setOpacity(i);
},block:function(){this.__ks.block();
},isBlocked:function(){return this.__ks.isBlocked();
},unblock:function(){this.__ks.unblock();
},forceUnblock:function(){this.__ks.forceUnblock();
},blockContent:function(k){this.__ks.blockContent(k);
},isContentBlocked:function(){return this.__ks.isContentBlocked();
},unblockContent:function(){this.__ks.unblockContent();
},forceUnblockContent:function(){this.__ks.forceUnblockContent();
},getBlocker:function(){return this.__ks;
}},destruct:function(){this._disposeObjects(e);
}});
})();
(function(){var t="help",s="contextmenu",r="qx.client",q="changeGlobalCursor",p="keypress",o="Boolean",n="root",m="",l=" !important",k="input",d="_applyGlobalCursor",j="Space",h="_applyNativeHelp",c=";",b="qx.ui.root.Abstract",g="abstract",f="textarea",i="String",a="*";
qx.Class.define(b,{type:g,extend:qx.ui.core.Widget,include:[qx.ui.core.MChildrenHandling,qx.ui.core.MBlocker,qx.ui.window.MDesktop],construct:function(){qx.ui.core.Widget.call(this);
qx.ui.core.FocusHandler.getInstance().addRoot(this);
qx.ui.core.queue.Visibility.add(this);
this.initNativeHelp();
this.addListener(p,this.__tU,this);
},properties:{appearance:{refine:true,init:n},enabled:{refine:true,init:true},focusable:{refine:true,init:true},globalCursor:{check:i,nullable:true,themeable:true,apply:d,event:q},nativeContextMenu:{refine:true,init:false},nativeHelp:{check:o,init:false,apply:h}},members:{__kt:null,isRootWidget:function(){return true;
},getLayout:function(){return this._getLayout();
},_applyGlobalCursor:qx.core.Variant.select(r,{"mshtml":function(u,v){},"default":function(w,x){var y=qx.bom.Stylesheet;
var z=this.__kt;

if(!z){this.__kt=z=y.createElement();
}y.removeAllRules(z);

if(w){y.addRule(z,a,qx.bom.element.Cursor.compile(w).replace(c,m)+l);
}}}),_applyNativeContextMenu:function(A,B){if(A){this.removeListener(s,this._onNativeContextMenu,this,true);
}else{this.addListener(s,this._onNativeContextMenu,this,true);
}},_onNativeContextMenu:function(e){if(e.getTarget().getNativeContextMenu()){return;
}e.preventDefault();
},__tU:function(e){if(e.getKeyIdentifier()!==j){return;
}var D=e.getTarget();
var C=qx.ui.core.FocusHandler.getInstance();

if(!C.isFocused(D)){return;
}var E=D.getContentElement().getNodeName();

if(E===k||E===f){return;
}e.preventDefault();
},_applyNativeHelp:qx.core.Variant.select(r,{"mshtml":function(F,G){if(G===false){qx.bom.Event.removeNativeListener(document,t,qx.lang.Function.returnFalse);
}
if(F===false){qx.bom.Event.addNativeListener(document,t,qx.lang.Function.returnFalse);
}},"default":function(){}})},destruct:function(){this.__kt=null;
},defer:function(H,I){qx.ui.core.MChildrenHandling.remap(I);
}});
})();
(function(){var n="resize",m="position",l="0px",k="webkit",j="paddingLeft",i="$$widget",h="qx.ui.root.Application",g="hidden",f="qx.client",d="div",a="paddingTop",c="100%",b="absolute";
qx.Class.define(h,{extend:qx.ui.root.Abstract,construct:function(o){this.__ku=qx.dom.Node.getWindow(o);
this.__kv=o;
qx.ui.root.Abstract.call(this);
qx.event.Registration.addListener(this.__ku,n,this._onResize,this);
this._setLayout(new qx.ui.layout.Canvas());
qx.ui.core.queue.Layout.add(this);
qx.ui.core.FocusHandler.getInstance().connectTo(this);
this.getContentElement().disableScrolling();
},members:{__ku:null,__kv:null,_createContainerElement:function(){var p=this.__kv;
if(qx.core.Variant.isSet(f,k)){if(!p.body){alert("The application could not be started due to a missing body tag in the HTML file!");
}}var t=p.documentElement.style;
var q=p.body.style;
t.overflow=q.overflow=g;
t.padding=t.margin=q.padding=q.margin=l;
t.width=t.height=q.width=q.height=c;
var s=p.createElement(d);
p.body.appendChild(s);
var r=new qx.html.Root(s);
r.setStyle(m,b);
r.setAttribute(i,this.toHashCode());
return r;
},_onResize:function(e){qx.ui.core.queue.Layout.add(this);
},_computeSizeHint:function(){var u=qx.bom.Viewport.getWidth(this.__ku);
var v=qx.bom.Viewport.getHeight(this.__ku);
return {minWidth:u,width:u,maxWidth:u,minHeight:v,height:v,maxHeight:v};
},_applyPadding:function(w,x,name){if(w&&(name==a||name==j)){throw new Error("The root widget does not support 'left', or 'top' paddings!");
}qx.ui.root.Abstract.prototype._applyPadding.call(this,w,x,name);
},_applyDecorator:function(y,z){qx.ui.root.Abstract.prototype._applyDecorator.call(this,y,z);

if(!y){return;
}var A=this.getDecoratorElement().getInsets();

if(A.left||A.top){throw new Error("The root widget does not support decorators with 'left', or 'top' insets!");
}}},destruct:function(){this.__ku=this.__kv=null;
}});
})();
(function(){var l="zIndex",k="px",j="keydown",h="deactivate",g="resize",f="keyup",d="keypress",c="backgroundColor",b="_applyOpacity",a="Boolean",x="opacity",w="interval",v="Tab",u="Color",t="qx.ui.root.Page",s="__kD",r="__kB",q="Number",p="qx.ui.core.Blocker",o="qx.ui.root.Application",m="__kz",n="_applyColor";
qx.Class.define(p,{extend:qx.core.Object,construct:function(y){qx.core.Object.call(this);
this._widget=y;
this._isPageRoot=(qx.Class.isDefined(t)&&y instanceof qx.ui.root.Page);

if(this._isPageRoot){y.addListener(g,this.__kE,this);
}
if(qx.Class.isDefined(o)&&y instanceof qx.ui.root.Application){this.setKeepBlockerActive(true);
}this.__kw=[];
this.__kx=[];
this.__ky=[];
},properties:{color:{check:u,init:null,nullable:true,apply:n,themeable:true},opacity:{check:q,init:1,apply:b,themeable:true},keepBlockerActive:{check:a,init:false}},members:{__kz:null,__kA:0,__kB:null,__ky:null,__kw:null,__kx:null,__kC:null,__kD:null,_isPageRoot:false,_widget:null,__kE:function(e){var z=e.getData();

if(this.isContentBlocked()){this.getContentBlockerElement().setStyles({width:z.width,height:z.height});
}
if(this.isBlocked()){this.getBlockerElement().setStyles({width:z.width,height:z.height});
}},_applyColor:function(A,B){var C=qx.theme.manager.Color.getInstance().resolve(A);
this.__kF(c,C);
},_applyOpacity:function(D,E){this.__kF(x,D);
},__kF:function(F,G){var H=[];
this.__kz&&H.push(this.__kz);
this.__kB&&H.push(this.__kB);

for(var i=0;i<H.length;i++){H[i].setStyle(F,G);
}},_backupActiveWidget:function(){var I=qx.event.Registration.getManager(window).getHandler(qx.event.handler.Focus);
this.__kw.push(I.getActive());
this.__kx.push(I.getFocus());

if(this._widget.isFocusable()){this._widget.focus();
}},_restoreActiveWidget:function(){var L=this.__kw.length;

if(L>0){var K=this.__kw[L-1];

if(K){qx.bom.Element.activate(K);
}this.__kw.pop();
}var J=this.__kx.length;

if(J>0){var K=this.__kx[J-1];

if(K){qx.bom.Element.focus(this.__kx[J-1]);
}this.__kx.pop();
}},__kG:function(){return new qx.html.Blocker(this.getColor(),this.getOpacity());
},getBlockerElement:function(){if(!this.__kz){this.__kz=this.__kG();
this.__kz.setStyle(l,15);
this._widget.getContainerElement().add(this.__kz);
this.__kz.exclude();
}return this.__kz;
},block:function(){this.__kA++;

if(this.__kA<2){this._backupActiveWidget();
var M=this.getBlockerElement();
M.include();
M.activate();
M.addListener(h,this.__kL,this);
M.addListener(d,this.__kK,this);
M.addListener(j,this.__kK,this);
M.addListener(f,this.__kK,this);
}},isBlocked:function(){return this.__kA>0;
},unblock:function(){if(!this.isBlocked()){return;
}this.__kA--;

if(this.__kA<1){this.__kH();
this.__kA=0;
}},forceUnblock:function(){if(!this.isBlocked()){return;
}this.__kA=0;
this.__kH();
},__kH:function(){this._restoreActiveWidget();
var N=this.getBlockerElement();
N.removeListener(h,this.__kL,this);
N.removeListener(d,this.__kK,this);
N.removeListener(j,this.__kK,this);
N.removeListener(f,this.__kK,this);
N.exclude();
},getContentBlockerElement:function(){if(!this.__kB){this.__kB=this.__kG();
this._widget.getContentElement().add(this.__kB);
this.__kB.exclude();
}return this.__kB;
},blockContent:function(O){var P=this.getContentBlockerElement();
P.setStyle(l,O);
this.__ky.push(O);

if(this.__ky.length<2){P.include();

if(this._isPageRoot){if(!this.__kD){this.__kD=new qx.event.Timer(300);
this.__kD.addListener(w,this.__kJ,this);
}this.__kD.start();
this.__kJ();
}}},isContentBlocked:function(){return this.__ky.length>0;
},unblockContent:function(){if(!this.isContentBlocked()){return;
}this.__ky.pop();
var Q=this.__ky[this.__ky.length-1];
var R=this.getContentBlockerElement();
R.setStyle(l,Q);

if(this.__ky.length<1){this.__kI();
this.__ky=[];
}},forceUnblockContent:function(){if(!this.isContentBlocked()){return;
}this.__ky=[];
var S=this.getContentBlockerElement();
S.setStyle(l,null);
this.__kI();
},__kI:function(){this.getContentBlockerElement().exclude();

if(this._isPageRoot){this.__kD.stop();
}},__kJ:function(){var T=this._widget.getContainerElement().getDomElement();
var U=qx.dom.Node.getDocument(T);
this.getContentBlockerElement().setStyles({height:U.documentElement.scrollHeight+k,width:U.documentElement.scrollWidth+k});
},__kK:function(e){if(e.getKeyIdentifier()==v){e.stop();
}},__kL:function(){if(this.getKeepBlockerActive()){this.getBlockerElement().activate();
}}},destruct:function(){if(this._isPageRoot){this._widget.removeListener(g,this.__kE,this);
}this._disposeObjects(r,m,s);
this.__kC=this.__kw=this.__kx=this._widget=this.__ky=null;
}});
})();
(function(){var k="cursor",j="100%",i="repeat",h="mousedown",g="url(",f=")",d="mouseout",c="qx.client",b="div",a="dblclick",w="mousewheel",v="qx.html.Blocker",u="mousemove",t="mouseover",s="appear",r="click",q="mshtml",p="mouseup",o="contextmenu",n="disappear",l="qx/static/blank.gif",m="absolute";
qx.Class.define(v,{extend:qx.html.Element,construct:function(x,y){var x=x?qx.theme.manager.Color.getInstance().resolve(x):null;
var z={position:m,width:j,height:j,opacity:y||0,backgroundColor:x};
if(qx.core.Variant.isSet(c,q)){z.backgroundImage=g+qx.util.ResourceManager.getInstance().toUri(l)+f;
z.backgroundRepeat=i;
}qx.html.Element.call(this,b,z);
this.addListener(h,this._stopPropagation,this);
this.addListener(p,this._stopPropagation,this);
this.addListener(r,this._stopPropagation,this);
this.addListener(a,this._stopPropagation,this);
this.addListener(u,this._stopPropagation,this);
this.addListener(t,this._stopPropagation,this);
this.addListener(d,this._stopPropagation,this);
this.addListener(w,this._stopPropagation,this);
this.addListener(o,this._stopPropagation,this);
this.addListener(s,this.__kM,this);
this.addListener(n,this.__kM,this);
},members:{_stopPropagation:function(e){e.stopPropagation();
},__kM:function(){var A=this.getStyle(k);
this.setStyle(k,null,true);
this.setStyle(k,A,true);
}}});
})();
(function(){var k="keypress",j="__kN",h="focusout",g="activate",f="Tab",d="singleton",c="deactivate",b="focusin",a="qx.ui.core.FocusHandler";
qx.Class.define(a,{extend:qx.core.Object,type:d,construct:function(){qx.core.Object.call(this);
this.__kN={};
},members:{__kN:null,__kO:null,__kP:null,__kQ:null,connectTo:function(m){m.addListener(k,this.__kR,this);
m.addListener(b,this._onFocusIn,this,true);
m.addListener(h,this._onFocusOut,this,true);
m.addListener(g,this._onActivate,this,true);
m.addListener(c,this._onDeactivate,this,true);
},addRoot:function(n){this.__kN[n.$$hash]=n;
},removeRoot:function(o){delete this.__kN[o.$$hash];
},getActiveWidget:function(){return this.__kO;
},isActive:function(p){return this.__kO==p;
},getFocusedWidget:function(){return this.__kP;
},isFocused:function(q){return this.__kP==q;
},isFocusRoot:function(r){return !!this.__kN[r.$$hash];
},_onActivate:function(e){var t=e.getTarget();
this.__kO=t;
var s=this.__kS(t);

if(s!=this.__kQ){this.__kQ=s;
}},_onDeactivate:function(e){var u=e.getTarget();

if(this.__kO==u){this.__kO=null;
}},_onFocusIn:function(e){var v=e.getTarget();

if(v!=this.__kP){this.__kP=v;
v.visualizeFocus();
}},_onFocusOut:function(e){var w=e.getTarget();

if(w==this.__kP){this.__kP=null;
w.visualizeBlur();
}},__kR:function(e){if(e.getKeyIdentifier()!=f){return;
}
if(!this.__kQ){return;
}e.stopPropagation();
e.preventDefault();
var x=this.__kP;

if(!e.isShiftPressed()){var y=x?this.__kW(x):this.__kU();
}else{var y=x?this.__kX(x):this.__kV();
}if(y){y.tabFocus();
}},__kS:function(z){var A=this.__kN;

while(z){if(A[z.$$hash]){return z;
}z=z.getLayoutParent();
}return null;
},__kT:function(B,C){if(B===C){return 0;
}var E=B.getTabIndex()||0;
var D=C.getTabIndex()||0;

if(E!=D){return E-D;
}var J=B.getContainerElement().getDomElement();
var I=C.getContainerElement().getDomElement();
var H=qx.bom.element.Location;
var G=H.get(J);
var F=H.get(I);
if(G.top!=F.top){return G.top-F.top;
}if(G.left!=F.left){return G.left-F.left;
}var K=B.getZIndex();
var L=C.getZIndex();

if(K!=L){return K-L;
}return 0;
},__kU:function(){return this.__lb(this.__kQ,null);
},__kV:function(){return this.__lc(this.__kQ,null);
},__kW:function(M){var N=this.__kQ;

if(N==M){return this.__kU();
}
while(M&&M.getAnonymous()){M=M.getLayoutParent();
}
if(M==null){return [];
}var O=[];
this.__kY(N,M,O);
O.sort(this.__kT);
var P=O.length;
return P>0?O[0]:this.__kU();
},__kX:function(Q){var R=this.__kQ;

if(R==Q){return this.__kV();
}
while(Q&&Q.getAnonymous()){Q=Q.getLayoutParent();
}
if(Q==null){return [];
}var S=[];
this.__la(R,Q,S);
S.sort(this.__kT);
var T=S.length;
return T>0?S[T-1]:this.__kV();
},__kY:function(parent,U,V){var W=parent.getLayoutChildren();
var X;

for(var i=0,l=W.length;i<l;i++){X=W[i];
if(!(X instanceof qx.ui.core.Widget)){continue;
}
if(!this.isFocusRoot(X)&&X.isEnabled()&&X.isVisible()){if(X.isTabable()&&this.__kT(U,X)<0){V.push(X);
}this.__kY(X,U,V);
}}},__la:function(parent,Y,ba){var bb=parent.getLayoutChildren();
var bc;

for(var i=0,l=bb.length;i<l;i++){bc=bb[i];
if(!(bc instanceof qx.ui.core.Widget)){continue;
}
if(!this.isFocusRoot(bc)&&bc.isEnabled()&&bc.isVisible()){if(bc.isTabable()&&this.__kT(Y,bc)>0){ba.push(bc);
}this.__la(bc,Y,ba);
}}},__lb:function(parent,bd){var be=parent.getLayoutChildren();
var bf;

for(var i=0,l=be.length;i<l;i++){bf=be[i];
if(!(bf instanceof qx.ui.core.Widget)){continue;
}if(!this.isFocusRoot(bf)&&bf.isEnabled()&&bf.isVisible()){if(bf.isTabable()){if(bd==null||this.__kT(bf,bd)<0){bd=bf;
}}bd=this.__lb(bf,bd);
}}return bd;
},__lc:function(parent,bg){var bh=parent.getLayoutChildren();
var bi;

for(var i=0,l=bh.length;i<l;i++){bi=bh[i];
if(!(bi instanceof qx.ui.core.Widget)){continue;
}if(!this.isFocusRoot(bi)&&bi.isEnabled()&&bi.isVisible()){if(bi.isTabable()){if(bg==null||this.__kT(bi,bg)>0){bg=bi;
}}bg=this.__lc(bi,bg);
}}return bg;
}},destruct:function(){this._disposeMap(j);
this.__kP=this.__kO=this.__kQ=null;
}});
})();
(function(){var l="qx.client",k="head",j="text/css",h="stylesheet",g="}",f='@import "',e="{",d='";',c="qx.bom.Stylesheet",b="link",a="style";
qx.Class.define(c,{statics:{includeFile:function(m,n){if(!n){n=document;
}var o=n.createElement(b);
o.type=j;
o.rel=h;
o.href=qx.util.ResourceManager.getInstance().toUri(m);
var p=n.getElementsByTagName(k)[0];
p.appendChild(o);
},createElement:qx.core.Variant.select(l,{"mshtml":function(q){var r=document.createStyleSheet();

if(q){r.cssText=q;
}return r;
},"default":function(s){var t=document.createElement(a);
t.type=j;

if(s){t.appendChild(document.createTextNode(s));
}document.getElementsByTagName(k)[0].appendChild(t);
return t.sheet;
}}),addRule:qx.core.Variant.select(l,{"mshtml":function(u,v,w){u.addRule(v,w);
},"default":function(x,y,z){x.insertRule(y+e+z+g,x.cssRules.length);
}}),removeRule:qx.core.Variant.select(l,{"mshtml":function(A,B){var C=A.rules;
var D=C.length;

for(var i=D-1;i>=0;--i){if(C[i].selectorText==B){A.removeRule(i);
}}},"default":function(E,F){var G=E.cssRules;
var H=G.length;

for(var i=H-1;i>=0;--i){if(G[i].selectorText==F){E.deleteRule(i);
}}}}),removeAllRules:qx.core.Variant.select(l,{"mshtml":function(I){var J=I.rules;
var K=J.length;

for(var i=K-1;i>=0;i--){I.removeRule(i);
}},"default":function(L){var M=L.cssRules;
var N=M.length;

for(var i=N-1;i>=0;i--){L.deleteRule(i);
}}}),addImport:qx.core.Variant.select(l,{"mshtml":function(O,P){O.addImport(P);
},"default":function(Q,R){Q.insertRule(f+R+d,Q.cssRules.length);
}}),removeImport:qx.core.Variant.select(l,{"mshtml":function(S,T){var U=S.imports;
var V=U.length;

for(var i=V-1;i>=0;i--){if(U[i].href==T){S.removeImport(i);
}}},"default":function(W,X){var Y=W.cssRules;
var ba=Y.length;

for(var i=ba-1;i>=0;i--){if(Y[i].href==X){W.deleteRule(i);
}}}}),removeAllImports:qx.core.Variant.select(l,{"mshtml":function(bb){var bc=bb.imports;
var bd=bc.length;

for(var i=bd-1;i>=0;i--){bb.removeImport(i);
}},"default":function(be){var bf=be.cssRules;
var bg=bf.length;

for(var i=bg-1;i>=0;i--){if(bf[i].type==bf[i].IMPORT_RULE){be.deleteRule(i);
}}}})}});
})();
(function(){var b="number",a="qx.ui.layout.Canvas";
qx.Class.define(a,{extend:qx.ui.layout.Abstract,members:{verifyLayoutProperty:null,renderLayout:function(c,d){var q=this._getLayoutChildren();
var g,p,n;
var s,top,e,f,j,h;
var o,m,r,k;

for(var i=0,l=q.length;i<l;i++){g=q[i];
p=g.getSizeHint();
n=g.getLayoutProperties();
o=g.getMarginTop();
m=g.getMarginRight();
r=g.getMarginBottom();
k=g.getMarginLeft();
s=n.left!=null?n.left:n.edge;

if(qx.lang.Type.isString(s)){s=Math.round(parseFloat(s)*c/100);
}e=n.right!=null?n.right:n.edge;

if(qx.lang.Type.isString(e)){e=Math.round(parseFloat(e)*c/100);
}top=n.top!=null?n.top:n.edge;

if(qx.lang.Type.isString(top)){top=Math.round(parseFloat(top)*d/100);
}f=n.bottom!=null?n.bottom:n.edge;

if(qx.lang.Type.isString(f)){f=Math.round(parseFloat(f)*d/100);
}if(s!=null&&e!=null){j=c-s-e-k-m;
if(j<p.minWidth){j=p.minWidth;
}else if(j>p.maxWidth){j=p.maxWidth;
}s+=k;
}else{j=n.width;

if(j==null){j=p.width;
}else{j=Math.round(parseFloat(j)*c/100);
if(j<p.minWidth){j=p.minWidth;
}else if(j>p.maxWidth){j=p.maxWidth;
}}
if(e!=null){s=c-j-e-m-k;
}else if(s==null){s=k;
}else{s+=k;
}}if(top!=null&&f!=null){h=d-top-f-o-r;
if(h<p.minHeight){h=p.minHeight;
}else if(h>p.maxHeight){h=p.maxHeight;
}top+=o;
}else{h=n.height;

if(h==null){h=p.height;
}else{h=Math.round(parseFloat(h)*d/100);
if(h<p.minHeight){h=p.minHeight;
}else if(h>p.maxHeight){h=p.maxHeight;
}}
if(f!=null){top=d-h-f-r-o;
}else if(top==null){top=o;
}else{top+=o;
}}g.renderLayout(s,top,j,h);
}},_computeSizeHint:function(){var I=0,H=0;
var F=0,D=0;
var B,A;
var z,x;
var t=this._getLayoutChildren();
var w,G,v;
var J,top,u,y;

for(var i=0,l=t.length;i<l;i++){w=t[i];
G=w.getLayoutProperties();
v=w.getSizeHint();
var E=w.getMarginLeft()+w.getMarginRight();
var C=w.getMarginTop()+w.getMarginBottom();
B=v.width+E;
A=v.minWidth+E;
J=G.left!=null?G.left:G.edge;

if(J&&typeof J===b){B+=J;
A+=J;
}u=G.right!=null?G.right:G.edge;

if(u&&typeof u===b){B+=u;
A+=u;
}I=Math.max(I,B);
H=Math.max(H,A);
z=v.height+C;
x=v.minHeight+C;
top=G.top!=null?G.top:G.edge;

if(top&&typeof top===b){z+=top;
x+=top;
}y=G.bottom!=null?G.bottom:G.edge;

if(y&&typeof y===b){z+=y;
x+=y;
}F=Math.max(F,z);
D=Math.max(D,x);
}return {width:I,minWidth:H,height:F,minHeight:D};
}}});
})();
(function(){var f="off",d="selectstart",c="qx.html.Root",b="chrome",a="qxSelectable";
qx.Class.define(c,{extend:qx.html.Element,construct:function(g){qx.html.Element.call(this);

if(g!=null){this.useElement(g);
}
if(qx.bom.client.Browser.NAME===b){this.addListener(d,this.__tV);
}},members:{useElement:function(h){qx.html.Element.prototype.useElement.call(this,h);
this.setRoot(true);
qx.html.Element._modified[this.$$hash]=this;
},__tV:function(e){var i=e.getTarget();
if(i&&i.nodeType===3){i=i.parentNode;
}
if(i){if(i.getAttribute(a)===f){e.preventDefault();
}}}}});
})();
(function(){var w="visible",v="excluded",u="resize",t="qx.event.type.Data",s="both",r="qx.ui.menu.Menu",q="_applySpacing",p="showItem",o="Boolean",n="icon",d="label",m="qx.ui.core.Widget",h="_applyOverflowIndicator",c="_applyOverflowHandling",b="changeShow",g="Integer",f="qx.ui.toolbar.ToolBar",j="hideItem",a="toolbar",k="changeOpenMenu";
qx.Class.define(f,{extend:qx.ui.core.Widget,include:qx.ui.core.MChildrenHandling,construct:function(){qx.ui.core.Widget.call(this);
this._setLayout(new qx.ui.layout.HBox());
this.__qr=[];
this.__qs=[];
},properties:{appearance:{refine:true,init:a},openMenu:{check:r,event:k,nullable:true},show:{init:s,check:[s,d,n],inheritable:true,event:b},spacing:{nullable:true,check:g,themeable:true,apply:q},overflowIndicator:{check:m,nullable:true,apply:h},overflowHandling:{init:false,check:o,apply:c}},events:{"hideItem":t,"showItem":t},members:{__qr:null,__qs:null,_computeSizeHint:function(){var z=qx.ui.core.Widget.prototype._computeSizeHint.call(this);

if(true&&this.getOverflowHandling()){var x=0;
var y=this.getOverflowIndicator();

if(y){x=y.getSizeHint().width+this.getSpacing();
}z.minWidth=x;
}return z;
},_onResize:function(e){this._recalculateOverflow(e.getData().width);
},_recalculateOverflow:function(A,B){if(!this.getOverflowHandling()){return;
}B=B||this.getSizeHint().width;
var C=this.getOverflowIndicator();
var I=0;

if(C){I=C.getSizeHint().width;
}
if(A==undefined&&this.getBounds()!=null){A=this.getBounds().width;
}if(A==undefined){return ;
}if(A<B){do{var J=this._getNextToHide();
if(!J){return;
}var L=J.getMarginLeft()+J.getMarginRight();
L=Math.max(L,this.getSpacing());
var G=J.getSizeHint().width+L;
this.__qu(J);
B-=G;
if(C&&C.getVisibility()!=w){C.setVisibility(w);
B+=I;
var E=C.getMarginLeft()+C.getMarginRight();
B+=Math.max(E,this.getSpacing());
}}while(B>A);
}else if(this.__qr.length>0){do{var M=this.__qr[0];
if(M){var L=M.getMarginLeft()+M.getMarginRight();
L=Math.max(L,this.getSpacing());
if(M.getDecoratorElement()==null){M.syncAppearance();
M.invalidateLayoutCache();
}var F=M.getSizeHint().width;
var K=false;
if(this.__qr.length==1&&I>0){var D=L-this.getSpacing();
var H=B-I+F+D;
K=A>H;
}if(A>B+F+L||K){this.__qt(M);
B+=F;
if(C&&this.__qr.length==0){C.setVisibility(v);
}}else{return;
}}}while(A>=B&&this.__qr.length>0);
}},__qt:function(N){N.setVisibility(w);
this.__qr.shift();
this.fireDataEvent(p,N);
},__qu:function(O){if(!O){return;
}this.__qr.unshift(O);
O.setVisibility(v);
this.fireDataEvent(j,O);
},_getNextToHide:function(){for(var i=this.__qs.length-1;i>=0;i--){var P=this.__qs[i];
if(P&&P.getVisibility&&P.getVisibility()==w){return P;
}}var Q=this._getChildren();

for(var i=Q.length-1;i>=0;i--){var R=Q[i];
if(R==this.getOverflowIndicator()){continue;
}if(R.getVisibility&&R.getVisibility()==w){return R;
}}},setRemovePriority:function(S,T,U){if(!U&&this.__qs[T]!=undefined){throw new Error("Priority already in use!");
}this.__qs[T]=S;
},_applyOverflowHandling:function(V,W){this.invalidateLayoutCache();
var parent=this.getLayoutParent();

if(parent){parent.invalidateLayoutCache();
}var Y=this.getBounds();

if(Y&&Y.width){this._recalculateOverflow(Y.width);
}if(V){this.addListener(u,this._onResize,this);
}else{this.removeListener(u,this._onResize,this);
var X=this.getOverflowIndicator();

if(X){X.setVisibility(v);
}for(var i=0;i<this.__qr.length;i++){this.__qr[i].setVisibility(w);
}this.__qr=[];
}},_applyOverflowIndicator:function(ba,bb){if(bb){this._remove(bb);
}
if(ba){if(this._indexOf(ba)==-1){throw new Error("Widget must be child of the toolbar.");
}ba.setVisibility(v);
}},__qv:false,_setAllowMenuOpenHover:function(bc){this.__qv=bc;
},_isAllowMenuOpenHover:function(){return this.__qv;
},_applySpacing:function(bd,be){var bf=this._getLayout();
bd==null?bf.resetSpacing():bf.setSpacing(bd);
},_add:function(bg,bh){qx.ui.core.Widget.prototype._add.call(this,bg,bh);
var bi=this.getSizeHint().width+bg.getSizeHint().width+2*this.getSpacing();
this._recalculateOverflow(null,bi);
},_addAt:function(bj,bk,bl){qx.ui.core.Widget.prototype._addAt.call(this,bj,bk,bl);
var bm=this.getSizeHint().width+bj.getSizeHint().width+2*this.getSpacing();
this._recalculateOverflow(null,bm);
},_addBefore:function(bn,bo,bp){qx.ui.core.Widget.prototype._addBefore.call(this,bn,bo,bp);
var bq=this.getSizeHint().width+bn.getSizeHint().width+2*this.getSpacing();
this._recalculateOverflow(null,bq);
},_addAfter:function(br,bs,bt){qx.ui.core.Widget.prototype._addAfter.call(this,br,bs,bt);
var bu=this.getSizeHint().width+br.getSizeHint().width+2*this.getSpacing();
this._recalculateOverflow(null,bu);
},_remove:function(bv){qx.ui.core.Widget.prototype._remove.call(this,bv);
var bw=this.getSizeHint().width-bv.getSizeHint().width-2*this.getSpacing();
this._recalculateOverflow(null,bw);
},_removeAt:function(bx){var bz=this._getChildren()[bx];
qx.ui.core.Widget.prototype._removeAt.call(this,bx);
var by=this.getSizeHint().width-bz.getSizeHint().width-2*this.getSpacing();
this._recalculateOverflow(null,by);
},_removeAll:function(){qx.ui.core.Widget.prototype._removeAll.call(this);
this._recalculateOverflow(null,0);
},addSpacer:function(){var bA=new qx.ui.core.Spacer;
this._add(bA,{flex:1});
return bA;
},addSeparator:function(){this.add(new qx.ui.toolbar.Separator);
},getMenuButtons:function(){var bC=this.getChildren();
var bB=[];
var bD;

for(var i=0,l=bC.length;i<l;i++){bD=bC[i];

if(bD instanceof qx.ui.menubar.Button){bB.push(bD);
}else if(bD instanceof qx.ui.toolbar.Part){bB.push.apply(bB,bD.getMenuButtons());
}}return bB;
}},destruct:function(){if(this.hasListener(u)){this.removeListener(u,this._onResize,this);
}}});
})();
(function(){var n="_applyLayoutChange",m="left",k="center",j="top",h="Decorator",g="middle",f="_applyReversed",e="bottom",d="Boolean",c="right",a="Integer",b="qx.ui.layout.HBox";
qx.Class.define(b,{extend:qx.ui.layout.Abstract,construct:function(o,p,q){qx.ui.layout.Abstract.call(this);

if(o){this.setSpacing(o);
}
if(p){this.setAlignX(p);
}
if(q){this.setSeparator(q);
}},properties:{alignX:{check:[m,k,c],init:m,apply:n},alignY:{check:[j,g,e],init:j,apply:n},spacing:{check:a,init:0,apply:n},separator:{check:h,nullable:true,apply:n},reversed:{check:d,init:false,apply:f}},members:{__oh:null,__oi:null,__oj:null,__ok:null,_applyReversed:function(){this._invalidChildrenCache=true;
this._applyLayoutChange();
},__ol:function(){var w=this._getLayoutChildren();
var length=w.length;
var t=false;
var r=this.__oh&&this.__oh.length!=length&&this.__oi&&this.__oh;
var u;
var s=r?this.__oh:new Array(length);
var v=r?this.__oi:new Array(length);
if(this.getReversed()){w=w.concat().reverse();
}for(var i=0;i<length;i++){u=w[i].getLayoutProperties();

if(u.width!=null){s[i]=parseFloat(u.width)/100;
}
if(u.flex!=null){v[i]=u.flex;
t=true;
}else{v[i]=0;
}}if(!r){this.__oh=s;
this.__oi=v;
}this.__oj=t;
this.__ok=w;
delete this._invalidChildrenCache;
},verifyLayoutProperty:null,renderLayout:function(x,y){if(this._invalidChildrenCache){this.__ol();
}var E=this.__ok;
var length=E.length;
var N=qx.ui.layout.Util;
var M=this.getSpacing();
var Q=this.getSeparator();

if(Q){var B=N.computeHorizontalSeparatorGaps(E,M,Q);
}else{var B=N.computeHorizontalGaps(E,M,true);
}var i,z,K,J;
var P=[];
var F=B;

for(i=0;i<length;i+=1){J=this.__oh[i];
K=J!=null?Math.floor((x-B)*J):E[i].getSizeHint().width;
P.push(K);
F+=K;
}if(this.__oj&&F!=x){var H={};
var L,O;

for(i=0;i<length;i+=1){L=this.__oi[i];

if(L>0){G=E[i].getSizeHint();
H[i]={min:G.minWidth,value:P[i],max:G.maxWidth,flex:L};
}}var C=N.computeFlexOffsets(H,x,F);

for(i in C){O=C[i].offset;
P[i]+=O;
F+=O;
}}var U=E[0].getMarginLeft();
if(F<x&&this.getAlignX()!=m){U=x-F;

if(this.getAlignX()===k){U=Math.round(U/2);
}}var G,top,A,K,D,S,I;
var M=this.getSpacing();
this._clearSeparators();
if(Q){var R=qx.theme.manager.Decoration.getInstance().resolve(Q).getInsets();
var T=R.left+R.right;
}for(i=0;i<length;i+=1){z=E[i];
K=P[i];
G=z.getSizeHint();
S=z.getMarginTop();
I=z.getMarginBottom();
A=Math.max(G.minHeight,Math.min(y-S-I,G.maxHeight));
top=N.computeVerticalAlignOffset(z.getAlignY()||this.getAlignY(),A,y,S,I);
if(i>0){if(Q){U+=D+M;
this._renderSeparator(Q,{left:U,top:0,width:T,height:y});
U+=T+M+z.getMarginLeft();
}else{U+=N.collapseMargins(M,D,z.getMarginLeft());
}}z.renderLayout(U,top,K,A);
U+=K;
D=z.getMarginRight();
}},_computeSizeHint:function(){if(this._invalidChildrenCache){this.__ol();
}var bc=qx.ui.layout.Util;
var bk=this.__ok;
var V=0,bd=0,ba=0;
var Y=0,bb=0;
var bh,W,bj;
for(var i=0,l=bk.length;i<l;i+=1){bh=bk[i];
W=bh.getSizeHint();
bd+=W.width;
var bg=this.__oi[i];
var X=this.__oh[i];

if(bg){V+=W.minWidth;
}else if(X){ba=Math.max(ba,Math.round(W.minWidth/X));
}else{V+=W.width;
}bj=bh.getMarginTop()+bh.getMarginBottom();
if((W.height+bj)>bb){bb=W.height+bj;
}if((W.minHeight+bj)>Y){Y=W.minHeight+bj;
}}V+=ba;
var bf=this.getSpacing();
var bi=this.getSeparator();

if(bi){var be=bc.computeHorizontalSeparatorGaps(bk,bf,bi);
}else{var be=bc.computeHorizontalGaps(bk,bf,true);
}return {minWidth:V+be,width:bd+be,minHeight:Y,height:bb};
}},destruct:function(){this.__oh=this.__oi=this.__ok=null;
}});
})();
(function(){var a="qx.ui.core.Spacer";
qx.Class.define(a,{extend:qx.ui.core.LayoutItem,construct:function(b,c){qx.ui.core.LayoutItem.call(this);
this.setWidth(b!=null?b:0);
this.setHeight(c!=null?c:0);
},members:{checkAppearanceNeeds:function(){},addChildrenToQueue:function(d){},destroy:function(){if(this.$$disposed){return;
}var parent=this.$$parent;

if(parent){parent._remove(this);
}qx.ui.core.queue.Dispose.add(this);
}}});
})();
(function(){var b="toolbar-separator",a="qx.ui.toolbar.Separator";
qx.Class.define(a,{extend:qx.ui.core.Widget,properties:{appearance:{refine:true,init:b},anonymous:{refine:true,init:true},width:{refine:true,init:0},height:{refine:true,init:0}}});
})();
(function(){var b="qx.ui.form.IExecutable",a="qx.event.type.Data";
qx.Interface.define(b,{events:{"execute":a},members:{setCommand:function(c){return arguments.length==1;
},getCommand:function(){},execute:function(){}}});
})();
(function(){var n="execute",m="toolTipText",l="icon",k="label",j="qx.ui.core.MExecutable",h="value",g="qx.event.type.Event",f="_applyCommand",d="enabled",c="menu",a="changeCommand",b="qx.ui.core.Command";
qx.Mixin.define(j,{events:{"execute":g},properties:{command:{check:b,apply:f,event:a,nullable:true}},members:{__ld:null,__le:false,__lf:null,_bindableProperties:[d,k,l,m,h,c],execute:function(){var o=this.getCommand();

if(o){if(this.__le){this.__le=false;
}else{this.__le=true;
o.execute(this);
}}this.fireEvent(n);
},__lg:function(e){if(this.__le){this.__le=false;
return;
}this.__le=true;
this.execute();
},_applyCommand:function(p,q){if(q!=null){q.removeListenerById(this.__lf);
}
if(p!=null){this.__lf=p.addListener(n,this.__lg,this);
}var t=this.__ld;

if(t==null){this.__ld=t={};
}var u;

for(var i=0;i<this._bindableProperties.length;i++){var s=this._bindableProperties[i];
if(q!=null&&!q.isDisposed()&&t[s]!=null){q.removeBinding(t[s]);
t[s]=null;
}if(p!=null&&qx.Class.hasProperty(this.constructor,s)){var r=p.get(s);

if(r==null){u=this.get(s);
}else{u=null;
}t[s]=p.bind(s,this,s);
if(u){this.set(s,u);
}}}}},destruct:function(){this.setCommand(null);
this.__ld=null;
}});
})();
(function(){var o="pressed",n="abandoned",m="hovered",l="Enter",k="Space",j="dblclick",i="qx.ui.form.Button",h="mouseup",g="mousedown",f="mouseover",b="mouseout",d="keydown",c="button",a="keyup";
qx.Class.define(i,{extend:qx.ui.basic.Atom,include:[qx.ui.core.MExecutable],implement:[qx.ui.form.IExecutable],construct:function(p,q,r){qx.ui.basic.Atom.call(this,p,q);

if(r!=null){this.setCommand(r);
}this.addListener(f,this._onMouseOver);
this.addListener(b,this._onMouseOut);
this.addListener(g,this._onMouseDown);
this.addListener(h,this._onMouseUp);
this.addListener(d,this._onKeyDown);
this.addListener(a,this._onKeyUp);
this.addListener(j,this._onStopEvent);
},properties:{appearance:{refine:true,init:c},focusable:{refine:true,init:true}},members:{_forwardStates:{focused:true,hovered:true,pressed:true,disabled:true},press:function(){if(this.hasState(n)){return;
}this.addState(o);
},release:function(){if(this.hasState(o)){this.removeState(o);
}},reset:function(){this.removeState(o);
this.removeState(n);
this.removeState(m);
},_onMouseOver:function(e){if(!this.isEnabled()||e.getTarget()!==this){return;
}
if(this.hasState(n)){this.removeState(n);
this.addState(o);
}this.addState(m);
},_onMouseOut:function(e){if(!this.isEnabled()||e.getTarget()!==this){return;
}this.removeState(m);

if(this.hasState(o)){this.removeState(o);
this.addState(n);
}},_onMouseDown:function(e){if(!e.isLeftPressed()){return;
}e.stopPropagation();
this.capture();
this.removeState(n);
this.addState(o);
},_onMouseUp:function(e){this.releaseCapture();
var s=this.hasState(o);
var t=this.hasState(n);

if(s){this.removeState(o);
}
if(t){this.removeState(n);
}else{this.addState(m);

if(s){this.execute();
}}e.stopPropagation();
},_onKeyDown:function(e){switch(e.getKeyIdentifier()){case l:case k:this.removeState(n);
this.addState(o);
e.stopPropagation();
}},_onKeyUp:function(e){switch(e.getKeyIdentifier()){case l:case k:if(this.hasState(o)){this.removeState(n);
this.removeState(o);
this.execute();
e.stopPropagation();
}}}}});
})();
(function(){var l="pressed",k="hovered",j="changeVisibility",i="qx.ui.menu.Menu",h="submenu",g="Enter",f="contextmenu",d="changeMenu",c="qx.ui.form.MenuButton",b="abandoned",a="_applyMenu";
qx.Class.define(c,{extend:qx.ui.form.Button,construct:function(m,n,o){qx.ui.form.Button.call(this,m,n);
if(o!=null){this.setMenu(o);
}},properties:{menu:{check:i,nullable:true,apply:a,event:d}},members:{_applyMenu:function(p,q){if(q){q.removeListener(j,this._onMenuChange,this);
q.resetOpener();
}
if(p){p.addListener(j,this._onMenuChange,this);
p.setOpener(this);
p.removeState(h);
p.removeState(f);
}},open:function(r){var s=this.getMenu();

if(s){qx.ui.menu.Manager.getInstance().hideAll();
s.setOpener(this);
s.open();
if(r){var t=s.getSelectables()[0];

if(t){s.setSelectedButton(t);
}}}},_onMenuChange:function(e){var u=this.getMenu();

if(u.isVisible()){this.addState(l);
}else{this.removeState(l);
}},_onMouseDown:function(e){qx.ui.form.Button.prototype._onMouseDown.call(this,e);
var v=this.getMenu();

if(v){if(!v.isVisible()){this.open();
}else{v.exclude();
}e.stopPropagation();
}},_onMouseUp:function(e){qx.ui.form.Button.prototype._onMouseUp.call(this,e);
e.stopPropagation();
},_onMouseOver:function(e){this.addState(k);
},_onMouseOut:function(e){this.removeState(k);
},_onKeyDown:function(e){switch(e.getKeyIdentifier()){case g:this.removeState(b);
this.addState(l);
var w=this.getMenu();

if(w){if(!w.isVisible()){this.open();
}else{w.exclude();
}}e.stopPropagation();
}},_onKeyUp:function(e){}},destruct:function(){if(this.getMenu()){if(!qx.core.ObjectRegistry.inShutDown){this.getMenu().destroy();
}}}});
})();
(function(){var h="pressed",g="hovered",f="inherit",d="qx.ui.menubar.Button",c="keydown",b="menubar-button",a="keyup";
qx.Class.define(d,{extend:qx.ui.form.MenuButton,construct:function(i,j,k){qx.ui.form.MenuButton.call(this,i,j,k);
this.removeListener(c,this._onKeyDown);
this.removeListener(a,this._onKeyUp);
},properties:{appearance:{refine:true,init:b},show:{refine:true,init:f},focusable:{refine:true,init:false}},members:{getMenuBar:function(){var parent=this;

while(parent){if(parent instanceof qx.ui.toolbar.ToolBar){return parent;
}parent=parent.getLayoutParent();
}return null;
},open:function(l){qx.ui.form.MenuButton.prototype.open.call(this,l);
var menubar=this.getMenuBar();
menubar._setAllowMenuOpenHover(true);
},_onMenuChange:function(e){var m=this.getMenu();
var menubar=this.getMenuBar();

if(m.isVisible()){this.addState(h);
if(menubar){menubar.setOpenMenu(m);
}}else{this.removeState(h);
if(menubar&&menubar.getOpenMenu()==m){menubar.resetOpenMenu();
menubar._setAllowMenuOpenHover(false);
}}},_onMouseUp:function(e){qx.ui.form.MenuButton.prototype._onMouseUp.call(this,e);
var n=this.getMenu();

if(n&&n.isVisible()&&!this.hasState(h)){this.addState(h);
}},_onMouseOver:function(e){this.addState(g);
if(this.getMenu()){var menubar=this.getMenuBar();

if(menubar._isAllowMenuOpenHover()){qx.ui.menu.Manager.getInstance().hideAll();
menubar._setAllowMenuOpenHover(true);
if(this.isEnabled()){this.open();
}}}}}});
})();
(function(){var t="keypress",s="interval",r="keydown",q="mousedown",p="keyup",o="__qe",n="blur",m="Enter",l="__qc",k="__qd",c="Up",j="Escape",g="qx.ui.menu.Manager",b="Left",a="Down",f="Right",d="singleton",h="Space";
qx.Class.define(g,{type:d,extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__qc=[];
var u=document.body;
var v=qx.event.Registration;
v.addListener(window.document.documentElement,q,this._onMouseDown,this,true);
v.addListener(u,r,this._onKeyUpDown,this,true);
v.addListener(u,p,this._onKeyUpDown,this,true);
v.addListener(u,t,this._onKeyPress,this,true);
if(!qx.bom.client.Feature.TOUCH){qx.bom.Element.addListener(window,n,this.hideAll,this);
}this.__qd=new qx.event.Timer;
this.__qd.addListener(s,this._onOpenInterval,this);
this.__qe=new qx.event.Timer;
this.__qe.addListener(s,this._onCloseInterval,this);
},members:{__qf:null,__qg:null,__qd:null,__qe:null,__qc:null,_getChild:function(w,x,y,z){var A=w.getChildren();
var length=A.length;
var B;

for(var i=x;i<length&&i>=0;i+=y){B=A[i];

if(B.isEnabled()&&!B.isAnonymous()){return B;
}}
if(z){i=i==length?0:length-1;

for(;i!=x;i+=y){B=A[i];

if(B.isEnabled()&&!B.isAnonymous()){return B;
}}}return null;
},_isInMenu:function(C){while(C){if(C instanceof qx.ui.menu.Menu){return true;
}C=C.getLayoutParent();
}return false;
},_getMenuButton:function(D){while(D){if(D instanceof qx.ui.menu.AbstractButton){return D;
}D=D.getLayoutParent();
}return null;
},add:function(E){{};
var F=this.__qc;
F.push(E);
E.setZIndex(1e6+F.length);
},remove:function(G){{};
var H=this.__qc;

if(H){qx.lang.Array.remove(H,G);
}},hideAll:function(){var I=this.__qc;

if(I){for(var i=I.length-1;i>=0;i--){I[i].exclude();
}}},getActiveMenu:function(){var J=this.__qc;
return J.length>0?J[J.length-1]:null;
},scheduleOpen:function(K){this.cancelClose(K);
if(K.isVisible()){if(this.__qf){this.cancelOpen(this.__qf);
}}else if(this.__qf!=K){this.__qf=K;
this.__qd.restartWith(K.getOpenInterval());
}},scheduleClose:function(L){this.cancelOpen(L);
if(!L.isVisible()){if(this.__qg){this.cancelClose(this.__qg);
}}else if(this.__qg!=L){this.__qg=L;
this.__qe.restartWith(L.getCloseInterval());
}},cancelOpen:function(M){if(this.__qf==M){this.__qd.stop();
this.__qf=null;
}},cancelClose:function(N){if(this.__qg==N){this.__qe.stop();
this.__qg=null;
}},_onOpenInterval:function(e){this.__qd.stop();
this.__qf.open();
this.__qf=null;
},_onCloseInterval:function(e){this.__qe.stop();
this.__qg.exclude();
this.__qg=null;
},_onMouseDown:function(e){var O=e.getTarget();
O=qx.ui.core.Widget.getWidgetByElement(O,true);
if(O==null){this.hideAll();
return;
}if(O.getMenu&&O.getMenu()&&O.getMenu().isVisible()){return;
}if(this.__qc.length>0&&!this._isInMenu(O)){this.hideAll();
}},__qh:{"Enter":1,"Space":1},__qi:{"Escape":1,"Up":1,"Down":1,"Left":1,"Right":1},_onKeyUpDown:function(e){var P=this.getActiveMenu();

if(!P){return;
}var Q=e.getKeyIdentifier();

if(this.__qi[Q]||(this.__qh[Q]&&P.getSelectedButton())){e.stopPropagation();
}},_onKeyPress:function(e){var R=this.getActiveMenu();

if(!R){return;
}var S=e.getKeyIdentifier();
var U=this.__qi[S];
var T=this.__qh[S];

if(U){switch(S){case c:this._onKeyPressUp(R);
break;
case a:this._onKeyPressDown(R);
break;
case b:this._onKeyPressLeft(R);
break;
case f:this._onKeyPressRight(R);
break;
case j:this.hideAll();
break;
}e.stopPropagation();
e.preventDefault();
}else if(T){var V=R.getSelectedButton();

if(V){switch(S){case m:this._onKeyPressEnter(R,V,e);
break;
case h:this._onKeyPressSpace(R,V,e);
break;
}e.stopPropagation();
e.preventDefault();
}}},_onKeyPressUp:function(W){var X=W.getSelectedButton();
var Y=W.getChildren();
var bb=X?W.indexOf(X)-1:Y.length-1;
var ba=this._getChild(W,bb,-1,true);
if(ba){W.setSelectedButton(ba);
}else{W.resetSelectedButton();
}},_onKeyPressDown:function(bc){var bd=bc.getSelectedButton();
var bf=bd?bc.indexOf(bd)+1:0;
var be=this._getChild(bc,bf,1,true);
if(be){bc.setSelectedButton(be);
}else{bc.resetSelectedButton();
}},_onKeyPressLeft:function(bg){var bl=bg.getOpener();

if(!bl){return;
}if(bl instanceof qx.ui.menu.AbstractButton){var bi=bl.getLayoutParent();
bi.resetOpenedButton();
bi.setSelectedButton(bl);
}else if(bl instanceof qx.ui.menubar.Button){var bk=bl.getMenuBar().getMenuButtons();
var bh=bk.indexOf(bl);
if(bh===-1){return;
}var bm=null;
var length=bk.length;

for(var i=1;i<=length;i++){var bj=bk[(bh-i+length)%length];

if(bj.isEnabled()){bm=bj;
break;
}}
if(bm&&bm!=bl){bm.open(true);
}}},_onKeyPressRight:function(bn){var bp=bn.getSelectedButton();
if(bp){var bo=bp.getMenu();

if(bo){bn.setOpenedButton(bp);
var bv=this._getChild(bo,0,1);

if(bv){bo.setSelectedButton(bv);
}return;
}}else if(!bn.getOpenedButton()){var bv=this._getChild(bn,0,1);

if(bv){bn.setSelectedButton(bv);

if(bv.getMenu()){bn.setOpenedButton(bv);
}return;
}}var bt=bn.getOpener();
if(bt instanceof qx.ui.menu.Button&&bp){while(bt){bt=bt.getLayoutParent();

if(bt instanceof qx.ui.menu.Menu){bt=bt.getOpener();

if(bt instanceof qx.ui.menubar.Button){break;
}}else{break;
}}
if(!bt){return;
}}if(bt instanceof qx.ui.menubar.Button){var bs=bt.getMenuBar().getMenuButtons();
var bq=bs.indexOf(bt);
if(bq===-1){return;
}var bu=null;
var length=bs.length;

for(var i=1;i<=length;i++){var br=bs[(bq+i)%length];

if(br.isEnabled()){bu=br;
break;
}}
if(bu&&bu!=bt){bu.open(true);
}}},_onKeyPressEnter:function(bw,bx,e){if(bx.hasListener(t)){var by=e.clone();
by.setBubbles(false);
by.setTarget(bx);
bx.dispatchEvent(by);
}this.hideAll();
},_onKeyPressSpace:function(bz,bA,e){if(bA.hasListener(t)){var bB=e.clone();
bB.setBubbles(false);
bB.setTarget(bA);
bA.dispatchEvent(bB);
}}},destruct:function(){var bD=qx.event.Registration;
var bC=document.body;
bD.removeListener(window.document.documentElement,q,this._onMouseDown,this,true);
bD.removeListener(bC,r,this._onKeyUpDown,this,true);
bD.removeListener(bC,p,this._onKeyUpDown,this,true);
bD.removeListener(bC,t,this._onKeyPress,this,true);
this._disposeObjects(k,o);
this._disposeArray(l);
}});
})();
(function(){var l="indexOf",k="addAfter",j="add",i="addBefore",h="_",g="addAt",f="hasChildren",e="removeAt",d="removeAll",c="getChildren",a="remove",b="qx.ui.core.MRemoteChildrenHandling";
qx.Mixin.define(b,{members:{__qj:function(m,n,o,p){var q=this.getChildrenContainer();

if(q===this){m=h+m;
}return (q[m])(n,o,p);
},getChildren:function(){return this.__qj(c);
},hasChildren:function(){return this.__qj(f);
},add:function(r,s){return this.__qj(j,r,s);
},remove:function(t){return this.__qj(a,t);
},removeAll:function(){return this.__qj(d);
},indexOf:function(u){return this.__qj(l,u);
},addAt:function(v,w,x){this.__qj(g,v,w,x);
},addBefore:function(y,z,A){this.__qj(i,y,z,A);
},addAfter:function(B,C,D){this.__qj(k,B,C,D);
},removeAt:function(E){this.__qj(e,E);
}}});
})();
(function(){var l="slidebar",k="Integer",j="resize",h="qx.ui.core.Widget",g="selected",f="visible",d="Boolean",c="mouseout",b="excluded",a="menu",A="_applySelectedButton",z="_applySpacingY",y="_blocker",x="_applyCloseInterval",w="_applyBlockerColor",v="_applyIconColumnWidth",u="mouseover",t="_applyArrowColumnWidth",s="qx.ui.menu.Menu",r="Color",p="Number",q="_applyOpenInterval",n="_applySpacingX",o="_applyBlockerOpacity",m="_applyOpenedButton";
qx.Class.define(s,{extend:qx.ui.core.Widget,include:[qx.ui.core.MPlacement,qx.ui.core.MRemoteChildrenHandling],construct:function(){qx.ui.core.Widget.call(this);
this._setLayout(new qx.ui.menu.Layout);
var B=this.getApplicationRoot();
B.add(this);
this.addListener(u,this._onMouseOver);
this.addListener(c,this._onMouseOut);
this.addListener(j,this._onResize,this);
B.addListener(j,this._onResize,this);
this._blocker=new qx.ui.core.Blocker(B);
this.initVisibility();
this.initKeepFocus();
this.initKeepActive();
},properties:{appearance:{refine:true,init:a},allowGrowX:{refine:true,init:false},allowGrowY:{refine:true,init:false},visibility:{refine:true,init:b},keepFocus:{refine:true,init:true},keepActive:{refine:true,init:true},spacingX:{check:k,apply:n,init:0,themeable:true},spacingY:{check:k,apply:z,init:0,themeable:true},iconColumnWidth:{check:k,init:0,themeable:true,apply:v},arrowColumnWidth:{check:k,init:0,themeable:true,apply:t},blockerColor:{check:r,init:null,nullable:true,apply:w,themeable:true},blockerOpacity:{check:p,init:1,apply:o,themeable:true},selectedButton:{check:h,nullable:true,apply:A},openedButton:{check:h,nullable:true,apply:m},opener:{check:h,nullable:true},openInterval:{check:k,themeable:true,init:250,apply:q},closeInterval:{check:k,themeable:true,init:250,apply:x},blockBackground:{check:d,themeable:true,init:false}},members:{__qk:null,__ql:null,_blocker:null,open:function(){if(this.getOpener()!=null){this.placeToWidget(this.getOpener());
this.__qn();
this.show();
this._placementTarget=this.getOpener();
}else{this.warn("The menu instance needs a configured 'opener' widget!");
}},openAtMouse:function(e){this.placeToMouse(e);
this.__qn();
this.show();
this._placementTarget={left:e.getDocumentLeft(),top:e.getDocumentTop()};
},openAtPoint:function(C){this.placeToPoint(C);
this.__qn();
this.show();
this._placementTarget=C;
},addSeparator:function(){this.add(new qx.ui.menu.Separator);
},getColumnSizes:function(){return this._getMenuLayout().getColumnSizes();
},getSelectables:function(){var D=[];
var E=this.getChildren();

for(var i=0;i<E.length;i++){if(E[i].isEnabled()){D.push(E[i]);
}}return D;
},_applyIconColumnWidth:function(F,G){this._getMenuLayout().setIconColumnWidth(F);
},_applyArrowColumnWidth:function(H,I){this._getMenuLayout().setArrowColumnWidth(H);
},_applySpacingX:function(J,K){this._getMenuLayout().setColumnSpacing(J);
},_applySpacingY:function(L,M){this._getMenuLayout().setSpacing(L);
},_applyVisibility:function(N,O){qx.ui.core.Widget.prototype._applyVisibility.call(this,N,O);
var P=qx.ui.menu.Manager.getInstance();

if(N===f){P.add(this);
var Q=this.getParentMenu();

if(Q){Q.setOpenedButton(this.getOpener());
}}else if(O===f){P.remove(this);
var Q=this.getParentMenu();

if(Q&&Q.getOpenedButton()==this.getOpener()){Q.resetOpenedButton();
}this.resetOpenedButton();
this.resetSelectedButton();
}this.__qm();
},__qm:function(){if(this.isVisible()){if(this.getBlockBackground()){var R=this.getZIndex();
this._blocker.blockContent(R-1);
}}else{if(this._blocker.isContentBlocked()){this._blocker.unblockContent();
}}},getParentMenu:function(){var S=this.getOpener();

if(!S||!(S instanceof qx.ui.menu.AbstractButton)){return null;
}
while(S&&!(S instanceof qx.ui.menu.Menu)){S=S.getLayoutParent();
}return S;
},_applySelectedButton:function(T,U){if(U){U.removeState(g);
}
if(T){T.addState(g);
}},_applyOpenedButton:function(V,W){if(W){W.getMenu().exclude();
}
if(V){V.getMenu().open();
}},_applyBlockerColor:function(X,Y){this._blocker.setColor(X);
},_applyBlockerOpacity:function(ba,bb){this._blocker.setOpacity(ba);
},getChildrenContainer:function(){return this.getChildControl(l,true)||this;
},_createChildControlImpl:function(bc,bd){var be;

switch(bc){case l:var be=new qx.ui.menu.MenuSlideBar();
var bg=this._getLayout();
this._setLayout(new qx.ui.layout.Grow());
var bf=be.getLayout();
be.setLayout(bg);
bf.dispose();
var bh=qx.lang.Array.clone(this.getChildren());

for(var i=0;i<bh.length;i++){be.add(bh[i]);
}this.removeListener(j,this._onResize,this);
be.getChildrenContainer().addListener(j,this._onResize,this);
this._add(be);
break;
}return be||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,bc);
},_getMenuLayout:function(){if(this.hasChildControl(l)){return this.getChildControl(l).getChildrenContainer().getLayout();
}else{return this._getLayout();
}},_getMenuBounds:function(){if(this.hasChildControl(l)){return this.getChildControl(l).getChildrenContainer().getBounds();
}else{return this.getBounds();
}},_computePlacementSize:function(){return this._getMenuBounds();
},__qn:function(){var bj=this._getMenuBounds();

if(!bj){this.addListenerOnce(j,this.__qn,this);
return;
}var bi=this.getLayoutParent().getBounds().height;
var top=this.getLayoutProperties().top;
var bk=this.getLayoutProperties().left;
if(top<0){this._assertSlideBar(function(){this.setHeight(bj.height+top);
this.moveTo(bk,0);
});
}else if(top+bj.height>bi){this._assertSlideBar(function(){this.setHeight(bi-top);
});
}else{this.setHeight(null);
}},_assertSlideBar:function(bl){if(this.hasChildControl(l)){return bl.call(this);
}this.__ql=bl;
qx.ui.core.queue.Widget.add(this);
},syncWidget:function(){this.getChildControl(l);

if(this.__ql){this.__ql.call(this);
delete this.__ql;
}},_onResize:function(){if(this.isVisible()){var bm=this._placementTarget;

if(!bm){return;
}else if(bm instanceof qx.ui.core.Widget){this.placeToWidget(bm);
}else if(bm.top!==undefined){this.placeToPoint(bm);
}else{throw new Error("Unknown target: "+bm);
}this.__qn();
}},_onMouseOver:function(e){var bo=qx.ui.menu.Manager.getInstance();
bo.cancelClose(this);
var bp=e.getTarget();

if(bp.isEnabled()&&bp instanceof qx.ui.menu.AbstractButton){this.setSelectedButton(bp);
var bn=bp.getMenu&&bp.getMenu();

if(bn){bn.setOpener(bp);
bo.scheduleOpen(bn);
this.__qk=bn;
}else{var bq=this.getOpenedButton();

if(bq){bo.scheduleClose(bq.getMenu());
}
if(this.__qk){bo.cancelOpen(this.__qk);
this.__qk=null;
}}}else if(!this.getOpenedButton()){this.resetSelectedButton();
}},_onMouseOut:function(e){var br=qx.ui.menu.Manager.getInstance();
if(!qx.ui.core.Widget.contains(this,e.getRelatedTarget())){var bs=this.getOpenedButton();
bs?this.setSelectedButton(bs):this.resetSelectedButton();
if(bs){br.cancelClose(bs.getMenu());
}if(this.__qk){br.cancelOpen(this.__qk);
}}}},destruct:function(){if(!qx.core.ObjectRegistry.inShutDown){qx.ui.menu.Manager.getInstance().remove(this);
}this.getApplicationRoot().removeListener(j,this._onResize,this);
this._placementTarget=null;
this._disposeObjects(y);
}});
})();
(function(){var n="_applyLayoutChange",m="top",k="left",j="middle",h="Decorator",g="center",f="_applyReversed",e="bottom",d="qx.ui.layout.VBox",c="Integer",a="right",b="Boolean";
qx.Class.define(d,{extend:qx.ui.layout.Abstract,construct:function(o,p,q){qx.ui.layout.Abstract.call(this);

if(o){this.setSpacing(o);
}
if(p){this.setAlignY(p);
}
if(q){this.setSeparator(q);
}},properties:{alignY:{check:[m,j,e],init:m,apply:n},alignX:{check:[k,g,a],init:k,apply:n},spacing:{check:c,init:0,apply:n},separator:{check:h,nullable:true,apply:n},reversed:{check:b,init:false,apply:f}},members:{__mU:null,__mV:null,__mW:null,__mX:null,_applyReversed:function(){this._invalidChildrenCache=true;
this._applyLayoutChange();
},__mY:function(){var w=this._getLayoutChildren();
var length=w.length;
var s=false;
var r=this.__mU&&this.__mU.length!=length&&this.__mV&&this.__mU;
var u;
var t=r?this.__mU:new Array(length);
var v=r?this.__mV:new Array(length);
if(this.getReversed()){w=w.concat().reverse();
}for(var i=0;i<length;i++){u=w[i].getLayoutProperties();

if(u.height!=null){t[i]=parseFloat(u.height)/100;
}
if(u.flex!=null){v[i]=u.flex;
s=true;
}else{v[i]=0;
}}if(!r){this.__mU=t;
this.__mV=v;
}this.__mW=s;
this.__mX=w;
delete this._invalidChildrenCache;
},verifyLayoutProperty:null,renderLayout:function(x,y){if(this._invalidChildrenCache){this.__mY();
}var F=this.__mX;
var length=F.length;
var P=qx.ui.layout.Util;
var O=this.getSpacing();
var S=this.getSeparator();

if(S){var C=P.computeVerticalSeparatorGaps(F,O,S);
}else{var C=P.computeVerticalGaps(F,O,true);
}var i,A,B,J;
var K=[];
var Q=C;

for(i=0;i<length;i+=1){J=this.__mU[i];
B=J!=null?Math.floor((y-C)*J):F[i].getSizeHint().height;
K.push(B);
Q+=B;
}if(this.__mW&&Q!=y){var H={};
var N,R;

for(i=0;i<length;i+=1){N=this.__mV[i];

if(N>0){G=F[i].getSizeHint();
H[i]={min:G.minHeight,value:K[i],max:G.maxHeight,flex:N};
}}var D=P.computeFlexOffsets(H,y,Q);

for(i in D){R=D[i].offset;
K[i]+=R;
Q+=R;
}}var top=F[0].getMarginTop();
if(Q<y&&this.getAlignY()!=m){top=y-Q;

if(this.getAlignY()===j){top=Math.round(top/2);
}}var G,U,L,B,I,M,E;
this._clearSeparators();
if(S){var T=qx.theme.manager.Decoration.getInstance().resolve(S).getInsets();
var z=T.top+T.bottom;
}for(i=0;i<length;i+=1){A=F[i];
B=K[i];
G=A.getSizeHint();
M=A.getMarginLeft();
E=A.getMarginRight();
L=Math.max(G.minWidth,Math.min(x-M-E,G.maxWidth));
U=P.computeHorizontalAlignOffset(A.getAlignX()||this.getAlignX(),L,x,M,E);
if(i>0){if(S){top+=I+O;
this._renderSeparator(S,{top:top,left:0,height:z,width:x});
top+=z+O+A.getMarginTop();
}else{top+=P.collapseMargins(O,I,A.getMarginTop());
}}A.renderLayout(U,top,L,B);
top+=B;
I=A.getMarginBottom();
}},_computeSizeHint:function(){if(this._invalidChildrenCache){this.__mY();
}var bc=qx.ui.layout.Util;
var bk=this.__mX;
var X=0,bb=0,ba=0;
var V=0,bd=0;
var bh,W,bj;
for(var i=0,l=bk.length;i<l;i+=1){bh=bk[i];
W=bh.getSizeHint();
bb+=W.height;
var bg=this.__mV[i];
var Y=this.__mU[i];

if(bg){X+=W.minHeight;
}else if(Y){ba=Math.max(ba,Math.round(W.minHeight/Y));
}else{X+=W.height;
}bj=bh.getMarginLeft()+bh.getMarginRight();
if((W.width+bj)>bd){bd=W.width+bj;
}if((W.minWidth+bj)>V){V=W.minWidth+bj;
}}X+=ba;
var bf=this.getSpacing();
var bi=this.getSeparator();

if(bi){var be=bc.computeVerticalSeparatorGaps(bk,bf,bi);
}else{var be=bc.computeVerticalGaps(bk,bf,true);
}return {minHeight:X+be,height:bb+be,minWidth:V,width:bd};
}},destruct:function(){this.__mU=this.__mV=this.__mX=null;
}});
})();
(function(){var c="Integer",b="_applyLayoutChange",a="qx.ui.menu.Layout";
qx.Class.define(a,{extend:qx.ui.layout.VBox,properties:{columnSpacing:{check:c,init:0,apply:b},spanColumn:{check:c,init:1,nullable:true,apply:b},iconColumnWidth:{check:c,init:0,themeable:true,apply:b},arrowColumnWidth:{check:c,init:0,themeable:true,apply:b}},members:{__qo:null,_computeSizeHint:function(){var q=this._getLayoutChildren();
var o,g,j;
var e=this.getSpanColumn();
var h=this.__qo=[0,0,0,0];
var m=this.getColumnSpacing();
var k=0;
var f=0;
for(var i=0,l=q.length;i<l;i++){o=q[i];

if(o.isAnonymous()){continue;
}g=o.getChildrenSizes();

for(var n=0;n<g.length;n++){if(e!=null&&n==e&&g[e+1]==0){k=Math.max(k,g[n]);
}else{h[n]=Math.max(h[n],g[n]);
}}var d=q[i].getInsets();
f=Math.max(f,d.left+d.right);
}if(e!=null&&h[e]+m+h[e+1]<k){h[e]=k-h[e+1]-m;
}if(k==0){j=m*2;
}else{j=m*3;
}if(h[0]==0){h[0]=this.getIconColumnWidth();
}if(h[3]==0){h[3]=this.getArrowColumnWidth();
}var p=qx.ui.layout.VBox.prototype._computeSizeHint.call(this).height;
return {minHeight:p,height:p,width:qx.lang.Array.sum(h)+f+j};
},getColumnSizes:function(){return this.__qo||null;
}},destruct:function(){this.__qo=null;
}});
})();
(function(){var b="menu-separator",a="qx.ui.menu.Separator";
qx.Class.define(a,{extend:qx.ui.core.Widget,properties:{appearance:{refine:true,init:b},anonymous:{refine:true,init:true}}});
})();
(function(){var t="icon",s="label",r="arrow",q="shortcut",p="changeLocale",o="qx.dynlocale",n="submenu",m="on",l="String",k="qx.ui.menu.Menu",d="qx.ui.menu.AbstractButton",j="keypress",h="",c="_applyIcon",b="mouseup",g="abstract",f="_applyLabel",i="_applyMenu",a="changeCommand";
qx.Class.define(d,{extend:qx.ui.core.Widget,include:[qx.ui.core.MExecutable],implement:[qx.ui.form.IExecutable],type:g,construct:function(){qx.ui.core.Widget.call(this);
this._setLayout(new qx.ui.menu.ButtonLayout);
this.addListener(b,this._onMouseUp);
this.addListener(j,this._onKeyPress);
this.addListener(a,this._onChangeCommand,this);
},properties:{blockToolTip:{refine:true,init:true},label:{check:l,apply:f,nullable:true},menu:{check:k,apply:i,nullable:true,dereference:true},icon:{check:l,apply:c,themeable:true,nullable:true}},members:{_createChildControlImpl:function(u,v){var w;

switch(u){case t:w=new qx.ui.basic.Image;
w.setAnonymous(true);
this._add(w,{column:0});
break;
case s:w=new qx.ui.basic.Label;
w.setAnonymous(true);
this._add(w,{column:1});
break;
case q:w=new qx.ui.basic.Label;
w.setAnonymous(true);
this._add(w,{column:2});
break;
case r:w=new qx.ui.basic.Image;
w.setAnonymous(true);
this._add(w,{column:3});
break;
}return w||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,u);
},_forwardStates:{selected:1},getChildrenSizes:function(){var x=0,y=0,z=0,D=0;

if(this._isChildControlVisible(t)){var E=this.getChildControl(t);
x=E.getMarginLeft()+E.getSizeHint().width+E.getMarginRight();
}
if(this._isChildControlVisible(s)){var B=this.getChildControl(s);
y=B.getMarginLeft()+B.getSizeHint().width+B.getMarginRight();
}
if(this._isChildControlVisible(q)){var A=this.getChildControl(q);
z=A.getMarginLeft()+A.getSizeHint().width+A.getMarginRight();
}
if(this._isChildControlVisible(r)){var C=this.getChildControl(r);
D=C.getMarginLeft()+C.getSizeHint().width+C.getMarginRight();
}return [x,y,z,D];
},_onMouseUp:function(e){},_onKeyPress:function(e){},_onChangeCommand:function(e){var H=e.getData();
if(H==null){return;
}
if(qx.core.Variant.isSet(o,m)){var F=e.getOldData();

if(!F){qx.locale.Manager.getInstance().addListener(p,this._onChangeLocale,this);
}
if(!H){qx.locale.Manager.getInstance().removeListener(p,this._onChangeLocale,this);
}}var G=H!=null?H.toString():h;
this.getChildControl(q).setValue(G);
},_onChangeLocale:qx.core.Variant.select(o,{"on":function(e){var I=this.getCommand();

if(I!=null){this.getChildControl(q).setValue(I.toString());
}},"off":null}),_applyIcon:function(J,K){if(J){this._showChildControl(t).setSource(J);
}else{this._excludeChildControl(t);
}},_applyLabel:function(L,M){if(L){this._showChildControl(s).setValue(L);
}else{this._excludeChildControl(s);
}},_applyMenu:function(N,O){if(O){O.resetOpener();
O.removeState(n);
}
if(N){this._showChildControl(r);
N.setOpener(this);
N.addState(n);
}else{this._excludeChildControl(r);
}}},destruct:function(){if(this.getMenu()){if(!qx.core.ObjectRegistry.inShutDown){this.getMenu().destroy();
}}
if(qx.core.Variant.isSet(o,m)){qx.locale.Manager.getInstance().removeListener(p,this._onChangeLocale,this);
}}});
})();
(function(){var c="middle",b="qx.ui.menu.ButtonLayout",a="left";
qx.Class.define(b,{extend:qx.ui.layout.Abstract,members:{verifyLayoutProperty:null,renderLayout:function(d,e){var q=this._getLayoutChildren();
var p;
var g;
var h=[];

for(var i=0,l=q.length;i<l;i++){p=q[i];
g=p.getLayoutProperties().column;
h[g]=p;
}var o=this.__qp(q[0]);
var r=o.getColumnSizes();
var k=o.getSpacingX();
var j=qx.lang.Array.sum(r)+k*(r.length-1);

if(j<d){r[1]+=d-j;
}var s=0,top=0;
var m=qx.ui.layout.Util;

for(var i=0,l=r.length;i<l;i++){p=h[i];

if(p){var f=p.getSizeHint();
var top=m.computeVerticalAlignOffset(p.getAlignY()||c,f.height,e,0,0);
var n=m.computeHorizontalAlignOffset(p.getAlignX()||a,f.width,r[i],p.getMarginLeft(),p.getMarginRight());
p.renderLayout(s+n,top,f.width,f.height);
}s+=r[i]+k;
}},__qp:function(t){while(!(t instanceof qx.ui.menu.Menu)){t=t.getLayoutParent();
}return t;
},_computeSizeHint:function(){var w=this._getLayoutChildren();
var v=0;
var x=0;

for(var i=0,l=w.length;i<l;i++){var u=w[i].getSizeHint();
x+=u.width;
v=Math.max(v,u.height);
}return {width:x,height:v};
}}});
})();
(function(){var a="qx.ui.core.MRemoteLayoutHandling";
qx.Mixin.define(a,{members:{setLayout:function(b){return this.getChildrenContainer().setLayout(b);
},getLayout:function(){return this.getChildrenContainer().getLayout();
}}});
})();
(function(){var q="horizontal",p="scrollpane",o="vertical",n="button-backward",m="button-forward",l="content",k="execute",j="qx.ui.container.SlideBar",i="scrollY",h="removeChildWidget",c="scrollX",g="_applyOrientation",f="mousewheel",b="Integer",a="slidebar",d="update";
qx.Class.define(j,{extend:qx.ui.core.Widget,include:[qx.ui.core.MRemoteChildrenHandling,qx.ui.core.MRemoteLayoutHandling],construct:function(r){qx.ui.core.Widget.call(this);
var s=this.getChildControl(p);
this._add(s,{flex:1});

if(r!=null){this.setOrientation(r);
}else{this.initOrientation();
}this.addListener(f,this._onMouseWheel,this);
},properties:{appearance:{refine:true,init:a},orientation:{check:[q,o],init:q,apply:g},scrollStep:{check:b,init:15,themeable:true}},members:{getChildrenContainer:function(){return this.getChildControl(l);
},_createChildControlImpl:function(t,u){var v;

switch(t){case m:v=new qx.ui.form.RepeatButton;
v.addListener(k,this._onExecuteForward,this);
v.setFocusable(false);
this._addAt(v,2);
break;
case n:v=new qx.ui.form.RepeatButton;
v.addListener(k,this._onExecuteBackward,this);
v.setFocusable(false);
this._addAt(v,0);
break;
case l:v=new qx.ui.container.Composite();
if(qx.bom.client.Engine.GECKO){v.addListener(h,this._onRemoveChild,this);
}this.getChildControl(p).add(v);
break;
case p:v=new qx.ui.core.scroll.ScrollPane();
v.addListener(d,this._onResize,this);
v.addListener(c,this._onScroll,this);
v.addListener(i,this._onScroll,this);
break;
}return v||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,t);
},_forwardStates:{barLeft:true,barTop:true,barRight:true,barBottom:true},scrollBy:function(w){var x=this.getChildControl(p);

if(this.getOrientation()===q){x.scrollByX(w);
}else{x.scrollByY(w);
}},scrollTo:function(y){var z=this.getChildControl(p);

if(this.getOrientation()===q){z.scrollToX(y);
}else{z.scrollToY(y);
}},_applyOrientation:function(A,B){var E=[this.getLayout(),this._getLayout()];
var D=this.getChildControl(m);
var C=this.getChildControl(n);
if(B==o){D.removeState(o);
C.removeState(o);
D.addState(q);
C.addState(q);
}else if(B==q){D.removeState(q);
C.removeState(q);
D.addState(o);
C.addState(o);
}
if(A==q){this._setLayout(new qx.ui.layout.HBox());
this.setLayout(new qx.ui.layout.HBox());
}else{this._setLayout(new qx.ui.layout.VBox());
this.setLayout(new qx.ui.layout.VBox());
}
if(E[0]){E[0].dispose();
}
if(E[1]){E[1].dispose();
}},_onMouseWheel:function(e){this.scrollBy(e.getWheelDelta()*this.getScrollStep());
e.stop();
},_onScroll:function(){this._updateArrowsEnabled();
},_onResize:function(e){var content=this.getChildControl(p).getChildren()[0];

if(!content){return;
}var F=this.getInnerSize();
var H=content.getBounds();
var G=(this.getOrientation()===q)?H.width>F.width:H.height>F.height;

if(G){this._showArrows();
this._updateArrowsEnabled();
}else{this._hideArrows();
}},_onExecuteBackward:function(){this.scrollBy(-this.getScrollStep());
},_onExecuteForward:function(){this.scrollBy(this.getScrollStep());
},_onRemoveChild:function(){qx.event.Timer.once(function(){this.scrollBy(this.getChildControl(p).getScrollX());
},this,50);
},_updateArrowsEnabled:function(){var J=this.getChildControl(p);

if(this.getOrientation()===q){var I=J.getScrollX();
var K=J.getScrollMaxX();
}else{var I=J.getScrollY();
var K=J.getScrollMaxY();
}this.getChildControl(n).setEnabled(I>0);
this.getChildControl(m).setEnabled(I<K);
},_showArrows:function(){this._showChildControl(m);
this._showChildControl(n);
},_hideArrows:function(){this._excludeChildControl(m);
this._excludeChildControl(n);
this.scrollTo(0);
}}});
})();
(function(){var f="execute",e="button-backward",d="vertical",c="button-forward",b="menu-slidebar",a="qx.ui.menu.MenuSlideBar";
qx.Class.define(a,{extend:qx.ui.container.SlideBar,construct:function(){qx.ui.container.SlideBar.call(this,d);
},properties:{appearance:{refine:true,init:b}},members:{_createChildControlImpl:function(g,h){var i;

switch(g){case c:i=new qx.ui.form.HoverButton();
i.addListener(f,this._onExecuteForward,this);
this._addAt(i,2);
break;
case e:i=new qx.ui.form.HoverButton();
i.addListener(f,this._onExecuteBackward,this);
this._addAt(i,0);
break;
}return i||qx.ui.container.SlideBar.prototype._createChildControlImpl.call(this,g);
}}});
})();
(function(){var n="pressed",m="abandoned",l="Integer",k="hovered",j="qx.event.type.Event",i="Enter",h="Space",g="press",f="qx.ui.form.RepeatButton",d="release",a="interval",c="execute",b="__ob";
qx.Class.define(f,{extend:qx.ui.form.Button,construct:function(o,p){qx.ui.form.Button.call(this,o,p);
this.__ob=new qx.event.AcceleratingTimer();
this.__ob.addListener(a,this._onInterval,this);
},events:{"execute":j,"press":j,"release":j},properties:{interval:{check:l,init:100},firstInterval:{check:l,init:500},minTimer:{check:l,init:20},timerDecrease:{check:l,init:2}},members:{__oc:null,__ob:null,press:function(){if(this.isEnabled()){if(!this.hasState(n)){this.__od();
}this.removeState(m);
this.addState(n);
}},release:function(q){if(!this.isEnabled()){return;
}if(this.hasState(n)){if(!this.__oc){this.execute();
}}this.removeState(n);
this.removeState(m);
this.__oe();
},_applyEnabled:function(r,s){qx.ui.form.Button.prototype._applyEnabled.call(this,r,s);

if(!r){this.removeState(n);
this.removeState(m);
this.__oe();
}},_onMouseOver:function(e){if(!this.isEnabled()||e.getTarget()!==this){return;
}
if(this.hasState(m)){this.removeState(m);
this.addState(n);
this.__ob.start();
}this.addState(k);
},_onMouseOut:function(e){if(!this.isEnabled()||e.getTarget()!==this){return;
}this.removeState(k);

if(this.hasState(n)){this.removeState(n);
this.addState(m);
this.__ob.stop();
}},_onMouseDown:function(e){if(!e.isLeftPressed()){return;
}this.capture();
this.__od();
e.stopPropagation();
},_onMouseUp:function(e){this.releaseCapture();

if(!this.hasState(m)){this.addState(k);

if(this.hasState(n)&&!this.__oc){this.execute();
}}this.__oe();
e.stopPropagation();
},_onKeyUp:function(e){switch(e.getKeyIdentifier()){case i:case h:if(this.hasState(n)){if(!this.__oc){this.execute();
}this.removeState(n);
this.removeState(m);
e.stopPropagation();
this.__oe();
}}},_onKeyDown:function(e){switch(e.getKeyIdentifier()){case i:case h:this.removeState(m);
this.addState(n);
e.stopPropagation();
this.__od();
}},_onInterval:function(e){this.__oc=true;
this.fireEvent(c);
},__od:function(){this.fireEvent(g);
this.__oc=false;
this.__ob.set({interval:this.getInterval(),firstInterval:this.getFirstInterval(),minimum:this.getMinTimer(),decrease:this.getTimerDecrease()}).start();
this.removeState(m);
this.addState(n);
},__oe:function(){this.fireEvent(d);
this.__ob.stop();
this.removeState(m);
this.removeState(n);
}},destruct:function(){this._disposeObjects(b);
}});
})();
(function(){var e="Integer",d="interval",c="__of",b="qx.event.type.Event",a="qx.event.AcceleratingTimer";
qx.Class.define(a,{extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__of=new qx.event.Timer(this.getInterval());
this.__of.addListener(d,this._onInterval,this);
},events:{"interval":b},properties:{interval:{check:e,init:100},firstInterval:{check:e,init:500},minimum:{check:e,init:20},decrease:{check:e,init:2}},members:{__of:null,__og:null,start:function(){this.__of.setInterval(this.getFirstInterval());
this.__of.start();
},stop:function(){this.__of.stop();
this.__og=null;
},_onInterval:function(){this.__of.stop();

if(this.__og==null){this.__og=this.getInterval();
}this.__og=Math.max(this.getMinimum(),this.__og-this.getDecrease());
this.__of.setInterval(this.__og);
this.__of.start();
this.fireEvent(d);
}},destruct:function(){this._disposeObjects(c);
}});
})();
(function(){var m="resize",l="scrollY",k="update",j="scrollX",i="_applyScrollX",h="_applyScrollY",g="qx.lang.Type.isNumber(value)&&value>=0&&value<=this.getScrollMaxX()",f="appear",d="qx.lang.Type.isNumber(value)&&value>=0&&value<=this.getScrollMaxY()",c="qx.event.type.Event",a="qx.ui.core.scroll.ScrollPane",b="scroll";
qx.Class.define(a,{extend:qx.ui.core.Widget,construct:function(){qx.ui.core.Widget.call(this);
this.set({minWidth:0,minHeight:0});
this._setLayout(new qx.ui.layout.Grow());
this.addListener(m,this._onUpdate);
var n=this.getContentElement();
n.addListener(b,this._onScroll,this);
n.addListener(f,this._onAppear,this);
},events:{update:c},properties:{scrollX:{check:g,apply:i,event:j,init:0},scrollY:{check:d,apply:h,event:l,init:0}},members:{add:function(o){var p=this._getChildren()[0];

if(p){this._remove(p);
p.removeListener(m,this._onUpdate,this);
}
if(o){this._add(o);
o.addListener(m,this._onUpdate,this);
}},remove:function(q){if(q){this._remove(q);
q.removeListener(m,this._onUpdate,this);
}},getChildren:function(){return this._getChildren();
},_onUpdate:function(e){this.fireEvent(k);
},_onScroll:function(e){var r=this.getContentElement();
this.setScrollX(r.getScrollX());
this.setScrollY(r.getScrollY());
},_onAppear:function(e){var v=this.getContentElement();
var s=this.getScrollX();
var t=v.getScrollX();

if(s!=t){v.scrollToX(s);
}var w=this.getScrollY();
var u=v.getScrollY();

if(w!=u){v.scrollToY(w);
}},getItemTop:function(z){var top=0;

do{top+=z.getBounds().top;
z=z.getLayoutParent();
}while(z&&z!==this);
return top;
},getItemBottom:function(A){return this.getItemTop(A)+A.getBounds().height;
},getItemLeft:function(B){var C=0;
var parent;

do{C+=B.getBounds().left;
parent=B.getLayoutParent();

if(parent){C+=parent.getInsets().left;
}B=parent;
}while(B&&B!==this);
return C;
},getItemRight:function(D){return this.getItemLeft(D)+D.getBounds().width;
},getScrollSize:function(){return this.getChildren()[0].getBounds();
},getScrollMaxX:function(){var F=this.getInnerSize();
var E=this.getScrollSize();

if(F&&E){return Math.max(0,E.width-F.width);
}return 0;
},getScrollMaxY:function(){var H=this.getInnerSize();
var G=this.getScrollSize();

if(H&&G){return Math.max(0,G.height-H.height);
}return 0;
},scrollToX:function(I){var J=this.getScrollMaxX();

if(I<0){I=0;
}else if(I>J){I=J;
}this.setScrollX(I);
},scrollToY:function(K){var L=this.getScrollMaxY();

if(K<0){K=0;
}else if(K>L){K=L;
}this.setScrollY(K);
},scrollByX:function(x){this.scrollToX(this.getScrollX()+x);
},scrollByY:function(y){this.scrollToY(this.getScrollY()+y);
},_applyScrollX:function(M){this.getContentElement().scrollToX(M);
},_applyScrollY:function(N){this.getContentElement().scrollToY(N);
}}});
})();
(function(){var i="Integer",h="hovered",g="hover-button",f="__qq",d="interval",c="mouseover",b="mouseout",a="qx.ui.form.HoverButton";
qx.Class.define(a,{extend:qx.ui.basic.Atom,include:[qx.ui.core.MExecutable],implement:[qx.ui.form.IExecutable],construct:function(j,k){qx.ui.basic.Atom.call(this,j,k);
this.addListener(c,this._onMouseOver,this);
this.addListener(b,this._onMouseOut,this);
this.__qq=new qx.event.AcceleratingTimer();
this.__qq.addListener(d,this._onInterval,this);
},properties:{appearance:{refine:true,init:g},interval:{check:i,init:80},firstInterval:{check:i,init:200},minTimer:{check:i,init:20},timerDecrease:{check:i,init:2}},members:{__qq:null,_onMouseOver:function(e){if(!this.isEnabled()||e.getTarget()!==this){return;
}this.__qq.set({interval:this.getInterval(),firstInterval:this.getFirstInterval(),minimum:this.getMinTimer(),decrease:this.getTimerDecrease()}).start();
this.addState(h);
},_onMouseOut:function(e){this.__qq.stop();
this.removeState(h);

if(!this.isEnabled()||e.getTarget()!==this){return;
}},_onInterval:function(){if(this.isEnabled()){this.execute();
}else{this.__qq.stop();
}}},destruct:function(){this._disposeObjects(f);
}});
})();
(function(){var b="qx.ui.menu.Button",a="menu-button";
qx.Class.define(b,{extend:qx.ui.menu.AbstractButton,construct:function(c,d,f,g){qx.ui.menu.AbstractButton.call(this);
if(c!=null){this.setLabel(c);
}
if(d!=null){this.setIcon(d);
}
if(f!=null){this.setCommand(f);
}
if(g!=null){this.setMenu(g);
}},properties:{appearance:{refine:true,init:a}},members:{_onMouseUp:function(e){if(e.isLeftPressed()){this.execute();
if(this.getMenu()){return;
}}qx.ui.menu.Manager.getInstance().hideAll();
},_onKeyPress:function(e){this.execute();
}}});
})();
(function(){var p="middle",o="left",n="right",m="container",k="handle",j="both",h="Integer",g="qx.ui.toolbar.Part",f="icon",e="label",b="syncAppearance",d="changeShow",c="_applySpacing",a="toolbar/part";
qx.Class.define(g,{extend:qx.ui.core.Widget,include:[qx.ui.core.MRemoteChildrenHandling],construct:function(){qx.ui.core.Widget.call(this);
this._setLayout(new qx.ui.layout.HBox);
this._createChildControl(k);
},properties:{appearance:{refine:true,init:a},show:{init:j,check:[j,e,f],inheritable:true,event:d},spacing:{nullable:true,check:h,themeable:true,apply:c}},members:{_createChildControlImpl:function(q,r){var s;

switch(q){case k:s=new qx.ui.basic.Image();
s.setAlignY(p);
this._add(s);
break;
case m:s=new qx.ui.toolbar.PartContainer();
s.addListener(b,this.__tX,this);
this._add(s);
break;
}return s||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,q);
},getChildrenContainer:function(){return this.getChildControl(m);
},_applySpacing:function(t,u){var v=this.getChildControl(m).getLayout();
t==null?v.resetSpacing():v.setSpacing(t);
},__tX:function(){var w=this.getChildrenContainer().getChildren();

for(var i=0;i<w.length;i++){if(i==0&&i!=w.length-1){w[i].addState(o);
w[i].removeState(n);
w[i].removeState(p);
}else if(i==w.length-1&&i!=0){w[i].addState(n);
w[i].removeState(o);
w[i].removeState(p);
}else if(i==0&&i==w.length-1){w[i].removeState(o);
w[i].removeState(p);
w[i].removeState(n);
}else{w[i].addState(p);
w[i].removeState(n);
w[i].removeState(o);
}}},addSeparator:function(){this.add(new qx.ui.toolbar.Separator);
},getMenuButtons:function(){var y=this.getChildren();
var x=[];
var z;

for(var i=0,l=y.length;i<l;i++){z=y[i];

if(z instanceof qx.ui.menubar.Button){x.push(z);
}}return x;
}}});
})();
(function(){var f="both",e="toolbar/part/container",d="icon",c="changeShow",b="qx.ui.toolbar.PartContainer",a="label";
qx.Class.define(b,{extend:qx.ui.container.Composite,construct:function(){qx.ui.container.Composite.call(this);
this._setLayout(new qx.ui.layout.HBox);
},properties:{appearance:{refine:true,init:e},show:{init:f,check:[f,a,d],inheritable:true,event:c}}});
})();
(function(){var e="arrow",d="qx.ui.toolbar.MenuButton",c="Boolean",b="_applyShowArrow",a="toolbar-menubutton";
qx.Class.define(d,{extend:qx.ui.menubar.Button,properties:{appearance:{refine:true,init:a},showArrow:{check:c,init:false,themeable:true,apply:b}},members:{_createChildControlImpl:function(f,g){var h;

switch(f){case e:h=new qx.ui.basic.Image();
h.setAnonymous(true);
this._addAt(h,10);
break;
}return h||qx.ui.menubar.Button.prototype._createChildControlImpl.call(this,f);
},_applyShowArrow:function(i,j){if(i){this._showChildControl(e);
}else{this._excludeChildControl(e);
}}}});
})();
(function(){var a="qx.ui.window.IWindowManager";
qx.Interface.define(a,{members:{setDesktop:function(b){this.assertInterface(b,qx.ui.window.IDesktop);
},changeActiveWindow:function(c,d){},updateStack:function(){},bringToFront:function(e){this.assertInstance(e,qx.ui.window.Window);
},sendToBack:function(f){this.assertInstance(f,qx.ui.window.Window);
}}});
})();
(function(){var b="__rB",a="qx.ui.window.Manager";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.ui.window.IWindowManager,members:{__rB:null,setDesktop:function(c){this.__rB=c;
this.updateStack();
},getDesktop:function(){return this.__rB;
},changeActiveWindow:function(d,e){if(d){this.bringToFront(d);
d.setActive(true);
}
if(e){e.resetActive();
}},_minZIndex:1e5,updateStack:function(){qx.ui.core.queue.Widget.add(this);
},syncWidget:function(){this.__rB.forceUnblockContent();
var f=this.__rB.getWindows();
var h=this._minZIndex;
var m=h+f.length*2;
var j=h+f.length*4;
var k=null;

for(var i=0,l=f.length;i<l;i++){var g=f[i];
if(!g.isVisible()){continue;
}k=k||g;
if(g.isModal()){g.setZIndex(j);
this.__rB.blockContent(j-1);
j+=2;
k=g;
}else if(g.isAlwaysOnTop()){g.setZIndex(m);
m+=2;
}else{g.setZIndex(h);
h+=2;
}if(!k.isModal()&&g.isActive()||g.getZIndex()>k.getZIndex()){k=g;
}}this.__rB.setActiveWindow(k);
},bringToFront:function(n){var o=this.__rB.getWindows();
var p=qx.lang.Array.remove(o,n);

if(p){o.push(n);
this.updateStack();
}},sendToBack:function(q){var r=this.__rB.getWindows();
var s=qx.lang.Array.remove(r,q);

if(s){r.unshift(q);
this.updateStack();
}}},destruct:function(){this._disposeObjects(b);
}});
})();
(function(){var k="Boolean",j="resize",i="mousedown",h="w-resize",g="sw-resize",f="n-resize",d="resizableRight",c="ne-resize",b="se-resize",a="Integer",z="e-resize",y="resizableLeft",x="mousemove",w="move",v="shorthand",u="maximized",t="nw-resize",s="mouseout",r="qx.ui.core.MResizable",q="mouseup",o="losecapture",p="resize-frame",m="resizableBottom",n="s-resize",l="resizableTop";
qx.Mixin.define(r,{construct:function(){var A=this.getContainerElement();
A.addListener(i,this.__rO,this,true);
A.addListener(q,this.__rP,this);
A.addListener(x,this.__rR,this);
A.addListener(s,this.__rS,this);
A.addListener(o,this.__rQ,this);
var B=this.getContainerElement().getDomElement();

if(B==null){B=window;
}this.__rC=qx.event.Registration.getManager(B).getHandler(qx.event.handler.DragDrop);
},properties:{resizableTop:{check:k,init:true},resizableRight:{check:k,init:true},resizableBottom:{check:k,init:true},resizableLeft:{check:k,init:true},resizable:{group:[l,d,m,y],mode:v},resizeSensitivity:{check:a,init:5},useResizeFrame:{check:k,init:true}},members:{__rC:null,__rD:null,__rE:null,__rF:null,__rG:null,__rH:null,__rI:null,RESIZE_TOP:1,RESIZE_BOTTOM:2,RESIZE_LEFT:4,RESIZE_RIGHT:8,__rJ:function(){var C=this.__rD;

if(!C){C=this.__rD=new qx.ui.core.Widget();
C.setAppearance(p);
C.exclude();
qx.core.Init.getApplication().getRoot().add(C);
}return C;
},__rK:function(){var location=this.__ue();
var D=this.__rJ();
D.setUserBounds(location.left,location.top,location.right-location.left,location.bottom-location.top);
D.show();
D.setZIndex(this.getZIndex()+1);
},__rL:function(e){var F=this.__rE;
var G=this.getSizeHint();
var K=this.__rI;
var J=this.__rH;
var E=J.width;
var I=J.height;
var H=J.containerWidth;
var M=J.containerHeight;
var N=J.left;
var top=J.top;
var L;

if((F&this.RESIZE_TOP)||(F&this.RESIZE_BOTTOM)){L=Math.max(K.top,Math.min(K.bottom,e.getDocumentTop()))-this.__rG;

if(F&this.RESIZE_TOP){I-=L;
M-=L;
}else{I+=L;
M+=L;
}
if(M<G.minHeight){I+=(G.minHeight-M);
M=G.minHeight;
}else if(M>G.maxHeight){I-=(G.maxHeight-M);
M=G.maxHeight;
}
if(F&this.RESIZE_TOP){top+=J.containerHeight-M;
}}
if((F&this.RESIZE_LEFT)||(F&this.RESIZE_RIGHT)){L=Math.max(K.left,Math.min(K.right,e.getDocumentLeft()))-this.__rF;

if(F&this.RESIZE_LEFT){E-=L;
H-=L;
}else{E+=L;
H+=L;
}
if(H<G.minWidth){E+=(G.minWidth-H);
H=G.minWidth;
}else if(E>G.maxWidth){E-=(G.maxWidth-H);
H=G.maxWidth;
}
if(F&this.RESIZE_LEFT){N+=J.containerWidth-H;
}}return {viewportLeft:N,viewportTop:top,parentLeft:J.bounds.left+N-J.left,parentTop:J.bounds.top+top-J.top,containerWidth:H,containerHeight:M,width:E,height:I};
},__rM:{1:f,2:n,4:h,8:z,5:t,6:g,9:c,10:b},__ue:function(){var O=this.getDecoratorElement();
if(O&&O.getDomElement()){return qx.bom.element.Location.get(O.getDomElement());
}else{return this.getContentLocation();
}},__rN:function(e){var location=this.__ue();
var P=this.getResizeSensitivity();
var S=e.getDocumentLeft();
var R=e.getDocumentTop();
var Q=this.__uf(location,S,R,P);
if(Q>0){Q=Q|this.__uf(location,S,R,P*2);
}this.__rE=Q;
},__uf:function(location,T,U,V){var W=0;
if(this.getResizableTop()&&Math.abs(location.top-U)<V&&T>location.left-V&&T<location.right+V){W+=this.RESIZE_TOP;
}else if(this.getResizableBottom()&&Math.abs(location.bottom-U)<V&&T>location.left-V&&T<location.right+V){W+=this.RESIZE_BOTTOM;
}if(this.getResizableLeft()&&Math.abs(location.left-T)<V&&U>location.top-V&&U<location.bottom+V){W+=this.RESIZE_LEFT;
}else if(this.getResizableRight()&&Math.abs(location.right-T)<V&&U>location.top-V&&U<location.bottom+V){W+=this.RESIZE_RIGHT;
}return W;
},__rO:function(e){if(!this.__rE){return;
}this.addState(j);
this.__rF=e.getDocumentLeft();
this.__rG=e.getDocumentTop();
var bb=this.getContainerLocation();
var X=this.__ue();
var ba=this.getBounds();
this.__rH={top:X.top,left:X.left,containerWidth:bb.right-bb.left,containerHeight:bb.bottom-bb.top,width:X.right-X.left,height:X.bottom-X.top,bounds:qx.lang.Object.clone(ba)};
var parent=this.getLayoutParent();
var bc=parent.getContentLocation();
var Y=parent.getBounds();
this.__rI={left:bc.left,top:bc.top,right:bc.left+Y.width,bottom:bc.top+Y.height};
if(this.getUseResizeFrame()){this.__rK();
}this.capture();
e.stop();
},__rP:function(e){if(!this.hasState(j)){return;
}if(this.getUseResizeFrame()){this.__rJ().exclude();
}var bd=this.__rL(e);
this.setWidth(bd.containerWidth);
this.setHeight(bd.containerHeight);
if(this.getResizableLeft()||this.getResizableTop()){this.setLayoutProperties({left:bd.parentLeft,top:bd.parentTop});
}this.__rE=0;
this.removeState(j);
this.resetCursor();
this.getApplicationRoot().resetGlobalCursor();
this.releaseCapture();
e.stopPropagation();
},__rQ:function(e){if(!this.__rE){return;
}this.resetCursor();
this.getApplicationRoot().resetGlobalCursor();
this.removeState(w);
if(this.getUseResizeFrame()){this.__rJ().exclude();
}},__rR:function(e){if(this.hasState(j)){var bh=this.__rL(e);
if(this.getUseResizeFrame()){var bf=this.__rJ();
bf.setUserBounds(bh.viewportLeft,bh.viewportTop,bh.width,bh.height);
}else{this.setWidth(bh.containerWidth);
this.setHeight(bh.containerHeight);
if(this.getResizableLeft()||this.getResizableTop()){this.setLayoutProperties({left:bh.parentLeft,top:bh.parentTop});
}}e.stopPropagation();
}else if(!this.hasState(u)&&!this.__rC.isSessionActive()){this.__rN(e);
var bi=this.__rE;
var bg=this.getApplicationRoot();

if(bi){var be=this.__rM[bi];
this.setCursor(be);
bg.setGlobalCursor(be);
}else if(this.getCursor()){this.resetCursor();
bg.resetGlobalCursor();
}}},__rS:function(e){if(this.getCursor()&&!this.hasState(j)){this.resetCursor();
this.getApplicationRoot().resetGlobalCursor();
}}},destruct:function(){if(this.__rD!=null&&!qx.core.ObjectRegistry.inShutDown){this.__rD.destroy();
this.__rD=null;
}this.__rC=null;
}});
})();
(function(){var l="move",k="Boolean",j="__rU",i="mouseup",h="mousedown",g="losecapture",f="qx.ui.core.MMovable",d="mousemove",c="maximized",b="__rT",a="move-frame";
qx.Mixin.define(f,{properties:{movable:{check:k,init:true},useMoveFrame:{check:k,init:false}},members:{__rT:null,__rU:null,__rV:null,__rW:null,__rX:null,__rY:null,__sa:null,__sb:false,__sc:null,__sd:0,_activateMoveHandle:function(m){if(this.__rT){throw new Error("The move handle could not be redefined!");
}this.__rT=m;
m.addListener(h,this._onMoveMouseDown,this);
m.addListener(i,this._onMoveMouseUp,this);
m.addListener(d,this._onMoveMouseMove,this);
m.addListener(g,this.__sh,this);
},__se:function(){var n=this.__rU;

if(!n){n=this.__rU=new qx.ui.core.Widget();
n.setAppearance(a);
n.exclude();
qx.core.Init.getApplication().getRoot().add(n);
}return n;
},__sf:function(){var location=this.getContainerLocation();
var p=this.getBounds();
var o=this.__se();
o.setUserBounds(location.left,location.top,p.width,p.height);
o.show();
o.setZIndex(this.getZIndex()+1);
},__sg:function(e){var r=this.__rV;
var u=Math.max(r.left,Math.min(r.right,e.getDocumentLeft()));
var t=Math.max(r.top,Math.min(r.bottom,e.getDocumentTop()));
var q=this.__rW+u;
var s=this.__rX+t;
return {viewportLeft:q,viewportTop:s,parentLeft:q-this.__rY,parentTop:s-this.__sa};
},_onMoveMouseDown:function(e){if(!this.getMovable()||this.hasState(c)){return;
}var parent=this.getLayoutParent();
var w=parent.getContentLocation();
var x=parent.getBounds();
if(qx.Class.implementsInterface(parent,qx.ui.window.IDesktop)){if(!parent.isContentBlocked()){this.__sc=parent.getBlockerColor();
this.__sd=parent.getBlockerOpacity();
parent.setBlockerColor(null);
parent.setBlockerOpacity(1);
parent.blockContent(this.getZIndex()-1);
this.__sb=true;
}}this.__rV={left:w.left,top:w.top,right:w.left+x.width,bottom:w.top+x.height};
var v=this.getContainerLocation();
this.__rY=w.left;
this.__sa=w.top;
this.__rW=v.left-e.getDocumentLeft();
this.__rX=v.top-e.getDocumentTop();
this.addState(l);
this.__rT.capture();
if(this.getUseMoveFrame()){this.__sf();
}e.stop();
},_onMoveMouseMove:function(e){if(!this.hasState(l)){return;
}var y=this.__sg(e);

if(this.getUseMoveFrame()){this.__se().setDomPosition(y.viewportLeft,y.viewportTop);
}else{this.setDomPosition(y.parentLeft,y.parentTop);
}e.stopPropagation();
},_onMoveMouseUp:function(e){if(!this.hasState(l)){return;
}this.removeState(l);
var parent=this.getLayoutParent();

if(qx.Class.implementsInterface(parent,qx.ui.window.IDesktop)){if(this.__sb){parent.unblockContent();
parent.setBlockerColor(this.__sc);
parent.setBlockerOpacity(this.__sd);
this.__sc=null;
this.__sd=0;
this.__sb=false;
}}this.__rT.releaseCapture();
var z=this.__sg(e);
this.setLayoutProperties({left:z.parentLeft,top:z.parentTop});
if(this.getUseMoveFrame()){this.__se().exclude();
}e.stopPropagation();
},__sh:function(e){if(!this.hasState(l)){return;
}this.removeState(l);
if(this.getUseMoveFrame()){this.__se().exclude();
}}},destruct:function(){this._disposeObjects(j,b);
this.__rV=null;
}});
})();
(function(){var p="Integer",o="_applyContentPadding",n="resetPaddingRight",m="setPaddingBottom",l="resetPaddingTop",k="qx.ui.core.MContentPadding",j="resetPaddingLeft",i="setPaddingTop",h="setPaddingRight",g="resetPaddingBottom",c="contentPaddingLeft",f="setPaddingLeft",e="contentPaddingTop",b="shorthand",a="contentPaddingRight",d="contentPaddingBottom";
qx.Mixin.define(k,{properties:{contentPaddingTop:{check:p,init:0,apply:o,themeable:true},contentPaddingRight:{check:p,init:0,apply:o,themeable:true},contentPaddingBottom:{check:p,init:0,apply:o,themeable:true},contentPaddingLeft:{check:p,init:0,apply:o,themeable:true},contentPadding:{group:[e,a,d,c],mode:b,themeable:true}},members:{__nd:{contentPaddingTop:i,contentPaddingRight:h,contentPaddingBottom:m,contentPaddingLeft:f},__ne:{contentPaddingTop:l,contentPaddingRight:n,contentPaddingBottom:g,contentPaddingLeft:j},_applyContentPadding:function(q,r,name){var s=this._getContentPaddingTarget();

if(q==null){var t=this.__ne[name];
s[t]();
}else{var u=this.__nd[name];
s[u](q);
}}}});
})();
(function(){var k="Boolean",j="qx.event.type.Event",i="captionbar",h="_applyCaptionBarChange",g="maximize-button",f="restore-button",d="minimize-button",c="close-button",b="maximized",a="execute",R="pane",Q="title",P="icon",O="statusbar-text",N="statusbar",M="String",L="showStatusbar",K="normal",J="active",I="beforeClose",r="beforeMinimize",s="mousedown",p="changeStatus",q="changeIcon",n="excluded",o="dblclick",l="_applyActive",m="beforeRestore",t="minimize",u="changeModal",A="changeAlwaysOnTop",z="_applyShowStatusbar",C="_applyStatus",B="qx.ui.window.Window",E="changeCaption",D="focusout",w="beforeMaximize",H="maximize",G="restore",F="window",v="close",x="changeActive",y="minimized";
qx.Class.define(B,{extend:qx.ui.core.Widget,include:[qx.ui.core.MRemoteChildrenHandling,qx.ui.core.MRemoteLayoutHandling,qx.ui.core.MResizable,qx.ui.core.MMovable,qx.ui.core.MContentPadding],construct:function(S,T){qx.ui.core.Widget.call(this);
this._setLayout(new qx.ui.layout.VBox());
this._createChildControl(i);
this._createChildControl(R);
if(T!=null){this.setIcon(T);
}
if(S!=null){this.setCaption(S);
}this._updateCaptionBar();
this.addListener(s,this._onWindowMouseDown,this,true);
this.addListener(D,this._onWindowFocusOut,this);
qx.core.Init.getApplication().getRoot().add(this);
this.initVisibility();
qx.ui.core.FocusHandler.getInstance().addRoot(this);
},statics:{DEFAULT_MANAGER_CLASS:qx.ui.window.Manager},events:{"beforeClose":j,"close":j,"beforeMinimize":j,"minimize":j,"beforeMaximize":j,"maximize":j,"beforeRestore":j,"restore":j},properties:{appearance:{refine:true,init:F},visibility:{refine:true,init:n},focusable:{refine:true,init:true},active:{check:k,init:false,apply:l,event:x},alwaysOnTop:{check:k,init:false,event:A},modal:{check:k,init:false,event:u},caption:{apply:h,event:E,nullable:true},icon:{check:M,nullable:true,apply:h,event:q,themeable:true},status:{check:M,nullable:true,apply:C,event:p},showClose:{check:k,init:true,apply:h,themeable:true},showMaximize:{check:k,init:true,apply:h,themeable:true},showMinimize:{check:k,init:true,apply:h,themeable:true},allowClose:{check:k,init:true,apply:h},allowMaximize:{check:k,init:true,apply:h},allowMinimize:{check:k,init:true,apply:h},showStatusbar:{check:k,init:false,apply:z}},members:{__si:null,__sj:null,getChildrenContainer:function(){return this.getChildControl(R);
},_forwardStates:{active:true,maximized:true,showStatusbar:true},setLayoutParent:function(parent){{};
qx.ui.core.Widget.prototype.setLayoutParent.call(this,parent);
},_createChildControlImpl:function(U,V){var W;

switch(U){case N:W=new qx.ui.container.Composite(new qx.ui.layout.HBox());
this._add(W);
W.add(this.getChildControl(O));
break;
case O:W=new qx.ui.basic.Label();
W.setValue(this.getStatus());
break;
case R:W=new qx.ui.container.Composite();
this._add(W,{flex:1});
break;
case i:var Y=new qx.ui.layout.Grid();
Y.setRowFlex(0,1);
Y.setColumnFlex(1,1);
W=new qx.ui.container.Composite(Y);
this._add(W);
W.addListener(o,this._onCaptionMouseDblClick,this);
this._activateMoveHandle(W);
break;
case P:W=new qx.ui.basic.Image(this.getIcon());
this.getChildControl(i).add(W,{row:0,column:0});
break;
case Q:W=new qx.ui.basic.Label(this.getCaption());
W.setWidth(0);
W.setAllowGrowX(true);
var X=this.getChildControl(i);
X.add(W,{row:0,column:1});
break;
case d:W=new qx.ui.form.Button();
W.setFocusable(false);
W.addListener(a,this._onMinimizeButtonClick,this);
this.getChildControl(i).add(W,{row:0,column:2});
break;
case f:W=new qx.ui.form.Button();
W.setFocusable(false);
W.addListener(a,this._onRestoreButtonClick,this);
this.getChildControl(i).add(W,{row:0,column:3});
break;
case g:W=new qx.ui.form.Button();
W.setFocusable(false);
W.addListener(a,this._onMaximizeButtonClick,this);
this.getChildControl(i).add(W,{row:0,column:4});
break;
case c:W=new qx.ui.form.Button();
W.setFocusable(false);
W.addListener(a,this._onCloseButtonClick,this);
this.getChildControl(i).add(W,{row:0,column:6});
break;
}return W||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,U);
},_updateCaptionBar:function(){var bb;
var bc=this.getIcon();

if(bc){this.getChildControl(P).setSource(bc);
this._showChildControl(P);
}else{this._excludeChildControl(P);
}var ba=this.getCaption();

if(ba){this.getChildControl(Q).setValue(ba);
this._showChildControl(Q);
}else{this._excludeChildControl(Q);
}
if(this.getShowMinimize()){this._showChildControl(d);
bb=this.getChildControl(d);
this.getAllowMinimize()?bb.resetEnabled():bb.setEnabled(false);
}else{this._excludeChildControl(d);
}
if(this.getShowMaximize()){if(this.isMaximized()){this._showChildControl(f);
this._excludeChildControl(g);
}else{this._showChildControl(g);
this._excludeChildControl(f);
}bb=this.getChildControl(g);
this.getAllowMaximize()?bb.resetEnabled():bb.setEnabled(false);
}else{this._excludeChildControl(g);
this._excludeChildControl(f);
}
if(this.getShowClose()){this._showChildControl(c);
bb=this.getChildControl(c);
this.getAllowClose()?bb.resetEnabled():bb.setEnabled(false);
}else{this._excludeChildControl(c);
}},close:function(){if(!this.isVisible()){return;
}
if(this.fireNonBubblingEvent(I,qx.event.type.Event,[false,true])){this.hide();
this.fireEvent(v);
}},open:function(){this.show();
this.setActive(true);
this.focus();
},center:function(){var parent=this.getLayoutParent();

if(parent){var be=parent.getBounds();

if(be){var bf=this.getSizeHint();
var bd=Math.round((be.width-bf.width)/2);
var top=Math.round((be.height-bf.height)/2);

if(top<0){top=0;
}this.moveTo(bd,top);
return;
}}{};
},maximize:function(){if(this.isMaximized()){return;
}var parent=this.getLayoutParent();

if(parent!=null&&parent.supportsMaximize()){if(this.fireNonBubblingEvent(w,qx.event.type.Event,[false,true])){if(!this.isVisible()){this.open();
}var bg=this.getLayoutProperties();
this.__sj=bg.left===undefined?0:bg.left;
this.__si=bg.top===undefined?0:bg.top;
this.setLayoutProperties({left:null,top:null,edge:0});
this.addState(b);
this._updateCaptionBar();
this.fireEvent(H);
}}},minimize:function(){if(!this.isVisible()){return;
}
if(this.fireNonBubblingEvent(r,qx.event.type.Event,[false,true])){var bh=this.getLayoutProperties();
this.__sj=bh.left===undefined?0:bh.left;
this.__si=bh.top===undefined?0:bh.top;
this.removeState(b);
this.hide();
this.fireEvent(t);
}},restore:function(){if(this.getMode()===K){return;
}
if(this.fireNonBubblingEvent(m,qx.event.type.Event,[false,true])){if(!this.isVisible()){this.open();
}var bi=this.__sj;
var top=this.__si;
this.setLayoutProperties({edge:null,left:bi,top:top});
this.removeState(b);
this._updateCaptionBar();
this.fireEvent(G);
}},moveTo:function(bj,top){if(this.isMaximized()){return;
}this.setLayoutProperties({left:bj,top:top});
},isMaximized:function(){return this.hasState(b);
},getMode:function(){if(!this.isVisible()){return y;
}else{if(this.isMaximized()){return b;
}else{return K;
}}},_applyActive:function(bk,bl){if(bl){this.removeState(J);
}else{this.addState(J);
}},_getContentPaddingTarget:function(){return this.getChildControl(R);
},_applyShowStatusbar:function(bm,bn){bm?this.addState(L):this.removeState(L);

if(bm){this._showChildControl(N);
}else{this._excludeChildControl(N);
}},_applyCaptionBarChange:function(bo,bp){this._updateCaptionBar();
},_applyStatus:function(bq,br){var bs=this.getChildControl(O,true);

if(bs){bs.setValue(bq);
}},_onWindowEventStop:function(e){e.stopPropagation();
},_onWindowMouseDown:function(e){this.setActive(true);
},_onWindowFocusOut:function(e){if(this.getModal()){return;
}var bt=e.getRelatedTarget();

if(bt!=null&&!qx.ui.core.Widget.contains(this,bt)){this.setActive(false);
}},_onCaptionMouseDblClick:function(e){if(this.getAllowMaximize()){this.isMaximized()?this.restore():this.maximize();
}},_onMinimizeButtonClick:function(e){this.minimize();
this.getChildControl(d).reset();
},_onRestoreButtonClick:function(e){this.restore();
this.getChildControl(f).reset();
},_onMaximizeButtonClick:function(e){this.maximize();
this.getChildControl(g).reset();
},_onCloseButtonClick:function(e){this.close();
this.getChildControl(c).reset();
}}});
})();
(function(){var d='Reload',c="lino.TableWindow",b="Reload. tm = ",a='execute';
qx.Class.define(c,{extend:qx.ui.window.Window,construct:function(e){qx.ui.window.Window.call(this);
this.__ug=e;
this.__uz=this.createTable();
var toolbar=new qx.ui.toolbar.ToolBar();
var g=new qx.ui.toolbar.Part();
toolbar.add(g);
var f=new qx.ui.toolbar.Button(d);
f.addListener(a,function(){var h=this.__uz.getTableModel();
console.log(b,h);
h.reloadData();
},this);
g.add(f);
this.setupToolbar(g);
this.set({width:600,height:400,contentPadding:[0,0,0,0]});
this.setLayout(new qx.ui.layout.VBox());
this.add(toolbar);
this.add(this.__uz,{flex:1});
},members:{__ug:null,__uz:null,showWindow:function(i){this.__ug.showWindow(i);
},createTableModel:function(){throw new Error("createTableModel is abstract");
},setupToolbar:function(j){}},events:{}});
})();
(function(){var h='Detail',g="Land",f='ID',e='execute',d='Name',c='PLZ',b="lino.CountriesCitiesTable",a='/api/countries/Cities';
qx.Class.define(b,{extend:lino.TableWindow,members:{content_type:9,before_row_edit:function(i){},createTable:function(){var k=new lino.RemoteTableModel(this,a);
k.setColumns([g,d,c,f],[1,2,3,4]);
k.setColumnSortable(0,true);
k.setColumnEditable(0,true);
var j=new qx.ui.table.Table(k);
var l=j.getTableColumnModel();
l.setDataCellRenderer(0,new lino.ForeignKeyCellRenderer(0));
return j;
},setupToolbar:function(m){var n=new qx.ui.toolbar.Button(h);
n.addListener(e,function(){alert("TODO : how to referencethe app? want to open new window...");
},this);
m.add(n);
}}});
})();
(function(){var a="qx.ui.window.IDesktop";
qx.Interface.define(a,{members:{setWindowManager:function(b){this.assertInterface(b,qx.ui.window.IWindowManager);
},getWindows:function(){},supportsMaximize:function(){},blockContent:function(c){this.assertInteger(c);
},unblockContent:function(){},isContentBlocked:function(){}}});
})();
(function(){var r="left",q="top",p="_applyLayoutChange",o="hAlign",n="flex",m="vAlign",h="Integer",g="minWidth",f="width",e="minHeight",b="qx.ui.layout.Grid",d="height",c="maxHeight",a="maxWidth";
qx.Class.define(b,{extend:qx.ui.layout.Abstract,construct:function(s,t){qx.ui.layout.Abstract.call(this);
this.__lQ=[];
this.__lR=[];

if(s){this.setSpacingX(s);
}
if(t){this.setSpacingY(t);
}},properties:{spacingX:{check:h,init:0,apply:p},spacingY:{check:h,init:0,apply:p}},members:{__lS:null,__lQ:null,__lR:null,__lT:null,__lU:null,__lV:null,__lW:null,__lX:null,__lY:null,verifyLayoutProperty:null,__ma:function(){var B=[];
var A=[];
var C=[];
var w=-1;
var v=-1;
var E=this._getLayoutChildren();

for(var i=0,l=E.length;i<l;i++){var z=E[i];
var D=z.getLayoutProperties();
var F=D.row;
var u=D.column;
D.colSpan=D.colSpan||1;
D.rowSpan=D.rowSpan||1;
if(F==null||u==null){throw new Error("The layout properties 'row' and 'column' of the child widget '"+z+"' must be defined!");
}
if(B[F]&&B[F][u]){throw new Error("Cannot add widget '"+z+"'!. "+"There is already a widget '"+B[F][u]+"' in this cell ("+F+", "+u+")");
}
for(var x=u;x<u+D.colSpan;x++){for(var y=F;y<F+D.rowSpan;y++){if(B[y]==undefined){B[y]=[];
}B[y][x]=z;
v=Math.max(v,x);
w=Math.max(w,y);
}}
if(D.rowSpan>1){C.push(z);
}
if(D.colSpan>1){A.push(z);
}}for(var y=0;y<=w;y++){if(B[y]==undefined){B[y]=[];
}}this.__lS=B;
this.__lT=A;
this.__lU=C;
this.__lV=w;
this.__lW=v;
this.__lX=null;
this.__lY=null;
delete this._invalidChildrenCache;
},_setRowData:function(G,H,I){var J=this.__lQ[G];

if(!J){this.__lQ[G]={};
this.__lQ[G][H]=I;
}else{J[H]=I;
}},_setColumnData:function(K,L,M){var N=this.__lR[K];

if(!N){this.__lR[K]={};
this.__lR[K][L]=M;
}else{N[L]=M;
}},setSpacing:function(O){this.setSpacingY(O);
this.setSpacingX(O);
return this;
},setColumnAlign:function(P,Q,R){{};
this._setColumnData(P,o,Q);
this._setColumnData(P,m,R);
this._applyLayoutChange();
return this;
},getColumnAlign:function(S){var T=this.__lR[S]||{};
return {vAlign:T.vAlign||q,hAlign:T.hAlign||r};
},setRowAlign:function(U,V,W){{};
this._setRowData(U,o,V);
this._setRowData(U,m,W);
this._applyLayoutChange();
return this;
},getRowAlign:function(X){var Y=this.__lQ[X]||{};
return {vAlign:Y.vAlign||q,hAlign:Y.hAlign||r};
},getCellWidget:function(ba,bb){if(this._invalidChildrenCache){this.__ma();
}var ba=this.__lS[ba]||{};
return ba[bb]||null;
},getRowCount:function(){if(this._invalidChildrenCache){this.__ma();
}return this.__lV+1;
},getColumnCount:function(){if(this._invalidChildrenCache){this.__ma();
}return this.__lW+1;
},getCellAlign:function(bc,bd){var bj=q;
var bh=r;
var bi=this.__lQ[bc];
var bf=this.__lR[bd];
var be=this.__lS[bc][bd];

if(be){var bg={vAlign:be.getAlignY(),hAlign:be.getAlignX()};
}else{bg={};
}if(bg.vAlign){bj=bg.vAlign;
}else if(bi&&bi.vAlign){bj=bi.vAlign;
}else if(bf&&bf.vAlign){bj=bf.vAlign;
}if(bg.hAlign){bh=bg.hAlign;
}else if(bf&&bf.hAlign){bh=bf.hAlign;
}else if(bi&&bi.hAlign){bh=bi.hAlign;
}return {vAlign:bj,hAlign:bh};
},setColumnFlex:function(bk,bl){this._setColumnData(bk,n,bl);
this._applyLayoutChange();
return this;
},getColumnFlex:function(bm){var bn=this.__lR[bm]||{};
return bn.flex!==undefined?bn.flex:0;
},setRowFlex:function(bo,bp){this._setRowData(bo,n,bp);
this._applyLayoutChange();
return this;
},getRowFlex:function(bq){var br=this.__lQ[bq]||{};
var bs=br.flex!==undefined?br.flex:0;
return bs;
},setColumnMaxWidth:function(bt,bu){this._setColumnData(bt,a,bu);
this._applyLayoutChange();
return this;
},getColumnMaxWidth:function(bv){var bw=this.__lR[bv]||{};
return bw.maxWidth!==undefined?bw.maxWidth:Infinity;
},setColumnWidth:function(bx,by){this._setColumnData(bx,f,by);
this._applyLayoutChange();
return this;
},getColumnWidth:function(bz){var bA=this.__lR[bz]||{};
return bA.width!==undefined?bA.width:null;
},setColumnMinWidth:function(bB,bC){this._setColumnData(bB,g,bC);
this._applyLayoutChange();
return this;
},getColumnMinWidth:function(bD){var bE=this.__lR[bD]||{};
return bE.minWidth||0;
},setRowMaxHeight:function(bF,bG){this._setRowData(bF,c,bG);
this._applyLayoutChange();
return this;
},getRowMaxHeight:function(bH){var bI=this.__lQ[bH]||{};
return bI.maxHeight||Infinity;
},setRowHeight:function(bJ,bK){this._setRowData(bJ,d,bK);
this._applyLayoutChange();
return this;
},getRowHeight:function(bL){var bM=this.__lQ[bL]||{};
return bM.height!==undefined?bM.height:null;
},setRowMinHeight:function(bN,bO){this._setRowData(bN,e,bO);
this._applyLayoutChange();
return this;
},getRowMinHeight:function(bP){var bQ=this.__lQ[bP]||{};
return bQ.minHeight||0;
},__mb:function(bR){var bV=bR.getSizeHint();
var bU=bR.getMarginLeft()+bR.getMarginRight();
var bT=bR.getMarginTop()+bR.getMarginBottom();
var bS={height:bV.height+bT,width:bV.width+bU,minHeight:bV.minHeight+bT,minWidth:bV.minWidth+bU,maxHeight:bV.maxHeight+bT,maxWidth:bV.maxWidth+bU};
return bS;
},_fixHeightsRowSpan:function(bW){var ck=this.getSpacingY();

for(var i=0,l=this.__lU.length;i<l;i++){var ca=this.__lU[i];
var cc=this.__mb(ca);
var cd=ca.getLayoutProperties();
var bY=cd.row;
var ci=ck*(cd.rowSpan-1);
var bX=ci;
var cf={};

for(var j=0;j<cd.rowSpan;j++){var cm=cd.row+j;
var cb=bW[cm];
var cl=this.getRowFlex(cm);

if(cl>0){cf[cm]={min:cb.minHeight,value:cb.height,max:cb.maxHeight,flex:cl};
}ci+=cb.height;
bX+=cb.minHeight;
}if(ci<cc.height){if(!qx.lang.Object.isEmpty(cf)){var cj=qx.ui.layout.Util.computeFlexOffsets(cf,cc.height,ci);

for(var k=0;k<cd.rowSpan;k++){var ce=cj[bY+k]?cj[bY+k].offset:0;
bW[bY+k].height+=ce;
}}else{var cg=ck*(cd.rowSpan-1);
var ch=cc.height-cg;
var cb=Math.floor(ch/cd.rowSpan);

for(var k=0;k<cd.rowSpan;k++){bW[bY+k].height=cb;
}}}if(bX<cc.minHeight){var cj=qx.ui.layout.Util.computeFlexOffsets(cf,cc.minHeight,bX);

for(var j=0;j<cd.rowSpan;j++){var ce=cj[bY+j]?cj[bY+j].offset:0;
bW[bY+j].minHeight+=ce;
}}}},_fixWidthsColSpan:function(cn){var cr=this.getSpacingX();

for(var i=0,l=this.__lT.length;i<l;i++){var co=this.__lT[i];
var cq=this.__mb(co);
var ct=co.getLayoutProperties();
var cp=ct.column;
var cz=cr*(ct.colSpan-1);
var cs=cz;
var cu={};
var cw;

for(var j=0;j<ct.colSpan;j++){var cA=ct.column+j;
var cy=cn[cA];
var cx=this.getColumnFlex(cA);
if(cx>0){cu[cA]={min:cy.minWidth,value:cy.width,max:cy.maxWidth,flex:cx};
}cz+=cy.width;
cs+=cy.minWidth;
}if(cz<cq.width){var cv=qx.ui.layout.Util.computeFlexOffsets(cu,cq.width,cz);

for(var j=0;j<ct.colSpan;j++){cw=cv[cp+j]?cv[cp+j].offset:0;
cn[cp+j].width+=cw;
}}if(cs<cq.minWidth){var cv=qx.ui.layout.Util.computeFlexOffsets(cu,cq.minWidth,cs);

for(var j=0;j<ct.colSpan;j++){cw=cv[cp+j]?cv[cp+j].offset:0;
cn[cp+j].minWidth+=cw;
}}}},_getRowHeights:function(){if(this.__lX!=null){return this.__lX;
}var cK=[];
var cD=this.__lV;
var cC=this.__lW;

for(var cL=0;cL<=cD;cL++){var cE=0;
var cG=0;
var cF=0;

for(var cJ=0;cJ<=cC;cJ++){var cB=this.__lS[cL][cJ];

if(!cB){continue;
}var cH=cB.getLayoutProperties().rowSpan||0;

if(cH>1){continue;
}var cI=this.__mb(cB);

if(this.getRowFlex(cL)>0){cE=Math.max(cE,cI.minHeight);
}else{cE=Math.max(cE,cI.height);
}cG=Math.max(cG,cI.height);
}var cE=Math.max(cE,this.getRowMinHeight(cL));
var cF=this.getRowMaxHeight(cL);

if(this.getRowHeight(cL)!==null){var cG=this.getRowHeight(cL);
}else{var cG=Math.max(cE,Math.min(cG,cF));
}cK[cL]={minHeight:cE,height:cG,maxHeight:cF};
}
if(this.__lU.length>0){this._fixHeightsRowSpan(cK);
}this.__lX=cK;
return cK;
},_getColWidths:function(){if(this.__lY!=null){return this.__lY;
}var cQ=[];
var cN=this.__lW;
var cP=this.__lV;

for(var cV=0;cV<=cN;cV++){var cT=0;
var cS=0;
var cO=Infinity;

for(var cW=0;cW<=cP;cW++){var cM=this.__lS[cW][cV];

if(!cM){continue;
}var cR=cM.getLayoutProperties().colSpan||0;

if(cR>1){continue;
}var cU=this.__mb(cM);

if(this.getColumnFlex(cV)>0){cS=Math.max(cS,cU.minWidth);
}else{cS=Math.max(cS,cU.width);
}cT=Math.max(cT,cU.width);
}var cS=Math.max(cS,this.getColumnMinWidth(cV));
var cO=this.getColumnMaxWidth(cV);

if(this.getColumnWidth(cV)!==null){var cT=this.getColumnWidth(cV);
}else{var cT=Math.max(cS,Math.min(cT,cO));
}cQ[cV]={minWidth:cS,width:cT,maxWidth:cO};
}
if(this.__lT.length>0){this._fixWidthsColSpan(cQ);
}this.__lY=cQ;
return cQ;
},_getColumnFlexOffsets:function(cX){var cY=this.getSizeHint();
var dd=cX-cY.width;

if(dd==0){return {};
}var db=this._getColWidths();
var da={};

for(var i=0,l=db.length;i<l;i++){var de=db[i];
var dc=this.getColumnFlex(i);

if((dc<=0)||(de.width==de.maxWidth&&dd>0)||(de.width==de.minWidth&&dd<0)){continue;
}da[i]={min:de.minWidth,value:de.width,max:de.maxWidth,flex:dc};
}return qx.ui.layout.Util.computeFlexOffsets(da,cX,cY.width);
},_getRowFlexOffsets:function(df){var dg=this.getSizeHint();
var dj=df-dg.height;

if(dj==0){return {};
}var dk=this._getRowHeights();
var dh={};

for(var i=0,l=dk.length;i<l;i++){var dl=dk[i];
var di=this.getRowFlex(i);

if((di<=0)||(dl.height==dl.maxHeight&&dj>0)||(dl.height==dl.minHeight&&dj<0)){continue;
}dh[i]={min:dl.minHeight,value:dl.height,max:dl.maxHeight,flex:di};
}return qx.ui.layout.Util.computeFlexOffsets(dh,df,dg.height);
},renderLayout:function(dm,dn){if(this._invalidChildrenCache){this.__ma();
}var dC=qx.ui.layout.Util;
var dq=this.getSpacingX();
var dw=this.getSpacingY();
var dH=this._getColWidths();
var dG=this._getColumnFlexOffsets(dm);
var dr=[];
var dJ=this.__lW;
var dp=this.__lV;
var dI;

for(var dK=0;dK<=dJ;dK++){dI=dG[dK]?dG[dK].offset:0;
dr[dK]=dH[dK].width+dI;
}var dz=this._getRowHeights();
var dB=this._getRowFlexOffsets(dn);
var dQ=[];

for(var dx=0;dx<=dp;dx++){dI=dB[dx]?dB[dx].offset:0;
dQ[dx]=dz[dx].height+dI;
}var dR=0;

for(var dK=0;dK<=dJ;dK++){var top=0;

for(var dx=0;dx<=dp;dx++){var dE=this.__lS[dx][dK];
if(!dE){top+=dQ[dx]+dw;
continue;
}var ds=dE.getLayoutProperties();
if(ds.row!==dx||ds.column!==dK){top+=dQ[dx]+dw;
continue;
}var dP=dq*(ds.colSpan-1);

for(var i=0;i<ds.colSpan;i++){dP+=dr[dK+i];
}var dF=dw*(ds.rowSpan-1);

for(var i=0;i<ds.rowSpan;i++){dF+=dQ[dx+i];
}var dt=dE.getSizeHint();
var dN=dE.getMarginTop();
var dD=dE.getMarginLeft();
var dA=dE.getMarginBottom();
var dv=dE.getMarginRight();
var dy=Math.max(dt.minWidth,Math.min(dP-dD-dv,dt.maxWidth));
var dO=Math.max(dt.minHeight,Math.min(dF-dN-dA,dt.maxHeight));
var dL=this.getCellAlign(dx,dK);
var dM=dR+dC.computeHorizontalAlignOffset(dL.hAlign,dy,dP,dD,dv);
var du=top+dC.computeVerticalAlignOffset(dL.vAlign,dO,dF,dN,dA);
dE.renderLayout(dM,du,dy,dO);
top+=dQ[dx]+dw;
}dR+=dr[dK]+dq;
}},invalidateLayoutCache:function(){qx.ui.layout.Abstract.prototype.invalidateLayoutCache.call(this);
this.__lY=null;
this.__lX=null;
},_computeSizeHint:function(){if(this._invalidChildrenCache){this.__ma();
}var dW=this._getColWidths();
var dY=0,ea=0;

for(var i=0,l=dW.length;i<l;i++){var eb=dW[i];

if(this.getColumnFlex(i)>0){dY+=eb.minWidth;
}else{dY+=eb.width;
}ea+=eb.width;
}var ec=this._getRowHeights();
var dU=0,dX=0;

for(var i=0,l=ec.length;i<l;i++){var ed=ec[i];

if(this.getRowFlex(i)>0){dU+=ed.minHeight;
}else{dU+=ed.height;
}dX+=ed.height;
}var dT=this.getSpacingX()*(dW.length-1);
var dS=this.getSpacingY()*(ec.length-1);
var dV={minWidth:dY+dT,width:ea+dT,minHeight:dU+dS,height:dX+dS};
return dV;
}},destruct:function(){this.__lS=this.__lQ=this.__lR=this.__lT=this.__lU=this.__lY=this.__lX=null;
}});
})();
(function(){var e="inherit",d="toolbar-button",c="keydown",b="qx.ui.toolbar.Button",a="keyup";
qx.Class.define(b,{extend:qx.ui.form.Button,construct:function(f,g,h){qx.ui.form.Button.call(this,f,g,h);
this.removeListener(c,this._onKeyDown);
this.removeListener(a,this._onKeyUp);
},properties:{appearance:{refine:true,init:d},show:{refine:true,init:e},focusable:{refine:true,init:false}}});
})();
(function(){var c="qx.event.type.Data",b="qx.event.type.Event",a="qx.ui.table.ITableModel";
qx.Interface.define(a,{events:{"dataChanged":c,"metaDataChanged":b,"sorted":c},members:{getRowCount:function(){},getRowData:function(d){},getColumnCount:function(){},getColumnId:function(e){},getColumnIndexById:function(f){},getColumnName:function(g){},isColumnEditable:function(h){},isColumnSortable:function(i){},sortByColumn:function(j,k){},getSortColumnIndex:function(){},isSortAscending:function(){},prefetchRows:function(l,m){},getValue:function(n,o){},getValueById:function(p,q){},setValue:function(r,s,t){},setValueById:function(u,v,w){}}});
})();
(function(){var e="metaDataChanged",d="qx.event.type.Data",c="qx.event.type.Event",b="abstract",a="qx.ui.table.model.Abstract";
qx.Class.define(a,{type:b,extend:qx.core.Object,implement:qx.ui.table.ITableModel,events:{"dataChanged":d,"metaDataChanged":c,"sorted":d},construct:function(){qx.core.Object.call(this);
this.__oU=[];
this.__oV=[];
this.__oW={};
},members:{__oU:null,__oV:null,__oW:null,__oX:null,init:function(f){},getRowCount:function(){throw new Error("getRowCount is abstract");
},getRowData:function(g){return null;
},isColumnEditable:function(h){return false;
},isColumnSortable:function(j){return false;
},sortByColumn:function(k,l){},getSortColumnIndex:function(){return -1;
},isSortAscending:function(){return true;
},prefetchRows:function(m,n){},getValue:function(o,p){throw new Error("getValue is abstract");
},getValueById:function(q,r){return this.getValue(this.getColumnIndexById(q),r);
},setValue:function(s,t,u){throw new Error("setValue is abstract");
},setValueById:function(v,w,x){this.setValue(this.getColumnIndexById(v),w,x);
},getColumnCount:function(){return this.__oU.length;
},getColumnIndexById:function(y){return this.__oW[y];
},getColumnId:function(z){return this.__oU[z];
},getColumnName:function(A){return this.__oV[A];
},setColumnIds:function(B){this.__oU=B;
this.__oW={};

for(var i=0;i<B.length;i++){this.__oW[B[i]]=i;
}this.__oV=new Array(B.length);
if(!this.__oX){this.fireEvent(e);
}},setColumnNamesByIndex:function(C){if(this.__oU.length!=C.length){throw new Error("this.__columnIdArr and columnNameArr have different length: "+this.__oU.length+" != "+C.length);
}this.__oV=C;
this.fireEvent(e);
},setColumnNamesById:function(D){this.__oV=new Array(this.__oU.length);

for(var i=0;i<this.__oU.length;++i){this.__oV[i]=D[this.__oU[i]];
}},setColumns:function(E,F){var G=this.__oU.length==0||F;

if(F==null){if(this.__oU.length==0){F=E;
}else{F=this.__oU;
}}
if(F.length!=E.length){throw new Error("columnIdArr and columnNameArr have different length: "+F.length+" != "+E.length);
}
if(G){this.__oX=true;
this.setColumnIds(F);
this.__oX=false;
}this.setColumnNamesByIndex(E);
}},destruct:function(){this.__oU=this.__oV=this.__oW=null;
}});
})();
(function(){var e="dataChanged",d="metaDataChanged",c="Integer",b="Boolean",a="qx.ui.table.model.Remote";
qx.Class.define(a,{extend:qx.ui.table.model.Abstract,construct:function(){qx.ui.table.model.Abstract.call(this);
this.__uj=-1;
this.__uk=true;
this.__ul=-1;
this.__um=0;
this.__un=-1;
this.__uo=-1;
this.__up=-1;
this.__uq=false;
this.__ur={};
this.__us=0;
this.__ut=null;
this.__uu=null;
},properties:{blockSize:{check:c,init:50},maxCachedBlockCount:{check:c,init:15},clearCacheOnRemove:{check:b,init:false},blockConcurrentLoadRowCount:{check:b,init:true}},members:{__ul:null,__uq:null,__um:null,__un:null,__uo:null,__up:null,__ur:null,__us:null,__uj:null,__uk:null,__uu:null,__ut:null,__uv:false,_getIgnoreCurrentRequest:function(){return this.__uq;
},getRowCount:function(){if(this.__ul==-1){if(!this.__uv||!this.getBlockConcurrentLoadRowCount()){this.__uv=true;
this._loadRowCount();
}return (this.__ul==-1)?0:this.__ul;
}else{return this.__ul;
}},_loadRowCount:function(){throw new Error("_loadRowCount is abstract");
},_onRowCountLoaded:function(f){if(this.getBlockConcurrentLoadRowCount()){this.__uv=false;
}if(f==null||f<0){f=0;
}this.__ul=Number(f);
var g={firstRow:0,lastRow:f-1,firstColumn:0,lastColumn:this.getColumnCount()-1};
this.fireDataEvent(e,g);
},reloadData:function(){this.clearCache();
if(this.__un!=-1){var h=this._cancelCurrentRequest();

if(h){this.__un=-1;
this.__uq=false;
}else{this.__uq=true;
}}this.__uo=-1;
this.__up=-1;
this.__uv=true;
this._loadRowCount();
},clearCache:function(){this.__ur={};
this.__us=0;
},getCacheContent:function(){return {sortColumnIndex:this.__uj,sortAscending:this.__uk,rowCount:this.__ul,lruCounter:this.__um,rowBlockCache:this.__ur,rowBlockCount:this.__us};
},restoreCacheContent:function(j){if(this.__un!=-1){var k=this._cancelCurrentRequest();

if(k){this.__un=-1;
this.__uq=false;
}else{this.__uq=true;
}}this.__uj=j.sortColumnIndex;
this.__uk=j.sortAscending;
this.__ul=j.rowCount;
this.__um=j.lruCounter;
this.__ur=j.rowBlockCache;
this.__us=j.rowBlockCount;
var l={firstRow:0,lastRow:this.__ul-1,firstColumn:0,lastColumn:this.getColumnCount()-1};
this.fireDataEvent(e,l);
},_cancelCurrentRequest:function(){return false;
},iterateCachedRows:function(m,n){var p=this.getBlockSize();
var o=Math.ceil(this.getRowCount()/p);
for(var w=0;w<=o;w++){var q=this.__ur[w];

if(q!=null){var v=w*p;
var u=q.rowDataArr;

for(var t=0;t<u.length;t++){var s=u[t];
var r=m.call(n,v+t,s);

if(r!=null){u[t]=r;
}}}}},prefetchRows:function(x,y){if(this.__un==-1){var z=this.getBlockSize();
var E=Math.ceil(this.__ul/z);
var D=parseInt(x/z,10)-1;

if(D<0){D=0;
}var C=parseInt(y/z,10)+1;

if(C>=E){C=E-1;
}var B=-1;
var A=-1;

for(var F=D;F<=C;F++){if(this.__ur[F]==null||this.__ur[F].isDirty){if(B==-1){B=F;
}A=F;
}}if(B!=-1){this.__uo=-1;
this.__up=-1;
this.__un=B;
this._loadRowData(B*z,(A+1)*z-1);
}}else{this.__uo=x;
this.__up=y;
}},_loadRowData:function(G,H){throw new Error("_loadRowCount is abstract");
},_onRowDataLoaded:function(I){if(I!=null&&!this.__uq){var L=this.getBlockSize();
var J=Math.ceil(I.length/L);

if(J==1){this._setRowBlockData(this.__un,I);
}else{for(var i=0;i<J;i++){var O=i*L;
var N=[];
var K=Math.min(L,I.length-O);

for(var P=0;P<K;P++){N.push(I[O+P]);
}this._setRowBlockData(this.__un+i,N);
}}var M={firstRow:this.__un*L,lastRow:(this.__un+J+1)*L-1,firstColumn:0,lastColumn:this.getColumnCount()-1};
this.fireDataEvent(e,M);
}this.__un=-1;
this.__uq=false;
if(this.__uo!=-1){this.prefetchRows(this.__uo,this.__up);
}},_setRowBlockData:function(Q,R){if(this.__ur[Q]==null){this.__us++;

while(this.__us>this.getMaxCachedBlockCount()){var V;
var U=this.__um;

for(var T in this.__ur){var S=this.__ur[T].lru;

if(S<U&&T>1){U=S;
V=T;
}}delete this.__ur[V];
this.__us--;
}}this.__ur[Q]={lru:++this.__um,rowDataArr:R};
},removeRow:function(W){if(this.getClearCacheOnRemove()){this.clearCache();
var be={firstRow:0,lastRow:this.getRowCount()-1,firstColumn:0,lastColumn:this.getColumnCount()-1};
this.fireDataEvent(e,be);
}else{var ba=this.getBlockSize();
var bb=Math.ceil(this.getRowCount()/ba);
var bc=parseInt(W/ba,10);
for(var bf=bc;bf<=bb;bf++){var X=this.__ur[bf];

if(X!=null){var Y=0;

if(bf==bc){Y=W-bf*ba;
}X.rowDataArr.splice(Y,1);

if(bf==bb-1){if(X.rowDataArr.length==0){delete this.__ur[bf];
}}else{var bd=this.__ur[bf+1];

if(bd!=null){X.rowDataArr.push(bd.rowDataArr[0]);
}else{X.isDirty=true;
}}}}
if(this.__ul!=-1){this.__ul--;
}if(this.hasListener(e)){var be={firstRow:W,lastRow:this.getRowCount()-1,firstColumn:0,lastColumn:this.getColumnCount()-1};
this.fireDataEvent(e,be);
}}},getRowData:function(bg){var bh=this.getBlockSize();
var bk=parseInt(bg/bh,10);
var bi=this.__ur[bk];

if(bi==null){return null;
}else{var bj=bi.rowDataArr[bg-(bk*bh)];
if(bi.lru!=this.__um){bi.lru=++this.__um;
}return bj;
}},getValue:function(bl,bm){var bn=this.getRowData(bm);

if(bn==null){return null;
}else{var bo=this.getColumnId(bl);
return bn[bo];
}},setValue:function(bp,bq,br){var bs=this.getRowData(bq);

if(bs==null){return ;
}else{var bu=this.getColumnId(bp);
bs[bu]=br;
if(this.hasListener(e)){var bt={firstRow:bq,lastRow:bq,firstColumn:bp,lastColumn:bp};
this.fireDataEvent(e,bt);
}}},setEditable:function(bv){this.__uu=[];

for(var bw=0;bw<this.getColumnCount();bw++){this.__uu[bw]=bv;
}this.fireEvent(d);
},setColumnEditable:function(bx,by){if(by!=this.isColumnEditable(bx)){if(this.__uu==null){this.__uu=[];
}this.__uu[bx]=by;
this.fireEvent(d);
}},isColumnEditable:function(bz){return (this.__uu?(this.__uu[bz]==true):false);
},setColumnSortable:function(bA,bB){if(bB!=this.isColumnSortable(bA)){if(this.__ut==null){this.__ut=[];
}this.__ut[bA]=bB;
this.fireEvent(d);
}},isColumnSortable:function(bC){return (this.__ut?(this.__ut[bC]!==false):true);
},sortByColumn:function(bD,bE){if(this.__uj!=bD||this.__uk!=bE){this.__uj=bD;
this.__uk=bE;
this.clearCache();
this.fireEvent(d);
}},getSortColumnIndex:function(){return this.__uj;
},isSortAscending:function(){return this.__uk;
},setSortColumnIndexWithoutSortingData:function(bF){this.__uj=bF;
},setSortAscendingWithoutSortingData:function(bG){this.__uk=bG;
}},destruct:function(){this.__ut=this.__uu=this.__ur=null;
}});
})();
(function(){var i='_loadRowData() got',h="&limit=",g="?fmt=json&offset=",f="application/json",d="completed",c="?fmt=json&offset=0&limit=0",b="GET",a='lino.RemoteTableModel';
qx.Class.define(a,{extend:qx.ui.table.model.Remote,construct:function(window,j){qx.ui.table.model.Remote.call(this);
this.__uw=j;
this.__uA=window;
},members:{__uw:null,__uA:null,_loadRowCount:function(){var k=this.__uw+c;
this.__ux(k,function(e){var l=e.getContent();

if(l){this._onRowCountLoaded(l.count);
this.__uA.setCaption(l.title);
}});
},_loadRowData:function(m,n){var o=this.__uw+g+m+h+(n-m);
this.__ux(o,function(e){var p=e.getContent();
console.log(i,p);
this._onRowDataLoaded(p.rows);
});
},__ux:function(q,r){var s=new qx.io.remote.Request(q,b,f);
s.addListener(d,r,this);
s.send();
}}});
})();
(function(){var k="Boolean",j="qx.event.type.Event",i="queued",h="String",g="sending",f="receiving",d="aborted",c="failed",b="nocache",a="completed",P="qx.io.remote.Response",O="POST",N="configured",M="timeout",L="GET",K="Pragma",J="no-url-params-on-post",I="PUT",H="no-cache",G="Cache-Control",r="Content-Type",s="text/plain",p="application/xml",q="application/json",n="text/html",o="application/x-www-form-urlencoded",l="qx.io.remote.Exchange",m="Integer",t="X-Qooxdoo-Response-Type",u="HEAD",y="qx.io.remote.Request",x="_applyResponseType",A="_applyState",z="text/javascript",C="changeState",B="_applyProhibitCaching",w="",F="_applyMethod",E="DELETE",D="boolean";
qx.Class.define(y,{extend:qx.core.Object,construct:function(Q,R,S){qx.core.Object.call(this);
this.__st={};
this.__su={};
this.__sv={};
this.__sw={};

if(Q!==undefined){this.setUrl(Q);
}
if(R!==undefined){this.setMethod(R);
}
if(S!==undefined){this.setResponseType(S);
}this.setProhibitCaching(true);
this.__sx=++qx.io.remote.Request.__sx;
},events:{"created":j,"configured":j,"sending":j,"receiving":j,"completed":P,"aborted":j,"failed":P,"timeout":P},statics:{__sx:0,methodAllowsRequestBody:function(T){return (T==O)||(T==I);
}},properties:{url:{check:h,init:w},method:{check:[L,O,I,u,E],apply:F,init:L},asynchronous:{check:k,init:true},data:{check:h,nullable:true},username:{check:h,nullable:true},password:{check:h,nullable:true},state:{check:[N,i,g,f,a,d,M,c],init:N,apply:A,event:C},responseType:{check:[s,z,q,p,n],init:s,apply:x},timeout:{check:m,nullable:true},prohibitCaching:{check:function(v){return typeof v==D||v===J;
},init:true,apply:B},crossDomain:{check:k,init:false},fileUpload:{check:k,init:false},transport:{check:l,nullable:true},useBasicHttpAuth:{check:k,init:false},parseJson:{check:k,init:true}},members:{__st:null,__su:null,__sv:null,__sw:null,__sx:null,send:function(){qx.io.remote.RequestQueue.getInstance().add(this);
},abort:function(){qx.io.remote.RequestQueue.getInstance().abort(this);
},reset:function(){switch(this.getState()){case g:case f:this.error("Aborting already sent request!");
case i:this.abort();
break;
}},isConfigured:function(){return this.getState()===N;
},isQueued:function(){return this.getState()===i;
},isSending:function(){return this.getState()===g;
},isReceiving:function(){return this.getState()===f;
},isCompleted:function(){return this.getState()===a;
},isAborted:function(){return this.getState()===d;
},isTimeout:function(){return this.getState()===M;
},isFailed:function(){return this.getState()===c;
},__sy:qx.event.GlobalError.observeMethod(function(e){var U=e.clone();
U.setTarget(this);
this.dispatchEvent(U);
}),_onqueued:function(e){this.setState(i);
this.__sy(e);
},_onsending:function(e){this.setState(g);
this.__sy(e);
},_onreceiving:function(e){this.setState(f);
this.__sy(e);
},_oncompleted:function(e){this.setState(a);
this.__sy(e);
this.dispose();
},_onaborted:function(e){this.setState(d);
this.__sy(e);
this.dispose();
},_ontimeout:function(e){this.setState(M);
this.__sy(e);
this.dispose();
},_onfailed:function(e){this.setState(c);
this.__sy(e);
this.dispose();
},_applyState:function(V,W){{};
},_applyProhibitCaching:function(X,Y){if(!X){this.removeParameter(b);
this.removeRequestHeader(K);
this.removeRequestHeader(G);
return;
}if(X!==J||this.getMethod()!=O){this.setParameter(b,new Date().valueOf());
}else{this.removeParameter(b);
}this.setRequestHeader(K,H);
this.setRequestHeader(G,H);
},_applyMethod:function(ba,bb){if(qx.io.remote.Request.methodAllowsRequestBody(ba)){this.setRequestHeader(r,o);
}else{this.removeRequestHeader(r);
}var bc=this.getProhibitCaching();
this._applyProhibitCaching(bc,bc);
},_applyResponseType:function(bd,be){this.setRequestHeader(t,bd);
},setRequestHeader:function(bf,bg){this.__st[bf]=bg;
},removeRequestHeader:function(bh){delete this.__st[bh];
},getRequestHeader:function(bi){return this.__st[bi]||null;
},getRequestHeaders:function(){return this.__st;
},setParameter:function(bj,bk,bl){if(bl){this.__sv[bj]=bk;
}else{this.__su[bj]=bk;
}},removeParameter:function(bm,bn){if(bn){delete this.__sv[bm];
}else{delete this.__su[bm];
}},getParameter:function(bo,bp){if(bp){return this.__sv[bo]||null;
}else{return this.__su[bo]||null;
}},getParameters:function(bq){return (bq?this.__sv:this.__su);
},setFormField:function(br,bs){this.__sw[br]=bs;
},removeFormField:function(bt){delete this.__sw[bt];
},getFormField:function(bu){return this.__sw[bu]||null;
},getFormFields:function(){return this.__sw;
},getSequenceNumber:function(){return this.__sx;
}},destruct:function(){this.setTransport(null);
this.__st=this.__su=this.__sv=this.__sw=null;
}});
})();
(function(){var b=".",a="qx.bom.client.Transport";
qx.Class.define(a,{statics:{getMaxConcurrentRequestCount:function(){var h;
var c=qx.bom.client.Engine;
var g=c.FULLVERSION.split(b);
var e=0;
var d=0;
var f=0;
if(g[0]){e=g[0];
}if(g[1]){d=g[1];
}if(g[2]){f=g[2];
}if(window.maxConnectionsPerServer){h=window.maxConnectionsPerServer;
}else if(c.OPERA){h=8;
}else if(c.WEBKIT){h=4;
}else if(c.GECKO&&((e>1)||((e==1)&&(d>9))||((e==1)&&(d==9)&&(f>=1)))){h=6;
}else{h=2;
}return h;
}}});
})();
(function(){var s="Integer",r="aborted",q="_onaborted",p="__sA",o="_on",n="_applyEnabled",m="Boolean",l="sending",k="interval",j="__sC",c="failed",h="qx.io.remote.RequestQueue",g="timeout",b="completed",a="queued",f="receiving",d="singleton";
qx.Class.define(h,{type:d,extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__sz=[];
this.__sA=[];
this.__sB=0;
this.__sC=new qx.event.Timer(500);
this.__sC.addListener(k,this._oninterval,this);
},properties:{enabled:{init:true,check:m,apply:n},maxTotalRequests:{check:s,nullable:true},maxConcurrentRequests:{check:s,init:qx.bom.client.Transport.getMaxConcurrentRequestCount()},defaultTimeout:{check:s,init:5000}},members:{__sz:null,__sA:null,__sB:null,__sC:null,getRequestQueue:function(){return this.__sz;
},getActiveQueue:function(){return this.__sA;
},_debug:function(){var t;
{};
},_check:function(){this._debug();
if(this.__sA.length==0&&this.__sz.length==0){this.__sC.stop();
}if(!this.getEnabled()){return;
}if(this.__sz.length==0||(this.__sz[0].isAsynchronous()&&this.__sA.length>=this.getMaxConcurrentRequests())){return;
}if(this.getMaxTotalRequests()!=null&&this.__sB>=this.getMaxTotalRequests()){return;
}var u=this.__sz.shift();
var v=new qx.io.remote.Exchange(u);
this.__sB++;
this.__sA.push(v);
this._debug();
v.addListener(l,this._onsending,this);
v.addListener(f,this._onreceiving,this);
v.addListener(b,this._oncompleted,this);
v.addListener(r,this._oncompleted,this);
v.addListener(g,this._oncompleted,this);
v.addListener(c,this._oncompleted,this);
v._start=(new Date).valueOf();
v.send();
if(this.__sz.length>0){this._check();
}},_remove:function(w){qx.lang.Array.remove(this.__sA,w);
w.dispose();
this._check();
},__sD:0,_onsending:function(e){{};
e.getTarget().getRequest()._onsending(e);
},_onreceiving:function(e){e.getTarget().getRequest()._onreceiving(e);
},_oncompleted:function(e){{};
var y=e.getTarget().getRequest();
var x=o+e.getType();
try{if(y[x]){y[x](e);
}}catch(z){this.error("Request "+y+" handler "+x+" threw an error: ",z);
try{if(y[q]){var event=qx.event.Registration.createEvent(r,qx.event.type.Event);
y[q](event);
}}catch(A){}}finally{this._remove(e.getTarget());
}},_oninterval:function(e){var H=this.__sA;

if(H.length==0){this.__sC.stop();
return;
}var C=(new Date).valueOf();
var F;
var D;
var G=this.getDefaultTimeout();
var E;
var B;

for(var i=H.length-1;i>=0;i--){F=H[i];
D=F.getRequest();

if(D.isAsynchronous()){E=D.getTimeout();
if(E==0){continue;
}
if(E==null){E=G;
}B=C-F._start;

if(B>E){this.warn("Timeout: transport "+F.toHashCode());
this.warn(B+"ms > "+E+"ms");
F.timeout();
}}}},_applyEnabled:function(I,J){if(I){this._check();
}this.__sC.setEnabled(I);
},add:function(K){K.setState(a);

if(K.isAsynchronous()){this.__sz.push(K);
}else{this.__sz.unshift(K);
}this._check();

if(this.getEnabled()){this.__sC.start();
}},abort:function(L){var M=L.getTransport();

if(M){M.abort();
}else if(qx.lang.Array.contains(this.__sz,L)){qx.lang.Array.remove(this.__sz,L);
}}},destruct:function(){this._disposeArray(p);
this._disposeObjects(j);
this.__sz=null;
}});
})();
(function(){var o="failed",n="sending",m="completed",k="receiving",j="aborted",h="timeout",g="qx.event.type.Event",f="Connection dropped",d="qx.io.remote.Response",c="=",bp="configured",bo="&",bn="Unknown status code. ",bm="qx.io.remote.transport.XmlHttp",bl="qx.io.remote.transport.Abstract",bk="Request-URL too large",bj="MSHTML-specific HTTP status code",bi="Not available",bh="Precondition failed",bg="Server error",v="Moved temporarily",w="qx.io.remote.Exchange",t="Possibly due to a cross-domain request?",u="Bad gateway",r="Gone",s="See other",p="Partial content",q="Server timeout",B="qx.io.remote.transport.Script",C="HTTP version not supported",L="Unauthorized",I="Possibly due to application URL using 'file:' protocol?",T="Multiple choices",O="Payment required",bc="Not implemented",Y="Proxy authentication required",E="Length required",bf="_applyState",be="changeState",bd="Not modified",D="qx.io.remote.Request",G="Connection closed by server",H="Moved permanently",K="_applyImplementation",M="",P="Method not allowed",V="Forbidden",bb="Use proxy",x="Ok",y="Conflict",F="Not found",S="Not acceptable",R="Request time-out",Q="Bad request",X="No content",W="file:",N="qx.io.remote.transport.Iframe",U="Request entity too large",a="Unknown status code",ba="Unsupported media type",z="Gateway time-out",A="created",J="Out of resources",b="undefined";
qx.Class.define(w,{extend:qx.core.Object,construct:function(bq){qx.core.Object.call(this);
this.setRequest(bq);
bq.setTransport(this);
},events:{"sending":g,"receiving":g,"completed":d,"aborted":g,"failed":d,"timeout":d},statics:{typesOrder:[bm,N,B],typesReady:false,typesAvailable:{},typesSupported:{},registerType:function(br,bs){qx.io.remote.Exchange.typesAvailable[bs]=br;
},initTypes:function(){if(qx.io.remote.Exchange.typesReady){return;
}
for(var bu in qx.io.remote.Exchange.typesAvailable){var bt=qx.io.remote.Exchange.typesAvailable[bu];

if(bt.isSupported()){qx.io.remote.Exchange.typesSupported[bu]=bt;
}}qx.io.remote.Exchange.typesReady=true;

if(qx.lang.Object.isEmpty(qx.io.remote.Exchange.typesSupported)){throw new Error("No supported transport types were found!");
}},canHandle:function(bv,bw,bx){if(!qx.lang.Array.contains(bv.handles.responseTypes,bx)){return false;
}
for(var by in bw){if(!bv.handles[by]){return false;
}}return true;
},_nativeMap:{0:A,1:bp,2:n,3:k,4:m},wasSuccessful:function(bz,bA,bB){if(bB){switch(bz){case null:case 0:return true;
case -1:return bA<4;
default:return typeof bz===b;
}}else{switch(bz){case -1:{};
return bA<4;
case 200:case 304:return true;
case 201:case 202:case 203:case 204:case 205:return true;
case 206:{};
return bA!==4;
case 300:case 301:case 302:case 303:case 305:case 400:case 401:case 402:case 403:case 404:case 405:case 406:case 407:case 408:case 409:case 410:case 411:case 412:case 413:case 414:case 415:case 500:case 501:case 502:case 503:case 504:case 505:{};
return false;
case 12002:case 12007:case 12029:case 12030:case 12031:case 12152:case 13030:{};
return false;
default:if(bz>206&&bz<300){return true;
}qx.log.Logger.debug(this,"Unknown status code: "+bz+" ("+bA+")");
return false;
}}},statusCodeToString:function(bC){switch(bC){case -1:return bi;
case 0:var bD=window.location.href;
if(qx.lang.String.startsWith(bD.toLowerCase(),W)){return (bn+I);
}else{return (bn+t);
}break;
case 200:return x;
case 304:return bd;
case 206:return p;
case 204:return X;
case 300:return T;
case 301:return H;
case 302:return v;
case 303:return s;
case 305:return bb;
case 400:return Q;
case 401:return L;
case 402:return O;
case 403:return V;
case 404:return F;
case 405:return P;
case 406:return S;
case 407:return Y;
case 408:return R;
case 409:return y;
case 410:return r;
case 411:return E;
case 412:return bh;
case 413:return U;
case 414:return bk;
case 415:return ba;
case 500:return bg;
case 501:return bc;
case 502:return u;
case 503:return J;
case 504:return z;
case 505:return C;
case 12002:return q;
case 12029:return f;
case 12030:return f;
case 12031:return f;
case 12152:return G;
case 13030:return bj;
default:return a;
}}},properties:{request:{check:D,nullable:true},implementation:{check:bl,nullable:true,apply:K},state:{check:[bp,n,k,m,j,h,o],init:bp,event:be,apply:bf}},members:{send:function(){var bH=this.getRequest();

if(!bH){return this.error("Please attach a request object first");
}qx.io.remote.Exchange.initTypes();
var bF=qx.io.remote.Exchange.typesOrder;
var bE=qx.io.remote.Exchange.typesSupported;
var bJ=bH.getResponseType();
var bK={};

if(bH.getAsynchronous()){bK.asynchronous=true;
}else{bK.synchronous=true;
}
if(bH.getCrossDomain()){bK.crossDomain=true;
}
if(bH.getFileUpload()){bK.fileUpload=true;
}for(var bI in bH.getFormFields()){bK.programaticFormFields=true;
break;
}var bL,bG;

for(var i=0,l=bF.length;i<l;i++){bL=bE[bF[i]];

if(bL){if(!qx.io.remote.Exchange.canHandle(bL,bK,bJ)){continue;
}
try{{};
bG=new bL;
this.setImplementation(bG);
bG.setUseBasicHttpAuth(bH.getUseBasicHttpAuth());
bG.send();
return true;
}catch(bM){this.error("Request handler throws error");
this.error(bM);
return;
}}}this.error("There is no transport implementation available to handle this request: "+bH);
},abort:function(){var bN=this.getImplementation();

if(bN){{};
bN.abort();
}else{{};
this.setState(j);
}},timeout:function(){var bQ=this.getImplementation();

if(bQ){var bP=M;

for(var bO in bQ.getParameters()){bP+=bo+bO+c+bQ.getParameters()[bO];
}this.warn("Timeout: implementation "+bQ.toHashCode()+", "+bQ.getUrl()+" ["+bQ.getMethod()+"], "+bP);
bQ.timeout();
}else{this.warn("Timeout: forcing state to timeout");
this.setState(h);
}this.__sE();
},__sE:function(){var bR=this.getRequest();

if(bR){bR.setTimeout(0);
}},_onsending:function(e){this.setState(n);
},_onreceiving:function(e){this.setState(k);
},_oncompleted:function(e){this.setState(m);
},_onabort:function(e){this.setState(j);
},_onfailed:function(e){this.setState(o);
},_ontimeout:function(e){this.setState(h);
},_applyImplementation:function(bS,bT){if(bT){bT.removeListener(n,this._onsending,this);
bT.removeListener(k,this._onreceiving,this);
bT.removeListener(m,this._oncompleted,this);
bT.removeListener(j,this._onabort,this);
bT.removeListener(h,this._ontimeout,this);
bT.removeListener(o,this._onfailed,this);
}
if(bS){var bV=this.getRequest();
bS.setUrl(bV.getUrl());
bS.setMethod(bV.getMethod());
bS.setAsynchronous(bV.getAsynchronous());
bS.setUsername(bV.getUsername());
bS.setPassword(bV.getPassword());
bS.setParameters(bV.getParameters(false));
bS.setFormFields(bV.getFormFields());
bS.setRequestHeaders(bV.getRequestHeaders());
if(bS instanceof qx.io.remote.transport.XmlHttp){bS.setParseJson(bV.getParseJson());
}var bY=bV.getData();

if(bY===null){var ca=bV.getParameters(true);
var bX=[];

for(var bU in ca){var bW=ca[bU];

if(bW instanceof Array){for(var i=0;i<bW.length;i++){bX.push(encodeURIComponent(bU)+c+encodeURIComponent(bW[i]));
}}else{bX.push(encodeURIComponent(bU)+c+encodeURIComponent(bW));
}}
if(bX.length>0){bS.setData(bX.join(bo));
}}else{bS.setData(bY);
}bS.setResponseType(bV.getResponseType());
bS.addListener(n,this._onsending,this);
bS.addListener(k,this._onreceiving,this);
bS.addListener(m,this._oncompleted,this);
bS.addListener(j,this._onabort,this);
bS.addListener(h,this._ontimeout,this);
bS.addListener(o,this._onfailed,this);
}},_applyState:function(cb,cc){{};

switch(cb){case n:this.fireEvent(n);
break;
case k:this.fireEvent(k);
break;
case m:case j:case h:case o:var ce=this.getImplementation();

if(!ce){break;
}this.__sE();

if(this.hasListener(cb)){var cf=qx.event.Registration.createEvent(cb,qx.io.remote.Response);

if(cb==m){var cd=ce.getResponseContent();
cf.setContent(cd);
if(cd===null){{};
cb=o;
}}else if(cb==o){cf.setContent(ce.getResponseContent());
}cf.setStatusCode(ce.getStatusCode());
cf.setResponseHeaders(ce.getResponseHeaders());
this.dispatchEvent(cf);
}this.setImplementation(null);
ce.dispose();
break;
}}},settings:{"qx.ioRemoteDebug":false,"qx.ioRemoteDebugData":false},destruct:function(){var cg=this.getImplementation();

if(cg){this.setImplementation(null);
cg.dispose();
}this.setRequest(null);
}});
})();
(function(){var q="qx.event.type.Event",p="String",o="failed",n="timeout",m="created",l="aborted",k="sending",j="configured",i="receiving",h="completed",c="Object",g="Boolean",f="abstract",b="_applyState",a="GET",e="changeState",d="qx.io.remote.transport.Abstract";
qx.Class.define(d,{type:f,extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.setRequestHeaders({});
this.setParameters({});
this.setFormFields({});
},events:{"created":q,"configured":q,"sending":q,"receiving":q,"completed":q,"aborted":q,"failed":q,"timeout":q},properties:{url:{check:p,nullable:true},method:{check:p,nullable:true,init:a},asynchronous:{check:g,nullable:true,init:true},data:{check:p,nullable:true},username:{check:p,nullable:true},password:{check:p,nullable:true},state:{check:[m,j,k,i,h,l,n,o],init:m,event:e,apply:b},requestHeaders:{check:c,nullable:true},parameters:{check:c,nullable:true},formFields:{check:c,nullable:true},responseType:{check:p,nullable:true},useBasicHttpAuth:{check:g,nullable:true}},members:{send:function(){throw new Error("send is abstract");
},abort:function(){{};
this.setState(l);
},timeout:function(){{};
this.setState(n);
},failed:function(){{};
this.setState(o);
},setRequestHeader:function(r,s){throw new Error("setRequestHeader is abstract");
},getResponseHeader:function(t){throw new Error("getResponseHeader is abstract");
},getResponseHeaders:function(){throw new Error("getResponseHeaders is abstract");
},getStatusCode:function(){throw new Error("getStatusCode is abstract");
},getStatusText:function(){throw new Error("getStatusText is abstract");
},getResponseText:function(){throw new Error("getResponseText is abstract");
},getResponseXml:function(){throw new Error("getResponseXml is abstract");
},getFetchedLength:function(){throw new Error("getFetchedLength is abstract");
},_applyState:function(u,v){{};

switch(u){case m:this.fireEvent(m);
break;
case j:this.fireEvent(j);
break;
case k:this.fireEvent(k);
break;
case i:this.fireEvent(i);
break;
case h:this.fireEvent(h);
break;
case l:this.fireEvent(l);
break;
case o:this.fireEvent(o);
break;
case n:this.fireEvent(n);
break;
}return true;
}},destruct:function(){this.setRequestHeaders(null);
this.setParameters(null);
this.setFormFields(null);
}});
})();
(function(){var l="=",k="",j="&",h="application/xml",g="application/json",f="text/html",d="qx.client",c="textarea",b="_data_",a="load",G="text/plain",F="text/javascript",E="completed",D="readystatechange",C="?",B="qx.io.remote.transport.Iframe",A="none",z="display",y="gecko",x="frame_",s="aborted",t="pre",q="javascript:void(0)",r="sending",o="form",p="failed",m="mshtml",n="form_",u="opera",v="timeout",w="qx/static/blank.gif";
qx.Class.define(B,{extend:qx.io.remote.transport.Abstract,construct:function(){qx.io.remote.transport.Abstract.call(this);
var H=(new Date).valueOf();
var I=x+H;
var J=n+H;
var K;

if(qx.core.Variant.isSet(d,m)){K=q;
}this.__sF=qx.bom.Iframe.create({id:I,name:I,src:K});
qx.bom.element.Style.set(this.__sF,z,A);
this.__sG=qx.bom.Element.create(o,{id:J,name:J,target:I});
qx.bom.element.Style.set(this.__sG,z,A);
qx.dom.Element.insertEnd(this.__sG,qx.dom.Node.getBodyElement(document));
this.__sH=qx.bom.Element.create(c,{id:b,name:b});
qx.dom.Element.insertEnd(this.__sH,this.__sG);
qx.dom.Element.insertEnd(this.__sF,qx.dom.Node.getBodyElement(document));
qx.event.Registration.addListener(this.__sF,a,this._onload,this);
this.__sI=qx.lang.Function.listener(this._onreadystatechange,this);
qx.bom.Event.addNativeListener(this.__sF,D,this.__sI);
},statics:{handles:{synchronous:false,asynchronous:true,crossDomain:false,fileUpload:true,programaticFormFields:true,responseTypes:[G,F,g,h,f]},isSupported:function(){return true;
},_numericMap:{"uninitialized":1,"loading":2,"loaded":2,"interactive":3,"complete":4}},members:{__sH:null,__sJ:0,__sG:null,__sF:null,__sI:null,send:function(){var M=this.getMethod();
var O=this.getUrl();
var S=this.getParameters(false);
var R=[];

for(var N in S){var P=S[N];

if(P instanceof Array){for(var i=0;i<P.length;i++){R.push(encodeURIComponent(N)+l+encodeURIComponent(P[i]));
}}else{R.push(encodeURIComponent(N)+l+encodeURIComponent(P));
}}
if(R.length>0){O+=(O.indexOf(C)>=0?j:C)+R.join(j);
}if(this.getData()===null){var S=this.getParameters(true);
var R=[];

for(var N in S){var P=S[N];

if(P instanceof Array){for(var i=0;i<P.length;i++){R.push(encodeURIComponent(N)+l+encodeURIComponent(P[i]));
}}else{R.push(encodeURIComponent(N)+l+encodeURIComponent(P));
}}
if(R.length>0){this.setData(R.join(j));
}}var L=this.getFormFields();

for(var N in L){var Q=document.createElement(c);
Q.name=N;
Q.appendChild(document.createTextNode(L[N]));
this.__sG.appendChild(Q);
}this.__sG.action=O;
this.__sG.method=M;
this.__sH.appendChild(document.createTextNode(this.getData()));
this.__sG.submit();
this.setState(r);
},_onload:qx.event.GlobalError.observeMethod(function(e){if(qx.bom.client.Engine.NAME==u&&this.getIframeHtmlContent()==k){return;
}
if(this.__sG.src){return;
}this._switchReadyState(qx.io.remote.transport.Iframe._numericMap.complete);
}),_onreadystatechange:qx.event.GlobalError.observeMethod(function(e){this._switchReadyState(qx.io.remote.transport.Iframe._numericMap[this.__sF.readyState]);
}),_switchReadyState:function(T){switch(this.getState()){case E:case s:case p:case v:this.warn("Ignore Ready State Change");
return;
}while(this.__sJ<T){this.setState(qx.io.remote.Exchange._nativeMap[++this.__sJ]);
}},setRequestHeader:function(U,V){},getResponseHeader:function(W){return null;
},getResponseHeaders:function(){return {};
},getStatusCode:function(){return 200;
},getStatusText:function(){return k;
},getIframeWindow:function(){return qx.bom.Iframe.getWindow(this.__sF);
},getIframeDocument:function(){return qx.bom.Iframe.getDocument(this.__sF);
},getIframeBody:function(){return qx.bom.Iframe.getBody(this.__sF);
},getIframeTextContent:function(){var X=this.getIframeBody();

if(!X){return null;
}
if(!X.firstChild){return k;
}if(X.firstChild.tagName&&X.firstChild.tagName.toLowerCase()==t){return X.firstChild.innerHTML;
}else{return X.innerHTML;
}},getIframeHtmlContent:function(){var Y=this.getIframeBody();
return Y?Y.innerHTML:null;
},getFetchedLength:function(){return 0;
},getResponseContent:function(){if(this.getState()!==E){{};
return null;
}{};
var ba=this.getIframeTextContent();

switch(this.getResponseType()){case G:{};
return ba;
break;
case f:ba=this.getIframeHtmlContent();
{};
return ba;
break;
case g:ba=this.getIframeHtmlContent();
{};

try{return ba&&ba.length>0?qx.util.Json.parse(ba,false):null;
}catch(bb){return this.error("Could not execute json: ("+ba+")",bb);
}case F:ba=this.getIframeHtmlContent();
{};

try{return ba&&ba.length>0?window.eval(ba):null;
}catch(bc){return this.error("Could not execute javascript: ("+ba+")",bc);
}case h:ba=this.getIframeDocument();
{};
return ba;
default:this.warn("No valid responseType specified ("+this.getResponseType()+")!");
return null;
}}},defer:function(){qx.io.remote.Exchange.registerType(qx.io.remote.transport.Iframe,B);
},destruct:function(){if(this.__sF){qx.event.Registration.removeListener(this.__sF,a,this._onload,this);
qx.bom.Event.removeNativeListener(this.__sF,D,this.__sI);
if(qx.core.Variant.isSet(d,y)){this.__sF.src=qx.util.ResourceManager.getInstance().toUri(w);
}qx.dom.Element.remove(this.__sF);
}
if(this.__sG){qx.dom.Element.remove(this.__sG);
}this.__sF=this.__sG=this.__sH=null;
}});
})();
(function(){var d="qx.event.handler.Iframe",c="load",b="iframe",a="navigate";
qx.Class.define(d,{extend:qx.core.Object,implement:qx.event.IEventHandler,statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{load:1,navigate:1},TARGET_CHECK:qx.event.IEventHandler.TARGET_DOMNODE,IGNORE_CAN_HANDLE:false,onevent:qx.event.GlobalError.observeMethod(function(e){var f=qx.bom.Iframe.queryCurrentUrl(e);

if(f!==e.$$url){qx.event.Registration.fireEvent(e,a,qx.event.type.Data,[f]);
e.$$url=f;
}qx.event.Registration.fireEvent(e,c);
})},members:{canHandleEvent:function(g,h){return g.tagName.toLowerCase()===b;
},registerEvent:function(i,j,k){},unregisterEvent:function(l,m,n){}},defer:function(o){qx.event.Registration.addHandler(o);
}});
})();
(function(){var f="load",e="qx.client",d="qx.bom.Iframe",c="webkit",b="iframe",a="body";
qx.Class.define(d,{statics:{DEFAULT_ATTRIBUTES:{onload:"qx.event.handler.Iframe.onevent(this)",frameBorder:0,frameSpacing:0,marginWidth:0,marginHeight:0,hspace:0,vspace:0,border:0,allowTransparency:true},create:function(g,h){var g=g?qx.lang.Object.clone(g):{};
var i=qx.bom.Iframe.DEFAULT_ATTRIBUTES;

for(var j in i){if(g[j]==null){g[j]=i[j];
}}return qx.bom.Element.create(b,g,h);
},getWindow:function(k){try{return k.contentWindow;
}catch(l){return null;
}},getDocument:qx.core.Variant.select(e,{"mshtml":function(m){try{var n=this.getWindow(m);
return n?n.document:null;
}catch(o){return null;
}},"default":function(p){try{return p.contentDocument;
}catch(q){return null;
}}}),getBody:function(r){try{var s=this.getDocument(r);
return s?s.getElementsByTagName(a)[0]:null;
}catch(t){return null;
}},setSource:function(u,v){try{if(this.getWindow(u)&&qx.dom.Hierarchy.isRendered(u)){try{if(qx.core.Variant.isSet(e,c)&&qx.bom.client.Platform.MAC){var w=this.getWindow(u);

if(w){w.stop();
}}this.getWindow(u).location.replace(v);
}catch(x){u.src=v;
}}else{u.src=v;
}this.__tW(u);
}catch(y){qx.log.Logger.warn("Iframe source could not be set!");
}},queryCurrentUrl:function(z){var A=this.getDocument(z);

try{if(A&&A.location){return A.location.href;
}}catch(B){}return null;
},__tW:function(C){var D=function(){qx.bom.Event.removeNativeListener(C,f,D);
C.$$url=qx.bom.Iframe.queryCurrentUrl(C);
};
qx.bom.Event.addNativeListener(C,f,D);
}}});
})();
(function(){var a="qx.dom.Element";
qx.Class.define(a,{statics:{hasChild:function(parent,b){return b.parentNode===parent;
},hasChildren:function(c){return !!c.firstChild;
},hasChildElements:function(d){d=d.firstChild;

while(d){if(d.nodeType===1){return true;
}d=d.nextSibling;
}return false;
},getParentElement:function(e){return e.parentNode;
},isInDom:function(f,g){if(!g){g=window;
}var h=g.document.getElementsByTagName(f.nodeName);

for(var i=0,l=h.length;i<l;i++){if(h[i]===f){return true;
}}return false;
},insertAt:function(j,parent,k){var m=parent.childNodes[k];

if(m){parent.insertBefore(j,m);
}else{parent.appendChild(j);
}return true;
},insertBegin:function(n,parent){if(parent.firstChild){this.insertBefore(n,parent.firstChild);
}else{parent.appendChild(n);
}},insertEnd:function(o,parent){parent.appendChild(o);
},insertBefore:function(p,q){q.parentNode.insertBefore(p,q);
return true;
},insertAfter:function(r,s){var parent=s.parentNode;

if(s==parent.lastChild){parent.appendChild(r);
}else{return this.insertBefore(r,s.nextSibling);
}return true;
},remove:function(t){if(!t.parentNode){return false;
}t.parentNode.removeChild(t);
return true;
},removeChild:function(u,parent){if(u.parentNode!==parent){return false;
}parent.removeChild(u);
return true;
},removeChildAt:function(v,parent){var w=parent.childNodes[v];

if(!w){return false;
}parent.removeChild(w);
return true;
},replaceChild:function(x,y){if(!y.parentNode){return false;
}y.parentNode.replaceChild(x,y);
return true;
},replaceAt:function(z,A,parent){var B=parent.childNodes[A];

if(!B){return false;
}parent.replaceChild(z,B);
return true;
}}});
})();
(function(){var a="qx.util.format.IFormat";
qx.Interface.define(a,{members:{format:function(b){},parse:function(c){}}});
})();
(function(){var t="",s="Number",r="-",q="0",p="String",o="changeNumberFormat",n='(',m="g",l="Boolean",k="$",d="NaN",j='([0-9]{1,3}(?:',g='{0,1}[0-9]{3}){0,})',c='\\d+){0,1}',b="qx.util.format.NumberFormat",f="Infinity",e="^",h=".",a="-Infinity",i='([-+]){0,1}';
qx.Class.define(b,{extend:qx.core.Object,implement:qx.util.format.IFormat,construct:function(u){qx.core.Object.call(this);
this.__mz=u;
},statics:{getIntegerInstance:function(){{};
var v=qx.util.format.NumberFormat;

if(v._integerInstance==null){v._integerInstance=new v();
v._integerInstance.setMaximumFractionDigits(0);
}return v._integerInstance;
},getInstance:function(){{};

if(!this._instance){this._instance=new this;
}return this._instance;
}},properties:{minimumIntegerDigits:{check:s,init:0},maximumIntegerDigits:{check:s,nullable:true},minimumFractionDigits:{check:s,init:0},maximumFractionDigits:{check:s,nullable:true},groupingUsed:{check:l,init:true},prefix:{check:p,init:t,event:o},postfix:{check:p,init:t,event:o}},members:{__mz:null,format:function(w){switch(w){case Infinity:return f;
case -Infinity:return a;
case NaN:return d;
}var A=(w<0);

if(A){w=-w;
}
if(this.getMaximumFractionDigits()!=null){var H=Math.pow(10,this.getMaximumFractionDigits());
w=Math.round(w*H)/H;
}var G=String(Math.floor(w)).length;
var x=t+w;
var D=x.substring(0,G);

while(D.length<this.getMinimumIntegerDigits()){D=q+D;
}
if(this.getMaximumIntegerDigits()!=null&&D.length>this.getMaximumIntegerDigits()){D=D.substring(D.length-this.getMaximumIntegerDigits());
}var C=x.substring(G+1);

while(C.length<this.getMinimumFractionDigits()){C+=q;
}
if(this.getMaximumFractionDigits()!=null&&C.length>this.getMaximumFractionDigits()){C=C.substring(0,this.getMaximumFractionDigits());
}if(this.getGroupingUsed()){var z=D;
D=t;
var F;

for(F=z.length;F>3;F-=3){D=t+qx.locale.Number.getGroupSeparator(this.__mz)+z.substring(F-3,F)+D;
}D=z.substring(0,F)+D;
}var B=this.getPrefix()?this.getPrefix():t;
var y=this.getPostfix()?this.getPostfix():t;
var E=B+(A?r:t)+D;

if(C.length>0){E+=t+qx.locale.Number.getDecimalSeparator(this.__mz)+C;
}E+=y;
return E;
},parse:function(I){var N=qx.lang.String.escapeRegexpChars(qx.locale.Number.getGroupSeparator(this.__mz)+t);
var L=qx.lang.String.escapeRegexpChars(qx.locale.Number.getDecimalSeparator(this.__mz)+t);
var J=new RegExp(e+qx.lang.String.escapeRegexpChars(this.getPrefix())+i+j+N+g+n+L+c+qx.lang.String.escapeRegexpChars(this.getPostfix())+k);
var M=J.exec(I);

if(M==null){throw new Error("Number string '"+I+"' does not match the number format");
}var O=(M[1]==r);
var Q=M[2];
var P=M[3];
Q=Q.replace(new RegExp(N,m),t);
var K=(O?r:t)+Q;

if(P!=null&&P.length!=0){P=P.replace(new RegExp(L),t);
K+=h+P;
}return parseFloat(K);
}}});
})();
(function(){var n=",",m="",k='"',j="string",h="null",g=':',f="qx.jsonDebugging",e='-',d='\\u00',c="new Date(Date.UTC(",N="__mw",M="__mn",L='\\\\',K="__ml",J='\\f',I='\\"',H="))",G='T',F="}",E='(',u='.',v="{",s='\\r',t=":",q='\\t',r="__mv",o="__mo",p="[",w="__mm",x="]",z="qx.jsonEncodeUndefined",y='\\b',B="qx.util.Json",A='Z"',D=')',C='\\n';
qx.Class.define(B,{statics:{__mj:null,BEAUTIFYING_INDENT:"  ",BEAUTIFYING_LINE_END:"\n",CONVERT_DATES:null,__mk:{"function":K,"boolean":w,"number":M,"string":o,"object":r,"undefined":N},NUMBER_FORMAT:new qx.util.format.NumberFormat(),__ml:function(O,P){return String(O);
},__mm:function(Q,R){return String(Q);
},__mn:function(S,T){return isFinite(S)?String(S):h;
},__mo:function(U,V){var W;

if(/["\\\x00-\x1f]/.test(U)){W=U.replace(/([\x00-\x1f\\"])/g,qx.util.Json.__mq);
}else{W=U;
}return k+W+k;
},__mp:{'\b':y,'\t':q,'\n':C,'\f':J,'\r':s,'"':I,'\\':L},__mq:function(a,b){var X=qx.util.Json.__mp[b];

if(X){return X;
}X=b.charCodeAt();
return d+Math.floor(X/16).toString(16)+(X%16).toString(16);
},__mr:function(Y,ba){var bc=[],bf=true,be,bb;
var bd=qx.util.Json.__my;
bc.push(p);

if(bd){qx.util.Json.__ms+=qx.util.Json.BEAUTIFYING_INDENT;
bc.push(qx.util.Json.__ms);
}
for(var i=0,l=Y.length;i<l;i++){bb=Y[i];
be=this.__mk[typeof bb];

if(be){bb=this[be](bb,i+m);

if(typeof bb==j){if(!bf){bc.push(n);

if(bd){bc.push(qx.util.Json.__ms);
}}bc.push(bb);
bf=false;
}}}
if(bd){qx.util.Json.__ms=qx.util.Json.__ms.substring(0,qx.util.Json.__ms.length-qx.util.Json.BEAUTIFYING_INDENT.length);
bc.push(qx.util.Json.__ms);
}bc.push(x);
return bc.join(m);
},__mt:function(bg,bh){if(!qx.util.Json.CONVERT_DATES){if(bg.toJSON&&!qx.bom.client.Engine.OPERA&&!qx.bom.client.Engine.MSHTML){return k+bg.toJSON()+k;
}var bi=this.NUMBER_FORMAT;
bi.setMinimumIntegerDigits(2);
var bk=bg.getUTCFullYear()+e+bi.format(bg.getUTCMonth()+1)+e+bi.format(bg.getUTCDate())+G+bi.format(bg.getUTCHours())+g+bi.format(bg.getUTCMinutes())+g+bi.format(bg.getUTCSeconds())+u;
bi.setMinimumIntegerDigits(3);
return k+bk+bi.format(bg.getUTCMilliseconds())+A;
}else{var bj=bg.getUTCFullYear()+n+bg.getUTCMonth()+n+bg.getUTCDate()+n+bg.getUTCHours()+n+bg.getUTCMinutes()+n+bg.getUTCSeconds()+n+bg.getUTCMilliseconds();
return c+bj+H;
}},__mu:function(bl,bm){var bp=[],br=true,bo,bn;
var bq=qx.util.Json.__my;
bp.push(v);

if(bq){qx.util.Json.__ms+=qx.util.Json.BEAUTIFYING_INDENT;
bp.push(qx.util.Json.__ms);
}
for(var bm in bl){bn=bl[bm];
bo=this.__mk[typeof bn];

if(bo){bn=this[bo](bn,bm);

if(typeof bn==j){if(!br){bp.push(n);

if(bq){bp.push(qx.util.Json.__ms);
}}bp.push(this.__mo(bm),t,bn);
br=false;
}}}
if(bq){qx.util.Json.__ms=qx.util.Json.__ms.substring(0,qx.util.Json.__ms.length-qx.util.Json.BEAUTIFYING_INDENT.length);
bp.push(qx.util.Json.__ms);
}bp.push(F);
return bp.join(m);
},__mv:function(bs,bt){if(bs){if(qx.lang.Type.isFunction(bs.toJSON)&&bs.toJSON!==this.__mj){return this.__mx(bs.toJSON(bt),bt);
}else if(qx.lang.Type.isDate(bs)){return this.__mt(bs,bt);
}else if(qx.lang.Type.isArray(bs)){return this.__mr(bs,bt);
}else if(qx.lang.Type.isObject(bs)){return this.__mu(bs,bt);
}return m;
}return h;
},__mw:function(bu,bv){if(qx.core.Setting.get(z)){return h;
}},__mx:function(bw,bx){return this[this.__mk[typeof bw]](bw,bx);
},stringify:function(by,bz){this.__my=bz;
this.__ms=this.BEAUTIFYING_LINE_END;
var bA=this.__mx(by,m);

if(typeof bA!=j){bA=null;
}if(qx.core.Setting.get(f)){qx.log.Logger.debug(this,"JSON request: "+bA);
}return bA;
},parse:function(bB,bC){if(bC===undefined){bC=true;
}
if(qx.core.Setting.get(f)){qx.log.Logger.debug(this,"JSON response: "+bB);
}
if(bC){if(/[^,:{}\[\]0-9.\-+Eaeflnr-u \n\r\t]/.test(bB.replace(/"(\\.|[^"\\])*"/g,m))){throw new Error("Could not parse JSON string!");
}}
try{var bD=(bB&&bB.length>0)?eval(E+bB+D):null;
return bD;
}catch(bE){throw new Error("Could not evaluate JSON string: "+bE.message);
}}},settings:{"qx.jsonEncodeUndefined":true,"qx.jsonDebugging":false},defer:function(bF){bF.__mj=Date.prototype.toJSON;
}});
})();
(function(){var d="cldr_number_decimal_separator",c="cldr_number_percent_format",b="qx.locale.Number",a="cldr_number_group_separator";
qx.Class.define(b,{statics:{getDecimalSeparator:function(e){return qx.locale.Manager.getInstance().localize(d,[],e);
},getGroupSeparator:function(f){return qx.locale.Manager.getInstance().localize(a,[],f);
},getPercentFormat:function(g){return qx.locale.Manager.getInstance().localize(c,[],g);
}}});
})();
(function(){var r="&",q="=",p="?",o="application/json",n="completed",m="text/plain",l="text/javascript",k="qx.io.remote.transport.Script",j="",h="_ScriptTransport_data",c="script",g="timeout",f="_ScriptTransport_",b="_ScriptTransport_id",a="aborted",e="utf-8",d="failed";
qx.Class.define(k,{extend:qx.io.remote.transport.Abstract,construct:function(){qx.io.remote.transport.Abstract.call(this);
var s=++qx.io.remote.transport.Script.__sK;

if(s>=2000000000){qx.io.remote.transport.Script.__sK=s=1;
}this.__sL=null;
this.__sK=s;
},statics:{__sK:0,_instanceRegistry:{},ScriptTransport_PREFIX:f,ScriptTransport_ID_PARAM:b,ScriptTransport_DATA_PARAM:h,handles:{synchronous:false,asynchronous:true,crossDomain:true,fileUpload:false,programaticFormFields:false,responseTypes:[m,l,o]},isSupported:function(){return true;
},_numericMap:{"uninitialized":1,"loading":2,"loaded":2,"interactive":3,"complete":4},_requestFinished:qx.event.GlobalError.observeMethod(function(t,content){var u=qx.io.remote.transport.Script._instanceRegistry[t];

if(u==null){{};
}else{u._responseContent=content;
u._switchReadyState(qx.io.remote.transport.Script._numericMap.complete);
}})},members:{__sM:0,__sL:null,__sK:null,send:function(){var x=this.getUrl();
x+=(x.indexOf(p)>=0?r:p)+qx.io.remote.transport.Script.ScriptTransport_ID_PARAM+q+this.__sK;
var A=this.getParameters();
var z=[];

for(var w in A){if(w.indexOf(qx.io.remote.transport.Script.ScriptTransport_PREFIX)==0){this.error("Illegal parameter name. The following prefix is used internally by qooxdoo): "+qx.io.remote.transport.Script.ScriptTransport_PREFIX);
}var y=A[w];

if(y instanceof Array){for(var i=0;i<y.length;i++){z.push(encodeURIComponent(w)+q+encodeURIComponent(y[i]));
}}else{z.push(encodeURIComponent(w)+q+encodeURIComponent(y));
}}
if(z.length>0){x+=r+z.join(r);
}var v=this.getData();

if(v!=null){x+=r+qx.io.remote.transport.Script.ScriptTransport_DATA_PARAM+q+encodeURIComponent(v);
}qx.io.remote.transport.Script._instanceRegistry[this.__sK]=this;
this.__sL=document.createElement(c);
this.__sL.charset=e;
this.__sL.src=x;
{};
document.body.appendChild(this.__sL);
},_switchReadyState:function(B){switch(this.getState()){case n:case a:case d:case g:this.warn("Ignore Ready State Change");
return;
}while(this.__sM<B){this.setState(qx.io.remote.Exchange._nativeMap[++this.__sM]);
}},setRequestHeader:function(C,D){},getResponseHeader:function(E){return null;
},getResponseHeaders:function(){return {};
},getStatusCode:function(){return 200;
},getStatusText:function(){return j;
},getFetchedLength:function(){return 0;
},getResponseContent:function(){if(this.getState()!==n){{};
return null;
}{};

switch(this.getResponseType()){case m:case o:case l:{};
var F=this._responseContent;
return (F===0?0:(F||null));
default:this.warn("No valid responseType specified ("+this.getResponseType()+")!");
return null;
}}},defer:function(){qx.io.remote.Exchange.registerType(qx.io.remote.transport.Script,k);
},destruct:function(){if(this.__sL){delete qx.io.remote.transport.Script._instanceRegistry[this.__sK];
document.body.removeChild(this.__sL);
}this.__sL=this._responseContent=null;
}});
})();
(function(){var m="failed",k="completed",j="=",h="aborted",g="",f="sending",d="&",c="configured",b="timeout",a="application/xml",J="qx.io.remote.transport.XmlHttp",I="application/json",H="text/html",G="qx.client",F="receiving",E="text/plain",D="text/javascript",C="?",B="created",A="Boolean",u='Referer',v='Basic ',r="\n</pre>",t="string",p='Authorization',q="<pre>Could not execute json: \n",n="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",o=':',w="parseerror",x="file:",z="webkit",y="object";
qx.Class.define(J,{extend:qx.io.remote.transport.Abstract,statics:{handles:{synchronous:true,asynchronous:true,crossDomain:false,fileUpload:false,programaticFormFields:false,responseTypes:[E,D,I,a,H]},createRequestObject:qx.core.Variant.select(G,{"default":function(){return new XMLHttpRequest;
},"mshtml":function(){if(window.ActiveXObject&&qx.xml.Document.XMLHTTP){return new ActiveXObject(qx.xml.Document.XMLHTTP);
}
if(window.XMLHttpRequest){return new XMLHttpRequest;
}}}),isSupported:function(){return !!this.createRequestObject();
}},properties:{parseJson:{check:A,init:true}},members:{__sN:false,__sO:0,__sP:null,getRequest:function(){if(this.__sP===null){this.__sP=qx.io.remote.transport.XmlHttp.createRequestObject();
this.__sP.onreadystatechange=qx.lang.Function.bind(this._onreadystatechange,this);
}return this.__sP;
},send:function(){this.__sO=0;
var O=this.getRequest();
var K=this.getMethod();
var R=this.getAsynchronous();
var Q=this.getUrl();
var M=(window.location.protocol===x&&!(/^http(s){0,1}\:/.test(Q)));
this.__sN=M;
var U=this.getParameters(false);
var S=[];

for(var L in U){var P=U[L];

if(P instanceof Array){for(var i=0;i<P.length;i++){S.push(encodeURIComponent(L)+j+encodeURIComponent(P[i]));
}}else{S.push(encodeURIComponent(L)+j+encodeURIComponent(P));
}}
if(S.length>0){Q+=(Q.indexOf(C)>=0?d:C)+S.join(d);
}if(this.getData()===null){var U=this.getParameters(true);
var S=[];

for(var L in U){var P=U[L];

if(P instanceof Array){for(var i=0;i<P.length;i++){S.push(encodeURIComponent(L)+j+encodeURIComponent(P[i]));
}}else{S.push(encodeURIComponent(L)+j+encodeURIComponent(P));
}}
if(S.length>0){this.setData(S.join(d));
}}var T=function(V){var bb=n;
var bf=g;
var Y,X,W;
var bc,bd,be,ba;
var i=0;

do{Y=V.charCodeAt(i++);
X=V.charCodeAt(i++);
W=V.charCodeAt(i++);
bc=Y>>2;
bd=((Y&3)<<4)|(X>>4);
be=((X&15)<<2)|(W>>6);
ba=W&63;

if(isNaN(X)){be=ba=64;
}else if(isNaN(W)){ba=64;
}bf+=bb.charAt(bc)+bb.charAt(bd)+bb.charAt(be)+bb.charAt(ba);
}while(i<V.length);
return bf;
};
try{if(this.getUsername()){if(this.getUseBasicHttpAuth()){O.open(K,Q,R);
O.setRequestHeader(p,v+T(this.getUsername()+o+this.getPassword()));
}else{O.open(K,Q,R,this.getUsername(),this.getPassword());
}}else{O.open(K,Q,R);
}}catch(bg){this.error("Failed with exception: "+bg);
this.failed();
return;
}if(!qx.core.Variant.isSet(G,z)){O.setRequestHeader(u,window.location.href);
}var N=this.getRequestHeaders();

for(var L in N){O.setRequestHeader(L,N[L]);
}try{{};
O.send(this.getData());
}catch(bh){if(M){this.failedLocally();
}else{this.error("Failed to send data: "+bh,"send");
this.failed();
}return;
}if(!R){this._onreadystatechange();
}},failedLocally:function(){if(this.getState()===m){return;
}this.warn("Could not load from file: "+this.getUrl());
this.failed();
},_onreadystatechange:qx.event.GlobalError.observeMethod(function(e){switch(this.getState()){case k:case h:case m:case b:{};
return;
}var bi=this.getReadyState();

if(bi==4){if(!qx.io.remote.Exchange.wasSuccessful(this.getStatusCode(),bi,this.__sN)){if(this.getState()===c){this.setState(f);
}this.failed();
return;
}}while(this.__sO<bi){this.setState(qx.io.remote.Exchange._nativeMap[++this.__sO]);
}}),getReadyState:function(){var bj=null;

try{bj=this.getRequest().readyState;
}catch(bk){}return bj;
},setRequestHeader:function(bl,bm){this.getRequestHeaders()[bl]=bm;
},getResponseHeader:function(bn){var bo=null;

try{bo=this.getRequest().getResponseHeader(bn)||null;
}catch(bp){}return bo;
},getStringResponseHeaders:function(){var br=null;

try{var bq=this.getRequest().getAllResponseHeaders();

if(bq){br=bq;
}}catch(bs){}return br;
},getResponseHeaders:function(){var bv=this.getStringResponseHeaders();
var bw={};

if(bv){var bt=bv.split(/[\r\n]+/g);

for(var i=0,l=bt.length;i<l;i++){var bu=bt[i].match(/^([^:]+)\s*:\s*(.+)$/i);

if(bu){bw[bu[1]]=bu[2];
}}}return bw;
},getStatusCode:function(){var bx=-1;

try{bx=this.getRequest().status;
}catch(by){}return bx;
},getStatusText:function(){var bz=g;

try{bz=this.getRequest().statusText;
}catch(bA){}return bz;
},getResponseText:function(){var bB=null;

try{bB=this.getRequest().responseText;
}catch(bC){bB=null;
}return bB;
},getResponseXml:function(){var bF=null;
var bD=this.getStatusCode();
var bE=this.getReadyState();

if(qx.io.remote.Exchange.wasSuccessful(bD,bE,this.__sN)){try{bF=this.getRequest().responseXML;
}catch(bG){}}if(typeof bF==y&&bF!=null){if(!bF.documentElement){var s=String(this.getRequest().responseText).replace(/<\?xml[^\?]*\?>/,g);
bF.loadXML(s);
}if(!bF.documentElement){throw new Error("Missing Document Element!");
}
if(bF.documentElement.tagName==w){throw new Error("XML-File is not well-formed!");
}}else{throw new Error("Response was not a valid xml document ["+this.getRequest().responseText+"]");
}return bF;
},getFetchedLength:function(){var bH=this.getResponseText();
return typeof bH==t?bH.length:0;
},getResponseContent:function(){var bI=this.getState();

if(bI!==k&&bI!=m){{};
return null;
}{};
var bK=this.getResponseText();

if(bI==m){{};
return bK;
}
switch(this.getResponseType()){case E:case H:{};
return bK;
case I:{};

try{if(bK&&bK.length>0){var bJ;

if(this.getParseJson()){bJ=qx.util.Json.parse(bK,false);
bJ=(bJ===0?0:(bJ||null));
}else{bJ=bK;
}return bJ;
}else{return null;
}}catch(bL){this.error("Could not execute json: ["+bK+"]",bL);
return q+bK+r;
}case D:{};

try{if(bK&&bK.length>0){var bJ=window.eval(bK);
return (bJ===0?0:(bJ||null));
}else{return null;
}}catch(bM){this.error("Could not execute javascript: ["+bK+"]",bM);
return null;
}case a:bK=this.getResponseXml();
{};
return (bK===0?0:(bK||null));
default:this.warn("No valid responseType specified ("+this.getResponseType()+")!");
return null;
}},_applyState:function(bN,bO){{};

switch(bN){case B:this.fireEvent(B);
break;
case c:this.fireEvent(c);
break;
case f:this.fireEvent(f);
break;
case F:this.fireEvent(F);
break;
case k:this.fireEvent(k);
break;
case m:this.fireEvent(m);
break;
case h:this.getRequest().abort();
this.fireEvent(h);
break;
case b:this.getRequest().abort();
this.fireEvent(b);
break;
}}},defer:function(){qx.io.remote.Exchange.registerType(qx.io.remote.transport.XmlHttp,J);
},destruct:function(){var bP=this.getRequest();

if(bP){bP.onreadystatechange=qx.lang.Function.empty;
switch(bP.readyState){case 1:case 2:case 3:bP.abort();
}}this.__sP=null;
}});
})();
(function(){var c="Integer",b="Object",a="qx.io.remote.Response";
qx.Class.define(a,{extend:qx.event.type.Event,properties:{state:{check:c,nullable:true},statusCode:{check:c,nullable:true},content:{nullable:true},responseHeaders:{check:b,nullable:true}},members:{clone:function(d){var e=qx.event.type.Event.prototype.clone.call(this,d);
e.setType(this.getType());
e.setState(this.getState());
e.setStatusCode(this.getStatusCode());
e.setContent(this.getContent());
e.setResponseHeaders(this.getResponseHeaders());
return e;
},getResponseHeader:function(f){var g=this.getResponseHeaders();

if(g){return g[f]||null;
}return null;
}}});
})();
(function(){var p="Boolean",o="column-button",n="Function",m="qx.event.type.Data",k="statusbar",h="qx.ui.table.pane.CellEvent",g="function",f="PageUp",e="dataChanged",d="changeLocale",bI="changeSelection",bH="appear",bG="qx.dynlocale",bF='"',bE="Enter",bD="metaDataChanged",bC="__pV",bB="on",bA="_applyStatusBarVisible",bz="columnVisibilityMenuCreateStart",w="blur",y="qx.ui.table.Table",u="columnVisibilityMenuCreateEnd",v="__pM",s="changeVisible",t="_applyResetSelectionOnHeaderClick",q="_applyMetaColumnCounts",r="focus",F="changeDataRowRenderer",G="changeHeaderCellHeight",ba="Escape",V="A",bi="changeSelectionModel",bd="Left",bu="__pU",bo="Down",O="Integer",by="_applyHeaderCellHeight",bw="visibilityChanged",bv="qx.ui.table.ITableModel",M="orderChanged",R="_applySelectionModel",T="menu-button",X="menu",bb="_applyAdditionalStatusBarText",be="_applyFocusCellOnMouseMove",bk="table",bq="_applyColumnVisibilityButtonVisible",z="__ui",A="changeTableModel",Q="qx.event.type.Event",bh="tableWidthChanged",bg="_applyHeaderCellsVisible",bf="Object",bm="__pL",bl="_applyShowCellFocusIndicator",bc="resize",bj="verticalScrollBarChanged",a="__pT",bp="changeScrollY",B="_applyTableModel",C="End",W="_applyKeepFirstVisibleRowComplete",b="widthChanged",c="one of one row",L="Home",D="_applyRowHeight",E="F2",K="Up",Y="%1 rows",bs="qx.ui.table.selection.Model",br="one row",S="PageDown",bt="%1 of %2 rows",N="keypress",bn="changeRowHeight",H="Number",J="header",P="_applyContextMenuFromDataCellsOnly",U="qx.ui.table.IRowRenderer",I="Right",bx="Space";
qx.Class.define(y,{extend:qx.ui.core.Widget,construct:function(bJ,bK){qx.ui.core.Widget.call(this);
if(!bK){bK={};
}
if(bK.initiallyHiddenColumns){this.setInitiallyHiddenColumns(bK.initiallyHiddenColumns);
}
if(bK.selectionManager){this.setNewSelectionManager(bK.selectionManager);
}
if(bK.selectionModel){this.setNewSelectionModel(bK.selectionModel);
}
if(bK.tableColumnModel){this.setNewTableColumnModel(bK.tableColumnModel);
}
if(bK.tablePane){this.setNewTablePane(bK.tablePane);
}
if(bK.tablePaneHeader){this.setNewTablePaneHeader(bK.tablePaneHeader);
}
if(bK.tablePaneScroller){this.setNewTablePaneScroller(bK.tablePaneScroller);
}
if(bK.tablePaneModel){this.setNewTablePaneModel(bK.tablePaneModel);
}
if(bK.columnMenu){this.setNewColumnMenu(bK.columnMenu);
}this._setLayout(new qx.ui.layout.VBox());
this.__pL=new qx.ui.container.Composite(new qx.ui.layout.HBox());
this._add(this.__pL,{flex:1});
this.setDataRowRenderer(new qx.ui.table.rowrenderer.Default(this));
this.__pM=this.getNewSelectionManager()(this);
this.setSelectionModel(this.getNewSelectionModel()(this));
this.setTableModel(bJ||this.getEmptyTableModel());
this.setMetaColumnCounts([-1]);
this.setTabIndex(1);
this.addListener(N,this._onKeyPress);
this.addListener(r,this._onFocusChanged);
this.addListener(w,this._onFocusChanged);
var bL=new qx.ui.core.Widget().set({height:0});
this._add(bL);
bL.addListener(bc,this._onResize,this);
this.__pN=null;
this.__pO=null;
if(qx.core.Variant.isSet(bG,bB)){qx.locale.Manager.getInstance().addListener(d,this._onChangeLocale,this);
}this.initStatusBarVisible();
bJ=this.getTableModel();

if(bJ.init&&typeof (bJ.init)==g){bJ.init(this);
}},events:{"columnVisibilityMenuCreateStart":m,"columnVisibilityMenuCreateEnd":m,"tableWidthChanged":Q,"verticalScrollBarChanged":m,"cellClick":h,"cellDblclick":h,"cellContextmenu":h,"dataEdited":m},statics:{__pP:{cellClick:1,cellDblclick:1,cellContextmenu:1}},properties:{appearance:{refine:true,init:bk},focusable:{refine:true,init:true},minWidth:{refine:true,init:50},initiallyHiddenColumns:{init:null},selectable:{refine:true,init:false},selectionModel:{check:bs,apply:R,event:bi},tableModel:{check:bv,apply:B,event:A},rowHeight:{check:H,init:20,apply:D,event:bn,themeable:true},forceLineHeight:{check:p,init:true},headerCellsVisible:{check:p,init:true,apply:bg,themeable:true},headerCellHeight:{check:O,init:16,apply:by,event:G,nullable:true,themeable:true},statusBarVisible:{check:p,init:true,apply:bA},additionalStatusBarText:{nullable:true,init:null,apply:bb},columnVisibilityButtonVisible:{check:p,init:true,apply:bq,themeable:true},metaColumnCounts:{check:bf,apply:q},focusCellOnMouseMove:{check:p,init:false,apply:be},rowFocusChangeModifiesSelection:{check:p,init:true},showCellFocusIndicator:{check:p,init:true,apply:bl},contextMenuFromDataCellsOnly:{check:p,init:true,apply:P},keepFirstVisibleRowComplete:{check:p,init:true,apply:W},alwaysUpdateCells:{check:p,init:false},resetSelectionOnHeaderClick:{check:p,init:true,apply:t},dataRowRenderer:{check:U,init:null,nullable:true,event:F},modalCellEditorPreOpenFunction:{check:n,init:null,nullable:true},newColumnMenu:{check:n,init:function(){return new qx.ui.table.columnmenu.Button();
}},newSelectionManager:{check:n,init:function(bM){return new qx.ui.table.selection.Manager(bM);
}},newSelectionModel:{check:n,init:function(bN){return new qx.ui.table.selection.Model(bN);
}},newTableColumnModel:{check:n,init:function(bO){return new qx.ui.table.columnmodel.Basic(bO);
}},newTablePane:{check:n,init:function(bP){return new qx.ui.table.pane.Pane(bP);
}},newTablePaneHeader:{check:n,init:function(bQ){return new qx.ui.table.pane.Header(bQ);
}},newTablePaneScroller:{check:n,init:function(bR){return new qx.ui.table.pane.Scroller(bR);
}},newTablePaneModel:{check:n,init:function(bS){return new qx.ui.table.pane.Model(bS);
}}},members:{__pN:null,__pO:null,__pL:null,__pM:null,__pQ:null,__pR:null,__pS:null,__pT:null,__pU:null,__pV:null,__uh:null,__ui:null,_createChildControlImpl:function(bT,bU){var bV;

switch(bT){case k:bV=new qx.ui.basic.Label();
bV.set({allowGrowX:true});
this._add(bV);
break;
case o:bV=this.getNewColumnMenu()();
bV.set({focusable:false});
var bW=bV.factory(X,{table:this});
bW.addListener(bH,this._initColumnMenu,this);
break;
}return bV||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,bT);
},_applySelectionModel:function(bX,bY){this.__pM.setSelectionModel(bX);

if(bY!=null){bY.removeListener(bI,this._onSelectionChanged,this);
}bX.addListener(bI,this._onSelectionChanged,this);
},_applyRowHeight:function(ca,cb){var cc=this._getPaneScrollerArr();

for(var i=0;i<cc.length;i++){cc[i].updateVerScrollBarMaximum();
}},_applyHeaderCellsVisible:function(cd,ce){var cf=this._getPaneScrollerArr();

for(var i=0;i<cf.length;i++){cf[i]._excludeChildControl(J);
}},_applyHeaderCellHeight:function(cg,ch){var ci=this._getPaneScrollerArr();

for(var i=0;i<ci.length;i++){ci[i].getHeader().setHeight(cg);
}},getEmptyTableModel:function(){if(!this.__pV){this.__pV=new qx.ui.table.model.Simple();
this.__pV.setColumns([]);
this.__pV.setData([]);
}return this.__pV;
},_applyTableModel:function(cj,ck){this.getTableColumnModel().init(cj.getColumnCount(),this);

if(ck!=null){ck.removeListener(bD,this._onTableModelMetaDataChanged,this);
ck.removeListener(e,this._onTableModelDataChanged,this);
}cj.addListener(bD,this._onTableModelMetaDataChanged,this);
cj.addListener(e,this._onTableModelDataChanged,this);
this._updateStatusBar();
this._updateTableData(0,cj.getRowCount(),0,cj.getColumnCount());
this._onTableModelMetaDataChanged();
if(ck&&cj.init&&typeof (cj.init)==g){cj.init(this);
}},getTableColumnModel:function(){if(!this.__pU){var co=this.__pU=this.getNewTableColumnModel()(this);
co.addListener(bw,this._onColVisibilityChanged,this);
co.addListener(b,this._onColWidthChanged,this);
co.addListener(M,this._onColOrderChanged,this);
var cn=this.getTableModel();
co.init(cn.getColumnCount(),this);
var cl=this._getPaneScrollerArr();

for(var i=0;i<cl.length;i++){var cm=cl[i];
var cp=cm.getTablePaneModel();
cp.setTableColumnModel(co);
}}return this.__pU;
},_applyStatusBarVisible:function(cq,cr){if(cq){this._showChildControl(k);
}else{this._excludeChildControl(k);
}
if(cq){this._updateStatusBar();
}},_applyAdditionalStatusBarText:function(cs,ct){this.__pQ=cs;
this._updateStatusBar();
},_applyColumnVisibilityButtonVisible:function(cu,cv){if(cu){this._showChildControl(o);
}else{this._excludeChildControl(o);
}},_applyMetaColumnCounts:function(cw,cx){var cE=cw;
var cy=this._getPaneScrollerArr();
var cC={};

if(cw>cx){var cG=qx.event.Registration.getManager(cy[0]);

for(var cH in qx.ui.table.Table.__pP){cC[cH]={};
cC[cH].capture=cG.getListeners(cy[0],cH,true);
cC[cH].bubble=cG.getListeners(cy[0],cH,false);
}}this._cleanUpMetaColumns(cE.length);
var cD=0;

for(var i=0;i<cy.length;i++){var cI=cy[i];
var cF=cI.getTablePaneModel();
cF.setFirstColumnX(cD);
cF.setMaxColumnCount(cE[i]);
cD+=cE[i];
}if(cE.length>cy.length){var cB=this.getTableColumnModel();

for(var i=cy.length;i<cE.length;i++){var cF=this.getNewTablePaneModel()(cB);
cF.setFirstColumnX(cD);
cF.setMaxColumnCount(cE[i]);
cD+=cE[i];
var cI=this.getNewTablePaneScroller()(this);
cI.setTablePaneModel(cF);
cI.addListener(bp,this._onScrollY,this);
for(cH in qx.ui.table.Table.__pP){if(!cC[cH]){break;
}
if(cC[cH].capture&&cC[cH].capture.length>0){var cz=cC[cH].capture;

for(var j=0;j<cz.length;j++){var cA=cz[j].context;

if(!cA){cA=this;
}else if(cA==cy[0]){cA=cI;
}cI.addListener(cH,cz[j].handler,cA,true);
}}
if(cC[cH].bubble&&cC[cH].bubble.length>0){var cK=cC[cH].bubble;

for(var j=0;j<cK.length;j++){var cA=cK[j].context;

if(!cA){cA=this;
}else if(cA==cy[0]){cA=cI;
}cI.addListener(cH,cK[j].handler,cA,false);
}}}var cJ=(i==cE.length-1)?1:0;
this.__pL.add(cI,{flex:cJ});
cy=this._getPaneScrollerArr();
}}for(var i=0;i<cy.length;i++){var cI=cy[i];
var cL=(i==(cy.length-1));
cI.getHeader().setHeight(this.getHeaderCellHeight());
cI.setTopRightWidget(cL?this.getChildControl(o):null);
}
if(!this.isColumnVisibilityButtonVisible()){this._excludeChildControl(o);
}this._updateScrollerWidths();
this._updateScrollBarVisibility();
},_applyFocusCellOnMouseMove:function(cM,cN){var cO=this._getPaneScrollerArr();

for(var i=0;i<cO.length;i++){cO[i].setFocusCellOnMouseMove(cM);
}},_applyShowCellFocusIndicator:function(cP,cQ){var cR=this._getPaneScrollerArr();

for(var i=0;i<cR.length;i++){cR[i].setShowCellFocusIndicator(cP);
}},_applyContextMenuFromDataCellsOnly:function(cS,cT){var cU=this._getPaneScrollerArr();

for(var i=0;i<cU.length;i++){cU[i].setContextMenuFromDataCellsOnly(cS);
}},_applyKeepFirstVisibleRowComplete:function(cV,cW){var cX=this._getPaneScrollerArr();

for(var i=0;i<cX.length;i++){cX[i].onKeepFirstVisibleRowCompleteChanged();
}},_applyResetSelectionOnHeaderClick:function(cY,da){var db=this._getPaneScrollerArr();

for(var i=0;i<db.length;i++){db[i].setResetSelectionOnHeaderClick(cY);
}},getSelectionManager:function(){return this.__pM;
},_getPaneScrollerArr:function(){return this.__pL.getChildren();
},getPaneScroller:function(dc){return this._getPaneScrollerArr()[dc];
},_cleanUpMetaColumns:function(dd){var de=this._getPaneScrollerArr();

if(de!=null){for(var i=de.length-1;i>=dd;i--){de[i].destroy();
}}},_onChangeLocale:function(df){this.updateContent();
this._updateStatusBar();
},_onSelectionChanged:function(dg){var dh=this._getPaneScrollerArr();

for(var i=0;i<dh.length;i++){dh[i].onSelectionChanged();
}this._updateStatusBar();
},_onTableModelMetaDataChanged:function(di){var dj=this._getPaneScrollerArr();

for(var i=0;i<dj.length;i++){dj[i].onTableModelMetaDataChanged();
}this._updateStatusBar();
},_onTableModelDataChanged:function(dk){var dl=dk.getData();
this._updateTableData(dl.firstRow,dl.lastRow,dl.firstColumn,dl.lastColumn,dl.removeStart,dl.removeCount);
},_updateTableData:function(dm,dn,dp,dq,dr,ds){var dt=this._getPaneScrollerArr();
if(ds){this.getSelectionModel().removeSelectionInterval(dr,dr+ds);
if(this.__pO>=dr&&this.__pO<(dr+ds)){this.setFocusedCell();
}}
for(var i=0;i<dt.length;i++){dt[i].onTableModelDataChanged(dm,dn,dp,dq);
}var du=this.getTableModel().getRowCount();

if(du!=this.__pR){this.__pR=du;
this._updateScrollBarVisibility();
this._updateStatusBar();
}},_onScrollY:function(dv){if(!this.__pS){this.__pS=true;
var dw=this._getPaneScrollerArr();

for(var i=0;i<dw.length;i++){dw[i].setScrollY(dv.getData());
}this.__pS=false;
}},_onKeyPress:function(dx){if(!this.getEnabled()){return;
}var dE=this.__pO;
var dB=true;
var dF=dx.getKeyIdentifier();

if(this.isEditing()){if(dx.getModifiers()==0){switch(dF){case bE:this.stopEditing();
var dE=this.__pO;
this.moveFocusedCell(0,1);

if(this.__pO!=dE){dB=this.startEditing();
}break;
case ba:this.cancelEditing();
this.focus();
break;
default:dB=false;
break;
}}}else{if(dx.isCtrlPressed()){dB=true;

switch(dF){case V:var dC=this.getTableModel().getRowCount();

if(dC>0){this.getSelectionModel().setSelectionInterval(0,dC-1);
}break;
default:dB=false;
break;
}}else{switch(dF){case bx:this.__pM.handleSelectKeyDown(this.__pO,dx);
break;
case E:case bE:this.startEditing();
dB=true;
break;
case L:this.setFocusedCell(this.__pN,0,true);
break;
case C:var dC=this.getTableModel().getRowCount();
this.setFocusedCell(this.__pN,dC-1,true);
break;
case bd:this.moveFocusedCell(-1,0);
break;
case I:this.moveFocusedCell(1,0);
break;
case K:this.moveFocusedCell(0,-1);
break;
case bo:this.moveFocusedCell(0,1);
break;
case f:case S:var dA=this.getPaneScroller(0);
var dD=dA.getTablePane();
var dz=this.getRowHeight();
var dy=(dF==f)?-1:1;
dC=dD.getVisibleRowCount()-1;
dA.setScrollY(dA.getScrollY()+dy*dC*dz);
this.moveFocusedCell(0,dy*dC);
break;
default:dB=false;
}}}
if(dE!=this.__pO&&this.getRowFocusChangeModifiesSelection()){this.__pM.handleMoveKeyDown(this.__pO,dx);
}
if(dB){dx.preventDefault();
dx.stopPropagation();
}},_onFocusChanged:function(dG){var dH=this._getPaneScrollerArr();

for(var i=0;i<dH.length;i++){dH[i].onFocusChanged();
}},_onColVisibilityChanged:function(dI){var dJ=this._getPaneScrollerArr();

for(var i=0;i<dJ.length;i++){dJ[i].onColVisibilityChanged();
}var dK=dI.getData();

if(this.__pT!=null&&dK.col!=null&&dK.visible!=null){this.__pT[dK.col].setVisible(dK.visible);
}this._updateScrollerWidths();
this._updateScrollBarVisibility();
},_onColWidthChanged:function(dL){var dM=this._getPaneScrollerArr();

for(var i=0;i<dM.length;i++){var dN=dL.getData();
dM[i].setColumnWidth(dN.col,dN.newWidth);
}this._updateScrollerWidths();
this._updateScrollBarVisibility();
},_onColOrderChanged:function(dO){var dP=this._getPaneScrollerArr();

for(var i=0;i<dP.length;i++){dP[i].onColOrderChanged();
}this._updateScrollerWidths();
this._updateScrollBarVisibility();
},getTablePaneScrollerAtPageX:function(dQ){var dR=this._getMetaColumnAtPageX(dQ);
return (dR!=-1)?this.getPaneScroller(dR):null;
},setFocusedCell:function(dS,dT,dU){if(!this.isEditing()&&(dS!=this.__pN||dT!=this.__pO)){if(dS===null){dS=0;
}this.__pN=dS;
this.__pO=dT;
var dV=this._getPaneScrollerArr();

for(var i=0;i<dV.length;i++){dV[i].setFocusedCell(dS,dT);
}
if(dS!==null&&dU){this.scrollCellVisible(dS,dT);
}}},resetSelection:function(){this.getSelectionModel().resetSelection();
},resetCellFocus:function(){this.setFocusedCell(null,null,false);
},getFocusedColumn:function(){return this.__pN;
},getFocusedRow:function(){return this.__pO;
},highlightFocusedRow:function(dW){this.getDataRowRenderer().setHighlightFocusRow(dW);
},clearFocusedRowHighlight:function(dX){if(dX){var ea=dX.getRelatedTarget();

if(ea instanceof qx.ui.table.pane.Pane||ea instanceof qx.ui.table.pane.FocusIndicator){return;
}}this.resetCellFocus();
var dY=this._getPaneScrollerArr();

for(var i=0;i<dY.length;i++){dY[i].onFocusChanged();
}},moveFocusedCell:function(eb,ec){var eg=this.__pN;
var eh=this.__pO;
if(eg==null||eh==null){return;
}
if(eb!=0){var ef=this.getTableColumnModel();
var x=ef.getVisibleX(eg);
var ee=ef.getVisibleColumnCount();
x=qx.lang.Number.limit(x+eb,0,ee-1);
eg=ef.getVisibleColumnAtX(x);
}
if(ec!=0){var ed=this.getTableModel();
eh=qx.lang.Number.limit(eh+ec,0,ed.getRowCount()-1);
}this.setFocusedCell(eg,eh,true);
},scrollCellVisible:function(ei,ej){var ek=this.getContentElement().getDomElement();
if(!ek){this.addListenerOnce(bH,function(){this.scrollCellVisible(ei,ej);
},this);
}var el=this.getTableColumnModel();
var x=el.getVisibleX(ei);
var em=this._getMetaColumnAtColumnX(x);

if(em!=-1){this.getPaneScroller(em).scrollCellVisible(ei,ej);
}},isEditing:function(){if(this.__pN!=null){var x=this.getTableColumnModel().getVisibleX(this.__pN);
var en=this._getMetaColumnAtColumnX(x);
return this.getPaneScroller(en).isEditing();
}return false;
},startEditing:function(){if(this.__pN!=null){var x=this.getTableColumnModel().getVisibleX(this.__pN);
var ep=this._getMetaColumnAtColumnX(x);
var eo=this.getPaneScroller(ep).startEditing();
return eo;
}return false;
},stopEditing:function(){if(this.__pN!=null){var x=this.getTableColumnModel().getVisibleX(this.__pN);
var eq=this._getMetaColumnAtColumnX(x);
this.getPaneScroller(eq).stopEditing();
}},cancelEditing:function(){if(this.__pN!=null){var x=this.getTableColumnModel().getVisibleX(this.__pN);
var er=this._getMetaColumnAtColumnX(x);
this.getPaneScroller(er).cancelEditing();
}},updateContent:function(){var es=this._getPaneScrollerArr();

for(var i=0;i<es.length;i++){es[i].getTablePane().updateContent(true);
}},blockHeaderElements:function(){var et=this._getPaneScrollerArr();

for(var i=0;i<et.length;i++){et[i].getHeader().getBlocker().blockContent(20);
}this.getChildControl(o).getBlocker().blockContent(20);
},unblockHeaderElements:function(){var eu=this._getPaneScrollerArr();

for(var i=0;i<eu.length;i++){eu[i].getHeader().getBlocker().unblockContent();
}this.getChildControl(o).getBlocker().unblockContent();
},_getMetaColumnAtPageX:function(ev){var ew=this._getPaneScrollerArr();

for(var i=0;i<ew.length;i++){var ex=ew[i].getContainerLocation();

if(ev>=ex.left&&ev<=ex.right){return i;
}}return -1;
},_getMetaColumnAtColumnX:function(ey){var eA=this.getMetaColumnCounts();
var eB=0;

for(var i=0;i<eA.length;i++){var ez=eA[i];
eB+=ez;

if(ez==-1||ey<eB){return i;
}}return -1;
},_updateStatusBar:function(){var eC=this.getTableModel();

if(this.getStatusBarVisible()){var eD=this.getSelectionModel().getSelectedCount();
var eF=eC.getRowCount();
var eE;

if(eF>=0){if(eD==0){eE=this.trn(br,Y,eF,eF);
}else{eE=this.trn(c,bt,eF,eD,eF);
}}
if(this.__pQ){if(eE){eE+=this.__pQ;
}else{eE=this.__pQ;
}}
if(eE){this.getChildControl(k).setValue(eE);
}}},_updateScrollerWidths:function(){var eG=this._getPaneScrollerArr();

for(var i=0;i<eG.length;i++){var eI=(i==(eG.length-1));
var eJ=eG[i].getTablePaneModel().getTotalWidth();
eG[i].setPaneWidth(eJ);
var eH=eI?1:0;
eG[i].setLayoutProperties({flex:eH});
}},_updateScrollBarVisibility:function(){if(!this.getBounds()){return;
}var eN=qx.ui.table.pane.Scroller.HORIZONTAL_SCROLLBAR;
var eP=qx.ui.table.pane.Scroller.VERTICAL_SCROLLBAR;
var eK=this._getPaneScrollerArr();
var eM=false;
var eO=false;

for(var i=0;i<eK.length;i++){var eQ=(i==(eK.length-1));
var eL=eK[i].getNeededScrollBars(eM,!eQ);

if(eL&eN){eM=true;
}
if(eQ&&(eL&eP)){eO=true;
}}for(var i=0;i<eK.length;i++){var eQ=(i==(eK.length-1));
eK[i].setHorizontalScrollBarVisible(eM);
if(eQ){if(this.__uh==null){this.__uh=eK[i].getVerticalScrollBarVisible();
this.__ui=qx.event.Timer.once(function(){this.__uh=null;
this.__ui=null;
},this,0);
}}eK[i].setVerticalScrollBarVisible(eQ&&eO);
if(eQ&&eO!=this.__uh){this.fireDataEvent(bj,eO);
}}},_initColumnMenu:function(){var eT=this.getTableModel();
var eU=this.getTableColumnModel();
var eV=this.getChildControl(o);
eV.empty();
var eS=eV.getMenu();
var eW={table:this,menu:eS,columnButton:eV};
this.fireDataEvent(bz,eW);
this.__pT={};

for(var eX=0,l=eT.getColumnCount();eX<l;eX++){var eR=eV.factory(T,{text:eT.getColumnName(eX),column:eX,bVisible:eU.isColumnVisible(eX)});
qx.core.Assert.assertInterface(eR,qx.ui.table.IColumnMenuItem);
eR.addListener(s,this._createColumnVisibilityCheckBoxHandler(eX),this);
this.__pT[eX]=eR;
}eW={table:this,menu:eS,columnButton:eV};
this.fireDataEvent(u,eW);
},_createColumnVisibilityCheckBoxHandler:function(eY){return function(fa){var fb=this.getTableColumnModel();
fb.setColumnVisible(eY,fa.getData());
};
},setColumnWidth:function(fc,fd){this.getTableColumnModel().setColumnWidth(fc,fd);
},_onResize:function(){this.fireEvent(bh);
this._updateScrollerWidths();
this._updateScrollBarVisibility();
},addListener:function(fe,ff,self,fg){if(this.self(arguments).__pP[fe]){var fi=[fe];

for(var i=0,fh=this._getPaneScrollerArr();i<fh.length;i++){fi.push(fh[i].addListener.apply(fh[i],arguments));
}return fi.join(bF);
}else{return qx.ui.core.Widget.prototype.addListener.call(this,fe,ff,self,fg);
}},removeListener:function(fj,fk,self,fl){if(this.self(arguments).__pP[fj]){for(var i=0,fm=this._getPaneScrollerArr();i<fm.length;i++){fm[i].removeListener.apply(fm[i],arguments);
}}else{qx.ui.core.Widget.prototype.removeListener.call(this,fj,fk,self,fl);
}},removeListenerById:function(fn){var fr=fn.split(bF);
var fq=fr.shift();

if(this.self(arguments).__pP[fq]){var fp=true;

for(var i=0,fo=this._getPaneScrollerArr();i<fo.length;i++){fp=fo[i].removeListenerById.call(fo[i],fr[i])&&fp;
}return fp;
}else{return qx.ui.core.Widget.prototype.removeListenerById.call(this,fn);
}},destroy:function(){this.getChildControl(o).getMenu().destroy();
qx.ui.core.Widget.prototype.destroy.call(this);
}},destruct:function(){if(qx.core.Variant.isSet(bG,bB)){qx.locale.Manager.getInstance().removeListener(d,this._onChangeLocale,this);
}var ft=this.getSelectionModel();

if(ft){ft.dispose();
}var fs=this.getDataRowRenderer();

if(fs){fs.dispose();
}this._cleanUpMetaColumns(0);
this.getTableColumnModel().dispose();
this._disposeObjects(v,bm,bC,bC,bu,z);
this._disposeMap(a);
}});
})();
(function(){var a="qx.ui.table.IRowRenderer";
qx.Interface.define(a,{members:{updateDataRowElement:function(b,c){},getRowHeightStyle:function(d){},createRowStyle:function(e){},getRowClass:function(f){}}});
})();
(function(){var t="",s="table-row-background-even",r="table-row-background-selected",q="table-row",p="background-color:",o="table-row-background-focused",n=';border-bottom: 1px solid ',m=';color:',l="table-row-selected",k="table-row-background-odd",d="default",j="table-row-background-focused-selected",g="qx.ui.table.rowrenderer.Default",c="table-row-line",b="'",f="height:",e=";",h="px;",a="1px solid ",i="Boolean";
qx.Class.define(g,{extend:qx.core.Object,implement:qx.ui.table.IRowRenderer,construct:function(){qx.core.Object.call(this);
this.__pW=t;
this.__pW={};
this._colors={};
this._renderFont(qx.theme.manager.Font.getInstance().resolve(d));
var u=qx.theme.manager.Color.getInstance();
this._colors.bgcolFocusedSelected=u.resolve(j);
this._colors.bgcolFocused=u.resolve(o);
this._colors.bgcolSelected=u.resolve(r);
this._colors.bgcolEven=u.resolve(s);
this._colors.bgcolOdd=u.resolve(k);
this._colors.colSelected=u.resolve(l);
this._colors.colNormal=u.resolve(q);
this._colors.horLine=u.resolve(c);
},properties:{highlightFocusRow:{check:i,init:true}},members:{_colors:null,__pY:null,__pW:null,_insetY:1,_renderFont:function(v){if(v){this.__pY=v.getStyles();
this.__pW=qx.bom.element.Style.compile(this.__pY);
this.__pW=this.__pW.replace(/"/g,b);
}else{this.__pW=t;
this.__pY=qx.bom.Font.getDefaultStyles();
}},updateDataRowElement:function(w,x){var z=this.__pY;
var y=x.style;
qx.bom.element.Style.setStyles(x,z);

if(w.focusedRow&&this.getHighlightFocusRow()){y.backgroundColor=w.selected?this._colors.bgcolFocusedSelected:this._colors.bgcolFocused;
}else{if(w.selected){y.backgroundColor=this._colors.bgcolSelected;
}else{y.backgroundColor=(w.row%2==0)?this._colors.bgcolEven:this._colors.bgcolOdd;
}}y.color=w.selected?this._colors.colSelected:this._colors.colNormal;
y.borderBottom=a+this._colors.horLine;
},getRowHeightStyle:function(A){if(qx.bom.client.Feature.CONTENT_BOX){A-=this._insetY;
}return f+A+h;
},createRowStyle:function(B){var C=[];
C.push(e);
C.push(this.__pW);
C.push(p);

if(B.focusedRow&&this.getHighlightFocusRow()){C.push(B.selected?this._colors.bgcolFocusedSelected:this._colors.bgcolFocused);
}else{if(B.selected){C.push(this._colors.bgcolSelected);
}else{C.push((B.row%2==0)?this._colors.bgcolEven:this._colors.bgcolOdd);
}}C.push(m);
C.push(B.selected?this._colors.colSelected:this._colors.colNormal);
C.push(n,this._colors.horLine);
return C.join(t);
},getRowClass:function(D){return t;
},getRowAttributes:function(E){return t;
}},destruct:function(){this._colors=this.__pY=this.__pW=null;
}});
})();
(function(){var a="qx.ui.table.IColumnMenuButton";
qx.Interface.define(a,{properties:{menu:{}},members:{factory:function(b,c){return true;
},empty:function(){return true;
}}});
})();
(function(){var f="menu-button",e="table-column-reset-button",d="separator",c="user-button",b="qx.ui.table.columnmenu.Button",a="menu";
qx.Class.define(b,{extend:qx.ui.form.MenuButton,implement:qx.ui.table.IColumnMenuButton,construct:function(){qx.ui.form.MenuButton.call(this);
this.__qa=new qx.ui.core.Blocker(this);
},members:{__qb:null,__qa:null,factory:function(g,h){switch(g){case a:var j=new qx.ui.menu.Menu();
this.setMenu(j);
return j;
case f:var m=new qx.ui.table.columnmenu.MenuItem(h.text);
m.setVisible(h.bVisible);
this.getMenu().add(m);
return m;
case c:var k=new qx.ui.menu.Button(h.text);
k.set({appearance:e});
return k;
case d:return new qx.ui.menu.Separator();
default:throw new Error("Unrecognized factory request: "+g);
}},getBlocker:function(){return this.__qa;
},empty:function(){var n=this.getMenu();
var o=n.getChildren();

for(var i=0,l=o.length;i<l;i++){o[0].destroy();
}}},destruct:function(){this.__qa.dispose();
}});
})();
(function(){var b="qx.ui.table.IColumnMenuItem",a="qx.event.type.Data";
qx.Interface.define(b,{properties:{visible:{}},events:{changeVisible:a}});
})();
(function(){var b="qx.ui.form.IBooleanForm",a="qx.event.type.Data";
qx.Interface.define(b,{events:{"changeValue":a},members:{setValue:function(c){return arguments.length==1;
},resetValue:function(){},getValue:function(){}}});
})();
(function(){var h="checked",g="menu-checkbox",f="Boolean",d="_applyValue",c="changeValue",b="qx.ui.menu.CheckBox",a="execute";
qx.Class.define(b,{extend:qx.ui.menu.AbstractButton,implement:[qx.ui.form.IBooleanForm],construct:function(i,j){qx.ui.menu.AbstractButton.call(this);
if(i!=null){if(i.translate){this.setLabel(i.translate());
}else{this.setLabel(i);
}}
if(j!=null){this.setMenu(j);
}this.addListener(a,this._onExecute,this);
},properties:{appearance:{refine:true,init:g},value:{check:f,init:false,apply:d,event:c,nullable:true}},members:{_applyValue:function(k,l){k?this.addState(h):this.removeState(h);
},_onExecute:function(e){this.toggleValue();
},_onMouseUp:function(e){if(e.isLeftPressed()){this.execute();
}qx.ui.menu.Manager.getInstance().hideAll();
},_onKeyPress:function(e){this.execute();
}}});
})();
(function(){var f="changeVisible",d="qx.ui.table.columnmenu.MenuItem",c="_applyVisible",b="Boolean",a="changeValue";
qx.Class.define(d,{extend:qx.ui.menu.CheckBox,implement:qx.ui.table.IColumnMenuItem,properties:{visible:{check:b,init:true,apply:c,event:f}},construct:function(g){qx.ui.menu.CheckBox.call(this,g);
this.addListener(a,function(e){this.bInListener=true;
this.setVisible(e.getData());
this.bInListener=false;
});
},members:{__qw:false,_applyVisible:function(h,i){if(!this.bInListener){this.setValue(h);
}}}});
})();
(function(){var b="qx.ui.table.selection.Model",a="qx.ui.table.selection.Manager";
qx.Class.define(a,{extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
},properties:{selectionModel:{check:b}},members:{__qx:null,handleMouseDown:function(c,d){if(d.isLeftPressed()){var e=this.getSelectionModel();

if(!e.isSelectedIndex(c)){this._handleSelectEvent(c,d);
this.__qx=true;
}else{this.__qx=false;
}}else if(d.isRightPressed()&&d.getModifiers()==0){var e=this.getSelectionModel();

if(!e.isSelectedIndex(c)){e.setSelectionInterval(c,c);
}}},handleMouseUp:function(f,g){if(g.isLeftPressed()&&!this.__qx){this._handleSelectEvent(f,g);
}},handleClick:function(h,i){},handleSelectKeyDown:function(j,k){this._handleSelectEvent(j,k);
},handleMoveKeyDown:function(l,m){var o=this.getSelectionModel();

switch(m.getModifiers()){case 0:o.setSelectionInterval(l,l);
break;
case qx.event.type.Dom.SHIFT_MASK:var n=o.getAnchorSelectionIndex();

if(n==-1){o.setSelectionInterval(l,l);
}else{o.setSelectionInterval(n,l);
}break;
}},_handleSelectEvent:function(p,q){var t=this.getSelectionModel();
var r=t.getLeadSelectionIndex();
var s=t.getAnchorSelectionIndex();

if(q.isShiftPressed()){if(p!=r||t.isSelectionEmpty()){if(s==-1){s=p;
}
if(q.isCtrlOrCommandPressed()){t.addSelectionInterval(s,p);
}else{t.setSelectionInterval(s,p);
}}}else if(q.isCtrlOrCommandPressed()){if(t.isSelectedIndex(p)){t.removeSelectionInterval(p,p);
}else{t.addSelectionInterval(p,p);
}}else{t.setSelectionInterval(p,p);
}}}});
})();
(function(){var l="]",k="..",h="changeSelection",g="_applySelectionMode",f='ie',d="qx.event.type.Event",c="Ranges:",b="qx.ui.table.selection.Model",a=" [";
qx.Class.define(b,{extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__qy=[];
this.__qz=-1;
this.__qA=-1;
this.hasBatchModeRefCount=0;
this.__qB=false;
},events:{"changeSelection":d},statics:{NO_SELECTION:1,SINGLE_SELECTION:2,SINGLE_INTERVAL_SELECTION:3,MULTIPLE_INTERVAL_SELECTION:4,MULTIPLE_INTERVAL_SELECTION_TOGGLE:5},properties:{selectionMode:{init:2,check:[1,2,3,4,5],apply:g}},members:{__qB:null,__qz:null,__qA:null,__qy:null,_applySelectionMode:function(m){this.resetSelection();
},setBatchMode:function(n){if(n){this.hasBatchModeRefCount+=1;
}else{if(this.hasBatchModeRefCount==0){throw new Error("Try to turn off batch mode althoug it was not turned on.");
}this.hasBatchModeRefCount-=1;

if(this.__qB){this.__qB=false;
this._fireChangeSelection();
}}return this.hasBatchMode();
},hasBatchMode:function(){return this.hasBatchModeRefCount>0;
},getAnchorSelectionIndex:function(){return this.__qz;
},_setAnchorSelectionIndex:function(o){this.__qz=o;
},getLeadSelectionIndex:function(){return this.__qA;
},_setLeadSelectionIndex:function(p){this.__qA=p;
},_getSelectedRangeArr:function(){return this.__qy;
},resetSelection:function(){if(!this.isSelectionEmpty()){this._resetSelection();
this._fireChangeSelection();
}},isSelectionEmpty:function(){return this.__qy.length==0;
},getSelectedCount:function(){var r=0;

for(var i=0;i<this.__qy.length;i++){var q=this.__qy[i];
r+=q.maxIndex-q.minIndex+1;
}return r;
},isSelectedIndex:function(s){for(var i=0;i<this.__qy.length;i++){var t=this.__qy[i];

if(s>=t.minIndex&&s<=t.maxIndex){return true;
}}return false;
},getSelectedRanges:function(){var u=[];

for(var i=0;i<this.__qy.length;i++){u.push({minIndex:this.__qy[i].minIndex,maxIndex:this.__qy[i].maxIndex});
}return u;
},iterateSelection:function(v,w){for(var i=0;i<this.__qy.length;i++){for(var j=this.__qy[i].minIndex;j<=this.__qy[i].maxIndex;j++){v.call(w,j);
}}},setSelectionInterval:function(x,y){var z=this.self(arguments);

switch(this.getSelectionMode()){case z.NO_SELECTION:return;
case z.SINGLE_SELECTION:if(this.isSelectedIndex(y)){return;
}x=y;
break;
case z.MULTIPLE_INTERVAL_SELECTION_TOGGLE:this.setBatchMode(true);

try{for(var i=x;i<=y;i++){if(!this.isSelectedIndex(i)){this._addSelectionInterval(i,i);
}else{this.removeSelectionInterval(i,i);
}}}catch(e){if(qx.bom.client.Browser.NAME==f&&qx.bom.client.Browser.VERSION<=7){this.setBatchMode(false);
}throw e;
}finally{this.setBatchMode(false);
}this._fireChangeSelection();
return;
}this._resetSelection();
this._addSelectionInterval(x,y);
this._fireChangeSelection();
},addSelectionInterval:function(A,B){var C=qx.ui.table.selection.Model;

switch(this.getSelectionMode()){case C.NO_SELECTION:return;
case C.MULTIPLE_INTERVAL_SELECTION:case C.MULTIPLE_INTERVAL_SELECTION_TOGGLE:this._addSelectionInterval(A,B);
this._fireChangeSelection();
break;
default:this.setSelectionInterval(A,B);
break;
}},removeSelectionInterval:function(D,E){this.__qz=D;
this.__qA=E;
var F=Math.min(D,E);
var H=Math.max(D,E);
for(var i=0;i<this.__qy.length;i++){var J=this.__qy[i];

if(J.minIndex>H){break;
}else if(J.maxIndex>=F){var K=(J.minIndex>=F)&&(J.minIndex<=H);
var I=(J.maxIndex>=F)&&(J.maxIndex<=H);

if(K&&I){this.__qy.splice(i,1);
i--;
}else if(K){J.minIndex=H+1;
}else if(I){J.maxIndex=F-1;
}else{var G={minIndex:H+1,maxIndex:J.maxIndex};
this.__qy.splice(i+1,0,G);
J.maxIndex=F-1;
break;
}}}this._fireChangeSelection();
},_resetSelection:function(){this.__qy=[];
this.__qz=-1;
this.__qA=-1;
},_addSelectionInterval:function(L,M){this.__qz=L;
this.__qA=M;
var N=Math.min(L,M);
var P=Math.max(L,M);
var O=0;

for(;O<this.__qy.length;O++){var Q=this.__qy[O];

if(Q.minIndex>N){break;
}}this.__qy.splice(O,0,{minIndex:N,maxIndex:P});
var R=this.__qy[0];

for(var i=1;i<this.__qy.length;i++){var Q=this.__qy[i];

if(R.maxIndex+1>=Q.minIndex){R.maxIndex=Math.max(R.maxIndex,Q.maxIndex);
this.__qy.splice(i,1);
i--;
}else{R=Q;
}}},_dumpRanges:function(){var S=c;

for(var i=0;i<this.__qy.length;i++){var T=this.__qy[i];
S+=a+T.minIndex+k+T.maxIndex+l;
}this.debug(S);
},_fireChangeSelection:function(){if(this.hasBatchMode()){this.__qB=true;
}else{this.fireEvent(h);
}}},destruct:function(){this.__qy=null;
}});
})();
(function(){var a="qx.ui.table.ICellEditorFactory";
qx.Interface.define(a,{members:{createCellEditor:function(b){return true;
},getCellEditorValue:function(c){return true;
}}});
})();
(function(){var f="",e="Function",d="abstract",c="number",b="appear",a="qx.ui.table.celleditor.AbstractField";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.ui.table.ICellEditorFactory,type:d,properties:{validationFunction:{check:e,nullable:true,init:null}},members:{_createEditor:function(){throw new Error("Abstract method call!");
},createCellEditor:function(g){var h=this._createEditor();
h.originalValue=g.value;

if(g.value===null||g.value===undefined){g.value=f;
}h.setValue(f+g.value);
h.addListener(b,function(){h.selectAllText();
});
return h;
},getCellEditorValue:function(i){var k=i.getValue();
var j=this.getValidationFunction();

if(j){k=j(k,i.originalValue);
}
if(typeof i.originalValue==c){k=parseFloat(k);
}return k;
}}});
})();
(function(){var c="number",b="qx.ui.table.celleditor.TextField",a="table-editor-textfield";
qx.Class.define(b,{extend:qx.ui.table.celleditor.AbstractField,members:{getCellEditorValue:function(d){var f=d.getValue();
var e=this.getValidationFunction();

if(e){f=e(f,d.originalValue);
}
if(typeof d.originalValue==c){if(f!=null){f=parseFloat(f);
}}return f;
},_createEditor:function(){var g=new qx.ui.form.TextField();
g.setAppearance(a);
return g;
}}});
})();
(function(){var a="qx.ui.table.IHeaderRenderer";
qx.Interface.define(a,{members:{createHeaderCell:function(b){return true;
},updateHeaderCell:function(c,d){return true;
}}});
})();
(function(){var b="qx.ui.table.headerrenderer.Default",a="String";
qx.Class.define(b,{extend:qx.core.Object,implement:qx.ui.table.IHeaderRenderer,statics:{STATE_SORTED:"sorted",STATE_SORTED_ASCENDING:"sortedAscending"},properties:{toolTip:{check:a,init:null,nullable:true}},members:{createHeaderCell:function(c){var d=new qx.ui.table.headerrenderer.HeaderCell();
this.updateHeaderCell(c,d);
return d;
},updateHeaderCell:function(e,f){var g=qx.ui.table.headerrenderer.Default;
if(e.name&&e.name.translate){f.setLabel(e.name.translate());
}else{f.setLabel(e.name);
}var h=f.getToolTip();

if(this.getToolTip()!=null){if(h==null){h=new qx.ui.tooltip.ToolTip(this.getToolTip());
f.setToolTip(h);
qx.util.DisposeUtil.disposeTriggeredBy(h,f);
}else{h.setLabel(this.getToolTip());
}}e.sorted?f.addState(g.STATE_SORTED):f.removeState(g.STATE_SORTED);
e.sortedAscending?f.addState(g.STATE_SORTED_ASCENDING):f.removeState(g.STATE_SORTED_ASCENDING);
}}});
})();
(function(){var a="qx.ui.table.ICellRenderer";
qx.Interface.define(a,{members:{createDataCellHtml:function(b,c){return true;
}}});
})();
(function(){var j="",i="px;",h=".qooxdoo-table-cell {",g="qooxdoo-table-cell",f='" ',e="nowrap",d="default",c="qx.client",b="}",a="width:",H=".qooxdoo-table-cell-right { text-align:right } ",G="0px 6px",F='<div class="',E="0px",D="height:",C="1px solid ",B=".qooxdoo-table-cell-bold { font-weight:bold } ",A="String",z="} ",y='>',q="mshtml",r='</div>',o="ellipsis",p="content-box",m='left:',n="qx.ui.table.cellrenderer.Abstract",k='" style="',l="abstract",s="none",t="hidden",v="table-column-line",u='px;',x=".qooxdoo-table-cell-italic { font-style:italic} ",w="absolute";
qx.Class.define(n,{type:l,implement:qx.ui.table.ICellRenderer,extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
var I=qx.ui.table.cellrenderer.Abstract;

if(!I.__pf){var K=qx.theme.manager.Color.getInstance();
I.__pf=this.self(arguments);
var J=h+
qx.bom.element.Style.compile({position:w,top:E,overflow:t,whiteSpace:e,borderRight:C+K.resolve(v),padding:G,cursor:d,textOverflow:o,userSelect:s})+z+H+x+B;

if(!qx.core.Variant.isSet(c,q)){J+=h+qx.bom.element.BoxSizing.compile(p)+b;
}I.__pf.stylesheet=qx.bom.Stylesheet.createElement(J);
}},properties:{defaultCellStyle:{init:null,check:A,nullable:true}},members:{_insetX:6+6+1,_insetY:0,_getCellClass:function(L){return g;
},_getCellStyle:function(M){return M.style||j;
},_getCellAttributes:function(N){return j;
},_getContentHtml:function(O){return O.value||j;
},_getCellSizeStyle:function(P,Q,R,S){var T=j;

if(qx.bom.client.Feature.CONTENT_BOX){P-=R;
Q-=S;
}T+=a+Math.max(P,0)+i;
T+=D+Math.max(Q,0)+i;
return T;
},createDataCellHtml:function(U,V){V.push(F,this._getCellClass(U),k,m,U.styleLeft,u,this._getCellSizeStyle(U.styleWidth,U.styleHeight,this._insetX,this._insetY),this._getCellStyle(U),f,this._getCellAttributes(U),y+this._getContentHtml(U),r);
}}});
})();
(function(){var h="",g="number",f="Boolean",e="qx.ui.table.cellrenderer.Default",d=" qooxdoo-table-cell-bold",c=" qooxdoo-table-cell-right",b=" qooxdoo-table-cell-italic",a="string";
qx.Class.define(e,{extend:qx.ui.table.cellrenderer.Abstract,statics:{STYLEFLAG_ALIGN_RIGHT:1,STYLEFLAG_BOLD:2,STYLEFLAG_ITALIC:4,_numberFormat:null},properties:{useAutoAlign:{check:f,init:true}},members:{_getStyleFlags:function(i){if(this.getUseAutoAlign()){if(typeof i.value==g){return qx.ui.table.cellrenderer.Default.STYLEFLAG_ALIGN_RIGHT;
}}return 0;
},_getCellClass:function(j){var k=qx.ui.table.cellrenderer.Abstract.prototype._getCellClass.call(this,j);

if(!k){return h;
}var l=this._getStyleFlags(j);

if(l&qx.ui.table.cellrenderer.Default.STYLEFLAG_ALIGN_RIGHT){k+=c;
}
if(l&qx.ui.table.cellrenderer.Default.STYLEFLAG_BOLD){k+=d;
}
if(l&qx.ui.table.cellrenderer.Default.STYLEFLAG_ITALIC){k+=b;
}return k;
},_getContentHtml:function(m){return qx.bom.String.escape(this._formatValue(m));
},_formatValue:function(n){var p=n.value;
var o;

if(p==null){return h;
}
if(typeof p==a){return p;
}else if(typeof p==g){if(!qx.ui.table.cellrenderer.Default._numberFormat){qx.ui.table.cellrenderer.Default._numberFormat=new qx.util.format.NumberFormat();
qx.ui.table.cellrenderer.Default._numberFormat.setMaximumFractionDigits(2);
}var o=qx.ui.table.cellrenderer.Default._numberFormat.format(p);
}else if(p instanceof Date){o=qx.util.format.DateFormat.getDateInstance().format(p);
}else{o=p;
}return o;
}}});
})();
(function(){var k="qx.event.type.Data",j="visibilityChanged",h="orderChanged",g="visibilityChangedPre",f="widthChanged",e="qx.ui.table.columnmodel.Basic",d="__pm",c="headerCellRendererChanged",b="__pn",a="__pl";
qx.Class.define(e,{extend:qx.core.Object,construct:function(){qx.core.Object.call(this);
this.__pg=[];
this.__ph=[];
},events:{"widthChanged":k,"visibilityChangedPre":k,"visibilityChanged":k,"orderChanged":k,"headerCellRendererChanged":k},statics:{DEFAULT_WIDTH:100,DEFAULT_HEADER_RENDERER:qx.ui.table.headerrenderer.Default,DEFAULT_DATA_RENDERER:qx.ui.table.cellrenderer.Default,DEFAULT_EDITOR_FACTORY:qx.ui.table.celleditor.TextField},members:{__pi:null,__pj:null,__ph:null,__pg:null,__pk:null,__pl:null,__pm:null,__pn:null,init:function(l,m){{};
this.__pk=[];
var q=qx.ui.table.columnmodel.Basic.DEFAULT_WIDTH;
var r=this.__pl||(this.__pl=new qx.ui.table.columnmodel.Basic.DEFAULT_HEADER_RENDERER());
var o=this.__pm||(this.__pm=new qx.ui.table.columnmodel.Basic.DEFAULT_DATA_RENDERER());
var n=this.__pn||(this.__pn=new qx.ui.table.columnmodel.Basic.DEFAULT_EDITOR_FACTORY());
this.__pg=[];
this.__ph=[];
var t;
if(m){t=m.getInitiallyHiddenColumns();
}t=t||[];

for(var u=0;u<l;u++){this.__pk[u]={width:q,headerRenderer:r,dataRenderer:o,editorFactory:n};
this.__pg[u]=u;
this.__ph[u]=u;
}this.__pj=null;
this.__pi=true;

for(var s=0;s<t.length;s++){this.setColumnVisible(t[s],false);
}this.__pi=false;

for(u=0;u<l;u++){var p={col:u,visible:this.isColumnVisible(u)};
this.fireDataEvent(g,p);
this.fireDataEvent(j,p);
}},getVisibleColumns:function(){return this.__ph!=null?this.__ph:[];
},setColumnWidth:function(v,w,y){{};
var A=this.__pk[v].width;

if(A!=w){this.__pk[v].width=w;
var z={col:v,newWidth:w,oldWidth:A,isMouseAction:y||false};
this.fireDataEvent(f,z);
}},getColumnWidth:function(B){{};
return this.__pk[B].width;
},setHeaderCellRenderer:function(C,D){{};
var E=this.__pk[C].headerRenderer;

if(E!==this.__pl){E.dispose();
}this.__pk[C].headerRenderer=D;
this.fireDataEvent(c,{col:C});
},getHeaderCellRenderer:function(F){{};
return this.__pk[F].headerRenderer;
},setDataCellRenderer:function(G,H){{};
this.__pk[G].dataRenderer=H;
var I=this.__pk[G].dataRenderer;

if(I!==this.__pm){return I;
}return null;
},getDataCellRenderer:function(J){{};
return this.__pk[J].dataRenderer;
},setCellEditorFactory:function(K,L){{};
var M=this.__pk[K].headerRenderer;

if(M!==this.__pn){M.dispose();
}this.__pk[K].editorFactory=L;
},getCellEditorFactory:function(N){{};
return this.__pk[N].editorFactory;
},_getColToXPosMap:function(){if(this.__pj==null){this.__pj={};

for(var Q=0;Q<this.__pg.length;Q++){var P=this.__pg[Q];
this.__pj[P]={overX:Q};
}
for(var O=0;O<this.__ph.length;O++){var P=this.__ph[O];
this.__pj[P].visX=O;
}}return this.__pj;
},getVisibleColumnCount:function(){return this.__ph!=null?this.__ph.length:0;
},getVisibleColumnAtX:function(R){{};
return this.__ph[R];
},getVisibleX:function(S){{};
return this._getColToXPosMap()[S].visX;
},getOverallColumnCount:function(){return this.__pg.length;
},getOverallColumnAtX:function(T){{};
return this.__pg[T];
},getOverallX:function(U){{};
return this._getColToXPosMap()[U].overX;
},isColumnVisible:function(V){{};
return (this._getColToXPosMap()[V].visX!=null);
},setColumnVisible:function(W,X){{};

if(X!=this.isColumnVisible(W)){if(X){var be=this._getColToXPosMap();
var bb=be[W].overX;

if(bb==null){throw new Error("Showing column failed: "+W+". The column is not added to this TablePaneModel.");
}var bc;

for(var x=bb+1;x<this.__pg.length;x++){var bd=this.__pg[x];
var Y=be[bd].visX;

if(Y!=null){bc=Y;
break;
}}if(bc==null){bc=this.__ph.length;
}this.__ph.splice(bc,0,W);
}else{var ba=this.getVisibleX(W);
this.__ph.splice(ba,1);
}this.__pj=null;
if(!this.__pi){var bf={col:W,visible:X};
this.fireDataEvent(g,bf);
this.fireDataEvent(j,bf);
}}},moveColumn:function(bg,bh){{};
this.__pi=true;
var bk=this.__pg[bg];
var bi=this.isColumnVisible(bk);

if(bi){this.setColumnVisible(bk,false);
}this.__pg.splice(bg,1);
this.__pg.splice(bh,0,bk);
this.__pj=null;

if(bi){this.setColumnVisible(bk,true);
}this.__pi=false;
var bj={col:bk,fromOverXPos:bg,toOverXPos:bh};
this.fireDataEvent(h,bj);
},setColumnsOrder:function(bl){{};

if(bl.length==this.__pg.length){this.__pi=true;
var bo=new Array(bl.length);

for(var bm=0;bm<this.__pg.length;bm++){var bn=this.isColumnVisible(bm);
bo[bm]=bn;

if(bn){this.setColumnVisible(bm,false);
}}this.__pg=qx.lang.Array.clone(bl);
this.__pj=null;
for(var bm=0;bm<this.__pg.length;bm++){if(bo[bm]){this.setColumnVisible(bm,true);
}}this.__pi=false;
this.fireDataEvent(h);
}else{throw new Error("setColumnsOrder: Invalid number of column positions given, expected "+this.__pg.length+", got "+bl.length);
}}},destruct:function(){for(var i=0;i<this.__pk.length;i++){this.__pk[i].headerRenderer.dispose();
this.__pk[i].dataRenderer.dispose();
this.__pk[i].editorFactory.dispose();
}this.__pg=this.__ph=this.__pk=this.__pj=null;
this._disposeObjects(a,d,b);
}});
})();
(function(){var m="qx.dynlocale",l="Boolean",k="changeLocale",j="changeInvalidMessage",i="on",h="String",g="invalid",f="",d="qx.ui.form.MForm",c="_applyValid",a="changeRequired",b="changeValid";
qx.Mixin.define(d,{construct:function(){if(qx.core.Variant.isSet(m,i)){qx.locale.Manager.getInstance().addListener(k,this.__lz,this);
}},properties:{valid:{check:l,init:true,apply:c,event:b},required:{check:l,init:false,event:a},invalidMessage:{check:h,init:f,event:j},requiredInvalidMessage:{check:h,nullable:true,event:j}},members:{_applyValid:function(n,o){n?this.removeState(g):this.addState(g);
},__lz:qx.core.Variant.select(m,{"on":function(e){var p=this.getInvalidMessage();

if(p&&p.translate){this.setInvalidMessage(p.translate());
}var q=this.getRequiredInvalidMessage();

if(q&&q.translate){this.setRequiredInvalidMessage(q.translate());
}},"off":null})},destruct:function(){if(qx.core.Variant.isSet(m,i)){qx.locale.Manager.getInstance().removeListener(k,this.__lz,this);
}}});
})();
(function(){var k="showingPlaceholder",j="",i="none",h="qx.dynlocale",g="Boolean",f="qx.client",d="color",c="qx.event.type.Data",b="readonly",a="placeholder",bc="input",bb="focusin",ba="visibility",Y="focusout",X="changeLocale",W="hidden",V="on",U="absolute",T="readOnly",S="text",r="_applyTextAlign",s="px",p="RegExp",q=")",n="syncAppearance",o="changeValue",l="A",m="change",v="textAlign",w="focused",E="center",C="visible",K="disabled",G="url(",O="off",M="String",y="resize",R="qx.ui.form.AbstractField",Q="transparent",P="spellcheck",x="false",A="right",B="PositiveInteger",D="mshtml",F="abstract",H="block",L="webkit",N="_applyReadOnly",t="_applyPlaceholder",u="left",z="qx/static/blank.gif",J="text-placeholder",I="changeReadOnly";
qx.Class.define(R,{extend:qx.ui.core.Widget,implement:[qx.ui.form.IStringForm,qx.ui.form.IForm],include:[qx.ui.form.MForm],type:F,construct:function(bd){qx.ui.core.Widget.call(this);
this.__oC=!qx.bom.client.Feature.PLACEHOLDER;

if(bd!=null){this.setValue(bd);
}this.getContentElement().addListener(m,this._onChangeContent,this);
if(this.__oC){this.addListener(n,this._syncPlaceholder,this);
}if(qx.core.Variant.isSet(h,V)){qx.locale.Manager.getInstance().addListener(X,this._onChangeLocale,this);
}},events:{"input":c,"changeValue":c},properties:{textAlign:{check:[u,E,A],nullable:true,themeable:true,apply:r},readOnly:{check:g,apply:N,event:I,init:false},selectable:{refine:true,init:true},focusable:{refine:true,init:true},maxLength:{check:B,init:Infinity},liveUpdate:{check:g,init:false},placeholder:{check:M,nullable:true,apply:t},filter:{check:p,nullable:true,init:null}},members:{__oD:true,__oE:null,__oF:null,__oG:null,__oC:true,getFocusElement:function(){var be=this.getContentElement();

if(be){return be;
}},_createInputElement:function(){return new qx.html.Input(S);
},renderLayout:function(bf,top,bg,bh){var bi=this._updateInsets;
var bm=qx.ui.core.Widget.prototype.renderLayout.call(this,bf,top,bg,bh);
if(!bm){return;
}var bk=bm.size||bi;
var bn=s;

if(bk||bm.local||bm.margin){var bj=this.getInsets();
var innerWidth=bg-bj.left-bj.right;
var innerHeight=bh-bj.top-bj.bottom;
innerWidth=innerWidth<0?0:innerWidth;
innerHeight=innerHeight<0?0:innerHeight;
}var bl=this.getContentElement();
if(bi&&this.__oC){this.__oJ().setStyles({"left":bj.left+bn,"top":bj.top+bn});
}
if(bk){if(this.__oC){this.__oJ().setStyles({"width":innerWidth+bn,"height":innerHeight+bn});
}bl.setStyles({"width":innerWidth+bn,"height":innerHeight+bn});
this._renderContentElement(innerHeight,bl);
}},_renderContentElement:function(innerHeight,bo){},_createContentElement:function(){var bp=this._createInputElement();
bp.setStyles({"border":i,"padding":0,"margin":0,"display":H,"background":Q,"outline":i,"appearance":i,"position":U,"autoComplete":O});
bp.setSelectable(this.getSelectable());
bp.setEnabled(this.getEnabled());
bp.addListener(bc,this._onHtmlInput,this);
bp.setAttribute(P,x);
if(qx.core.Variant.isSet(f,L)){bp.setStyle(y,i);
}if(qx.core.Variant.isSet(f,D)){bp.setStyles({backgroundImage:G+qx.util.ResourceManager.getInstance().toUri(z)+q});
}return bp;
},_applyEnabled:function(bq,br){qx.ui.core.Widget.prototype._applyEnabled.call(this,bq,br);
this.getContentElement().setEnabled(bq);

if(this.__oC){if(bq){this._showPlaceholder();
}else{this._removePlaceholder();
}}else{var bs=this.getContentElement();
bs.setAttribute(a,bq?this.getPlaceholder():j);
}},__oH:{width:16,height:16},_getContentHint:function(){return {width:this.__oH.width*10,height:this.__oH.height||16};
},_applyFont:function(bt,bu){var bv;

if(bt){var bw=qx.theme.manager.Font.getInstance().resolve(bt);
bv=bw.getStyles();
}else{bv=qx.bom.Font.getDefaultStyles();
}this.getContentElement().setStyles(bv);
if(this.__oC){this.__oJ().setStyles(bv);
}if(bt){this.__oH=qx.bom.Label.getTextSize(l,bv);
}else{delete this.__oH;
}qx.ui.core.queue.Layout.add(this);
},_applyTextColor:function(bx,by){if(bx){this.getContentElement().setStyle(d,qx.theme.manager.Color.getInstance().resolve(bx));
}else{this.getContentElement().removeStyle(d);
}},tabFocus:function(){qx.ui.core.Widget.prototype.tabFocus.call(this);
this.selectAllText();
},_getTextSize:function(){return this.__oH;
},_onHtmlInput:function(e){var bC=e.getData();
var bB=true;
this.__oD=false;
if(this.getFilter()!=null){var bD=j;
var bz=bC.search(this.getFilter());
var bA=bC;

while(bz>=0){bD=bD+(bA.charAt(bz));
bA=bA.substring(bz+1,bA.length);
bz=bA.search(this.getFilter());
}
if(bD!=bC){bB=false;
bC=bD;
this.getContentElement().setValue(bC);
}}if(bC.length>this.getMaxLength()){bB=false;
this.getContentElement().setValue(bC.substr(0,this.getMaxLength()));
}if(bB){this.fireDataEvent(bc,bC,this.__oG);
this.__oG=bC;
if(this.getLiveUpdate()){this.__oI(bC);
}}},__oI:function(bE){var bF=this.__oF;
this.__oF=bE;

if(bF!=bE){this.fireNonBubblingEvent(o,qx.event.type.Data,[bE,bF]);
}},setValue:function(bG){if(bG===null){if(this.__oD){return bG;
}bG=j;
this.__oD=true;
}else{this.__oD=false;
if(this.__oC){this._removePlaceholder();
}}
if(qx.lang.Type.isString(bG)){var bI=this.getContentElement();

if(bG.length>this.getMaxLength()){bG=bG.substr(0,this.getMaxLength());
}
if(bI.getValue()!=bG){var bJ=bI.getValue();
bI.setValue(bG);
var bH=this.__oD?null:bG;
this.__oF=bJ;
this.__oI(bH);
}if(this.__oC){this._showPlaceholder();
}return bG;
}throw new Error("Invalid value type: "+bG);
},getValue:function(){var bK=this.getContentElement().getValue();
return this.__oD?null:bK;
},resetValue:function(){this.setValue(null);
},_onChangeContent:function(e){this.__oD=e.getData()===null;
this.__oI(e.getData());
},getTextSelection:function(){return this.getContentElement().getTextSelection();
},getTextSelectionLength:function(){return this.getContentElement().getTextSelectionLength();
},getTextSelectionStart:function(){return this.getContentElement().getTextSelectionStart();
},getTextSelectionEnd:function(){return this.getContentElement().getTextSelectionEnd();
},setTextSelection:function(bL,bM){this.getContentElement().setTextSelection(bL,bM);
},clearTextSelection:function(){this.getContentElement().clearTextSelection();
},selectAllText:function(){this.setTextSelection(0);
},_showPlaceholder:function(){var bO=this.getValue()||j;
var bN=this.getPlaceholder();

if(bN!=null&&bO==j&&!this.hasState(w)&&!this.hasState(K)){if(this.hasState(k)){this._syncPlaceholder();
}else{this.addState(k);
}}},_removePlaceholder:function(){if(this.hasState(k)){this.__oJ().setStyle(ba,W);
this.removeState(k);
}},_syncPlaceholder:function(){if(this.hasState(k)){this.__oJ().setStyle(ba,C);
}},__oJ:function(){if(this.__oE==null){this.__oE=new qx.html.Label();
var bP=qx.theme.manager.Color.getInstance();
this.__oE.setStyles({"visibility":W,"zIndex":6,"position":U,"color":bP.resolve(J)});
this.getContainerElement().add(this.__oE);
}return this.__oE;
},_onChangeLocale:qx.core.Variant.select(h,{"on":function(e){var content=this.getPlaceholder();

if(content&&content.translate){this.setPlaceholder(content.translate());
}},"off":null}),_applyPlaceholder:function(bQ,bR){if(this.__oC){this.__oJ().setValue(bQ);

if(bQ!=null){this.addListener(bb,this._removePlaceholder,this);
this.addListener(Y,this._showPlaceholder,this);
this._showPlaceholder();
}else{this.removeListener(bb,this._removePlaceholder,this);
this.removeListener(Y,this._showPlaceholder,this);
this._removePlaceholder();
}}else{if(this.getEnabled()){this.getContentElement().setAttribute(a,bQ);
}}},_applyTextAlign:function(bS,bT){this.getContentElement().setStyle(v,bS);
},_applyReadOnly:function(bU,bV){var bW=this.getContentElement();
bW.setAttribute(T,bU);

if(bU){this.addState(b);
this.setFocusable(false);
}else{this.removeState(b);
this.setFocusable(true);
}}},destruct:function(){this.__oE=null;

if(qx.core.Variant.isSet(h,V)){qx.locale.Manager.getInstance().removeListener(X,this._onChangeLocale,this);
}}});
})();
(function(){var e='px',d="mshtml",c="qx.ui.form.TextField",b="qx.client",a="textfield";
qx.Class.define(c,{extend:qx.ui.form.AbstractField,properties:{appearance:{refine:true,init:a},allowGrowY:{refine:true,init:false},allowShrinkY:{refine:true,init:false}},members:{_renderContentElement:function(innerHeight,f){if(qx.core.Variant.isSet(b,d)&&qx.bom.client.Engine.VERSION<9){f.setStyles({"line-height":innerHeight+e});
}}}});
})();
(function(){var n="wrap",m="value",l="textarea",k="none",j="qx.client",i="",h="overflow",g="input",f="qx.html.Input",e="select",b="disabled",d="read-only",c="overflowX",a="overflowY";
qx.Class.define(f,{extend:qx.html.Element,construct:function(o,p,q){if(o===e||o===l){var r=o;
}else{r=g;
}qx.html.Element.call(this,r,p,q);
this.__oK=o;
},members:{__oK:null,__oL:null,__oM:null,_createDomElement:function(){return qx.bom.Input.create(this.__oK);
},_applyProperty:function(name,s){qx.html.Element.prototype._applyProperty.call(this,name,s);
var t=this.getDomElement();

if(name===m){qx.bom.Input.setValue(t,s);
}else if(name===n){qx.bom.Input.setWrap(t,s);
this.setStyle(h,t.style.overflow,true);
this.setStyle(c,t.style.overflowX,true);
this.setStyle(a,t.style.overflowY,true);
}},setEnabled:qx.core.Variant.select(j,{"webkit":function(u){this.__oM=u;

if(!u){this.setStyles({"userModify":d,"userSelect":k});
}else{this.setStyles({"userModify":null,"userSelect":this.__oL?null:k});
}},"default":function(v){this.setAttribute(b,v===false);
}}),setSelectable:qx.core.Variant.select(j,{"webkit":function(w){this.__oL=w;
qx.html.Element.prototype.setSelectable.call(this,this.__oM&&w);
},"default":function(x){qx.html.Element.prototype.setSelectable.call(this,x);
}}),setValue:function(y){var z=this.getDomElement();

if(z){if(z.value!=y){qx.bom.Input.setValue(z,y);
}}else{this._setProperty(m,y);
}return this;
},getValue:function(){var A=this.getDomElement();

if(A){return qx.bom.Input.getValue(A);
}return this._getProperty(m)||i;
},setWrap:function(B,C){if(this.__oK===l){this._setProperty(n,B,C);
}else{throw new Error("Text wrapping is only support by textareas!");
}return this;
},getWrap:function(){if(this.__oK===l){return this._getProperty(n);
}else{throw new Error("Text wrapping is only support by textareas!");
}}}});
})();
(function(){var w="change",v="input",u="qx.client",t="text",s="password",r="checkbox",q="radio",p="textarea",n="keypress",m="opera",d="propertychange",k="blur",h="keydown",c="keyup",b="select-multiple",g="checked",f="value",j="select",a="qx.event.handler.Input";
qx.Class.define(a,{extend:qx.core.Object,implement:qx.event.IEventHandler,construct:function(){qx.core.Object.call(this);
this._onChangeCheckedWrapper=qx.lang.Function.listener(this._onChangeChecked,this);
this._onChangeValueWrapper=qx.lang.Function.listener(this._onChangeValue,this);
this._onInputWrapper=qx.lang.Function.listener(this._onInput,this);
this._onPropertyWrapper=qx.lang.Function.listener(this._onProperty,this);
if(qx.core.Variant.isSet(u,m)){this._onKeyDownWrapper=qx.lang.Function.listener(this._onKeyDown,this);
this._onKeyUpWrapper=qx.lang.Function.listener(this._onKeyUp,this);
this._onBlurWrapper=qx.lang.Function.listener(this._onBlur,this);
}},statics:{PRIORITY:qx.event.Registration.PRIORITY_NORMAL,SUPPORTED_TYPES:{input:1,change:1},TARGET_CHECK:qx.event.IEventHandler.TARGET_DOMNODE,IGNORE_CAN_HANDLE:false},members:{__oN:false,__oO:null,__oP:null,canHandleEvent:function(x,y){var z=x.tagName.toLowerCase();

if(y===v&&(z===v||z===p)){return true;
}
if(y===w&&(z===v||z===p||z===j)){return true;
}return false;
},registerEvent:qx.core.Variant.select(u,{"mshtml":function(A,B,C){if(!A.__oQ){var D=A.tagName.toLowerCase();
var E=A.type;

if(E===t||E===s||D===p||E===r||E===q){qx.bom.Event.addNativeListener(A,d,this._onPropertyWrapper);
}
if(E!==r&&E!==q){qx.bom.Event.addNativeListener(A,w,this._onChangeValueWrapper);
}
if(E===t||E===s){this._onKeyPressWrapped=qx.lang.Function.listener(this._onKeyPress,this,A);
qx.bom.Event.addNativeListener(A,n,this._onKeyPressWrapped);
}A.__oQ=true;
}},"default":function(F,G,H){if(G===v){this.__oR(F);
}else if(G===w){if(F.type===q||F.type===r){qx.bom.Event.addNativeListener(F,w,this._onChangeCheckedWrapper);
}else{qx.bom.Event.addNativeListener(F,w,this._onChangeValueWrapper);
}if(qx.core.Variant.isSet(u,m)){if(F.type===t||F.type===s){this._onKeyPressWrapped=qx.lang.Function.listener(this._onKeyPress,this,F);
qx.bom.Event.addNativeListener(F,n,this._onKeyPressWrapped);
}}}}}),__oR:qx.core.Variant.select(u,{"mshtml":null,"webkit":function(I){var J=I.tagName.toLowerCase();
if(qx.bom.client.Engine.VERSION<532&&J==p){qx.bom.Event.addNativeListener(I,n,this._onInputWrapper);
}qx.bom.Event.addNativeListener(I,v,this._onInputWrapper);
},"opera":function(K){qx.bom.Event.addNativeListener(K,c,this._onKeyUpWrapper);
qx.bom.Event.addNativeListener(K,h,this._onKeyDownWrapper);
qx.bom.Event.addNativeListener(K,k,this._onBlurWrapper);
qx.bom.Event.addNativeListener(K,v,this._onInputWrapper);
},"default":function(L){qx.bom.Event.addNativeListener(L,v,this._onInputWrapper);
}}),unregisterEvent:qx.core.Variant.select(u,{"mshtml":function(M,N){if(M.__oQ){var O=M.tagName.toLowerCase();
var P=M.type;

if(P===t||P===s||O===p||P===r||P===q){qx.bom.Event.removeNativeListener(M,d,this._onPropertyWrapper);
}
if(P!==r&&P!==q){qx.bom.Event.removeNativeListener(M,w,this._onChangeValueWrapper);
}
if(P===t||P===s){qx.bom.Event.removeNativeListener(M,n,this._onKeyPressWrapped);
}
try{delete M.__oQ;
}catch(Q){M.__oQ=null;
}}},"default":function(R,S){if(S===v){this.__oR(R);
}else if(S===w){if(R.type===q||R.type===r){qx.bom.Event.removeNativeListener(R,w,this._onChangeCheckedWrapper);
}else{qx.bom.Event.removeNativeListener(R,w,this._onChangeValueWrapper);
}}
if(qx.core.Variant.isSet(u,m)){if(R.type===t||R.type===s){qx.bom.Event.removeNativeListener(R,n,this._onKeyPressWrapped);
}}}}),__oS:qx.core.Variant.select(u,{"mshtml":null,"webkit":function(T){var U=T.tagName.toLowerCase();
if(qx.bom.client.Engine.VERSION<532&&U==p){qx.bom.Event.removeNativeListener(T,n,this._onInputWrapper);
}qx.bom.Event.removeNativeListener(T,v,this._onInputWrapper);
},"opera":function(V){qx.bom.Event.removeNativeListener(V,c,this._onKeyUpWrapper);
qx.bom.Event.removeNativeListener(V,h,this._onKeyDownWrapper);
qx.bom.Event.removeNativeListener(V,k,this._onBlurWrapper);
qx.bom.Event.removeNativeListener(V,v,this._onInputWrapper);
},"default":function(W){qx.bom.Event.removeNativeListener(W,v,this._onInputWrapper);
}}),_onKeyPress:qx.core.Variant.select(u,{"mshtml|opera":function(e,X){if(e.keyCode===13){if(X.value!==this.__oP){this.__oP=X.value;
qx.event.Registration.fireEvent(X,w,qx.event.type.Data,[X.value]);
}}},"default":null}),_onKeyDown:qx.core.Variant.select(u,{"opera":function(e){if(e.keyCode===13){this.__oN=true;
}},"default":null}),_onKeyUp:qx.core.Variant.select(u,{"opera":function(e){if(e.keyCode===13){this.__oN=false;
}},"default":null}),_onBlur:qx.core.Variant.select(u,{"opera":function(e){if(this.__oO&&qx.bom.client.Browser.VERSION<10.6){window.clearTimeout(this.__oO);
}},"default":null}),_onInput:qx.event.GlobalError.observeMethod(function(e){var ba=qx.bom.Event.getTarget(e);
var Y=ba.tagName.toLowerCase();
if(!this.__oN||Y!==v){if(qx.core.Variant.isSet(u,m)&&qx.bom.client.Browser.VERSION<10.6){this.__oO=window.setTimeout(function(){qx.event.Registration.fireEvent(ba,v,qx.event.type.Data,[ba.value]);
},0);
}else{qx.event.Registration.fireEvent(ba,v,qx.event.type.Data,[ba.value]);
}}}),_onChangeValue:qx.event.GlobalError.observeMethod(function(e){var bc=qx.bom.Event.getTarget(e);
var bb=bc.value;

if(bc.type===b){var bb=[];

for(var i=0,o=bc.options,l=o.length;i<l;i++){if(o[i].selected){bb.push(o[i].value);
}}}qx.event.Registration.fireEvent(bc,w,qx.event.type.Data,[bb]);
}),_onChangeChecked:qx.event.GlobalError.observeMethod(function(e){var bd=qx.bom.Event.getTarget(e);

if(bd.type===q){if(bd.checked){qx.event.Registration.fireEvent(bd,w,qx.event.type.Data,[bd.value]);
}}else{qx.event.Registration.fireEvent(bd,w,qx.event.type.Data,[bd.checked]);
}}),_onProperty:qx.core.Variant.select(u,{"mshtml":qx.event.GlobalError.observeMethod(function(e){var be=qx.bom.Event.getTarget(e);
var bf=e.propertyName;

if(bf===f&&(be.type===t||be.type===s||be.tagName.toLowerCase()===p)){if(!be.$$inValueSet){qx.event.Registration.fireEvent(be,v,qx.event.type.Data,[be.value]);
}}else if(bf===g){if(be.type===r){qx.event.Registration.fireEvent(be,w,qx.event.type.Data,[be.checked]);
}else if(be.checked){qx.event.Registration.fireEvent(be,w,qx.event.type.Data,[be.value]);
}}}),"default":function(){}})},defer:function(bg){qx.event.Registration.addHandler(bg);
}});
})();
(function(){var v="",u="select",t="soft",s="off",r="qx.client",q="textarea",p="auto",o="wrap",n="text",m="mshtml",d="number",k="checkbox",g="select-one",c="input",b="option",f="value",e="radio",h="qx.bom.Input",a="nowrap",j="normal";
qx.Class.define(h,{statics:{__oT:{text:1,textarea:1,select:1,checkbox:1,radio:1,password:1,hidden:1,submit:1,image:1,file:1,search:1,reset:1,button:1},create:function(w,x,y){{};
var x=x?qx.lang.Object.clone(x):{};
var z;

if(w===q||w===u){z=w;
}else{z=c;
x.type=w;
}return qx.bom.Element.create(z,x,y);
},setValue:function(A,B){var G=A.nodeName.toLowerCase();
var D=A.type;
var Array=qx.lang.Array;
var H=qx.lang.Type;

if(typeof B===d){B+=v;
}
if((D===k||D===e)){if(H.isArray(B)){A.checked=Array.contains(B,A.value);
}else{A.checked=A.value==B;
}}else if(G===u){var C=H.isArray(B);
var I=A.options;
var E,F;

for(var i=0,l=I.length;i<l;i++){E=I[i];
F=E.getAttribute(f);

if(F==null){F=E.text;
}E.selected=C?Array.contains(B,F):B==F;
}
if(C&&B.length==0){A.selectedIndex=-1;
}}else if((D===n||D===q)&&qx.core.Variant.isSet(r,m)){A.$$inValueSet=true;
A.value=B;
A.$$inValueSet=null;
}else{A.value=B;
}},getValue:function(J){var P=J.nodeName.toLowerCase();

if(P===b){return (J.attributes.value||{}).specified?J.value:J.text;
}
if(P===u){var K=J.selectedIndex;
if(K<0){return null;
}var Q=[];
var S=J.options;
var R=J.type==g;
var O=qx.bom.Input;
var N;
for(var i=R?K:0,M=R?K+1:S.length;i<M;i++){var L=S[i];

if(L.selected){N=O.getValue(L);
if(R){return N;
}Q.push(N);
}}return Q;
}else{return (J.value||v).replace(/\r/g,v);
}},setWrap:qx.core.Variant.select(r,{"mshtml":function(T,U){var W=U?t:s;
var V=U?p:v;
T.wrap=W;
T.style.overflowY=V;
},"gecko|webkit":function(X,Y){var bb=Y?t:s;
var ba=Y?v:p;
X.setAttribute(o,bb);
X.style.overflow=ba;
},"default":function(bc,bd){bc.style.whiteSpace=bd?j:a;
}})}});
})();
(function(){var i="icon",h="label",g="String",f="sort-icon",e="_applySortIcon",d="_applyIcon",c="table-header-cell",b="qx.ui.table.headerrenderer.HeaderCell",a="_applyLabel";
qx.Class.define(b,{extend:qx.ui.container.Composite,construct:function(){qx.ui.container.Composite.call(this);
var j=new qx.ui.layout.Grid();
j.setRowFlex(0,1);
j.setColumnFlex(1,1);
j.setColumnFlex(2,1);
this.setLayout(j);
},properties:{appearance:{refine:true,init:c},label:{check:g,init:null,nullable:true,apply:a},sortIcon:{check:g,init:null,nullable:true,apply:e,themeable:true},icon:{check:g,init:null,nullable:true,apply:d}},members:{_applyLabel:function(k,l){if(k){this._showChildControl(h).setValue(k);
}else{this._excludeChildControl(h);
}},_applySortIcon:function(m,n){if(m){this._showChildControl(f).setSource(m);
}else{this._excludeChildControl(f);
}},_applyIcon:function(o,p){if(o){this._showChildControl(i).setSource(o);
}else{this._excludeChildControl(i);
}},_createChildControlImpl:function(q,r){var s;

switch(q){case h:s=new qx.ui.basic.Label(this.getLabel()).set({anonymous:true,allowShrinkX:true});
this._add(s,{row:0,column:1});
break;
case f:s=new qx.ui.basic.Image(this.getSortIcon());
s.setAnonymous(true);
this._add(s,{row:0,column:2});
break;
case i:s=new qx.ui.basic.Image(this.getIcon()).set({anonymous:true,allowShrinkX:true});
this._add(s,{row:0,column:0});
break;
}return s||qx.ui.container.Composite.prototype._createChildControlImpl.call(this,q);
}}});
})();
(function(){var g="",f="<br",e=" &nbsp;",d="<br>",c=" ",b="\n",a="qx.bom.String";
qx.Class.define(a,{statics:{TO_CHARCODE:{"quot":34,"amp":38,"lt":60,"gt":62,"nbsp":160,"iexcl":161,"cent":162,"pound":163,"curren":164,"yen":165,"brvbar":166,"sect":167,"uml":168,"copy":169,"ordf":170,"laquo":171,"not":172,"shy":173,"reg":174,"macr":175,"deg":176,"plusmn":177,"sup2":178,"sup3":179,"acute":180,"micro":181,"para":182,"middot":183,"cedil":184,"sup1":185,"ordm":186,"raquo":187,"frac14":188,"frac12":189,"frac34":190,"iquest":191,"Agrave":192,"Aacute":193,"Acirc":194,"Atilde":195,"Auml":196,"Aring":197,"AElig":198,"Ccedil":199,"Egrave":200,"Eacute":201,"Ecirc":202,"Euml":203,"Igrave":204,"Iacute":205,"Icirc":206,"Iuml":207,"ETH":208,"Ntilde":209,"Ograve":210,"Oacute":211,"Ocirc":212,"Otilde":213,"Ouml":214,"times":215,"Oslash":216,"Ugrave":217,"Uacute":218,"Ucirc":219,"Uuml":220,"Yacute":221,"THORN":222,"szlig":223,"agrave":224,"aacute":225,"acirc":226,"atilde":227,"auml":228,"aring":229,"aelig":230,"ccedil":231,"egrave":232,"eacute":233,"ecirc":234,"euml":235,"igrave":236,"iacute":237,"icirc":238,"iuml":239,"eth":240,"ntilde":241,"ograve":242,"oacute":243,"ocirc":244,"otilde":245,"ouml":246,"divide":247,"oslash":248,"ugrave":249,"uacute":250,"ucirc":251,"uuml":252,"yacute":253,"thorn":254,"yuml":255,"fnof":402,"Alpha":913,"Beta":914,"Gamma":915,"Delta":916,"Epsilon":917,"Zeta":918,"Eta":919,"Theta":920,"Iota":921,"Kappa":922,"Lambda":923,"Mu":924,"Nu":925,"Xi":926,"Omicron":927,"Pi":928,"Rho":929,"Sigma":931,"Tau":932,"Upsilon":933,"Phi":934,"Chi":935,"Psi":936,"Omega":937,"alpha":945,"beta":946,"gamma":947,"delta":948,"epsilon":949,"zeta":950,"eta":951,"theta":952,"iota":953,"kappa":954,"lambda":955,"mu":956,"nu":957,"xi":958,"omicron":959,"pi":960,"rho":961,"sigmaf":962,"sigma":963,"tau":964,"upsilon":965,"phi":966,"chi":967,"psi":968,"omega":969,"thetasym":977,"upsih":978,"piv":982,"bull":8226,"hellip":8230,"prime":8242,"Prime":8243,"oline":8254,"frasl":8260,"weierp":8472,"image":8465,"real":8476,"trade":8482,"alefsym":8501,"larr":8592,"uarr":8593,"rarr":8594,"darr":8595,"harr":8596,"crarr":8629,"lArr":8656,"uArr":8657,"rArr":8658,"dArr":8659,"hArr":8660,"forall":8704,"part":8706,"exist":8707,"empty":8709,"nabla":8711,"isin":8712,"notin":8713,"ni":8715,"prod":8719,"sum":8721,"minus":8722,"lowast":8727,"radic":8730,"prop":8733,"infin":8734,"ang":8736,"and":8743,"or":8744,"cap":8745,"cup":8746,"int":8747,"there4":8756,"sim":8764,"cong":8773,"asymp":8776,"ne":8800,"equiv":8801,"le":8804,"ge":8805,"sub":8834,"sup":8835,"sube":8838,"supe":8839,"oplus":8853,"otimes":8855,"perp":8869,"sdot":8901,"lceil":8968,"rceil":8969,"lfloor":8970,"rfloor":8971,"lang":9001,"rang":9002,"loz":9674,"spades":9824,"clubs":9827,"hearts":9829,"diams":9830,"OElig":338,"oelig":339,"Scaron":352,"scaron":353,"Yuml":376,"circ":710,"tilde":732,"ensp":8194,"emsp":8195,"thinsp":8201,"zwnj":8204,"zwj":8205,"lrm":8206,"rlm":8207,"ndash":8211,"mdash":8212,"lsquo":8216,"rsquo":8217,"sbquo":8218,"ldquo":8220,"rdquo":8221,"bdquo":8222,"dagger":8224,"Dagger":8225,"permil":8240,"lsaquo":8249,"rsaquo":8250,"euro":8364},escape:function(h){return qx.util.StringEscape.escape(h,qx.bom.String.FROM_CHARCODE);
},unescape:function(i){return qx.util.StringEscape.unescape(i,qx.bom.String.TO_CHARCODE);
},fromText:function(j){return qx.bom.String.escape(j).replace(/(  |\n)/g,function(k){var l={"  ":e,"\n":d};
return l[k]||k;
});
},toText:function(m){return qx.bom.String.unescape(m.replace(/\s+|<([^>])+>/gi,function(n){if(n.indexOf(f)===0){return b;
}else if(n.length>0&&n.replace(/^\s*/,g).replace(/\s*$/,g)==g){return c;
}else{return g;
}}));
}},defer:function(o){o.FROM_CHARCODE=qx.lang.Object.invert(o.TO_CHARCODE);
}});
})();
(function(){var g=";",f="&",e='X',d="",c='#',b="&#",a="qx.util.StringEscape";
qx.Class.define(a,{statics:{escape:function(h,j){var m,o=d;

for(var i=0,l=h.length;i<l;i++){var n=h.charAt(i);
var k=n.charCodeAt(0);

if(j[k]){m=f+j[k]+g;
}else{if(k>0x7F){m=b+k+g;
}else{m=n;
}}o+=m;
}return o;
},unescape:function(p,q){return p.replace(/&[#\w]+;/gi,function(r){var s=r;
var r=r.substring(1,r.length-1);
var t=q[r];

if(t){s=String.fromCharCode(t);
}else{if(r.charAt(0)==c){if(r.charAt(1).toUpperCase()==e){t=r.substring(2);
if(t.match(/^[0-9A-Fa-f]+$/gi)){s=String.fromCharCode(parseInt(t,16));
}}else{t=r.substring(1);
if(t.match(/^\d+$/gi)){s=String.fromCharCode(parseInt(t,10));
}}}}return s;
});
}}});
})();
(function(){var bC="(\\d\\d?)",bB="format",bA="",bz="stand-alone",by="abbreviated",bx="wide",bw="(",bv=")",bu="|",bt="wildcard",bi="default",bh="literal",bg="'",bf="hour",be="(\\d\\d?\\d?)",bd="ms",bc="narrow",bb="-",ba="quoted_literal",Y='a',bJ="HH:mm:ss",bK="+",bH="HHmmss",bI="long",bF='z',bG="0",bD="day",bE='Z',bL=" ",bM="(\\d\\d\\d\\d)",bm="min",bl="sec",bo="mm",bn="(\\d+)",bq="h",bp="KK",bs='L',br="Z",bk="(\\d\\d+)",bj="EEEE",a="^",b=":",c='y',d="K",e="a",f="([\\+\\-]\\d\\d:?\\d\\d)",g="GMT",h="dd",j="qx.util.format.DateFormat",k="yyy",bQ="H",bP="YYYY",bO="y",bN="HH",bU="EE",bT='h',bS="S",bR='s',bW='A',bV="yyyyyy",I="kk",J="ss",G='H',H='S',M="MMMM",N='c',K="d",L="([a-zA-Z]+)",E='k',F="m",s='Y',r='D',u="yyyyy",t='K',o="hh",n="SSS",q="MM",p="yy",m="(\\d\\d\\d\\d\\d\\d+)",l="yyyy-MM-dd HH:mm:ss",S="(\\d\\d\\d\\d\\d+)",T="short",U='d',V="unkown",O='m',P="(\\d\\d\\d+)",Q="k",R='M',W="SS",X="MMM",C="s",B="M",A='w',z="EEE",y="$",x="?",w='E',v="z",D="yyyy";
qx.Class.define(j,{extend:qx.core.Object,implement:qx.util.format.IFormat,construct:function(bX,bY){qx.core.Object.call(this);

if(!bY){this.__pr=qx.locale.Manager.getInstance().getLocale();
}else{this.__pr=bY;
}
if(bX!=null){this.__ps=bX.toString();
}else{this.__ps=qx.locale.Date.getDateFormat(bI,this.__pr)+bL+qx.locale.Date.getDateTimeFormat(bH,bJ,this.__pr);
}},statics:{getDateTimeInstance:function(){var cb=qx.util.format.DateFormat;
var ca=qx.locale.Date.getDateFormat(bI)+bL+qx.locale.Date.getDateTimeFormat(bH,bJ);

if(cb._dateInstance==null||cb._dateInstance.__ps!=ca){cb._dateTimeInstance=new cb();
}return cb._dateTimeInstance;
},getDateInstance:function(){var cd=qx.util.format.DateFormat;
var cc=qx.locale.Date.getDateFormat(T)+bA;

if(cd._dateInstance==null||cd._dateInstance.__ps!=cc){cd._dateInstance=new cd(cc);
}return cd._dateInstance;
},ASSUME_YEAR_2000_THRESHOLD:30,LOGGING_DATE_TIME__format:l,AM_MARKER:"am",PM_MARKER:"pm",MEDIUM_TIMEZONE_NAMES:["GMT"],FULL_TIMEZONE_NAMES:["Greenwich Mean Time"]},members:{__pr:null,__ps:null,__pt:null,__pu:null,__pv:null,__pw:function(ce,cf){var cg=bA+ce;

while(cg.length<cf){cg=bG+cg;
}return cg;
},__px:function(ch){var ci=new Date(ch.getTime());
var cj=ci.getDate();

while(ci.getMonth()!=0){ci.setDate(-1);
cj+=ci.getDate()+1;
}return cj;
},__py:function(ck){return new Date(ck.getTime()+(3-((ck.getDay()+6)%7))*86400000);
},__pz:function(cl){var cn=this.__py(cl);
var co=cn.getFullYear();
var cm=this.__py(new Date(co,0,4));
return Math.floor(1.5+(cn.getTime()-cm.getTime())/86400000/7);
},format:function(cp){if(cp==null){return null;
}var cv=qx.util.format.DateFormat;
var cw=this.__pr;
var cG=cp.getFullYear();
var cA=cp.getMonth();
var cI=cp.getDate();
var cq=cp.getDay();
var cB=cp.getHours();
var cx=cp.getMinutes();
var cC=cp.getSeconds();
var cE=cp.getMilliseconds();
var cH=cp.getTimezoneOffset();
var ct=cH>0?1:-1;
var cr=Math.floor(Math.abs(cH)/60);
var cy=Math.abs(cH)%60;
this.__pA();
var cF=bA;

for(var i=0;i<this.__pv.length;i++){var cD=this.__pv[i];

if(cD.type==bh){cF+=cD.text;
}else{var cu=cD.character;
var cz=cD.size;
var cs=x;

switch(cu){case c:case s:if(cz==2){cs=this.__pw(cG%100,2);
}else{cs=cG+bA;

if(cz>cs.length){for(var i=cs.length;i<cz;i++){cs=bG+cs;
}}}break;
case r:cs=this.__pw(this.__px(cp),cz);
break;
case U:cs=this.__pw(cI,cz);
break;
case A:cs=this.__pw(this.__pz(cp),cz);
break;
case w:if(cz==2){cs=qx.locale.Date.getDayName(bc,cq,cw,bz);
}else if(cz==3){cs=qx.locale.Date.getDayName(by,cq,cw,bB);
}else if(cz==4){cs=qx.locale.Date.getDayName(bx,cq,cw,bB);
}break;
case N:if(cz==2){cs=qx.locale.Date.getDayName(bc,cq,cw,bz);
}else if(cz==3){cs=qx.locale.Date.getDayName(by,cq,cw,bz);
}else if(cz==4){cs=qx.locale.Date.getDayName(bx,cq,cw,bz);
}break;
case R:if(cz==1||cz==2){cs=this.__pw(cA+1,cz);
}else if(cz==3){cs=qx.locale.Date.getMonthName(by,cA,cw,bB);
}else if(cz==4){cs=qx.locale.Date.getMonthName(bx,cA,cw,bB);
}break;
case bs:if(cz==1||cz==2){cs=this.__pw(cA+1,cz);
}else if(cz==3){cs=qx.locale.Date.getMonthName(by,cA,cw,bz);
}else if(cz==4){cs=qx.locale.Date.getMonthName(bx,cA,cw,bz);
}break;
case Y:cs=(cB<12)?qx.locale.Date.getAmMarker(cw):qx.locale.Date.getPmMarker(cw);
break;
case G:cs=this.__pw(cB,cz);
break;
case E:cs=this.__pw((cB==0)?24:cB,cz);
break;
case t:cs=this.__pw(cB%12,cz);
break;
case bT:cs=this.__pw(((cB%12)==0)?12:(cB%12),cz);
break;
case O:cs=this.__pw(cx,cz);
break;
case bR:cs=this.__pw(cC,cz);
break;
case H:cs=this.__pw(cE,cz);
break;
case bF:if(cz==1){cs=g+((ct>0)?bb:bK)+this.__pw(Math.abs(cr))+b+this.__pw(cy,2);
}else if(cz==2){cs=cv.MEDIUM_TIMEZONE_NAMES[cr];
}else if(cz==3){cs=cv.FULL_TIMEZONE_NAMES[cr];
}break;
case bE:cs=((ct>0)?bb:bK)+this.__pw(Math.abs(cr),2)+this.__pw(cy,2);
break;
}cF+=cs;
}}return cF;
},parse:function(cJ){this.__pB();
var cP=this.__pt.regex.exec(cJ);

if(cP==null){throw new Error("Date string '"+cJ+"' does not match the date format: "+this.__ps);
}var cK={year:1970,month:0,day:1,hour:0,ispm:false,min:0,sec:0,ms:0};
var cL=1;

for(var i=0;i<this.__pt.usedRules.length;i++){var cN=this.__pt.usedRules[i];
var cM=cP[cL];

if(cN.field!=null){cK[cN.field]=parseInt(cM,10);
}else{cN.manipulator(cK,cM);
}cL+=(cN.groups==null)?1:cN.groups;
}var cO=new Date(cK.year,cK.month,cK.day,(cK.ispm)?(cK.hour+12):cK.hour,cK.min,cK.sec,cK.ms);

if(cK.month!=cO.getMonth()||cK.year!=cO.getFullYear()){throw new Error("Error parsing date '"+cJ+"': the value for day or month is too large");
}return cO;
},__pA:function(){if(this.__pv!=null){return;
}this.__pv=[];
var cU;
var cS=0;
var cW=bA;
var cQ=this.__ps;
var cT=bi;
var i=0;

while(i<cQ.length){var cV=cQ.charAt(i);

switch(cT){case ba:if(cV==bg){if(i+1>=cQ.length){i++;
break;
}var cR=cQ.charAt(i+1);

if(cR==bg){cW+=cV;
i++;
}else{i++;
cT=V;
}}else{cW+=cV;
i++;
}break;
case bt:if(cV==cU){cS++;
i++;
}else{this.__pv.push({type:bt,character:cU,size:cS});
cU=null;
cS=0;
cT=bi;
}break;
default:if((cV>=Y&&cV<=bF)||(cV>=bW&&cV<=bE)){cU=cV;
cT=bt;
}else if(cV==bg){if(i+1>=cQ.length){cW+=cV;
i++;
break;
}var cR=cQ.charAt(i+1);

if(cR==bg){cW+=cV;
i++;
}i++;
cT=ba;
}else{cT=bi;
}
if(cT!=bi){if(cW.length>0){this.__pv.push({type:bh,text:cW});
cW=bA;
}}else{cW+=cV;
i++;
}break;
}}if(cU!=null){this.__pv.push({type:bt,character:cU,size:cS});
}else if(cW.length>0){this.__pv.push({type:bh,text:cW});
}},__pB:function(){if(this.__pt!=null){return ;
}var db=this.__ps;
this.__pC();
this.__pA();
var dh=[];
var dd=a;

for(var cY=0;cY<this.__pv.length;cY++){var di=this.__pv[cY];

if(di.type==bh){dd+=qx.lang.String.escapeRegexpChars(di.text);
}else{var da=di.character;
var de=di.size;
var dc;

for(var dj=0;dj<this.__pu.length;dj++){var df=this.__pu[dj];

if(da==df.pattern.charAt(0)&&de==df.pattern.length){dc=df;
break;
}}if(dc==null){var dg=bA;

for(var i=0;i<de;i++){dg+=da;
}throw new Error("Malformed date format: "+db+". Wildcard "+dg+" is not supported");
}else{dh.push(dc);
dd+=dc.regex;
}}}dd+=y;
var cX;

try{cX=new RegExp(dd);
}catch(dk){throw new Error("Malformed date format: "+db);
}this.__pt={regex:cX,"usedRules":dh,pattern:dd};
},__pC:function(){var dv=qx.util.format.DateFormat;
var dy=qx.lang.String;

if(this.__pu!=null){return ;
}var dw=this.__pu=[];
var dm=qx.locale.Date.getAmMarker(this.__pr).toString()||dv.AM_MARKER;
var dD=qx.locale.Date.getPmMarker(this.__pr).toString()||dv.PM_MARKER;
var dr=function(dH,dI){dI=parseInt(dI,10);

if(dI<dv.ASSUME_YEAR_2000_THRESHOLD){dI+=2000;
}else if(dI<100){dI+=1900;
}dH.year=dI;
};
var dt=function(dJ,dK){dJ.month=parseInt(dK,10)-1;
};
var dp=function(dL,dM){var dN=qx.locale.Date.getPmMarker(this.__pr).toString()||dv.PM_MARKER;
dL.ispm=(dM==dN);
};
var dF=function(dO,dP){dO.hour=parseInt(dP,10)%24;
};
var dn=function(dQ,dR){dQ.hour=parseInt(dR,10)%12;
};
var dA=function(dS,dT){return;
};
var dG=qx.locale.Date.getMonthNames(by,this.__pr,bB);

for(var i=0;i<dG.length;i++){dG[i]=dy.escapeRegexpChars(dG[i].toString());
}var dq=function(dU,dV){dV=dy.escapeRegexpChars(dV);
dU.month=dG.indexOf(dV);
};
var dx=qx.locale.Date.getMonthNames(bx,this.__pr,bB);

for(var i=0;i<dx.length;i++){dx[i]=dy.escapeRegexpChars(dx[i].toString());
}var dB=function(dW,dX){dX=dy.escapeRegexpChars(dX);
dW.month=dx.indexOf(dX);
};
var dl=qx.locale.Date.getDayNames(bc,this.__pr,bz);

for(var i=0;i<dl.length;i++){dl[i]=dy.escapeRegexpChars(dl[i].toString());
}var dE=function(dY,ea){ea=dy.escapeRegexpChars(ea);
dY.month=dl.indexOf(ea);
};
var dC=qx.locale.Date.getDayNames(by,this.__pr,bB);

for(var i=0;i<dC.length;i++){dC[i]=dy.escapeRegexpChars(dC[i].toString());
}var ds=function(eb,ec){ec=dy.escapeRegexpChars(ec);
eb.month=dC.indexOf(ec);
};
var dz=qx.locale.Date.getDayNames(bx,this.__pr,bB);

for(var i=0;i<dz.length;i++){dz[i]=dy.escapeRegexpChars(dz[i].toString());
}var du=function(ed,ee){ee=dy.escapeRegexpChars(ee);
ed.month=dz.indexOf(ee);
};
dw.push({pattern:bP,regex:bM,manipulator:dr});
dw.push({pattern:bO,regex:bn,manipulator:dr});
dw.push({pattern:p,regex:bk,manipulator:dr});
dw.push({pattern:k,regex:P,manipulator:dr});
dw.push({pattern:D,regex:bM,manipulator:dr});
dw.push({pattern:u,regex:S,manipulator:dr});
dw.push({pattern:bV,regex:m,manipulator:dr});
dw.push({pattern:B,regex:bC,manipulator:dt});
dw.push({pattern:q,regex:bC,manipulator:dt});
dw.push({pattern:X,regex:bw+dG.join(bu)+bv,manipulator:dq});
dw.push({pattern:M,regex:bw+dx.join(bu)+bv,manipulator:dB});
dw.push({pattern:h,regex:bC,field:bD});
dw.push({pattern:K,regex:bC,field:bD});
dw.push({pattern:bU,regex:bw+dl.join(bu)+bv,manipulator:dE});
dw.push({pattern:z,regex:bw+dC.join(bu)+bv,manipulator:ds});
dw.push({pattern:bj,regex:bw+dz.join(bu)+bv,manipulator:du});
dw.push({pattern:e,regex:bw+dm+bu+dD+bv,manipulator:dp});
dw.push({pattern:bN,regex:bC,field:bf});
dw.push({pattern:bQ,regex:bC,field:bf});
dw.push({pattern:I,regex:bC,manipulator:dF});
dw.push({pattern:Q,regex:bC,manipulator:dF});
dw.push({pattern:bp,regex:bC,field:bf});
dw.push({pattern:d,regex:bC,field:bf});
dw.push({pattern:o,regex:bC,manipulator:dn});
dw.push({pattern:bq,regex:bC,manipulator:dn});
dw.push({pattern:bo,regex:bC,field:bm});
dw.push({pattern:F,regex:bC,field:bm});
dw.push({pattern:J,regex:bC,field:bl});
dw.push({pattern:C,regex:bC,field:bl});
dw.push({pattern:n,regex:be,field:bd});
dw.push({pattern:W,regex:be,field:bd});
dw.push({pattern:bS,regex:be,field:bd});
dw.push({pattern:br,regex:f,manipulator:dA});
dw.push({pattern:v,regex:L,manipulator:dA});
}},destruct:function(){this.__pv=this.__pt=this.__pu=null;
}});
})();
(function(){var k="_",j="format",h="thu",g="sat",f="cldr_day_",e="cldr_month_",d="wed",c="fri",b="tue",a="mon",B="sun",A="short",z="HH:mm",y="HHmmsszz",x="HHmm",w="HHmmss",v="cldr_date_format_",u="HH:mm:ss zz",t="full",s="cldr_pm",q="long",r="medium",o="cldr_am",p="qx.locale.Date",m="cldr_date_time_format_",n="cldr_time_format_",l="HH:mm:ss";
qx.Class.define(p,{statics:{__pD:qx.locale.Manager.getInstance(),getAmMarker:function(C){return this.__pD.localize(o,[],C);
},getPmMarker:function(D){return this.__pD.localize(s,[],D);
},getDayNames:function(length,E,F){var F=F?F:j;
{};
var H=[B,a,b,d,h,c,g];
var I=[];

for(var i=0;i<H.length;i++){var G=f+F+k+length+k+H[i];
I.push(this.__pD.localize(G,[],E));
}return I;
},getDayName:function(length,J,K,L){var L=L?L:j;
{};
var N=[B,a,b,d,h,c,g];
var M=f+L+k+length+k+N[J];
return this.__pD.localize(M,[],K);
},getMonthNames:function(length,O,P){var P=P?P:j;
{};
var R=[];

for(var i=0;i<12;i++){var Q=e+P+k+length+k+(i+1);
R.push(this.__pD.localize(Q,[],O));
}return R;
},getMonthName:function(length,S,T,U){var U=U?U:j;
{};
var V=e+U+k+length+k+(S+1);
return this.__pD.localize(V,[],T);
},getDateFormat:function(W,X){{};
var Y=v+W;
return this.__pD.localize(Y,[],X);
},getDateTimeFormat:function(ba,bb,bc){var be=m+ba;
var bd=this.__pD.localize(be,[],bc);

if(bd==be){bd=bb;
}return bd;
},getTimeFormat:function(bf,bg){{};
var bi=n+bf;
var bh=this.__pD.localize(bi,[],bg);

if(bh!=bi){return bh;
}
switch(bf){case A:case r:return qx.locale.Date.getDateTimeFormat(x,z);
case q:return qx.locale.Date.getDateTimeFormat(w,l);
case t:return qx.locale.Date.getDateTimeFormat(y,u);
default:throw new Error("This case should never happen.");
}},getWeekStart:function(bj){var bk={"MV":5,"AE":6,"AF":6,"BH":6,"DJ":6,"DZ":6,"EG":6,"ER":6,"ET":6,"IQ":6,"IR":6,"JO":6,"KE":6,"KW":6,"LB":6,"LY":6,"MA":6,"OM":6,"QA":6,"SA":6,"SD":6,"SO":6,"TN":6,"YE":6,"AS":0,"AU":0,"AZ":0,"BW":0,"CA":0,"CN":0,"FO":0,"GE":0,"GL":0,"GU":0,"HK":0,"IE":0,"IL":0,"IS":0,"JM":0,"JP":0,"KG":0,"KR":0,"LA":0,"MH":0,"MN":0,"MO":0,"MP":0,"MT":0,"NZ":0,"PH":0,"PK":0,"SG":0,"TH":0,"TT":0,"TW":0,"UM":0,"US":0,"UZ":0,"VI":0,"ZA":0,"ZW":0,"MW":0,"NG":0,"TJ":0};
var bl=qx.locale.Date._getTerritory(bj);
return bk[bl]!=null?bk[bl]:1;
},getWeekendStart:function(bm){var bo={"EG":5,"IL":5,"SY":5,"IN":0,"AE":4,"BH":4,"DZ":4,"IQ":4,"JO":4,"KW":4,"LB":4,"LY":4,"MA":4,"OM":4,"QA":4,"SA":4,"SD":4,"TN":4,"YE":4};
var bn=qx.locale.Date._getTerritory(bm);
return bo[bn]!=null?bo[bn]:6;
},getWeekendEnd:function(bp){var bq={"AE":5,"BH":5,"DZ":5,"IQ":5,"JO":5,"KW":5,"LB":5,"LY":5,"MA":5,"OM":5,"QA":5,"SA":5,"SD":5,"TN":5,"YE":5,"AF":5,"IR":5,"EG":6,"IL":6,"SY":6};
var br=qx.locale.Date._getTerritory(bp);
return bq[br]!=null?bq[br]:0;
},isWeekend:function(bs,bt){var bv=qx.locale.Date.getWeekendStart(bt);
var bu=qx.locale.Date.getWeekendEnd(bt);

if(bu>bv){return ((bs>=bv)&&(bs<=bu));
}else{return ((bs>=bv)||(bs<=bu));
}},_getTerritory:function(bw){if(bw){var bx=bw.split(k)[1]||bw;
}else{bx=this.__pD.getTerritory()||this.__pD.getLanguage();
}return bx.toUpperCase();
}}});
})();
(function(){var k="",j="Number",h='</div>',g='" ',f="paneUpdated",e='<div>',d="</div>",c="overflow: hidden;",b="qx.event.type.Data",a="paneReloadsData",E="div",D='style="',C="_applyMaxCacheLines",B="qx.ui.table.pane.Pane",A="width: 100%;",z="qx.event.type.Event",w="_applyVisibleRowCount",v='>',u="line-height: ",t="appear",r='class="',s="width:100%;",p="px;",q='<div ',n="'>",o="_applyFirstVisibleRow",l="<div style='",m=";position:relative;";
qx.Class.define(B,{extend:qx.ui.core.Widget,construct:function(F){qx.ui.core.Widget.call(this);
this.__qC=F;
this.__qD=0;
this.__qE=0;
this.__qF=[];
},events:{"paneReloadsData":b,"paneUpdated":z},properties:{firstVisibleRow:{check:j,init:0,apply:o},visibleRowCount:{check:j,init:0,apply:w},maxCacheLines:{check:j,init:1000,apply:C},allowShrinkX:{refine:true,init:false}},members:{__qE:null,__qD:null,__qC:null,__qG:null,__qH:null,__qI:null,__qF:null,__qJ:0,_applyFirstVisibleRow:function(G,H){this.updateContent(false,G-H);
},_applyVisibleRowCount:function(I,J){this.updateContent(true);
},_getContentHint:function(){return {width:this.getPaneScroller().getTablePaneModel().getTotalWidth(),height:400};
},getPaneScroller:function(){return this.__qC;
},getTable:function(){return this.__qC.getTable();
},setFocusedCell:function(K,L,M){if(K!=this.__qI||L!=this.__qH){var N=this.__qH;
this.__qI=K;
this.__qH=L;
if(L!=N&&!M){if(N!==null){this.updateContent(false,null,N,true);
}
if(L!==null){this.updateContent(false,null,L,true);
}}}},onSelectionChanged:function(){this.updateContent(false,null,null,true);
},onFocusChanged:function(){this.updateContent(false,null,null,true);
},setColumnWidth:function(O,P){this.updateContent(true);
},onColOrderChanged:function(){this.updateContent(true);
},onPaneModelChanged:function(){this.updateContent(true);
},onTableModelDataChanged:function(Q,R,S,T){this.__qK();
var V=this.getFirstVisibleRow();
var U=this.getVisibleRowCount();

if(R==-1||R>=V&&Q<V+U){this.updateContent();
}},onTableModelMetaDataChanged:function(){this.updateContent(true);
},_applyMaxCacheLines:function(W,X){if(this.__qJ>=W&&W!==-1){this.__qK();
}},__qK:function(){this.__qF=[];
this.__qJ=0;
},__qL:function(Y,ba,bb){if(!ba&&!bb&&this.__qF[Y]){return this.__qF[Y];
}else{return null;
}},__qM:function(bc,bd,be,bf){var bg=this.getMaxCacheLines();

if(!be&&!bf&&!this.__qF[bc]&&bg>0){this._applyMaxCacheLines(bg);
this.__qF[bc]=bd;
this.__qJ+=1;
}},updateContent:function(bh,bi,bj,bk){if(bh){this.__qK();
}if(bi&&Math.abs(bi)<=Math.min(10,this.getVisibleRowCount())){this._scrollContent(bi);
}else if(bk&&!this.getTable().getAlwaysUpdateCells()){this._updateRowStyles(bj);
}else{this._updateAllRows();
}},_updateRowStyles:function(bl){var bp=this.getContentElement().getDomElement();

if(!bp||!bp.firstChild){this._updateAllRows();
return;
}var bt=this.getTable();
var bn=bt.getSelectionModel();
var bq=bt.getTableModel();
var bu=bt.getDataRowRenderer();
var bo=bp.firstChild.childNodes;
var bs={table:bt};
var bv=this.getFirstVisibleRow();
var y=0;
var bm=bo.length;

if(bl!=null){var br=bl-bv;

if(br>=0&&br<bm){bv=bl;
y=br;
bm=br+1;
}else{return;
}}
for(;y<bm;y++,bv++){bs.row=bv;
bs.selected=bn.isSelectedIndex(bv);
bs.focusedRow=(this.__qH==bv);
bs.rowData=bq.getRowData(bv);
bu.updateDataRowElement(bs,bo[y]);
}},_getRowsHtml:function(bw,bx){var bD=this.getTable();
var bG=bD.getSelectionModel();
var bA=bD.getTableModel();
var bB=bD.getTableColumnModel();
var bV=this.getPaneScroller().getTablePaneModel();
var bL=bD.getDataRowRenderer();
bA.prefetchRows(bw,bw+bx-1);
var bS=bD.getRowHeight();
var bU=bV.getColumnCount();
var bC=0;
var bz=[];
for(var x=0;x<bU;x++){var bY=bV.getColumnAtX(x);
var bF=bB.getColumnWidth(bY);
bz.push({col:bY,xPos:x,editable:bA.isColumnEditable(bY),focusedCol:this.__qI==bY,styleLeft:bC,styleWidth:bF});
bC+=bF;
}var bX=[];
var ca=false;

for(var bE=bw;bE<bw+bx;bE++){var bH=bG.isSelectedIndex(bE);
var bK=(this.__qH==bE);
var bP=this.__qL(bE,bH,bK);

if(bP){bX.push(bP);
continue;
}var by=[];
var bR={table:bD};
bR.styleHeight=bS;
bR.row=bE;
bR.selected=bH;
bR.focusedRow=bK;
bR.rowData=bA.getRowData(bE);

if(!bR.rowData){ca=true;
}by.push(q);
var bO=bL.getRowAttributes(bR);

if(bO){by.push(bO);
}var bN=bL.getRowClass(bR);

if(bN){by.push(r,bN,g);
}var bM=bL.createRowStyle(bR);
bM+=m+bL.getRowHeightStyle(bS)+s;

if(bM){by.push(D,bM,g);
}by.push(v);
var bW=false;

for(x=0;x<bU&&!bW;x++){var bI=bz[x];

for(var bT in bI){bR[bT]=bI[bT];
}var bY=bR.col;
bR.value=bA.getValue(bY,bE);
var bJ=bB.getDataCellRenderer(bY);
bR.style=bJ.getDefaultCellStyle();
bW=bJ.createDataCellHtml(bR,by)||false;
}by.push(h);
var bQ=by.join(k);
this.__qM(bE,bQ,bH,bK);
bX.push(bQ);
}this.fireDataEvent(a,ca);
return bX.join(k);
},_scrollContent:function(cb){var cc=this.getContentElement().getDomElement();

if(!(cc&&cc.firstChild)){this._updateAllRows();
return;
}var cl=cc.firstChild;
var cd=cl.childNodes;
var cj=this.getVisibleRowCount();
var ci=this.getFirstVisibleRow();
var cg=this.getTable().getTableModel();
var cm=0;
cm=cg.getRowCount();
if(ci+cj>cm){this._updateAllRows();
return;
}var cn=cb<0?cj+cb:0;
var ce=cb<0?0:cj-cb;

for(i=Math.abs(cb)-1;i>=0;i--){var ch=cd[cn];

try{cl.removeChild(ch);
}catch(co){break;
}}if(!this.__qG){this.__qG=document.createElement(E);
}var ck=e;
ck+=this._getRowsHtml(ci+ce,Math.abs(cb));
ck+=h;
this.__qG.innerHTML=ck;
var cf=this.__qG.firstChild.childNodes;
if(cb>0){for(var i=cf.length-1;i>=0;i--){var ch=cf[0];
cl.appendChild(ch);
}}else{for(var i=cf.length-1;i>=0;i--){var ch=cf[cf.length-1];
cl.insertBefore(ch,cl.firstChild);
}}if(this.__qH!==null){this._updateRowStyles(this.__qH-cb);
this._updateRowStyles(this.__qH);
}this.fireEvent(f);
},_updateAllRows:function(){var cs=this.getContentElement().getDomElement();

if(!cs){this.addListenerOnce(t,arguments.callee,this);
return;
}var cy=this.getTable();
var cv=cy.getTableModel();
var cx=this.getPaneScroller().getTablePaneModel();
var cw=cx.getColumnCount();
var cp=cy.getRowHeight();
var ct=this.getFirstVisibleRow();
var cq=this.getVisibleRowCount();
var cz=cv.getRowCount();

if(ct+cq>cz){cq=Math.max(0,cz-ct);
}var cr=cx.getTotalWidth();
var cu;
if(cq>0){cu=[l,A,(cy.getForceLineHeight()?u+cp+p:k),c,n,this._getRowsHtml(ct,cq),d];
}else{cu=[];
}var cA=cu.join(k);
cs.innerHTML=cA;
this.setWidth(cr);
this.__qD=cw;
this.__qE=cq;
this.fireEvent(f);
}},destruct:function(){this.__qG=this.__qC=this.__qF=null;
}});
})();
(function(){var e="first",d="last",c="hovered",b="__qO",a="qx.ui.table.pane.Header";
qx.Class.define(a,{extend:qx.ui.core.Widget,construct:function(f){qx.ui.core.Widget.call(this);
this._setLayout(new qx.ui.layout.HBox());
this.__qN=new qx.ui.core.Blocker(this);
this.__qO=f;
},members:{__qO:null,__qP:null,__qQ:null,__qN:null,getPaneScroller:function(){return this.__qO;
},getTable:function(){return this.__qO.getTable();
},getBlocker:function(){return this.__qN;
},onColOrderChanged:function(){this._updateContent(true);
},onPaneModelChanged:function(){this._updateContent(true);
},onTableModelMetaDataChanged:function(){this._updateContent();
},setColumnWidth:function(g,h,i){var j=this.getHeaderWidgetAtColumn(g);

if(j!=null){j.setWidth(h);
}},setMouseOverColumn:function(k){if(k!=this.__qQ){if(this.__qQ!=null){var l=this.getHeaderWidgetAtColumn(this.__qQ);

if(l!=null){l.removeState(c);
}}
if(k!=null){this.getHeaderWidgetAtColumn(k).addState(c);
}this.__qQ=k;
}},getHeaderWidgetAtColumn:function(m){var n=this.getPaneScroller().getTablePaneModel().getX(m);
return this._getChildren()[n];
},showColumnMoveFeedback:function(o,x){var s=this.getContainerLocation();

if(this.__qP==null){var y=this.getTable();
var p=this.getPaneScroller().getTablePaneModel().getX(o);
var r=this._getChildren()[p];
var t=y.getTableModel();
var v=y.getTableColumnModel();
var w={xPos:p,col:o,name:t.getColumnName(o),table:y};
var u=v.getHeaderCellRenderer(o);
var q=u.createHeaderCell(w);
var z=r.getBounds();
q.setWidth(z.width);
q.setHeight(z.height);
q.setZIndex(1000000);
q.setOpacity(0.8);
q.setLayoutProperties({top:s.top});
this.getApplicationRoot().add(q);
this.__qP=q;
}this.__qP.setLayoutProperties({left:s.left+x});
this.__qP.show();
},hideColumnMoveFeedback:function(){if(this.__qP!=null){this.__qP.destroy();
this.__qP=null;
}},isShowingColumnMoveFeedback:function(){return this.__qP!=null;
},_updateContent:function(A){var K=this.getTable();
var E=K.getTableModel();
var H=K.getTableColumnModel();
var J=this.getPaneScroller().getTablePaneModel();
var M=this._getChildren();
var F=J.getColumnCount();
var I=E.getSortColumnIndex();
if(A){this._cleanUpCells();
}var B={};
B.sortedAscending=E.isSortAscending();

for(var x=0;x<F;x++){var D=J.getColumnAtX(x);

if(D===undefined){continue;
}var L=H.getColumnWidth(D);
var G=H.getHeaderCellRenderer(D);
B.xPos=x;
B.col=D;
B.name=E.getColumnName(D);
B.editable=E.isColumnEditable(D);
B.sorted=(D==I);
B.table=K;
var C=M[x];
if(C==null){C=G.createHeaderCell(B);
C.set({width:L});
this._add(C);
}else{G.updateHeaderCell(B,C);
}if(x===0){C.addState(e);
C.removeState(d);
}else if(x===F-1){C.removeState(e);
C.addState(d);
}else{C.removeState(e);
C.removeState(d);
}}},_cleanUpCells:function(){var O=this._getChildren();

for(var x=O.length-1;x>=0;x--){var N=O[x];
N.destroy();
}}},destruct:function(){this.__qN.dispose();
this._disposeObjects(b);
}});
})();
(function(){var b="qx.nativeScrollBars",a="qx.ui.core.scroll.MScrollBarFactory";
qx.core.Setting.define(b,false);
qx.Mixin.define(a,{members:{_createScrollBar:function(c){if(qx.core.Setting.get(b)){return new qx.ui.core.scroll.NativeScrollBar(c);
}else{return new qx.ui.core.scroll.ScrollBar(c);
}}}});
})();
(function(){var m="Boolean",l="resize-line",k="mousedown",j="qx.event.type.Data",i="mouseup",h="qx.ui.table.pane.CellEvent",g="scroll",d="focus-indicator",c="excluded",b="scrollbar-y",bm="table-scroller-focus-indicator",bl="visible",bk="mousemove",bj="header",bi="editing",bh="click",bg="modelChanged",bf="scrollbar-x",be="cellClick",bd="pane",t="mouseout",u="__qS",r="changeHorizontalScrollBarVisible",s="bottom",p="_applyScrollTimeout",q="changeScrollX",n="_applyTablePaneModel",o="Integer",z="dblclick",A="dataEdited",I="__rb",G="mousewheel",Q="interval",L="qx.ui.table.pane.Scroller",Y="__qT",V="_applyShowCellFocusIndicator",C="__qY",bc="resize",bb="vertical",ba="changeScrollY",B="appear",E="__qU",F="__qW",H="table-scroller",J="beforeSort",M="cellDblclick",S="horizontal",X="__ra",v="losecapture",w="contextmenu",D="__qX",P="col-resize",O="disappear",N="_applyVerticalScrollBarVisible",U="__qV",T="_applyHorizontalScrollBarVisible",K="cellContextmenu",R="close",a="changeTablePaneModel",W="qx.ui.table.pane.Model",y="changeVerticalScrollBarVisible";
qx.Class.define(L,{extend:qx.ui.core.Widget,include:qx.ui.core.scroll.MScrollBarFactory,construct:function(bn){qx.ui.core.Widget.call(this);
this.__qR=bn;
var bo=new qx.ui.layout.Grid();
bo.setColumnFlex(0,1);
bo.setRowFlex(1,1);
this._setLayout(bo);
this.__qS=this._showChildControl(bf);
this.__qT=this._showChildControl(b);
this.__qU=this._showChildControl(bj);
this.__qV=this._showChildControl(bd);
this.__qW=new qx.ui.container.Composite(new qx.ui.layout.HBox()).set({minWidth:0});
this._add(this.__qW,{row:0,column:0,colSpan:2});
this.__qX=new qx.ui.table.pane.Clipper();
this.__qX.add(this.__qU);
this.__qX.addListener(v,this._onChangeCaptureHeader,this);
this.__qX.addListener(bk,this._onMousemoveHeader,this);
this.__qX.addListener(k,this._onMousedownHeader,this);
this.__qX.addListener(i,this._onMouseupHeader,this);
this.__qX.addListener(bh,this._onClickHeader,this);
this.__qW.add(this.__qX,{flex:1});
this.__qY=new qx.ui.table.pane.Clipper();
this.__qY.add(this.__qV);
this.__qY.addListener(G,this._onMousewheel,this);
this.__qY.addListener(bk,this._onMousemovePane,this);
this.__qY.addListener(k,this._onMousedownPane,this);
this.__qY.addListener(i,this._onMouseupPane,this);
this.__qY.addListener(bh,this._onClickPane,this);
this.__qY.addListener(w,this._onContextMenu,this);
this.__qY.addListener(z,this._onDblclickPane,this);
this.__qY.addListener(bc,this._onResizePane,this);
this._add(this.__qY,{row:1,column:0});
this.__ra=this.getChildControl(d);
this.initShowCellFocusIndicator();
this.getChildControl(l).hide();
this.addListener(t,this._onMouseout,this);
this.addListener(B,this._onAppear,this);
this.addListener(O,this._onDisappear,this);
this.__rb=new qx.event.Timer();
this.__rb.addListener(Q,this._oninterval,this);
this.initScrollTimeout();
},statics:{MIN_COLUMN_WIDTH:10,RESIZE_REGION_RADIUS:5,CLICK_TOLERANCE:5,HORIZONTAL_SCROLLBAR:1,VERTICAL_SCROLLBAR:2},events:{"changeScrollY":j,"changeScrollX":j,"cellClick":h,"cellDblclick":h,"cellContextmenu":h,"beforeSort":j},properties:{horizontalScrollBarVisible:{check:m,init:false,apply:T,event:r},verticalScrollBarVisible:{check:m,init:false,apply:N,event:y},tablePaneModel:{check:W,apply:n,event:a},liveResize:{check:m,init:false},focusCellOnMouseMove:{check:m,init:false},selectBeforeFocus:{check:m,init:false},showCellFocusIndicator:{check:m,init:true,apply:V},contextMenuFromDataCellsOnly:{check:m,init:true},resetSelectionOnHeaderClick:{check:m,init:true},scrollTimeout:{check:o,init:100,apply:p},appearance:{refine:true,init:H}},members:{__rc:null,__qR:null,__rd:null,__re:null,__rf:null,__rg:null,__rh:null,__ri:null,__rj:null,__rk:null,__rl:null,__rm:null,__rn:null,__ro:null,__rp:false,__rq:null,__rr:null,__rs:null,__rt:null,__ru:null,__rv:null,__rw:null,__rx:null,__qS:null,__qT:null,__qU:null,__qX:null,__qV:null,__qY:null,__ra:null,__qW:null,__rb:null,getPaneInsetRight:function(){var br=this.getTopRightWidget();
var bs=br&&br.isVisible()&&br.getBounds()?br.getBounds().width+br.getMarginLeft()+br.getMarginRight():0;
var bq=this.__qT;
var bp=this.getVerticalScrollBarVisible()?this.getVerticalScrollBarWidth()+bq.getMarginLeft()+bq.getMarginRight():0;
return Math.max(bs,bp);
},setPaneWidth:function(bt){if(this.isVerticalScrollBarVisible()){bt+=this.getPaneInsetRight();
}this.setWidth(bt);
},_createChildControlImpl:function(bu,bv){var bw;

switch(bu){case bj:bw=(this.getTable().getNewTablePaneHeader())(this);
break;
case bd:bw=(this.getTable().getNewTablePane())(this);
break;
case d:bw=new qx.ui.table.pane.FocusIndicator(this);
bw.setUserBounds(0,0,0,0);
bw.setZIndex(1000);
bw.addListener(i,this._onMouseupFocusIndicator,this);
this.__qY.add(bw);
bw.show();
bw.setDecorator(null);
break;
case l:bw=new qx.ui.core.Widget();
bw.setUserBounds(0,0,0,0);
bw.setZIndex(1000);
this.__qY.add(bw);
break;
case bf:bw=this._createScrollBar(S).set({minWidth:0,alignY:s});
bw.addListener(g,this._onScrollX,this);
this._add(bw,{row:2,column:0});
break;
case b:bw=this._createScrollBar(bb);
bw.addListener(g,this._onScrollY,this);
this._add(bw,{row:1,column:1});
break;
}return bw||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,bu);
},_applyHorizontalScrollBarVisible:function(bx,by){this.__qS.setVisibility(bx?bl:c);
},_applyVerticalScrollBarVisible:function(bz,bA){this.__qT.setVisibility(bz?bl:c);
},_applyTablePaneModel:function(bB,bC){if(bC!=null){bC.removeListener(bg,this._onPaneModelChanged,this);
}bB.addListener(bg,this._onPaneModelChanged,this);
},_applyShowCellFocusIndicator:function(bD,bE){if(bD){this.__ra.setDecorator(bm);
this._updateFocusIndicator();
}else{if(this.__ra){this.__ra.setDecorator(null);
}}},getScrollY:function(){return this.__qT.getPosition();
},setScrollY:function(scrollY,bF){this.__qT.scrollTo(scrollY);

if(bF){this._updateContent();
}},getScrollX:function(){return this.__qS.getPosition();
},setScrollX:function(scrollX){this.__qS.scrollTo(scrollX);
},getTable:function(){return this.__qR;
},onColVisibilityChanged:function(){this.updateHorScrollBarMaximum();
this._updateFocusIndicator();
},setColumnWidth:function(bG,bH){this.__qU.setColumnWidth(bG,bH);
this.__qV.setColumnWidth(bG,bH);
var bI=this.getTablePaneModel();
var x=bI.getX(bG);

if(x!=-1){this.updateHorScrollBarMaximum();
this._updateFocusIndicator();
}},onColOrderChanged:function(){this.__qU.onColOrderChanged();
this.__qV.onColOrderChanged();
this.updateHorScrollBarMaximum();
},onTableModelDataChanged:function(bJ,bK,bL,bM){this.__qV.onTableModelDataChanged(bJ,bK,bL,bM);
var bN=this.getTable().getTableModel().getRowCount();

if(bN!=this.__rc){this.updateVerScrollBarMaximum();

if(this.getFocusedRow()>=bN){if(bN==0){this.setFocusedCell(null,null);
}else{this.setFocusedCell(this.getFocusedColumn(),bN-1);
}}this.__rc=bN;
}},onSelectionChanged:function(){this.__qV.onSelectionChanged();
},onFocusChanged:function(){this.__qV.onFocusChanged();
},onTableModelMetaDataChanged:function(){this.__qU.onTableModelMetaDataChanged();
this.__qV.onTableModelMetaDataChanged();
},_onPaneModelChanged:function(){this.__qU.onPaneModelChanged();
this.__qV.onPaneModelChanged();
},_onResizePane:function(){this.updateHorScrollBarMaximum();
this.updateVerScrollBarMaximum();
this._updateContent();
this.__qU._updateContent();
this.__qR._updateScrollBarVisibility();
},updateHorScrollBarMaximum:function(){var bR=this.__qY.getInnerSize();

if(!bR){return ;
}var bP=this.getTablePaneModel().getTotalWidth();
var bQ=this.__qS;

if(bR.width<bP){var bO=Math.max(0,bP-bR.width);
bQ.setMaximum(bO);
bQ.setKnobFactor(bR.width/bP);
var bS=bQ.getPosition();
bQ.setPosition(Math.min(bS,bO));
}else{bQ.setMaximum(0);
bQ.setKnobFactor(1);
bQ.setPosition(0);
}},updateVerScrollBarMaximum:function(){var cb=this.__qY.getInnerSize();

if(!cb){return ;
}var bY=this.getTable().getTableModel();
var bU=bY.getRowCount();

if(this.getTable().getKeepFirstVisibleRowComplete()){bU+=1;
}var bT=this.getTable().getRowHeight();
var bW=bU*bT;
var ca=this.__qT;

if(cb.height<bW){var bV=Math.max(0,bW-cb.height);
ca.setMaximum(bV);
ca.setKnobFactor(cb.height/bW);
var bX=ca.getPosition();
ca.setPosition(Math.min(bX,bV));
}else{ca.setMaximum(0);
ca.setKnobFactor(1);
ca.setPosition(0);
}},onKeepFirstVisibleRowCompleteChanged:function(){this.updateVerScrollBarMaximum();
this._updateContent();
},_onAppear:function(){this._startInterval(this.getScrollTimeout());
},_onDisappear:function(){this._stopInterval();
},_onScrollX:function(e){var cc=e.getData();
this.fireDataEvent(q,cc,e.getOldData());
this.__qX.scrollToX(cc);
this.__qY.scrollToX(cc);
},_onScrollY:function(e){this.fireDataEvent(ba,e.getData(),e.getOldData());
this._postponedUpdateContent();
},_onMousewheel:function(e){var cd=this.getTable();

if(!cd.getEnabled()){return;
}var cf=qx.bom.client.Engine.GECKO?1:3;
var ce=this.__qT.getPosition()+((e.getWheelDelta()*cf)*cd.getRowHeight());
this.__qT.scrollTo(ce);
if(this.__rr&&this.getFocusCellOnMouseMove()){this._focusCellAtPagePos(this.__rr,this.__rs);
}e.stop();
},__ry:function(cg){var cl=this.getTable();
var cm=this.__qU.getHeaderWidgetAtColumn(this.__rl);
var ch=cm.getSizeHint().minWidth;
var cj=Math.max(ch,this.__rn+cg-this.__rm);

if(this.getLiveResize()){var ci=cl.getTableColumnModel();
ci.setColumnWidth(this.__rl,cj,true);
}else{this.__qU.setColumnWidth(this.__rl,cj,true);
var ck=this.getTablePaneModel();
this._showResizeLine(ck.getColumnLeft(this.__rl)+cj);
}this.__rm+=cj-this.__rn;
this.__rn=cj;
},__rz:function(cn){var co=qx.ui.table.pane.Scroller.CLICK_TOLERANCE;

if(this.__qU.isShowingColumnMoveFeedback()||cn>this.__rk+co||cn<this.__rk-co){this.__rh+=cn-this.__rk;
this.__qU.showColumnMoveFeedback(this.__rg,this.__rh);
var cp=this.__qR.getTablePaneScrollerAtPageX(cn);

if(this.__rj&&this.__rj!=cp){this.__rj.hideColumnMoveFeedback();
}
if(cp!=null){this.__ri=cp.showColumnMoveFeedback(cn);
}else{this.__ri=null;
}this.__rj=cp;
this.__rk=cn;
}},_onMousemoveHeader:function(e){var cw=this.getTable();

if(!cw.getEnabled()){return;
}var cx=false;
var cq=null;
var cu=e.getDocumentLeft();
var cv=e.getDocumentTop();
this.__rr=cu;
this.__rs=cv;

if(this.__rl!=null){this.__ry(cu);
cx=true;
e.stopPropagation();
}else if(this.__rg!=null){this.__rz(cu);
e.stopPropagation();
}else{var cr=this._getResizeColumnForPageX(cu);

if(cr!=-1){cx=true;
}else{var ct=cw.getTableModel();
var cy=this._getColumnForPageX(cu);

if(cy!=null&&ct.isColumnSortable(cy)){cq=cy;
}}}var cs=cx?P:null;
this.getApplicationRoot().setGlobalCursor(cs);
this.setCursor(cs);
this.__qU.setMouseOverColumn(cq);
},_onMousemovePane:function(e){var cz=this.getTable();

if(!cz.getEnabled()){return;
}var cB=e.getDocumentLeft();
var cC=e.getDocumentTop();
this.__rr=cB;
this.__rs=cC;
var cA=this._getRowForPagePos(cB,cC);

if(cA!=null&&this._getColumnForPageX(cB)!=null){if(this.getFocusCellOnMouseMove()){this._focusCellAtPagePos(cB,cC);
}}this.__qU.setMouseOverColumn(null);
},_onMousedownHeader:function(e){if(!this.getTable().getEnabled()){return;
}var cE=e.getDocumentLeft();
var cF=this._getResizeColumnForPageX(cE);

if(cF!=-1){this._startResizeHeader(cF,cE);
e.stop();
}else{var cD=this._getColumnForPageX(cE);

if(cD!=null){this._startMoveHeader(cD,cE);
e.stop();
}}},_startResizeHeader:function(cG,cH){var cI=this.getTable().getTableColumnModel();
this.__rl=cG;
this.__rm=cH;
this.__rn=cI.getColumnWidth(this.__rl);
this.__qX.capture();
},_startMoveHeader:function(cJ,cK){this.__rg=cJ;
this.__rk=cK;
this.__rh=this.getTablePaneModel().getColumnLeft(cJ);
this.__qX.capture();
},_onMousedownPane:function(e){var cO=this.getTable();

if(!cO.getEnabled()){return;
}
if(cO.isEditing()){cO.stopEditing();
}var cL=e.getDocumentLeft();
var cN=e.getDocumentTop();
var cQ=this._getRowForPagePos(cL,cN);
var cP=this._getColumnForPageX(cL);

if(cQ!==null){this.__ro={row:cQ,col:cP};
this.__rp=false;
var cM=this.getSelectBeforeFocus();

if(cM){cO.getSelectionManager().handleMouseDown(cQ,e);
}if(!this.getFocusCellOnMouseMove()){this._focusCellAtPagePos(cL,cN);
}
if(!cM){cO.getSelectionManager().handleMouseDown(cQ,e);
}}},_onMouseupFocusIndicator:function(e){if(this.__ro&&!this.__rp&&!this.isEditing()&&this.__ra.getRow()==this.__ro.row&&this.__ra.getColumn()==this.__ro.col){this.fireEvent(be,qx.ui.table.pane.CellEvent,[this,e,this.__ro.row,this.__ro.col],true);
this.__rp=true;
}else if(!this.isEditing()){this._onMousedownPane(e);
}},_onChangeCaptureHeader:function(e){if(this.__rl!=null){this._stopResizeHeader();
}
if(this.__rg!=null){this._stopMoveHeader();
}},_stopResizeHeader:function(){var cR=this.getTable().getTableColumnModel();
if(!this.getLiveResize()){this._hideResizeLine();
cR.setColumnWidth(this.__rl,this.__rn,true);
}this.__rl=null;
this.__qX.releaseCapture();
this.getApplicationRoot().setGlobalCursor(null);
this.setCursor(null);
if(this.isEditing()){var cS=this.__rv.getBounds().height;
this.__rv.setUserBounds(0,0,this.__rn,cS);
}},_stopMoveHeader:function(){var cX=this.getTable().getTableColumnModel();
var cY=this.getTablePaneModel();
this.__qU.hideColumnMoveFeedback();

if(this.__rj){this.__rj.hideColumnMoveFeedback();
}
if(this.__ri!=null){var db=cY.getFirstColumnX()+cY.getX(this.__rg);
var cW=this.__ri;

if(cW!=db&&cW!=db+1){var da=cX.getVisibleColumnAtX(db);
var cV=cX.getVisibleColumnAtX(cW);
var cU=cX.getOverallX(da);
var cT=(cV!=null)?cX.getOverallX(cV):cX.getOverallColumnCount();

if(cT>cU){cT--;
}cX.moveColumn(cU,cT);
this._updateFocusIndicator();
}}this.__rg=null;
this.__ri=null;
this.__qX.releaseCapture();
},_onMouseupPane:function(e){var dc=this.getTable();

if(!dc.getEnabled()){return;
}var dd=this._getRowForPagePos(e.getDocumentLeft(),e.getDocumentTop());

if(dd!=-1&&dd!=null&&this._getColumnForPageX(e.getDocumentLeft())!=null){dc.getSelectionManager().handleMouseUp(dd,e);
}},_onMouseupHeader:function(e){var de=this.getTable();

if(!de.getEnabled()){return;
}
if(this.__rl!=null){this._stopResizeHeader();
this.__rq=true;
e.stop();
}else if(this.__rg!=null){this._stopMoveHeader();
e.stop();
}},_onClickHeader:function(e){if(this.__rq){this.__rq=false;
return;
}var dj=this.getTable();

if(!dj.getEnabled()){return;
}var dh=dj.getTableModel();
var di=e.getDocumentLeft();
var dg=this._getResizeColumnForPageX(di);

if(dg==-1){var dm=this._getColumnForPageX(di);

if(dm!=null&&dh.isColumnSortable(dm)){var df=dh.getSortColumnIndex();
var dk=(dm!=df)?true:!dh.isSortAscending();
var dl={column:dm,ascending:dk,clickEvent:e};

if(this.fireDataEvent(J,dl,null,true)){dh.sortByColumn(dm,dk);

if(this.getResetSelectionOnHeaderClick()){dj.getSelectionModel().resetSelection();
}}}}e.stop();
},_onClickPane:function(e){var dn=this.getTable();

if(!dn.getEnabled()){return;
}var dr=e.getDocumentLeft();
var ds=e.getDocumentTop();
var dp=this._getRowForPagePos(dr,ds);
var dq=this._getColumnForPageX(dr);

if(dp!=null&&dq!=null){dn.getSelectionManager().handleClick(dp,e);

if(this.__ra.isHidden()||(this.__ro&&!this.__rp&&!this.isEditing()&&dp==this.__ro.row&&dq==this.__ro.col)){this.fireEvent(be,qx.ui.table.pane.CellEvent,[this,e,dp,dq],true);
this.__rp=true;
}}},_onContextMenu:function(e){var dw=e.getDocumentLeft();
var dx=e.getDocumentTop();
var du=this._getRowForPagePos(dw,dx);
var dv=this._getColumnForPageX(dw);
if(du===null&&this.getContextMenuFromDataCellsOnly()){return;
}
if(!this.getShowCellFocusIndicator()||du===null||(this.__ro&&du==this.__ro.row&&dv==this.__ro.col)){this.fireEvent(K,qx.ui.table.pane.CellEvent,[this,e,du,dv],true);
var dt=this.getTable().getContextMenu();

if(dt){if(dt.getChildren().length>0){dt.openAtMouse(e);
}else{dt.exclude();
}e.preventDefault();
}}},_onContextMenuOpen:function(e){},_onDblclickPane:function(e){var dz=e.getDocumentLeft();
var dA=e.getDocumentTop();
this._focusCellAtPagePos(dz,dA);
this.startEditing();
var dy=this._getRowForPagePos(dz,dA);

if(dy!=-1&&dy!=null){this.fireEvent(M,qx.ui.table.pane.CellEvent,[this,e,dy],true);
}},_onMouseout:function(e){var dB=this.getTable();

if(!dB.getEnabled()){return;
}if(this.__rl==null){this.setCursor(null);
this.getApplicationRoot().setGlobalCursor(null);
}this.__qU.setMouseOverColumn(null);
},_showResizeLine:function(x){var dD=this._showChildControl(l);
var dC=dD.getWidth();
var dE=this.__qY.getBounds();
dD.setUserBounds(x-Math.round(dC/2),0,dC,dE.height);
},_hideResizeLine:function(){this._excludeChildControl(l);
},showColumnMoveFeedback:function(dF){var dO=this.getTablePaneModel();
var dN=this.getTable().getTableColumnModel();
var dI=this.__qV.getContainerLocation().left;
var dM=dO.getColumnCount();
var dJ=0;
var dH=0;
var dR=dI;

for(var dG=0;dG<dM;dG++){var dK=dO.getColumnAtX(dG);
var dP=dN.getColumnWidth(dK);

if(dF<dR+dP/2){break;
}dR+=dP;
dJ=dG+1;
dH=dR-dI;
}var dL=this.__qY.getContainerLocation().left;
var dQ=this.__qY.getBounds().width;
var scrollX=dL-dI;
dH=qx.lang.Number.limit(dH,scrollX+2,scrollX+dQ-1);
this._showResizeLine(dH);
return dO.getFirstColumnX()+dJ;
},hideColumnMoveFeedback:function(){this._hideResizeLine();
},_focusCellAtPagePos:function(dS,dT){var dV=this._getRowForPagePos(dS,dT);

if(dV!=-1&&dV!=null){var dU=this._getColumnForPageX(dS);
this.__qR.setFocusedCell(dU,dV);
}},setFocusedCell:function(dW,dX){if(!this.isEditing()){this.__qV.setFocusedCell(dW,dX,this.__re);
this.__rt=dW;
this.__ru=dX;
this._updateFocusIndicator();
}},getFocusedColumn:function(){return this.__rt;
},getFocusedRow:function(){return this.__ru;
},scrollCellVisible:function(dY,ea){var ek=this.getTablePaneModel();
var eb=ek.getX(dY);

if(eb!=-1){var eh=this.__qY.getInnerSize();

if(!eh){return;
}var ei=this.getTable().getTableColumnModel();
var ee=ek.getColumnLeft(dY);
var el=ei.getColumnWidth(dY);
var ec=this.getTable().getRowHeight();
var em=ea*ec;
var scrollX=this.getScrollX();
var scrollY=this.getScrollY();
var ej=Math.min(ee,ee+el-eh.width);
var eg=ee;
this.setScrollX(Math.max(ej,Math.min(eg,scrollX)));
var ed=em+ec-eh.height;

if(this.getTable().getKeepFirstVisibleRowComplete()){ed+=ec;
}var ef=em;
this.setScrollY(Math.max(ed,Math.min(ef,scrollY)),true);
}},isEditing:function(){return this.__rv!=null;
},startEditing:function(){var er=this.getTable();
var ep=er.getTableModel();
var et=this.__rt;

if(!this.isEditing()&&(et!=null)&&ep.isColumnEditable(et)){var eu=this.__ru;
var en=this.getTablePaneModel().getX(et);
var eo=ep.getValue(et,eu);
this.scrollCellVisible(en,eu);
this.__rw=er.getTableColumnModel().getCellEditorFactory(et);
var eq={col:et,row:eu,xPos:en,value:eo,table:er};
this.__rv=this.__rw.createCellEditor(eq);
if(this.__rv===null){return false;
}else if(this.__rv instanceof qx.ui.window.Window){this.__rv.setModal(true);
this.__rv.setShowClose(false);
this.__rv.addListener(R,this._onCellEditorModalWindowClose,this);
var f=er.getModalCellEditorPreOpenFunction();

if(f!=null){f(this.__rv,eq);
}this.__rv.open();
}else{var es=this.__ra.getInnerSize();
this.__rv.setUserBounds(0,0,es.width,es.height);
this.__ra.addListener(k,function(e){this.__ro={row:this.__ru,col:this.__rt};
e.stopPropagation();
},this);
this.__ra.add(this.__rv);
this.__ra.addState(bi);
this.__ra.setKeepActive(false);
this.__ra.setDecorator(bm);
this.__rv.focus();
this.__rv.activate();
}return true;
}return false;
},stopEditing:function(){if(!this.getShowCellFocusIndicator()){this.__ra.setDecorator(null);
}this.flushEditor();
this.cancelEditing();
},flushEditor:function(){if(this.isEditing()){var ew=this.__rw.getCellEditorValue(this.__rv);
var ev=this.getTable().getTableModel().getValue(this.__rt,this.__ru);
this.getTable().getTableModel().setValue(this.__rt,this.__ru,ew);
this.__qR.focus();
this.__qR.fireDataEvent(A,{row:this.__ru,col:this.__rt,oldValue:ev,value:ew});
}},cancelEditing:function(){if(this.isEditing()&&!this.__rv.pendingDispose){if(this._cellEditorIsModalWindow){this.__rv.destroy();
this.__rv=null;
this.__rw=null;
this.__rv.pendingDispose=true;
}else{this.__ra.removeState(bi);
this.__ra.setKeepActive(true);
this.__rv.destroy();
this.__rv=null;
this.__rw=null;
}}},_onCellEditorModalWindowClose:function(e){this.stopEditing();
},_getColumnForPageX:function(ex){var eA=this.getTable().getTableColumnModel();
var eB=this.getTablePaneModel();
var ez=eB.getColumnCount();
var eD=this.__qU.getContainerLocation().left;

for(var x=0;x<ez;x++){var ey=eB.getColumnAtX(x);
var eC=eA.getColumnWidth(ey);
eD+=eC;

if(ex<eD){return ey;
}}return null;
},_getResizeColumnForPageX:function(eE){var eI=this.getTable().getTableColumnModel();
var eJ=this.getTablePaneModel();
var eH=eJ.getColumnCount();
var eL=this.__qU.getContainerLocation().left;
var eF=qx.ui.table.pane.Scroller.RESIZE_REGION_RADIUS;

for(var x=0;x<eH;x++){var eG=eJ.getColumnAtX(x);
var eK=eI.getColumnWidth(eG);
eL+=eK;

if(eE>=(eL-eF)&&eE<=(eL+eF)){return eG;
}}return -1;
},_getRowForPagePos:function(eM,eN){var eO=this.__qV.getContentLocation();

if(eM<eO.left||eM>eO.right){return null;
}
if(eN>=eO.top&&eN<=eO.bottom){var eP=this.getTable().getRowHeight();
var scrollY=this.__qT.getPosition();

if(this.getTable().getKeepFirstVisibleRowComplete()){scrollY=Math.floor(scrollY/eP)*eP;
}var eS=scrollY+eN-eO.top;
var eU=Math.floor(eS/eP);
var eT=this.getTable().getTableModel();
var eQ=eT.getRowCount();
return (eU<eQ)?eU:null;
}var eR=this.__qU.getContainerLocation();

if(eN>=eR.top&&eN<=eR.bottom&&eM<=eR.right){return -1;
}return null;
},setTopRightWidget:function(eV){var eW=this.__rx;

if(eW!=null){this.__qW.remove(eW);
}
if(eV!=null){this.__qW.add(eV);
}this.__rx=eV;
},getTopRightWidget:function(){return this.__rx;
},getHeader:function(){return this.__qU;
},getTablePane:function(){return this.__qV;
},getVerticalScrollBarWidth:function(){var eX=this.__qT;
return eX.isVisible()?(eX.getSizeHint().width||0):0;
},getNeededScrollBars:function(eY,fa){var fj=this.__qT;
var fn=fj.getSizeHint().width+fj.getMarginLeft()+fj.getMarginRight();
var fp=this.__qS;
var fo=fp.getSizeHint().height+fp.getMarginTop()+fp.getMarginBottom();
var fh=this.__qY.getInnerSize();
var fb=fh?fh.width:0;

if(this.getVerticalScrollBarVisible()){fb+=fn;
}var fm=fh?fh.height:0;

if(this.getHorizontalScrollBarVisible()){fm+=fo;
}var fi=this.getTable().getTableModel();
var ff=fi.getRowCount();
var fc=this.getTablePaneModel().getTotalWidth();
var fk=this.getTable().getRowHeight()*ff;
var fe=false;
var fl=false;

if(fc>fb){fe=true;

if(fk>fm-fo){fl=true;
}}else if(fk>fm){fl=true;

if(!fa&&(fc>fb-fn)){fe=true;
}}var fg=qx.ui.table.pane.Scroller.HORIZONTAL_SCROLLBAR;
var fd=qx.ui.table.pane.Scroller.VERTICAL_SCROLLBAR;
return ((eY||fe)?fg:0)|((fa||!fl)?0:fd);
},getPaneClipper:function(){return this.__qY;
},_applyScrollTimeout:function(fq,fr){this._startInterval(fq);
},_startInterval:function(fs){this.__rb.setInterval(fs);
this.__rb.start();
},_stopInterval:function(){this.__rb.stop();
},_postponedUpdateContent:function(){this._updateContent();
},_oninterval:qx.event.GlobalError.observeMethod(function(){if(this.__re&&!this.__qV._layoutPending){this.__re=false;
this._updateContent();
}}),_updateContent:function(){var fx=this.__qY.getInnerSize();

if(!fx){return;
}var fA=fx.height;
var scrollX=this.__qS.getPosition();
var scrollY=this.__qT.getPosition();
var fu=this.getTable().getRowHeight();
var fv=Math.floor(scrollY/fu);
var fz=this.__qV.getFirstVisibleRow();
this.__qV.setFirstVisibleRow(fv);
var fw=Math.ceil(fA/fu);
var ft=0;
var fy=this.getTable().getKeepFirstVisibleRowComplete();

if(!fy){fw++;
ft=scrollY%fu;
}this.__qV.setVisibleRowCount(fw);

if(fv!=fz){this._updateFocusIndicator();
}this.__qY.scrollToX(scrollX);
if(!fy){this.__qY.scrollToY(ft);
}},_updateFocusIndicator:function(){var fB=this.getTable();

if(!fB.getEnabled()){return;
}this.__ra.moveToCell(this.__rt,this.__ru);
}},destruct:function(){this._stopInterval();
var fC=this.getTablePaneModel();

if(fC){fC.dispose();
}this.__ro=this.__rx=this.__qR=null;
this._disposeObjects(u,Y,D,C,X,E,U,F,I);
}});
})();
(function(){var b="qx.ui.core.scroll.IScrollBar",a="qx.event.type.Data";
qx.Interface.define(b,{events:{"scroll":a},properties:{orientation:{},maximum:{},position:{},knobFactor:{}},members:{scrollTo:function(c){this.assertNumber(c);
},scrollBy:function(d){this.assertNumber(d);
},scrollBySteps:function(e){this.assertNumber(e);
}}});
})();
(function(){var k="horizontal",j="px",i="scroll",h="vertical",g="-1px",f="qx.client",d="0",c="hidden",b="mousedown",a="qx.ui.core.scroll.NativeScrollBar",z="PositiveNumber",y="Integer",x="__nJ",w="mousemove",v="_applyMaximum",u="_applyOrientation",t="appear",s="opera",r="PositiveInteger",q="mshtml",o="mouseup",p="Number",m="_applyPosition",n="scrollbar",l="native";
qx.Class.define(a,{extend:qx.ui.core.Widget,implement:qx.ui.core.scroll.IScrollBar,construct:function(A){qx.ui.core.Widget.call(this);
this.addState(l);
this.getContentElement().addListener(i,this._onScroll,this);
this.addListener(b,this._stopPropagation,this);
this.addListener(o,this._stopPropagation,this);
this.addListener(w,this._stopPropagation,this);

if(qx.core.Variant.isSet(f,s)){this.addListener(t,this._onAppear,this);
}this.getContentElement().add(this._getScrollPaneElement());
if(A!=null){this.setOrientation(A);
}else{this.initOrientation();
}},properties:{appearance:{refine:true,init:n},orientation:{check:[k,h],init:k,apply:u},maximum:{check:r,apply:v,init:100},position:{check:p,init:0,apply:m,event:i},singleStep:{check:y,init:20},knobFactor:{check:z,nullable:true}},members:{__nI:null,__nJ:null,_getScrollPaneElement:function(){if(!this.__nJ){this.__nJ=new qx.html.Element();
}return this.__nJ;
},renderLayout:function(B,top,C,D){var E=qx.ui.core.Widget.prototype.renderLayout.call(this,B,top,C,D);
this._updateScrollBar();
return E;
},_getContentHint:function(){var F=qx.bom.element.Overflow.getScrollbarWidth();
return {width:this.__nI?100:F,maxWidth:this.__nI?null:F,minWidth:this.__nI?null:F,height:this.__nI?F:100,maxHeight:this.__nI?F:null,minHeight:this.__nI?F:null};
},_applyEnabled:function(G,H){qx.ui.core.Widget.prototype._applyEnabled.call(this,G,H);
this._updateScrollBar();
},_applyMaximum:function(I){this._updateScrollBar();
},_applyPosition:function(J){var content=this.getContentElement();

if(this.__nI){content.scrollToX(J);
}else{content.scrollToY(J);
}},_applyOrientation:function(K,L){var M=this.__nI=K===k;
this.set({allowGrowX:M,allowShrinkX:M,allowGrowY:!M,allowShrinkY:!M});

if(M){this.replaceState(h,k);
}else{this.replaceState(k,h);
}this.getContentElement().setStyles({overflowX:M?i:c,overflowY:M?c:i});
qx.ui.core.queue.Layout.add(this);
},_updateScrollBar:function(){var O=this.__nI;
var P=this.getBounds();

if(!P){return;
}
if(this.isEnabled()){var Q=O?P.width:P.height;
var N=this.getMaximum()+Q;
}else{N=0;
}if(qx.core.Variant.isSet(f,q)){var P=this.getBounds();
this.getContentElement().setStyles({left:O?d:g,top:O?g:d,width:(O?P.width:P.width+1)+j,height:(O?P.height+1:P.height)+j});
}this._getScrollPaneElement().setStyles({left:0,top:0,width:(O?N:1)+j,height:(O?1:N)+j});
this.scrollTo(this.getPosition());
},scrollTo:function(R){this.setPosition(Math.max(0,Math.min(this.getMaximum(),R)));
},scrollBy:function(S){this.scrollTo(this.getPosition()+S);
},scrollBySteps:function(T){var U=this.getSingleStep();
this.scrollBy(T*U);
},_onScroll:function(e){var W=this.getContentElement();
var V=this.__nI?W.getScrollX():W.getScrollY();
this.setPosition(V);
},_onAppear:function(e){this.scrollTo(this.getPosition());
},_stopPropagation:function(e){e.stopPropagation();
}},destruct:function(){this._disposeObjects(x);
}});
})();
(function(){var k="slider",j="horizontal",i="button-begin",h="vertical",g="button-end",f="Integer",d="execute",c="right",b="left",a="down",z="up",y="PositiveNumber",x="changeValue",w="qx.lang.Type.isNumber(value)&&value>=0&&value<=this.getMaximum()",v="_applyKnobFactor",u="knob",t="qx.ui.core.scroll.ScrollBar",s="resize",r="_applyOrientation",q="_applyPageStep",o="PositiveInteger",p="scroll",m="_applyPosition",n="scrollbar",l="_applyMaximum";
qx.Class.define(t,{extend:qx.ui.core.Widget,implement:qx.ui.core.scroll.IScrollBar,construct:function(A){qx.ui.core.Widget.call(this);
this._createChildControl(i);
this._createChildControl(k).addListener(s,this._onResizeSlider,this);
this._createChildControl(g);
if(A!=null){this.setOrientation(A);
}else{this.initOrientation();
}},properties:{appearance:{refine:true,init:n},orientation:{check:[j,h],init:j,apply:r},maximum:{check:o,apply:l,init:100},position:{check:w,init:0,apply:m,event:p},singleStep:{check:f,init:20},pageStep:{check:f,init:10,apply:q},knobFactor:{check:y,apply:v,nullable:true}},members:{__nK:2,_createChildControlImpl:function(B,C){var D;

switch(B){case k:D=new qx.ui.core.scroll.ScrollSlider();
D.setPageStep(100);
D.setFocusable(false);
D.addListener(x,this._onChangeSliderValue,this);
this._add(D,{flex:1});
break;
case i:D=new qx.ui.form.RepeatButton();
D.setFocusable(false);
D.addListener(d,this._onExecuteBegin,this);
this._add(D);
break;
case g:D=new qx.ui.form.RepeatButton();
D.setFocusable(false);
D.addListener(d,this._onExecuteEnd,this);
this._add(D);
break;
}return D||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,B);
},_applyMaximum:function(E){this.getChildControl(k).setMaximum(E);
},_applyPosition:function(F){this.getChildControl(k).setValue(F);
},_applyKnobFactor:function(G){this.getChildControl(k).setKnobFactor(G);
},_applyPageStep:function(H){this.getChildControl(k).setPageStep(H);
},_applyOrientation:function(I,J){var K=this._getLayout();

if(K){K.dispose();
}if(I===j){this._setLayout(new qx.ui.layout.HBox());
this.setAllowStretchX(true);
this.setAllowStretchY(false);
this.replaceState(h,j);
this.getChildControl(i).replaceState(z,b);
this.getChildControl(g).replaceState(a,c);
}else{this._setLayout(new qx.ui.layout.VBox());
this.setAllowStretchX(false);
this.setAllowStretchY(true);
this.replaceState(j,h);
this.getChildControl(i).replaceState(b,z);
this.getChildControl(g).replaceState(c,a);
}this.getChildControl(k).setOrientation(I);
},scrollTo:function(L){this.getChildControl(k).slideTo(L);
},scrollBy:function(M){this.getChildControl(k).slideBy(M);
},scrollBySteps:function(N){var O=this.getSingleStep();
this.getChildControl(k).slideBy(N*O);
},_onExecuteBegin:function(e){this.scrollBy(-this.getSingleStep());
},_onExecuteEnd:function(e){this.scrollBy(this.getSingleStep());
},_onChangeSliderValue:function(e){this.setPosition(e.getData());
},_onResizeSlider:function(e){var P=this.getChildControl(k).getChildControl(u);
var S=P.getSizeHint();
var Q=false;
var R=this.getChildControl(k).getInnerSize();

if(this.getOrientation()==h){if(R.height<S.minHeight+this.__nK){Q=true;
}}else{if(R.width<S.minWidth+this.__nK){Q=true;
}}
if(Q){P.exclude();
}else{P.show();
}}}});
})();
(function(){var a="qx.ui.form.IRange";
qx.Interface.define(a,{members:{setMinimum:function(b){return arguments.length==1;
},getMinimum:function(){},setMaximum:function(c){return arguments.length==1;
},getMaximum:function(){},setSingleStep:function(d){return arguments.length==1;
},getSingleStep:function(){},setPageStep:function(e){return arguments.length==1;
},getPageStep:function(){}}});
})();
(function(){var b="qx.ui.form.INumberForm",a="qx.event.type.Data";
qx.Interface.define(b,{events:{"changeValue":a},members:{setValue:function(c){return arguments.length==1;
},resetValue:function(){},getValue:function(){}}});
})();
(function(){var k="knob",j="horizontal",i="vertical",h="Integer",g="hovered",f="left",d="top",c="mouseup",b="pressed",a="px",V="changeValue",U="interval",T="mousemove",S="resize",R="slider",Q="mousedown",P="PageUp",O="mouseout",N='qx.event.type.Data',M="Left",r="Down",s="Up",p="dblclick",q="qx.ui.form.Slider",n="PageDown",o="mousewheel",l="_applyValue",m="_applyKnobFactor",t="End",u="height",B="Right",z="width",F="_applyOrientation",D="Home",I="mouseover",H="floor",w="_applyMinimum",L="click",K="typeof value==='number'&&value>=this.getMinimum()&&value<=this.getMaximum()",J="keypress",v="ceil",x="losecapture",y="contextmenu",A="_applyMaximum",C="Number",E="changeMaximum",G="changeMinimum";
qx.Class.define(q,{extend:qx.ui.core.Widget,implement:[qx.ui.form.IForm,qx.ui.form.INumberForm,qx.ui.form.IRange],include:[qx.ui.form.MForm],construct:function(W){qx.ui.core.Widget.call(this);
this._setLayout(new qx.ui.layout.Canvas());
this.addListener(J,this._onKeyPress);
this.addListener(o,this._onMouseWheel);
this.addListener(Q,this._onMouseDown);
this.addListener(c,this._onMouseUp);
this.addListener(x,this._onMouseUp);
this.addListener(S,this._onUpdate);
this.addListener(y,this._onStopEvent);
this.addListener(L,this._onStopEvent);
this.addListener(p,this._onStopEvent);
if(W!=null){this.setOrientation(W);
}else{this.initOrientation();
}},events:{changeValue:N},properties:{appearance:{refine:true,init:R},focusable:{refine:true,init:true},orientation:{check:[j,i],init:j,apply:F},value:{check:K,init:0,apply:l,nullable:true},minimum:{check:h,init:0,apply:w,event:G},maximum:{check:h,init:100,apply:A,event:E},singleStep:{check:h,init:1},pageStep:{check:h,init:10},knobFactor:{check:C,apply:m,nullable:true}},members:{__nL:null,__nM:null,__nN:null,__nO:null,__nP:null,__nQ:null,__nR:null,__nS:null,__nT:null,__nU:null,__nV:null,__nW:null,_forwardStates:{invalid:true},_createChildControlImpl:function(X,Y){var ba;

switch(X){case k:ba=new qx.ui.core.Widget();
ba.addListener(S,this._onUpdate,this);
ba.addListener(I,this._onMouseOver);
ba.addListener(O,this._onMouseOut);
this._add(ba);
break;
}return ba||qx.ui.core.Widget.prototype._createChildControlImpl.call(this,X);
},_onMouseOver:function(e){this.addState(g);
},_onMouseOut:function(e){this.removeState(g);
},_onMouseWheel:function(e){var bb=e.getWheelDelta()>0?1:-1;
this.slideBy(bb*this.getSingleStep());
e.stop();
},_onKeyPress:function(e){var bd=this.getOrientation()===j;
var bc=bd?M:s;
var forward=bd?B:r;

switch(e.getKeyIdentifier()){case forward:this.slideForward();
break;
case bc:this.slideBack();
break;
case n:this.slidePageForward();
break;
case P:this.slidePageBack();
break;
case D:this.slideToBegin();
break;
case t:this.slideToEnd();
break;
default:return;
}e.stop();
},_onMouseDown:function(e){if(this.__nO){return;
}var bg=this.__nY;
var be=this.getChildControl(k);
var bf=bg?f:d;
var bi=bg?e.getDocumentLeft():e.getDocumentTop();
var bj=this.__nL=qx.bom.element.Location.get(this.getContentElement().getDomElement())[bf];
var bh=this.__nM=qx.bom.element.Location.get(be.getContainerElement().getDomElement())[bf];

if(e.getTarget()===be){this.__nO=true;

if(!this.__nU){this.__nU=new qx.event.Timer(100);
this.__nU.addListener(U,this._fireValue,this);
}this.__nU.start();
this.__nP=bi+bj-bh;
be.addState(b);
}else{this.__nQ=true;
this.__nR=bi<=bh?-1:1;
this.__oa(e);
this._onInterval();
if(!this.__nT){this.__nT=new qx.event.Timer(100);
this.__nT.addListener(U,this._onInterval,this);
}this.__nT.start();
}this.addListener(T,this._onMouseMove);
this.capture();
e.stopPropagation();
},_onMouseUp:function(e){if(this.__nO){this.releaseCapture();
delete this.__nO;
this.__nU.stop();
this._fireValue();
delete this.__nP;
this.getChildControl(k).removeState(b);
if(e.getType()===c){var bl;
var bm;
var bk;

if(this.__nY){bl=e.getDocumentLeft()-(this._valueToPosition(this.getValue())+this.__nL);
bk=qx.bom.element.Location.get(this.getContentElement().getDomElement())[d];
bm=e.getDocumentTop()-(bk+this.getChildControl(k).getBounds().top);
}else{bl=e.getDocumentTop()-(this._valueToPosition(this.getValue())+this.__nL);
bk=qx.bom.element.Location.get(this.getContentElement().getDomElement())[f];
bm=e.getDocumentLeft()-(bk+this.getChildControl(k).getBounds().left);
}
if(bm<0||bm>this.__nN||bl<0||bl>this.__nN){this.getChildControl(k).removeState(g);
}}}else if(this.__nQ){this.__nT.stop();
this.releaseCapture();
delete this.__nQ;
delete this.__nR;
delete this.__nS;
}this.removeListener(T,this._onMouseMove);
if(e.getType()===c){e.stopPropagation();
}},_onMouseMove:function(e){if(this.__nO){var bo=this.__nY?e.getDocumentLeft():e.getDocumentTop();
var bn=bo-this.__nP;
this.slideTo(this._positionToValue(bn));
}else if(this.__nQ){this.__oa(e);
}e.stopPropagation();
},_onInterval:function(e){var bp=this.getValue()+(this.__nR*this.getPageStep());
if(bp<this.getMinimum()){bp=this.getMinimum();
}else if(bp>this.getMaximum()){bp=this.getMaximum();
}var bq=this.__nR==-1;

if((bq&&bp<=this.__nS)||(!bq&&bp>=this.__nS)){bp=this.__nS;
}this.slideTo(bp);
},_onUpdate:function(e){var bs=this.getInnerSize();
var bt=this.getChildControl(k).getBounds();
var br=this.__nY?z:u;
this._updateKnobSize();
this.__nX=bs[br]-bt[br];
this.__nN=bt[br];
this._updateKnobPosition();
},__nY:false,__nX:0,__oa:function(e){var bu=this.__nY;
var bB=bu?e.getDocumentLeft():e.getDocumentTop();
var bD=this.__nL;
var bv=this.__nM;
var bF=this.__nN;
var bC=bB-bD;

if(bB>=bv){bC-=bF;
}var bz=this._positionToValue(bC);
var bw=this.getMinimum();
var bx=this.getMaximum();

if(bz<bw){bz=bw;
}else if(bz>bx){bz=bx;
}else{var bA=this.getValue();
var by=this.getPageStep();
var bE=this.__nR<0?H:v;
bz=bA+(Math[bE]((bz-bA)/by)*by);
}if(this.__nS==null||(this.__nR==-1&&bz<=this.__nS)||(this.__nR==1&&bz>=this.__nS)){this.__nS=bz;
}},_positionToValue:function(bG){var bH=this.__nX;
if(bH==null||bH==0){return 0;
}var bJ=bG/bH;

if(bJ<0){bJ=0;
}else if(bJ>1){bJ=1;
}var bI=this.getMaximum()-this.getMinimum();
return this.getMinimum()+Math.round(bI*bJ);
},_valueToPosition:function(bK){var bL=this.__nX;

if(bL==null){return 0;
}var bM=this.getMaximum()-this.getMinimum();
if(bM==0){return 0;
}var bK=bK-this.getMinimum();
var bN=bK/bM;

if(bN<0){bN=0;
}else if(bN>1){bN=1;
}return Math.round(bL*bN);
},_updateKnobPosition:function(){this._setKnobPosition(this._valueToPosition(this.getValue()));
},_setKnobPosition:function(bO){var bP=this.getChildControl(k).getContainerElement();

if(this.__nY){bP.setStyle(f,bO+a,true);
}else{bP.setStyle(d,bO+a,true);
}},_updateKnobSize:function(){var bR=this.getKnobFactor();

if(bR==null){return;
}var bQ=this.getInnerSize();

if(bQ==null){return;
}if(this.__nY){this.getChildControl(k).setWidth(Math.round(bR*bQ.width));
}else{this.getChildControl(k).setHeight(Math.round(bR*bQ.height));
}},slideToBegin:function(){this.slideTo(this.getMinimum());
},slideToEnd:function(){this.slideTo(this.getMaximum());
},slideForward:function(){this.slideBy(this.getSingleStep());
},slideBack:function(){this.slideBy(-this.getSingleStep());
},slidePageForward:function(){this.slideBy(this.getPageStep());
},slidePageBack:function(){this.slideBy(-this.getPageStep());
},slideBy:function(bS){this.slideTo(this.getValue()+bS);
},slideTo:function(bT){if(bT<this.getMinimum()){bT=this.getMinimum();
}else if(bT>this.getMaximum()){bT=this.getMaximum();
}else{bT=this.getMinimum()+Math.round((bT-this.getMinimum())/this.getSingleStep())*this.getSingleStep();
}this.setValue(bT);
},_applyOrientation:function(bU,bV){var bW=this.getChildControl(k);
this.__nY=bU===j;
if(this.__nY){this.removeState(i);
bW.removeState(i);
this.addState(j);
bW.addState(j);
bW.setLayoutProperties({top:0,right:null,bottom:0});
}else{this.removeState(j);
bW.removeState(j);
this.addState(i);
bW.addState(i);
bW.setLayoutProperties({right:0,bottom:null,left:0});
}this._updateKnobPosition();
},_applyKnobFactor:function(bX,bY){if(bX!=null){this._updateKnobSize();
}else{if(this.__nY){this.getChildControl(k).resetWidth();
}else{this.getChildControl(k).resetHeight();
}}},_applyValue:function(ca,cb){if(ca!=null){this._updateKnobPosition();

if(this.__nO){this.__nW=[ca,cb];
}else{this.fireEvent(V,qx.event.type.Data,[ca,cb]);
}}else{this.resetValue();
}},_fireValue:function(){if(!this.__nW){return;
}var cc=this.__nW;
this.__nW=null;
this.fireEvent(V,qx.event.type.Data,cc);
},_applyMinimum:function(cd,ce){if(this.getValue()<cd){this.setValue(cd);
}this._updateKnobPosition();
},_applyMaximum:function(cf,cg){if(this.getValue()>cf){this.setValue(cf);
}this._updateKnobPosition();
}}});
})();
(function(){var d="horizontal",c="mousewheel",b="qx.ui.core.scroll.ScrollSlider",a="keypress";
qx.Class.define(b,{extend:qx.ui.form.Slider,construct:function(e){qx.ui.form.Slider.call(this,e);
this.removeListener(a,this._onKeyPress);
this.removeListener(c,this._onMouseWheel);
},members:{getSizeHint:function(f){var g=qx.ui.form.Slider.prototype.getSizeHint.call(this);
if(this.getOrientation()===d){g.width=0;
}else{g.height=0;
}return g;
}}});
})();
(function(){var a="qx.ui.table.pane.Clipper";
qx.Class.define(a,{extend:qx.ui.container.Composite,construct:function(){qx.ui.container.Composite.call(this,new qx.ui.layout.Grow());
this.setMinWidth(0);
},members:{scrollToX:function(b){this.getContentElement().scrollToX(b,false);
},scrollToY:function(c){this.getContentElement().scrollToY(c,true);
}}});
})();
(function(){var g="Integer",f="Escape",d="keypress",c="Enter",b="excluded",a="qx.ui.table.pane.FocusIndicator";
qx.Class.define(a,{extend:qx.ui.container.Composite,construct:function(h){qx.ui.container.Composite.call(this);
this.__rA=h;
this.setKeepActive(true);
this.addListener(d,this._onKeyPress,this);
},properties:{visibility:{refine:true,init:b},row:{check:g,nullable:true},column:{check:g,nullable:true}},members:{__rA:null,_onKeyPress:function(e){var i=e.getKeyIdentifier();

if(i!==f&&i!==c){e.stopPropagation();
}},moveToCell:function(j,k){if(!this.__rA.getShowCellFocusIndicator()&&!this.__rA.getTable().getTableModel().isColumnEditable(j)){this.exclude();
return;
}else{this.show();
}
if(j==null){this.hide();
this.setRow(null);
this.setColumn(null);
}else{var l=this.__rA.getTablePaneModel().getX(j);

if(l==-1){this.hide();
this.setRow(null);
this.setColumn(null);
}else{var q=this.__rA.getTable();
var o=q.getTableColumnModel();
var p=this.__rA.getTablePaneModel();
var n=this.__rA.getTablePane().getFirstVisibleRow();
var m=q.getRowHeight();
this.setUserBounds(p.getColumnLeft(j)-2,(k-n)*m-2,o.getColumnWidth(j)+3,m+3);
this.show();
this.setRow(k);
this.setColumn(j);
}}}},destruct:function(){this.__rA=null;
}});
})();
(function(){var b="Integer",a="qx.ui.table.pane.CellEvent";
qx.Class.define(a,{extend:qx.event.type.Mouse,properties:{row:{check:b,nullable:true},column:{check:b,nullable:true}},members:{init:function(c,d,e,f){d.clone(this);
this.setBubbles(false);

if(e!=null){this.setRow(e);
}else{this.setRow(c._getRowForPagePos(this.getDocumentLeft(),this.getDocumentTop()));
}
if(f!=null){this.setColumn(f);
}else{this.setColumn(c._getColumnForPageX(this.getDocumentLeft()));
}},clone:function(g){var h=qx.event.type.Mouse.prototype.clone.call(this,g);
h.set({row:this.getRow(),column:this.getColumn()});
return h;
}}});
})();
(function(){var a="qx.lang.Number";
qx.Class.define(a,{statics:{isInRange:function(b,c,d){return b>=c&&b<=d;
},isBetweenRange:function(e,f,g){return e>f&&e<g;
},limit:function(h,i,j){if(j!=null&&h>j){return j;
}else if(i!=null&&h<i){return i;
}else{return h;
}}}});
})();
(function(){var h="headerCellRendererChanged",g="visibilityChangedPre",f="Number",e="qx.event.type.Event",d="_applyFirstColumnX",c="Integer",b="qx.ui.table.pane.Model",a="_applyMaxColumnCount";
qx.Class.define(b,{extend:qx.core.Object,construct:function(i){qx.core.Object.call(this);
this.setTableColumnModel(i);
},events:{"modelChanged":e},statics:{EVENT_TYPE_MODEL_CHANGED:"modelChanged"},properties:{firstColumnX:{check:c,init:0,apply:d},maxColumnCount:{check:f,init:-1,apply:a}},members:{__sk:null,__sl:null,_applyFirstColumnX:function(j,k){this.__sk=null;
this.fireEvent(qx.ui.table.pane.Model.EVENT_TYPE_MODEL_CHANGED);
},_applyMaxColumnCount:function(l,m){this.__sk=null;
this.fireEvent(qx.ui.table.pane.Model.EVENT_TYPE_MODEL_CHANGED);
},setTableColumnModel:function(n){if(this.__sl){this.__sl.removeListener(g,this._onColVisibilityChanged,this);
this.__sl.removeListener(h,this._onColVisibilityChanged,this);
}this.__sl=n;
this.__sl.addListener(g,this._onColVisibilityChanged,this);
this.__sl.addListener(h,this._onHeaderCellRendererChanged,this);
this.__sk=null;
},_onColVisibilityChanged:function(o){this.__sk=null;
this.fireEvent(qx.ui.table.pane.Model.EVENT_TYPE_MODEL_CHANGED);
},_onHeaderCellRendererChanged:function(p){this.fireEvent(qx.ui.table.pane.Model.EVENT_TYPE_MODEL_CHANGED);
},getColumnCount:function(){if(this.__sk==null){var q=this.getFirstColumnX();
var s=this.getMaxColumnCount();
var r=this.__sl.getVisibleColumnCount();

if(s==-1||(q+s)>r){this.__sk=r-q;
}else{this.__sk=s;
}}return this.__sk;
},getColumnAtX:function(t){var u=this.getFirstColumnX();
return this.__sl.getVisibleColumnAtX(u+t);
},getX:function(v){var w=this.getFirstColumnX();
var y=this.getMaxColumnCount();
var x=this.__sl.getVisibleX(v)-w;

if(x>=0&&(y==-1||x<y)){return x;
}else{return -1;
}},getColumnLeft:function(z){var C=0;
var B=this.getColumnCount();

for(var x=0;x<B;x++){var A=this.getColumnAtX(x);

if(A==z){return C;
}C+=this.__sl.getColumnWidth(A);
}return -1;
},getTotalWidth:function(){var D=0;
var E=this.getColumnCount();

for(var x=0;x<E;x++){var F=this.getColumnAtX(x);
D+=this.__sl.getColumnWidth(F);
}return D;
}},destruct:function(){if(this.__sl){this.__sl.removeListener(g,this._onColVisibilityChanged,this);
this.__sl.removeListener(h,this._onColVisibilityChanged,this);
}this.__sl=null;
}});
})();
(function(){var e="dataChanged",d="metaDataChanged",c="qx.ui.table.model.Simple",b="Boolean",a="sorted";
qx.Class.define(c,{extend:qx.ui.table.model.Abstract,construct:function(){qx.ui.table.model.Abstract.call(this);
this.__oY=[];
this.__pa=-1;
this.__pb=[];
this.__pc=null;
},properties:{caseSensitiveSorting:{check:b,init:true}},statics:{_defaultSortComparatorAscending:function(f,g){var h=f[arguments.callee.columnIndex];
var k=g[arguments.callee.columnIndex];

if(qx.lang.Type.isNumber(h)&&qx.lang.Type.isNumber(k)){var l=isNaN(h)?isNaN(k)?0:1:isNaN(k)?-1:null;

if(l!=null){return l;
}}return (h>k)?1:((h==k)?0:-1);
},_defaultSortComparatorInsensitiveAscending:function(m,n){var o=(m[arguments.callee.columnIndex].toLowerCase?m[arguments.callee.columnIndex].toLowerCase():m[arguments.callee.columnIndex]);
var p=(n[arguments.callee.columnIndex].toLowerCase?n[arguments.callee.columnIndex].toLowerCase():n[arguments.callee.columnIndex]);

if(qx.lang.Type.isNumber(o)&&qx.lang.Type.isNumber(p)){var q=isNaN(o)?isNaN(p)?0:1:isNaN(p)?-1:null;

if(q!=null){return q;
}}return (o>p)?1:((o==p)?0:-1);
},_defaultSortComparatorDescending:function(r,s){var t=r[arguments.callee.columnIndex];
var u=s[arguments.callee.columnIndex];

if(qx.lang.Type.isNumber(t)&&qx.lang.Type.isNumber(u)){var v=isNaN(t)?isNaN(u)?0:1:isNaN(u)?-1:null;

if(v!=null){return v;
}}return (t<u)?1:((t==u)?0:-1);
},_defaultSortComparatorInsensitiveDescending:function(w,x){var y=(w[arguments.callee.columnIndex].toLowerCase?w[arguments.callee.columnIndex].toLowerCase():w[arguments.callee.columnIndex]);
var z=(x[arguments.callee.columnIndex].toLowerCase?x[arguments.callee.columnIndex].toLowerCase():x[arguments.callee.columnIndex]);

if(qx.lang.Type.isNumber(y)&&qx.lang.Type.isNumber(z)){var A=isNaN(y)?isNaN(z)?0:1:isNaN(z)?-1:null;

if(A!=null){return A;
}}return (y<z)?1:((y==z)?0:-1);
}},members:{__oY:null,__pc:null,__pd:null,__pb:null,__pa:null,__pe:null,getRowData:function(B){var C=this.__oY[B];

if(C==null||C.originalData==null){return C;
}else{return C.originalData;
}},getRowDataAsMap:function(D){var F=this.__oY[D];

if(F!=null){var E={};
for(var G=0;G<this.getColumnCount();G++){E[this.getColumnId(G)]=F[G];
}
if(F.originalData!=null){for(var H in F.originalData){if(E[H]==undefined){E[H]=F.originalData[H];
}}}return E;
}return (F&&F.originalData)?F.originalData:null;
},getDataAsMapArray:function(){var J=this.getRowCount();
var I=[];

for(var i=0;i<J;i++){I.push(this.getRowDataAsMap(i));
}return I;
},setEditable:function(K){this.__pc=[];

for(var L=0;L<this.getColumnCount();L++){this.__pc[L]=K;
}this.fireEvent(d);
},setColumnEditable:function(M,N){if(N!=this.isColumnEditable(M)){if(this.__pc==null){this.__pc=[];
}this.__pc[M]=N;
this.fireEvent(d);
}},isColumnEditable:function(O){return this.__pc?(this.__pc[O]==true):false;
},setColumnSortable:function(P,Q){if(Q!=this.isColumnSortable(P)){if(this.__pd==null){this.__pd=[];
}this.__pd[P]=Q;
this.fireEvent(d);
}},isColumnSortable:function(R){return (this.__pd?(this.__pd[R]!==false):true);
},sortByColumn:function(S,T){var W;
var V=this.__pb[S];

if(V){W=(T?V.ascending:V.descending);
}else{if(this.getCaseSensitiveSorting()){W=(T?qx.ui.table.model.Simple._defaultSortComparatorAscending:qx.ui.table.model.Simple._defaultSortComparatorDescending);
}else{W=(T?qx.ui.table.model.Simple._defaultSortComparatorInsensitiveAscending:qx.ui.table.model.Simple._defaultSortComparatorInsensitiveDescending);
}}W.columnIndex=S;
this.__oY.sort(W);
this.__pa=S;
this.__pe=T;
var U={columnIndex:S,ascending:T};
this.fireDataEvent(a,U);
this.fireEvent(d);
},setSortMethods:function(X,Y){var ba;

if(qx.lang.Type.isFunction(Y)){ba={ascending:Y,descending:function(bb,bc){return Y(bc,bb);
}};
}else{ba=Y;
}this.__pb[X]=ba;
},getSortMethods:function(bd){return this.__pb[bd];
},clearSorting:function(){if(this.__pa!=-1){this.__pa=-1;
this.__pe=true;
this.fireEvent(d);
}},getSortColumnIndex:function(){return this.__pa;
},_setSortColumnIndex:function(be){this.__pa=be;
},isSortAscending:function(){return this.__pe;
},_setSortAscending:function(bf){this.__pe=bf;
},getRowCount:function(){return this.__oY.length;
},getValue:function(bg,bh){if(bh<0||bh>=this.__oY.length){throw new Error("this.__rowArr out of bounds: "+bh+" (0.."+this.__oY.length+")");
}return this.__oY[bh][bg];
},setValue:function(bi,bj,bk){if(this.__oY[bj][bi]!=bk){this.__oY[bj][bi]=bk;
if(this.hasListener(e)){var bl={firstRow:bj,lastRow:bj,firstColumn:bi,lastColumn:bi};
this.fireDataEvent(e,bl);
}
if(bi==this.__pa){this.clearSorting();
}}},setData:function(bm,bn){this.__oY=bm;
if(this.hasListener(e)){var bo={firstRow:0,lastRow:bm.length-1,firstColumn:0,lastColumn:this.getColumnCount()-1};
this.fireDataEvent(e,bo);
}
if(bn!==false){this.clearSorting();
}},getData:function(){return this.__oY;
},setDataAsMapArray:function(bp,bq,br){this.setData(this._mapArray2RowArr(bp,bq),br);
},addRows:function(bs,bt,bu){if(bt==null){bt=this.__oY.length;
}bs.splice(0,0,bt,0);
Array.prototype.splice.apply(this.__oY,bs);
var bv={firstRow:bt,lastRow:this.__oY.length-1,firstColumn:0,lastColumn:this.getColumnCount()-1};
this.fireDataEvent(e,bv);

if(bu!==false){this.clearSorting();
}},addRowsAsMapArray:function(bw,bx,by,bz){this.addRows(this._mapArray2RowArr(bw,by),bx,bz);
},setRows:function(bA,bB,bC){if(bB==null){bB=0;
}bA.splice(0,0,bB,bA.length);
Array.prototype.splice.apply(this.__oY,bA);
var bD={firstRow:bB,lastRow:this.__oY.length-1,firstColumn:0,lastColumn:this.getColumnCount()-1};
this.fireDataEvent(e,bD);

if(bC!==false){this.clearSorting();
}},setRowsAsMapArray:function(bE,bF,bG,bH){this.setRows(this._mapArray2RowArr(bE,bG),bF,bH);
},removeRows:function(bI,bJ,bK){this.__oY.splice(bI,bJ);
var bL={firstRow:bI,lastRow:this.__oY.length-1,firstColumn:0,lastColumn:this.getColumnCount()-1,removeStart:bI,removeCount:bJ};
this.fireDataEvent(e,bL);

if(bK!==false){this.clearSorting();
}},_mapArray2RowArr:function(bM,bN){var bR=bM.length;
var bO=this.getColumnCount();
var bQ=new Array(bR);
var bP;

for(var i=0;i<bR;++i){bP=[];

if(bN){bP.originalData=bM[i];
}
for(var j=0;j<bO;++j){bP[j]=bM[i][this.getColumnId(j)];
}bQ[i]=bP;
}return bQ;
}},destruct:function(){this.__oY=this.__pc=this.__pb=this.__pd=null;
}});
})();
(function(){var s="",r="==",q=">",p="between",o="<",n="regex",m="!between",l=">=",k="!=",j="<=",c="font-weight",h=";",f="text-align",b='g',a=":",e="qx.ui.table.cellrenderer.Conditional",d="color",g="font-style";
qx.Class.define(e,{extend:qx.ui.table.cellrenderer.Default,construct:function(t,u,v,w){qx.ui.table.cellrenderer.Default.call(this);
this.numericAllowed=[r,k,q,o,l,j];
this.betweenAllowed=[p,m];
this.conditions=[];
this.__uB=t||s;
this.__uC=u||s;
this.__uD=v||s;
this.__uE=w||s;
},members:{__uB:null,__uC:null,__uD:null,__uE:null,__uF:function(x,y){if(x[1]!=null){y[f]=x[1];
}
if(x[2]!=null){y[d]=x[2];
}
if(x[3]!=null){y[g]=x[3];
}
if(x[4]!=null){y[c]=x[4];
}},addNumericCondition:function(z,A,B,C,D,E,F){var G=null;

if(qx.lang.Array.contains(this.numericAllowed,z)){if(A!=null){G=[z,B,C,D,E,A,F];
}}
if(G!=null){this.conditions.push(G);
}else{throw new Error("Condition not recognized or value is null!");
}},addBetweenCondition:function(H,I,J,K,L,M,N,O){if(qx.lang.Array.contains(this.betweenAllowed,H)){if(I!=null&&J!=null){var P=[H,K,L,M,N,I,J,O];
}}
if(P!=null){this.conditions.push(P);
}else{throw new Error("Condition not recognized or value1/value2 is null!");
}},addRegex:function(Q,R,S,T,U,V){if(Q!=null){var W=[n,R,S,T,U,Q,V];
}
if(W!=null){this.conditions.push(W);
}else{throw new Error("regex cannot be null!");
}},_getCellStyle:function(X){if(!this.conditions.length){return X.style||s;
}var bd=X.table.getTableModel();
var i;
var bf;
var Y;
var bb={"text-align":this.__uB,"color":this.__uC,"font-style":this.__uD,"font-weight":this.__uE};

for(i in this.conditions){bf=false;

if(qx.lang.Array.contains(this.numericAllowed,this.conditions[i][0])){if(this.conditions[i][6]==null){Y=X.value;
}else{Y=bd.getValueById(this.conditions[i][6],X.row);
}
switch(this.conditions[i][0]){case r:if(Y==this.conditions[i][5]){bf=true;
}break;
case k:if(Y!=this.conditions[i][5]){bf=true;
}break;
case q:if(Y>this.conditions[i][5]){bf=true;
}break;
case o:if(Y<this.conditions[i][5]){bf=true;
}break;
case l:if(Y>=this.conditions[i][5]){bf=true;
}break;
case j:if(Y<=this.conditions[i][5]){bf=true;
}break;
}}else if(qx.lang.Array.contains(this.betweenAllowed,this.conditions[i][0])){if(this.conditions[i][7]==null){Y=X.value;
}else{Y=bd.getValueById(this.conditions[i][7],X.row);
}
switch(this.conditions[i][0]){case p:if(Y>=this.conditions[i][5]&&Y<=this.conditions[i][6]){bf=true;
}break;
case m:if(Y<this.conditions[i][5]&&Y>this.conditions[i][6]){bf=true;
}break;
}}else if(this.conditions[i][0]==n){if(this.conditions[i][6]==null){Y=X.value;
}else{Y=bd.getValueById(this.conditions[i][6],X.row);
}var ba=new RegExp(this.conditions[i][5],b);
bf=ba.test(Y);
}if(bf==true){this.__uF(this.conditions[i],bb);
}}var be=[];

for(var bc in bb){if(bb[bc]){be.push(bc,a,bb[bc],h);
}}return be.join(s);
}},destruct:function(){this.numericAllowed=this.betweenAllowed=this.conditions=null;
}});
})();
(function(){var c="qx.ui.table.cellrenderer.String",b="qooxdoo-table-cell",a="";
qx.Class.define(c,{extend:qx.ui.table.cellrenderer.Conditional,members:{_getContentHtml:function(d){return qx.bom.String.escape(d.value||a);
},_getCellClass:function(e){return b;
}}});
})();
(function(){var b="",a="lino.ForeignKeyCellRenderer";
qx.Class.define(a,{extend:qx.ui.table.cellrenderer.String,construct:function(c){qx.ui.table.cellrenderer.String.call(this);
this.__uG=c;
},members:{__uG:null,_getContentHtml:function(d){if(d.rowData){return qx.bom.String.escape(d.rowData[this.__uG]);
}return b;
}}});
})();
(function(){var c="Tango",b="qx/icon/Tango",a="qx.theme.icon.Tango";
qx.Theme.define(a,{title:c,aliases:{"icon":b},icons:{}});
})();
(function(){var bz="white",by="#EEEEEE",bx="#E4E4E4",bw="#F3F3F3",bv="#F0F0F0",bu="#E8E8E8",bt="#CCCCCC",bs="#EFEFEF",br="#1a1a1a",bq="#00204D",bf="gray",be="#F4F4F4",bd="#fffefe",bc="#AFAFAF",bb="#084FAB",ba="#FCFCFC",Y="#CCC",X="#F2F2F2",W="black",V="#ffffdd",bG="#b6b6b6",bH="#004DAD",bE="#BABABA",bF="#005BC3",bC="#334866",bD="#CECECE",bA="#D9D9D9",bB="#D8D8D8",bI="#99C3FE",bJ="#001533",bj="#B3B3B3",bi="#D5D5D5",bl="#C3C3C3",bk="#DDDDDD",bn="#FF9999",bm="#E8E8E9",bp="#084FAA",bo="#C5C5C5",bh="#DBDBDB",bg="#4a4a4a",a="#83BAEA",b="#D7E7F4",c="#07125A",d="#FAF2F2",e="#87AFE7",f="#F7EAEA",g="#777D8D",h="#FBFBFB",i="#CACACA",j="#909090",bN="#9B9B9B",bM="#F0F9FE",bL="#314a6e",bK="#B4B4B4",bR="#787878",bQ="qx.theme.modern.Color",bP="#000000",bO="#26364D",bT="#A7A7A7",bS="#D1E4FF",F="#5CB0FD",G="#EAEAEA",D="#003B91",E="#80B4EF",J="#FF6B78",K="#949494",H="#808080",I="#930000",B="#7B7B7B",C="#C82C2C",r="#DFDFDF",q="#B6B6B6",t="#0880EF",s="#4d4d4d",n="#f4f4f4",m="#7B7A7E",p="#D0D0D0",o="#f8f8f8",l="#404955",k="#959595",P="#AAAAAA",Q="#F7E9E9",R="#314A6E",S="#C72B2B",L="#FAFAFA",M="#FBFCFB",N="#B2D2FF",O="#666666",T="#CBC8CD",U="#999999",A="#8EB8D6",z="#b8b8b8",y="#727272",x="#33508D",w="#F1F1F1",v="#990000",u="#00368A";
qx.Theme.define(bQ,{colors:{"background-application":r,"background-pane":bw,"background-light":ba,"background-medium":by,"background-splitpane":bc,"background-tip":V,"background-tip-error":S,"background-odd":bx,"htmlarea-background":bz,"progressbar-background":bz,"text-light":j,"text-gray":bg,"text-label":br,"text-title":bL,"text-input":bP,"text-hovered":bJ,"text-disabled":m,"text-selected":bd,"text-active":bO,"text-inactive":l,"text-placeholder":T,"border-inner-scrollbar":bz,"border-main":s,"menu-separator-top":bo,"menu-separator-bottom":L,"border-separator":H,"broder-toolbar-button-outer":bG,"broder-toolbar-broder-inner":o,"border-toolbar-separator-right":n,"border-toolbar-separator-left":z,"border-input":bC,"border-inner-input":bz,"border-disabled":q,"border-pane":bq,"border-button":O,"border-column":bt,"border-focused":bI,"invalid":v,"border-focused-invalid":bn,"border-dragover":x,"keyboard-focus":W,"table-pane":bw,"table-focus-indicator":t,"table-row-background-focused-selected":bb,"table-row-background-focused":E,"table-row-background-selected":bb,"table-row-background-even":bw,"table-row-background-odd":bx,"table-row-selected":bd,"table-row":br,"table-row-line":Y,"table-column-line":Y,"table-header-hovered":bz,"progressive-table-header":P,"progressive-table-header-border-right":X,"progressive-table-row-background-even":be,"progressive-table-row-background-odd":bx,"progressive-progressbar-background":bf,"progressive-progressbar-indicator-done":bt,"progressive-progressbar-indicator-undone":bz,"progressive-progressbar-percent-background":bf,"progressive-progressbar-percent-text":bz,"selected-start":bH,"selected-end":u,"tabview-background":c,"shadow":U,"pane-start":h,"pane-end":bv,"group-background":bu,"group-border":bK,"radiobutton-background":bs,"checkbox-border":R,"checkbox-focus":e,"checkbox-hovered":N,"checkbox-hovered-inner":bS,"checkbox-inner":by,"checkbox-start":bx,"checkbox-end":bw,"checkbox-disabled-border":bR,"checkbox-disabled-inner":i,"checkbox-disabled-start":p,"checkbox-disabled-end":bB,"checkbox-hovered-inner-invalid":d,"checkbox-hovered-invalid":Q,"radiobutton-checked":bF,"radiobutton-disabled":bi,"radiobutton-checked-disabled":B,"radiobutton-hovered-invalid":f,"tooltip-error":C,"scrollbar-start":bt,"scrollbar-end":w,"scrollbar-slider-start":by,"scrollbar-slider-end":bl,"button-border-disabeld":k,"button-start":bv,"button-end":bc,"button-disabled-start":be,"button-disabled-end":bE,"button-hovered-start":bM,"button-hovered-end":A,"button-focused":a,"border-invalid":I,"input-start":bv,"input-end":M,"input-focused-start":b,"input-focused-end":F,"input-focused-inner-invalid":J,"input-border-disabled":bN,"input-border-inner":bz,"toolbar-start":bs,"toolbar-end":bk,"window-border":bq,"window-border-caption":y,"window-caption-active-text":bz,"window-caption-active-start":bp,"window-caption-active-end":D,"window-caption-inactive-start":X,"window-caption-inactive-end":bh,"window-statusbar-background":bs,"tabview-start":ba,"tabview-end":by,"tabview-inactive":g,"tabview-inactive-start":G,"tabview-inactive-end":bD,"table-header-start":bu,"table-header-end":bj,"menu-start":bm,"menu-end":bA,"menubar-start":bu,"groupitem-start":bT,"groupitem-end":K,"groupitem-text":bz,"virtual-row-layer-background-even":bz,"virtual-row-layer-background-odd":bz}});
})();
(function(){var a="lino.theme.Color";
qx.Theme.define(a,{extend:qx.theme.modern.Color,colors:{}});
})();
(function(){var k="_applyBoxShadow",j="px ",i="Integer",h="shadowHorizontalLength",g="box-shadow",f="-webkit-box-shadow",e="shadowVerticalLength",d="-moz-box-shadow",c="shorthand",b="qx.ui.decoration.MBoxShadow",a="Color";
qx.Mixin.define(b,{properties:{shadowHorizontalLength:{nullable:true,check:i,apply:k},shadowVerticalLength:{nullable:true,check:i,apply:k},shadowBlurRadius:{nullable:true,check:i,apply:k},shadowColor:{nullable:true,check:a,apply:k},shadowLength:{group:[h,e],mode:c}},members:{_styleBoxShadow:function(l){var m=qx.theme.manager.Color.getInstance();
var p=m.resolve(this.getShadowColor());

if(p!=null){var q=this.getShadowVerticalLength()||0;
var n=this.getShadowHorizontalLength()||0;
var blur=this.getShadowBlurRadius()||0;
var o=n+j+q+j+blur+j+p;
l[d]=o;
l[f]=o;
l[g]=o;
}},_applyBoxShadow:function(){{};
}}});
})();
(function(){var d="qx.ui.decoration.MBackgroundColor",c="Color",b="_applyBackgroundColor",a="";
qx.Mixin.define(d,{properties:{backgroundColor:{check:c,nullable:true,apply:b}},members:{_tintBackgroundColor:function(e,f,g){var h=qx.theme.manager.Color.getInstance();

if(f==null){f=this.getBackgroundColor();
}g.backgroundColor=h.resolve(f)||a;
},_resizeBackgroundColor:function(i,j,k){var l=this.getInsets();
j-=l.left+l.right;
k-=l.top+l.bottom;
return {left:l.left,top:l.top,width:j,height:k};
},_applyBackgroundColor:function(){{};
}}});
})();
(function(){var r="_applyBackgroundImage",q="repeat",p="",o="mshtml",n="backgroundPositionX",m='<div style="',l="backgroundPositionY",k='</div>',j="no-repeat",i="scale",c='">',h=" ",f="repeat-x",b="qx.client",a="repeat-y",e="hidden",d="qx.ui.decoration.MBackgroundImage",g="String";
qx.Mixin.define(d,{properties:{backgroundImage:{check:g,nullable:true,apply:r},backgroundRepeat:{check:[q,f,a,j,i],init:q,apply:r},backgroundPositionX:{nullable:true,apply:r},backgroundPositionY:{nullable:true,apply:r},backgroundPosition:{group:[l,n]}},members:{_generateMarkup:this._generateBackgroundMarkup,_generateBackgroundMarkup:function(s,content){var w=p;
var v=this.getBackgroundImage();
var u=this.getBackgroundRepeat();
var top=this.getBackgroundPositionY();

if(top==null){top=0;
}var x=this.getBackgroundPositionX();

if(x==null){x=0;
}s.backgroundPosition=x+h+top;
if(v){var t=qx.util.AliasManager.getInstance().resolve(v);
w=qx.bom.element.Decoration.create(t,u,s);
}else{if(qx.core.Variant.isSet(b,o)){if(qx.bom.client.Engine.VERSION<7||qx.bom.client.Feature.QUIRKS_MODE){s.overflow=e;
}}
if(!content){content=p;
}w=m+qx.bom.element.Style.compile(s)+c+content+k;
}return w;
},_applyBackgroundImage:function(){{};
}}});
})();
(function(){var j="solid",i="_applyStyle",h="double",g="px ",f="dotted",e="_applyWidth",d="Color",c="",b="dashed",a="Number",D=" ",C="shorthand",B="widthTop",A="styleRight",z="styleBottom",y="widthBottom",x="widthLeft",w="styleTop",v="colorBottom",u="styleLeft",q="widthRight",r="colorLeft",o="colorRight",p="colorTop",m="border-top",n="border-left",k="border-right",l="qx.ui.decoration.MSingleBorder",s="border-bottom",t="absolute";
qx.Mixin.define(l,{properties:{widthTop:{check:a,init:0,apply:e},widthRight:{check:a,init:0,apply:e},widthBottom:{check:a,init:0,apply:e},widthLeft:{check:a,init:0,apply:e},styleTop:{nullable:true,check:[j,f,b,h],init:j,apply:i},styleRight:{nullable:true,check:[j,f,b,h],init:j,apply:i},styleBottom:{nullable:true,check:[j,f,b,h],init:j,apply:i},styleLeft:{nullable:true,check:[j,f,b,h],init:j,apply:i},colorTop:{nullable:true,check:d,apply:i},colorRight:{nullable:true,check:d,apply:i},colorBottom:{nullable:true,check:d,apply:i},colorLeft:{nullable:true,check:d,apply:i},left:{group:[x,u,r]},right:{group:[q,A,o]},top:{group:[B,w,p]},bottom:{group:[y,z,v]},width:{group:[B,q,y,x],mode:C},style:{group:[w,A,z,u],mode:C},color:{group:[p,o,v,r],mode:C}},members:{_styleBorder:function(E){var F=qx.theme.manager.Color.getInstance();
var G=this.getWidthTop();

if(G>0){E[m]=G+g+this.getStyleTop()+D+(F.resolve(this.getColorTop())||c);
}var G=this.getWidthRight();

if(G>0){E[k]=G+g+this.getStyleRight()+D+(F.resolve(this.getColorRight())||c);
}var G=this.getWidthBottom();

if(G>0){E[s]=G+g+this.getStyleBottom()+D+(F.resolve(this.getColorBottom())||c);
}var G=this.getWidthLeft();

if(G>0){E[n]=G+g+this.getStyleLeft()+D+(F.resolve(this.getColorLeft())||c);
}{};
E.position=t;
E.top=0;
E.left=0;
},_resizeBorder:function(H,I,J){var K=this.getInsets();
I-=K.left+K.right;
J-=K.top+K.bottom;
return {left:K.left-this.getWidthLeft(),top:K.top-this.getWidthTop(),width:I,height:J};
},_getDefaultInsetsForBorder:function(){return {top:this.getWidthTop(),right:this.getWidthRight(),bottom:this.getWidthBottom(),left:this.getWidthLeft()};
},_applyWidth:function(){this._applyStyle();
this._resetInsets();
},_applyStyle:function(){{};
}}});
})();
(function(){var b="px",a="qx.ui.decoration.Single";
qx.Class.define(a,{extend:qx.ui.decoration.Abstract,include:[qx.ui.decoration.MBackgroundImage,qx.ui.decoration.MBackgroundColor,qx.ui.decoration.MSingleBorder],construct:function(c,d,e){qx.ui.decoration.Abstract.call(this);
if(c!=null){this.setWidth(c);
}
if(d!=null){this.setStyle(d);
}
if(e!=null){this.setColor(e);
}},members:{_markup:null,getMarkup:function(f){if(this._markup){return this._markup;
}var g={};
this._styleBorder(g,f);
var h=this._generateBackgroundMarkup(g);
return this._markup=h;
},resize:function(i,j,k){var l=this.getInsets();
j-=l.left+l.right;
k-=l.top+l.bottom;
if(j<0){j=0;
}
if(k<0){k=0;
}i.style.width=j+b;
i.style.height=k+b;
var m=this._resizeBorder(i,j,k);
i.style.left=m.left+b;
i.style.top=m.top+b;
},tint:function(n,o){this._tintBackgroundColor(n,o,n.style);
},_isInitialized:function(){return !!this._markup;
},_getDefaultInsets:function(){return this._getDefaultInsetsForBorder();
}},destruct:function(){this._markup=null;
}});
})();
(function(){var a="qx.ui.decoration.Uniform";
qx.Class.define(a,{extend:qx.ui.decoration.Single,construct:function(b,c,d){qx.ui.decoration.Single.call(this);
if(b!=null){this.setWidth(b);
}
if(c!=null){this.setStyle(c);
}
if(d!=null){this.setColor(d);
}}});
})();
(function(){var j="px ",i=" ",h='',g="Color",f="Number",e="border-top",d="border-left",c="border-bottom",b="border-right",a="shorthand",y="line-height",x="innerWidthRight",w="innerColorBottom",v="innerWidthTop",u="innerColorRight",t="innerColorTop",s="relative",r="innerColorLeft",q="qx.ui.decoration.MDoubleBorder",p="left",n="top",o="innerWidthBottom",l="innerWidthLeft",m="position",k="absolute";
qx.Mixin.define(q,{include:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MBackgroundImage],construct:function(){this._getDefaultInsetsForBorder=this.__ud;
this._resizeBorder=this.__uc;
this._styleBorder=this.__ua;
this._generateMarkup=this.__ub;
},properties:{innerWidthTop:{check:f,init:0},innerWidthRight:{check:f,init:0},innerWidthBottom:{check:f,init:0},innerWidthLeft:{check:f,init:0},innerWidth:{group:[v,x,o,l],mode:a},innerColorTop:{nullable:true,check:g},innerColorRight:{nullable:true,check:g},innerColorBottom:{nullable:true,check:g},innerColorLeft:{nullable:true,check:g},innerColor:{group:[t,u,w,r],mode:a}},members:{__tY:null,__ua:function(z){var A=qx.theme.manager.Color.getInstance();
z.position=s;
var B=this.getInnerWidthTop();

if(B>0){z[e]=B+j+this.getStyleTop()+i+A.resolve(this.getInnerColorTop());
}var B=this.getInnerWidthRight();

if(B>0){z[b]=B+j+this.getStyleRight()+i+A.resolve(this.getInnerColorRight());
}var B=this.getInnerWidthBottom();

if(B>0){z[c]=B+j+this.getStyleBottom()+i+A.resolve(this.getInnerColorBottom());
}var B=this.getInnerWidthLeft();

if(B>0){z[d]=B+j+this.getStyleLeft()+i+A.resolve(this.getInnerColorLeft());
}{};
},__ub:function(C){var F=this._generateBackgroundMarkup(C);
var D=qx.theme.manager.Color.getInstance();
C[e]=h;
C[b]=h;
C[c]=h;
C[d]=h;
C[y]=0;
if((qx.bom.client.Engine.MSHTML&&qx.bom.client.Engine.VERSION<8)||(qx.bom.client.Engine.MSHTML&&qx.bom.client.Engine.DOCUMENT_MODE<8)){C[y]=h;
}var E=this.getWidthTop();

if(E>0){C[e]=E+j+this.getStyleTop()+i+D.resolve(this.getColorTop());
}var E=this.getWidthRight();

if(E>0){C[b]=E+j+this.getStyleRight()+i+D.resolve(this.getColorRight());
}var E=this.getWidthBottom();

if(E>0){C[c]=E+j+this.getStyleBottom()+i+D.resolve(this.getColorBottom());
}var E=this.getWidthLeft();

if(E>0){C[d]=E+j+this.getStyleLeft()+i+D.resolve(this.getColorLeft());
}{};
C[m]=k;
C[n]=0;
C[p]=0;
return this.__tY=this._generateBackgroundMarkup(C,F);
},__uc:function(G,H,I){var J=this.getInsets();
H-=J.left+J.right;
I-=J.top+J.bottom;
var K=J.left-this.getWidthLeft()-this.getInnerWidthLeft();
var top=J.top-this.getWidthTop()-this.getInnerWidthTop();
return {left:K,top:top,width:H,height:I,elementToApplyDimensions:G.firstChild};
},__ud:function(){return {top:this.getWidthTop()+this.getInnerWidthTop(),right:this.getWidthRight()+this.getInnerWidthRight(),bottom:this.getWidthBottom()+this.getInnerWidthBottom(),left:this.getWidthLeft()+this.getInnerWidthLeft()};
}}});
})();
(function(){var c="px",b="qx.ui.decoration.Background",a="absolute";
qx.Class.define(b,{extend:qx.ui.decoration.Abstract,include:[qx.ui.decoration.MBackgroundImage,qx.ui.decoration.MBackgroundColor],construct:function(d){qx.ui.decoration.Abstract.call(this);

if(d!=null){this.setBackgroundColor(d);
}},members:{__lj:null,_getDefaultInsets:function(){return {top:0,right:0,bottom:0,left:0};
},_isInitialized:function(){return !!this.__lj;
},getMarkup:function(e){if(this.__lj){return this.__lj;
}var f={position:a,top:0,left:0};
var g=this._generateBackgroundMarkup(f);
return this.__lj=g;
},resize:function(h,i,j){var k=this.getInsets();
h.style.width=(i-k.left-k.right)+c;
h.style.height=(j-k.top-k.bottom)+c;
h.style.left=-k.left+c;
h.style.top=-k.top+c;
},tint:function(l,m){this._tintBackgroundColor(l,m,l.style);
}},destruct:function(){this.__lj=null;
}});
})();
(function(){var j='"></div>',i="_applyStyle",h="1px",g='<div style="',f='border:',e="1px solid ",d="Color",c=";",b="px",a='</div>',v="qx.ui.decoration.Beveled",u='<div style="position:absolute;top:1px;left:1px;',t='border-bottom:',s='border-right:',r="",q='border-left:',p='border-top:',o="Number",n='<div style="position:absolute;top:1px;left:0px;',m='position:absolute;top:0px;left:1px;',k='<div style="overflow:hidden;font-size:0;line-height:0;">',l="absolute";
qx.Class.define(v,{extend:qx.ui.decoration.Abstract,include:[qx.ui.decoration.MBackgroundImage,qx.ui.decoration.MBackgroundColor],construct:function(w,x,y){qx.ui.decoration.Abstract.call(this);
if(w!=null){this.setOuterColor(w);
}
if(x!=null){this.setInnerColor(x);
}
if(y!=null){this.setInnerOpacity(y);
}},properties:{innerColor:{check:d,nullable:true,apply:i},innerOpacity:{check:o,init:1,apply:i},outerColor:{check:d,nullable:true,apply:i}},members:{__lk:null,_getDefaultInsets:function(){return {top:2,right:2,bottom:2,left:2};
},_isInitialized:function(){return !!this.__lk;
},_applyStyle:function(){{};
},getMarkup:function(){if(this.__lk){return this.__lk;
}var z=qx.theme.manager.Color.getInstance();
var A=[];
var D=e+z.resolve(this.getOuterColor())+c;
var C=e+z.resolve(this.getInnerColor())+c;
A.push(k);
A.push(g);
A.push(f,D);
A.push(qx.bom.element.Opacity.compile(0.35));
A.push(j);
A.push(n);
A.push(q,D);
A.push(s,D);
A.push(qx.bom.element.Opacity.compile(1));
A.push(j);
A.push(g);
A.push(m);
A.push(p,D);
A.push(t,D);
A.push(qx.bom.element.Opacity.compile(1));
A.push(j);
var B={position:l,top:h,left:h,opacity:1};
A.push(this._generateBackgroundMarkup(B));
A.push(u);
A.push(f,C);
A.push(qx.bom.element.Opacity.compile(this.getInnerOpacity()));
A.push(j);
A.push(a);
return this.__lk=A.join(r);
},resize:function(E,F,G){if(F<4){F=4;
}
if(G<4){G=4;
}if(qx.bom.client.Feature.CONTENT_BOX){var outerWidth=F-2;
var outerHeight=G-2;
var M=outerWidth;
var L=outerHeight;
var innerWidth=F-4;
var innerHeight=G-4;
}else{var outerWidth=F;
var outerHeight=G;
var M=F-2;
var L=G-2;
var innerWidth=M;
var innerHeight=L;
}var O=b;
var K=E.childNodes[0].style;
K.width=outerWidth+O;
K.height=outerHeight+O;
var J=E.childNodes[1].style;
J.width=outerWidth+O;
J.height=L+O;
var I=E.childNodes[2].style;
I.width=M+O;
I.height=outerHeight+O;
var H=E.childNodes[3].style;
H.width=M+O;
H.height=L+O;
var N=E.childNodes[4].style;
N.width=innerWidth+O;
N.height=innerHeight+O;
},tint:function(P,Q){this._tintBackgroundColor(P,Q,P.childNodes[3].style);
}},destruct:function(){this.__lk=null;
}});
})();
(function(){var j="_applyLinearBackgroundGradient",i=" ",h=")",g="horizontal",f=",",e=" 0",d="px",c="background",b="0",a="shorthand",z="Color",y="vertical",x="",w="Number",v="%",u="),to(",t="from(",s="linear-gradient(",r="-moz-",q="-webkit-gradient(linear,",o="startColorPosition",p="deg, ",m="startColor",n="qx.ui.decoration.MLinearBackgroundGradient",k="endColorPosition",l="endColor";
qx.Mixin.define(n,{properties:{startColor:{check:z,nullable:true,apply:j},endColor:{check:z,nullable:true,apply:j},orientation:{check:[g,y],init:y,apply:j},startColorPosition:{check:w,init:0,apply:j},endColorPosition:{check:w,init:100,apply:j},colorPositionUnit:{check:[d,v],init:v,apply:j},gradientStart:{group:[m,o],mode:a},gradientEnd:{group:[l,k],mode:a}},members:{_styleLinearBackgroundGradient:function(A){var D=qx.theme.manager.Color.getInstance();
var J=this.getColorPositionUnit();

if(qx.bom.client.Engine.WEBKIT){J=J===d?x:J;

if(this.getOrientation()==g){var I=this.getStartColorPosition()+J+e+J;
var H=this.getEndColorPosition()+J+e+J;
}else{var I=b+J+i+this.getStartColorPosition()+J;
var H=b+J+i+this.getEndColorPosition()+J;
}var F=t+D.resolve(this.getStartColor())+u+D.resolve(this.getEndColor())+h;
var E=q+I+f+H+f+F+h;
A[c]=E;
}else{var K=this.getOrientation()==g?0:270;
var C=D.resolve(this.getStartColor())+i+this.getStartColorPosition()+J;
var B=D.resolve(this.getEndColor())+i+this.getEndColorPosition()+J;
var G=qx.bom.client.Engine.GECKO?r:x;
A[c]=G+s+K+p+C+f+B+h;
}},_resizeLinearBackgroundGradient:function(L,M,N){var O=this.getInsets();
M-=O.left+O.right;
N-=O.top+O.bottom;
return {left:O.left,top:O.top,width:M,height:N};
},_applyLinearBackgroundGradient:function(){{};
}}});
})();
(function(){var m="Number",l="_applyInsets",k="-l",j="insetRight",i="insetTop",h="_applyBaseImage",g="insetBottom",f="set",e="shorthand",d="-t",a="insetLeft",c="String",b="qx.ui.decoration.Grid";
qx.Class.define(b,{extend:qx.core.Object,implement:[qx.ui.decoration.IDecorator],construct:function(n,o){qx.core.Object.call(this);

if(qx.ui.decoration.css3.BorderImage.IS_SUPPORTED){this.__lm=new qx.ui.decoration.css3.BorderImage();

if(n){this.__ln(n);
}}else{this.__lm=new qx.ui.decoration.GridDiv(n);
}
if(o!=null){this.__lm.setInsets(o);
}},properties:{baseImage:{check:c,nullable:true,apply:h},insetLeft:{check:m,nullable:true,apply:l},insetRight:{check:m,nullable:true,apply:l},insetBottom:{check:m,nullable:true,apply:l},insetTop:{check:m,nullable:true,apply:l},insets:{group:[i,j,g,a],mode:e}},members:{__lm:null,getMarkup:function(){return this.__lm.getMarkup();
},resize:function(p,q,r){this.__lm.resize(p,q,r);
},tint:function(s,t){},getInsets:function(){return this.__lm.getInsets();
},_applyInsets:function(u,v,name){var w=f+qx.lang.String.firstUp(name);
this.__lm[w](u);
},_applyBaseImage:function(x,y){if(this.__lm instanceof qx.ui.decoration.GridDiv){this.__lm.setBaseImage(x);
}else{this.__ln(x);
}},__ln:function(z){var B,D;
this.__lm.setBorderImage(z);
var F=qx.util.AliasManager.getInstance().resolve(z);
var G=/(.*)(\.[a-z]+)$/.exec(F);
var C=G[1];
var E=G[2];
var A=qx.util.ResourceManager.getInstance();
var H=A.getImageHeight(C+d+E);
var I=A.getImageWidth(C+k+E);
{};
this.__lm.setSlice([H,I]);
}},destruct:function(){this.__lm=null;
}});
})();
(function(){var u="px",t="_applyBorderRadius",s="Integer",r="border-bottom-right-radius",q="radiusTopRight",p="radiusTopLeft",o="-moz-border-radius-topleft",n="border-top-left-radius",m="-webkit-border-bottom-left-radius",l="-webkit-border-top-right-radius",e="-moz-border-radius-bottomright",k="border-top-right-radius",h="qx.ui.decoration.MBorderRadius",c="-moz-border-radius-topright",b="border-bottom-left-radius",g="radiusBottomLeft",f="-webkit-border-top-left-radius",i="shorthand",a="-moz-border-radius-bottomleft",j="radiusBottomRight",d="-webkit-border-bottom-right-radius";
qx.Mixin.define(h,{properties:{radiusTopLeft:{nullable:true,check:s,apply:t},radiusTopRight:{nullable:true,check:s,apply:t},radiusBottomLeft:{nullable:true,check:s,apply:t},radiusBottomRight:{nullable:true,check:s,apply:t},radius:{group:[p,q,j,g],mode:i}},members:{_styleBorderRadius:function(v){var w=this.getRadiusTopLeft();

if(w>0){v[o]=w+u;
v[f]=w+u;
v[n]=w+u;
}w=this.getRadiusTopRight();

if(w>0){v[c]=w+u;
v[l]=w+u;
v[k]=w+u;
}w=this.getRadiusBottomLeft();

if(w>0){v[a]=w+u;
v[m]=w+u;
v[b]=w+u;
}w=this.getRadiusBottomRight();

if(w>0){v[e]=w+u;
v[d]=w+u;
v[r]=w+u;
}},_applyBorderRadius:function(){{};
}}});
})();
(function(){var cH="solid",cG="invalid",cF="scale",cE="border-main",cD="border-invalid",cC="shadow",cB="border-separator",cA="checkbox-hovered",cz="button-start",cy="button-end",bI="background-light",bH="tabview-background",bG="repeat-x",bF="radiobutton",bE="button-css",bD="border-input",bC="border-inner-input",bB="border-inner-scrollbar",bA="radiobutton-checked",bz="tabview-inactive",cO="checkbox",cP="window-border",cM="radiobutton-disabled",cN="radiobutton-hovered-invalid",cK="tabview-page-button-top-active-css",cL="button-border-disabeld",cI="tabview-page-button-top-inactive-css",cJ="decoration/form/input.png",cQ="broder-toolbar-button-outer",cR="input-css",ch="border-disabled",cg="broder-toolbar-broder-inner",cj="background-pane",ci="border-focused-invalid",cl="checkbox-disabled-border",ck="button-hovered-end",cn="repeat-y",cm="border-dragover",cf="button-hovered-start",ce="progressive-table-header-border-right",k="decoration/scrollbar/scrollbar-button-bg-vertical.png",l="radiobutton-background",m="checkbox-focus",n="scrollbar-slider-horizontal-css",o="menu-end",p="decoration/selection.png",q="horizontal",r="table-header-start",s="decoration/scrollbar/scrollbar-button-bg-horizontal.png",t="decoration/form/input-focused.png",dg="checkbox-hovered-invalid",df="decoration/table/header-cell.png",de="tabview-inactive-start",dd="table-header-end",dk="border-button",dj="button-focused-css",di="checkbox-border",dh="tabview-start",dm="checkbox-start",dl="decoration/tabview/tab-button-top-active.png",Y="group-background",ba="decoration/form/button-c.png",W="keyboard-focus",X="button-disabled-start",bd="selected-end",be="table-header-hovered",bb="decoration/groupbox/groupbox.png",bc="decoration/pane/pane.png",U="decoration/menu/background.png",V="tooltip-error",H="decoration/toolbar/toolbar-part.gif",G="input-focused-css",J="decoration/menu/bar-background.png",I="window-border-caption",D="radiobutton-hovered",C="decoration/tabview/tab-button-bottom-active.png",F="radiobutton-checked-focused",E="groupitem-end",B="button-disabled-css",A="group-border",bj="scrollbar-slider-vertical-css",bk="decoration/form/button-checked.png",bl="selected-start",bm="tabview-end",bf="window-statusbar-background",bg="decoration/scrollbar/scrollbar-bg-vertical.png",bh="button-pressed-css",bi="toolbar-button-hovered-css",bn="window-caption-active-end",bo="dotted",R="checkbox-disabled-end",Q="window-caption-active-start",P="button-focused",O="menu-start",N="decoration/form/tooltip-error.png",M="window-captionbar-active-css",L="qx/decoration/Modern",K="border-toolbar-separator-left",T="decoration/scrollbar/scrollbar-bg-horizontal.png",S="decoration/tabview/tab-button-left-active.png",bp="decoration/tabview/tab-button-right-inactive.png",bq="decoration/tabview/tab-button-bottom-inactive.png",br="decoration/form/button-disabled.png",bs="decoration/form/button-pressed.png",bt="background-splitpane",bu="decoration/form/button-checked-focused.png",bv="px",bw="decoration/window/statusbar.png",bx="input-border-disabled",by="checkbox-inner",bM="scrollbar-horizontal-css",bL="button-disabled-end",bK="center",bJ="toolbar-end",bQ="groupitem-start",bP="decoration/form/button-hovered.png",bO="checkbox-hovered-inner",bN="input-focused-start",bS="scrollbar-start",bR="scrollbar-slider-start",ca="radiobutton-checked-disabled",cb="checkbox-focused",bX="qx.theme.modern.Decoration",bY="decoration/form/button.png",bV="decoration/app-header.png",bW="decoration/form/button-focused.png",bT="radiobutton-checked-hovered",bU="button-hovered-css",cc="checkbox-disabled-inner",cd="border-toolbar-separator-right",cr="border-focused",cq="decoration/shadow/shadow.png",ct="scrollbar-end",cs="decoration/group-item.png",cv="window-caption-inactive-end",cu="checkbox-end",cx="tabview-inactive-end",cw="input-end",cp="no-repeat",co="decoration/tabview/tab-button-left-inactive.png",cY="input-focused-inner-invalid",da="menu-separator-top",db="window-caption-inactive-start",dc="scrollbar-slider-end",cU="decoration/window/captionbar-inactive.png",cV="decoration/tabview/tab-button-top-inactive.png",cW="pane-end",cX="input-focused-end",cS="decoration/form/tooltip-error-arrow.png",cT="menubar-start",j="toolbar-start",i="checkbox-disabled-start",h="radiobutton-focused",g="pane-start",f="table-focus-indicator",e="button-checked-css",d="decoration/form/button-checked-c.png",c="menu-separator-bottom",b="decoration/shadow/shadow-small.png",a="input-start",w="decoration/tabview/tabview-pane.png",x="decoration/window/captionbar-active.png",u="decoration/tabview/tab-button-right-active.png",v="button-checked-focused-css",y="decoration/toolbar/toolbar-gradient.png",z="checkbox-hovered-inner-invalid";
qx.Theme.define(bX,{aliases:{decoration:L},decorations:{"main":{decorator:qx.ui.decoration.Uniform,style:{width:1,color:cE}},"selected":{decorator:qx.ui.decoration.Background,style:{backgroundImage:p,backgroundRepeat:cF}},"selected-css":{decorator:[qx.ui.decoration.MLinearBackgroundGradient],style:{startColorPosition:0,endColorPosition:100,startColor:bl,endColor:bd}},"selected-dragover":{decorator:qx.ui.decoration.Single,style:{backgroundImage:p,backgroundRepeat:cF,bottom:[2,cH,cm]}},"dragover":{decorator:qx.ui.decoration.Single,style:{bottom:[2,cH,cm]}},"pane":{decorator:qx.ui.decoration.Grid,style:{baseImage:bc,insets:[0,2,3,0]}},"pane-css":{decorator:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MBorderRadius,qx.ui.decoration.MBoxShadow,qx.ui.decoration.MLinearBackgroundGradient],style:{width:1,color:bH,radius:3,shadowColor:cC,shadowBlurRadius:2,shadowLength:0,gradientStart:[g,0],gradientEnd:[cW,100]}},"group":{decorator:qx.ui.decoration.Grid,style:{baseImage:bb}},"group-css":{decorator:[qx.ui.decoration.MBackgroundColor,qx.ui.decoration.MBorderRadius,qx.ui.decoration.MSingleBorder],style:{backgroundColor:Y,radius:4,color:A,width:1}},"border-invalid":{decorator:qx.ui.decoration.Beveled,style:{outerColor:cG,innerColor:bC,innerOpacity:0.5,backgroundImage:cJ,backgroundRepeat:bG,backgroundColor:bI}},"keyboard-focus":{decorator:qx.ui.decoration.Single,style:{width:1,color:W,style:bo}},"radiobutton":{decorator:[qx.ui.decoration.MDoubleBorder,qx.ui.decoration.MBackgroundColor,qx.ui.decoration.MBorderRadius,qx.ui.decoration.MBoxShadow],style:{backgroundColor:l,radius:5,width:1,innerWidth:2,color:di,innerColor:l,shadowLength:0,shadowBlurRadius:0,shadowColor:m,insetLeft:5}},"radiobutton-checked":{include:bF,style:{backgroundColor:bA}},"radiobutton-checked-focused":{include:bA,style:{shadowBlurRadius:4}},"radiobutton-checked-hovered":{include:bA,style:{innerColor:cA}},"radiobutton-focused":{include:bF,style:{shadowBlurRadius:4}},"radiobutton-hovered":{include:bF,style:{backgroundColor:cA,innerColor:cA}},"radiobutton-disabled":{include:bF,style:{innerColor:cM,backgroundColor:cM,color:cl}},"radiobutton-checked-disabled":{include:cM,style:{backgroundColor:ca}},"radiobutton-invalid":{include:bF,style:{color:cG}},"radiobutton-checked-invalid":{include:bA,style:{color:cG}},"radiobutton-checked-focused-invalid":{include:F,style:{color:cG,shadowColor:cG}},"radiobutton-checked-hovered-invalid":{include:bT,style:{color:cG,innerColor:cN}},"radiobutton-focused-invalid":{include:h,style:{color:cG,shadowColor:cG}},"radiobutton-hovered-invalid":{include:D,style:{color:cG,innerColor:cN,backgroundColor:cN}},"separator-horizontal":{decorator:qx.ui.decoration.Single,style:{widthLeft:1,colorLeft:cB}},"separator-vertical":{decorator:qx.ui.decoration.Single,style:{widthTop:1,colorTop:cB}},"tooltip-error":{decorator:qx.ui.decoration.Grid,style:{baseImage:N,insets:[2,5,5,2]}},"tooltip-error-css":{decorator:[qx.ui.decoration.MBackgroundColor,qx.ui.decoration.MBorderRadius,qx.ui.decoration.MBoxShadow],style:{backgroundColor:V,radius:4,shadowColor:cC,shadowBlurRadius:2,shadowLength:1}},"tooltip-error-arrow":{decorator:qx.ui.decoration.Background,style:{backgroundImage:cS,backgroundPositionY:bK,backgroundRepeat:cp,insets:[0,0,0,10]}},"shadow-window":{decorator:qx.ui.decoration.Grid,style:{baseImage:cq,insets:[4,8,8,4]}},"shadow-window-css":{decorator:[qx.ui.decoration.MBoxShadow,qx.ui.decoration.MBackgroundColor],style:{shadowColor:cC,shadowBlurRadius:2,shadowLength:1}},"shadow-popup":{decorator:qx.ui.decoration.Grid,style:{baseImage:b,insets:[0,3,3,0]}},"popup-css":{decorator:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MBoxShadow,qx.ui.decoration.MBackgroundColor],style:{width:1,color:cE,shadowColor:cC,shadowBlurRadius:3,shadowLength:1}},"scrollbar-horizontal":{decorator:qx.ui.decoration.Background,style:{backgroundImage:T,backgroundRepeat:bG}},"scrollbar-vertical":{decorator:qx.ui.decoration.Background,style:{backgroundImage:bg,backgroundRepeat:cn}},"scrollbar-slider-horizontal":{decorator:qx.ui.decoration.Beveled,style:{backgroundImage:s,backgroundRepeat:cF,outerColor:cE,innerColor:bB,innerOpacity:0.5}},"scrollbar-slider-horizontal-disabled":{decorator:qx.ui.decoration.Beveled,style:{backgroundImage:s,backgroundRepeat:cF,outerColor:ch,innerColor:bB,innerOpacity:0.3}},"scrollbar-slider-vertical":{decorator:qx.ui.decoration.Beveled,style:{backgroundImage:k,backgroundRepeat:cF,outerColor:cE,innerColor:bB,innerOpacity:0.5}},"scrollbar-slider-vertical-disabled":{decorator:qx.ui.decoration.Beveled,style:{backgroundImage:k,backgroundRepeat:cF,outerColor:ch,innerColor:bB,innerOpacity:0.3}},"scrollbar-horizontal-css":{decorator:[qx.ui.decoration.MLinearBackgroundGradient],style:{gradientStart:[bS,0],gradientEnd:[ct,100]}},"scrollbar-vertical-css":{include:bM,style:{orientation:q}},"scrollbar-slider-horizontal-css":{decorator:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MLinearBackgroundGradient],style:{gradientStart:[bR,0],gradientEnd:[dc,100],color:cE,width:1}},"scrollbar-slider-vertical-css":{include:n,style:{orientation:q}},"scrollbar-slider-horizontal-disabled-css":{include:n,style:{color:cL}},"scrollbar-slider-vertical-disabled-css":{include:bj,style:{color:cL}},"button-css":{decorator:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MLinearBackgroundGradient,qx.ui.decoration.MBorderRadius],style:{radius:3,color:dk,width:1,startColor:cz,endColor:cy,startColorPosition:35,endColorPosition:100}},"button-disabled-css":{include:bE,style:{color:cL,startColor:X,endColor:bL}},"button-hovered-css":{include:bE,style:{startColor:cf,endColor:ck}},"button-checked-css":{include:bE,style:{endColor:cz,startColor:cy}},"button-pressed-css":{include:bE,style:{endColor:cf,startColor:ck}},"button-focused-css":{decorator:[qx.ui.decoration.MDoubleBorder,qx.ui.decoration.MLinearBackgroundGradient,qx.ui.decoration.MBorderRadius],style:{radius:3,color:dk,width:1,innerColor:P,innerWidth:2,startColor:cz,endColor:cy,startColorPosition:30,endColorPosition:100}},"button-checked-focused-css":{include:dj,style:{endColor:cz,startColor:cy}},"button-invalid-css":{include:bE,style:{color:cD}},"button-disabled-invalid-css":{include:B,style:{color:cD}},"button-hovered-invalid-css":{include:bU,style:{color:cD}},"button-checked-invalid-css":{include:e,style:{color:cD}},"button-pressed-invalid-css":{include:bh,style:{color:cD}},"button-focused-invalid-css":{include:dj,style:{color:cD}},"button-checked-focused-invalid-css":{include:v,style:{color:cD}},"button":{decorator:qx.ui.decoration.Grid,style:{baseImage:bY,insets:2}},"button-disabled":{decorator:qx.ui.decoration.Grid,style:{baseImage:br,insets:2}},"button-focused":{decorator:qx.ui.decoration.Grid,style:{baseImage:bW,insets:2}},"button-hovered":{decorator:qx.ui.decoration.Grid,style:{baseImage:bP,insets:2}},"button-pressed":{decorator:qx.ui.decoration.Grid,style:{baseImage:bs,insets:2}},"button-checked":{decorator:qx.ui.decoration.Grid,style:{baseImage:bk,insets:2}},"button-checked-focused":{decorator:qx.ui.decoration.Grid,style:{baseImage:bu,insets:2}},"button-invalid-shadow":{decorator:qx.ui.decoration.Beveled,style:{outerColor:cG,innerColor:ci,insets:[1]}},"checkbox-invalid-shadow":{decorator:qx.ui.decoration.Beveled,style:{outerColor:cG,innerColor:ci,insets:[0]}},"checkbox":{decorator:[qx.ui.decoration.MDoubleBorder,qx.ui.decoration.MLinearBackgroundGradient,qx.ui.decoration.MBoxShadow],style:{width:1,color:di,innerWidth:1,innerColor:by,gradientStart:[dm,0],gradientEnd:[cu,100],shadowLength:0,shadowBlurRadius:0,shadowColor:m,insetLeft:4}},"checkbox-hovered":{include:cO,style:{innerColor:bO,gradientStart:[cA,0],gradientEnd:[cA,100]}},"checkbox-focused":{include:cO,style:{shadowBlurRadius:4}},"checkbox-disabled":{include:cO,style:{color:cl,innerColor:cc,gradientStart:[i,0],gradientEnd:[R,100]}},"checkbox-invalid":{include:cO,style:{color:cG}},"checkbox-hovered-invalid":{include:cA,style:{color:cG,innerColor:z,gradientStart:[dg,0],gradientEnd:[dg,100]}},"checkbox-focused-invalid":{include:cb,style:{color:cG,shadowColor:cG}},"input-css":{decorator:[qx.ui.decoration.MDoubleBorder,qx.ui.decoration.MLinearBackgroundGradient,qx.ui.decoration.MBackgroundColor],style:{color:bD,innerColor:bC,innerWidth:1,width:1,backgroundColor:bI,startColor:a,endColor:cw,startColorPosition:0,endColorPosition:12,colorPositionUnit:bv}},"border-invalid-css":{include:cR,style:{color:cD}},"input-focused-css":{include:cR,style:{startColor:bN,innerColor:cX,endColorPosition:4}},"input-focused-invalid-css":{include:G,style:{innerColor:cY,color:cD}},"input-disabled-css":{include:cR,style:{color:bx}},"input":{decorator:qx.ui.decoration.Beveled,style:{outerColor:bD,innerColor:bC,innerOpacity:0.5,backgroundImage:cJ,backgroundRepeat:bG,backgroundColor:bI}},"input-focused":{decorator:qx.ui.decoration.Beveled,style:{outerColor:bD,innerColor:cr,backgroundImage:t,backgroundRepeat:bG,backgroundColor:bI}},"input-focused-invalid":{decorator:qx.ui.decoration.Beveled,style:{outerColor:cG,innerColor:ci,backgroundImage:t,backgroundRepeat:bG,backgroundColor:bI,insets:[2]}},"input-disabled":{decorator:qx.ui.decoration.Beveled,style:{outerColor:ch,innerColor:bC,innerOpacity:0.5,backgroundImage:cJ,backgroundRepeat:bG,backgroundColor:bI}},"toolbar":{decorator:qx.ui.decoration.Background,style:{backgroundImage:y,backgroundRepeat:cF}},"toolbar-css":{decorator:[qx.ui.decoration.MLinearBackgroundGradient],style:{startColorPosition:40,endColorPosition:60,startColor:j,endColor:bJ}},"toolbar-button-hovered":{decorator:qx.ui.decoration.Beveled,style:{outerColor:cQ,innerColor:cg,backgroundImage:ba,backgroundRepeat:cF}},"toolbar-button-checked":{decorator:qx.ui.decoration.Beveled,style:{outerColor:cQ,innerColor:cg,backgroundImage:d,backgroundRepeat:cF}},"toolbar-button-hovered-css":{decorator:[qx.ui.decoration.MDoubleBorder,qx.ui.decoration.MLinearBackgroundGradient,qx.ui.decoration.MBorderRadius],style:{color:cQ,width:1,innerWidth:1,innerColor:cg,radius:2,gradientStart:[cz,30],gradientEnd:[cy,100]}},"toolbar-button-checked-css":{include:bi,style:{gradientStart:[cy,30],gradientEnd:[cz,100]}},"toolbar-separator":{decorator:qx.ui.decoration.Single,style:{widthLeft:1,widthRight:1,colorLeft:K,colorRight:cd,styleLeft:cH,styleRight:cH}},"toolbar-part":{decorator:qx.ui.decoration.Background,style:{backgroundImage:H,backgroundRepeat:cn}},"tabview-pane":{decorator:qx.ui.decoration.Grid,style:{baseImage:w,insets:[4,6,7,4]}},"tabview-pane-css":{decorator:[qx.ui.decoration.MBorderRadius,qx.ui.decoration.MLinearBackgroundGradient,qx.ui.decoration.MSingleBorder],style:{width:1,color:cP,radius:3,gradientStart:[dh,90],gradientEnd:[bm,100]}},"tabview-page-button-top-active":{decorator:qx.ui.decoration.Grid,style:{baseImage:dl}},"tabview-page-button-top-inactive":{decorator:qx.ui.decoration.Grid,style:{baseImage:cV}},"tabview-page-button-bottom-active":{decorator:qx.ui.decoration.Grid,style:{baseImage:C}},"tabview-page-button-bottom-inactive":{decorator:qx.ui.decoration.Grid,style:{baseImage:bq}},"tabview-page-button-left-active":{decorator:qx.ui.decoration.Grid,style:{baseImage:S}},"tabview-page-button-left-inactive":{decorator:qx.ui.decoration.Grid,style:{baseImage:co}},"tabview-page-button-right-active":{decorator:qx.ui.decoration.Grid,style:{baseImage:u}},"tabview-page-button-right-inactive":{decorator:qx.ui.decoration.Grid,style:{baseImage:bp}},"tabview-page-button-top-active-css":{decorator:[qx.ui.decoration.MBorderRadius,qx.ui.decoration.MSingleBorder,qx.ui.decoration.MBackgroundColor,qx.ui.decoration.MBoxShadow],style:{radius:[3,3,0,0],width:[1,1,0,1],color:bH,backgroundColor:dh,shadowLength:1,shadowColor:cC,shadowBlurRadius:2}},"tabview-page-button-top-inactive-css":{decorator:[qx.ui.decoration.MBorderRadius,qx.ui.decoration.MSingleBorder,qx.ui.decoration.MLinearBackgroundGradient],style:{radius:[3,3,0,0],color:bz,colorBottom:bH,width:1,gradientStart:[de,0],gradientEnd:[cx,100]}},"tabview-page-button-bottom-active-css":{include:cK,style:{radius:[0,0,3,3],width:[0,1,1,1],backgroundColor:de}},"tabview-page-button-bottom-inactive-css":{include:cI,style:{radius:[0,0,3,3],width:[0,1,1,1],colorBottom:bz,colorTop:bH}},"tabview-page-button-left-active-css":{include:cK,style:{radius:[3,0,0,3],width:[1,0,1,1],shadowLength:0,shadowBlurRadius:0}},"tabview-page-button-left-inactive-css":{include:cI,style:{radius:[3,0,0,3],width:[1,0,1,1],colorBottom:bz,colorRight:bH}},"tabview-page-button-right-active-css":{include:cK,style:{radius:[0,3,3,0],width:[1,1,1,0],shadowLength:0,shadowBlurRadius:0}},"tabview-page-button-right-inactive-css":{include:cI,style:{radius:[0,3,3,0],width:[1,1,1,0],colorBottom:bz,colorLeft:bH}},"splitpane":{decorator:qx.ui.decoration.Uniform,style:{backgroundColor:cj,width:3,color:bt,style:cH}},"window":{decorator:qx.ui.decoration.Single,style:{backgroundColor:cj,width:1,color:cE,widthTop:0}},"window-captionbar-active":{decorator:qx.ui.decoration.Grid,style:{baseImage:x}},"window-captionbar-inactive":{decorator:qx.ui.decoration.Grid,style:{baseImage:cU}},"window-statusbar":{decorator:qx.ui.decoration.Grid,style:{baseImage:bw}},"window-captionbar-active-css":{decorator:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MBorderRadius,qx.ui.decoration.MLinearBackgroundGradient,qx.ui.decoration.MBoxShadow],style:{width:1,color:cP,colorBottom:I,radius:[5,5,0,0],gradientStart:[Q,30],gradientEnd:[bn,70],shadowBlurRadius:4,shadowLength:2,shadowColor:cC}},"window-captionbar-inactive-css":{include:M,style:{gradientStart:[db,30],gradientEnd:[cv,70]}},"window-statusbar-css":{decorator:[qx.ui.decoration.MBackgroundColor,qx.ui.decoration.MSingleBorder,qx.ui.decoration.MBorderRadius,qx.ui.decoration.MBoxShadow],style:{backgroundColor:bf,width:[0,1,1,1],color:cP,radius:[0,0,5,5],shadowBlurRadius:4,shadowLength:2,shadowColor:cC}},"window-css":{decorator:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MBoxShadow,qx.ui.decoration.MBackgroundColor],style:{backgroundColor:cj,width:1,color:cP,widthTop:0,shadowBlurRadius:4,shadowLength:2,shadowColor:cC}},"table":{decorator:qx.ui.decoration.Single,style:{width:1,color:cE,style:cH}},"table-statusbar":{decorator:qx.ui.decoration.Single,style:{widthTop:1,colorTop:cE,style:cH}},"table-scroller-header":{decorator:qx.ui.decoration.Single,style:{backgroundImage:df,backgroundRepeat:cF,widthBottom:1,colorBottom:cE,style:cH}},"table-scroller-header-css":{decorator:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MLinearBackgroundGradient],style:{gradientStart:[r,10],gradientEnd:[dd,90],widthBottom:1,colorBottom:cE}},"table-header-cell":{decorator:qx.ui.decoration.Single,style:{widthRight:1,colorRight:cB,styleRight:cH}},"table-header-cell-hovered":{decorator:qx.ui.decoration.Single,style:{widthRight:1,colorRight:cB,styleRight:cH,widthBottom:1,colorBottom:be,styleBottom:cH}},"table-scroller-focus-indicator":{decorator:qx.ui.decoration.Single,style:{width:2,color:f,style:cH}},"progressive-table-header":{decorator:qx.ui.decoration.Single,style:{width:1,color:cE,style:cH}},"progressive-table-header-cell":{decorator:qx.ui.decoration.Single,style:{backgroundImage:df,backgroundRepeat:cF,widthRight:1,colorRight:ce,style:cH}},"progressive-table-header-cell-css":{decorator:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MLinearBackgroundGradient],style:{gradientStart:[r,10],gradientEnd:[dd,90],widthRight:1,colorRight:ce}},"menu":{decorator:qx.ui.decoration.Single,style:{backgroundImage:U,backgroundRepeat:cF,width:1,color:cE,style:cH}},"menu-css":{decorator:[qx.ui.decoration.MLinearBackgroundGradient,qx.ui.decoration.MBoxShadow,qx.ui.decoration.MSingleBorder],style:{gradientStart:[O,0],gradientEnd:[o,100],shadowColor:cC,shadowBlurRadius:2,shadowLength:1,width:1,color:cE}},"menu-separator":{decorator:qx.ui.decoration.Single,style:{widthTop:1,colorTop:da,widthBottom:1,colorBottom:c}},"menubar":{decorator:qx.ui.decoration.Single,style:{backgroundImage:J,backgroundRepeat:cF,width:1,color:cB,style:cH}},"menubar-css":{decorator:[qx.ui.decoration.MSingleBorder,qx.ui.decoration.MLinearBackgroundGradient],style:{gradientStart:[cT,0],gradientEnd:[o,100],width:1,color:cB}},"app-header":{decorator:qx.ui.decoration.Background,style:{backgroundImage:bV,backgroundRepeat:cF}},"progressbar":{decorator:qx.ui.decoration.Single,style:{width:1,color:bD}},"group-item":{decorator:qx.ui.decoration.Background,style:{backgroundImage:cs,backgroundRepeat:cF}},"group-item-css":{decorator:[qx.ui.decoration.MLinearBackgroundGradient],style:{startColorPosition:0,endColorPosition:100,startColor:bQ,endColor:E}}}});
})();
(function(){var a="lino.theme.Decoration";
qx.Theme.define(a,{extend:qx.theme.modern.Decoration,decorations:{}});
})();
(function(){var ek="widget",ej="atom",ei="button-frame",eh="-css",eg="middle",ef="main",ee="image",ed="text-selected",ec="button",eb="bold",cw="selected",cv="label",cu="background-light",ct="text-disabled",cs="groupbox",cr="decoration/arrows/down.png",cq="popup",cp="cell",co="border-invalid",cn="input-disabled",er="menu-button",es="input",ep="input-focused-invalid",eq="toolbar-button",en="spinner",eo="input-focused",el="list",em="tooltip",et="qx/static/blank.gif",eu="radiobutton",dC="tree-item",dB="combobox",dE="treevirtual-contract",dD="scrollbar",dG="datechooser/nav-button",dF="center",dI="virtual-tree-item",dH="checkbox",dz="treevirtual-expand",dy="",p="textfield",q="-invalid",r="decoration/arrows/right.png",s="background-application",t="decoration/tree/closed.png",u="invalid",v="right-top",w="decoration/tree/open.png",x="selectbox",y="text-title",eI="icon/22/places/folder-open.png",eH="icon/16/places/folder-open.png",eG="radiobutton-hovered",eF="scrollbar/button",eM="right",eL="combobox/button",eK="icon/16/places/folder.png",eJ="radiobutton-checked-focused",eO="text-label",eN="table-scroller-header",bt="scrollbar-slider-horizontal",bu="checkbox-hovered",br="checkbox-checked",bs="virtual-list",bx="decoration/arrows/left.png",by="decoration/tree/open-selected.png",bv="radiobutton-checked",bw="button-focused",bp="text-light",bq="menu-slidebar-button",U="checkbox-undetermined",T="table-scroller-header-css",W="text-input",V="slidebar/button-forward",Q="background-splitpane",P="icon/22/mimetypes/office-document.png",S="decoration/tree/closed-selected.png",R="text-hovered",O=".png",N="default",bE="decoration/arrows/down-small.png",bF="datechooser",bG="slidebar/button-backward",bH="radiobutton-checked-disabled",bA="checkbox-focused",bB="radiobutton-checked-hovered",bC="treevirtual-folder",bD="shadow-popup",bI="icon/16/mimetypes/office-document.png",bJ="background-medium",bi="icon/32/places/folder-open.png",bh="icon/22/places/folder.png",bg="table",bf="decoration/arrows/up.png",be="decoration/form/",bd="radiobutton-focused",bc="button-checked",bb="decoration/window/maximize-active-hovered.png",bm="keyboard-focus",bl="group-item",bK="menu-css",bL="decoration/cursors/",bM="icon/16/apps/office-calendar.png",bN="slidebar",bO="tooltip-error-arrow",bP="table-scroller-focus-indicator",bQ="popup-css",bR="move-frame",bS="nodrop",bT="decoration/table/boolean-true.png",cE="-invalid-css",cD="menu",cC="app-header",cB="row-layer",cI="text-inactive",cH="move",cG="selected-css",cF="decoration/window/restore-active-hovered.png",cM="border-separator",cL="shadow-window",dl="right.png",dm="checkbox-undetermined-hovered",dj="tabview-page-button-bottom-inactive",dk="tooltip-error",dh="window-css",di="window-statusbar",df="button-hovered",dg="decoration/scrollbar/scrollbar-",du="background-tip",dv="menubar-css",dN="scrollbar-slider-horizontal-disabled",dM="radiobutton-disabled",dP="button-pressed",dO="table-pane",dR="decoration/window/close-active.png",dQ="native",dT="button-invalid-shadow",dS="decoration/window/minimize-active-hovered.png",dK="menubar",dJ="icon/16/actions/dialog-cancel.png",eB="tabview-page-button-top-inactive",eC="tabview-page-button-left-inactive",eD="menu-slidebar",eE="toolbar-button-checked",ex="decoration/window/minimize-inactive.png",ey="group-item-css",ez="group",eA="tabview-page-button-right-inactive",ev="decoration/window/minimize-active.png",ew="decoration/window/restore-inactive.png",k="checkbox-checked-focused",j="splitpane",i="combobox/textfield",h="decoration/window/close-active-hovered.png",g="qx/icon/Tango/16/actions/window-close.png",f="checkbox-pressed",e="button-disabled",d="selected-dragover",c="tooltip-error-css",b="decoration/window/maximize-inactive.png",D="dragover",E="scrollarea",B="scrollbar-vertical",C="decoration/menu/checkbox-invert.gif",H="decoration/toolbar/toolbar-handle-knob.gif",I="table-header-cell",F="button-checked-focused",G="up.png",K="best-fit",L="pane-css",cQ="qx.theme.modern.Appearance",cK="text-active",cX="checkbox-disabled",cT="toolbar-button-hovered",cz="decoration/form/checked.png",cx="progressive-table-header",Y="decoration/table/select-column-order.png",cA="decoration/menu/radiobutton.gif",bk="decoration/arrows/forward.png",bj="decoration/table/descending.png",ce="decoration/form/undetermined.png",cf="window-captionbar-active",cg="checkbox-checked-hovered",ch="scrollbar-slider-vertical",ci="toolbar",cj="alias",ck="decoration/window/restore-active.png",cl="decoration/table/boolean-false.png",cb="icon/32/mimetypes/office-document.png",cc="tabview-pane",cy="decoration/arrows/rewind.png",cW="top",cV="icon/16/actions/dialog-ok.png",cU="progressbar-background",dc="table-header-cell-hovered",db="window-statusbar-css",da="window",cY="text-gray",cS="decoration/menu/radiobutton-invert.gif",cR="text-placeholder",J="slider",bo="toolbar-css",bn="keep-align",cJ="down.png",bz="groupitem-text",cP="tabview-page-button-top-active",cO="decoration/window/maximize-active.png",cN="checkbox-checked-pressed",X="decoration/window/close-inactive.png",de="tabview-page-button-left-active",M="toolbar-part",ba="decoration/splitpane/knob-vertical.png",bU=".gif",bV="virtual-row-layer-background-odd",bW="table-statusbar",bX="progressive-table-header-cell-css",bY="window-captionbar-inactive",ca="copy",dx="decoration/arrows/down-invert.png",cd="decoration/menu/checkbox.gif",dV="window-caption-active-text",dU="decoration/splitpane/knob-horizontal.png",dX="group-css",dW="icon/32/places/folder.png",ea="virtual-row-layer-background-even",dY="toolbar-separator",cm="tabview-page-button-bottom-active",dL="decoration/arrows/up-small.png",dd="decoration/table/ascending.png",dA="decoration/arrows/up-invert.png",z="small",A="tabview-page-button-right-active",ds="-disabled",dt="scrollbar-horizontal",dq="progressbar",dr="checkbox-undetermined-focused",dn="progressive-table-header-cell",dp="menu-separator",a="tabview-pane-css",dw="pane",o="htmlarea-background",n="decoration/arrows/right-invert.png",m="left.png",l="icon/16/actions/view-refresh.png";
qx.Theme.define(cQ,{appearances:{"widget":{},"root":{style:function(eP){return {backgroundColor:s,textColor:eO,font:N};
}},"label":{style:function(eQ){return {textColor:eQ.disabled?ct:undefined};
}},"move-frame":{style:function(eR){return {decorator:ef};
}},"resize-frame":bR,"dragdrop-cursor":{style:function(eS){var eT=bS;

if(eS.copy){eT=ca;
}else if(eS.move){eT=cH;
}else if(eS.alias){eT=cj;
}return {source:bL+eT+bU,position:v,offset:[2,16,2,6]};
}},"image":{style:function(eU){return {opacity:!eU.replacement&&eU.disabled?0.3:1};
}},"atom":{},"atom/label":cv,"atom/icon":ee,"popup":{style:function(eV){var eW=qx.bom.client.Feature.CSS_BOX_SHADOW;
return {decorator:eW?bQ:ef,backgroundColor:cu,shadow:eW?undefined:bD};
}},"button-frame":{alias:ej,style:function(eX){var fc,fb;
var eY=[3,9];

if(eX.checked&&eX.focused&&!eX.inner){fc=F;
fb=undefined;
eY=[1,7];
}else if(eX.disabled){fc=e;
fb=undefined;
}else if(eX.pressed){fc=dP;
fb=R;
}else if(eX.checked){fc=bc;
fb=undefined;
}else if(eX.hovered){fc=df;
fb=R;
}else if(eX.focused&&!eX.inner){fc=bw;
fb=undefined;
eY=[1,7];
}else{fc=ec;
fb=undefined;
}var fa;
if(qx.bom.client.Feature.CSS_BORDER_RADIUS&&qx.bom.client.Feature.CSS_GRADIENTS){if(eX.invalid&&!eX.disabled){fc+=cE;
}else{fc+=eh;
}}else{fa=eX.invalid&&!eX.disabled?dT:undefined;
eY=[2,8];
}return {decorator:fc,textColor:fb,shadow:fa,padding:eY};
}},"button-frame/image":{style:function(fd){return {opacity:!fd.replacement&&fd.disabled?0.5:1};
}},"button":{alias:ei,include:ei,style:function(fe){return {center:true};
}},"hover-button":{alias:ej,include:ej,style:function(ff){var fg=ff.hovered?cw:undefined;

if(fg&&qx.bom.client.Feature.CSS_GRADIENTS){fg+=eh;
}return {decorator:fg,textColor:ff.hovered?ed:undefined};
}},"splitbutton":{},"splitbutton/button":ec,"splitbutton/arrow":{alias:ec,include:ec,style:function(fh,fi){return {icon:cr,padding:[fi.padding[0],fi.padding[1]-6],marginLeft:1};
}},"checkbox":{alias:ej,style:function(fj){var fk=qx.bom.client.Feature.CSS_GRADIENTS&&qx.bom.client.Feature.CSS_BOX_SHADOW;
var fm;

if(fk){if(fj.checked){fm=cz;
}else if(fj.undetermined){fm=ce;
}else{fm=et;
}}else{if(fj.checked){if(fj.disabled){fm=br;
}else if(fj.focused){fm=k;
}else if(fj.pressed){fm=cN;
}else if(fj.hovered){fm=cg;
}else{fm=br;
}}else if(fj.undetermined){if(fj.disabled){fm=U;
}else if(fj.focused){fm=dr;
}else if(fj.hovered){fm=dm;
}else{fm=U;
}}else if(!fj.disabled){if(fj.focused){fm=bA;
}else if(fj.pressed){fm=f;
}else if(fj.hovered){fm=bu;
}}fm=fm||dH;
var fl=fj.invalid&&!fj.disabled?q:dy;
fm=be+fm+fl+O;
}return {icon:fm,gap:fk?8:6};
}},"checkbox/icon":{style:function(fn){var fp=qx.bom.client.Feature.CSS_GRADIENTS&&qx.bom.client.Feature.CSS_BOX_SHADOW;

if(!fp){return {opacity:!fn.replacement&&fn.disabled?0.3:1};
}var fq;

if(fn.disabled){fq=cX;
}else if(fn.focused){fq=bA;
}else if(fn.hovered){fq=bu;
}else{fq=dH;
}fq+=fn.invalid&&!fn.disabled?q:dy;
var fo;
if(fn.undetermined){fo=[2,0];
}return {decorator:fq,padding:fo,width:12,height:10};
}},"radiobutton":{alias:ej,style:function(fr){var fs=qx.bom.client.Feature.CSS_BORDER_RADIUS&&qx.bom.client.Feature.CSS_BOX_SHADOW;
var fu;

if(fs){fu=et;
}else{if(fr.checked&&fr.focused){fu=eJ;
}else if(fr.checked&&fr.disabled){fu=bH;
}else if(fr.checked&&fr.hovered){fu=bB;
}else if(fr.checked){fu=bv;
}else if(fr.focused){fu=bd;
}else if(fr.hovered){fu=eG;
}else{fu=eu;
}var ft=fr.invalid&&!fr.disabled?q:dy;
fu=be+fu+ft+O;
}return {icon:fu,gap:fs?8:6};
}},"radiobutton/icon":{style:function(fv){var fw=qx.bom.client.Feature.CSS_BORDER_RADIUS&&qx.bom.client.Feature.CSS_BOX_SHADOW;

if(!fw){return {opacity:!fv.replacement&&fv.disabled?0.3:1};
}var fx;

if(fv.disabled&&!fv.checked){fx=dM;
}else if(fv.checked&&fv.focused){fx=eJ;
}else if(fv.checked&&fv.disabled){fx=bH;
}else if(fv.checked&&fv.hovered){fx=bB;
}else if(fv.checked){fx=bv;
}else if(fv.focused){fx=bd;
}else if(fv.hovered){fx=eG;
}else{fx=eu;
}fx+=fv.invalid&&!fv.disabled?q:dy;
return {decorator:fx,width:12,height:10};
}},"textfield":{style:function(fy){var fD;
var fB=!!fy.focused;
var fC=!!fy.invalid;
var fz=!!fy.disabled;

if(fB&&fC&&!fz){fD=ep;
}else if(fB&&!fC&&!fz){fD=eo;
}else if(fz){fD=cn;
}else if(!fB&&fC&&!fz){fD=co;
}else{fD=es;
}
if(qx.bom.client.Feature.CSS_GRADIENTS){fD+=eh;
}var fA;

if(fy.disabled){fA=ct;
}else if(fy.showingPlaceholder){fA=cR;
}else{fA=W;
}return {decorator:fD,padding:[2,4,1],textColor:fA};
}},"textarea":{include:p,style:function(fE){return {padding:4};
}},"spinner":{style:function(fF){var fJ;
var fH=!!fF.focused;
var fI=!!fF.invalid;
var fG=!!fF.disabled;

if(fH&&fI&&!fG){fJ=ep;
}else if(fH&&!fI&&!fG){fJ=eo;
}else if(fG){fJ=cn;
}else if(!fH&&fI&&!fG){fJ=co;
}else{fJ=es;
}
if(qx.bom.client.Feature.CSS_GRADIENTS){fJ+=eh;
}return {decorator:fJ};
}},"spinner/textfield":{style:function(fK){return {marginRight:2,padding:[2,4,1],textColor:fK.disabled?ct:W};
}},"spinner/upbutton":{alias:ei,include:ei,style:function(fL,fM){return {icon:dL,padding:[fM.padding[0]-1,fM.padding[1]-5],shadow:undefined};
}},"spinner/downbutton":{alias:ei,include:ei,style:function(fN,fO){return {icon:bE,padding:[fO.padding[0]-1,fO.padding[1]-5],shadow:undefined};
}},"datefield":dB,"datefield/button":{alias:eL,include:eL,style:function(fP){return {icon:bM,padding:[0,3],decorator:undefined};
}},"datefield/textfield":i,"datefield/list":{alias:bF,include:bF,style:function(fQ){return {decorator:undefined};
}},"groupbox":{style:function(fR){return {legendPosition:cW};
}},"groupbox/legend":{alias:ej,style:function(fS){return {padding:[1,0,1,4],textColor:fS.invalid?u:y,font:eb};
}},"groupbox/frame":{style:function(fT){var fU=qx.bom.client.Feature.CSS_BORDER_RADIUS;
return {padding:fU?10:12,margin:fU?1:undefined,decorator:fU?dX:ez};
}},"check-groupbox":cs,"check-groupbox/legend":{alias:dH,include:dH,style:function(fV){return {padding:[1,0,1,4],textColor:fV.invalid?u:y,font:eb};
}},"radio-groupbox":cs,"radio-groupbox/legend":{alias:eu,include:eu,style:function(fW){return {padding:[1,0,1,4],textColor:fW.invalid?u:y,font:eb};
}},"scrollarea":{style:function(fX){return {minWidth:50,minHeight:50};
}},"scrollarea/corner":{style:function(fY){return {backgroundColor:s};
}},"scrollarea/pane":ek,"scrollarea/scrollbar-x":dD,"scrollarea/scrollbar-y":dD,"scrollbar":{style:function(ga){if(ga[dQ]){return {};
}var gb=qx.bom.client.Feature.CSS_GRADIENTS;
var gc=ga.horizontal?dt:B;

if(gb){gc+=eh;
}return {width:ga.horizontal?undefined:16,height:ga.horizontal?16:undefined,decorator:gc,padding:1};
}},"scrollbar/slider":{alias:J,style:function(gd){return {padding:gd.horizontal?[0,1,0,1]:[1,0,1,0]};
}},"scrollbar/slider/knob":{include:ei,style:function(ge){var gf=qx.bom.client.Feature.CSS_GRADIENTS;
var gg=ge.horizontal?bt:ch;

if(ge.disabled){gg+=ds;
}
if(gf){gg+=eh;
}return {decorator:gg,minHeight:ge.horizontal?undefined:9,minWidth:ge.horizontal?9:undefined,padding:undefined};
}},"scrollbar/button":{alias:ei,include:ei,style:function(gh){var gi=dg;

if(gh.left){gi+=m;
}else if(gh.right){gi+=dl;
}else if(gh.up){gi+=G;
}else{gi+=cJ;
}
if(gh.left||gh.right){return {padding:[0,0,0,gh.left?3:4],icon:gi,width:15,height:14};
}else{return {padding:3,icon:gi,width:14,height:15};
}}},"scrollbar/button-begin":eF,"scrollbar/button-end":eF,"slider":{style:function(gj){var gn;
var gl=!!gj.focused;
var gm=!!gj.invalid;
var gk=!!gj.disabled;

if(gl&&gm&&!gk){gn=ep;
}else if(gl&&!gm&&!gk){gn=eo;
}else if(gk){gn=cn;
}else if(!gl&&gm&&!gk){gn=co;
}else{gn=es;
}
if(qx.bom.client.Feature.CSS_GRADIENTS){gn+=eh;
}return {decorator:gn};
}},"slider/knob":{include:ei,style:function(go){return {decorator:go.disabled?dN:bt,shadow:undefined,height:14,width:14,padding:0};
}},"list":{alias:E,style:function(gp){var gt;
var gr=!!gp.focused;
var gs=!!gp.invalid;
var gq=!!gp.disabled;

if(gr&&gs&&!gq){gt=ep;
}else if(gr&&!gs&&!gq){gt=eo;
}else if(gq){gt=cn;
}else if(!gr&&gs&&!gq){gt=co;
}else{gt=es;
}
if(qx.bom.client.Feature.CSS_GRADIENTS){gt+=eh;
}return {backgroundColor:cu,decorator:gt};
}},"list/pane":ek,"listitem":{alias:ej,style:function(gu){var gv;

if(gu.dragover){gv=gu.selected?d:D;
}else{gv=gu.selected?cw:undefined;

if(gv&&qx.bom.client.Feature.CSS_GRADIENTS){gv+=eh;
}}return {padding:gu.dragover?[4,4,2,4]:4,textColor:gu.selected?ed:undefined,decorator:gv};
}},"slidebar":{},"slidebar/scrollpane":{},"slidebar/content":{},"slidebar/button-forward":{alias:ei,include:ei,style:function(gw){return {padding:5,center:true,icon:gw.vertical?cr:r};
}},"slidebar/button-backward":{alias:ei,include:ei,style:function(gx){return {padding:5,center:true,icon:gx.vertical?bf:bx};
}},"tabview":{style:function(gy){return {contentPadding:16};
}},"tabview/bar":{alias:bN,style:function(gz){var gA={marginBottom:gz.barTop?-1:0,marginTop:gz.barBottom?-4:0,marginLeft:gz.barRight?-3:0,marginRight:gz.barLeft?-1:0,paddingTop:0,paddingRight:0,paddingBottom:0,paddingLeft:0};

if(gz.barTop||gz.barBottom){gA.paddingLeft=5;
gA.paddingRight=7;
}else{gA.paddingTop=5;
gA.paddingBottom=7;
}return gA;
}},"tabview/bar/button-forward":{include:V,alias:V,style:function(gB){if(gB.barTop||gB.barBottom){return {marginTop:2,marginBottom:2};
}else{return {marginLeft:2,marginRight:2};
}}},"tabview/bar/button-backward":{include:bG,alias:bG,style:function(gC){if(gC.barTop||gC.barBottom){return {marginTop:2,marginBottom:2};
}else{return {marginLeft:2,marginRight:2};
}}},"tabview/bar/scrollpane":{},"tabview/pane":{style:function(gD){var gE=qx.bom.client.Feature.CSS_GRADIENTS&&qx.bom.client.Feature.CSS_BORDER_RADIUS;
return {decorator:gE?a:cc,minHeight:100,marginBottom:gD.barBottom?-1:0,marginTop:gD.barTop?-1:0,marginLeft:gD.barLeft?-1:0,marginRight:gD.barRight?-1:0};
}},"tabview-page":{alias:ek,include:ek,style:function(gF){var gG=qx.bom.client.Feature.CSS_GRADIENTS&&qx.bom.client.Feature.CSS_BORDER_RADIUS;
return {padding:gG?[4,3]:undefined};
}},"tabview-page/button":{alias:ej,style:function(gH){var gO,gK=0;
var gN=0,gI=0,gL=0,gM=0;
var gJ=qx.bom.client.Feature.CSS_BORDER_RADIUS&&qx.bom.client.Feature.CSS_BOX_SHADOW&&qx.bom.client.Feature.CSS_GRADIENTS;

if(gH.checked){if(gH.barTop){gO=cP;
gK=gJ?[5,11]:[6,14];
gL=gH.firstTab?0:-5;
gM=gH.lastTab?0:-5;
}else if(gH.barBottom){gO=cm;
gK=gJ?[5,11]:[6,14];
gL=gH.firstTab?0:-5;
gM=gH.lastTab?0:-5;
gN=3;
}else if(gH.barRight){gO=A;
gK=gJ?[5,10]:[6,13];
gN=gH.firstTab?0:-5;
gI=gH.lastTab?0:-5;
gL=2;
}else{gO=de;
gK=gJ?[5,10]:[6,13];
gN=gH.firstTab?0:-5;
gI=gH.lastTab?0:-5;
}}else{if(gH.barTop){gO=eB;
gK=gJ?[3,9]:[4,10];
gN=4;
gL=gH.firstTab?5:1;
gM=1;
}else if(gH.barBottom){gO=dj;
gK=gJ?[3,9]:[4,10];
gI=4;
gL=gH.firstTab?5:1;
gM=1;
gN=3;
}else if(gH.barRight){gO=eA;
gK=gJ?[3,9]:[4,10];
gM=5;
gN=gH.firstTab?5:1;
gI=1;
gL=3;
}else{gO=eC;
gK=gJ?[3,9]:[4,10];
gL=5;
gN=gH.firstTab?5:1;
gI=1;
gM=1;
}}
if(gO&&gJ){gO+=eh;
}return {zIndex:gH.checked?10:5,decorator:gO,padding:gK,marginTop:gN,marginBottom:gI,marginLeft:gL,marginRight:gM,textColor:gH.checked?cK:cI};
}},"tabview-page/button/label":{alias:cv,style:function(gP){return {padding:[0,1,0,1],margin:gP.focused?0:1,decorator:gP.focused?bm:undefined};
}},"tabview-page/button/close-button":{alias:ej,style:function(gQ){return {icon:g};
}},"toolbar":{style:function(gR){var gS=qx.bom.client.Feature.CSS_GRADIENTS;
return {decorator:gS?bo:ci,spacing:2};
}},"toolbar/part":{style:function(gT){return {decorator:M,spacing:2};
}},"toolbar/part/container":{style:function(gU){return {paddingLeft:2,paddingRight:2};
}},"toolbar/part/handle":{style:function(gV){return {source:H,marginLeft:3,marginRight:3};
}},"toolbar-button":{alias:ej,style:function(gW){var gY;

if(gW.pressed||(gW.checked&&!gW.hovered)||(gW.checked&&gW.disabled)){gY=eE;
}else if(gW.hovered&&!gW.disabled){gY=cT;
}var gX=qx.bom.client.Feature.CSS_GRADIENTS&&qx.bom.client.Feature.CSS_BORDER_RADIUS;

if(gX&&gY){gY+=eh;
}return {marginTop:2,marginBottom:2,padding:(gW.pressed||gW.checked||gW.hovered)&&!gW.disabled||(gW.disabled&&gW.checked)?3:5,decorator:gY};
}},"toolbar-menubutton":{alias:eq,include:eq,style:function(ha){return {showArrow:true};
}},"toolbar-menubutton/arrow":{alias:ee,include:ee,style:function(hb){return {source:bE};
}},"toolbar-splitbutton":{style:function(hc){return {marginTop:2,marginBottom:2};
}},"toolbar-splitbutton/button":{alias:eq,include:eq,style:function(hd){return {icon:cr,marginTop:undefined,marginBottom:undefined};
}},"toolbar-splitbutton/arrow":{alias:eq,include:eq,style:function(he){if(he.pressed||he.checked||(he.hovered&&!he.disabled)){var hf=1;
}else{var hf=3;
}return {padding:hf,icon:cr,marginTop:undefined,marginBottom:undefined};
}},"toolbar-separator":{style:function(hg){return {decorator:dY,margin:7};
}},"tree":el,"tree-item":{style:function(hh){var hi=hh.selected?cw:undefined;

if(hi&&qx.bom.client.Feature.CSS_GRADIENTS){hi+=eh;
}return {padding:[2,6],textColor:hh.selected?ed:undefined,decorator:hi};
}},"tree-item/icon":{include:ee,style:function(hj){return {paddingRight:5};
}},"tree-item/label":cv,"tree-item/open":{include:ee,style:function(hk){var hl;

if(hk.selected&&hk.opened){hl=by;
}else if(hk.selected&&!hk.opened){hl=S;
}else if(hk.opened){hl=w;
}else{hl=t;
}return {padding:[0,5,0,2],source:hl};
}},"tree-folder":{include:dC,alias:dC,style:function(hm){var ho,hn;

if(hm.small){ho=hm.opened?eH:eK;
hn=eH;
}else if(hm.large){ho=hm.opened?bi:dW;
hn=bi;
}else{ho=hm.opened?eI:bh;
hn=eI;
}return {icon:ho,iconOpened:hn};
}},"tree-file":{include:dC,alias:dC,style:function(hp){return {icon:hp.small?bI:hp.large?cb:P};
}},"treevirtual":bg,"treevirtual-folder":{style:function(hq){return {icon:hq.opened?eH:eK};
}},"treevirtual-file":{include:bC,alias:bC,style:function(hr){return {icon:bI};
}},"treevirtual-line":{style:function(hs){return {icon:et};
}},"treevirtual-contract":{style:function(ht){return {icon:w,paddingLeft:5,paddingTop:2};
}},"treevirtual-expand":{style:function(hu){return {icon:t,paddingLeft:5,paddingTop:2};
}},"treevirtual-only-contract":dE,"treevirtual-only-expand":dz,"treevirtual-start-contract":dE,"treevirtual-start-expand":dz,"treevirtual-end-contract":dE,"treevirtual-end-expand":dz,"treevirtual-cross-contract":dE,"treevirtual-cross-expand":dz,"treevirtual-end":{style:function(hv){return {icon:et};
}},"treevirtual-cross":{style:function(hw){return {icon:et};
}},"tooltip":{include:cq,style:function(hx){return {backgroundColor:du,padding:[1,3,2,3],offset:[15,5,5,5]};
}},"tooltip/atom":ej,"tooltip-error":{include:em,style:function(hy){var hz=qx.bom.client.Feature.CSS_BORDER_RADIUS&&qx.bom.client.Feature.CSS_BOX_SHADOW;
return {textColor:ed,backgroundColor:undefined,placeMethod:ek,offset:[0,0,0,14],marginTop:-2,position:v,showTimeout:100,hideTimeout:10000,decorator:hz?c:dk,shadow:bO,font:eb,padding:hz?3:undefined};
}},"tooltip-error/atom":ej,"window":{style:function(hA){var hB=qx.bom.client.Feature.CSS_BORDER_RADIUS&&qx.bom.client.Feature.CSS_GRADIENTS&&qx.bom.client.Feature.CSS_BOX_SHADOW;
return {decorator:hB?undefined:cL,contentPadding:[10,10,10,10]};
}},"window/pane":{style:function(hC){var hD=qx.bom.client.Feature.CSS_BORDER_RADIUS&&qx.bom.client.Feature.CSS_GRADIENTS&&qx.bom.client.Feature.CSS_BOX_SHADOW;
return {decorator:hD?dh:da,margin:hD?[0,5,hC.showStatusbar?0:5,0]:
undefined};
}},"window/captionbar":{style:function(hE){var hF=qx.bom.client.Feature.CSS_BORDER_RADIUS&&qx.bom.client.Feature.CSS_GRADIENTS&&qx.bom.client.Feature.CSS_BOX_SHADOW;
var hG=hE.active?cf:bY;

if(hF){hG+=eh;
}return {decorator:hG,textColor:hE.active?dV:cY,minHeight:26,paddingRight:2,margin:hF?[0,5,0,0]:
undefined};
}},"window/icon":{style:function(hH){return {margin:[5,0,3,6]};
}},"window/title":{style:function(hI){return {alignY:eg,font:eb,marginLeft:6,marginRight:12};
}},"window/minimize-button":{alias:ej,style:function(hJ){return {icon:hJ.active?hJ.hovered?dS:ev:ex,margin:[4,8,2,0]};
}},"window/restore-button":{alias:ej,style:function(hK){return {icon:hK.active?hK.hovered?cF:ck:ew,margin:[5,8,2,0]};
}},"window/maximize-button":{alias:ej,style:function(hL){return {icon:hL.active?hL.hovered?bb:cO:b,margin:[4,8,2,0]};
}},"window/close-button":{alias:ej,style:function(hM){return {icon:hM.active?hM.hovered?h:dR:X,margin:[4,8,2,0]};
}},"window/statusbar":{style:function(hN){var hO=qx.bom.client.Feature.CSS_BORDER_RADIUS&&qx.bom.client.Feature.CSS_GRADIENTS&&qx.bom.client.Feature.CSS_BOX_SHADOW;
return {padding:[2,6],decorator:hO?db:di,minHeight:18,margin:hO?[0,5,5,0]:
undefined};
}},"window/statusbar-text":{style:function(hP){return {font:z};
}},"iframe":{style:function(hQ){return {decorator:ef};
}},"resizer":{style:function(hR){var hS=qx.bom.client.Feature.CSS_BOX_SHADOW&&qx.bom.client.Feature.CSS_BORDER_RADIUS&&qx.bom.client.Feature.CSS_GRADIENTS;
return {decorator:hS?L:dw};
}},"splitpane":{style:function(hT){return {decorator:j};
}},"splitpane/splitter":{style:function(hU){return {width:hU.horizontal?3:undefined,height:hU.vertical?3:undefined,backgroundColor:Q};
}},"splitpane/splitter/knob":{style:function(hV){return {source:hV.horizontal?dU:ba};
}},"splitpane/slider":{style:function(hW){return {width:hW.horizontal?3:undefined,height:hW.vertical?3:undefined,backgroundColor:Q};
}},"selectbox":ei,"selectbox/atom":ej,"selectbox/popup":cq,"selectbox/list":{alias:el},"selectbox/arrow":{include:ee,style:function(hX){return {source:cr,paddingLeft:5};
}},"datechooser":{style:function(hY){var id;
var ib=!!hY.focused;
var ic=!!hY.invalid;
var ia=!!hY.disabled;

if(ib&&ic&&!ia){id=ep;
}else if(ib&&!ic&&!ia){id=eo;
}else if(ia){id=cn;
}else if(!ib&&ic&&!ia){id=co;
}else{id=es;
}
if(qx.bom.client.Feature.CSS_GRADIENTS){id+=eh;
}return {padding:2,decorator:id,backgroundColor:cu};
}},"datechooser/navigation-bar":{},"datechooser/nav-button":{include:ei,alias:ei,style:function(ie){var ig={padding:[2,4],shadow:undefined};

if(ie.lastYear){ig.icon=cy;
ig.marginRight=1;
}else if(ie.lastMonth){ig.icon=bx;
}else if(ie.nextYear){ig.icon=bk;
ig.marginLeft=1;
}else if(ie.nextMonth){ig.icon=r;
}return ig;
}},"datechooser/last-year-button-tooltip":em,"datechooser/last-month-button-tooltip":em,"datechooser/next-year-button-tooltip":em,"datechooser/next-month-button-tooltip":em,"datechooser/last-year-button":dG,"datechooser/last-month-button":dG,"datechooser/next-month-button":dG,"datechooser/next-year-button":dG,"datechooser/month-year-label":{style:function(ih){return {font:eb,textAlign:dF,textColor:ih.disabled?ct:undefined};
}},"datechooser/date-pane":{style:function(ii){return {textColor:ii.disabled?ct:undefined,marginTop:2};
}},"datechooser/weekday":{style:function(ij){return {textColor:ij.disabled?ct:ij.weekend?bp:undefined,textAlign:dF,paddingTop:2,backgroundColor:bJ};
}},"datechooser/week":{style:function(ik){return {textAlign:dF,padding:[2,4],backgroundColor:bJ};
}},"datechooser/day":{style:function(il){var im=il.disabled?undefined:il.selected?cw:undefined;

if(im&&qx.bom.client.Feature.CSS_GRADIENTS){im+=eh;
}return {textAlign:dF,decorator:im,textColor:il.disabled?ct:il.selected?ed:il.otherMonth?bp:undefined,font:il.today?eb:undefined,padding:[2,4]};
}},"combobox":{style:function(io){var is;
var iq=!!io.focused;
var ir=!!io.invalid;
var ip=!!io.disabled;

if(iq&&ir&&!ip){is=ep;
}else if(iq&&!ir&&!ip){is=eo;
}else if(ip){is=cn;
}else if(!iq&&ir&&!ip){is=co;
}else{is=es;
}
if(qx.bom.client.Feature.CSS_GRADIENTS){is+=eh;
}return {decorator:is};
}},"combobox/popup":cq,"combobox/list":{alias:el},"combobox/button":{include:ei,alias:ei,style:function(it,iu){var iv={icon:cr,padding:[iu.padding[0],iu.padding[1]-6],shadow:undefined};

if(it.selected){iv.decorator=bw;
}return iv;
}},"combobox/textfield":{include:p,style:function(iw){return {decorator:undefined};
}},"menu":{style:function(ix){var iy=qx.bom.client.Feature.CSS_GRADIENTS&&qx.bom.client.Feature.CSS_BOX_SHADOW;
var iz={decorator:iy?bK:cD,shadow:iy?undefined:bD,spacingX:6,spacingY:1,iconColumnWidth:16,arrowColumnWidth:4,placementModeY:ix.submenu||ix.contextmenu?K:bn};

if(ix.submenu){iz.position=v;
iz.offset=[-2,-3];
}return iz;
}},"menu/slidebar":eD,"menu-slidebar":ek,"menu-slidebar-button":{style:function(iA){var iB=iA.hovered?cw:undefined;

if(iB&&qx.bom.client.Feature.CSS_GRADIENTS){iB+=eh;
}return {decorator:iB,padding:7,center:true};
}},"menu-slidebar/button-backward":{include:bq,style:function(iC){return {icon:iC.hovered?dA:bf};
}},"menu-slidebar/button-forward":{include:bq,style:function(iD){return {icon:iD.hovered?dx:cr};
}},"menu-separator":{style:function(iE){return {height:0,decorator:dp,margin:[4,2]};
}},"menu-button":{alias:ej,style:function(iF){var iG=iF.selected?cw:undefined;

if(iG&&qx.bom.client.Feature.CSS_GRADIENTS){iG+=eh;
}return {decorator:iG,textColor:iF.selected?ed:undefined,padding:[4,6]};
}},"menu-button/icon":{include:ee,style:function(iH){return {alignY:eg};
}},"menu-button/label":{include:cv,style:function(iI){return {alignY:eg,padding:1};
}},"menu-button/shortcut":{include:cv,style:function(iJ){return {alignY:eg,marginLeft:14,padding:1};
}},"menu-button/arrow":{include:ee,style:function(iK){return {source:iK.selected?n:r,alignY:eg};
}},"menu-checkbox":{alias:er,include:er,style:function(iL){return {icon:!iL.checked?undefined:iL.selected?C:cd};
}},"menu-radiobutton":{alias:er,include:er,style:function(iM){return {icon:!iM.checked?undefined:iM.selected?cS:cA};
}},"menubar":{style:function(iN){var iO=qx.bom.client.Feature.CSS_GRADIENTS;
return {decorator:iO?dv:dK};
}},"menubar-button":{alias:ej,style:function(iP){var iQ=(iP.pressed||iP.hovered)&&!iP.disabled?cw:undefined;

if(iQ&&qx.bom.client.Feature.CSS_GRADIENTS){iQ+=eh;
}return {decorator:iQ,textColor:iP.pressed||iP.hovered?ed:undefined,padding:[3,8]};
}},"colorselector":ek,"colorselector/control-bar":ek,"colorselector/control-pane":ek,"colorselector/visual-pane":cs,"colorselector/preset-grid":ek,"colorselector/colorbucket":{style:function(iR){return {decorator:ef,width:16,height:16};
}},"colorselector/preset-field-set":cs,"colorselector/input-field-set":cs,"colorselector/preview-field-set":cs,"colorselector/hex-field-composite":ek,"colorselector/hex-field":p,"colorselector/rgb-spinner-composite":ek,"colorselector/rgb-spinner-red":en,"colorselector/rgb-spinner-green":en,"colorselector/rgb-spinner-blue":en,"colorselector/hsb-spinner-composite":ek,"colorselector/hsb-spinner-hue":en,"colorselector/hsb-spinner-saturation":en,"colorselector/hsb-spinner-brightness":en,"colorselector/preview-content-old":{style:function(iS){return {decorator:ef,width:50,height:10};
}},"colorselector/preview-content-new":{style:function(iT){return {decorator:ef,backgroundColor:cu,width:50,height:10};
}},"colorselector/hue-saturation-field":{style:function(iU){return {decorator:ef,margin:5};
}},"colorselector/brightness-field":{style:function(iV){return {decorator:ef,margin:[5,7]};
}},"colorselector/hue-saturation-pane":ek,"colorselector/hue-saturation-handle":ek,"colorselector/brightness-pane":ek,"colorselector/brightness-handle":ek,"colorpopup":{alias:cq,include:cq,style:function(iW){return {padding:5,backgroundColor:s};
}},"colorpopup/field":{style:function(iX){return {decorator:ef,margin:2,width:14,height:14,backgroundColor:cu};
}},"colorpopup/selector-button":ec,"colorpopup/auto-button":ec,"colorpopup/preview-pane":cs,"colorpopup/current-preview":{style:function(iY){return {height:20,padding:4,marginLeft:4,decorator:ef,allowGrowX:true};
}},"colorpopup/selected-preview":{style:function(ja){return {height:20,padding:4,marginRight:4,decorator:ef,allowGrowX:true};
}},"colorpopup/colorselector-okbutton":{alias:ec,include:ec,style:function(jb){return {icon:cV};
}},"colorpopup/colorselector-cancelbutton":{alias:ec,include:ec,style:function(jc){return {icon:dJ};
}},"table":{alias:ek,style:function(jd){return {decorator:bg};
}},"table/statusbar":{style:function(je){return {decorator:bW,padding:[0,2]};
}},"table/column-button":{alias:ei,style:function(jf){var jg=qx.bom.client.Feature.CSS_GRADIENTS;
return {decorator:jg?T:eN,padding:3,icon:Y};
}},"table-column-reset-button":{include:er,alias:er,style:function(){return {icon:l};
}},"table-scroller":ek,"table-scroller/scrollbar-x":dD,"table-scroller/scrollbar-y":dD,"table-scroller/header":{style:function(jh){var ji=qx.bom.client.Feature.CSS_GRADIENTS;
return {decorator:ji?T:eN};
}},"table-scroller/pane":{style:function(jj){return {backgroundColor:dO};
}},"table-scroller/focus-indicator":{style:function(jk){return {decorator:bP};
}},"table-scroller/resize-line":{style:function(jl){return {backgroundColor:cM,width:2};
}},"table-header-cell":{alias:ej,style:function(jm){return {minWidth:13,minHeight:20,padding:jm.hovered?[3,4,2,4]:[3,4],decorator:jm.hovered?dc:I,sortIcon:jm.sorted?(jm.sortedAscending?dd:bj):undefined};
}},"table-header-cell/label":{style:function(jn){return {minWidth:0,alignY:eg,paddingRight:5};
}},"table-header-cell/sort-icon":{style:function(jo){return {alignY:eg,alignX:eM};
}},"table-header-cell/icon":{style:function(jp){return {minWidth:0,alignY:eg,paddingRight:5};
}},"table-editor-textfield":{include:p,style:function(jq){return {decorator:undefined,padding:[2,2],backgroundColor:cu};
}},"table-editor-selectbox":{include:x,alias:x,style:function(jr){return {padding:[0,2],backgroundColor:cu};
}},"table-editor-combobox":{include:dB,alias:dB,style:function(js){return {decorator:undefined,backgroundColor:cu};
}},"progressive-table-header":{alias:ek,style:function(jt){return {decorator:cx};
}},"progressive-table-header-cell":{alias:ej,style:function(ju){var jv=qx.bom.client.Feature.CSS_GRADIENTS;
return {minWidth:40,minHeight:25,paddingLeft:6,decorator:jv?bX:dn};
}},"app-header":{style:function(jw){return {font:eb,textColor:ed,padding:[8,12],decorator:cC};
}},"app-header-label":cv,"virtual-list":el,"virtual-list/row-layer":cB,"row-layer":{style:function(jx){return {colorEven:ea,colorOdd:bV};
}},"group-item":{include:cv,alias:cv,style:function(jy){return {padding:4,decorator:qx.bom.client.Feature.CSS_GRADIENTS?ey:bl,textColor:bz,font:eb};
}},"virtual-selectbox":x,"virtual-selectbox/dropdown":cq,"virtual-selectbox/dropdown/list":{alias:bs},"virtual-combobox":dB,"virtual-combobox/dropdown":cq,"virtual-combobox/dropdown/list":{alias:bs},"virtual-tree":el,"virtual-tree-item":{style:function(jz){return {padding:[2,6],textColor:jz.selected?ed:undefined,decorator:jz.selected?cw:undefined};
}},"virtual-tree-item/icon":{include:ee,style:function(jA){return {paddingRight:5,alignY:eg};
}},"virtual-tree-item/label":{include:cv,style:function(jB){return {alignY:eg};
}},"virtual-tree-folder":{include:dI,alias:dI,style:function(jC){return {icon:jC.opened?eI:bh};
}},"virtual-tree-folder/open":{include:ee,style:function(jD){var jE;

if(jD.selected&&jD.opened){jE=by;
}else if(jD.selected&&!jD.opened){jE=S;
}else if(jD.opened){jE=w;
}else{jE=t;
}return {padding:[0,5,0,2],source:jE,alignY:eg};
}},"virtual-tree-file":{include:dI,alias:dI,style:function(jF){return {icon:P};
}},"column-layer":ek,"cell":{style:function(jG){return {textColor:jG.selected?ed:eO,padding:[3,6],font:N};
}},"cell-string":cp,"cell-number":{include:cp,style:function(jH){return {textAlign:eM};
}},"cell-image":cp,"cell-boolean":{include:cp,style:function(jI){return {iconTrue:bT,iconFalse:cl};
}},"cell-atom":cp,"cell-date":cp,"cell-html":cp,"htmlarea":{"include":ek,style:function(jJ){return {backgroundColor:o};
}},"progressbar":{style:function(jK){return {decorator:dq,padding:[1],backgroundColor:cU};
}},"progressbar/progress":{style:function(jL){return {decorator:qx.bom.client.Feature.CSS_GRADIENTS?cG:cw};
}}}});
})();
(function(){var a="lino.theme.Appearance";
qx.Theme.define(a,{extend:qx.theme.modern.Appearance,appearances:{}});
})();
(function(){var n="Liberation Sans",m="Arial",l="Lucida Grande",k="sans-serif",j="Tahoma",i="Candara",h="Segoe UI",g="Consolas",f="Courier New",e="Monaco",b="monospace",d="Lucida Console",c="qx.theme.modern.Font",a="DejaVu Sans Mono";
qx.Theme.define(c,{fonts:{"default":{size:(qx.bom.client.System.WINVISTA||qx.bom.client.System.WIN7)?12:11,lineHeight:1.4,family:qx.bom.client.Platform.MAC?[l]:(qx.bom.client.System.WINVISTA||qx.bom.client.System.WIN7)?[h,i]:[j,n,m,k]},"bold":{size:(qx.bom.client.System.WINVISTA||qx.bom.client.System.WIN7)?12:11,lineHeight:1.4,family:qx.bom.client.Platform.MAC?[l]:(qx.bom.client.System.WINVISTA||qx.bom.client.System.WIN7)?[h,i]:[j,n,m,k],bold:true},"small":{size:(qx.bom.client.System.WINVISTA||qx.bom.client.System.WIN7)?11:10,lineHeight:1.4,family:qx.bom.client.Platform.MAC?[l]:(qx.bom.client.System.WINVISTA||qx.bom.client.System.WIN7)?[h,i]:[j,n,m,k]},"monospace":{size:11,lineHeight:1.4,family:qx.bom.client.Platform.MAC?[d,e]:(qx.bom.client.System.WINVISTA||qx.bom.client.System.WIN7)?[g]:[g,a,f,b]}}});
})();
(function(){var a="lino.theme.Font";
qx.Theme.define(a,{extend:qx.theme.modern.Font,fonts:{}});
})();
(function(){var a="lino.theme.Theme";
qx.Theme.define(a,{meta:{color:lino.theme.Color,decoration:lino.theme.Decoration,font:lino.theme.Font,icon:qx.theme.icon.Tango,appearance:lino.theme.Appearance}});
})();
(function(){var j="_applyStyle",i="stretch",h="Integer",g="px",f=" ",e="repeat",d="round",c="shorthand",b="px ",a="sliceBottom",y=";'></div>",x="<div style='",w="sliceLeft",v="sliceRight",u="repeatX",t="String",s="qx.ui.decoration.css3.BorderImage",r="border-box",q="",p='") ',n="sliceTop",o='url("',l="hidden",m="repeatY",k="absolute";
qx.Class.define(s,{extend:qx.ui.decoration.Abstract,construct:function(z,A){qx.ui.decoration.Abstract.call(this);
if(z!=null){this.setBorderImage(z);
}
if(A!=null){this.setSlice(A);
}},statics:{IS_SUPPORTED:qx.bom.element.Style.isPropertySupported("borderImage")},properties:{borderImage:{check:t,nullable:true,apply:j},sliceTop:{check:h,init:0,apply:j},sliceRight:{check:h,init:0,apply:j},sliceBottom:{check:h,init:0,apply:j},sliceLeft:{check:h,init:0,apply:j},slice:{group:[n,v,a,w],mode:c},repeatX:{check:[i,e,d],init:i,apply:j},repeatY:{check:[i,e,d],init:i,apply:j},repeat:{group:[u,m],mode:c}},members:{__lo:null,_getDefaultInsets:function(){return {top:0,right:0,bottom:0,left:0};
},_isInitialized:function(){return !!this.__lo;
},getMarkup:function(){if(this.__lo){return this.__lo;
}var B=this._resolveImageUrl(this.getBorderImage());
var C=[this.getSliceTop(),this.getSliceRight(),this.getSliceBottom(),this.getSliceLeft()];
var D=[this.getRepeatX(),this.getRepeatY()].join(f);
this.__lo=[x,qx.bom.element.Style.compile({"borderImage":o+B+p+C.join(f)+f+D,position:k,lineHeight:0,fontSize:0,overflow:l,boxSizing:r,borderWidth:C.join(b)+g}),y].join(q);
return this.__lo;
},resize:function(E,F,G){E.style.width=F+g;
E.style.height=G+g;
},tint:function(H,I){},_applyStyle:function(){{};
},_resolveImageUrl:function(J){return qx.util.ResourceManager.getInstance().toUri(qx.util.AliasManager.getInstance().resolve(J));
}},destruct:function(){this.__lo=null;
}});
})();
(function(){var j="px",i="0px",h="-1px",g="no-repeat",f="scale-x",e="scale-y",d="-tr",c="-l",b='</div>',a="scale",x="qx.client",w="-br",v="-t",u="-tl",t="-r",s='<div style="position:absolute;top:0;left:0;overflow:hidden;font-size:0;line-height:0;">',r="_applyBaseImage",q="-b",p="String",o="",m="-bl",n="qx.ui.decoration.GridDiv",k="-c",l="mshtml";
qx.Class.define(n,{extend:qx.ui.decoration.Abstract,construct:function(y,z){qx.ui.decoration.Abstract.call(this);
if(y!=null){this.setBaseImage(y);
}
if(z!=null){this.setInsets(z);
}},properties:{baseImage:{check:p,nullable:true,apply:r}},members:{__lp:null,__lq:null,__lr:null,_getDefaultInsets:function(){return {top:0,right:0,bottom:0,left:0};
},_isInitialized:function(){return !!this.__lp;
},getMarkup:function(){if(this.__lp){return this.__lp;
}var A=qx.bom.element.Decoration;
var B=this.__lq;
var C=this.__lr;
var D=[];
D.push(s);
D.push(A.create(B.tl,g,{top:0,left:0}));
D.push(A.create(B.t,f,{top:0,left:C.left+j}));
D.push(A.create(B.tr,g,{top:0,right:0}));
D.push(A.create(B.bl,g,{bottom:0,left:0}));
D.push(A.create(B.b,f,{bottom:0,left:C.left+j}));
D.push(A.create(B.br,g,{bottom:0,right:0}));
D.push(A.create(B.l,e,{top:C.top+j,left:0}));
D.push(A.create(B.c,a,{top:C.top+j,left:C.left+j}));
D.push(A.create(B.r,e,{top:C.top+j,right:0}));
D.push(b);
return this.__lp=D.join(o);
},resize:function(E,F,G){var H=this.__lr;
var innerWidth=F-H.left-H.right;
var innerHeight=G-H.top-H.bottom;
if(innerWidth<0){innerWidth=0;
}
if(innerHeight<0){innerHeight=0;
}E.style.width=F+j;
E.style.height=G+j;
E.childNodes[1].style.width=innerWidth+j;
E.childNodes[4].style.width=innerWidth+j;
E.childNodes[7].style.width=innerWidth+j;
E.childNodes[6].style.height=innerHeight+j;
E.childNodes[7].style.height=innerHeight+j;
E.childNodes[8].style.height=innerHeight+j;

if(qx.core.Variant.isSet(x,l)){if(qx.bom.client.Engine.VERSION<7||(qx.bom.client.Feature.QUIRKS_MODE&&qx.bom.client.Engine.VERSION<8)){if(F%2==1){E.childNodes[2].style.marginRight=h;
E.childNodes[5].style.marginRight=h;
E.childNodes[8].style.marginRight=h;
}else{E.childNodes[2].style.marginRight=i;
E.childNodes[5].style.marginRight=i;
E.childNodes[8].style.marginRight=i;
}
if(G%2==1){E.childNodes[3].style.marginBottom=h;
E.childNodes[4].style.marginBottom=h;
E.childNodes[5].style.marginBottom=h;
}else{E.childNodes[3].style.marginBottom=i;
E.childNodes[4].style.marginBottom=i;
E.childNodes[5].style.marginBottom=i;
}}}},tint:function(I,J){},_applyBaseImage:function(K,L){{};

if(K){var P=this._resolveImageUrl(K);
var Q=/(.*)(\.[a-z]+)$/.exec(P);
var O=Q[1];
var N=Q[2];
var M=this.__lq={tl:O+u+N,t:O+v+N,tr:O+d+N,bl:O+m+N,b:O+q+N,br:O+w+N,l:O+c+N,c:O+k+N,r:O+t+N};
this.__lr=this._computeEdgeSizes(M);
}},_resolveImageUrl:function(R){return qx.util.AliasManager.getInstance().resolve(R);
},_computeEdgeSizes:function(S){var T=qx.util.ResourceManager.getInstance();
return {top:T.getImageHeight(S.t),bottom:T.getImageHeight(S.b),left:T.getImageWidth(S.l),right:T.getImageWidth(S.r)};
}},destruct:function(){this.__lp=this.__lq=this.__lr=null;
}});
})();


qx.$$loader.init();

