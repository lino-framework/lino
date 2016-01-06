.. _team.enduser_testing:
.. _team.testing:

=========================
The `testing` environment
=========================

On certain customer sites it can be useful to provide a separate
"testing" site of their application.

This is a subdomain with its own Python environment and database.  It
can be used for end-user driven tests before a release.  End-user
tests usually don't reveil important regressions (though that might
happen).  The primary goal of such a setup is more social than
technical: it encourages the local Lino community to develop a sane
communication culture for discussing about new features, and
priorities.

This setup introduces an official :doc:`workflow`.
