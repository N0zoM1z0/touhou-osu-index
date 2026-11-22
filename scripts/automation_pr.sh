#!/usr/bin/env bash
# Commit regenerated catalog shards to an automation branch, open or update
# its review PR, and dispatch CI for it.
#
# usage: scripts/automation_pr.sh BRANCH TITLE COMMIT_MESSAGE BODY_FILE
#
# Pushes made with GITHUB_TOKEN do not start pull_request workflows (they end
# in "action_required"), so this script dispatches Validate and a structural
# Deep review on the branch explicitly. workflow_dispatch is exempt from that
# restriction and its checks attach to the PR head commit.
set -euo pipefail

if [[ $# -ne 4 ]]; then
  echo "usage: $0 BRANCH TITLE COMMIT_MESSAGE BODY_FILE" >&2
  exit 2
fi
branch=$1
title=$2
commit_message=$3
body_file=$4

git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git switch -c "$branch"
git add -A data/catalog
git commit -q -m "$commit_message"

pushed=true
if git fetch -q --no-tags --depth=1 origin "refs/heads/$branch" 2>/dev/null \
  && [[ "$(git rev-parse FETCH_HEAD:data/catalog)" == "$(git rev-parse HEAD:data/catalog)" ]]; then
  # Re-pushing identical data only creates a new SHA, which invalidates
  # reviews and re-runs CI for no reason.
  echo "::notice::$branch already proposes this exact catalog; skipping push."
  pushed=false
else
  git push -q --force origin "HEAD:refs/heads/$branch"
fi

pr_number=$(gh pr list --head "$branch" --state open --json number --jq '.[0].number // empty')
if [[ -n "$pr_number" ]]; then
  gh pr edit "$pr_number" --title "$title" --body-file "$body_file"
else
  gh pr create --base main --head "$branch" --title "$title" --body-file "$body_file"
fi

if [[ "$pushed" == true ]]; then
  gh workflow run validate.yml --ref "$branch"
  gh workflow run deep-review.yml --ref "$branch" \
    -f mode=structural \
    -f ref="$branch" \
    -f base_ref=main \
    -f scope=changed \
    -f forbid_existing_changes=false
fi
