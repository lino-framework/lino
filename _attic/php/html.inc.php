<?php

// $headerLevel = 1;
// $renderNestingLevel=0; // see Query.Render()

// $showHeaderNumbers = array(FALSE);



class HtmlRenderer {
  
  function ShowTitle($text,$level=1,$num=NULL) {
    echo ( '<H'.$level.'>');
    if (!is_null($num))
      echo ( $num . ' ');
    echo ( $text );
    echo ( '</H'.$level.'>');
  }

  function ShowPage() {
    include('header.inc.php');

    echo $GLOBALS['superTitleBuffer'];

    $this->ShowTitle($GLOBALS['pageTitle'],1,$GLOBALS['pageTitleNum']);
    
    // echo "<H1>$GLOBALS['title']</H1>";

    if (isset($GLOBALS['mainComponent'])) {

      // if (isset($GLOBALS['HTTP_SESSION_VARS']['renderedQuery'])) {

      $this->ShowSubTitle($GLOBALS['mainComponent']);
//        $this->ShowSubTitle($GLOBALS['HTTP_SESSION_VARS']
//                            ['renderedQuery']);
    }

    global $UserLog;
    if (strlen($UserLog) > 0) {
      echo '<quote>';
      echo 'UserLog:';
      echo $UserLog;
      echo '</quote>';
    }
  
    // table to separate body and margin:
    echo '<table><tr><td>' ;
    
    // the actual body contents
    echo $GLOBALS['bodyBuffer'];
    
    // similar to FlushPageMargin:
    // ToDebug( ('EndPageMargin()'));
    echo( '</td><td width="15%">');
    echo( $GLOBALS['marginBuffer']);
    echo( '</td></tr></table>');
    
    // echo $GLOBALS['BodyBuffer'];
    // unset($GLOBALS['BodyBuffer']);
    
    include('footer.inc.php');
    // $GLOBALS['superTitleBuffer'] = '';
  }

  function ShowBeginSequence($seq) {
    if (!is_null($seq->title))
      echo '<p><b>' . $seq->title . '</b>.';
    switch ($seq->format) {
    case SEQ_BR:
      // echo '<p>';
      break;
    case SEQ_UL:
      echo '<ul>'; break;
    case SEQ_OL:
      echo '<ol>'; break;
    case SEQ_PARBOX:
      echo '<blockquote>'; break;
    case SEQ_FORM:
      echo '<table>'; break;
    case SEQ_PAR:
      break;
    case SEQ_SENTENCES:
      break;
    default:
      trigger_error('bad sequence format');
    }
  }
  
  function ShowEndSequence($seq) {
    switch ($seq->format) {
    case SEQ_BR:
      // echo '</p>';
      break;
    case SEQ_UL:
      echo '</ul>'; break;
    case SEQ_OL:
      echo '</ol>'; break;
    case SEQ_PARBOX:
      echo '</blockquote>'; break;
    case SEQ_FORM:
      echo '</table>'; break;
    case SEQ_PAR:
      // echo '</p>';
      break;
    case SEQ_SENTENCES:
      // echo '</p>';
      break;
    default:
      trigger_error('bad sequence format');
    }
  }

  function ShowBeginItem($seq,$label=NULL) {
    echo "\n";
    if ($seq->format == SEQ_UL)
      echo '<li>';
    elseif ($seq->format == SEQ_OL)
      echo '<li>';
    elseif ($seq->format == SEQ_PARBOX)
      echo '<p>';
    elseif ($seq->format == SEQ_BR)
      echo '<br>';
    elseif ($seq->format == SEQ_PAR)
      echo '<p>';
    elseif ($seq->format == SEQ_SENTENCES)
      echo '';
    elseif ($seq->format == SEQ_FORM)
      echo '<tr><td valign="top">';
    else
      trigger_error($seq->format . ' : bad style');

    if ($seq->showLables) { //  && !is_null($label)) {
    
      echo $label; 
    
      if ($seq->format == SEQ_FORM)
        echo '</td><td valign="top">';
      else
        echo ' : ';
    }
      
  }
  
