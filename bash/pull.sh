set -e

function pull_here() {
  pwd
  git pull
  find -name '*.pyc' -exec rm -f {} +
}

REPOS=/path/to/your/repositories

cd $REPOS/lino ; pull_here
cd $REPOS/xl ; pull_here
cd $REPOS/cosi ; pull_here
cd $REPOS/voga ; pull_here

