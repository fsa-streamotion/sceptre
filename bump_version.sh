#!/usr/bin/env bash

set -o errexit

usage() {
  echo "Usage: $0 VERSION [PART]"
  echo "e.g. $0 2.10.0"
  echo "e.g. $0 3.0.0 major"
  exit 1
}

get_opts() {
  [ -z "$1" ] && usage
  version="$1"
  part="minor"
  [ -n "$2" ] && part="$2" 
}

validate_opts() {
  if ! grep -Eq '^\d+\.\d+\.\d+$' <<< "$version" ; then
    echo "Version '$version' looks wrong"
    usage
  fi

  if ! grep -wq "$part" <<< "major minor" ; then
    echo "Part '$part' looks wrong, should be major or minor"
    usage
  fi
}

release() {
  local branch_name="release-$(tr -d "." <<< "$version")"

  git co -b "$branch_name"
  bumpversion --new-version "$version" "$part"
  git push origin "$branch_name"

  echo "\
Now raise a PR:
https://github.com/fsa-streamotion/sceptre/compare/\
develop...fsa-streamotion:$branch_name?expand=1"
}

main() {
  get_opts "$@"
  validate_opts
  release
}

if [ "$0" == "${BASH_SOURCE[0]}" ] ; then
  main "$@"
fi
