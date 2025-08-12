#!/bin/bash

# Rebranding script for all projects

declare -A projects=(
    ["self-learning"]="evolux:evolux-ai:Evolux:Self-evolving AI that learns and improves continuously"
    ["deep-reasoner"]="cognitron:cognitron-engine:Cognitron:Advanced multi-layer reasoning engine for complex problem solving"
    ["auto-coder"]="codeforge:codeforge-ai:CodeForge:Intelligent code generation and self-modification framework"
    ["smart-planner"]="strategix:strategix-planner:Strategix:Intelligent task planning and execution orchestrator"
    ["o-s-a-autonomous"]="autonomix:autonomix-engine:Autonomix:Self-directed decision engine for autonomous systems"
    ["langgraph-orchestrator"]="flowmaster:flowmaster-orchestrator:FlowMaster:Advanced workflow orchestration for multi-agent systems"
    ["persistent-ai-memory"]="memcore:memcore-ai:MemCore:Persistent memory system for intelligent applications"
)

for module_dir in "${!projects[@]}"; do
    IFS=':' read -r package_name repo_name project_name description <<< "${projects[$module_dir]}"
    
    echo "🔄 Rebranding $module_dir to $project_name..."
    
    cd "/Users/MAC/Documents/projects/omnimind/modules/$module_dir"
    
    # Update setup.py
    if [ -f "setup.py" ]; then
        sed -i '' "s/o-s-a-autonomous/$package_name/g" setup.py
        sed -i '' "s/o_s_a_autonomous/${package_name//-/_}/g" setup.py
        sed -i '' "s/osa-.*/$repo_name/g" setup.py
        sed -i '' "s/OSA Contributors/$project_name Team/g" setup.py
        sed -i '' "s/osa@omnimind.ai/team@$package_name.ai/g" setup.py
        sed -i '' "s/Extracted from OSA/$description/g" setup.py
        sed -i '' "s/OSA.*project/$description/g" setup.py
    fi
    
    # Update pyproject.toml
    if [ -f "pyproject.toml" ]; then
        sed -i '' "s/adaptive-learner/$package_name/g" pyproject.toml
        sed -i '' "s/adaptive_learner/${package_name//-/_}/g" pyproject.toml
        sed -i '' "s/deep-reasoner/$package_name/g" pyproject.toml
        sed -i '' "s/deep_reasoner/${package_name//-/_}/g" pyproject.toml
        sed -i '' "s/auto-coder/$package_name/g" pyproject.toml
        sed -i '' "s/auto_coder/${package_name//-/_}/g" pyproject.toml
        sed -i '' "s/smart-planner/$package_name/g" pyproject.toml
        sed -i '' "s/smart_planner/${package_name//-/_}/g" pyproject.toml
        sed -i '' "s/o-s-a-autonomous/$package_name/g" pyproject.toml
        sed -i '' "s/o_s_a_autonomous/${package_name//-/_}/g" pyproject.toml
        sed -i '' "s/langgraph-orchestrator/$package_name/g" pyproject.toml
        sed -i '' "s/langgraph_orchestrator/${package_name//-/_}/g" pyproject.toml
        sed -i '' "s/persistent-ai-memory/$package_name/g" pyproject.toml
        sed -i '' "s/persistent_ai_memory/${package_name//-/_}/g" pyproject.toml
        sed -i '' "s/OSA Contributors/$project_name Team/g" pyproject.toml
        sed -i '' "s/osa@omnimind.ai/team@$package_name.ai/g" pyproject.toml
    fi
    
    # Update README.md
    if [ -f "README.md" ]; then
        cat > README.md << EOF
# $project_name

$description

## Installation

