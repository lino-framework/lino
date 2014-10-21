==================
My Git cheat sheet
==================

.. highlight:: bash


Contributing pull requests to foreign projects
----------------------------------------------

Most projects don't use the "shared repository model" (several users
writing to a repo) but the "fork & pull" model as explained in `Using
pull requests <https://help.github.com/categories/collaborating/>`_).

So if I want to contribute to Ahmed's ablog project, I need to fork
the project on GitHub (using their web interface) and then::

    $ git clone git@github.com:lsaffre/ablog.git

I.e. I make a clone of *my* ablog repository (which is a fork of the
original repository).

Now I make my modifs::

    $ e ablog/__init__.py 

I create a branch, commit it and push it to *my* repo::

    $ git checkout -b feed_encoding
    $ git commit -m "Added encoding utf-8 to file atom.xml"
    $ git push origin feed_encoding 
    Total 0 (delta 0), reused 0 (delta 0)
    To git@github.com:lsaffre/ablog.git
     * [new branch]      feed_encoding -> feed_encoding

Now their web interface sees my commit and allows me to turn it into
pull request.
    
Merge from upstream
--------------------

Ahmet made changes in ablog to support `multiple postings per document
<https://github.com/abakan/ablog/issues/4>`_ and asked me to test
them.  So I needed to merge his changes into the local copy of my
fork.  This is called `Syncing a fork
<https://help.github.com/articles/syncing-a-fork>`_.

Every local project repository has a set of *tracked repositories*,
also called "remotes".  The default remote is called "origin"
(i.e. the place from where this repo has been cloned)::

  $ git remote -v
  origin   git@github.com:lsaffre/ablog.git (fetch)
  origin   git@github.com:lsaffre/ablog.git (push)

First I must add Ahmed's repo as a new remote, which is usually called
"upstream"::
    
    $ git remote add upstream git@github.com:abakan/ablog.git

My local repo now has two remotes::

    $ git remote -v
    origin	git@github.com:lsaffre/ablog.git (fetch)
    origin	git@github.com:lsaffre/ablog.git (push)
    upstream	git@github.com:abakan/ablog.git (fetch)
    upstream	git@github.com:abakan/ablog.git (push)

If I have local changes, I must check out the master before
continuing::

    $ git checkout master

Now I can fetch all changes from the upstream repository::

    $ git fetch upstream

And merge them into my local repo::

    $ git merge upstream/master


TODO: 

- How to return back to my local changes?

- What was this?

  ::

    $ git pull upstream master


Select a branch
---------------

Here is how to select the master branch:: 
   
    $ git checkout master


Merge from upstream while local branch active
---------------------------------------------

I had started a branch in my local copy of ablog::

    $ git status
    On branch trans_estonian
    nothing to commit, working directory clean
    $ git push origin trans_estonian 
    Everything up-to-date

Bibliography
------------

- `Git branches tutorial
  <https://www.atlassian.com/git/tutorial/git-branches>`_

- `stackoverflow
  <http://stackoverflow.com/questions/6286571/git-fork-is-git-clone>`_

- `Collaboration on Github
  <http://www.eqqon.com/index.php/Collaborative_Github_Workflow>`_)
  
- GitHub help 
  `Fork a repo <https://help.github.com/articles/fork-a-repo/>`_  


