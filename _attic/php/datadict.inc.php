<?php
/**
 * datadict.inc.php : classes used to manage the data dictionary 
 */

define('TYPE_INT',   'int');
define('TYPE_AUTO',   'auto');
// define('TYPE_DEC',   'dec');
define('TYPE_BOOL',  'bool');
define('TYPE_STRING','string');
define('TYPE_MEMO',  'memo');
define('TYPE_DATE',  'date');
define('TYPE_ROW',  'row');
define('TYPE_QUERY',  'query');

$types = array(
               TYPE_INT    => new IntType(),
               TYPE_AUTO   => new AutoIncType(),
               TYPE_BOOL   => new BoolType(),
               TYPE_STRING => new TextType(),
               TYPE_MEMO   => new MemoType(),
               TYPE_DATE   => new DateType(),
               TYPE_ROW    => new RowType(),
               TYPE_QUERY  => new QueryType()
               );

define('DEPTH_HIDDEN',   0);
define('DEPTH_REF',      1);
define('DEPTH_SHORTLIST',2);
define('DEPTH_LIST',     3);
define('DEPTH_TABLE',    4);
define('DEPTH_PAGE',     5);

//  define ('STYLE_DEFAULT',0);
//  define ('STYLE_ITEM',1);
//  define ('STYLE_PARA',2);
//  define ('STYLE_SECTION',3);


$depths = array( DEPTH_HIDDEN => 'do not show',
                 DEPTH_REF => 'show reference',
                 DEPTH_SHORTLIST => 'show short list',
                 DEPTH_LIST => 'show list',
                 DEPTH_TABLE => 'show table',
                 DEPTH_PAGE => 'show page',
                 );

//  $maxDetailDepth = array( DEPTH_HIDDEN    => DEPTH_HIDDEN,
//                           DEPTH_REF       => DEPTH_HIDDEN,
//                           DEPTH_SHORTLIST => DEPTH_HIDDEN,
//                           DEPTH_LIST      => DEPTH_SHORTLIST,
//                           DEPTH_TABLE     => DEPTH_TABLE,
//                           DEPTH_PAGE      => DEPTH_PAGE);
                         
//  $defaultDetailDepth = array( DEPTH_HIDDEN    => DEPTH_HIDDEN,
//                               DEPTH_REF       => DEPTH_HIDDEN,
//                               DEPTH_SHORTLIST => DEPTH_HIDDEN,
//                               DEPTH_LIST      => DEPTH_HIDDEN,
//                               DEPTH_TABLE     => DEPTH_SHORTLIST,
//                               DEPTH_PAGE      => DEPTH_TABLE);

/**
 * Abstract class to describe the data type of a value.  Each {@link
 * Field} will contain one Type instance. But also for example the
 * return type of a {@link Vurt} is a Type subclass.
 * */
class Type { 
//    var $width;

//    function Type($width) {
//      $this->width=$width;
//    }

//    function ShowEditor($name,$value,$readonly) {
//      $GLOBALS['renderer']->ShowTextInput($name,
//                                          $value,
//                                          $this->width,
//                                          $readonly);
//    }

//    function ShowValue($value) {
//      $GLOBALS['renderer']->ShowTextValue($value);
//    }
  
//    function SetWidth($width) {
//      $this->width = $width;
//      return $this;
//    }

  function str2value($str) {
    if (strlen($str)==0) return NULL;
    return $str;
  }

  function to_sql($value) {
    if (strlen($value) == 0) return 'NULL';
    return $value;
  }

  function CanQuickFilter() {
    return FALSE;
  }

  /**
   ** overridden by AutoIncType because references to an
   ** AUTO_INCREMENT field are not AUTO_INCREMENT...
   **/
  function GetRefType() {
    return $this;
  }

  function IsVisible($query) {
    return TRUE;
  }
  
  function GetDefaultFormat() {
    return NULL;
  }
  
}
 
/**
 * Boolean values.
 */
class BoolType extends Type {

//    function ShowValue($value) {
//      if ($value)
//        $GLOBALS['renderer']->ShowTextValue('yes');
//      else
//        $GLOBALS['renderer']->ShowTextValue('no');
//    }
 
//    function ShowEditor($name,$value,$readonly) { 
//      $GLOBALS['renderer']->ShowBoolInput($name,
//                                          $value,
//                                          $readonly);
//    }
  
}

/**
 *  Single-line text values.
 */
class TextType extends Type {
  // var $babel = FALSE;

  /**********
  function SetBabel($b) {
     return $this->babel;
  }
  function GetLabel($b) {
     if ($this->babel) {
        return $this->label + ;
     } else return $this->label;
  }
  ****************/
  
  function to_sql($value) {
    if (strlen($value) == 0) return 'NULL';
    if (get_magic_quotes_gpc()) {
      return '"' . $value . '"';
    } else {
      return '"' . addslashes($value) . '"';
    }
  }
  
  function CanQuickFilter() {
    return TRUE;
  }
  
  function GetDefaultFormat() {
    return array(50);
  }
}

/**
 * DATE values.
 * Currently does not add anything at all.
 */
class DateType extends TextType {
  function GetDefaultFormat() {
    return array(10);
  }
}

/**
 * Numeric integer values. Currently does not add anything at all.
 */
class IntType extends TextType {
  function GetDefaultFormat() {
    return array(5);
  }
}

/**
 * AUTO_INCREMENT integer values.
 * Currently does not add anything at all.
 */
class AutoIncType extends IntType {
  function GetRefType() {
    return $GLOBALS['types'][TYPE_INT]; // new IntType(5);
  }
}


//  /**
//   *
//   * We can imagine many different subclasses of Type.  EMailAddress is
//   * currently just an idea. Not yet really used.
//   *
//   */
//  class EMailAddress extends TextType {

//    function GetJavaScript() {
//      return <<<EOD
//        function emailCheck(theForm)
//        { 
//          if (theForm.listmember_email.value.length < 7
//              || theForm.listmember_email.value.indexOf('@') < 1
//              || theForm.listmember_email.value.indexOf('.') < 1) { 
//            alert('Bitte geben Sie eine gueltige Emailadresse ein!'); 
//            theForm.listmember_email.focus(); 
//            return false; 
//          } 
//        }
//  EOD;
//    }
  
//    function ShowValue($value) {
//      echo ($GLOBALS['renderer']->GetUrlRef('mailto:'.$value,$value));
//    }
//  }



/**
 * Memos are texts with more than one line and which can contain
 * markup tags for formatting.
 * */
class MemoType extends TextType {
  // var $height;

//    function MemoType($width,$height) {
//      $this->TextType($width);
//      $this->height=$height;
//    }
//    function ShowEditor($name,$value,$readonly) { 
//      $GLOBALS['renderer']->ShowMemoInput($name,
//                                          $value,
//                                          $this->width,
//                                          $this->height,
//                                          $readonly);
    
//    }

//    function ShowValue($value) {
//      $GLOBALS['renderer']->ShowMemoValue($value);
//    }
  
  function IsVisible($query) {
    if ($query->depth == DEPTH_PAGE) return TRUE;
    return FALSE;
  }
  
  function GetDefaultFormat() {
    return array( 50, 4 );
  }
}

class QueryType extends Type {
  function GetDefaultFormat() {
    return array(DEPTH_TABLE);
  }
}



class RowType extends Type {
}





/**
 *
 *
 */
class Field {
  var $label;
  var $type;
  var $format;
  var $name;
  var $pickfunc;
  
  function Field(&$type,$format,$name,$label) {
    // assert('is_a($type,"type")');
    $this->type =& $type; // $GLOBALS['types'][$typeName];
    $this->format = $format;
    $this->label = $label;
    $this->name = $name;
  }
  
  function inspect() {
    echo ( 'Field instance {');
    inspect($this->type,'type');
    inspect($this->name,'name');
    echo ( '}');
  }
  
  function SetPickFunc($pickfunc) {
    $this->pickfunc = $pickfunc;
  }
  
//    function MakeColumn($alias,$isMaster,$label) {
//      return new FieldColumn($alias, $isMaster, $this, $label);
//    }

  function GetType() {
    return $this->type;
  }

  function IsVisible($query) {
    return $this->type->IsVisible($query);
  }

}

/**
 ** a JoinField is a pointer to a foreign table. If the foreign table
 ** has a complex primary key, then the join has one JoinField for
 ** each field of the primary key.
 **/
class JoinField extends Field {
  var $join;  // the referred (foreign) table

  function JoinField(&$join,$toField)
  {
    assert('is_a($join,"join")||inspect($join)');
    $this->join =& $join;
    $this->Field($join->toTable->fields[$toField]->type->GetRefType(),
                 $join->toTable->fields[$toField]->format,
                 $join->alias.'_'.$toField,
                 $join->GetLabel().'.'.$toField);
    
  }

  function inspect() {
    echo ( 'JoinField instance {');
    inspect($this->name,'name');
    inspect($this->join,'join');
    inspect($this->type,'type');
    echo ( '}');
  }
  
  function IsVisible($query) {
    if (!$query->IsEditing()) return FALSE;
    return $this->type->IsVisible($query);
  }
//    function MakeColumn($alias,$isMaster,$label) {
//      return new JoinFieldColumn($alias, $isMaster, $this, $label);
//    }

}

// an Action is a method to be executed on a row of a table
// concretely implemented as a php script

class Action {
  var $img = 'FormQuery.jpg';
  var $name; // name of the script to be called
  var $label;
  var $type;
  // var $cond; // whether this action is available or not
  
  function Action($name,$label) {
    $this->name = $name;
    $this->label = $label;
    // $this->cond = $cond;
    $this->type = new TextType(5);
  }
  
  function ShowImg() {
    echo ( '<img src="images/query/');
    echo ( $this->img);
    echo ( '" border=0 width=15 height=15>');
  }

  function ShowLink($query,$row) {
    trigger_error('not implemented',E_USER_ERROR);
//      echo ( '<a href="' . $this->name);
//      echo ( '?query=' . $query->id);
//      // echo ( '&sort=' . $HTTP_GET_VARS['sort']);
//      echo ( '&recno=' . ($query->recno));
//      /***********
//      if ($HTTP_GET_VARS['view'] == 'form') {
//        echo ( '&recno=' . ($query->recno));
//      } else {
//        echo ( '&view=form');
//        echo ( '&recno=' . ($query->recno));
//      }
//      **********/
//      echo ( '">');
//      $this->ShowImg();
//      echo ( '</a>';      ) 
  }

