#!/bin/bash

if [ "${{ github.event_name }}" = "pull_request" ]; then
    CHANGED_FILES=$(git diff --name-only ${{ github.event.pull_request.base.sha }} ${{ github.sha }})
else
    CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD)
fi

echo "changes=$CHANGED_FILES" >> $GITHUB_OUTPUTs
