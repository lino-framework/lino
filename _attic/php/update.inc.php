<?php
include('lino.inc.php');

// $query = GetRequestedQuery();

$query =& $HTTP_SESSION_VARS['renderedQuery'];
// $HTTP_SESSION_VARS['editingQuery'] = NULL;

// global $HTTP_POST_VARS;
$i = 0;
assert('is_array($query->editingRows)');
foreach($query->editingRows as $row) {
  $sep = '';
  
  $query->row = $row; /* because canEdit() or other methods need the
                         current row. */
  $changed = 0;
  foreach($query->queryColumns as $cell) {
    $name = $cell->column->GetEditorName();
    if ($cell->column->canEdit($this)) { 
      $type = $cell->column->GetType();
      $newvalue = $HTTP_POST_VARS[$name][$i];
      if ($row[$name] != $newvalue) {
        $row[$name] = $newvalue;
        $changed++;
      }
    }
  }
  if ($changed > 0 || $row['_new']) {
    $query->master->dbd->sql_commit_row($query->master,$row);
  }
  $i++;
}

$query->isEditing = 0;

RedirectTo($query->GetUrlToSelf());

// $query->Render();

// $query =& $HTTP_SESSION_VARS['editingQuery'];
//  if (is_null($query)) {
//    ob_end_clean();
//    RedirectTo('index.php'); // LocationIndex();
//  }
//  ob_end_flush();
//  assert('$query->IsEditing()');

//  $query->Update();
// $query->RunAsMainComponent();

// do_GET_This();


// $msg = release();
// if (strlen($msg)!=0) LogMsg(MSG_DEBUG,$msg);
?>
