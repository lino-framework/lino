<?php

class DBITEMS extends SuperMemoTable {
  function SetupFields() {
    parent::SetupFields();
    $this->AddStringField('id','ID');
    
    // $this->AddAutoIncField('seq','Seq');

    $this->SetLabel('DocBook items');
    // $this->AddIndex('seq','seq');
  }

  function SetupMainQuery(&$query) {
    // echo 'DBITEMS';
    // parent::SetupMainQuery($query);
    $query->SetLabel('DocBooks');
    $query->SetDepth(DEPTH_LIST);
    $query->order = 'superSeq';
    if (count($query->slices)==0)
      $query->SetFilter('ISNULL('.$this->name.'.super_id)');
  }

  function GetRowLabel($row) {
    return $row['title'];
  }

//    function ShowInList($query)
//    {
//      if (strlen($query->row['title']) > 0) {
//        echo '<b>';
//        echo $query->row['title'];
//        echo '</b>. ';
//      }
//      echo $query->row['abstract'];
//      // $query->ShowMore();
//    }

  /**
   ** move the current item up within the list of its siblings.
   **/
  function MoveUp($mySeq,$mySuper) {
    // $mySeq = $query->row['seq'];
    // $mySuper = $query->row['super'];
    $myNewSeq = NULL;

    $sql = 'SELECT * FROM DBITEMS WHERE super = ' . $mySuper
      . ' AND seq < ' . $mySeq;
    $result = sql_select($sql);
    // in fact i need only the last row
    while ($row = mysql_fetch_array($result,MYSQL_ASSOC)) {
      $myNewSeq = $row['seq'];
    }
    if (is_null($myNewSeq)) {
      ToUserLog('This is the top-most element of its list!');
      return;
    }
    $this->SwapSiblings($mySuper,$mySeq,$myNewSeq);
  }

  function SwapSiblings($super,$s1,$s2) {
    $peek = sql_peek('DBITEMS',
                     'super = '. $super,
                     'MAX(seq),*' );
    if ($peek ==NULL) {
      ToUserLog('Sorry... aborting SwapSiblings()');
      return FALSE;
    }
    $tmpSeq = 1 + $peek[0];
    $seqType = $this->fields['seq']->type;
    if (! sql_update('DBITEMS',
                     'super = ' . $super . ' AND seq = ' . $s1,
                     array(array('seq' =>
                                  $seqType->to_sql($tmpSeq))
                           )
                     )) return FALSE;
    if (! sql_update('DBITEMS',
                     'super = ' . $super . ' AND seq = ' . $s2,
                     array(array('seq' =>
                                 $seqType->to_sql($s1)))
                     )) return FALSE;
    if (! sql_update('DBITEMS',
                     'super = ' . $super . ' AND seq = ' . $tmpSeq,
                     array(array('seq' =>
                                 $seqType->to_sql($s2)))
                     )) return FALSE;
    return TRUE;
//      $a = array();
//      $a[] = 'UPDATE DBITEMS SET seq = ' . $tmpSeq
//        . ' WHERE super = ' . $super
//        . ' AND seq = ' . $s1;
//      $a[] = 'UPDATE DBITEMS SET seq = ' . $s1
//        . ' WHERE super = ' . $super
//        . ' AND seq = ' . $s2;
    
//      $a[] = 'UPDATE DBITEMS SET seq = ' . $s2
//        . ' WHERE super = ' . $super
//        . ' AND seq = ' . $tmpSeq;
    
//      return sql_update($a);
  }

}

class DBI2DBI extends LinkTable {
  
  function DBI2DBI() {
    $this->LinkTable('DBITEMS','seeAlso',
                     'DBITEMS','seenAlsoFrom');
  }
}

class TOPICS extends Table {
  function SetupFields() {
    $this->AddIntField('id','ID');
    $this->AddStringField('name_en','Topic');

    $this->SetLabel('Topics');
  }

  function GetRowLabel($row) {
    return $row['name_en'];
  }
}

class TOPIC2TOPIC extends LinkTable {
  
  function TOPIC2TOPIC() {
    $this->LinkTable('TOPICS','superTopics',
                     'TOPICS','subTopics');
  }
}



  
class DOCBOOK extends Module {
  
  function SetupTables() {
    $this->DeclareTable('TOPICS',new TOPICS());
    $this->DeclareTable('DBITEMS',new DBITEMS());
    
    $this->DeclareTable('DBI2DBI',new DBI2DBI());
    $this->DeclareTable('TOPIC2TOPIC',new TOPIC2TOPIC());
  }
  
//    function SetupLinks() {
//      $this->AddLink('DBITEMS','super','Container',
//                     'DBITEMS','superDetail','Contents'); 
//    }
  
}


?>
