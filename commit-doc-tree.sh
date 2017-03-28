#!/bin/bash

# Script to automatically generate documentation and commit this to the gh-pages
# branch.

# check, if index is empty
if ! git diff-index --cached --quiet --ignore-submodules HEAD ; then
  echo "Fatal: cannot work with indexed files!"
  exit 1
fi

docdirectory=$(git config gh-pages.dir)
if [ -z "$docdirectory" ]; then
    echo "Fatal: git config gh-pages.dir not found"
    exit 2
fi

if $(git rev-parse gh-pages &>/dev/null); then
    localbranch="$(git rev-parse gh-pages 2>/dev/null)"
    remotebranch="$(git rev-parse $(git config branch.gh-pages.remote)/gh-pages 2>/dev/null)"
    if [[ -n $localbranch && -n $remotebranch && $localbranch != $remotebranch ]]; then
        echo "Fatal: local branch 'gh-pages' and "\
             "remote branch '$(git config  branch.gh-pages.remote)' are out of sync!"
        exit 3
    fi
fi    

# get the 'git describe' output
git_describe=$(git describe --always)

# Add the doc files to the index
git add -f $docdirectory

# write a tree using the current index
tree=$(git write-tree --prefix=$docdirectory)

# we’ll have a commit
if $(git rev-parse gh-pages &>/dev/null); then
    commit=$(echo "site generated from $git_describe" | git commit-tree $tree -p gh-pages)

    # move the branch to the commit we made, i.e. one up
    git update-ref refs/heads/gh-pages $commit
else
    commit=$(echo "site generated from $git_describe" | git commit-tree $tree)
    git branch gh-pages $commit
fi

# clean index
git reset HEAD

# print the commit message
git log -1 --oneline gh-pages