  function GetType() {
    return $this->type;
  }
}
  
// a Vurt is a virtual field in a table
// a value to be computed for each row
// by calling a PHP method
// (not by the SQL server)
class Vurt { 

  var $name; // the method to be called on each row
  var $type; // result type of method
  var $label; 

  function Vurt($type,$name,$label) {
    $this->type = $type;
    $this->name = $name;
    $this->label = $label;
  }

  function GetValueIn($query) {
    return call_user_func(
      array( &$query->view->leader,$this->name),
      $query);
  }

  function GetType() {
    return $this->type;
  }
}

class Detail {
  var $master;
  var $slaveTableName;
  // var $slaveKeys;
  var $name; // the method to be called on each row
  // var $type; // result type of method
  var $label;
  var $joinName;
  var $depth;
  
  function Detail(&$master,
                  $slaveTableName,
                  $joinName,
                  $label,
                  $depth
                  )
  {
    ToDebug("Detail()");
    $this->master = &$master; // ->GetPrimaryKey();
    $this->slaveTableName = $slaveTableName;
    $this->joinName = $joinName;
    
    // $this->type = new MemoType(3,40);
    $this->label = $label;
    $this->depth = $depth;
  }

  function inspect() {
    echo ( 'Detail instance {');
    // inspect($this->name,'name' );
    inspect($this->master,'master' );
    // inspect($this->slaveKeys,'slaveKey' );
    inspect($this->slaveTableName,'slaveTableName' );
    // inspect($this->query,'query' );
    echo ( '}');
  }
  

//    function SetLevel($level) {
//      $this->level = $level;
//    }


  
  function GetLabel() {
    return $this->label;
  }
}



class Join {
  var $toTable; // the referred (foreign) table
  var $alias; // alias of foreign table
  var $fields = array();
  var $label;
  
  function Join(&$toTable,$alias,$label) {
    $this->toTable =& $toTable;
    $this->alias = $alias;
    $this->label = $label;
  }

  function AddField(&$field) {
    $this->fields[] =& $field;
  }

  
  function inspect() {
    echo ( 'Join instance {');
    inspect($this->alias,'alias' );
    inspect($this->toTable->name,'toTable->name' );
    inspect($this->fields,'fields' );
    echo ( '}');
  }

  function GetLabel() {
    return $this->label;
  }
}



class Table {
  var $name;
  var $label;
  var $fields = array();
  var $actions = array();
  var $vurts = array();
  var $details = array();
  var $joins = array();  
  var $views = array();
  var $dbd;
  var $indexes = array();
  // var $moduleName;

  // function Table($moduleName,$name) {
  function DoDeclare(&$module,$name,&$dbd) {
    ToDebug("Table($name)");
    // $this->moduleName = $moduleName;
    $this->name = $name;
    $this->label = $name;
    $this->module =& $module;
    $this->dbd =& $dbd;
  }

  function SetupFields() {
  }
  
  function inspect() {
    echo ( "$this->name instance {");
    inspect($this->fields,'$this->fields');
    inspect($this->joins,'$this->joins');
    inspect($this->details,'$this->details');
    echo ( '} ');
  }
  

  
  function SetupMainQuery(&$query) {
    // override this to do things like
    // $query->order = ''
  }

  function SetupLinks() {}

  
  function AddTextVurt($name,$label,$width=40) {
    $v = new Vurt(TYPE_STRING,array($width),$name,$label);
    $this->vurts[] = $v;
    return $v;
  }
  
  function AddMemoVurt($name,$label,$width=40,$height=3) {
    $v = new Vurt(TYPE_MEMO,array($width,$height),$name,$label);
    $this->vurts[] = $v;
    return $v;
  }
  
  function AddAction($name,$label) {
    $a = new Action($name,$label);
    $this->actions[] = $a;
    return $a;
  }

  function &AddIntField($name,$label,$width=5) {
    $f = new Field($GLOBALS['types'][TYPE_INT],
                   array($width),$name,$label);
    return $this->AddField($f);
  }

  function &AddAutoIncField($name,$label,$width=5) {
    $f = new Field($GLOBALS['types'][TYPE_AUTO],
                   array($width),$name,$label);
    return $this->AddField($f);
  }

  function &AddBoolField($name,$label) {
    $f = new Field($GLOBALS['types'][TYPE_BOOL],
                   NULL,$name,$label);
    return $this->AddField($f);
  }
  
  function &AddMemoField($name,$label,$width=50,$height=3) {
    $f = new Field($GLOBALS['types'][TYPE_MEMO],
                   array($width,$height),
                   $name,$label);
    return $this->AddField($f);
  }
  

  function &AddStringField($name,$label,$width=50) {
    $f = new Field($GLOBALS['types'][TYPE_STRING],
                   array($width),$name,$label);
    return $this->AddField($f);
  }
  
  function &AddDateField($name,$label) {
    $f = new Field($GLOBALS['types'][TYPE_DATE],
                   array(10),$name,$label);
    return $this->AddField($f);
  }

  function AddBabelMemoField($name,$label,$width=50,$height=3) {
    if (count($GLOBALS['babelLangs']) > 1) {
      foreach ($GLOBALS['babelLangs'] as $lang) {
        $this->AddMemoField($name."_".$lang,$label,$width,$height);
      }
    } else {
      $this->AddMemoField($name,$label,$width,$height);
    }
  }
  
  function AddBabelStringField($name,$label,$width=50) {
    if (count($GLOBALS['babelLangs']) > 1) {
      foreach ($GLOBALS['babelLangs'] as $lang) {
        $this->AddStringField($name."_".$lang,$label,$width);
      }
    } else {
      $this->AddStringField($name,$label,$width);
    }
  }
  
  

  function SetLabel($label) {
    $this->label = $label;
  }
  
  function AddJoin($name,$label,&$toTable)
  {
    assert('is_subclass_of($toTable,"table")||inspect($toTable)');
    // echo ( $this->name);
    ToDebug( "$this->name.AddJoin($name,$label,$toTable->name)");

    $join = new Join($toTable,$name,$label);
    $this->joins[$name] =& $join;
    foreach ($toTable->GetPrimaryKey() as $key) {
      // $fld = $toTable->fields[$key];
      $f =& $this->AddField(new JoinField($join,
                                          $key));
//                                         ...$fld->type->GetRefType(),
//                                         ...$name.'_'.$key,
//                                         ...$label));
      $join->AddField($f);
    }
    
    
//      if (!is_null($toDetail)) {
//        $toTable->details[$toDetail] =
//          new Detail($toTable,$toDetail,
//                     $this,$name,'Detail');
//      }
    
  }

  function AddIndex($indexName,$columns) {
    $this->indexes[] = 'INDEX ' . $indexName . ' (' . $columns . ')';
  }

  function OnSinglePage($query) {
    $params = array(
                    'depth' => NULL,
                    'page' => NULL,
                    'pglen' => NULL
                    );
    ToSuperTitle($query->GetRef(NULL,$params));
  }
  
  function &AddField(&$f) {
    $this->fields[$f->name] =& $f;
    ToDebug($this->name . '.AddField ' . $f->name);
    return $f;
  }

  function AddDetail($name,
                     $slaveTableName,
                     $joinName,
                     $label,
                     $depth=DEPTH_REF)
  {
    ToDebug($this->name.".AddDetail($name,$slaveTableName,...)");
    $d = new Detail($this,$slaveTableName,$joinName,$label,$depth);
    $this->details[$name] = $d;
    // 20020607 $this->details[$name] =& $d;
    // ToDebug( "AddDetail($name,$slaveTableName,$slaveKey,$label)");
    // return $d;
  }


  function f_SetPickList($pickfunc) {
    // $f = $this->fields[];
  }

//    function InitDetails($query) {
//      ToDebug("Table($this->name).InitDetails()");
//      foreach (array_keys($this->details) as $key) {
//        $this->details[$key]->init($query);
//      }
//      inspect($this->details,'after details->init()');
//    }

  
  function GetPrimaryKey() {
    assert('isset($this->fields["id"])||print($this->name)');
    return array( 'id' );
  }

//    function FindField($fieldname) {
//      foreach($this->fields as $f) 
//        if ($f->name == $fieldname)
//          return $f;
//      trigger_error($fieldname
//                    . ' : no such field in '
//                    . $this->name,E_USER_ERROR);
//    }
  function FindAction($name) {
    foreach($this->actions as $a) 
      if ($a->name == $name)
        return $a;
    trigger_error($name . ' : no such action in '
                  .$this->name,E_USER_ERROR);
  }
  
  function FindVurt($name) {
    foreach($this->vurts as $v) 
      if ($v->name == $name)
        return $v;
    trigger_error($name . ' : no such vurt in '.$this->name,
                  E_USER_ERROR);
  }

//    function FindDetail($name) {
//      reset($this->details);
//      while (list($key, $d) = each ($this->details)) {
//        if ($key == $name)
//        $value->init();
//        // echo ( "Key: $key; Value:$value\n");
//      }
    
//      foreach($this->details as $d) 
//        if ($d->name == $name)
//          return $d;
//      trigger_error($name . ' : no such detail in '
//                    .$this->name,E_USER_ERROR);
//    }

  function &FindJoin($alias) {
    // trigger_error('TODO: foreach->reset/while?',E_USER_ERROR);
    foreach (array_keys($this->joins) as $key) {
      $join &= $this->joins[$key];
      if ($join->alias == $alias) return $join->table;
    }
    trigger_error($alias . ' : no such join in '. $this->name,
                  E_USER_ERROR);
  }

  // Table.Peek()
  function Peek($id,$columns='*') {
    return $this->dbd->Peek($this,$id,$columns);
  }

//    function SqlSelectFrom() {
//      $s = 'FROM ' . $this->name;
//      $sep = ',';
//      foreach ($this->joins as $join) {
//        // $join->AddSelectJoin($this,$s,$sep);
//        $s .= ' LEFT JOIN '
//          . $join->toTable->name;
//        if ($join->alias != $join->toTable->name) {
//          $s .= ' AS ' . $join->alias;
//        }
//        $rpk = $join->toTable->GetPrimaryKey();
//        $s .= ' ON (';
//        // $i = 0;
//        $sep = '';
//        foreach($join->fields as $i => $field) {
//          $s .= $sep
//            . $this->name . '.' . $field->name
//            . ' = '
//            . $join->alias . '.' . $rpk[$i];
//          // $i++;
//          $sep = ' AND ';
//        }    
//        $s .= ')';
//      }
//      return $s;
//    }


