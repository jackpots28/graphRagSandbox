#!/bin/bash
for f in $(git diff --name-only --cached); do
    if [[ $f == *.ipynb ]]; then
        jupyter nbconvert --clear-output --inplace $f
        git add $f
    fi
done

if git diff --name-only --cached --exit-code
then
    echo "No changes detected after removing notebook output"
    exit 1
fi

