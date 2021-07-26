#!/bin/bash

declare -a repos=(
  "highlightjs/highlight.js"
)

awk -F "\"*,\"*" '{print $0}' repos_list.csv


REPOS_DATA_DIR=./repos/
for repo in "${repos[@]}"
do
  repo_dir=$(tr '/' '#' <<< "$repo")
  # If the project directory doesn't exist, make the directory and clone the project
  if [ ! -d "${REPOS_DATA_DIR}${repo_dir}" ]
  then
    mkdir ./repos/${repo_dir}
    git clone git@github.com:${repo}.git ${REPOS_DATA_DIR}${repo_dir}
  fi
done