==================
My Git cheat sheet
==================

.. highlight:: bash


Contributing pull requests to foreign projects
----------------------------------------------

The explanation was that I need to fork the project on GitHub (using
their web interface) and then::

    $ git clone git@github.com:lsaffre/ablog.git
    $ e ablog/__init__.py  # Make my modifs
    $ git checkout -b feed_encoding
    $ git commit -m "Added encoding utf-8 to file atom.xml"
    $ git push origin feed_encoding 
    Total 0 (delta 0), reused 0 (delta 0)
    To git@github.com:lsaffre/ablog.git
     * [new branch]      feed_encoding -> feed_encoding

Now their web interface sees my commit and allows me to turn it into
pull request.
    
Later I made also this::
    
    $ git remote add upstream git@github.com:abakan/ablog.git
    $ git pull upstream master

(Thanks to `Git branches tutorial
<https://www.atlassian.com/git/tutorial/git-branches>`_,
`stackoverflow
<http://stackoverflow.com/questions/6286571/git-fork-is-git-clone>`_
and `Collaboration on Github
<http://www.eqqon.com/index.php/Collaborative_Github_Workflow>`_)
    


Merge from upstream
--------------------

Ahmet made changes in ablog to support `multiple postings per document
<https://github.com/abakan/ablog/issues/4>`_ and asked me to test
them.  So I needed to merge his changes into the local copy of my fork.
The GitHub help section about `Syncing a fork
<https://help.github.com/articles/syncing-a-fork>`_ worked like a
charm for me::

    $ git fetch upstream
    $ git checkout master
    $ git merge upstream/master


Select a branch
---------------

:: 
   
    $ git checkout master


Merge from upstream while local branch active
---------------------------------------------

I had started a branch in my local copy of ablog::

    $ git status
    On branch trans_estonian
    nothing to commit, working directory clean
    $ git push origin trans_estonian 
    Everything up-to-date
