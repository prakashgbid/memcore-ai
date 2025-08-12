#!/bin/bash
# Build PyPI packages for all modules

echo "🏗️ Building PyPI packages for all modules..."

# Array of modules
modules=(
    "self-learning"
    "deep-reasoner"
    "auto-coder"
    "smart-planner"
    "o-s-a-autonomous"
    "langgraph-orchestrator"
    "persistent-ai-memory"
)

# Build each module
for module in "${modules[@]}"; do
    echo "📦 Building $module..."
    cd "/Users/MAC/Documents/projects/omnimind/modules/$module"
    
    # Clean previous builds
    rm -rf dist/ build/ *.egg-info
    
    # Build the package
    python3 -m pip install --upgrade build
    python3 -m build
    
    echo "✅ Built $module"
done

echo "🎉 All packages built successfully!"
echo "📝 To upload to PyPI, run: python3 -m twine upload dist/*"