/*
 Copyright 2012 Luc Saffre
 This file is part of the Lino project.
 Lino is free software; you can redistribute it and/or modify 
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 3 of the License, or
 (at your option) any later version.
 Lino is distributed in the hope that it will be useful, 
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
 GNU General Public License for more details.
 You should have received a copy of the GNU General Public License
 along with Lino; if not, see <http://www.gnu.org/licenses/>.

*/


//~ function waitFor(testFx, onReady, timeOutMillis) {
    //~ var maxtimeOutMillis = timeOutMillis ? timeOutMillis : 8001, //< Default Max Timeout is 8s
        //~ start = new Date().getTime(),
        //~ condition = false,
        //~ interval = setInterval(function() {
            //~ if ( (new Date().getTime() - start < maxtimeOutMillis) && !condition ) {
                //~ // If not time-out yet and condition not yet fulfilled
                //~ condition = (typeof(testFx) === "string" ? eval(testFx) : testFx()); //< defensive code
            //~ } else {
                //~ if(!condition) {
                    //~ // If condition still not fulfilled (timeout but condition is 'false')
                    //~ console.log("'waitFor()' timeout");
                    //~ phantom.exit(1);
                //~ } else {
                    //~ // Condition fulfilled (timeout and/or condition is 'true')
                    //~ console.log("'waitFor()' finished in " + (new Date().getTime() - start) + "ms.");
                    //~ typeof(onReady) === "string" ? eval(onReady) : onReady(); //< Do what it's supposed to do once the condition is fulfilled
                    //~ clearInterval(interval); //< Stop this interval
                //~ }
            //~ }
        //~ }, 500); //< repeat check every 100ms
//~ }; 

function waitfor(msg,until,limit,todo) {
    if (until()) {
      console.log("Done",msg);
      todo(true);
      return;
    };
    if (limit <= 0) {
      console.log("Giving up",msg);
      todo(false);
      //~ task_done(msg,false);
      return;
    };
    console.log('Retry',msg,'('+String(limit),"attempts left)");
    window.setTimeout(function() { waitfor(msg,until,limit-1,todo)},1000);
};


  
var tasks_waiting = [];
var running_tasks = 0;
var tasks_done = [];
var tasks_failed = [];

var OUTPUT_ROOT = 'gen/screenshots';
var SERVER_ROOT = 'http://127.0.0.1:8000';

var add_screenshot = function(url,filename) {
  console.log("add_screenshot",url,'to',filename);
  var task = function () {
    var address = SERVER_ROOT + url;
    var output = OUTPUT_ROOT + '/' + filename;
    
    var page = require('webpage').create();
    page.viewportSize = { width: 1024, height: 768};
    page.onConsoleMessage = function (msg) { console.log(msg); };
    page.onError = function (msg, trace) {
        console.log(msg);
        trace.forEach(function(item) {
            console.log('  ', item.file, ':', item.line);
        })
    }
    
    var loaded = function () { 
      return page.evaluate(function() { 
            //~ return !Ext.Ajax.isLoading();
            if (Lino && Lino.current_window) {
                return !Lino.current_window.main_item.is_loading();
            }
        }
      );
    };
    
    var todo = function (ok) { 
        console.log("Rendering to",output,ok);
        page.render(output);
        task_done(output,ok);
    };
    
    var on_opened = function (status) { 
        if (status !== 'success') {
            console.log('Unable to load ',address,status);
        } else {
            waitfor(output,loaded,3,todo);
        }
    };
    
    console.log("Loading",address,'to',output);
    
    page.open(address,on_opened);
    
  };
  tasks_waiting.push(task);
};


function task_done(msg,ok) {
    running_tasks -= 1;
    if(ok)
        tasks_done.push(msg);
    else
        tasks_failed.push(msg);
    next_task();
}

//~ function foreach(a,fn) {
    //~ for (var i = 0; i < a.length; i++) {
       //~ fn(a[i]);
    //~ }
//~ };

function next_task() {
    if (tasks_waiting.length == 0) {
      if (running_tasks == 0) {
          tasks_done.forEach(function(msg){console.log('done',msg)});
          tasks_failed.forEach(function(msg){console.log('failed',msg)});
          phantom.exit();
      }
      return;
    }
    console.log('next task of',tasks_waiting.length);
    var task = tasks_waiting.shift();
    running_tasks += 1;
    task();
}

console.log('screenshooter.js has been loaded');
