#!/bin/bash
# Safe version with backup
for file in *.py; do
    if [ -f "$file" ]; then
        if ! head -1 "$file" | grep -q "^#!/"; then
            echo "Adding shebang to $file (backup created as $file.bak)"
            cp "$file" "$file.bak"
            sed -i '1i#!/usr/bin/env python3' "$file"
        else
            echo "Shebang already exists in $file"
        fi
    fi
done
