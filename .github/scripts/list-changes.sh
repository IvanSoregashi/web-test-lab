#!/bin/bash

EVENT_NAME=${1:-}
BASE_SHA=${2:-}
GITHUB_SHA=${3:-}

echo "detecting changes in $EVENT_NAME"

if [ -n "$BASE_SHA" ] && [ -n "$GITHUB_SHA" ]; then
    echo "assuming pull request event"
    DIFF_BASE="$BASE_SHA"
    DIFF_HEAD="$GITHUB_SHA"
else
    echo "assuming push or unknown event"
    DIFF_BASE="HEAD~1"
    DIFF_HEAD="HEAD"
fi

CHANGED_FILES=$(git diff --name-only "$DIFF_BASE" "$DIFF_HEAD")
echo "changed files: $CHANGED_FILES"

OTHER=$(echo "$CHANGED_FILES" | grep -Ev '^(python|java|javascript)/' || true)
if [ -n "$OTHER" ]; then
    echo "other changes detected"
    echo "other_files=$OTHER" >> $GITHUB_OUTPUT
fi

PYTHON_PROJECTS=$(git diff --name-only "$DIFF_BASE" "$DIFF_HEAD" -- 'python/*/**' \
                | cut -d/ -f2 | sort -u \
                | jq -R -s -c 'split("\n") | map(select(length>0))')
echo "python projects: $PYTHON_PROJECTS"
echo "python_projects=$PYTHON_PROJECTS" >> $GITHUB_OUTPUT

JAVA_PROJECTS=$(git diff --name-only "$DIFF_BASE" "$DIFF_HEAD" -- 'java/*/**' \
                | cut -d/ -f2 | sort -u \
                | jq -R -s -c 'split("\n") | map(select(length>0))')
echo "java projects: $JAVA_PROJECTS"
echo "java_projects=$JAVA_PROJECTS" >> $GITHUB_OUTPUT

JAVASCRIPT_PROJECTS=$(git diff --name-only "$DIFF_BASE" "$DIFF_HEAD" -- 'javascript/*/**' \
                | cut -d/ -f2 | sort -u \
                | jq -R -s -c 'split("\n") | map(select(length>0))')
echo "javascript projects: $JAVASCRIPT_PROJECTS"
echo "javascript_projects=$JAVASCRIPT_PROJECTS" >> $GITHUB_OUTPUT