  function CreateRow() {
    $row = array();
    foreach($this->fields as $field) {
      $row[$field->name] = '';
    }
    $row['_new'] = TRUE;
    foreach($this->joins as $join) {
      $row[$join->alias] = $join->toTable->CreateRow();
    }
    return $row;
  }

  
  /**
   ** Table.GetRef()
   **/
  function GetRef($label=NULL,$params=NULL,$title=NULL) {
    if (is_null($label)) {
      $label = $this->GetLabel();
      // $label = 'foo';
    }
    if (is_null($params)) {
      $params=array();
    }
    $params['t'] = $this->name;
    global $renderer;
    return $renderer->GetUrlRef(MakeUrl("render.php",$params),
                                $label,
                                $title);
//      global $renderer;
//      return $renderer->GetUrlRef($url,$label,$title);
    
  }
  /*
    Table.GetPeekRef()
    show a link to an URL where ShowPage() will answer
  */
  function GetPeekRef($row,$label=NULL) {
    assert('is_array($row)||inspect($row)');
    $params = array('t'  => $this->name,
                    'depth'=> DEPTH_PAGE
                    );
    // $i = 0;
    $pkeys = $this->GetPrimaryKey();
    foreach($pkeys as $i => $pk) {
      $params['_'.$pk] = $row[$pk];
      // $i++;
    }
    if(is_null($label)) {
      $label = trim($this->GetRowLabel($row));
      if (strlen($label)==0) {
        $label = $this->name . ':xyz';
      }
//        }
    }
    global $renderer;
    return $renderer->GetUrlRef(MakeUrl("render.php",$params),$label);
  //    return ShowPeekRef($this->name,$id,$label);
  }


//    /**
//     ** called if a query with this as master table is going to display
//     ** the main page header...
//     **
//     **
//     **
//     **/
//    function OnStartOutput($query) {
//    }

  /**
   ** Table.ShowInPage() show the current row in the specified query
   ** (whose leader table is this) in "page" format
   **/
  // 20020729
  function ShowInPage($query,$first) {
//      if ($first) {
//        // echo '<p>(This is a generated standard form)<p>';
//      } else {
//        /* note: i think that i will disable completely the possibility
//           to have more than one rows in page view.*/
//        echo '<hr>';
//      }
    foreach($query->queryColumns as $i => $cell) 
      $cell->column->ShowAsItem($query,NULL,TRUE);
//        echo $cell->column->GetLabel(); // ShowColumnLabel($query,$i);
//        echo ( '&nbsp;: ');
//        if ($query->IsEditing()) {
//          $cell->column->ShowColEditor($query);
//        } else {
//          $cell->column->ShowValueIn($query);
//        }
//        echo ( '<br>');
//      }

    
//      $s = 'row ';
//      $sep = '';
//      foreach($this->GetPrimaryKey() as $pk) {
//        $s .= $sep . $query->row[$pk];
//        $sep = '.';
//      }
//      ToMargin($s . ' in '
//               . $query->view->leader->GetRef()
//               );
  }

  function ShowInList($query)
  {
    $sep = '';
    foreach($query->queryColumns as $qcol) {
      echo ( $sep . $qcol->column->GetLabel() . ': ');
      $qcol->column->ShowValueIn($query);
      $sep = ' &bull; ';
    }
    $query->ShowMore();
  }
  
  function ShowInShortList($query)
  {
    $label = $query->view->leader->GetRowLabel($query->row);
    $query->ShowMore($label);
  }
  
//    function ShowInForm($query) {
//      echo ( "\n".'<table width="100%" class="form">');
//      foreach($query->queryColumns as $cell) {
//        echo ( "\n".'<tr>');
//        echo ( "\n".'<td>' . $cell->column->GetLabel() . '</td>');
//        echo ( "\n".'<td>');
//        // if ($query->IsEditing()) {
//        $cell->column->ShowColEditor($query);
//        //          } else {
//        //            $col->Render($query);
//        //          }
//        echo ( '</td>');
//        echo ( '</tr>');
//        // }
//      }
//      echo ( "\n".'</table>');
//    }

  // return a string representing the current row
  function GetRowLabel($row) {
    $pk = $this->GetPrimaryKey();
    $s = $this->name . ':';
    $sep = '';
    foreach($pk as $k) {
      $s .= $sep . $row[$k];
      $sep = ',';
    }
    return $s;
  }

  /**
     Table.GetQueryLabel()
   */
  function GetQueryLabel($query) {
    ToDebug('Table.GetQueryLabel()');
    $s = $this->GetLabel();
    if (count($query->slices) != 0 ) {
      $sep = ' (';
      foreach($query->slices as $key => $value) {
        $col = $query->view->columns[$key]; // FindColumn($key);
        $s .= $sep . $col->label . '=' 
          . $col->GetValueLabel($value);
        $sep = ', ';
      }
      $s .= ')';
    }
    return $s;
  }

  /*
    Table.GetLabel()
   */
  function GetLabel() {
    return $this->label;
  }
  
  function &GiveView($viewName) {
    ToDebug("Table($this->name).GiveView($viewName)");
    if (isset($this->views[$viewName]))
      return $this->views[$viewName];
    $view = new View($this,$viewName);
    $this->views[$viewName] =& $view;
    return $view;
  }

  // default view to use when displaying records of this table
  // TODO : make use of parameter $format 
  function GetDefaultView($format=NULL) {
    return $this->name;
  }

}




class LinkTable extends Table {
  var $fromTable;
  var $toTable;

  function LinkTable($fromTableName,$parentDetailName,
                     $toTableName,$childDetailName)
  {
    ToDebug("function LinkTable($fromTableName,$toTableName)");
    $this->fromTable =& GetTable($fromTableName);
    $this->toTable =& GetTable($toTableName);
    $this->parentDetailName = $parentDetailName;
    $this->childDetailName = $childDetailName;
  }
  
  function GetPrimaryKey() {
    // TODO: support link to tables with complex primary key
    return array( 'p_id','c_id');
  }


  function SetupLinks()
  {
    $this->AddJoin('p','Parent',$this->fromTable);
    $this->AddJoin('c','Child',$this->toTable);

    $this->fromTable->AddDetail($this->parentDetailName,
                                // 'c'.$this->name,
                                $this->name,
                                'p',
                                $this->parentDetailName,
                                // GetLabel().' children',
                                DEPTH_SHORTLIST
                                );
    $this->toTable->AddDetail($this->childDetailName,
                              // 'p'.$this->name,
                              $this->name,
                              'c',
                              $this->childDetailName,
                              // $this->GetLabel() .' parents',
                              DEPTH_SHORTLIST
                              );
  }
  /*
    LinkTable.ShowInShortList()
   */
  function ShowInShortList($query)
  {
    if (isset($query->slices['p_id'])) {
      // $row = $query->joinRows['c'];
      $row = $query->row['c'];
      if (is_null($row)) return 'NULL';
      // $row = $query->GetJoinRow('c');
      $join = $this->joins['c'];
      // $label = $jf->join->toTable->GetRowLabel($row);
      // $id = array($query->row['c']);
      // echo ( $jf->join->toTable->GetPeekRef($id, $label));
      echo ( $join->toTable->GetPeekRef($row));
      return;
    }
    if (isset($query->slices['c_id'])) {
      // $row = $query->joinRows['p'];
      $row = $query->row['p'];
      if (is_null($row)) return 'NULL';
      // $row = $query->GetJoinRow('p');
      $join = $this->joins['p'];
//        // $label = $jf->join->toTable->GetRowLabel($query->joinRows[1]);
//        $label =
//          $jf->join->toTable->GetRowLabel($row);
//        // $label = $jf->table->GetRowLabel($query,'id1_');
//        // print_r($row);
//        $id = array($query->row['p']);
//        echo ( $jf->join->toTable->GetPeekRef($id,$label));
      echo ( $join->toTable->GetPeekRef($row));
      return;
    };
    parent::ShowInShortList($query);  
  }


}


class MemoTable extends Table {
  function SetupFields() {
    $this->AddBabelStringField('title','Title');
    $this->AddBabelMemoField('abstract','Abstract');
    $this->AddBabelMemoField('body','Body');
  }

  function ShowInList($query)
  {
    BeginSequence(SEQ_PAR,
                  $this->GetRowLabel($query->row));
    // echo ( '<b>');
    // echo ( $this->GetRowLabel($query->row));
    // echo ( '</b> : ');
    // $col = $query->view->FindColumn('abstract');
    // $col->ShowValueIn($query);
    $query->ShowCell('abstract');
    $query->ShowMore();
    EndSequence();
  }

  function ShowInPage($query,$first) {
    BeginSequence(SEQ_PAR,NULL,FALSE);
    $query->ShowCell('abstract');
    $query->ShowCell('body');
    EndSequence();

//      if (isset($query->row['id'])) {
//        ToMargin($query->GetRef($query->row['id'],
//                                array(
//                                      'depth'=>DEPTH_PAGE,
//                                      '_id' => $query->row['id']
//                                      )).'<br>');
    
//        ToMargin($query->GetRef('[edit]',
//                                array(
//                                      'depth'=>DEPTH_PAGE,
//                                      'edit' => 1,
//                                      '_id' => $query->row['id']
//                                      )));
//      } else {
//        ToMargin('(TODO: MemoTable::ShowInPage())');
//      }
  }
}

/**
   a MemoTable where each row additionally can have a "super" row in
   the same table. And consequently a list of rows who use this row as
   super row. The classical directory tree, here for MemoTable rows.

   SuperMemoTable subclasses currently don't support a complex primary
   key
   
 **/
class SuperMemoTable extends MemoTable {

  function SetupFields() {
    parent::SetupFields();
    $this->AddIntField('superSeq','Seq in Super');
    // $this->AddIndex('superSeq','superSeq');
  }
  