\`\`\`bash
pip install $package_name
\`\`\`

Or install from source:

\`\`\`bash
git clone https://github.com/prakashgbid/$repo_name.git
cd $repo_name
pip install -e .
\`\`\`

## Quick Start

\`\`\`python
from $package_name import core

# Initialize the system
system = core.System()

# Use the main functionality
result = system.process(your_data)
print(result)
\`\`\`

## Features

- High-performance processing engine
- Scalable architecture for production use
- Simple API for easy integration
- Comprehensive error handling
- Extensive logging and monitoring

## Documentation

Full documentation is available at: https://prakashgbid.github.io/$repo_name/

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Issues: [GitHub Issues](https://github.com/prakashgbid/$repo_name/issues)
- Discussions: [GitHub Discussions](https://github.com/prakashgbid/$repo_name/discussions)

---

*Built with ❤️ by the $project_name Team*
EOF
    fi
    
    # Rename source directory if needed
    if [ -d "src/adaptive_learner" ]; then
        mv "src/adaptive_learner" "src/$package_name"
    elif [ -d "src/deep_reasoner" ]; then
        mv "src/deep_reasoner" "src/$package_name"
    elif [ -d "src/auto_coder" ]; then
        mv "src/auto_coder" "src/$package_name"
    elif [ -d "src/smart_planner" ]; then
        mv "src/smart_planner" "src/$package_name"
    elif [ -d "src/o_s_a_autonomous" ]; then
        mv "src/$package_name" "src/$package_name"
    elif [ -d "src/langgraph_orchestrator" ]; then
        mv "src/langgraph_orchestrator" "src/$package_name"
    elif [ -d "src/persistent_ai_memory" ]; then
        mv "src/persistent_ai_memory" "src/$package_name"
    fi
    
    # Update Python files to remove OSA references
    find . -name "*.py" -type f -exec sed -i '' "s/OSA/$project_name/g" {} \;
    find . -name "*.py" -type f -exec sed -i '' "s/Omnimind Studio Assistant/$project_name/g" {} \;
    find . -name "*.py" -type f -exec sed -i '' "s/adaptive_learner/$package_name/g" {} \;
    find . -name "*.py" -type f -exec sed -i '' "s/deep_reasoner/$package_name/g" {} \;
    find . -name "*.py" -type f -exec sed -i '' "s/auto_coder/$package_name/g" {} \;
    find . -name "*.py" -type f -exec sed -i '' "s/smart_planner/$package_name/g" {} \;
    find . -name "*.py" -type f -exec sed -i '' "s/o_s_a_autonomous/$package_name/g" {} \;
    find . -name "*.py" -type f -exec sed -i '' "s/langgraph_orchestrator/$package_name/g" {} \;
    find . -name "*.py" -type f -exec sed -i '' "s/persistent_ai_memory/$package_name/g" {} \;
    
    # Update documentation
    if [ -f "mkdocs.yml" ]; then
        sed -i '' "s/osa-.*/$repo_name/g" mkdocs.yml
        sed -i '' "s/OSA.*/$project_name Documentation/g" mkdocs.yml
        sed -i '' "s/OSA Contributors/$project_name Team/g" mkdocs.yml
        sed -i '' "s/Extracted from.*/$description/g" mkdocs.yml
    fi
    
    if [ -f "docs/index.md" ]; then
        sed -i '' "s/osa-.*/$repo_name/g" docs/index.md
        sed -i '' "s/OSA.*project/$project_name/g" docs/index.md
        sed -i '' "s/Omnimind Studio Assistant/$project_name/g" docs/index.md
        sed -i '' "s/adaptive-learner/$package_name/g" docs/index.md
        sed -i '' "s/deep-reasoner/$package_name/g" docs/index.md
        sed -i '' "s/auto-coder/$package_name/g" docs/index.md
        sed -i '' "s/smart-planner/$package_name/g" docs/index.md
        sed -i '' "s/o-s-a-autonomous/$package_name/g" docs/index.md
        sed -i '' "s/langgraph-orchestrator/$package_name/g" docs/index.md
        sed -i '' "s/persistent-ai-memory/$package_name/g" docs/index.md
    fi
    
    echo "✅ Rebranded $module_dir to $project_name"
done

echo "🎉 All projects rebranded successfully!"