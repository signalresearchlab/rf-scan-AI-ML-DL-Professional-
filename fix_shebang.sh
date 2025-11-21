#!/bin/bash
# Add Python shebang to files that don't have it
for file in *.py; do
    if [ -f "$file" ]; then
        if ! head -1 "$file" | grep -q "^#!/"; then
            echo "Adding shebang to $file"
            sed -i '1i#!/usr/bin/env python3' "$file"
        else
            echo "Shebang already exists in $file"
        fi
    fi
done