  function OnSinglePage($query) {
    // function ParentsToSuperTitle($query) {
    $parents = array();
    
    $superRow = $query->row['super'];
    // $superRow = $query->GetJoinRow('super');
    while (!is_null($superRow)) {
      // print_r($superRow);
      $label = $this->GetRowLabel($superRow);
      // insert item at the top of array
      array_unshift($parents,
                    $this->GetPeekRef($superRow,$label));
      $id = $superRow['super_id'];
      $superRow = $this->Peek(array($id));
    }
    foreach($parents as $item) {
      ToSuperTitle($item. ': ');
    }
  }
  
  function SetupMainQuery(&$query) {
    // echo 'foo';
    $query->order = 'id';
    $query->SetDepth(DEPTH_LIST);
    $query->SetFilter('ISNULL('.$this->name.'.super_id)');
  }
  
//    function SetupDetailQuery($master,&$detailQuery) {
//      ToDebug('SuperMemoTable.SetupDetailQuery()');
//      if ($master->depth == DEPTH_PAGE) {
//        if ($master->GetNestingLevel() < 2) {
//          // if ($GLOBALS['renderNestingLevel'] < 2) {
//          // if ($master->GetLevel() < 2)
//          $detailQuery->SetDepth(DEPTH_PAGE);
//        } else
//          $detailQuery->SetDepth(DEPTH_LIST);
//      } else
//        parent::SetupDetailQuery($master,$detailQuery);
//    }
  
  function ShowInPage($query,$first) {
    // if ($first) $this->ParentsToSuperTitle($query);
    parent::ShowInPage($query,$first);
    // FlushPageMargin();
    $query->ShowCell('superDetail',DEPTH_LIST);
  }
  
  function SetupLinks() {
    
    $this->AddJoin('super',
                   'Container',
                   $this);
    $this->AddDetail('superDetail',
                     $this->name,
                     'super',
                     'Contents');
  }
  
}




class Column {
  var $label;
  var $hidden = FALSE;
  
  function Column($label) {
    $this->label = $label;
  }
//    function ShowColumnLabel($query,$i) {
//      if ($GLOBALS['showJoinFields']) {
//        echo ( $this->GetEditorName() . "\n<br>");
//      }
//      echo ( $this->label);
//    }
  function IsQuickFilter() {
    return 0;
  }
  
  function IsEmpty($query) {
    return FALSE;
  }
  
  function IsVisible($query) {
    return TRUE; // return (!is_null($this->label));
  }

//    function InitRow($row) {
//      // Overridden by FieldColumn.
//    }

  /* Column.GetLabel() */
  function GetLabel() {
    return $this->label;
  }

  function GetValueLabel($value) {
    return $value;
  }

  function SetHidden($hidden) {
    $this->hidden = $hidden;
  }

//    function GetValue($query) {
//      return '';
//    }
  
  function canEdit($query) {
    return FALSE;
  }
  /**
   * IsReadOnly() should only return TRUE if canEdit() said TRUE and
   * now we want to veto the editability...
   */
  function IsReadOnly($query) {
    return FALSE;
  }
  
  function canSort($query) {
    return FALSE;
  }
//    function canSee($query) {
//      return TRUE;
//  //      return !isset($query->slices[$this->GetEditorName()]);
//  //      // return !$this->hidden;
//    }
  
  /**
   **
   ** The editor name is used for example to access a column them via
   ** ShowCell().
   ** 
  **/
  function GetEditorName() {
    // Overridden by subclasses who canEdit();
  }
  
  function GetSqlName() {
    return $this->GetEditorName();
  }
  
//    function ShowColEditor($query) {
//    }
  
  function GetValueIn($query) {
    $s = $query->row[$this->GetEditorName()];
    if (strlen($s)==0) return NULL;
    return $s; 
  }
  
  function SetValueIn(&$row,$value) {
    $row[$this->GetEditorName()] = $value;
  }

  /*
    Column.ShowValueIn()
   */
  function ShowValueIn($query) {
    // $value = $query->row[$this->GetEditorName()];
    $GLOBALS['renderer']->ShowColValue($this,
                                       $this->GetValueIn($query));
    // $this->field->type->ShowValue($this->GetValueIn($query));
  }
  
  function ShowAsItem($query,$format) {
    
    $value = $this->GetValueIn($query);

    BeginItem($this->GetLabel());

    $GLOBALS['renderer']->ShowColValue($this,
                                       $value,
                                       $format
                                       );
    EndItem();
  }
  
//      $GLOBALS['renderer']->ShowColAsItem($query,$this,$format);
//    }


//        echo $cell->column->GetLabel(); // ShowColumnLabel($query,$i);
//        echo ( '&nbsp;: ');
//        if ($query->IsEditing()) {
//          $cell->column->ShowColEditor($query);
//        } else {
//          $cell->column->ShowValueIn($query);
//        }
//        echo ( '<br>');
}
  
class FieldColumn extends Column {
  // var $index; // index of this column in result set
  var $field; // the field to represent
  var $alias;
  var $qfilter;
  // var $isMaster;
  
  function FieldColumn($alias,&$field,$label) { 
    // $this->index = $i;
    $this->field = $field; 
    // BUG 20020607 : $this->field =& $field; 
    $this->alias = $alias;
    $this->Column($label);
    // $type = $field->GetType();
    $this->qfilter = $field->type->CanQuickFilter();
    // $this->isMaster = $isMaster;
  }


  function inspect() {
    echo ( 'FieldColumn instance {');
    inspect($this->GetEditorName(),'GetEditorName()');
    inspect($this->field->name,'field->name');
    inspect($this->alias,'alias');
    // inspect($this->isMaster,'isMaster');
    echo ( '}');
  }

  function sql_where($colname,$op,$value) {
    return $colname . $op . $this->field->type->to_sql($value);
  }

  function canSort($query) {
    return TRUE;
  }
  
  
  function IsQuickFilter() {
    return $this->qfilter;
  }
//    function InitRow($row) {
//      $row[$this->GetSqlName()] = '';
//    }

  /* FieldColumn.GetLabel() */
//    function GetLabel() {
//      return $this->label;
//    }
  
  function GetSqlName() {
    // if (is_null($this->alias)) return $this->field->name;
    return $this->alias . '.' . $this->field->name;
  }
  
//    function GetValueIn($query) {
//      $s = $query->row[$this->field->name];
//      if (strlen($s)==0) return NULL;
//      // if ($this->isMaster)
//      return $s
//  //      $row = $query->GetJoinRow($this->alias);
//  //      return $row[$this->field->name];
//    }
  
  function GetEditorName() {
    // if ($this->isMaster)
    return $this->field->name;
    // return $this->alias . '_' . $this->field->name;
    
    // if (is_null($this->alias)) return $this->field->name;
    // return $this->alias . '_' . $this->field->name;
  }
  
//    function canSee($query) {
//      if ($GLOBALS['showJoinFields']) return TRUE;
//      return $this->isMaster;
//    }
  
  function canEdit($query) {
    // if (!$this->isMaster) return FALSE;
    return TRUE;
  }

  function IsVisible($query) {
    // if (is_null($this->label)) return FALSE;
    return $this->field->IsVisible($query);
  }
  
  function IsReadOnly($query) {
    $pkeys = $query->view->leader->GetPrimaryKey();
    foreach($pkeys as $pk) {
      if ($this->field->name == $pk)
        if (! $query->row['_new'])
          return TRUE;
    }
    return FALSE;
  }
  
//    function sql_dump() { // toSQL() {
//      $s = '"F", '
//        . '"' . $this->alias . '", '
//        . '"' . $this->field->name . '", '
//        . '"' . $this->label . '" '
//        . $this->qfilter;
//      return $s;
//    }

//    // FieldColumn.ShowColEditor
//    function ShowColEditor($query) {
//      $value = $this->GetValueIn($query);
//      // $value = $query->row[$this->GetEditorName()];
//      $this->field->type->ShowEditor(
//        $this->GetEditorName() . '[]',
//        $value,
//        $this->IsReadOnly($query)
//      );
//    }


  

//    function ShowColumnLabel($query,$i) {
       
//      if ($GLOBALS['showJoinFields']) {
//        echo ( $this->GetEditorName() . "\n<br>");
//      }
//      // if ($query->IsMainComponent() && !$query->IsSingleRow()) {
//      if ($query->depth == DEPTH_TABLE) {
//        echo ( $query->GetRef($this->label,array('sort'=>$i)));
//      } else
//        echo ( $this->label);
//    }
  
  function GetType() {
    return $this->field->type;
  }
}

class JoinColumn extends Column {

  var $join;
  // var $type;

  function JoinColumn(&$join) {
    $this->Column($join->GetLabel());
    $this->join =& $join;
    // $this->type = new MemoType(40,3);
  }
  
  function inspect() {
    echo ( 'JoinColumn instance {');
    inspect($this->GetEditorName(),'GetEditorName()');
    inspect($this->join->toTable->name,'join->toTable->name');
    inspect($this->label,'label');
    echo ( '}');
  }

  function sql_where($colname,$op,$value) {
    $s = '(';
    $sep = '';
    foreach($this->join->toTable->GetPrimaryKey() as $i => $pk) {
      $field = $this->join->toTable->fields[$pk];
      $s .= $sep
        . $colname . '_' . $pk
        . $op
        . $field->type->to_sql($value[$i]);
      $sep = ' AND ';
    }
    $s .= ')';
    return $s;
  }

  function GetType() {
    return $GLOBALS['types'][TYPE_ROW];
  }
  
//    function GetType() {
//      return $this->type;
//    }
  
  /**
   ** the value of a JoinColumn is a row 
   **/
  function GetValueIn($query) {
    ToDebug('JoinColumn.GetValueIn()');
    // return $query->joinRows[$this->join->alias];
    return $query->row[$this->GetEditorName()];
    // return $query->GetJoinRow($this->join->alias);
//      $row = $query->GetJoinRow($this->alias);
//      $a = array();
//      foreach($this->field->join->toTable->GetPrimaryKey() as $pk) {
//        $a[] = $row[$pk];
//      }
//      return $a;
  }

//    function GetLabel() {
//      return $this->join->alias;
//    }
  
  function GetEditorName() {
    return $this->join->alias;
  }
  
  /*
    JoinColumn.ShowValueIn()
   */
  function ShowValueIn($query) {
    $row = $this->GetValueIn($query);
    // $id = $query->row[$this->field->name];
//      if (strlen($id) == 0) {
//        echo ( 'NULL');
//        return;
//      }
    
    // $id is the foreign key.

    // $row = $query->GetJoinRow($this->join->alias);
    
    // I let the foreign table decide how to display it:
    // $label = $this->join->toTable->GetRowLabel($row);

    // GetPeekRef
    if (is_null($row)) return 'NULL';
    echo ( $this->join->toTable->GetPeekRef($row));

  }
  
