#!/bin/bash
echo "=== Preparing files for GitHub upload ==="

# 1. Add shebang to Python files
echo "1. Adding shebang to Python files..."
for file in *.py; do
    if [ -f "$file" ] && ! head -1 "$file" | grep -q "^#!/"; then
        sed -i '1i#!/usr/bin/env python3' "$file"
        echo "  ✓ Fixed: $file"
    fi
done

# 2. Make all scripts executable
echo "2. Making scripts executable..."
chmod +x *.py *.sh

# 3. Verify changes
echo "3. Verifying permissions..."
ls -la *.py *.sh | head -10

# 4. Create .gitignore if missing
if [ ! -f .gitignore ]; then
    echo "4. Creating .gitignore..."
    cat > .gitignore << 'GITIGNORE'
# Virtual environments
.venv/
venv/
env/

# Python cache
__pycache__/
*.py[cod]
*$py.class

# Build artifacts
*.egg-info/
build/
dist/

# Environment variables
.env
.secrets

# OS files
.DS_Store
Thumbs.db
GITIGNORE
    echo "  ✓ Created .gitignore"
fi

echo "=== Setup complete! Ready for GitHub upload ==="
