#!/bin/bash

EVENT_NAME=${1:-}
BASE_SHA=${2:-}
GITHUB_SHA=${3:-}

if [ "$EVENT_NAME" = "pull_request" ]; then
    CHANGED_FILES=$(git diff --name-only $BASE_SHA $GITHUB_SHA)
else
    CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD)
fi

# Output for GitHub Actions
if [ -n "$GITHUB_OUTPUT" ]; then
    echo "changes=$CHANGED_FILES" >> "$GITHUB_OUTPUT"
else
    echo "changes=$CHANGED_FILES"
fi
