#!/usr/bin/env bash
# Configures GitHub repo settings after the first push:
#   - Squash merge only (no merge commits, no rebase)
#   - Branch protection on main: require PR + tests to pass, no direct pushes
#
# Usage: ./setup-github.sh <owner/repo>
# Requires: gh CLI authenticated (gh auth login)

set -euo pipefail

REPO="${1:?Usage: ./setup-github.sh owner/repo}"

echo "Configuring $REPO..."

# Squash-merge only
gh api "repos/$REPO" --method PATCH \
  --field allow_squash_merge=true \
  --field allow_merge_commit=false \
  --field allow_rebase_merge=false \
  --field squash_merge_commit_title=PR_TITLE \
  --field squash_merge_commit_message=PR_BODY \
  --silent
echo "✅  Squash merge only."

# Branch protection on main:
#   - Require PR before merging (blocks direct pushes)
#   - Required status check: "Run tests" job from pr-checks.yml
#     GitHub formats the context as: "PR Checks / Run tests"
#   - Linear history (consistent with squash-only)
gh api "repos/$REPO/branches/main/protection" --method PUT \
  --header "Accept: application/vnd.github+json" \
  --input - <<'JSON'
{
  "required_status_checks": {
    "strict": true,
    "checks": [
      { "context": "Run tests" }
    ]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "required_approving_review_count": 0,
    "dismiss_stale_reviews": false
  },
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON
echo "✅  Branch protection on main: PRs required, tests must pass, no direct pushes."

echo ""
echo "Done. Push a PR to verify the 'Run tests' check appears before merging."
echo ""
echo "Note: if the required check context doesn't match, find the exact string"
echo "under a PR's Checks tab and update the 'context' value in this script."
