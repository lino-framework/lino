<?php

$GLOBALS['UserLog'] = '';
$GLOBALS['superTitleBuffer'] = '';
$GLOBALS['marginBuffer'] = '';
$GLOBALS['headerNumbers'] = array(0);
$GLOBALS['sequences'] = array();

function ToDebug($msg) {
  if ($GLOBALS['debug']) ToUserLog($msg);
}

function ToUserLog($msg) {
  $GLOBALS['UserLog'] .= '<br>' . $msg;
}


function ToSuperTitle($text) {
  if (isset($GLOBALS['superTitleBuffer']))
    $GLOBALS['superTitleBuffer'] .= $text;
}


function ToMargin($text) {
  $GLOBALS['marginBuffer'] .= $text;
}

function FlushPageMargin() {
  // echo ( ('FlushPageMargin()'));
  if (isset($GLOBALS['marginBuffer'])) {
    // if (strlen($GLOBALS['marginBuffer'])>0) {
      echo ( '</td><td width="15%" valign="top">');
      echo ( $GLOBALS['marginBuffer']);
      echo ( '</td></tr><tr><td>');
      $GLOBALS['marginBuffer'] = '';
      // }
  }
}

define('SEQ_BR',1);
define('SEQ_UL',2);
define('SEQ_OL',3);
define('SEQ_PARBOX' ,4);
define('SEQ_FORM',5);
define('SEQ_SENTENCES',6);
define('SEQ_PAR',7);

class Sequence {
  function Sequence($format,$title,$showLabels) {
    $this->format = $format;
    $this->title = $title;
    $this->showLables = $showLabels;
  }
}

function BeginSequence($format,$title=NULL,$showLabels=TRUE) {
  $seq = new Sequence($format,$title,$showLabels);
  global $sequences;
  $sequences[count($sequences)] = $seq;
  $GLOBALS['renderer']->ShowBeginSequence($seq);
}

function GetSequence() {
  global $sequences;
  if (count($sequences) == 0) return NULL;
  return $sequences[count($sequences)-1];
}

function BeginItem($label=NULL) {
  $seq = GetSequence();
  $GLOBALS['renderer']->ShowBeginItem($seq,$label);
}

function EndItem() {
  $seq = GetSequence();
  $GLOBALS['renderer']->ShowEndItem($seq);
}

function EndSequence() {
  global $sequences;
  $seq = $sequences[count($sequences)-1];
  $GLOBALS['renderer']->ShowEndSequence($seq);
  unset($sequences[count($sequences)-1]);
}
  


function BeginSection($title,
                      $num=NULL,
                      $mainComponent=NULL) { // ,$showNumbering=FALSE) {
  ToDebug("BeginSection($title)");
  global $headerNumbers;
  $headerNumbers[count($headerNumbers)-1]++;
  $headerLevel = count($headerNumbers);
  if ($headerLevel == 1) {
    BeginPage($title,$num,$mainComponent);
  } else {
    FlushPageMargin();
    if (is_null($num)) {
      $num = '';
      $i = 0;
      foreach($headerNumbers as $n) {
        if ($i>0) 
          $num .= $n . '.';
        $i++;
      }
    }
    $GLOBALS['renderer']->ShowTitle($title,$headerLevel,$num);
  }
  // $showHeaderNumbers[count($headerNumbers)] = $showNumbering;
  $headerNumbers[count($headerNumbers)] = 0;
//    }
  // print_r($headerNumbers);
}

function EndSection() {
  global $headerNumbers;
  ToDebug('EndSection()');
  // print_r($headerNumbers);
  unset($headerNumbers[count($headerNumbers)-1]);
  if (count($headerNumbers) == 1) {
    EndPage();
  }
// reset($headerNumbers);
  // print_r($headerNumbers);
  // if (count($headerNumbers)==0)
  // include('footer.inc.php');
  // ShowFooter();

}

function BeginPage($title,$num,$mainComponent) {
  $GLOBALS['pageTitle'] = $title;
  $GLOBALS['pageTitleNum'] = $num;
  $GLOBALS['mainComponent'] = $mainComponent;
  ob_start();
}

function EndPage() {

  $GLOBALS['bodyBuffer'] = ob_get_contents();
  ob_end_clean(); // necessary?

  $GLOBALS['renderer']->ShowPage();

  unset($GLOBALS['superTitleBuffer']);
  unset($GLOBALS['marginBuffer']);
  unset($GLOBALS['bodyBuffer']);
  unset($GLOBALS['pageTitle']);
  unset($GLOBALS['pageTitleNum']);
}


?>
