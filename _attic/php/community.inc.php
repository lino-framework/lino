<?php


class NEWS extends MemoTable {
  function SetupFields() {
    parent::SetupFields();
    $this->AddAutoIncField('id','ID');

    $this->AddDateField('date','Date');
//      $this->AddStringField('title','Title');
    
//      $this->AddMemoField('abstract','Abstract');
//      $this->AddMemoField('body','Body');
    
    $this->SetLabel('News');
  }

  function SetupMainQuery(&$q) {
    $q->order = 'date,id DESC';
    $q->depth = DEPTH_LIST;
  }
  
  function GetRowLabel($row) {
    $s = $row['title'];
    if (strlen($s) == 0)
      $s = $row['date'];
    else
      $s .= ' (' . $row['date'] . ')';
    return $s;
  }

//    function ShowInList($query)
//    {
//      if (strlen($query->row['date']) > 0) {
//        echo '<b>';
//        $query->ShowCell('date');
//        echo '</b>. ';
//      }
//      if (strlen($query->row['title']) > 0) {
//        echo '<b>';
//        $query->ShowCell('title');
//        echo '</b>. ';
//      }
//      $query->ShowCell('abstract');
//      $query->ShowMore();
//    }

  function ShowInPage($query,$first) {
    $query->ShowCell('date');
    $query->ShowCell('author');
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
//      echo '</p>';
    parent::ShowInPage($query,$first);
  }
}

class NEWSGROUPS extends Table {

  function SetupFields() {
    $this->AddStringField('id','ID');
    $this->AddStringField('name','Name');
    $this->SetLabel( 'News Groups');
  }

  
  function GetRowLabel($row) {
    return $row['name'] .' ('.$row['id'].')';
  }

}

class PROJECTS extends MemoTable {
  
  function SetupFields() {
    parent::SetupFields();
    $this->AddAutoIncField('id','ID');
    $this->AddDateField('date','Date started');
    $this->AddDateField('stopDate','Date stopped');
    $this->AddTextVurt('StatusText','Status');
    $this->SetLabel('Projects');
  }
  // 20020729
//    function ShowInPage($query,$first) {
//      if ($query->GetNestingLevel() < 2) {
//        echo '<blockquote>';
//        echo  '<p>Project ID : ' . $query->row['id'];
//        if (strlen($query->row['sponsor_id']) > 0) {
//          echo '<p>Sponsor: ';
//          $query->ShowCell('sponsor');
//          echo '</p>';
//        }
//        if (strlen($query->row['date']) > 0) {
//          echo 'started: ';    
//          $query->ShowCell('date');
//          if (strlen($query->row['stopDate']) > 0) {
//            echo ' (stopped: ';    
//            $query->ShowCell('stopDate');
//            echo ')';
//          } else {
//            echo ' (active)';    
//          }
//        } else {
//          echo '(not started)';
//        }
//        echo '</blockquote>';
//        echo '<p>';
//      }
//      parent::ShowInPage($query,$first);
//      $query->ShowCell('news');
//    }

  function StatusText($query) {
    $s = '';
    if (strlen($query->row['date']) > 0) {
      $s = 'started: '
        . $query->row['date'];
      if (strlen($query->row['stopDate']) > 0) {
        $s .= ' (stopped: '
          . $query->row['stopDate']
          .')';
      } else {
        $s = ' (active)';    
      }
    } else {
      $s = '(not started)';
    }
    return $s;
  }

  function GetRowLabel($row) {
    // return 
    return $row['title'];
  }

}

//  class PRJ2PRJ extends LinkTable {
  
//    function PRJ2PRJ() {
//      $this->LinkTable('PROJECTS','PROJECTS');
//      // $this->link();
//    }
//  }

class COMMUNITY extends Module {
  function SetupTables() {
    $this->DeclareTable('NEWS',new NEWS());
    $this->DeclareTable('NEWSGROUPS',new NEWSGROUPS());
    $this->DeclareTable('PROJECTS',new PROJECTS());
    
    $this->DeclareTable('PRJ2PRJ',
                        new LinkTable('PROJECTS','seeAlso',
                                      'PROJECTS','seeAlsoBack'));
    $this->DeclareTable('NEWS2NEWSGROUPS',
                        new LinkTable('NEWS','groups',
                                      'NEWSGROUPS','news'));
  }
  
  function SetupLinks() {
    // global $ADDRBOOK;
    $this->AddLink('NEWS','author','Author',
                   'PERSONS','news','News by Author');

    
    $this->AddLink('NEWS','project','Project',
                   'PROJECTS','news','News by Project');
    $this->AddLink('NEWS','lang','Language',
                   'LANG');
    $this->AddLink('PROJECTS','sponsor','Sponsor',
                   'ORG','projects','Projects by Sponsor');
    $this->AddLink('PROJECTS','responsible','Responsible',
                   'PERSONS','projects','Projects by Responsible');

  }
}

?>
