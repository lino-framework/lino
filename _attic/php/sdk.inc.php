<?php



//  class API extends MemoTable {
//    function SetupFields() {
//      parent::init();
//      $this->AddStringField('id','ID');

//      $this->SetLabel('API');
//    }

//    function SetupMainQuery(&$query) {
//      $query->order = 'id';
//      $query->SetDepth(DEPTH_LIST);
//    }
  
//    function GetRowLabel($row) {
//      return $row['id'] . ' : ' . $row['title'];
//    }

//  }

//  class API2API extends LinkTable {
  
//    function SetupFields() {
//      parent::init('API','API');
//      // $this->link();
//    }
//  }



class FILES extends MemoTable {
  function SetupFields() {
    parent::SetupFields();
    $this->AddStringField('id','ID');

    $this->SetLabel('Files');
  }

  function SetupMainQuery(&$query) {
    $query->order = 'id';
    $query->SetDepth(DEPTH_TABLE);
  }
  
//    function GetRowLabel($row) {
//      return 'file ' . $row['id'];
//    }
  function GetRowLabel($row) {
    return $row['id'];
  }
}

class CLASSES extends SuperMemoTable {
  function SetupFields() {
    parent::SetupFields();
    $this->AddStringField('id','ID');

    $this->SetLabel('Classes');
  }

//    function SetupMainQuery(&$query) {
//      $query->order = 'id';
//      $query->SetDepth(DEPTH_LIST);
//    }
  
  function GetRowLabel($row) {
    return $row['id'];
  }
}

class METHODS extends MemoTable {
  function SetupFields() {
    parent::SetupFields();
    $this->AddStringField('name','Name');

    $this->SetLabel( 'Methods');
  }

  function GetPrimaryKey() {
    return array( 'class_id', 'name');
  }

  function SetupMainQuery(&$query) {
    $query->order = 'class_id,name';
    $query->SetDepth(DEPTH_LIST);
  }
  
  function GetRowLabel($row) {
    return $row['class_id'].'::'.$row['name'] . '()';
  }
}



class CHANGES extends MemoTable {
  function SetupFields() {
    parent::SetupFields();
    $this->AddAutoIncField('id','ID');
    $this->AddDateField('date','Date');
    
    // $this->AddBoolField('salesVisible','sales');
    // $this->AddBoolField('userVisible','user');
    // $this->AddBoolField('adminVisible','admin');
    
    $this->SetLabel('Changes');
  }

  function SetupMainQuery(&$query) {
    $query->order = 'date desc';
    $query->SetDepth(DEPTH_TABLE);
  }
  
  function SetupMainQuery(&$q) {
    $q->order = 'date,id DESC';
    $q->depth = DEPTH_LIST;
  }
  
  function GetRowLabel($row) {
    $s = $row['date'];
    if (strlen($row['title']) > 0) 
      $s .= '. ' . $row['title'];
    return $s;
  }

  // 20020729

//    function ShowInPage($query,$first) {
//      // ShowTitle($query->master->GetRowLabel($query->row));
//      echo '<p>';
//      if (strlen($query->row['date']) > 0) {
//        $query->ShowCell('date');
//        echo '. ';
//      }
//      if (strlen($query->row['author_id']) > 0) {
//        echo 'By ';
//        $query->ShowCell('author');
//        echo '. ';
//      }
//      if (strlen($query->row['version_release']) > 0) {
//        echo 'Version: ';
//        $query->ShowCell('version');
//        echo '.';
//      }
//      echo '</p>';
//      parent::ShowInPage($query,$first);
//  //      $query->ShowCell('abstract');
//  //      echo '<p>';
//  //      $query->ShowCell('body');
//    }
}

class FILES2CHANGES extends LinkTable {
  
  function FILES2CHANGES() {
    $this->LinkTable('FILES','changes',
                     'CHANGES','files');
  }
}

class VERSIONS extends Table {
  
  function SetupFields() {
    $this->AddIntField('major','Maj');
    $this->AddIntField('minor','Min');
    $this->AddIntField('release','Rel');
    // $this->AddStringField('title','Title');
    $this->AddDateField('date','release date');
    // $this->AddDateField('stopDate','Date stopped');
    $this->SetLabel('Versions');
  }

  function GetPrimaryKey() {
    return array('major','minor','release');
  }
  
//    function ShowInPage($query,$first) {
//      echo '<p>';    
//      $query->ShowCell('id');
//      echo ' : ';    
//      $query->ShowCell('title');
//      echo ' : ';    
//      $query->ShowCell('date');
    
//      $query->ShowCell('changes');
//      // $query->ShowMore();
//    }

  function GetRowLabel($row) {
    // return 
    return 'Version '
      . $row['major']
      . '.' . $row['minor']
      . '.' . $row['release'];
  }

}




  
class SDK extends Module {
  
  function SetupTables() {
    $this->DeclareTable('FILES',new FILES());
    $this->DeclareTable('CLASSES',new CLASSES());
    $this->DeclareTable('METHODS',new METHODS());
    $this->DeclareTable('CHANGES',new CHANGES());
    $this->DeclareTable('VERSIONS',new VERSIONS());
  }
  
  function SetupLinks() {
    $this->AddLink('CLASSES','file','Defined in',
                   'FILES','classes','Classes');
    $this->AddLink('CLASSES','super','Extends',
                   'CLASSES','superDetail','SubClasses');
    $this->AddLink('METHODS','class','Class',
                   'CLASSES','methods','Methods');
    
//      AddLink('CHANGES','project','Project',
//              'PROJECTS','changes','Changes by Project');
    
    $this->AddLink('CHANGES','version','since Version',
                   'VERSIONS','changes','Changes by Version');
    
    $this->AddLink('PROJECTS','version','scheduled for',
                   'VERSIONS','projects','scheduled Projects');
    
    $this->AddLink('CHANGES','author','Author',
                   'PERSONS','changes','Changes by Author');
    
  }
}

?>