  function GetValueLabel($value) {
    ToDebug('JoinColumn.GetValueLabel()');
    //    if (strlen($value) == 0) {
//        return 'NULL';
//      }
//      // return 'okay...';
    $row = $this->join->toTable->Peek($value);
    return $this->join->toTable->GetRowLabel($row);
  }

//    // JoinColumn.ShowColEditor
//    function ShowColEditor($query) {
//      ToDebug('JoinColumn.ShowColEditor()');
//  //      $value = $this->GetValueIn($query);
//  //      // $value = $query->row[$this->GetEditorName()];
//  //      $this->field->type->ShowEditor(
//  //        $this->GetEditorName() . '[]',
//  //        $value,
//  //        $this->IsReadOnly($query)
//  //      );
//      echo ( 'TODO:JoinColumn::ShowColEditor()');
//    }
  
  /*
    JoinColumn.ShowValueIn()
    hier muss doch eigentlich ein Link zur Pageview gemacht werden?
  */
  function ShowValueIn($query) {
    ToDebug('JoinColumn.ShowValueIn()');
    $row = $this->GetValueIn($query);
    if (!is_null($row))
      echo ( $this->join->toTable->GetPeekRef($row));
//      foreach($this->join->toTable->GetPrimaryKey()
//              as $i => $pk) {
//        $type = $this->join->toTable->fields[$pk]->type;
//        $type->ShowValue($value[$i]);
//      }
  }
  
  function IsVisible($query) {
    // if (is_null($this->label)) return FALSE;
    if (!$query->IsEditing()) return TRUE;
    return FALSE;
  }
  
}


class VurtColumn extends Column {
  
  var $vurt;
  
  function VurtColumn($vurt) {
    $this->vurt = $vurt;
    $this->Column($vurt->label);
  }
  
//    function sql_dump() { // toSQL() {
//      $s = '"V", '
//        . 'NULL,'
//        . '"' . $this->vurt->name . '", '
//        . '"' . $this->label . '" '
//        . NULL;
//      return $s;
//    }

  /*
    VurtColumn.ShowValueIn()
   */
  function ShowValueIn($query) {
    echo $this->vurt->GetValueIn($query);
  }
  

  
  function GetType() {
    return $this->vurt->GetType();
  }
  
  function GetEditorName() {
    // return 'V_' . $this->vurt->name;
     return $this->vurt->name;
  }
  
}

class DetailColumn extends Column {
  
  var $detail;
  // var $query;
  var $name;
  
  function DetailColumn($name,&$detail) {
    ToDebug('DetailColumn()');
    $this->detail =& $detail;
    $this->name = $name;
    $this->Column($detail->GetLabel());
  }
  
  function inspect() {
    echo ( 'DetailColumn instance {');
    inspect($this->GetEditorName(),'GetEditorName()');
    inspect($this->detail,'detail');
    inspect($this->label,'label');
    echo ( '}');
  }
//    function sql_dump() { // toSQL() {
//      $s = '"D", '
//        . 'NULL,'
//        . '"' . $this->detail->name . '", '
//        . '"' . $this->label . '" '
//        . NULL;
//      return $s;
//    }

  /*
    DetailColumn.ShowValueIn()
   */
  function GetValueIn(&$masterQuery)
  {
    ToDebug("DetailColumn.GetValueIn()");
    $query = new Query($this->detail->slaveTableName);
    $query->SetCaller($masterQuery);
    
    $query->SetDepth($this->detail->depth);
    
    foreach($this->detail->master->GetPrimaryKey() as $i => $pk) {
      $query->SetSlice( $this->detail->joinName . '_' . $pk,
                        $masterQuery->row[$pk]
                        );
    }


    if ($masterQuery->depth == DEPTH_PAGE) {
      if ($masterQuery->GetNestingLevel() < 2) {
        $query->SetDepth(DEPTH_PAGE);
      } else {
        $query->SetDepth(DEPTH_TABLE);
      }
//      } elseif ($masterQuery->depth == DEPTH_SHORTLIST) {
//        $query->page = 1;
//        $query->pagelength = 5;
    }

    return $query;
    
//      if ($masterQuery->depth == DEPTH_PAGE && !is_null($this->label))
//        BeginSection($this->GetLabel());
//      // $masterQuery->master->SetupDetailQuery($masterQuery,$query);
//      $query->Render();
//      if ($masterQuery->depth == DEPTH_PAGE && !is_null($this->label))
//        EndSection();
    
  }
  
  function ShowAsItem($query,$format) {
    if ($format == DEPTH_PAGE || $format == DEPTH_TABLE) {
      BeginSection($this->GetLabel());
      $GLOBALS['renderer']->ShowColValue($this,
                                         $this->GetValueIn($query)
                                         );
      EndSection();
    }
    else
      parent::ShowAsItem($query,$format);
//        $GLOBALS['renderer']->ShowColAsItem($query,$this,
//                                            $format );
  }
  
//    // DetailColumn.ShowColEditor
//    function ShowColEditor($query) {
//      $this->ShowValueIn($query);
//    }
  
  
  function GetType() {
    return $GLOBALS['types'][TYPE_QUERY];
    // return $this->detail->GetType();
  }
  
  function GetEditorName() {
    // trigger_error('Detail.GetEditorName()');
    return $this->name;
  }

  /**
     DetailColumn.IsVisible()
   */
  function IsVisible($query) {
    if ($query->IsEditing()) return FALSE;
    // if (! parent::canSee($query)) return FALSE;
    if ($query->depth <= DEPTH_LIST) return FALSE;
    return TRUE;
    // TODO : visibility
  }
}

class ActionColumn extends Column {
  var $action;
  
  function ActionColumn($action) {
    $this->action = $action;
    $this->Column($action->label);
  }

  /*
    ActionColumn.ShowValueIn()
   */
  function ShowValueIn($query) {
    return $this->action->ShowLink($query);
  }
  
//    // ActionColumn.ShowColEditor
//    function ShowColEditor($query) {
//      return $this->action->ShowLink($query);
//    }
  
  function GetType() {
    return $this->action->GetType();
  }
  
}



class View {
  var $columns = array();
  var $name;

  var $label = NULL; // '(no title)';
  var $filter;
  
  function View(&$leader,$name=NULL) {
    ToDebug("new View($leader->name,$name)");
//      if (strlen($name) == 0)
//        trigger_error('you specified an empty view name',E_USER_ERROR);

    $this->name = $name;
    $this->leader =& $leader;
    $this->label = $leader->GetLabel();
    if (is_null($name)) {
      $this->CreateDefaultView($leader);
    } else {
      $this->LoadView($leader,$name);
    }
  }
  
  function inspect() {
    echo ('View instance {<ul>');
    echo ('<li>'); inspect($this->leader,'leader');
    echo ('<li>'); inspect($this->name,'name');
    echo ('<li>'); inspect($this->columns,'columns');
    echo ('</ul>}');
  }

  function GetName() {
    if (is_null($this->name)) return '(*'.$this->leader->name.')';
    return $this->name;
  }

  
  //    $this->pagelength = $HTTP_GET_VARS['pglen'];
  function LoadView(&$master) {
    trigger_error('change 2002-07-03 not supported');
//      $row = sql_peek('QUERIES','id="' . $this->name . '"');
//      if (!is_null($row)) {
//        $this->label = $row['label_en'];
//        // $this->pagelength = $row['pglen'];
//        if (strlen($row['filter'])>0) {
//          $this->filter = $row['filter'];
//        }
//        // mysql_result($result,0,'label_en');
      
//        $s = 'SELECT * FROM QRYCOLS'
//          . ' WHERE query="'
//          . $this->name
//          . '" ORDER BY seq';
//        $result = sql_select($s);
//        // echo (($s));

//        $i=0;
//        while($row = mysql_fetch_array($result,MYSQL_ASSOC)) {
//          // while($row = mysql_fetch_row($result)) {
//          $i++;
//          // print_r($row);
//          switch ($row['coltype']) {
//          case 'A':
//            $action = $master->FindAction($row['fieldname']);
//            $col = new ActionColumn($action);
//            break;
//          case 'V':
//            $vurt = $master->FindVurt($row['fieldname']);
//            $col = new VurtColumn($vurt);
//            break;
//          case 'D':
//            $detail =& $master->details[($row['fieldname'])];
//            $col =& new DetailColumn($row['fieldname'],$detail,$this);
//            break;
//          case 'F':
//            $alias = $row['alias'];
//            if ($alias == $master->name) {
//              $table = $master;
//              $isMaster = TRUE;
//            } else {
//              $table =& $master->FindJoin($alias);
//              $isMaster = FALSE;
//            }
//            $f =& $table->fields[$row['fieldname']];
//            $col = $f->MakeColumn($alias,$isMaster,$row['label_en']);
//            break;
//          default:
//            trigger_error($row['coltype'].' : bad column type',
//                          E_USER_ERROR);
//          }
//          // if ($row['visible']==1) { }
//          $this->columns[] = $col;
//        }
//      }
    
  }

//    function QrySave() {
//      echo ( 'Saving Query ' . $this->name . '...');
//      echo ( '<ol>');
//      $s = 'UPDATE QUERIES'
//        . ' SET '
//        . ' label_en = "' . $this->label . '"'
//        . ' WHERE name = "' . $this->name . '"';
//      echo ( '<li>');
//      echo ( $s);
//      sql_query($s);
//      // mysql_query($s) or die('Invalid query:' . $s);
    
//      $s = 'DELETE FROM QRYCOLS'
//        . ' WHERE query = "' . $this->name . '"';    
//      echo ( '<li>');
//      echo ( $s);
//      sql_query($s);
//      // mysql_query($s) or die('Invalid query:' . $s);


//      $seq = 1;
//      foreach ($this->columns as $col) {
//        $s = 'INSERT INTO QRYCOLS'
//          . ' (query,seq,coltype,tablename,fieldname,label_en)'
//          . ' VALUES ('
//            . '"' . $this->name . '", '
//            . $seq . ', '
//            . $col->sql_dump() 
//            . ')';
//        echo ( '<li>');
//        echo ( $s);
//        sql_query($s);
//        // mysql_query($s) or die('Invalid query:' . $s);
//        $seq ++;
        
//      }
//      echo ( '</ol>');
//      echo ( 'The query parameters have been saved.');

//      // echo ( '[<a href="show.php?query='.$this->id.'">Show</a>]');
//      echo ( '[<a href="show.php">Show</a>]');
    
//    }


