Templates (obsolete)
====================

URL                    View                           Templates
---------------------- ------------------------------ ----------------------------
...?fmt=view&row=n     ViewReportRenderer.view_one    tom/page_show_html
...?fmt=view           ViewReportRenderer.view_many   tom/grid_show.html
---------------------- ------------------------------ ----------------------------
...?fmt=form&row=n     FormReportRenderer.view_one    tom/page_edit_html
...?fmt=form           FormReportRenderer.view_many   tom/grid_edit.html
---------------------- ------------------------------ ----------------------------
/edit/APP/MODEL/1      Reports.edit_instance          tom/instance.html
---------------------- ------------------------------ ----------------------------
/menu/...              Menu.view                      tom/menu.html