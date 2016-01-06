.. _team.workflow:

Deployment workflow
===================

-  **Stable**.  The normal state of a production site.

   Any problems reported by users are collected as tickets. Users get
   a regular report about the "known problems" on their site ("liste
   des erreurs en cours de résolution").

   In Noi we have a milestone labelled "coming" for each site. When a
   tickets is done, then we create a "deployment" for this milestone
   on this ticket.

   Users can ask at any moment to start a release. This happens when
   they decided that the advantage of having these tickets solved is
   worth the work and risks caused by a release.

-  **Preview**. We installed the latest version on their testing
   environment.  Users are now invited to test that preview and to
   report their observations.

   After some time of preview, the users declare that the preview is
   okay and that they want it to go into production.

-  **After release** -- We upgrade their production environment to use
   the version which has been in preview so far. During some time we
   concentrate on removing any side effects and keep ready to react to
   potential regression reports which might occur (because our test
   suite ha not 100% coverage and because end-users didn't test
   perfectly).

   There can be additional updates during the next days which are
   added to that same deployment in Noi.

   After some time there are no more regressions and side effects
   reported: we return to the **Stable** operation mode. This is the
   moment to decide whether an official release (on PyPI) of the
   involved projects makes sense.