  /**
   ** View.FindColumn()
   **
   **
   **/
  function &FindColumn($name) {
    foreach(array_keys($this->columns) as $colKey) {
      $col =& $this->columns[$colKey];
      if ($col->GetEditorName() == $name) return $col;
    }
    trigger_error($name . ' : no such column in '. $this->GetName(),
                  E_USER_ERROR);
  }


  function CreateDefaultView(&$table) {
    ToDebug("View.AddAllColumns($table->name)");
    foreach(array_keys($table->fields) as $key) {
      $f =& $table->fields[$key];
      $label = $f->label;
      $col = new FieldColumn($table->name,
                             $f,
                             $label);      
      $this->columns[$key] = $col;
    }
//      foreach($table->actions as $a) {
//        $this->columns[] = new ActionColumn($a);
//      }
//      foreach($table->vurts as $v) {
//        $this->columns[] = new VurtColumn($v);
//      }
    foreach(array_keys($table->joins) as $joinKey) {
      $join =& $table->joins[$joinKey];
      $this->columns[$joinKey] = new JoinColumn($join);
//        foreach(array_keys($join->toTable->fields) as $fieldKey) {
//          $f =& $join->toTable->fields[$fieldKey];
//          $this->columns[] =
//            $f->MakeColumn($join->alias,
//                           FALSE,
//                           $join->toTable->name.'->'.$f->label);
//        }
    }
    foreach(array_keys($table->details) as $key) {
      $col = new DetailColumn($key,$table->details[$key]);
      $this->columns[$key] = $col;
      // assert('is_ref($detail,$col->detail)');
    }
    // echo ( "<p>inspect($table->name):");
    // inspect($table,'<p>$table in AddAllColumns()');
    // print_r($this->columns);
  }

  function SetLabel($label) {
     $this->label = $label;
  }
  
  /* View.GetLabel() */
  function GetLabel() {
    ToDebug('View.GetLabel()');
    return $this->label;
  }

}



class QueryColumn {
  var $column;
  var $format;
  
  function QueryColumn(&$column,$format=NULL) {
    assert('is_a($column,"column")||inspect($column)');
    $this->column =& $column;
    if (is_null($format)) {
      // inspect($column,'*');
      $type = $column->GetType();
      $this->format = $type->GetDefaultFormat();
    } else {
      $this->format = $format;
    }
    // $this->format = $column->GetDefaultFormat();
  }

  function GetFormat() {
    return $this->format;
  }

}


class Query {
  var $pagelength = 10;
  var $view;
  var $editingRows;
  var $orderby = NULL;
  var $page=1;
  // var $rowcount = NULL;
  // var $recno; // current record
  var $depth = DEPTH_TABLE;
  var $slices = array();
  var $queryColumns;
  var $isEditing = FALSE;  
  var $row;  // the current row in leader table
  // var $joinRows; // array of current rows in joined tables
  var $caller = NULL; // the query to restore when Close()
  var $qfilter = NULL;
  var $filter = NULL;
  var $append = FALSE;
  // var $master;
  var $caller;
  var $showDetails = 1;
  var $label;

  function Query($leaderTableName) // , $viewName=NULL)
  {
    ToDebug("new Query($leaderTableName)");
    global $HTTP_SESSION_VARS;
    $this->leader =& GetTable($leaderTableName);
//      if (is_null($viewName)) {
//        $viewName = $this->master->GetDefaultView();
//        // ToDebug($view->name);
//      }
//      $this->view =& $this->master->GiveView($viewName);
  }

  function SetCaller(&$caller) {
    $this->caller =& $caller;
  }

  function SetLabel($label) {
    $this->label = $label;
  }

  function SetView($name) {
    $this->view = new View($this->leader,$name);
  }

  /**
   ** Setup() can be called more than one time, but only the first
   ** time will actually do the setup.
   **/
  function Setup() {
    if (isset($this->queryColumns)) return;
//      $this->leader->SetupQuery($this);
    if (!isset($this->view))
      $this->view = new View($this->leader);
    $this->queryColumns = array();
    foreach($this->view->columns as $name => $col) {
      assert('is_a($col,"column")||inspect($col)');
      if ($col->IsVisible($this)) {
        $this->queryColumns[] =
          new QueryColumn($this->view->columns[$name]);
      }
    }
  }

  function SetColumnList($colNames) {
    if (!isset($this->view))
      $this->view = new View($this->leader);
    $this->queryColumns = array();
    if (is_array($colNames)) {
      foreach($colNames as $name) {
        $col =& $this->view->columns[$name];
        $this->queryColumns[]
          = new QueryColumn($col);
      }
    } else {
      for($i=0;$i<func_num_args();$i++) {
        $name = func_get_arg($i);
        $col =& $this->view->columns[$name];
        if (is_null($col)) {
          trigger_error($name.': no such column in view '
                        . $this->view->GetName());
        }
        $this->queryColumns[]
          = new QueryColumn($col);
      }
    }
  }

  function inspect() {
    echo ( "Query instance {");
    // inspect($this->leader->name,'$this->leader->name');
    inspect($this->view,'$this->view');
    // inspect($this->view->name,'$this->view->name');
    // inspect($this->rowcount,'$this->rowcount');
    inspect($this->slices,'$this->slices');
    // inspect($this->rngval,'$this->rngval');
    if(isset($this->row))
      inspect($this->row,'$this->row');
    echo ( '} ');
  }
  
  function GetDefaultDetailDepth() {
    return $GLOBALS['defaultDetailDepth'][$this->depth];
  }

  function GetNestingLevel() {
    $i = 1;
    $p = $this->caller;
    while (! is_null($p)) {
      $p = $p->caller;
      $i++;
    }
    return $i;
  }

  function GetPageLength() {
    // if ($this->view == 'form') return 1;
    return $this->pagelength;
  }

//    function GetShowDetails() {
//      // if ($this->format == QRYFORMAT_PAGE) return 2;
//      return $this->showDetails;
//    }

//    function SetSingleRow() {
//      $this->isSingleRow = TRUE;
//    }
  
  function IsSection() {
    // return ! $this->IsSingleRow();
    // return $this->IsMainComponent();// && ! $this->IsPageFormat();
    if (!$this->IsMainComponent()) return FALSE;
    // && ! $this->IsSingleRow();
    if ($this->pagelength == 1 && $this->depth == DEPTH_PAGE)
      // if ($this->result->rowcount == 1 && $this->depth == DEPTH_PAGE)
      return FALSE;
    return TRUE;
  }

  function IsSinglePage() {
    return $this->result->rowcount != 0 && $this->pagelength == 1;
    // return $this->isSingleRow || $this->pagelength == 1;
  }
  
  function IsPageFormat() {
    return ($this->depth == DEPTH_PAGE);
//      if ($this->format == QRYFORMAT_PAGE) return 1;
//      if ($this->format == QRYFORMAT_FORM) return 1;
//      return 0;
  }

  function SetSlice($colName,$value) {
    // echo $colName . "=". print_r($value);
    $this->slices[$colName] = $value;
    $this->HideColumn($colName);
  }

  function GetColIndex($colName) {
    $this->Setup();
    // $i = 0;
    foreach($this->queryColumns as $i => $cell) {
      if ($cell->column->GetEditorName() == $colName)
        return $i;
    }
    return -1;
    // trigger_error($colName);
  }

  function HideColumn($colName) {
    $i = $this->GetColIndex($colName);
    if ($i != -1)
      unset($this->queryColumns[$i]);
    // array_delitem($this->queryColumns,$i);
    // $col =& $this->view->columns[$colName];
    // $col->SetHidden(TRUE);
  }
  
//    function SetRngKey($colnames) {
//      ToDebug("SetRngKey($colnames)");
//      $this->rngkey = array();
//      foreach ($colnames as $colname) {
//        $this->rngkey[] =& $this->master->fields[$colname];
//        $col =& $this->view->FindColumn($colname);
//        $col->SetHidden(TRUE);
//        // $this->rngkey[] =& $this->view->FindColumn($colname);
//      }
//    }
//    function SetRngVal($values) {
//      $this->rngval = $values;
//  //      $this->rngval = array();
//  //      foreach ($values as $value) {
//  //        $this->rngval[] = $value;
//  //      }
//    }

  function SetFilter($filter) {
    $this->filter = $filter;
  }
  
  function SetLabel($label) {
    $this->label = $label;
  }
  
  function SetDepth($depth) {
    $this->depth = $depth;
  }
  
  function SetAppend($append) {
    $this->append = $append;
  }
  
//    function SetFormat($format) {
//      switch ($format) {
//      case QRYFORMAT_TABLE:
//        $this->renderer = new TableRenderer();
//        break;
//      case QRYFORMAT_COMMALIST:
//        $this->renderer = new CommaListRenderer();
//        break;
//  //      case QRYFORMAT_LINK:
//  //        $this->renderer = new LinkRenderer();
//  //        break;
//      case QRYFORMAT_PLIST:
//        $this->renderer = new ParListRenderer();
//        break;
//      case QRYFORMAT_UL:
//        $this->renderer = new BulletListRenderer();
//        break;
//      case QRYFORMAT_PAGE:
//        $this->renderer = new PageRenderer();
//        $this->view->pagelength = 1;
//        break;
//      case QRYFORMAT_FORM:
//        $this->renderer = new FormRenderer();
//        $this->view->pagelength = 1;
//        break;
//      default:
//        ToDebug($HTTP_GET_VARS['format'] . ' : unknown format');
//      }
//    }

  function IsMainComponent() {
    // if (is_null($this->caller)) return TRUE;
    // inspect($this->caller,'$this->caller');
    return is_null($this->caller);
    // return $this->isMainComponent;
//      global $HTTP_SESSION_VARS;
//      $q = $HTTP_SESSION_VARS['query'];
//      if (is_null($q)) return FALSE;
//      if ($q == $this) return TRUE;
//      return FALSE;                       
//      // return ($HTTP_SESSION_VARS['query'] =& $this;
  }
  
