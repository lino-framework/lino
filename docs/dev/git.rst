==================
My Git cheat sheet
==================

.. highlight:: bash


Make a pull request
-------------------

- http://git-scm.com/book/en/Distributed-Git-Contributing-to-a-Project
- https://help.github.com/articles/creating-a-pull-request



Branching
---------

My summary after reading the `Branching
<http://git-scm.com/book/en/Git-Branching>`_ chapter of Scott Chacon's
Pro Git book:

- *master* : the default branch which will be selected after cloning
  your repo.

- *HEAD* : pointer to the "current branch" (the one that is checked out).

- Create a new branch called "20141022":  ``git branch 20141022``
- Select a branch : ``git checkout 20141022``
- Shortcut to create and select : ``git checkout -b 20141022``
- List all branches: ``git branch`` (``*`` indicates the HEAD)
- See which branches are already merged into HEAD : ``git branch --merged``
- See all the branches that contain work you haven’t yet merged :
  ``git branch --merged``
- Merge a branch into current branch:  ``git merge 20141022``
  (in case of a merge conflict, start reading at `Basic Merge Conflicts <http://git-scm.com/book/en/Git-Branching-Basic-Branching-and-Merging#Basic-Merge-Conflicts>`_)

- Delete a branch: ``git branch -d 20141022``
- Common names for *long-term branches*: *develop*, *proposed*, *next*.


Remote branches
---------------

When you want to share a branch with the world, you need to push it up
to a remote that you have write access to.

- Remote branches : ``(remote)/(branch)``

TODO: Continue to read 
http://git-scm.com/book/en/Git-Branching-Remote-Branches


Contributing pull requests to foreign projects
----------------------------------------------

Most projects don't use the "shared repository model" (several users
writing to a repo) but the "fork & pull" model as explained in `Using
pull requests <https://help.github.com/categories/collaborating/>`_).

Example: I have a fork of Ahmet's ablog project.  Ahmet made changes
in ablog and asked me to test them.  So I need to merge his changes
into the local copy of my fork.

So if I want to contribute to Ahmet's ablog project, I need to fork
the project on GitHub (using their web interface) and then get a clone
of this fork::

    $ git clone git@github.com:lsaffre/ablog.git

Now I make my changes::

    $ e ablog/__init__.py 

When I decided that I want to share my local changes, I create a
branch, commit it and push it to *my* repo::

    $ git checkout -b feed_encoding
    $ git commit -m "Added encoding utf-8 to file atom.xml"
    $ git push origin feed_encoding 

Now their web interface sees my branch and allows me to turn it into a
pull request.
    

Merge from upstream
--------------------

Every local project repository has a set of *tracked repositories*,
also called "remotes".  The default remote (the place from where my
local repo has been taken) is called **origin**.

List all remotes::

  $ git remote -v
  origin   git@github.com:lsaffre/ablog.git (fetch)
  origin   git@github.com:lsaffre/ablog.git (push)

First I must add Ahmet's repo as a new remote, which is usually called
**upstream**::
    
    $ git remote add upstream git@github.com:abakan/ablog.git

My local repo now has two remotes::

    $ git remote -v
    origin	git@github.com:lsaffre/ablog.git (fetch)
    origin	git@github.com:lsaffre/ablog.git (push)
    upstream	git@github.com:abakan/ablog.git (fetch)
    upstream	git@github.com:abakan/ablog.git (push)


Now I can fetch all changes from the upstream repository::

    $ git fetch upstream

Before continuing, make sure where you want the changes from upstream
to go. Usually you want them to go to `master`, so you must select
this branch::

    $ git checkout master

And finally I can merge them into my local repo::

    $ git merge upstream/master

`fetch upstream` looks up the specified remote, fetches any data from
it that you don’t yet have, and updates your local database, moving
your ``upstream/master`` pointer to its new position.




TODO: 

- How to return back to my local changes?

- What was this?

  ::

    $ git pull upstream master



Merge from upstream while local branch active
---------------------------------------------

I had started a branch in my local copy of ablog::

    $ git status
    On branch trans_estonian
    nothing to commit, working directory clean
    $ git push origin trans_estonian 
    Everything up-to-date



Accept a pull request
---------------------

Example: cuchac posted a pull request for a branch which he named
``export_excel_datetime`` (on his fork of my project `lino`).

Check that there are no local changes in my repo::

    $ go lino
    $ git status
    On branch master
    Your branch is up-to-date with 'origin/master'.
    nothing to commit, working directory clean

Check out his branch into a new branch ``inbox`` in order to test the
changes::

    $ git checkout -b inbox master
    $ git pull git@github.com:cuchac/lino.git export_excel_datetime
    remote: Counting objects: 6, done.
    remote: Compressing objects: 100% (3/3), done.
    remote: Total 6 (delta 4), reused 5 (delta 3)
    Unpacking objects: 100% (6/6), done.
    From github.com:cuchac/lino
     * branch            export_excel_datetime -> FETCH_HEAD
    Merge made by the 'recursive' strategy.
     lino/modlib/export_excel/models.py | 21 +++++++++++++++++++--
     1 file changed, 19 insertions(+), 2 deletions(-)
    
Test the changes::
    
    $ fab test
    [localhost] local: python setup.py -q test
    ...........................................
    ----------------------------------------------------------------------
    Ran 43 tests in 36.290s

    OK

    Done.

Reactivate master and merge the changes::

    $ git checkout master
    M	docs/tutorials/pisa/pisa.Person-1.pdf
    Switched to branch 'master'
    Your branch is up-to-date with 'origin/master'.
    
    $ git merge --no-ff inbox
    Merge made by the 'recursive' strategy.
     lino/modlib/export_excel/models.py | 21 +++++++++++++++++++--
     1 file changed, 19 insertions(+), 2 deletions(-)
    
Note: is the ``--no-ff`` option necessary?

Push everything to the master::    
    
    $ git push origin master
    Counting objects: 43, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (11/11), done.
    Writing objects: 100% (11/11), 1.39 KiB | 0 bytes/s, done.
    Total 11 (delta 8), reused 0 (delta 0)
    To git@github.com:lsaffre/lino.git
       988adf9..55961b9  master -> master

And finally delete the ``inbox`` branch::

    $ git branch -v --merged
      inbox  bfd3f39 Merge branch 'export_excel_datetime' of github.com:cuchac/lino into inbox
    * master 55961b9 Merge branch 'inbox'
    
    $ git branch -d inbox
    Deleted branch inbox (was bfd3f39).


Bibliography
------------

- `Git branches tutorial
  <https://www.atlassian.com/git/tutorial/git-branches>`_

- `stackoverflow
  <http://stackoverflow.com/questions/6286571/git-fork-is-git-clone>`_

- `Collaboration on Github
  <http://www.eqqon.com/index.php/Collaborative_Github_Workflow>`_)
  
- GitHub help:
  `Fork a repo <https://help.github.com/articles/fork-a-repo/>`_,
  `Syncing a fork <https://help.github.com/articles/syncing-a-fork>`_.

