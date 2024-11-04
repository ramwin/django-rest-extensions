#!/bin/bash
# Xiang Wang(ramwin@qq.com)

if [ -d _build ]
then
    rm -r _build
fi

sphinx-autobuild \
    -j auto \
    --port 18011 \
    . _build/html/ \
    --re-ignore "\.mypy_cache" \
    --re-ignore "\.git"    \
    --re-ignore "\.*\.swp"