  function SetPage($page) {
    if ($page != $this->page) {
      $this->page = $page;
    }
  }

  /**
    Query.GetUrlToSelf()
    
    show a link to a page where this query would be executed.
   */
  function GetUrlToSelf($changeParams=NULL) {
    // echo $this->depth;
    $params = array(
                    't' => $this->leader->name,
                    'page' => $this->page,
                    'pglen' => $this->pagelength,
                    'depth' => $this->depth,
                    );
    if (!is_null($this->filter))
      $params['filter'] = $this->filter;
    if (!is_null($this->view->name)) 
      $params['v'] = $this->view->name;
    
    foreach ($this->slices as $col => $value) {
      $params['_' . $col] = $value;
    }
    if (!is_null($changeParams)) {
      foreach($changeParams as $k=>$v) {
        $params[$k] = $v;
      }
    }
    return MakeUrl('render.php',$params);
  }

  /**
   ** Query.GetRef()
   **/
  function GetRef($label=NULL,$changeParams=NULL,$title=NULL) {
    // echo $this->depth;
    if (is_null($label)) {
      $label = $this->GetLabel();
      // $label = 'foo';
    }
    $url = $this->GetUrlToSelf($changeParams);
    return $GLOBALS['renderer']->GetUrlRef($url,$label,$title);
    
  }


    // echo ( '<font size="-5">' . $s . '</font>');
    // echo ( ' (' . $this->rowcount . ' rows selected)');
  
//    function &GetRenderer() {
//      global $htmlRenderers,$HTTP_GET_VARS;
//      if (isset($HTTP_GET_VARS['xml']))
//        return new XmlRenderer();
//      else
//        return $htmlRenderers[$this->format];
//    }

//    function CreateRow() {
//      $this->row = $this->master->CreateRow();
//      // $this->joinRows = array();
//      foreach($this->master->joins as $join) {
//        $this->row[$join->alias]
//          = $join->toTable->CreateRow();
//      }
//    }

  function insert_row() {
    $row = $this->leader->CreateRow();
    // $row = $this->CreateRow();
    foreach($this->queryColumns as $i => $qcol) {
      $value = func_get_arg($i);
      // inspect($value,'value');
      // Fatal error: func_get_arg(): Can't be used as a function parameter
      $qcol->column->SetValueIn($row,$value);
//        $row[$qcol->column->GetEditorName()]
//          = func_get_arg($i);
    }
    // inspect($row,'row');
    $this->leader->dbd->sql_commit_row($this->leader,$row);
  }

//    function GetJoinRow($alias) {
//      $i = 0;
//      foreach($this->leader->joins as $join) {
//        if ($join->alias == $alias) {
//          return $this->joinRows[$i];
//        }
//        $i++;
//      }
//      trigger_error($alias.' : no such join alias in '
//                    . $this->leader->name,
//                    E_USER_ERROR);
//    }

  function ShowMore($label='[more]') {
    $params = array(
                    'depth' => DEPTH_PAGE,
                    'page' => $this->result->recno,
                    'pglen' => 1
                    // ,'filter' => NULL
                    );
    echo ( $this->GetRef($label,$params));
  }

  function CanEdit() {
    return ($this->depth >= DEPTH_TABLE);
//      if ($this->format == QRYFORMAT_TABLE) return TRUE;
//      return FALSE;
  }

//    function GetLevel() {
//      return $GLOBALS['level']; // this->level;
//    }
                       

    
  /**
    Query.Render()
   */
  function Render() {
    // $GLOBALS['renderNestingLevel']++;
    ToDebug('Query.Render()');
    // ToDebug('GetLabel() : '. $this->GetLabel());
    
    $this->Setup();
    
    global $renderer; 

    $this->result = $this->leader->dbd->OpenQuery($this);

    if ($this->isEditing) {
      $this->editingRows = array();
    }
    
    $first = TRUE;
    
    $renderer->ShowQueryHeader($this);
    if ($this->depth >= DEPTH_SHORTLIST) {
      while($this->leader->dbd->fetch_row($this,$this->result)) {
        $renderer->ShowQueryRow($this,$first);
        if ($this->isEditing) {
          $this->editingRows[] = $this->row;
        }
        $first = FALSE;
      }
    }
    if ($this->depth >= DEPTH_TABLE) {
      if ($this->isEditing) {
        $this->row = $this->leader->CreateRow();
        $renderer->ShowQueryRow($this,$first);
        $this->editingRows[] = $this->row;
      }
    }
    $renderer->ShowQueryFooter($this);
    // echo 'rows';
  }

  function HasMore() {
    return ($this->result->recno < $this->result->rowcount);
  }

  function GetCellValue($colName) {
    ToDebug('Query.GetCellValue()');
    $col = $this->view->FindColumn($colName);
    return $col->GetValueIn($this);
  }
  
  /**
   ** shortcut : if you know that the column is a join, then don't use
   ** GetCellValue() but GetJoinValue(). That's more efficient...
   **/
//    function GetJoinValue($alias) {
//      return $this->joinRows[$alias];
//    }
  
  /**
   ** shortcut : if you know that the column is a field in the leader
   ** table, then don't use GetCellValue() but GetFieldValue(). That's
   ** more efficient...
   **/
  function GetFieldValue($name) {
    return $this->row[$name];
  }

  /**
     Query.ShowCell()

     renders the value of the specified column in current row
   */
  function ShowCell($name,$format=NULL) {
    ToDebug("ShowCell($name)");
    $col = $this->view->FindColumn($name);
    $col->ShowAsItem($this,$format);
  }

  function SetColumnHidden($name,$hidden=TRUE) {
    // ToDebug("ShowCell($name)");
    $col =& $this->view->FindColumn($name);
    $col->SetHidden($hidden);
  }
  

  function IsEditing() {
    return $this->isEditing;
  }




  /* Query.GetLabel() */
  function GetLabel() {
    if (!is_null($this->label)) return $this->label;
    return $this->leader->GetQueryLabel($this);
  }

  
//    /*
//      Query.UpdateUsingPOST
//     */
//    function UpdateUsingPOST() {
//      ToDebug('UpdateUsingPOST()');
//      global $HTTP_POST_VARS;
//      $i = 0;
//      // $rows = $this->GetRows();
//      assert('is_array($this->editingRows)');
//      foreach($this->editingRows as $row) {
//        $sep = '';
      
//        $this->row = $row; /* because canEdit() or other methods need the
//                              current row. */
      
//  //        if ($row['_new']) {
//  //          $sql = 'INSERT INTO '
//  //            . $this->leader->name
//  //            . '(';
        
//  //          foreach($this->view->columns as $col) {
//  //            $name = $col->GetEditorName();
//  //            if (isset($HTTP_POST_VARS[$name])) {
//  //              $sql .= $sep . $name; // $col->GetSqlName();
//  //              $sep = ', ';
//  //            }
//  //          }
//  //          $sql .=  ')'
//  //            . ' VALUES (';
//  //        } else {
//  //          $sql = 'UPDATE ' . $this->leader->name . ' SET ';
//  //        }
//        $changed = 0;
//        // $sep = '';
//        foreach($this->queryColumns as $cell) {
//          // if ($col->canSee($this)) {
//            $name = $cell->column->GetEditorName();
//            if ($cell->column->canEdit($this)) { 
//              $type = $cell->column->GetType();
//              $newvalue = $HTTP_POST_VARS[$name][$i];
//  //              if ($row['_new']) {
//  //                $sql .= $sep . $type->to_sql($newvalue);
//  //              } else {
//  //                $sql .= $sep . $name // col->GetEditorName()
//  //                  . ' = '
//  //                  . $type->to_sql($newvalue);
//  //              }
//  //              $sep = ', ';
//              if ($row[$name] != $newvalue) {
//                $row[$name] = $newvalue;
//                $changed++;
//              }
//            }
//            // }
//        }
//        if ($changed > 0 || $row['_new']) {
//  //          if ($row['_new']) {
//  //            $sql .= ')';
//  //          } else {
//  //            $pkeys = $this->master->GetPrimaryKey();
//  //            $sql .= ' WHERE ';
//  //            $sep = '';
//  //            foreach($pkeys as $pk) {
//  //              $type = $this->master->fields[$pk]->type;
//  //              $sql .= $sep . $pk . ' = '
//  //                . $type->to_sql($row[$pk]);
//  //              $sep = ' AND ';
//  //            }
//  //          }
//  //          // echo ( "\n<p>");
//  //          // echo ( $sql);
//          $this->master->dbd->sql_commit_row($this->master,$row);
        
//        }
//        $i++;
//      }
//      // echo ( 'Updating : done');
//      // $this->editingRows = array();
//      // $this->Render();
//    }

}


//  class Link {
//    var $fromTable;
//    var $fromDetail;
//    var $toTable;
//    var $toDetail;
//    var $lnkView;

//    function Link($lnkView,
//                  $fromTable,$fromDetail,
//                  $toTable,$toDetail)
//    {
//      $this->lnkView =& GetView($lnkView);
//      $this->fromTable =& LoadTable($fromTable);
//      $this->toTable =& LoadTable($toTable);
//      $this->fromDetail = $fromDetail;
//      $this->toDetail = $toDetail;
//    }
//  }



//  class LnkType {
//    var $table1;
//    var $table2;
//    var $label;
  
//    function LnkType($id) {
//      $row = sql_peek('LNKTYPES',"id = $id");
//      $this->table1 = GetTable($row['table1']);
//      $this->table2 = GetTable($row['table2']);
//      $this->label = $row['label_en'];
//    }
//  }


//  function &GetLnkType($id) {
//    global $HTTP_SESSION_VARS;
//    if (isset($HTTP_SESSION_VARS['lnktypes'][$id])) {
//      return $HTTP_SESSION_VARS['lnktypes'][$id];
//    } else {
//      $t = new LnkType($id);
//      $HTTP_SESSION_VARS['lnktypes'][$id] =& $t;
//    }
//  }



//  function &GetView($name) {
//    global $HTTP_SESSION_VARS;
//    // echo ( '$name = ';  print_r($name));
//    if (isset($HTTP_SESSION_VARS['views'][$name])) {
//      return $HTTP_SESSION_VARS['views'][$name];
//    }
//    $view =& new View($name);
//    $HTTP_SESSION_VARS['views'][$name] =& $view;
//    return $view;
//  }

