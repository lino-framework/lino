<?php

class XmlRenderer {

  function ShowValue($type,$value) {
    echo '<value type="'.get_class($type).'">';
    echo htmlspecialchars($value);
    echo '</value>';
  }
  
  function ShowPage() {
    header('Content-type: text/xml');
    echo ( '<?xml version="1.0" encoding="ISO-8859-1"?>');
    echo ( "\n");
    
    echo '<page>';
    
    echo '<superTitle>';
    echo $GLOBALS['superTitleBuffer'];
    echo '</superTitle>';
    
    echo '<body>';
    $this->ShowTitle(1,'',$GLOBALS['title']);
    echo $GLOBALS['bodyBuffer'];
    echo '</body>';
    
    echo '<userLog>';
    echo $GLOBALS['UserLog'];
    echo '</userLog>';

    echo '<margin>';
    echo( $GLOBALS['marginBuffer']);
    echo '</margin>';
    
    echo '</page>';
  }
  
  function ShowTitle($level,$prefix,$text) {
    echo ( '<title level="'.$level .'">');
    echo ( $prefix . ' ');
    echo ( $text );
    echo ( '</title>');
  }
  
//    function ShowTextInput($name,$value,$width,$readonly) {
//       echo ( '<input type="Text" name="' . $name . '"');
//       if ($readonly) echo ( ' readonly'    ) ;
//       echo ( ' size=' . $width
//         . ' value="' . htmlspecialchars($value)
//         . '">');
//       echo ( "\n");
//    }
  
//    function ShowBoolInput($name,$value,$readonly) {
//      echo ( '<input type="checkbox"');
//      if ($value) echo ( ' checked');
//      if ($readonly) echo ( ' readonly');
//      echo ( ' name="' . $name . '" value="yes">');
//      echo ( "\n");
//    }
  
//    function ShowMemoInput($name,$value,$width,$height,$readonly) {
//      echo ( '<textarea cols=' . $width
//        .' rows=' . $height
//        .' name="' . $name . '"');
//      if ($readonly) echo ( ' readonly'    ) ;
//      echo ( '>');
//      echo ( $value);
//      echo ( '</textarea>');
//    }

  

//    function ShowTextValue($value) {
//      echo ( $value);
//    }
  
//    function ShowMemoValue($value) {
//      echo ( htmlspecialchars($value));
//    }
  
  function GetUrlRef($url,$label=NULL,$title=NULL) {
    if (is_null($label)) $label = $url;
    $s = '<a href="' . htmlspecialchars($url). '"';
    if (isset($title)) {
      $s .= ' title="'.htmlentities($title).'"';
    }
    $s .= '>'.htmlspecialchars($label).'</a>';
    return $s;
  }
  
  function ShowQueryHeader($query) {
    if ($query->IsSection()) {
      // if ($GLOBALS['level'] == 1) {
      BeginSection($query->GetLabel());
      // $this->ShowSubTitle($query);
    }
    
//      if ($query->IsMainComponent()) {
//        header("Content-type: text/xml");
//        echo ( '<.?xml version="1.0" encoding="ISO-8859-1"?.>');
//        echo ( "\n");
//        // echo ( '<.?xml:stylesheet type="text/xsl" href="query.xsl"?.>');
//      }
//      echo ( "\n<query>");
//      echo ( "\n<header>");
//      echo ( "\n<title>");
//  //      if ($query->IsSingleRow()) {
//  //        echo ( htmlentities($query->master->GetRowLabel($query->row)));
//  //      } else {
//        echo ( htmlentities($query->GetLabel()));
//  //      }
//      echo ( "</title>");
//      if ($query->IsEditing()) {
//        echo ( "\n<isEditing>");
//      }
//      echo ( "\n</header>");
    echo ( "\n<columns>");
    foreach ($query->queryColumns as $cell) {
      // if ($col->canSee($query)) {
      $col = $cell->column;
      $t = $col->GetType();
      echo ( "\n<column ");
      echo ( 'name="'.$col->GetEditorName().'">');
      echo ( "\n<type>" . get_class($t). "</type>");
      // echo ( "\n<width>" . $t->width. "</width>");
      echo ( "\n<label>" . htmlentities($col->GetLabel()). "</label>");
      if ($query->IsEditing() and $col->canEdit($query)) {
        echo ( "\n<editing/>");
      }
      echo ( "\n</column>");
        // }
    }     
    echo ( "\n</columns>");
    echo ( "\n<rows>");
  }
  
  function ShowQueryRow($query,$first) {
    echo ( "\n<row>");
    foreach ($query->queryColumns as $cell) {
      // if ($col->canSee($query)) {
      $col = $cell->column;
      $t = $col->GetType();
      echo ( "\n<cell ");
      echo ( 'column="'.$col->GetEditorName().'">');
      if ($col->IsReadOnly($query)) {
        echo ( "\n<readonly/>");
      }
      // echo ( "\n<value>");
      $col->ShowValueIn($query);
      // echo ( "</value>\n");
      echo ( "</cell>\n");
        // }
    }
    echo ( "\n</row>");
  }
  
  function ShowQueryFooter($query) {
    echo ( "\n</rows>");
    if ($query->IsSection()) {
      EndSection();
    }
    // echo ( "\n</query>");
  }

}

?>
