<?php

$errortype = array (
                    1    =>  "Error",
                    2    =>  "Warning",
                    4    =>  "Parsing Error",
                    8    =>  "Notice",
                    16   =>  "Core Error",
                    32   =>  "Core Warning",
                    64   =>  "Compile Error",
                    128  =>  "Compile Warning",
                    256  =>  "User Error",
                    512  =>  "User Warning",
                    1024 =>  "User Notice"
                    );
  


function error_handler ($level, $message, $file, $line, $context)
{
  
  echo '<html>';
  global $errortype;
  echo '<b>' . $errortype[$level] . ':</b> ' ;
  echo $message;
  echo "\n<br>in <b>$file</b> on line <b>$line</b>.";
  echo "\n".'<p><a href="index.php?meth=reset">Restart</a>';
  echo "\n".'<a href="index.php">Home</a>';

  
  // echo "\n".'<h2>Session Log</h2>';
  // log_show();
  
  echo "\n".'<h2>context:</h2>'
    ."\n".'<ul>';

  foreach($context as $k =>$v) {
    echo "\n".'<li>';
    inspect($v,$k);//  . ' = ' . $v;
    echo "</li>\n";
  }
  // print_r ($context);
  echo "\n".'</ul>';
  
  echo "\n".'<p><b>' . $errortype[$level] . ':</b> ' ;
  echo $message;
  echo "\n<br>in <b>$file</b> on line <b>$line</b>.";
  echo "\n".'</p><p><a href="logout.php">Restart</a></p>';
  echo '</html>';
  EndPage();
  die();
}

// Set the error handler to the error_handler() function
set_error_handler ('error_handler');

//  function LogMsg($type,$msg) {
//    global $HTTP_SERVER_VARS, $HTTP_SESSION_VARS, $verbose;
//    // $msg = $HTTP_SERVER_VARS['SCRIPT_NAME'] . ':' . $msg;
//    // if (isset($HTTP_SESSION_VARS['modules'])) {
//      if ($verbose == 2) {
//        echo '<br>' . $msg;
//      } else {
//        $HTTP_SESSION_VARS['log'][] = $msg;
//        $num = count($HTTP_SESSION_VARS['log']);
//        if ($verbose == 1) {
//          echo '<a href="log_show.php#' . $num
//            . '" title="'
//            . htmlspecialchars($msg)
//            . '">' . $num
//            . '</a>';
//        }
//  //      else if ($debug == 0) {
//  //        // okay
//  //      } else trigger_error('$debug : invalid value '.$debug,
//  //                           E_USER_ERROR);
//      }
//      // }
    
//  }

//  define('MSG_DEBUG','d');
//  define('MSG_SQL','*');

//  function LogDebug($msg) {
//    global $debug;
//    if ($debug) LogMsg(MSG_DEBUG,$msg);
//  }



//  function log_init() {
//    // trigger_error('log_init()',E_USER_ERROR);
//    global $HTTP_SESSION_VARS;
//    $HTTP_SESSION_VARS['log'] = array();
//  }

//  function log_show() {
//    global $HTTP_SESSION_VARS;
//    if (isset($HTTP_SESSION_VARS['log'])) {
//      echo '<p>' . count($HTTP_SESSION_VARS['log']). ' logged messages:';
//      echo '<ol>';

//      $i = 0;
//      foreach($HTTP_SESSION_VARS['log'] as $msg) {
//        echo '<li>';
//        echo '<a name ="'.$i.'">';
//        echo $msg;
//        echo '</a>';
//        echo '</li>';
//        $i++;
//      }
    
//      echo '</ol>';

//      log_init();
//      echo '<p>(Log has been cleared)';
//    }
//  }

// stop reporting errors
function catch() {
  global $oldErrorLevel;
  $oldErrorLevel = error_reporting(E_PARSE
                                   & E_COMPILE_ERROR
                                   & E_COMPILE_WARNING);
}

// start reporting errors
function release() {
  global $oldErrorLevel, $php_errormsg;
  error_reporting($oldErrorLevel);
  return $php_errormsg;
}


function svar_dump($var) {
  ob_start();
  var_dump($var);
  $line = ob_get_contents();
  ob_end_clean();
  return $line;
}

//  function StartLino() {

//  }


function init_option($name,$default) {
  global $HTTP_GET_VARS, $HTTP_SESSION_VARS;
  if (isset($HTTP_GET_VARS[$name])) {
    $HTTP_SESSION_VARS[$name] = $HTTP_GET_VARS[$name];
  } else if (!isset($HTTP_SESSION_VARS[$name])) {
    $HTTP_SESSION_VARS[$name] = $default;
  }
  $GLOBALS[$name] =& $HTTP_SESSION_VARS[$name];
}



//  function GetOption($name) {
//    global $HTTP_SESSION_VARS;
//    if (isset($HTTP_SESSION_VARS[$name]))
//      return $HTTP_SESSION_VARS[$name];
//    if (isset($HTTP_GET_VARS[$name]))
//      return $HTTP_GET_VARS[$name];
//    return 0;
//  }

//  class Option {
//    var $options = array();
//    var $id;
//    var $label;
//    function Option($id,$label) {
//      $this->id = $id;
//      $this->label=label;
//    }
//    function AddOption($id,$label) {
//      $this->options[] = new Option($id,$label);
//    }
//    function get
//  }


// function LocationIndex($filename='index.php') {
function RedirectTo($filename='index.php') {
  global $HTTP_SESSION_VARS,$HTTP_SERVER_VARS, $verbose;
  if (TRUE) {
    // if (!ob_get_length()) {
    // if ($verbose == 0) {
    header("Location: http://".$HTTP_SERVER_VARS['HTTP_HOST']
           .dirname($HTTP_SERVER_VARS['PHP_SELF'])
           .'/'.$filename);
    // $HTTP_SESSION_VARS['query'] = NULL;
    exit;
  } else {
    // echo 'foo';
    BeginSection('RedirectTo');
    
    echo 'Automatic redirection is disabled. Please click yourself ';
    
    echo '<a href="'.$filename.'">here</a>';
    echo ' to continue.';
    EndSection();
    exit;
  }

  
}

//  class Inspector {
//    var $level;
//    var $value;
//    function Inspector() {
//    }
//  }

function inspect($arg,$label=NULL) {
  static $level = 0;
  // if ($GLOBALS['debug']==0) return;
  if ($level > 4) return;
  if (!is_null($label)) {
    echo '<b>' . $label . ':</b> ';
  }
  $level++;
  if (is_object($arg)) {
    if (method_exists($arg,'inspect')) {
      $arg->inspect();
    } else {  
      echo ' ';
      // echo get_class($arg);
      print_r($arg);
    }
  } else if (is_array($arg)) {
    echo 'Array (<ul>';
    foreach($arg as $k=>$v) {
      echo '<li>' . $k . ' => ';
      inspect($v);
    }
    echo '</ul>)';
  } else {
    var_dump($arg);
    // echo $arg . ':' . gettype($arg);
  }
  $level--;
  // echo '<br>';
  // }
}

//  function init_console() {
//    $GLOBALS['HTTP_SESSION_VARS']['UserLog'] = '';
//    ToUserLog('init_console()');
//  }

//  function ToUserLog($msg) {
//    $GLOBALS['HTTP_SESSION_VARS']['UserLog'] .= '<br>' . $msg;
//  }



?>
