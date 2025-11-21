#!/bin/bash

# Legal header text
LEGAL_HEADER='"""
RF Scanner AI - Educational Use Only
====================================
WARNING: This software is for EDUCATIONAL and RESEARCH purposes only.

PROHIBITED: Illegal surveillance, privacy violation, unauthorized access
LEGAL: Users must comply with all applicable laws and regulations

Developer: Shahnawaz Khurram - Signal Research Lab
Contact: signalresearchlab@gmail.com
"""'

# Add to all Python files
for file in *.py; do
    if [ -f "$file" ]; then
        # Check if header already exists
        if ! grep -q "RF Scanner AI - Educational Use Only" "$file"; then
            # Create temporary file with header
            temp_file=$(mktemp)
            echo "$LEGAL_HEADER" > "$temp_file"
            cat "$file" >> "$temp_file"
            mv "$temp_file" "$file"
            echo "✅ Added legal header to: $file"
        else
            echo "⚠️  Header already exists in: $file"
        fi
    fi
done

echo "🎉 Legal headers added to all Python files!"