  function ShowEndItem($seq) {
    if ($seq->format == SEQ_BR)
      echo '<br>';
    elseif ($seq->format == SEQ_UL)
      echo '</li>';
    elseif ($seq->format == SEQ_OL)
      echo '</li>';
    elseif ($seq->format == SEQ_PARBOX)
      echo '</p>';
    elseif ($seq->format == SEQ_SENTENCES)
      echo '. ';
    elseif ($seq->format == SEQ_PAR)
      echo '</p>';
    elseif ($seq->format == SEQ_FORM)
      echo '</td></tr>';
    else
      trigger_error('bad style');
  }
  


//    function ShowColAsParagraph($query,$col) {
//      echo '<p>';
//      $this->ShowColValue($col,
//                          $col->GetValueIn($query)
//                          );
//      echo '</p>';
//    }

  
  function ShowEditor($type,$format,$name,$value,$readonly) {
    if (is_a($type,'memotype')) {
      $width = $format[0];
      $height = $format[1];
      echo ( '<textarea cols=' . $width
             .' rows=' . $height
             .' name="' . $name . '"');
      if ($readonly) echo ( ' readonly' ) ;
      echo ( '>');
      echo ( $value);
      echo ( '</textarea>');
    } elseif (is_a($type,'booltype')) {
      echo ( '<input type="checkbox"');
      if ($value) echo ( ' checked');
      if ($readonly) echo ( ' readonly'    ) ;
      echo ( ' name="' . $name
             . '" value="yes">');
      echo ( "\n");

    } elseif (is_a($type,'texttype')) {
      
      $width = $format[0];
      echo ( '<input type="Text" name="' . $name . '"');
      if ($readonly) echo ( ' readonly'    ) ;
      echo ( ' size=' . $width
             . ' value="' . htmlspecialchars($value)
             . '">');
      echo ( "\n");
    } else {
      trigger_error('no editor for type '. get_class($type));
    }
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
//      if ($readonly) echo ( ' readonly'    ) ;
//      echo ( ' name="' . $name
//        . '" value="yes">');
//      echo ( "\n");
//    }
  
//    function ShowMemoInput($name,$value,$width,$height,$readonly) {
//      echo ( '<textarea cols=' . $width
//        .' rows=' . $height
//        .' name="' . $name . '"');
//      if ($readonly) echo ( ' readonly' ) ;
//      echo ( '>');
//      echo ( $value);
//      echo ( '</textarea>');
//    }
  
  function ShowColValue($col,$value,$format=NULL) {
    $type = $col->GetType();
    if (is_a($type,'querytype')) {
      if (!is_null($format)) $value->SetDepth($format);
      $value->Render();
    } elseif (is_a($type,'rowtype')) {
      if (is_null($value)) {
        echo 'NULL';
        return;
      }
      echo ( $col->join->toTable->GetPeekRef($value));
    } elseif (is_a($type,'memotype')) {
      // QuickTags

      /**
         - a litteral '[ref' (or '[url', or...)

         - followed by at least one whitespace
      
         - followed by a word (a greedy sequence of at least one
         character which is neither ']' nor whitespace). This will be $1
         in $replPattern
      
         - followed optionally by more whitespace and a sequence of any
         characters (including whitespace), but except ']' because this
         is the terminator.
      
         Note: currently it is not possible for this label string to
         contain a ']'
      
         if a quantifier is followed  by  a  question  mark,
         then it ceases to be greedy...
         http://ee.php.net/manual/en/pcre.pattern.syntax.php

      */
    
      // $findPattern = '/^\\\[url\w+(^\w+)\w+(.*)\]/e';
      $findPattern = '/\[url\s+([^\]\s]+)\s*(.*)\]/e';
      $replPattern = 'urlref(\'$1\',\'$2\')';
      $value = preg_replace($findPattern,$replPattern,$value);
    
      $findPattern = '/\[ref\s+([^\]\s]+)\s*?(.*?)\]/e';
      // $findPattern = '/\[ref\s+(\w+)\s*?(.*?)\]/e';
      $replPattern = 'ref(\'$1\',\'$2\')';
      $value = preg_replace($findPattern,$replPattern,$value);
    
      // $findPattern = '/\[srcref\s+(\S+)\s*(.*)\]/e';
      // $replPattern = 'srcref(\'$1\',\'$2\')';
      $findPattern = '/\[srcref\s+([^\]\s]+)\s*?(.*?)\]/e';
      // $findPattern = '/\[srcref\s+(\S+)\]/e';
      $replPattern = 'srcref(\'$1\')';
      $value = preg_replace($findPattern,$replPattern,$value);
      echo ($value);
    } elseif (is_a($type,'booltype')) {
      if ($value)
        echo 'yes';
      else
        echo 'no';
    } else {
      echo $value;
    }
  }
    
//    function ShowTextValue($value) {
//      echo ( $value);
//    }
  
//    function ShowMemoValue($value) {

//      // QuickTags

//      /**
//        - a litteral '[ref' (or '[url', or...)

//        - followed by at least one whitespace
      
//        - followed by a word (a greedy sequence of at least one
//        character which is neither ']' nor whitespace). This will be $1
//        in $replPattern
      
//        - followed optionally by more whitespace and a sequence of any
//        characters (including whitespace), but except ']' because this
//        is the terminator.
      
//        Note: currently it is not possible for this label string to
//        contain a ']'
      
//        if a quantifier is followed  by  a  question  mark,
//        then it ceases to be greedy...
//        http://ee.php.net/manual/en/pcre.pattern.syntax.php

//      */
    
//      // $findPattern = '/^\\\[url\w+(^\w+)\w+(.*)\]/e';
//      $findPattern = '/\[url\s+([^\]\s]+)\s*(.*)\]/e';
//      $replPattern = 'urlref(\'$1\',\'$2\')';
//      $value = preg_replace($findPattern,$replPattern,$value);
    
//      $findPattern = '/\[ref\s+([^\]\s]+)\s*?(.*?)\]/e';
//      // $findPattern = '/\[ref\s+(\w+)\s*?(.*?)\]/e';
//      $replPattern = 'ref(\'$1\',\'$2\')';
//      $value = preg_replace($findPattern,$replPattern,$value);
    
//      // $findPattern = '/\[srcref\s+(\S+)\s*(.*)\]/e';
//      // $replPattern = 'srcref(\'$1\',\'$2\')';
//      $findPattern = '/\[srcref\s+([^\]\s]+)\s*?(.*?)\]/e';
//      // $findPattern = '/\[srcref\s+(\S+)\]/e';
//      $replPattern = 'srcref(\'$1\')';
//      $value = preg_replace($findPattern,$replPattern,$value);

//      echo $value;
    
//      // echo ( eval('?.>' . $value . '<.?php '));
//    }
  
  function GetUrlRef($url,$label=NULL,$title=NULL) {
    if (is_null($label)) $label = $url;
    $s = '<a href="' . $url . '"';
    if (isset($title)) {
      $s .= ' title="'.htmlentities($title).'"';
    }
    $s .= '>'.htmlentities($label).'</a>';
    return $s;
  }
  
  function ShowQueryHeader($query) {
    // if ($query->pagelength != 1) {
    
    if ($query->IsMainComponent()) {
      if ($query->IsSinglePage()) {
        $query->leader->OnSinglePage($query);
      } else {
        // if ($query->IsSection()) {
        BeginSection($query->GetLabel(),NULL,$query);
      }
    } 

    if ($query->IsEditing()) {
      echo ( '<form name="edit_'
             .$query->leader->name
             .'" action="update.php" method="POST">');
      echo "\n";
    }
    switch ($query->depth) {
    case DEPTH_TABLE:
      echo ( "\n".'<table width="100%" class="list">');
      echo ( "\n<tr>");
      // $i = 0;
      foreach ($query->queryColumns as $name => $cell) {
        $width = $cell->format[0];
        echo ( "\n".'<td class="headrow"'
               . ' style="width:'. ($width * 10) . 'px"'
               . '>');
        
        // $cell->column->ShowColumnLabel($query,$i);

        if ($cell->column->canSort($query)) {
        
          echo ( $query->GetRef($cell->column->label,
                                array('sort'=>$name)));
        } else {
          echo $cell->column->label;
        }
          
        echo ( "\n".'</td>');
      }     
      echo ( "\n".'</tr>');
      break;
    case DEPTH_LIST:
      echo ( '<ul>');
      echo "\n";
      // default:
      break;
    case DEPTH_REF:
      echo $query->GetRef('('.$query->result->rowcount.')',
                          array('depth'=>DEPTH_TABLE));
    }
  }

  function ShowQueryFooter($query) {
    switch ($query->depth) {
    case DEPTH_TABLE:
      echo ( "\n".'</table>');
      break;
    case DEPTH_LIST:
      echo ( '</ul>');
      break;
    case DEPTH_SHORTLIST:
      if ($query->HasMore() && ! $query->IsSingleRow()) {
        echo ($query->
              GetRef(' [all]',
                     array('depth'=>DEPTH_LIST,
                           'page' => 0,
                           'edit'=>0
                           )
                     ));
      }
      break;
    }
    if ($query->IsEditing()) {
      echo ( '<input type="submit" value="Update">');
      echo ( '</form>');
    }
    
//      if ($query->IsSingleRow()) {
//        if ($query->IsMainComponent()) {
//          echo '<hr noshade><p>This is row ' . $query->row['id']
//            . ' in ';
//          echo GetQueryRef($query->leader->name);
      
//          echo '</p>';
//          $query->ShowNavigator();
//          $query->ShowOptionPanel();
//        }
//      }
    
    // if ($query->pagelength != 1) {
    if ($query->IsMainComponent()) {
      if (!$query->IsSinglePage()) {
        EndSection();
      }
    }
  }


  
  function ShowQueryRow($query,$first) {
    switch ($query->depth) {
    case DEPTH_SHORTLIST:
      if (! $first)
        echo ( ', ');
      $query->leader->ShowInShortList($query);
      break;
      
    case DEPTH_LIST:
      echo ( '<li>');
      $query->leader->ShowInList($query);
      echo ( '</li>');
      echo "\n";
      break;
      
    case DEPTH_TABLE:
      echo ( "\n".'<tr>');
      foreach($query->queryColumns as $cell) {
        // if ($cell->canSee($query)) {
          echo ( "\n".'<td class="'
            . ($query->result->recno % 2 != 0 ? 'oddrow' : 'evenrow')
            . '" valign="top">');
          // $query->OnCell($query->row,$col);
          if ($query->IsEditing() and $cell->column->canEdit($query)) {
            $col = $cell->column;
            $this->ShowEditor(
                              $col->GetType(),
                              $cell->format,
                              $col->GetEditorName().'[]',
                              $col->GetValueIn($query),
                              $col->IsReadOnly($query)
                              );
            // $cell->column->ShowColEditor($query);
          } else {
            $value = $cell->column->GetValueIn($query);
            $this->ShowColValue($cell->column, $value);
          }
          echo ( "\n".'</td>');
          // }
      }
      echo ( "\n".'</tr>');
      break;

    case DEPTH_PAGE:
//        if ($query->GetNestingLevel() == 1)
//          $query->leader->OnStartOutput($query);
      
      
      BeginSection($query->leader->GetRowLabel($query->row),
                   $query->result->recno . '.');
      
      if ($query->GetNestingLevel() == 1) {
        $s = 'row ';
        $sep = '';
        foreach($query->leader->GetPrimaryKey() as $pk) {
          $s .= $sep . $query->row[$pk];
          $sep = '.';
        }
        ToMargin($s . ' in '
                 . $query->leader->GetRef()
                 );
      }
      

      if ($query->IsEditing()) {
        // $query->leader->ShowInForm($query,$first);
        echo ( "\n".'<table width="100%" class="form">');
        foreach($query->queryColumns as $cell) {
          echo ( "\n".'<tr>');
          echo ( "\n".'<td>' . $cell->column->GetLabel() . '</td>');
          echo ( "\n".'<td>');
          // $cell->column->ShowColEditor($query);
          $col = $cell->column;
          $this->ShowEditor(
                            $col->GetType(),
                            $cell->format,
                            $col->GetEditorName().'[]',
                            $col->GetValueIn($query),
                            $col->IsReadOnly($query)
                            );
            
          echo ( '</td>');
          echo ( '</tr>');
        }
        echo ( "\n".'</table>');
      } else {
        $query->leader->ShowInPage($query,$first);
      }
      // echo ( '<td bgcolor="gold" valign="top">');
      // $query->leader->ShowPageMarginContent($query,$first);
      // echo ( '</tr></table>');
      // FlushPageMargin();
      EndSection();
      break;
//      case QRYFORMAT_FORM:
//        // if (! $query->IsSingleRow())
//        BeginSection($query->leader->GetRowLabel($query->row));
//        $query->leader->ShowInForm($query);
//        EndSection();
//        FlushPageMargin();
//        break;
//      case QRYFORMAT_PLIST:
//        if (! $first)
//          echo ( '<p>');
//        $query->leader->ShowInParList($query);
//        break;
    }
  }
  

  function ShowSubTitle($query) {
    switch ($query->depth) {
    case DEPTH_LIST:
      $this->ShowNavigator($query);
      $this->ShowDepthSelector($query);
      break;
    case DEPTH_TABLE:
      $this->ShowFormatSelector($query);
      $this->ShowQuickFilter($query);
      $this->ShowDepthSelector($query);
      $this->ShowNavigator($query);
      $this->ShowOptionPanel($query);
      break;
    case DEPTH_PAGE:
      $this->ShowNavigator($query);
      break;
    }
  }



  function ShowDepthSelector($query) {

    echo ( '<p>Depth :');

    foreach($GLOBALS['depths'] as $id => $name) {
      echo ( '&nbsp;');
      if ($id == $query->depth)
        echo ( '['.$id.']');
      else
        echo ( $query->GetRef('['.$id.']',
                           array('depth'=>$id),
                           $name));
    }
    
    echo ( '</p>');
  }
    
  function ShowFormatSelector($query) {
    echo ( '<p>Renderer :');
    echo ( '&nbsp;');
    echo ( $query->GetRef('[XML]',
                   array('renderer'=>'xml'),
                   'show result as XML'));

    echo ( '</p>');
    
    
    echo ( '<p>View Editor : ');

    echo ( $GLOBALS['renderer']->
      GetUrlRef('render.php?t=QUERIES&depth='.DEPTH_PAGE
                .'&edit=1'
                .'&_id='. $query->view->name,
                '[Edit View]'));
    
    echo ( '</p>');

  }
  
  function ShowQuickFilter($query) {
    $self = 'render_p.php';
    // $self = $query->GetUrlToSelf(); // array('method'=>'"GET"'));
    // echo $self;
    echo ( '<p><form name="navigator" action="'
      . $self
      . '" method="POST">');
    // 'render.php?t=' . $query->leader->name . '" method="GET">';
    echo ( 'Quick filter : ');
    
//      echo ( '<input type="hidden" name="t" value="'
//             .$query->leader->name
//             .'"');
    echo ( '<input type="text" name="qfilter"');
    if (!is_null($query->qfilter)) {    
      echo ( ' value="' . $query->qfilter . '"');
    }
    echo ( '>');
    
    echo ( '<input type="image" src="images/go.gif"'
           .' title="set filter">');
    echo ( '</form>');
    echo ( '</p>');
       
  }

  function ShowNavigator($query) {
    if ($query->page == 0) {
      // echo ( '(no navigator since all rows are displayed)');
      return;
    }
    if ( $query->GetPageLength() <= 0) {
      return;
    }
    $maxpage=(int)ceil($query->result->rowcount /
                       $query->GetPageLength());
    
    if ($maxpage == 1) return;
    
    echo ( '<p>Navigator : ');
    
    if ($query->page > 1) {
      echo ( '&nbsp;');
      echo ( $query->GetRef('[first]',array('page'=>1)));
      echo ( '&nbsp;');
      echo ( $query->GetRef('[prev]',array('page'=>$query->page-1)));
      //ShowButtonRef('this.php?page=1','first');
      //ShowButtonRef('this.php?page='.($query->page-1),'prev');
    }
    
    for ($i=max(1,$query->page-10);
         $i<=min($maxpage,$query->page+10);
         $i++)
      {
        if ($i == $query->page) 
          print "&nbsp; $i\n";
        else {
          echo ( '&nbsp;');
          echo ( $query->GetRef($i,array('page'=>$i)));
        }
        
        // print "<a href=\"this.php?page=$i\">$i</a>&nbsp;";
      }
    
    if ($query->page < $maxpage) {
      echo ( '&nbsp;');
      echo ( $query->GetRef('[next]',array('page'=>$query->page+1)));
      echo ( '&nbsp;');
      echo ( $query->GetRef('[last]',array('page'=>$maxpage)));
      // ShowButtonRef('this.php?page='.$maxpage,'last');
      // ShowButtonRef('this.php?page='.($query->page+1),'next');
    }
    
    echo ( '&nbsp;');
    echo ( $query->GetRef('[all]',array('page'=>0,'pglen'=>0)));
    echo ( '</p>');
  }

  function ShowOptionPanel($query) {
    
    echo ( '<p>Options : ');

    if ($query->CanEdit()) {
      echo ( 'isEditing : ');
      if ($query->isEditing) {
        echo ( '[on]');
        echo ( '&nbsp;');
        echo ( $query->GetRef('[off]',array('edit'=>0)));
      } else {
        echo ( $query->GetRef('[on]',array('edit'=>1)));
        echo ( '&nbsp;');
        echo ( '[off]');
      }
      echo ( ', ');
    }
    
    echo ( 'showDetails : ');
    echo ( '&nbsp;');
    if ($query->showDetails == 0)
      echo ( '[0]');
    else
      echo ( $query->GetRef('[0]',array('sd'=>0)));
    echo ( '&nbsp;');
    if ($query->showDetails == 1)
      echo ( '[1]');
    else
      echo ( $query->GetRef('[1]',array('sd'=>1)));
//      echo ( '&nbsp;');
//      if ($query->detailLevel == 2)
//        echo ( '[2]');
//      else
//        $query->ShowRef('[2]',array('dl'=>2));
    echo ( '</p>');
  }

}



//  function ShowFooter() {
//    global $HTTP_SESSION_VARS;
//    global $HTTP_SERVER_VARS;
  
//  }



//  function ToBody($text) {
//    if (isset($GLOBALS['BodyBuffer']))
//      $GLOBALS['BodyBuffer'] .= $text;
//    else
//      echo $text;
//  }




function ref($peek,$label=NULL,$title=NULL) {
  if (!is_null($label) && strlen($label)==0)
    $label = NULL;
  $a = split(':',$peek);
  if (count($a) == 2) {
    $id = split('\.',$a[1]);
    // function GetPeekRef($tableName,$id,$label=NULL) {
    $table = GetTable($a[0]);
    $row = $table->Peek($id);
    if (is_null($row))
      return '[?ref '.$peek.']';
    return $table->GetPeekRef($row,$label);
    // return GetPeekRef($a[0],$id,$label,$title);
  } else if (count($a) == 1) {
    // function GetQueryRef($tableName,$viewName=NULL,$label=NULL) {
    $query = new Query($a[0]);
    $query->leader->SetupMainQuery($query);
    // echo $query->depth;
    // $query->Setup();
    return $query->GetRef($label);
    //    $table =& Table::GetInstance($tableName);
    //    if ($viewName==NULL) $viewName = $table->GetDefaultView();
    //    $view = $this->GiveView($viewName);
    //    $view->ShowRef($this,$label);
  
    // }

  // return GetQueryRef($a[0],$label,$title);
  } else {
    trigger_error('invalid reference...',E_USER_ERROR);
  }
}


//  /**
//   ** used only in index.php
//   **/
//  function Render($what) {
//    $a = split(':',$what);
//    if (count($a) == 2) {
//      $query = new Query($a[0]);
//      $query->SetDepth(DEPTH_PAGE);
//      $id = split(',',$a[1]);
//      $pkeys = $query->leader->GetPrimaryKey();
//      foreach($pkeys as $i => $pk) {
//        $query->SetSlice($pk,$id[$i]);
//      }
//      // $query->SetSingleRow();
//      // $query->isMainComponent = TRUE;
//      $query->Render();
//    } else if (count($a) == 1) {
//      return GetQueryRef($a[0],$label,$title);
//    } else {
//      trigger_error($what . ' : cannot render',E_USER_ERROR);
//    }
//  }

function urlref($url,$label=NULL,$title=NULL) {
  if (!is_null($label) && strlen($label)==0)
    $label = NULL;
  //$renderer = GetRenderer();
  global $renderer;
  return $renderer->GetUrlRef($url,$label,$title);
//    echo ( '<a href="'. $url);
//    echo '">'
//      . (is_null($label) ? $url : $label)
//      .'</a>';
}

function srcref($file,$label=NULL,$title=NULL) {
  global $renderer;
  if(is_null($label)  || strlen($label)==0) {
    $label = $file;
  }
  return $renderer->GetUrlRef('source.php?file='.$file,$label,$title);
//    echo '<a href="source.php?file='.
//      $file .'">'
//      . (is_null($label) ? $file : $label)
//      .'</a>';
}


?>
