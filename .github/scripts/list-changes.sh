#!/bin/bash

EVENT_NAME=${1:-}
BASE_SHA=${2:-}
GITHUB_SHA=${3:-}
shift 3 || true
PATHS=("$@")

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

if [ ${#PATHS[@]} -gt 0 ]; then
    echo "using pathspecs"
    CHANGED_FILES=$(git diff --name-only "$DIFF_BASE" "$DIFF_HEAD" -- "${PATHS[@]}")
else
    echo "using default diff"
    CHANGED_FILES=$(git diff --name-only "$DIFF_BASE" "$DIFF_HEAD")
fi

if [ -n "$GITHUB_OUTPUT" ]; then
    echo "output changes to github output"
    echo "changes=$CHANGED_FILES" >> $GITHUB_OUTPUT
else
    echo "GITHUB_OUTPUT is not set. THIS IS AN ISSUE"
    echo "changes=$CHANGED_FILES"
fi

PYTHON=$(echo "$CHANGED_FILES" | grep "^python/" || true)
if [ -n "$PYTHON" ]; then
    echo "python changes detected"
    PYTHON_PROJECTS=$(git diff --name-only "$DIFF_BASE" "$DIFF_HEAD" -- 'python/*' | cut -d/ -f2 | sort -u)
    echo "python projects: $PYTHON_PROJECTS"
    echo "python_projects=$PYTHON_PROJECTS" >> $GITHUB_OUTPUT
fi
JAVA=$(echo "$CHANGED_FILES" | grep "^java/" || true)
if [ -n "$JAVA" ]; then
    echo "java changes detected"
    JAVA_PROJECTS=$(git diff --name-only "$DIFF_BASE" "$DIFF_HEAD" -- 'java/*' | cut -d/ -f2 | sort -u)
    echo "java projects: $JAVA_PROJECTS"
    echo "java_projects=$JAVA_PROJECTS" >> $GITHUB_OUTPUT
fi
JAVASCRIPT=$(echo "$CHANGED_FILES" | grep "^javascript/" || true)
if [ -n "$JAVASCRIPT" ]; then
    echo "javascript changes detected"
    JAVASCRIPT_PROJECTS=$(git diff --name-only "$DIFF_BASE" "$DIFF_HEAD" -- 'javascript/*' | cut -d/ -f2 | sort -u)
    echo "javascript projects: $JAVASCRIPT_PROJECTS"
    echo "javascript_projects=$JAVASCRIPT_PROJECTS" >> $GITHUB_OUTPUT
fi
OTHER=$(echo "$CHANGED_FILES" | grep -Ev '^(python|java|javascript)/' || true)
if [ -n "$OTHER" ]; then
    echo "other changes detected"
    echo "other_files=$OTHER" >> $GITHUB_OUTPUT
fi

echo "python=$PYTHON"
echo "java=$JAVA"
echo "javascript=$JAVASCRIPT"
echo "other=$OTHER"