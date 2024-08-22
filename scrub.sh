#!/bin/bash
for file in $(git diff --name-only --cached); do
    if [[ "${file}" == *.ipynb ]]; then
        jupyter nbconvert --clear-output --inplace "${file}"
        git add "${file}"
    fi
done

if git diff --name-only --cached --exit-code
then
    echo "No changes detected after removing notebook output"
    exit 1
fi

