.. _team.enduser_testing:

=======================================
Deployment process using end-user tests
=======================================

On certain customer sites it can be useful to provide a separate
"testing" site of their application.

This is a subdomain with its own Python environment and database.  It
can be used for end-user driven tests before a release. 

End-user tests usually don't reveil important regressions (though that
might happen).  The primary goal of such a setup is more social than
technical: it encourages the local Lino community to develop a sane
communication culture for discussing about new features, and
priorities.

This setup introduces an official "Deployment workflow":

a) "Stable".  The normal state of a production site. 

   Any problems reported by users are collected as tickets. Users get
   a regular report about the "known problems" on their site ("liste
   des erreurs en cours de résolutions").

   In Noi we have a milestone labelled "coming" for each site. When a
   tickets is done, then we create a deployment for this milestone on
   this ticket.  

b) "Preview". We installed the latest version on their test
   environment. Users are now invited to try out that preview.  

c) "After release". We upgrade their production environment to use the
   version which has been in preview so far. During some time we
   concentrate on removing any side effects. There can be additional
   updates during the next days which are added to that same
   deployment in Noi.


a -> b

   Users can ask at any moment to start a release. This happens when
   they decided that the advantage of having these tickets solved is
   worth the work and risks caused by a release.

b -> c

   After some time of preview, the users declare that the preview is
   okay and that they want it to go into production.


c -> a

   After some time there are no more regressions and side effects
   reported.

   
