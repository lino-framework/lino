INSERT INTO FILES (body, abstract, id, title) VALUES (NULL, NULL, "datadict.inc.php", "Data Dictionary");
INSERT INTO FILES (body, abstract, id, title) VALUES (NULL, NULL, "lino.inc.php", "Lino main include file");
INSERT INTO FILES (body, abstract, id, title) VALUES (NULL, NULL, "html.inc.php", "HTML rendering");
INSERT INTO FILES (body, abstract, id, title) VALUES (NULL, "Instantiates a Query, translates the URL parameters to Query
settings, then renders this query.
", "render.php", "render the specified query");
INSERT INTO CLASSES (body, super_id, file_id, title, abstract, id) VALUES (NULL, NULL, "datadict.inc.php", "Base class for data type descriptors", NULL, "Type");
INSERT INTO CLASSES (body, super_id, file_id, title, abstract, id) VALUES (NULL, "Type", "datadict.inc.php", "type-specific methods for values of type CHAR or VARCHAR", NULL, "TextType");
INSERT INTO CLASSES (body, super_id, file_id, title, abstract, id) VALUES (NULL, "Type", "datadict.inc.php", "type-specific methods for values of type INT or BIGINT", NULL, "IntType");
INSERT INTO CLASSES (body, super_id, file_id, title, abstract, id) VALUES (NULL, "TextType", "datadict.inc.php", "type-specific methods for values of type TEXT", NULL, "MemoType");
INSERT INTO CLASSES (body, super_id, file_id, title, abstract, id) VALUES (NULL, NULL, "datadict.inc.php", "A named set of columns on a master table", "Views are the part of a query
which can be modified and saved.
A View contains an ordererd set of columns.
A View is valid for one known master table.
", "View");
INSERT INTO CLASSES (body, super_id, file_id, title, abstract, id) VALUES (NULL, NULL, "datadict.inc.php", "Query", NULL, "Query");
INSERT INTO CLASSES (body, super_id, file_id, title, abstract, id) VALUES (NULL, NULL, "datadict.inc.php", "a field in a Table", NULL, "Table");
INSERT INTO CLASSES (body, super_id, file_id, title, abstract, id) VALUES (NULL, NULL, "datadict.inc.php", "a field in a Table", NULL, "Field");
INSERT INTO CLASSES (body, super_id, file_id, title, abstract, id) VALUES (NULL, NULL, "datadict.inc.php", "a field in a Table", NULL, "Detail");
INSERT INTO CLASSES (body, super_id, file_id, title, abstract, id) VALUES (NULL, NULL, "datadict.inc.php", "a reference to another Table", "Represents the fact that this table is linked to another table. 
Each Join in a table will be translated to SQL by a \"LEFT JOIN\"
clause.
Each Join will create automatically one or more [ref
CLASSES:JoinField] instances.
", "Join");
INSERT INTO CLASSES (body, super_id, file_id, title, abstract, id) VALUES (NULL, NULL, "datadict.inc.php", "(abstract) the element of a View", NULL, "Column");
INSERT INTO CLASSES (body, super_id, file_id, title, abstract, id) VALUES (NULL, "Column", "datadict.inc.php", "a column representing a Field", NULL, "FieldColumn");
INSERT INTO CLASSES (body, super_id, file_id, title, abstract, id) VALUES (NULL, "Column", "datadict.inc.php", "a column representing a Detail", NULL, "DetailColumn");
INSERT INTO CLASSES (body, super_id, file_id, title, abstract, id) VALUES (NULL, "FieldColumn", "datadict.inc.php", "a column representing a joined table", NULL, "JoinFieldColumn");
INSERT INTO CLASSES (body, super_id, file_id, title, abstract, id) VALUES (NULL, NULL, "datadict.inc.php", "(abstract) base class for Lino modules", NULL, "Module");
INSERT INTO CLASSES (body, super_id, file_id, title, abstract, id) VALUES (NULL, "Module", "apidoc.inc.php", "API documentation", NULL, "APIDOC");
INSERT INTO CLASSES (body, super_id, file_id, title, abstract, id) VALUES (NULL, "Module", "crm.inc.php", "Addressbook", NULL, "ADDBOOK");
INSERT INTO METHODS (body, class_id, abstract, name, title) VALUES ("Lino's Links are directed. They always go *from* one table
*to* another table.

<p>Example:
a link from NEWS to PERSONS means that each NEWS item has an \"author\"
field which points to the PERSONS table. And each PERSON has a \"News
by author\" field which shows a list with the NEWS items written by
this person.

<p>", "Module", "Creates two objects which together represent
the Link: a [ref CLASSES:Join]
in the from-Table and a [ref CLASSES:Detail] in the to-Table.
There is no \"Link\" class in Lino.
", "AddLink", "Create a link from one table to another");
INSERT INTO METHODS (body, class_id, abstract, name, title) VALUES (NULL, "Query", NULL, "Render", "Execute the query and output the data");
INSERT INTO METHODS (body, class_id, abstract, name, title) VALUES (NULL, "Query", NULL, "GetDefaultDetailDepth", NULL);
INSERT INTO METHODS (body, class_id, abstract, name, title) VALUES (NULL, "Query", NULL, "UpdateUsingPOST", "Compare POST data to editingRows and update database");
INSERT INTO METHODS (body, class_id, abstract, name, title) VALUES (NULL, "MemoType", NULL, "ShowValue", "Show a value of type memo");
INSERT INTO METHODS (body, class_id, abstract, name, title) VALUES (NULL, "JoinFieldColumn", NULL, "Render", "output the value of this column in current row");
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("This property does not depend on the renderer.
Removed class EditRender (editing capacity is now in the query).

<p>", 0,0,9, "updating data", "2002-06-04.", "You can now switch on or off the isEditing property of a query.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,9, "Navigator components", "2002-06-04.", "I splitted the navigator into its components:
Format Selector, Navigator, Quick Filter, View Editor, and the new
Editing toggle.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,9, NULL, "2002-06-05", "Detail->ShowRenderer : if masterId is NULL, don't try
to display details.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,9, "A Detail now shows an [edit] button.", "2002-06-05", "This [edit] button links to a page where this detail is displayed as
main component and thus editable.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,9, NULL, "2002-06-05", "\"reusing\" a Query which isEditing() would mean that it would be possible
to save the data in an edited form without submitting it. This is
currently not possible. If you edit data in a form, then forget to
click the submit button, your changes are simply lost.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("The primary key is a column who canEdit(), but in practice this
editor is readonly on all existing rows. You can modify the primary
key only on a new row.

<p>This use of readonly editors is necessary if there is more than one
row in the form. There must be an editor for each row in the form,
otherwise the update method gets messed because the arrays are not all
of same length. 

<p>", 0,0,9, "canEdit() and isReadOnly()", "2002-06-05", "There is a difference between canEdit() and IsReadOnly(). A column who
canEdit() *must* canEdit() for each row. But IsReadOnly() is allowed
to change from row to row.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,9, "Updating and inserting rows works now.", "2002-06-05", "At least in queries without SetRngKey().
<br>TODO: if Query->SetRngKey() are set, canEdit()
for these columns must return FALSE. And CreateRow() must fill them
with the correct SetRngVal().
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,9, NULL, "2002-06-05", "Renderer->OnHeader() is back. It was *not* useless: difference between
OnHeader() and OnRow() with if($first) is that the latter will be
executed only if there is at least one row.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,9, NULL, "2002-06-05", "I am developing my debugging techniques...
It is now possible to start Lino using
<?= urlref(\"index.php?debug=1&verbose=2&meth=reset\")?>.
<tt>meth=reset</tt> works on any page
(which includes lino.php)
and causes a new session to be started.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,9, NULL, "2002-06-06", "source.php had a bug. This was the first bug
discovered by somebody else than the author.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,9, NULL, "2002-06-06", "Looking for a solution to the circular references
problem in datadict...
<li>http://www.ideenreich.com/php/methoden.shtml
<li>http://php.planetmirror.com/manual/en/language.oop.serialization.php
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("<li>http://ee.php.net/manual/en/language.references.pass.php:

<p>Note that there's no reference sign on function call - only on function definition. Function definition alone is enough to correctly pass the argument by reference. 

<p>", 0,0,9, NULL, "2002-06-07", "Continued: circular or bi-directional references in datadict...
<li>http://ee.php.net/manual/en/language.references.arent.php
<li>http://www.digiways.com/articles/php/smartcompare/
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("Reference problem: PHP is very sticky in making copies of objects. Lino
initialized the data dictionary, but then suddenly some parts were
again un-initialized. Because in fact a copy had been initialized. And
there were in fact a lot of unnecessary copies in the session
data. The is_ref() function (original name comparereferences() by Val
Samko, http://www.digiways.com/articles/php/smartcompare/ ) finally
helped me out of this.

<p>One big background change :
the user-code interface is completely new.
Look at index.php

<p><ul>
<li>Before :
<pre>
&lt;li>Addressbook : 
&lt;?= $ADDRBOOK->PERS->ShowViewRef()?>,
</pre>

<p><li>Now:
<pre>
&ltli>Addressbook :
&lt?= ShowQueryRef('PERS')?>,
</pre>
</ul>

<p>", 0,0,9, "Release 0.0.7 is ready.", "2002-06-08", "I worked almost two
full days on a frustrating reference problem.
One big background change:
the user-code interface is completely new.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("A \"slot\" is one of the following: phone or fax number, email
adress, url, ...

<p><pre>
class SLOTS extends Table {

<p>  function init() {
    $this->AddIntField('id','ID');
    $this->AddTextField('type','Type');
    $this->AddTextField('slot','Slot');
    $this->label = 'Slots';
  }
  
  function GetRowLabel($query,$alias='') {
    $s = '';
    $s .= $query->row[$alias.'type'];
    $s .= ' ' . $query->row[$alias.'slot'];
    return $s;
  }
}
</pre>

<p>And later during ADDRBOOK::link():
<pre>
AddLink('SLOTS','pers','Person',
        'PERS','slots','Slots');
AddLink('SLOTS','org','Organisation',
        'ORG','slots','Slots');
</pre>
a slot knows its Person and/or Organisation.

<p>", 0,0,9, "New table \"SLOTS\"", "2002-06-09", "I modified the database structure for module ADDRBOOK.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,9, "pin2sql.py", "2002-06-09", "I wrote pin2sql.py, a little Python script which converts a \"pinboard\"
file into SQL statements.  Result: my change log is now really in the
NEWS table.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("pin2sql.py reads a Pinboard input file (from stdin, by default) and
outputs an SQL script which, if executed in MySQL, will create the
actual rows in the SQL database.

<p>I have now a dbinit.bat which does:
<pre>
python ..\pinboard\pin2sql.py < ..\pinboard\changes.pin > changes.sql
type sys.sql > dbinit.sql
type lang.sql >> dbinit.sql
type addrbook.sql >> dbinit.sql
type nations.sql >> dbinit.sql
type community.sql >> dbinit.sql
type changes.sql >> dbinit.sql
mysql %1 < dbinit.sql
</pre>

<p>The Pinboard format is inspired by RFC2822 (the format used for email
messages), but with flexible headers. Look at
[srcref pinboard/changes.pin]
and ask questions if you want...

<p>", 0,0,9, "pin2sql.py version 2", "2002-06-10", "I re-wrote pin2sql.py, now it is worth to speak about it.
I invented the \"Pinboard\" format because I prefer Emacs to all other
user interfaces which i have seen so far.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("Results :
<ul>
<li>The Browser's Back Button now works as expected.
<li>[Close] and [Refresh] buttons are no longer necessary
</ul>

<p>Another advantage: you can now copy and paste a link to a certain view
since the query's state no longer depends on session data.

<p>TODO:
The update button is currently broken. 

<p>", 0,0,9, "this.php no longer used", "2002-06-10", "Release 0.0.8 had a bug in this.php.  The idea of this.php was to have
a \"current query\", that is, a Query instance stored in the session
data.  Now the current state of the Query is completely reflected in
each URL, and the Query instance is re-created for each page.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("<ul>
<li>Table.ShowPeekRef($id,$label):
shows a link to a page where the row with the specified primary key
will be displayed.
Used for example
(1) to render a JoinFieldColumn (that is, a Column which
links to another table).
Or (2) as default implementation for Table.ShowInCommaList().

<p><li>Table.ShowInCommaList($query):
<li>Table.GetRowLabel($query,$alias=''):
</ul>

<p>", 0,0,9, "ShowPageRef(), ShowPeekRef()", "2002-06-10", "There is still some chaos in this part of the API...
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,9, "Documentation outdated", "2002-06-11", "Even though there is not much documentation, there were already some
seriously outdated things written in <a href=\"tour.php\">Le Tour de
Lino</a>.  There are probably more such things on other places.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("<b>Notice</b>: Undefined property: editingRows
<br>in /home/luc/public_html/lino-0.0.8/datadict.php on line 2056

<p>A Query which is editing will now store itself into the session data
($_SESSION['editingQuery']) where update.php will take it out again.

<p>The Query->editingRows[] attribute is an array of the rows which have
been rendered with editors.

<p>There is currently no record locking mechanism. So, it two users ask
to edit the same data at the same time, you will have surprising
results. 

<p>", 0,0,9, "Undefined property: editingRows", "2002-06-11", "Query updating was broken.  When you clicked on \"isEditing : [on]\",
you got only a run-time error.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("class Renderer renamed to HtmlRenderer.  HTML renderers
are now singleton objects in a global array $htmlRenderers
which maps the format name to the renderer instance.
Query->renderer no longer exists. Was used only in Query.Render().
Instead there is now again Query->format.
Query.Render() usually chooses the renderer by getting it from
$htmlRenderers. Exception:
if isset($HTTP_GET_VARS['xml']) (that is:
\"&xml\" was added to the URL (which is done if click on
the [XML] pseudo button)),
it always chooses the unique XmlRenderer.

<p>", 0,0,9, "Renderers", "2002-06-12", "Some internal changes as preparation for XML support.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("This XML is probably not very valid.
I will wait a little bit for ideas
about how to continue...

<p>What is XSLT?
Interesting article about XSLT at
<? urlref('http://www.xml.com/pub/a/2000/08/holman/')?>.

<p>", 0,0,9, "Lino speaks XML", "2002-06-12", "Now Lino gives XML output...
but you should probably ask
your browser to show the page's source.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,9, "Setting debug level and verbosity", "2002-06-12", "title.php: The togglers for $debug and $verbose
referenced still to this.php...
Now they work at least when you are on index.php.
On render.php for example they still don't work.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("<b>Notice</b>: Undefined index: editingQuery
<br>in /home/luc/public_html/lino-0.0.9/update.php on line 7.

<p>This error is not reproduceable on my local installation (PHP
4.2.0). Perhaps somebody who knows PHP better than me finds the
reason?

<p>At the end of Query.ShowRef()
(file <? srcref('datadict.php')?>)
I save the current query to
session data:
<pre>
$HTTP_SESSION_VARS['editingQuery'] = $this;
</pre>

<p>Then, if the user clicks Submit,
<? srcref('update.php')?> is called, and at this
moment 
$HTTP_SESSION_VARS['editingQuery'] is not defined.
Mysterious...

<p>", 0,0,9, "Updating rows", "2002-06-12", "There is now another runtime error when you try to update rows. One
click later than before.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,9, "0.0.9 released", "2002-06-12", "Lino 0.0.9 is out at http://www.girf.ee/~luc/lino-0.0.9/index.php
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("Notice: Undefined property: row
in /home/luc/public_html/lino-0.0.9/datadict.php on line 1887.

<p>", 0,0,10, "Undefined property: row", "2002-06-12", "A little bug, came only if $debug was 1.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,10, "Projects and News linked", "2002-06-12", "There is now a new Table PRJ2PRJ (a Project can have parents and
children).
And there is a Link from NEWS to PROJECTS : each NEWS itemcan be
assigned to a single project.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,10, "pin2sql.py : ArrayType", "2002-06-12", "To encode the projects.pin file i wanted a new header field type
\"Array\". So now I can create PROJECTS using Pinboard format. They need
a field \"parentProjects\" which is a list of 0 to N Project id's...
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("Answer: Because I omitted to send the appropriate HTTP header. PHP by
default answers in HTML. If I answer in XML, I must explicitly say it
using <tt>header(\"Content-type: text/xml\");</tt>.

<p>Now the client browser knows that Lino answers in XML.  Result: since
the browser now also checks whether this is <i>valid</i> XML,
and since Lino's XML is not yet perfect,
you don't see anything but an error message indicating what is invalid.

<p>", 0,0,10, "HTTP content-type", "2002-06-12", "Why does my browser display other people's xml pages as xml, while
Lino's XML output is displayed in a very strange manner?
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("There is now a global variable $renderer. There are currently two
Renderer classes : HtmlRenderer and XmlRenderer.
Renderer.OnRow renamed to Renderer.ShowQueryRow.
Renderer.OnHeader renamed to Renderer.ShowQueryHeader.
Renderer.OnFooter renamed to Renderer.ShowQueryFooter.

<p>", 0,0,10, "Renderer", "2002-06-13", "Some internal changes to get the XML output working.
It seems to work
now for queries where the contents has no special characters
(umlauts).
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("I read 
[url http://www.devshed.com/Server_Side/PHP/SelfDoc/print] and
looked at
[url http://www.phpdoc.de/doc/introduction.html 2].
A tool like PHPDoc would be nice, but the current Version 1.0beta has
a conceptual problem: it does not really parse the code. It
would have problems to create the Lino API since almost all
classes are in one file.
This Version 1.0beta is more than one yar old:
the project seems dead...

<p>", 0,0,11, "Use PHPDoc?", "2002-06-17", "PHPDoc is a tool like JavaDoc which could be useful to create the Lino
API documentation.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("<table>
<tr>
<td>Code
<td>Result
<tr>
<td><tt>ref('PERS:1')</tt>
<td><?= ref('PERS:1')?>
<tr>
<td><tt>ref('PERS:1','Luc')</tt>
<td><?= ref('PERS:1','Luc')?>
</table>

<p>", 0,0,11, "new global function ref()", "2002-06-18", "Shows a reference to a single record in a table.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("<table>

<p><tr>
<td>Quick tag
<td>equivalent PHP code
<td>Result

<p><tr>
<td><tt>&#91;url http://www.url.com]</tt>
<td><tt>&lt;? urlref('http://www.url.com')?></tt>
<td>[url http://www.url.com]

<p><tr>
<td><tt>&#91;url http://www.url.com url]</tt>
<td><tt>&lt;? urlref('http://www.url.com','url')?></tt>
<td>[url http://www.url.com url]

<p><tr>
<td><tt>&#91;ref PERS:1]</tt>
<td><tt>&lt;? ref('PERS:1')?></tt>
<td>[ref PERS:1]

<p><tr>
<td><tt>&#91;ref PERS:1 Luc]</tt>
<td><tt>&lt;? ref('PERS:1','Luc')?></tt>
<td>[ref PERS:1 Luc]
</table>

<p>This system is implemented using preg_replace(),
actually 2 x 3 lines of code.
Look at the source of [ref METHODS:MemoType,ShowValue].

<p>API change as side effect: all Show*Ref() methods
renamed to Get*Ref().
They don't echo the string themselves but just return it.

<p>", 0,0,11, "Quick Command Tags", "2002-06-18", "In memo fields you can now use quick tags instead of the quite
complicated PHP code.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,11, "JoinFieldColumn.Render() did not work.", "2002-06-18", "[ref METHODS:JoinFieldColumn,Render] always displayed an url with an
empty label. Fixed.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,11, "API for GetRowLabel() changed", "2002-06-18", "GetRowLabel($query,$alias)
replaced by
GetRowLabel($row)
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("API change : [ref METHODS:Table,GetPrimaryKey]
must now return an array of references to
the fields who serve as primary key.

<p>", 0,0,11, "Compound primary keys", "2002-06-18", "It is now possible to define tables whose primary key is more than one
column.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,11, "Internal structure of data dictionary modified", "2002-06-18", "Some important internal changes in the data dictionary.
The Join class now represents more closely a link.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,11, "New module APIDOC", "2002-06-18", "I started the new module [ref CLASSES:APIDOC]
in the hope that it helps me to write
API documentation. 
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,11, "todo: \"&id=\"", "2002-06-20", "If you change the showDetail option using OptionPanel on a IsSingleRow
query, then this property gets lost because Query.GetRef() does not
know about it...
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("After reading 
[url http://www.faqts.com/knowledge_base/view.phtml/aid/562/fid/9] and
[url http://www.phpbuilder.com/tips/item.php?id=66],
i won't rename them to *.inc but to *.inc.php.

<p>", 0,0,11, "include files", "2002-06-21", "How should include files be named? foo.php? foo.inc? foo.inc.php?
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("[ref DBITEMS:tour] is now implemented using DocBook and pin2sql.
The pinboard source used to feed the database
is [srcref pinboard/doc.pin]

<p>", 0,0,11, "new DocBook module", "2002-06-22", "A module to write structured documents such as books or articles. This
module will probably also replace the [ref CLASSES:APIDOC ApiDoc]
module.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("ShowTitle($title) and ShowFooter() are now replaced by BeginSection()
and EndSection().

<p>There is now the concept of a margin and a new global function
ToMargin().

<p>", 0,0,11, "The margin", "2002-06-22", "Some important works in presentation logic.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("<ul>
<li>
We decided that Lino should be split into a
[ref DBITEMS:architecture_backend Backend]
and a [ref DBITEMS:architecture_middle Middle Tier]
(meeting on Thursday 2002-06-20 at Girf).
We must continue to
think together about this change in architecture.
I need more concrete decisions before I can implement something.

<p><li>If web users update the database, Lino can write this update to a
log file and notify some responsible person (me, for example). It
would be a step towards using Lino as a community tool if people can
easily add their remarks to DocBook entries.

<p><li>
I have still quite some ideas for the HTML presentation layer
which I would like to become visible.
I hope that the Lino HTML interface
can soon be considered \"usable\".
The first application would be the DocBook module.

<p><li>When calling show source, user gets Fatal error: Call to a member
function on a non-object in html.inc.php on line 137.
The $renderer must become independent from Lino. BeginSection() and
EndSection(), ToMargin() must become methods of the renderer.

<p></ul>

<p>", 0,0,11, "Release 0.0.11 is ready", "2002-06-22", "Here an overview of where Lino is and what to do next.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("The data dictionary must not speak about the format of a query, but
well about its depth.

<p><ul>

<p><li>The most superficial query which i can imagine
(depth 1) is the <b>reference</b> to a potential query.
It needs a user's click before Lino even executes such a query.

<p><li><b>short list</b> (depth 2) means that yes, i am interested in
the result of this query, but please don't waste space. Maximum one
paragraph for the whole result.

<p><li><b>list</b> (depth 3) means that I expect a series of
paragraphs, one for each row. (List can become later a simple
paragraph list, a numbered list, a bullet list,...)

<p><li><b>table</b> (depth 4) shows all rows in the well-known table.

<p><li><b>page</b> (depth 5) shows one row at a time. \"I want to see
this row, only this one.\"

<p></ul>

<p>Let's add one item to the beginning of this list: depth 0 means
that Lino should not show this query at all. This depth is not
meaningful for a main-level query, but our travel into the depths of a
query is not finished.

<p><b>The depth of details.</b>

<p><ul>
<li>A query with depth 1 or 2 will not show any details.
maxDetailDepth() is 0.

<p><li>A List query (depth 3) usually also won't show any details.  But
it could. It is able to show references to details, and it could even
show details as short lists. But certainly not more.
maxDetailDepth() is 2.
defaultDetailDepth is 0.

<p><li>A table query (depth 4) is able to show details as a list. Even
(rarely) as a table (which is a table inside a table).
maxDetailDepth() is 4.  defaultDetailDepth is 3.

<p><li>A page query (depth 5) can show details in any formats. (oops:
here it is again, the word \"format\"). maxDetailDepth() is 5.
defaultDetailDepth is 4.

<p></ul>

<p>Note that the depth level is represented by an integer. It is no
longer a format keyword but a \"level\".

<p>Lino uses this to determine the default depth of detail queries.
because (by default) a page query will display 

<p>Notes concerning the HTML interface:
<ul>
<li>only table and page queries can directly modify
the data (using isEditing).

<p><li>there can now be a button to increase or decrease
the depth.
</ul>

<p>", 0,0,12, "The depth of a query", "2002-06-25", "I introduced a new concept: the <b>depth</b> property of a query.
This is a more abstract replacement for the current \"format\" property.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,13, "Many little changes", "2002-06-28", "<ul>
<li>URL to Query now handled in [ref FILES:render.php].
<li>Module::SetupLinks() and SetupTables()
<li>peek with complex primary key
<li>Projects table moved from COMMUNITY to APIDOC module.
<li>Structure changes in APIDOC module
<li>many more...
</ul>
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("isMainComponent and renderNestingLevel are now replaced by the
Query->parent attribute.  isMainComponent() now simply returns
is_null($this->parent), and NestingLevel() loops backwards through the
chain of parents. Either a simple count, or perhaps the sum of all.
Perhaps with weight factors?

<p>When a Detail creates its Query, it can decide about the depth.

<p>", 0,0,14, "Actions (not finished)", "2002-06-29", "DBITEMS::MoveUp()
$HTTP_SESSION_VARS['editingQuery']
replaced by 
$HTTP_SESSION_VARS['renderedQuery']
function show() is used only in index.php
and does not work with renderedQuery
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,14, "Some new tables and names", "2002-07-02", "New table TOPICS in DOCBOOK module.
Module APIDOC renamed to SDK (Software Development Kit).
New table VERSIONS in SDK module.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,14, "pin2sql.py enhanced.", "2002-07-03", NULL, 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("There are still some minor bugs due to this.
TODO: automatically create default data in these tables. Currently
they are absolutely virgin.

<p>", 0,0,14, "Lino can now create tables automatically", "2002-07-03", "meth=create_tables : Lino creates now himself the CREATE TABLE
statements for each table.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("New function Table::insert_row() for usage in these *.ini.php files.

<p>TODO: currently all fields must be specified, and in the right
order. Which is not so elegant. In Python this would be easy by using
keyword arguments.

<p>TODO: it is probably better to not have one separate file for each
table. It is better to have a set of demo data files.

<p>", 0,0,14, "default data for tables", "2002-07-03", "Some tables should have default content. create_tables now looks if
there is a file (tablename).init.php. If it exists, then it gets
executed.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("The difference between a Join and a JoinField becomes important if a
join is made using more than one field (that is, if the refered table
has a complex primary key).
Each JoinField is represented in its own colum. And each Join is
represented in another column.

<p>Example:

<p>The Methods table has a complex primary key : (class_id, name) where
class is itself a JoinField (a pointer to the Classes table).

<p>A Query with Methods as master table will have:
<ul>
<li>a JoinField column 'class_id'.
GetCellValue('class_id') returns a string.
<li>a JoinField column 'name'
GetCellValue('name') returns a string.
<li>a Join column 'class'
GetCellValue('class') returns a row.

<p><li>there is no longer a column class_title. If you want to access the
class's title, you must use $row = GetCellValue('class'); return
$row['title']

<p></ul>

<p>Loading views from database is currently broken. Was not used anyway.

<p>", 0,0,14, "JoinColumn", "2002-07-03", "Joins on complex primary keys did not work.
JoinFieldColumn replaced by JoinColumn.
A JoinField now also is represented by a FieldColumn.
The new JoinColumn represents a Join.
The joined fields no longer have their own column in the Query.
So the unelegant isMaster property can go away.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("A Cell is a Column in a Query.
Cells are stored in Query.cells[] with numeric index.
Columns are now stored in the view with their name as index.
View.FindColumn() no longer necessary.
Query.SetSlice() does not set a \"hidden\" flag (or, alternatively I
tried also that Column.canSee() tests each time whether it is
contained in $query->slices...) but simply deletes the Cell instance
from the Query.
Column::canSee() no longer necessary.

<p>Column::IsEmpty($query) tells whether the column is empty in the
specified query.

<p>Query::Setup() performs internal actions necessary to Render() the
query. But these actions are only necessary to actually render it. Not
each Query instance gets rendered. Sometimes they are just created to
collect some parameters and then display a Query->GetRef(). That's why
I don't do it simply in the constructor.

<p>Setup() is automatically called by Render().
But some Query settings (currently SetSlice() and
HideColumn()) will automatically cause Setup() to start. 

<p>", 0,0,14, "Misc", "2002-07-04", "New class Cell.
<ul>
<li>Cell->column : reference to the Column instance in View
</ul>
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("new Method Query::SetColumnList() to specify explicitly the list of
QueryColumns. To be used in *.init.php and later in ImportCsv().

<p>", 0,0,14, "Misc", "2002-07-06", "Renamed class \"Cell\" to \"QueryColumn\". Because the name \"Cell\" was
really not appropriate.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,14, "Pipelining", "2002-07-07", "Messages which had been sent to ToUserLog() became visible only on the
next page. I use now ob_start() to catch the stdout. The output itself
is only started during EndPage(). error_handler() also calls EndPage()
before die(). 
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,14, "PHP tags in memo fields no longer supported", "2002-07-08", "ShowMemoValue() does no longer evaluate php tags. Only QuickTags are
allowed. This was a security hole.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("GetTable() returns the table singleton.
The table name is now independant of the implementing class.
There will be a list of standard table names.
For example, modules must agree whether the Persons table's name is
PERS, PERSON, or something else... P, for example?

<p>The same is true for Modules. Any module can be declared as ADDRBOOK,
for example.
Hmm... this sounds now as if it were better to use
inheritance. Modules who want to be an AddressbookModule should simply
inherit a standard AddressbookModule class. To be continued...

<p>", 0,0,14, "new Application class", "2002-07-08", "I implemented the announced change about intermodule connectivity.
Intermodule Cooperation is a better name, btw.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES ("(But there are still many differences)

<p>", 0,0,14, "pin2sql.py", "2002-07-09", "pin2sql.py now supports more interesting things and has become more
close to the Lino data dictionary.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,14, "Quick Filter", "2002-07-10", "The Quick filter works again. render.php looks now also to the POST
vars. The qfilter property is now transferred via POST. Because if I
make a form with method=GET, then it will remove any parameters in the
URL. That was surprising.
", 1, NULL);
INSERT INTO CHANGES (body, version_major,version_minor,version_release, title, date, abstract, author_id, id) VALUES (NULL, 0,0,14, NULL, "2002-07-10", NULL, 1, NULL);
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES (NULL, NULL, "doc", "LinoConcepts", "Lino Concepts");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("The first Lino uses in the near future will be:

<p><ul>
<li>a Community Platform for Software Development
(in particular, for developing the Lino software)

<p><li>a CRM application
</ul>

<p>Technically, an application is defined by
<ul>
<li>a database 
<li>a domain (directory on the server) where the
application specific php files reside.
</ul>

<p>", "The behaviour of a Lino Application is defined by the set of modules
which have been chosen to be part of this particular
applications.
[url http://www.girf.ee/luc/lino] is currently the only
known Lino Application.
", "LinoConcepts", "tour_Applications", "Applications");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("Let's look at two table definitions :

<p><pre>
class PERSONS extends Table {

<p>  function init() {

<p>    $this->AddIntField(\"id\",\"ID\");
    $this->AddTextField(\"name\",\"Name\");
    $this->AddTextField(\"fname\",\"First Name\");
    $this->AddTextField(\"title\",\"Title\");
    
    $this->label = \"Persons\";
  }

<p>}

<p>class ADDRESSES extends Table {

<p>  function init() {
    $this->AddIntField('id','ID');

<p>    $this->AddTextField('email','E-Mail');

<p>    $this->AddTextField('zip','Zip Code');
    $this->AddTextField('city','City');
    
    $this->AddTextField('street','Street');
    $this->AddIntField('house','#');
    $this->AddTextField('box','box');

<p>    $this->label = 'Addresses';

<p>  }
  
}
</pre>

<p>", "A Table in Lino describes a data table in the SQL database.  A Lino
Table contains not only Fields (SQL columns), but also Vurts (Virtual
fields) and Actions.  (Vurts and Actions are for later. Currently there
is no concrete example to show their use.)
", "LinoConcepts", "tour_Tables", "Tables");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("Examples of Lino Standard Modules :

<p><ul>

<p><li>System (Users, Views, Languages)

<p><li>Addressbook (Persons, Organisations, Addresses)
<li>Agenda (Talks, Meetings)
<li>Community (News,Projects,To-Do-List)

<p><li>Topics, Products, Ordering, Invoicing, Accounting...
</ul>

<p>Each module is theoretically implemented in its own .php file.  But
the list of Standard Modules and tables is still unstable.
That's why currently the file
<a href=\"source.php?file=crm.php\">crm.php</a>
provides three modules ADDRESS, COMMUNITY and
AGENDA.

<p>Another file
<a href=\"source.php?file=sys.php\">sys.php</a>
provides the System module.

<p>", "A Lino Module is currently
nothing more than a collection of
<b>table
definitions</b> and the <b>links</b> between them.
", "LinoConcepts", "tour_Modules", "Modules");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("<pre>
class ADDRBOOK extends Module {
  
  function init() {
    AddTable('PERSONS');
    AddTable('ADDRESSES');
  }

<p>  function link() {

<p>    AddLink('ADDRESSES','pers','Person',
            'PERSONS','addresses','Addresses');
    
  }
</pre>

<p>(Implementation note: Lino currently initializes in two steps: init()
and link(). This is because all tables must be initialized before it
is possible to create links between them.)

<p>Here the ADDRBOOK Module defines two Tables PERSONS and
ADDRESSES. These tables are linked together : FROM Addresses TO
Persons.  This Link will automatically create another special field
'pers' in the ADDRESSES table which is a pointer to a PERSON. This
Link is a 0-N relation : 1 Person can have 0, 1 or many addresses.

<p>The User will see this Link as follows:

<p><ul>
<li>If you create an Address, you must specify a Person who lives at
this address.
<li>If you look at a Person, you can see a list of Adresses
which are connected to this Person.
</ul>

<p>", "Lino simplifies the programming of links between tables.
Here again some code:
", "LinoConcepts", "tour_Links", "Links");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("This is somewhat unconventional.
Lino separates the definition of \"real\" data fields from fields who
are just pointers. This makes it easy to juggle around with different
variants of database structures during a prototype phase.

<p>", "Note that the \"pers\" field must not be specified in the table
definition. It comes automatically because you linked the two tables.
", "LinoConcepts", "tour_Separating", "Separating data definition from link definition");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("Of course, the specified id must be unique. And the name of a person
may not be empty. These are constraints which even MySQL can
handle.

<p>Another case for validation is : id is unique, but there is already
another person with same (name,first_name). Okay, if the birth dates
are different, we can assume that they are different persons. But if
the new person has no birthdate specified? There is no general rule
for such cases. The appropriate reaction depends on the application. 

<p>Lino can refuse any database update because of such reasons which are
application-specific rules.

<p>Instead of refusing, Lino can also say \"Do you want that I ask for
manual confirmation by some operator\". Lino would then send an e-mail
to a responsible human database supervisor: User X asked to create a
Person (id, first_name, name, birthdate), but there is possible
duplicate creation. Please give your confirmation.

<p>", "Imagine a database with a table of Persons. Somebody asks Lino to add
a new Person (id, first_name, name,
birthdate).
", "LinoConcepts", "tour_validation", "Data validation");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("Examples of data which don't come from SQL database:

<p><ul>
<li>Calendar : a virtual table. The rows of the calendar represent
each day of the year. They are not stored anywhere since they are
well-known and easy to compute.
But DateFields could automaticaly link to the Calendar,
and a Calendar
query has a lot of Details.

<p><li>The currency exchange rates could be stored in an array which is
initialized via Internet from a currency exchange rates server.

<p><li>A FileSystem table could represent the tree structured directories
and files of a file system.

<p></ul>

<p>Note that this connectivity can also be implemented using
\"Database Agents\", that is little daemons which update the Lino
database independently of the Lino server....

<p>", "Currently Lino has one database for one application, and Lino can
manage only SQL data. This could change in the future.
", "LinoConcepts", "Heterogenous", "Heterogenous data sources");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES (NULL, NULL, NULL, "doc", "The Lino DocBook");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES (NULL, NULL, "doc", "tour_intro", "Introduction");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("<ul>
<li>Programming Framework : Lino is not meant for end-users, but as
a library or engine to be used by Lino Providers.

<p><li>Web Application : a Web-based interface to an SQL database.
</ul>

<p>", "Lino is a
<b>Programming Framework</b>
to create high-quality, low-cost <b>Web Applications</b>.
", "tour_intro", "tour_whatis", "What is Lino?");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("In its current implementation (PHP, MySQL), Lino has probably some
technical limits, so it is not a choice for large-scale
applications. [TODO: Is this true? What limits?]

<p>", "Lino aims the low-cost Web Application market. Potential End-users are
medium-sized or small companies who understand that they need
assistance from IT experts for the analysis and setup of their
Information System and who are willing to dedicate an appropriate
budget to these services.
", "tour_intro", "tour_for_whom", "For whom is Lino?");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("<ol>

<p><li>Selling:
<ul>

<p><li>Know the <b>Standard Modules</b> and what they do. Know also what
they can <b>not</b> do.

<p><li>Analysis :
Speak with the User to find out which modules are necessary.

<p></ul>

<p><li>System Administration
<ul>
<li>Install Apache, MySQL, PHP, Lino
<li>Manage SQL databases
<li>Install backup possibilities. Explain to the User how to use them.
</ul>

<p><li>Maintenance
<ul>
<li>Training : Explain to the User how to use their Lino.

<p><li>Support : Answer to the User's questions.

<p><li>Check continuously with the User if the analysis is correct or
whether there are new needs.
</ul>

<p><li>Take part in the development process:
<ul>
<li>Understand the Lino source code and how Lino works internally.
<li>Specify requirements for new Lino Modules.
<li>Test Lino modules and report bugs to a Developer.
</ul>
</ol>

<p>A Lino Developer is somebody who writes new Lino Modules.  Currently
there is only one such person, but I don't want to stay alone.

<p>Since Lino is Free Software, the Lino Service Providers are not
legally bound to the developer. They can decide to rely on their own
Lino Developer.

<p>", "A Lino Service Provider is a company who knows enough about Lino to be
able to give quality service to end-users. A Lino Service Provider
should have the following abilities:
", "tour_intro", "tour_providers", "Service Providers");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("I am currently working on Lino without getting money for this
work. This shows only that I personally believe that there is need for
Lino. I may be wrong.

<p>I currently get moral and technical support from
the people at [url http://www.girf.ee Girf].
Without them, you would not be able to see Lino:
they are not only hosting the currently only Lino instance of the WWW,
but they gave me the idea to implement Lino in PHP and MySQL.

<p>", "Lino is born from my 10 years of experience in Software Development
at [url http://www.pacsystems.be PAC Systems].  I had to stop
working for PAC Systems because I moved from Belgium to Estonia and
because Lino was not finished, not even visible, at this time.
There is hope that Lino could become a successor for good old TIM.
", "tour_intro", "tour_who", "Who is developing Lino?");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("Note that the current
implementation is only a draft of the big plans for the future.

<p>", "Here is an overview of the Lino components and how they interact.
", "doc", "architecture", "Lino Architecture");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES (NULL, "Lino works with any SQL-compatible database server, even MySQL.
There will be optimized <b>database drivers</b> for
PostgreSQL, Oracle...
", "architecture", "components.dbserver", "Database Server");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES (NULL, "The Lino Backend 
sits around the database and controls
the accesses to this database.
", "architecture", "architecture_backend", "The Backend");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("See [ref DBITEMS:tour_validation] for an example of rules in the
datadict. 

<p>The data dictionary also contains abstract presentation logic.

<p>", "The Data Dictionary contains meta-data
about an application:
Which tables are available,
how they are linked together,
user actions,
business rules,...
", "architecture_backend", "components.datadict", "Data Dictionary");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("The backend is the only component who communicates directly with the
database. This is to protect the database from accesses which don't
obbey the application's rules and thus would corrupt the data
integrity.

<p>The [ref DBITEMS:pinboard_interface pin2sql tool] which I currently
use is an example of short-cutting this architecture.  pin2sql
should better create Lino XML statements.  These statements are sent
to the Lino Backend who translates them to SQL and sends them to the
database server.

<p>", "The Backend communicates 
with the
database, using a <b>Database Driver</b> who creates the SQL
statements to be sent to the database server.
", "architecture_backend", "components.dbdriver", "Database driver");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("TODO: 
Is the Backend a HTTP server?
Or a simple TCP server?
What about user authentification?
Which programming language (Python, Java, PHP, ...)?

<p>[TODO: XML specification]

<p>Why do you want to split the XML server from the HTML renderer?
Because here is a reason why you should not split them: The Backend
and the HTML renderer access the same data. And they usually run
on the same server.
Why do you want to split them into two processes?

<p>Unsplit: Lino backend gets data from Database. As an array of
rows. Then he passes this array to the renderer who will output it
with the appropriate HTML tags around it.

<p>Split: Backend gets data from database as array. Renders it as
XML (putting the appropriate tags around the data and sending this to
stdout).
Then another Lino component reads this XML stream, parses it,
re-creates the original array, then continues the second part of the
job (HTML renderer).

<p>Load balancing. If there are many processes.

<p>", "The Backend communicates with the outside world using XML.
", "architecture_backend", "components.comm", "Communication");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES (NULL, "The Middle Tier is a suite of software components, also third-party
products, which translate Lino's XML interface into more useful
outside-world languages (HTML, PDF, ...).
", "architecture", "architecture_middle", "The Middle Tier");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES (NULL, "The <b>HTML interface</b>
is a little HTTP server who accepts HTTP
requests and forwards them to Lino. 
The answer from Lino which is in XML can
be translated to HTML using XSLT.
", "architecture_middle", "html_interface", "The HTML interface");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("Currently this tool shortcuts the Lino Backend and writes directly to
the database. 

<p>", "I decided to develop my own format to edit structured texts.  I called
it Pinboard. And I wrote a little tool which imports pinboard
documents into Lino.
", "architecture_middle", "pinboard_interface", "The Pinboard interface");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES (NULL, NULL, "doc", "limits", "Limits");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("Lino does not yet reflect your structure changes automatically into an
existing database.  You must do this yourself.

<p>Databases are currently being created manually using SQL scripts.

<p>", "Juggling around with the data structure is very easy and useful,
but for the moment only if you don't forget to modify the underlying
SQL database structure accordingly.
", "limits", "database", "Database");
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES (NULL, "en", "OAGIS interface", "2002-06-26", "Lino should perhaps support business-to-business communication using
the OAGIS XML specification for Business Object Documents
(e.g. Purchase Orders, Invoices, Shipments,...).
[url http://www.openapplications.org]
", NULL, 1, NULL);
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES ("Lino also uses a technique which I could call pipelining:

<p>ToBody(), ToMargin() and
ToSuperHeader() are pipeline streamers. A method does not write simply
to \"stdout\" but to one of these pipelines.
Body, Margin and SuperHeader are pipeline areas.

<p>", "en", "AxKit and Apache", "2002-06-26", "AxKit ([url http://www.axkit.org]),
a Perl-based XML application server framework
for Apache [url http://www.xml.apache.org],
uses a technique which they call \"Pipelining\".
", NULL, 1, NULL);
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES ("<quote>
Tamino XML Server is the first XML platform to store XML information
without converting it to other formats, such as relational tables. It
integrates relational or object-oriented data into XML structures.
</quote>

<p>Luc: But XML is not a data storage format?

<p><quote>
The XML engine in Tamino XML Server (...)  has been designed for
URL-based access.  It cooperates with existing standard HTTP servers.
(...)  Tamino XML Server's query language X-Query is based on the
XPath standard. This allows for powerful queries on stored documents
as part of a URL issued either via standard Web browsers or through an
application.</quote>

<p>Luc: Interesting.
So they don't use XML as language for the requests.
I would like to see their query language.
Aha, here is an example:

<p><quote>
The following example of X-Query syntax illustrates a request for a
doctor's details by patient name (for example, a patient is in trouble
and the nurse wants to contact the doctor):

<p><tt>...?_xql=hospital/patient[p-surname=\"Jones\"]/doctor</tt>

<p>where \"...\" stands for the address of the Tamino XML Server. This
query retrieves the record of the doctor associated with the patient
called \"Jones\". The user does not know that the patient's record is
stored in XML format and the doctor's details are retrieved from an
SQL table. In practice, the X-Query syntax is also hidden from the
user by an application GUI.

<p></quote>

<p><quote> The XML engine's basic function is to store XML objects in and
retrieve them from their respective data sources. It does this based
on schemas defined by the administrator in the Data Map. XML objects
are stored natively in Tamino.  (...)  XML objects to be stored by the
XML engine are described by their schema stored in Tamino's Data
Map. Tamino XML Server's built-in XML parser checks the syntactical
correctness of the schema and ensures that incoming XML objects are
well-formed.</quote>

<p>Luc: Lino uses the pure programming language (currently PHP) to define
the data map. If a system administrator wants to adapt the data
dictionary to her needs, she must do this in PHP. Why should XML be
better? One advantage: if a new Lino version decides to switch to
Java, they must all convert their data dictionaries... But...)

<p>More on [url http://tamino.demozone.softwareag.com/mainSiteX/].

<p>", "en", "Tamino XML server", "2002-06-26", "Commented excerpts from [url http://www.softwareag.com/tamino].
", NULL, 1, NULL);
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES ("We could even imagine to use Lino as a server without any user
interface: he gets data input from some application, validates and
processes this data and stores it into his database,
and then some
triggering will call him to send the data to some other application.

<p>", "en", "Meeting Hannes, Andres & Luc", "2002-06-27", "We met again to speak about Lino architecture. One thing was clear:
Lino should not only import data occasionally, but should provide a
lot of possibilities to connect to other applications.
", NULL, 1, NULL);
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES ("Known bugs:
<ul>
<li>the [more] link does not always work
<li>displaying the Persons list with depth 5 causes a User Error
\"sponsor : no such join alias in CHANGES\".
<li>The [url
http://localhost/phptest/lino/render.php?t=DBITEMS&v=DBITEMS&page=1&pglen=10&depth=3&filter=ISNULL(DBITEMS.super)
DocBook items] link does not show the general page header.
</ul>    

<p>", "en", "Summer Release 0.0.13 ready", "2002-06-28", "Many little changes. Some known bugs.
", 7, 1, NULL);
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES ("And, especially after reading
[url http://www.xach.com/aolserver/mysql-to-postgresql.html],
I thought about switching from [ref TOPICS:3 MySQL] to PostgreSQL.

<p>I will switch to PostgreSQL progressively: I must first get the
database driver system functional.

<p>BTW: PostgreSQL installation is in fact very simple: you just need to
install [ref TOPICS:4 Cygwin].

<p>", "en", "PostgreSQL", "2002-07-02", "I finally managed to get
[ref TOPICS:2 PostgreSQL]
running on my machine.
", 7, 1, NULL);
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES ("I unpacked the distribution to s:\webware
There i started python install.py.
They don't use distutils.

<p>I currently use the CGI interface of [ref TOPICS:1 Apache].  I just
copied the WebKit.cgi file from the WebWare distribution to my cgi-bin
directory, then i modified the copy as follows:

<p><pre>
#!u:/cygwin/bin/python.exe 
WebwareDir = \"s:/webware\"
</pre>

<p>To start the WebWare Application server, I open a DOS window and type

<p><pre>
call i.bat
s:
cd S:\Webware\WebKit
call AppServer.bat
</pre>

<p>After this I can point my browser to
[url http://localhost/cgi-bin/webkit.cgi]
to see the example page.

<p>", "en", "Installed WebWare Application Server", "2002-07-02", "I installed WebWare for Python.
This is a suite of software components for developing
object-oriented, web-based applications.
[url http://webware.sourceforge.net/]
", 7, 1, NULL);
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES ("A View is a singleton object and part of the data dictionary.  Queries
are instanciated for (almost) each request, and most Queries
instanciate themselves automatic sub-queries which are also Query
instances.  Views serve as a model to create Queries.  A
Query represents what the user decided to do with the View.

<p>The QueryColumn currently just points to the View's Column, and the
only benefit of yesterday's change was to solve the problem of hiding
columns: if one Query decides to hide some Column, then this Column
must not be hidden also in other Queries who use the same View).

<p>But QueryColumn will contain also its own state data. For example: the
\"ColumnFilter\" on a column. Or the \"transparence\" of a column. Users
should also be able to hide columns on the fly, or to change their
order.

<p>The 'query' entry in HTTP_SESSION_VARS. It contains the 'current
query'. This is in fact the Query instance which was the main
component of the previous HTTP response page. It is currently used
only by update.php (who calls [ref
METHODS:Query.UpdateUsingPOST()]). I plan to use it also because it
would be quite difficult to propagate the state of each QueryColumn
via URL.

<p>One consequence of this will be that the contents and appearance of a
Query will partly depend on session information which is not visible
in the URL. The disadvantage of this is that you cannot bookmark such
a page. OTOH I will make a \"Save View\" button which allows to give a
name to such on-the-fly changes and store them as a View. 

<p>", "en", "Queries, Views and Columns", "2002-07-05", "Columns are the principal components of a View.
QueryColumns are the principal components of a Query.
Some words about these objects. 
", 7, 1, NULL);
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES ("<ul>
<li>PHP does not show a call stack when a run-time error occurs.  No
notion of exceptions and catching them.  This is really time-wasting
during development. I am almost more time looking for some stupid bug
than experimenting with the design.

<p><li>The Python language itself is simply better:
Possibility of using keyword arguments.
Multiple inheritance.

<p><li>
It is important to have a good API because Module code should be easy
to understand and modify, also by non-gurus.

<p><li>With Python it is possible to start thinking about a classical GUI
(not Web) user interface. Or a command-line interface.

<p><li>Possibility to integrate Lino into the WebWare application
server. 

<p></ul>

<p>Meanwhile I continue in PHP, because:

<p><ul>

<p><li>The PHP implementation is now running.  Routine and efficiency is
coming into my work.

<p><li>It would be work without visible result.
<li>People who want to
make money with Lino are quite allergic to such decisions (...nicht
wahr? ;-)
<li>Though I prefer Python, PHP is also usable and Lino itself gives
me enough fun.

<p></ul>

<p>", "en", "Switch from PHP to Python", "2002-07-05", "I seriously think about rewriting Lino in Python. Here are some
reasons.
", 7, 1, NULL);
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES ("The Application class is not necessary for the PHP implementation
since the data dictionary is completely re-created for each session
(and I don't see an easy possibility to change this). But there are
some things who have their logical place in an Application class.

<p>The first Application will be \"LinoSite\". Candidates for new
applications in the near future:
<ul>
<li>SimpleShop : modules AddressBook, Products, Business
<li>SimpleCRM : modules AddressBook, Community, Agenda
<li>QuoteManager

<p>Module and Table instances are then stored in the application. Entries
in HTTP_SESSION_VARS : 'tables' and 'modules' will go away. The new
entry 'app' contains the Application singleton.

<p>Vocabulary: An Application is a collection of Modules. Modules are
reusable Application components. Modules are currently nothing more
than a list of tables and links.

<p>I started to have an \"Administrator Menu\" which currently only points
to the initdb.php (\"Database initialization\") page. This page is meant
to show a list of available \"initialization sets\" for this
application. 

<p>", "en", "Applications", "2002-07-06", "I am going to have a new class \"Application\" because a Lino server
must be able to handle different applications.
", 7, 1, NULL);
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES ("Lino's Links are directed. They always go *from* one table
*to* another table.  There is no \"Link\" class in Lino. The method [ref
METHODS:Module.AddLink] creates two objects which together represent the
Link: a Join in the from-Table and a Detail in the to-Table. Example:
a link from NEWS to PERSONS means that each NEWS item has an \"author\"
field which points to the PERSONS table. And each PERSON has a \"News
by author\" field which shows a list with the NEWS items written by
this person.

<p>Lino has the class LinkTable which are used to represent N:M
(many-to-many) relationships.  A LinkTable are in fact Tables who
automatically will create a double Link.

<p>The most frequently used Link
is a 0,1:N (0-or-1-to-many) relationship.
This is the only one which is currently implemented.
There will be some variants:
<ul>
<li>MandatoryJoin : pointer cannot be NULL
<li>EmbeddedJoin : the referred table becomes virtually part of the
referring table. 
</ul>

<p>", "en", "What is a link?", "2002-07-06", "Some notions around the concept of a link. A link means that some
table is somehow related to some other table.
", 7, 1, NULL);
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES ("<ul>
<li>CSV is a quite practical data exchange format used by many
applications.

<p><li>pin2sql.py would then become pin2csv.py and no longer write
directly into the database.
</ul>

<p>", "en", "Importing CSV files", "2002-07-06", "I want to write an import function for CSV (comma-separated values)
files.
", 7, 1, NULL);
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES ("Tables (Vocabulary)
<ul>
<li>Products. ProductGroups. 
<li>Manufacturers : a Manufacturer is the Organization who produces a
Product. 

<p><li>Suppliers : a Supplier is an Organization (or Person) where I can
buy Products.

<p><li>Customers : a Customer is an Organization or Person who can buy my
Products.

<p><li>Partners : a Partner is either a Customer or a Supplier.

<p><li>Orders, Shipments, Invoices : these are
BusinessDocuments. BusinessDocuments have some aspects in common, and
this will be a nice application of inheritance.

<p></ul>

<p>It is better to separate Products, ProductGroups and Manufacturers
into a spearate module because there will be users who want to manage
Products with Lino, but not their BusinessDocuments.
So there will be in fact also a ProductsModule which is used by
BusinessModule. 

<p>", "en", "Brainstorming for BusinessModule", "2002-07-06", "I start to think about the BUSINESS module.
", 7, 1, NULL);
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES ("Tables : Accounts, FinancialDocuments, Movements (or what is
the usual English word to designate these transactions from one
account to another?).

<p>Accounts can be linked to a Partner or not. Each Customer and Supplier
must have an Account.

<p>In Belgium there is the PCMN (plan comptable minimum normalisé) which
is a mandatory minimum classification of the accounts to be used in a
general ledger. 

<p>", "en", "Brainstorming for AccountingModule", "2002-07-06", "I start to think about the ACCOUNTING module.
", 7, 1, NULL);
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES ("The current implementation needs a little internal change which will
have a little influence to the API.

<p>Currently a module looks like this:
<pre>
ProvidesModule('COMMUNITY');
class NEWS extends Table {
  // ...
}

<p>class COMMUNITY extends Module {
  function SetupTables() {
    $this->AddTable('NEWS');
    // ...
  }
  
  // ...
}

<p></pre>

<p>I plan to change this into::
<pre>
class NewsTable extends Table {
  // ...
}
class CommunityModule extends Module {
  function SetupTables() {
    $this->DeclareTable('NEWS',new NewsTable());
    // ...
  }
  
  // ...
}
DeclareModule('COMMUNITY',new CommunityModule());

<p></pre>

<p>Here are some reasons for this change:

<p><ul>
<li>In PHP all classes are global, and there would soon be naming
conflicts.

<p><li>Modules must be able to override existing data dictionary
definitions (which have been made by other moduls) during the
initialization.

<p></ul>

<p>", "en", "Inter-Module connectivity", "2002-07-06", "There will be a kind of inter-module connectivity. For example the
BusinessModule will work only in an Application who has also an
AddressbookModule. It uses an AddressbookModule. But it must *not*
worry about the implementation details of the address book. I will
only ask some functionality.
", 7, 1, NULL);
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES (NULL, "de", "Erstmals was Neues in Deutsch", "2002-07-08", "Yes, this news item is the first one in another language than 
English. Specifying the Language of a News item is a good case for a
listbox entry.
", 7, 1, NULL);
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES ("The view editor will be a master/detail form:

<p><pre>
 id:     PERS________
 title:  Persons_____
 filter: ____________

<p>seq  field  label      params
---  -----  ---------- -----------
  1   name  Surname    width=30
  2  fname  First Name color=green
  3  _____  __________ ___________
---  -----  ---------- -----------
</pre>

<p>Such a form contains data from two different tables (here QUERIES and
QRYCOLS). This is not yet supported. I see two approaches to manage
this situation:

<p></ul>

<p><li>
Only one table at a time is editing.
User can switch between upper and lower part of the form.
TODO:
Currently only the main component can be editing.

<p><li>Everything is editable.
TODO:
UpdateUsingPOST() must support to receive data from multiple tables.
Main Query is QUERIES, with an \"editable detail\" to QRYCOLS
</ul>

<p>", "de", "View Editor", "2002-07-09", "Okay, I start to think about the View Editor who doesn't work since
some time.
", 7, 1, NULL);
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES ("A View is a model for Queries. A View is the same for all users of an
application, while Queries are the user-specific instances of these
Views.  In fact I created the View class with performance in
mind. This is stupid. I don't need to cache this information.  The
system tables QUERIES and QRYCOLS are the persistent counterpart of a
Query. They represent the View.  If necessary, i should rather write a
CachedDatasource for these tables. But I should not use a separate
class.  Hmm.. not sure... any comments...?

<p>It is not necessary that each Query instance makes a database lookup
to know her columns. Only the \"visible\" Queries must do this.  In fact
this is not a real case of persistence since a Query knows her default
configuration if there is nothing in the QUERIES table. Currently this
table is absolutely empty and all Queries only show a default set of
columns. (And I want that this default configuration remains
satisfying in most cases, at least to create prototypes...)

<p>Idea: the Query->view property is empty if we are using the default
configuration. No lookup in QUERIES table.

<p>", "de", "Parameters for QuickTags?", "2002-07-09", "Is it useful to continue to differenciate between Columns and
QueryColumns, and between Queries and Views? Perhaps I should merge
the View class into the Query class.
", 7, 1, NULL);
INSERT INTO NEWS (body, lang_id, title, date, abstract, project_id, author_id, id) VALUES ("Note that [ref PERSONS] is almost equivalent to
[url render.php?t=PERSONS Persons].
(The difference is that the reference's label (here \"Persons\") will be
the one from data dictionary.

<p>tbc...

<p>", "de", "Parameters for QuickTags?", "2002-07-09", "Currently it is impossible to create a ref to a customized query.
QuickTags should support some parameters, similar to the direct url.
", 7, 1, NULL);
INSERT INTO PROJECTS (body, date, version_major,version_minor,version_release, responsible_id, title, sponsor_id, abstract, stopDate, id) VALUES ("Tasks
<ul>

<p><li>Get an LDAP server running on my machine.
Currently working on [url http://www.openldap.prg].

<p><li>Read more about LDAP.
[url http://www.faqs.org/rfcs/rfc2849.html RFC2849],
[url http://developer.netscape.com/docs/manuals/directory/deploy30
Netscape Directory Server Deployment Guide],
[url http://python-ldap.sourceforge.net/pydoc/ldif.html Python ldif
module], 
...

<p><li>A more simple variant of the
[ref CLASSES:ADDRBOOK AddrBook module]
which is more easy to integrate
into an LDAP connection.

<p><li>New concept of DataSupplier:
can be either SqlDataSupplier or LdapDataSupplier

<p></ul>

<p>", NULL, NULL,NULL,NULL, 1, "Addressbook connection to & from  LDAP server.", 2, "Lino would show the content stored by an LDAP server. For the user it
is not important where the data really comes from.
", NULL, 9);
INSERT INTO PRJ2PRJ (p_id,c_id) VALUES (21,21);
INSERT INTO PROJECTS (body, date, version_major,version_minor,version_release, responsible_id, title, sponsor_id, abstract, stopDate, id) VALUES ("Tasks
<ul>
<li>a logging system for the changes
<li>an XML syntax
<li>a first XML data import slot.
</ul>

<p>", NULL, NULL,NULL,NULL, 1, "Data replication", 1, "Data replication would mean that Lino logs each change in a local
database and provides possibilities to replicate such changelogs to
another database.
", NULL, 10);
INSERT INTO PRJ2PRJ (p_id,c_id) VALUES (8,8);
INSERT INTO PROJECTS (body, date, version_major,version_minor,version_release, responsible_id, title, sponsor_id, abstract, stopDate, id) VALUES ("Tasks
<ul>
<li>General presentation philopsophy
<li>View Editor does not work
<li>Quick Filter does not work
<li>Searching 
<li>Delete and Append buttons
<li>\"picker\" : Button to select a value of a JoinField
<li>Data validation
</ul>

<p>", NULL, NULL,NULL,NULL, 1, "HTML interface", 1, "There are some important details to do before the HTML interface can
be considered usable.
", NULL, 11);
INSERT INTO PRJ2PRJ (p_id,c_id) VALUES (8,8);
INSERT INTO PROJECTS (body, date, version_major,version_minor,version_release, responsible_id, title, sponsor_id, abstract, stopDate, id) VALUES ("<ul>
<li>CALENDAR as a virtual table (new class CalendarDataSupplier)
<li>DateType fields automatically link to Calendar
<li>php scripts day.php, week.php, month.php
</ul>

<p>", NULL, NULL,NULL,NULL, 1, "Calendar", 1, "A Calendar would be a user interface to manage a calendar.
With views by day, week, month.
", NULL, 12);
INSERT INTO PRJ2PRJ (p_id,c_id) VALUES (11,11);
INSERT INTO PROJECTS (body, date, version_major,version_minor,version_release, responsible_id, title, sponsor_id, abstract, stopDate, id) VALUES ("<ul>
<li>InfoCenter : Topics
<li>Business :
Products, Manufacturers,
Suppliers, Customers, Orders, Shipments, Invoices
<li>Financial : Accounts, Statements
<li>Items, Reservations
<li>PRESTO : Consultation Services
<li>
</ul>

<p>", "2002-06-28", NULL,NULL,NULL, 1, "More modules", 1, "I have a few more modules in mind which I should create so that a new
visitor can see more concretely what Lino can do.
", NULL, 13);
INSERT INTO PRJ2PRJ (p_id,c_id) VALUES (8,8);
INSERT INTO PROJECTS (body, date, version_major,version_minor,version_release, responsible_id, title, sponsor_id, abstract, stopDate, id) VALUES ("Probably create a new class Section which holds the title and number
of a section...

<p>", NULL, NULL,NULL,NULL, 1, "Pipelining", 1, "Pipelines are a step towards renderer abstraction.
BeginSection() should become visible only if there is
at least some output. If EndSection() is called before any output,
then the title should not be visible at all.
", NULL, 14);
INSERT INTO PRJ2PRJ (p_id,c_id) VALUES (11,11);
INSERT INTO PROJECTS (body, date, version_major,version_minor,version_release, responsible_id, title, sponsor_id, abstract, stopDate, id) VALUES (NULL, NULL, NULL,NULL,NULL, 1, "Internationalization (i18n)", 1, "I18N means that the User Interface is in the user's language.
", NULL, 15);
INSERT INTO PRJ2PRJ (p_id,c_id) VALUES (8,8);
INSERT INTO PROJECTS (body, date, version_major,version_minor,version_release, responsible_id, title, sponsor_id, abstract, stopDate, id) VALUES ("A BabelText and BabelMemo fields would be special fields who represent
a set of table columns which mean the same thing in different
languages.

<p>Example : if the Products table has a BabelText field \"name\", and if
the database is declared to work for languages de and fr, then the
table in the database has two independant columns name_de and
name_fr. But Lino knows that they are in fact the \"name\" column....

<p>", NULL, NULL,NULL,NULL, 1, "Multilingual applications (BabelText)", 1, "Besides Internationalization I have some ideas to support multiple
languages applications.
", NULL, 16);
INSERT INTO PRJ2PRJ (p_id,c_id) VALUES (8,8);
INSERT INTO PROJECTS (body, date, version_major,version_minor,version_release, responsible_id, title, sponsor_id, abstract, stopDate, id) VALUES (NULL, NULL, NULL,NULL,NULL, 1, "Login and User management", 1, "Of course there must also come a Login window. A Users table, possibly
retrieved from LDAP server, and an access attribution system.
", NULL, 17);
INSERT INTO PRJ2PRJ (p_id,c_id) VALUES (8,8);
INSERT INTO PROJECTS (body, date, version_major,version_minor,version_release, responsible_id, title, sponsor_id, abstract, stopDate, id) VALUES ("But that's not enough.
(todo: Sure? Bugs are just little
projects. They are sub-projects of releases...)

<p>", NULL, 0,0,14, 1, "Tables for Bugs and Releases", 1, "The APIDOC module should have separate Tables BUGS and
RELEASES. Currently they are handled as PROJECTS.
", NULL, 18);
INSERT INTO PRJ2PRJ (p_id,c_id) VALUES (8,8);
INSERT INTO PROJECTS (body, date, version_major,version_minor,version_release, responsible_id, title, sponsor_id, abstract, stopDate, id) VALUES ("<ul>
<li>query : \"please give me some data from your database\".
Parameters: table, view, slices, pagelength, page, filter,
renderer, ...
Answer: the result set.
<li>update : \"please do the following updates in your database\".
An update request must then post some data in some XML syntax
(to be specified.) 
<li>action : e.g. shutdown, database integrity check
</ul>

<p>", NULL, NULL,NULL,NULL, 1, "XML Server", 2, "Lino should be able to respond to requests.
", NULL, 19);
INSERT INTO PRJ2PRJ (p_id,c_id) VALUES (8,8);
INSERT INTO PROJECTS (body, date, version_major,version_minor,version_release, responsible_id, title, sponsor_id, abstract, stopDate, id) VALUES (NULL, NULL, NULL,NULL,NULL, 1, "Connection to & from MS-Exchange server", 2, "MS-Exchange has also an XML interface. You can then ask (e.g.)
I want to create a meeting with the following participants. Then you
can find a time and date where most participants are available, then
create the meeting. Interesting connectivity slot to be explored.
", NULL, 20);
INSERT INTO PRJ2PRJ (p_id,c_id) VALUES (21,21);
INSERT INTO PROJECTS (body, date, version_major,version_minor,version_release, responsible_id, title, sponsor_id, abstract, stopDate, id) VALUES (NULL, NULL, NULL,NULL,NULL, 1, "Connectivity", NULL, "Connectivity means to not simply import and
export many foreign file formats,
but establish a real-time connection to avoid replication.
", NULL, 21);
INSERT INTO PRJ2PRJ (p_id,c_id) VALUES (8,8);
INSERT INTO PROJECTS (body, date, version_major,version_minor,version_release, responsible_id, title, sponsor_id, abstract, stopDate, id) VALUES ("For example:
<ul>
<li>DBITEMS: MoveUp, MoveDown, MoveLeft, MoveRight to modify the
item's super and seq fields.
</ul>

<p>", NULL, NULL,NULL,NULL, 1, "Implement Actions", 1, "There is currently no Action example being used.
I should implement some actions.
", NULL, 22);
INSERT INTO PRJ2PRJ (p_id,c_id) VALUES (11,11);
INSERT INTO PROJECTS (body, date, version_major,version_minor,version_release, responsible_id, title, sponsor_id, abstract, stopDate, id) VALUES ("<tt>render.php?t=SiteSearch&qfilter=foo</tt> would then display a list
of links to records from different tables.

<p>A SiteSeach table has Fields, Details, Vurts as any other table. But
it does not get the data as any other table.

<p>But which other parameters are useful for a SiteSearch? For example
minDate (that is: don't display rows older than a certain date).
This would become a slice in the SiteSearch query.
SiteSearch table would have a field _minDate... hmmm...

<p>", NULL, NULL,NULL,NULL, 1, "SiteSearch on all tables", NULL, "I could implement a SiteSearch on all tables using a new type of
Table. This would be a first example of a table that does not map a
database table.
", NULL, 24);
INSERT INTO PRJ2PRJ (p_id,c_id) VALUES (11,11);
INSERT INTO PROJECTS (body, date, version_major,version_minor,version_release, responsible_id, title, sponsor_id, abstract, stopDate, id) VALUES ("Imagine an author who writes a short news item to be inserted
into the database. Most authors have their own preferred text editor,
which is certainly not a web form entry field.

<p>The mail body must then carry some data (for example date, title,
project_id,...) using pinboard format.
", NULL, NULL,NULL,NULL, 1, "Updating via Email", NULL, "It can be useful to provide an Email interface for updating
data.
", NULL, 25);
INSERT INTO PRJ2PRJ (p_id,c_id) VALUES (21,21);
INSERT INTO VERSIONS (release, date, major, minor) VALUES (9, "2002-06-12", 0, 0);
INSERT INTO VERSIONS (release, date, major, minor) VALUES (10, "2002-06-13", 0, 0);
INSERT INTO VERSIONS (release, date, major, minor) VALUES (11, "2002-06-22", 0, 0);
INSERT INTO VERSIONS (release, date, major, minor) VALUES (12, "2002-06-25", 0, 0);
INSERT INTO VERSIONS (release, date, major, minor) VALUES (13, "2002-06-28", 0, 0);
INSERT INTO VERSIONS (release, date, major, minor) VALUES (14, "2002-07-04", 0, 0);
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("User code
<ul>
<li>should be quite easy to understand
<li>uses only the documented functions of the Lino API,
<li>should not need modification between different Lino versions.
</ul>

<p>", "If you want to look at the Lino source files, you can split them into
two categories: (1) \"user code\" and (2) the \"Lino kernel\".
", "tour_source", "tour_userVersusKernel", "\"User\" versus \"Kernel\" code");
INSERT INTO DBITEMS (body, abstract, super_id, id, title) VALUES ("These files are Lino kernel
and must reside on the server somewhere in the PHP include path. 

<p><li>The collection of standard modules
<ul>
<li>[srcref sys.inc.php]
<li>[srcref crm.inc.php]
<li>[srcref apidoc.inc.php]
<li>[srcref docbook.inc.php]
</ul>

<p>These files are user code, but since the come with Lino they also
reside on the server somewhere in the PHP include path.

<p><li>Query actions
<ul>                 

<p><li>[srcref render.php] :
instanciates a Query and renders it.

<p><li>[srcref update.php] :
process POST data to update the currently editing Query.

<p></ul>

<p>These files are also to be considered kernel code, but
they must reside on the server in the application directory
(which is not nice).

<p><li>Application-specific files
<ul>
<li>[srcref config.inc.php]
tells Lino the database name and how to access it.
<li>[srcref modules.inc.php]
tells Lino which modules are being used for this application.
<li>[srcref index.inc.php]
</ul>

<p></ol>

<p>", "<ol>
<li>Class and function definitions :
<ul>
<li>[srcref lino.inc.php]
<li>[srcref html.inc.php]
<li>[srcref console.inc.php]
<li>[srcref mysql.inc.php]
<li>[srcref datadict.inc.php]
</ul>
", "source", "tour_files", "Lino source files");
INSERT INTO TOPICS (name_en, id) VALUES ("Apache", 1);
INSERT INTO TOPIC2TOPIC (p_id,c_id) VALUES (5,5);
INSERT INTO TOPICS (name_en, id) VALUES ("PostgreSQL", 2);
INSERT INTO TOPIC2TOPIC (p_id,c_id) VALUES (5,5);
INSERT INTO TOPICS (name_en, id) VALUES ("MySQL", 3);
INSERT INTO TOPIC2TOPIC (p_id,c_id) VALUES (5,5);
INSERT INTO TOPICS (name_en, id) VALUES ("Cygwin", 4);
INSERT INTO TOPIC2TOPIC (p_id,c_id) VALUES (8,8);
INSERT INTO TOPICS (name_en, id) VALUES ("Software", 5);
INSERT INTO TOPICS (name_en, id) VALUES ("Database", 6);
INSERT INTO TOPIC2TOPIC (p_id,c_id) VALUES (5,5);
INSERT INTO TOPICS (name_en, id) VALUES ("Web Server", 7);
INSERT INTO TOPIC2TOPIC (p_id,c_id) VALUES (5,5);
INSERT INTO TOPICS (name_en, id) VALUES ("Development tools", 8);
INSERT INTO TOPIC2TOPIC (p_id,c_id) VALUES (5,5);
