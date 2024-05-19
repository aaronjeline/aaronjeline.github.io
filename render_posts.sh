#!/bin/bash

function render_post {
    if [[ -z "$1" ]]; then
        echo "Usage: $0 <post_to_render>"
        exit 1
    fi
    echo "Rendering: $1"
    post_name=$(basename "$1" .md)
    pandoc "posts_md/$1" -o "renders/posts/$post_name.html"
    python3 ./render.py "posts_md/$1" "renders/posts/$post_name.html" "posts/$post_name.html"
}

. ./venv/bin/activate

for post in $(ls posts_md); do
    render_post "$post"
done