//  function &GetTable($name) {
  
//    if (strlen($name)==0) 
//      trigger_error('table name is empty',E_USER_ERROR);
  
//    global $HTTP_SESSION_VARS;
//    if (isset($HTTP_SESSION_VARS['tables'][$name])) {
//      return $HTTP_SESSION_VARS['tables'][$name];
//    }
    
//    // LogMsg('Instanciating table : ' . $name);
//    $x = 'return new ' . $name . '(\'' . $name . '\');';
//    ToDebug('eval('.$x.')');
//    $table = eval($x);
//    if (is_null($table)) 
//      trigger_error($name . ' : no such table',E_USER_ERROR);
  
//    $HTTP_SESSION_VARS['tables'][$name] =& $table;
  
//    $table->init();
  
//    return $table;
  
//  }


//  function ShowButtonRef($ref,$label,$title=NULL)
//  {
//    echo ( '&nbsp;[<a href="'
//      . $ref
//      . '"');
//    if (isset($title)) {
//      echo ' title="'
//        . htmlspecialchars($title)
//        . '"';
//    }
//    echo '>' . $label .'</a>]&nbsp;';
//  }

//  function linkto($viewname,$label=NULL) {
//    if ($label == NULL) {
//      $view = GetView($viewname);
//      $label = $view->GetLabel();
//    }
//    return '<a href="show.php?view=' . $viewname
//      . '">' . $label . '</a>';
//  }

class Result {
  var $handle;
  var $rowcount;
  var $recno = 0;
}



class Module {

  function DeclareTable($tableName,$table,$dbd=NULL) {
    if (is_null($dbd)) {
      $dbd = $GLOBALS['dbd'];
    }
    $table->DoDeclare($this,$tableName,$dbd);
    $table->SetupFields();
    global $HTTP_SESSION_VARS;
    $HTTP_SESSION_VARS['app']->tables[$tableName] = $table;
  }
  
  function SetupTables() {}
  function SetupLinks() {}

  function AddLink( $fromTableName,
                    $joinName,
                    $fromLabel,
                    $toTableName,
                    $toTableDetail=NULL,
                    $toLabel=NULL)
  {
    
    ToDebug("AddLink($fromTableName,,...,$toTableName,...)");
    global $HTTP_SESSION_VARS;
    $fromTable =& GetTable($fromTableName);
    $toTable =& GetTable($toTableName);
    
    $fromTable->AddJoin($joinName,
                        $fromLabel,
                        $toTable);
    if (!is_null($toTableDetail)) {
      $toTable->AddDetail($toTableDetail,
                          $fromTableName,
                          $joinName,
                          $toLabel);
    }
  }
}

function TableExists($name) {
  return isset($GLOBALS['HTTP_SESSION_VARS']['app']->tables[$name]);
}

function &GetTable($name) {
  if (!TableExists($name))
    trigger_error("$name : no such table");
  return $GLOBALS['HTTP_SESSION_VARS']['app']->tables[$name];
}

function DeclareModule($name,&$module) {
  global $HTTP_SESSION_VARS;
  $HTTP_SESSION_VARS['app']->modules[$name] =& $module;
}

class Application {
  var $tables = array();
  var $modules = array();

  function init() {
    ToDebug('<h2>SetupTables...</h2>');
    foreach($this->modules as $modName=>$notused) {
      ToDebug('<p>'.$modName.'->SetupTables()...');
      $this->modules[$modName]->SetupTables();
    }
    
    ToDebug('<h2>SetupLinks...</h2>');
    foreach($this->modules as $modName=>$notused) {
      ToDebug('<p>'.$modName.'->SetupLinks()...');
      $this->modules[$modName]->SetupLinks();
    }
    
    ToDebug('<h2>Setup Tables...</h2>');
    // global $HTTP_SESSION_VARS;
    // $tables =& $HTTP_SESSION_VARS['tables'];
    foreach(array_keys($this->tables) as $key) {
      assert('!is_null($this->tables[$key])||inspect($key)');
      $this->tables[$key]->SetupLinks();
    }

    if (TRUE) {
      ToDebug('<h2>Assert Tables...</h2>');
      foreach($this->tables as $table) {
        $pkeys = $table->GetPrimaryKey();
        foreach($pkeys as $pk) {
          assert('isset($table->fields[$pk])||inspect(array($table,$pk))');
        }
      }
    }
    
  }
  
}

/*
  LoadModule() is normally called from init_session.php
  
  example : LoadModule('CRM') will (1) instanciate the CRM module (a
  singleton instance of a class with name 'CRM' which should extend
  class 'Module'), (2) define a global variable $CRM for easy
  reference to this instance in scripts and (3) store a reference into
  $HTTP_SESSION_VARS['modules'] so that we have a global list of all
  modules.

*/

// $modNames = array();

//  function ProvidesModule($name) {
//    ToDebug("function LoadModule($name)");
//    global $modNames;
//    $modNames[] = $name;
//  }



//  function do_GET_OpenQuery() {
//    global $HTTP_GET_VARS,$HTTP_SESSION_VARS;
  
//    $module = $GLOBALS[$HTTP_GET_VARS['m']];
//    $tableName = $HTTP_GET_VARS['t'];

//    $x = 'return $module->' . $tableName .';';
//    $table = eval($x);

//    if (isset($HTTP_GET_VARS['v'])) {
//      $query = $table->CreateQuery($HTTP_GET_VARS['v']);
//      // $view = $table->GiveView($HTTP_GET_VARS['v']);
//    } else {
//      $query = $table->CreateQuery();
//      // $view = $table->GiveView($table->GetDefaultView());
//    }

//    // $query = new Query($view); 

//    $query->do_GET();
  
//  }

//  function do_GET_This() {
//    global $HTTP_GET_VARS,$HTTP_SESSION_VARS;
//    $query =& $HTTP_SESSION_VARS['query'];
//    if (is_null($query)) LocationIndex();
//    $query->do_GET();
//  }



//  function GetRequestedQuery() {
    
//    ToDebug('GetRequestedQuery()');

//    global $HTTP_GET_VARS, $HTTP_SESSION_VARS;
//    if (isset($HTTP_GET_VARS['v'])) {
//      $query = new Query($HTTP_GET_VARS['t'],$HTTP_GET_VARS['v']);
//    } else {
//      $query = new Query($HTTP_GET_VARS['t']);
//    }

//    $query->isMainComponent = TRUE;

//    if (isset($HTTP_GET_VARS['pglen'])) {
//      $query->pagelength = $HTTP_GET_VARS['pglen'];
//    }
  
//    if (isset($HTTP_GET_VARS['sd'])) {
//      $query->showDetails = $HTTP_GET_VARS['sd'];
//    }
    
//    if (isset($HTTP_GET_VARS['page']))
//      $query->SetPage($HTTP_GET_VARS['page']);
  
//    if (isset($HTTP_GET_VARS['sort'])) {
//      $col = $query->view->columns[$HTTP_GET_VARS['sort']];
//      ToDebug('sort set to '. $col->GetEditorName());
//      $query->orderby = $col->GetEditorName();
//    }


//    if (isset($HTTP_GET_VARS['qfilter'])) 
//      $query->qfilter = $HTTP_GET_VARS['qfilter'];
    
//    if (isset($HTTP_GET_VARS['filter'])) 
//      $query->SetFilter($HTTP_GET_VARS['filter']);
    
//    if (isset($HTTP_GET_VARS['rngkey'])) {
//      $query->SetRngKey($HTTP_GET_VARS['rngkey']);
//      $query->SetRngVal($HTTP_GET_VARS['rngval']);
//      // $query->rngkey = $HTTP_GET_VARS['rngkey'];
//      // $query->rngval = $HTTP_GET_VARS['rngval'];
//    }
    
//  //      if (isset($HTTP_GET_VARS['edit']))
//  //        $query->editing = $HTTP_GET_VARS['edit'];
      
//    if (isset($HTTP_GET_VARS['id'])) {
//      $query->rngkey =& $query->master->GetPrimaryKey();
//      $query->SetRngVal($HTTP_GET_VARS['id']);
//      // $query->SetSingleRow();
//    }

//    if (isset($HTTP_GET_VARS['recno'])) {
//      $query->recno = $HTTP_GET_VARS['recno'];
//      if ($query->GetPageLength() != 0) {
//        $query->page =
//          intval($query->recno / $query->GetPageLength()) +1;
//      }
//    }

//    $query->master->SetupMainQuery($query);
//    // $query->Setup();
    
//    if (isset($HTTP_GET_VARS['edit'])) {
//      $query->isEditing = ($HTTP_GET_VARS['edit'] == 1);
//    }
//    if (isset($HTTP_GET_VARS['append'])) {
//      $query->SetAppend($HTTP_GET_VARS['append']);
//    }
//    if (isset($HTTP_GET_VARS['depth'])) {
//      // $query->SetFormat($HTTP_GET_VARS['depth']);
//      $query->SetDepth($HTTP_GET_VARS['depth']);
//    }

//  //    if ($query->IsSingleRow()) {
//  //      $query->format = QRYFORMAT_PAGE;
//  //    }
      
  
//    // if (isset($HTTP_GET_VARS['fcols'])) {
//    //   $query->fcols = $HTTP_GET_VARS['fcols'];
//    // }
  
  
//    return $query;
//  }




/*
  returns TRUE if the two variables refer to the same thing.
  
  source : http://www.digiways.com/articles/php/smartcompare/
  
  original name was comparereferences(&$a, &$b), but i prefer
  is_ref()...
 */

function is_ref(&$a, &$b)
{
  // creating unique name for the new member variable
  $tmp = uniqid("");
  // creating member variable with the name $tmp in the object $a
  $a->$tmp = true;
  // checking if it appeared in $b
  $bResult = !empty($b->$tmp);
  // cleaning up
  unset($a->$tmp);
  return $bResult;
}


function MakeUrl($url,$params) {
  $sep = "?";
  foreach($params as $k=>$v) {
    if (!is_null($v)) {
      if (is_array($v)) {
        // note : array keys are lost
        foreach($v as $i) {
          $url .= $sep . $k . '[]=' . $i;
          $sep = "&";
        }
      } else {
        $url .= $sep . $k . '=' . $v;
      }
      $sep = "&";
    }
  }
  return $url;
}


 

?>
