<?php

include('lino.inc.php');

if (!isset($HTTP_GET_VARS['t'])) {
  trigger_error('no table specified');
}
$query = new Query($HTTP_GET_VARS['t']);

//  if (isset($HTTP_GET_VARS['v'])) {
//    $query = new Query($HTTP_GET_VARS['t'],
//                       $HTTP_GET_VARS['v']);
//  } else {
//    $query = new Query($HTTP_GET_VARS['t']);
//  }

/**
  SetupMainQuery() is used only to set parameters of a default query
  to be opened via ref(). Not for any query. If SetupMainQuery sets a
  filter in DBITEMS. This filter must be active only for queries
  called via ref(), not those opened via GetRef()
  
  // $query->master->SetupMainQuery($query);
  
**/

foreach($HTTP_GET_VARS as $key => $value) {
  switch ($key) {
  case 'pglen':
    $query->pagelength = $value;
    break;
  case 'v':
    $query->SetView($value);
    break;
  case 'sd':
    $query->showDetails = $value;
    break;
//    case 'qfilter':
//      $query->qfilter = $value;
//      break;
  case 'filter':
    $query->filter = $value;
    break;
  case 'edit':
    $query->isEditing = $value;
    break;
  case 'depth':
    $query->SetDepth($value);
    break;
  case 'append':
    $query->SetAppend($value);
    break;
  case 'page':
    $query->SetPage($value);
    break;
  case 'sort':
    $query->Setup();
    $col = $query->queryColumns[$value];
    // inspect($col,'$col');
    // inspect($query->queryColumns);
    // ToDebug('sort set to '. $col->column->GetEditorName());
    $query->orderby = $col->column->GetSqlName();
    break;
  default:
    if (substr($key,0,1) == '_') {
      // inspect($value,'value');
      $query->SetSlice(substr($key,1),$value);
    } // else
    // trigger_error($key.'='.$value.' : no such option',E_USER_ERROR);
  }
}

$HTTP_SESSION_VARS['renderedQuery'] =& $query;
// inspect($query,'query');
$query->Render();

?>
