<?php

define ('LINO_VERSION','0.1.0');

$GLOBALS['babelLangs'] = array("en");
$GLOBALS['userLang'] = "en";

//  function LinoVersion() {
//    $s = 'Lino Version ';
//    $sep = '';
//    foreach(LINO_VERSION as $i) {
//      $s .= $sep . $i;
//      $sep = '.';
//    }
//    return $s;
//  }
// define ('LINO_DATE','2002-02-28'); // release date

$r = 'html';

if (isset($HTTP_GET_VARS['renderer'])) 
  $r = $HTTP_GET_VARS['renderer'];

switch ($HTTP_GET_VARS['renderer']) {
 case 'xml':
   include('xml.inc.php');
   $renderer = new XmlRenderer();
   break;
 default:
   include('html.inc.php');
   $renderer = new HtmlRenderer();
   break;
}

include('config.inc.php');
include('console.inc.php');
include('ostreams.inc.php');
include('datadict.inc.php');

/*
  modules.php will include the server specific set of modules.
*/

include('modules.inc.php');
// StartLino();

session_start();

// ob_get_contents();
// ob_end_clean();

// global $HTTP_SESSION_VARS;
// global $HTTP_GET_VARS;


init_option('debug',0);
init_option('verbose',0);
init_option('showJoinFields',0);

if (isset($HTTP_GET_VARS['meth'])) {
  switch ($HTTP_GET_VARS['meth']) {
  case 'reset':
    //$savedebug = $debug;
    //$saveverbose = $verbose;
    //$saveShowJoinFields = $showJoinFields;
    
    $HTTP_SESSION_VARS = array();
    
    //init_option('debug',$savedebug);
    //init_option('verbose',$saveverbose);
    //init_option('showJoinFields',$saveShowJoinFields);
    break;
//    case 'create_tables':
//      foreach($HTTP_SESSION_VARS['tables'] as $table) {
//        sql_create_table($table);
//      }
//      break;
  }
}


if (isset($HTTP_SESSION_VARS['app'])) {
  ToDebug('reuse session');
} else {

  // log_init();
  // ToUserLog('new session');
  
  $HTTP_SESSION_VARS['app'] = new Application();

  ToUserLog('Initialize modules...');
  include('appinit.inc.php');
  
  $HTTP_SESSION_VARS['app']->init();
  
  /*
    initialize modules and tables
  */
  // init_console();
  
//    $HTTP_SESSION_VARS['tables'] = array();
//    $HTTP_SESSION_VARS['modules'] = array();
  
//    ToDebug('<h2>initialize modules...</h2>');
//    global $modNames;
//    foreach($modNames as $modName) {
//      Module::GetInstance($modName);
//    }


//    ToDebug('<h2>Setup Tables...</h2>');

//    $tables =& $HTTP_SESSION_VARS['tables'];
//    foreach(array_keys($tables) as $key) {
//      $table =& $tables[$key];
//      $table->SetupLinks();
//    }

//    if (TRUE) {
//      ToDebug('<h2>Assert Tables...</h2>');
//      foreach($HTTP_SESSION_VARS['tables'] as $table) {
//        $pkeys = $table->GetPrimaryKey();
//        foreach($pkeys as $pk) {
//          assert('isset($table->fields[$pk])||inspect(array($table,$pk))');
//        }
//      }
//    }

  
  
  // include('init_session.php');
  
//    ToDebug('<h2>inspect tables...</h2>');
  
//    inspect($HTTP_SESSION_VARS['tables'],
//            '$HTTP_SESSION_VARS["tables"]');
  
}

if (TRUE) {
  $q = new Query('QUERIES');
  assert('isset($q->leader->details["columns"])');
  // inspect($q->view);
  // assert('isset($q->view->columns[""]->detail)');
  // assert('is_ref($q->view->columns[5]->detail,$q->master->details["columns"])');
  // assert('isset($q->view->columns[5]->detail->slaveQuery)');
} 

ToDebug('lino.inc.php completed.');
// ob_end_flush();
?>
