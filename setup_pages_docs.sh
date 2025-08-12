#!/bin/bash

# Setup GitHub Pages documentation for all projects in parallel

echo "🚀 Setting up GitHub Pages documentation for all projects..."

# Function to setup docs for a project
setup_docs() {
    local module_dir=$1
    local repo_name=$2
    local project_name=$3
    local package_name=$4
    local description=$5
    
    echo "📚 Setting up docs for $project_name..."
    
    cd "/Users/MAC/Documents/projects/omnimind/modules/$module_dir"
    
    # Update MkDocs configuration with proper branding
    cat > mkdocs.yml << EOF
site_name: $project_name
site_url: https://prakashgbid.github.io/${repo_name}/
site_description: $description
site_author: $project_name Team
repo_name: prakashgbid/${repo_name}
repo_url: https://github.com/prakashgbid/${repo_name}
edit_uri: edit/main/docs/

theme:
  name: material
  custom_dir: docs/overrides
  logo: assets/logo.png
  favicon: assets/favicon.ico
  features:
    - announce.dismiss
    - content.action.edit
    - content.action.view
    - content.code.annotate
    - content.code.copy
    - content.tabs.link
    - content.tooltips
    - header.autohide
    - navigation.expand
    - navigation.footer
    - navigation.indexes
    - navigation.instant
    - navigation.prune
    - navigation.sections
    - navigation.tabs
    - navigation.tabs.sticky
    - navigation.top
    - navigation.tracking
    - search.highlight
    - search.share
    - search.suggest
    - toc.follow
    - toc.integrate
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  font:
    text: Roboto
    code: Roboto Mono
  icon:
    logo: logo

plugins:
  - search:
      separator: '[\s\-,:!=\[\]()"`/]+|\.(?!\d)|&[lg]t;|(?!\b)(?=[A-Z][a-z])'
  - minify:
      minify_html: true
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true
            show_root_heading: true
            show_root_full_path: false
            show_object_full_path: false
            show_category_heading: true
            show_if_no_docstring: true
            show_signature: true
            show_signature_annotations: true
            separate_signature: true
            line_length: 80
            merge_init_into_class: true
            docstring_style: google

nav:
  - Home: index.md
  - Getting Started:
    - Installation: getting-started/installation.md
    - Quick Start: getting-started/quickstart.md
    - Configuration: getting-started/configuration.md
    - Tutorials: getting-started/tutorials.md
  - User Guide:
    - Overview: guide/overview.md
    - Basic Usage: guide/basic-usage.md
    - Advanced Features: guide/advanced-features.md
    - Best Practices: guide/best-practices.md
    - Performance: guide/performance.md
  - API Reference:
    - Core Module: api/core.md
    - Types: api/types.md
    - Utils: api/utils.md
    - Exceptions: api/exceptions.md
  - Examples:
    - Basic Examples: examples/basic.md
    - Advanced Examples: examples/advanced.md
    - Integration Examples: examples/integration.md
    - Real World: examples/real-world.md
  - Architecture:
    - Overview: architecture/overview.md
    - Components: architecture/components.md
    - Design Patterns: architecture/patterns.md
    - Scalability: architecture/scalability.md
  - Development:
    - Contributing: development/contributing.md
    - Development Setup: development/setup.md
    - Testing: development/testing.md
    - Code Style: development/style.md
    - Release Process: development/release.md
  - Resources:
    - FAQ: resources/faq.md
    - Troubleshooting: resources/troubleshooting.md
    - Glossary: resources/glossary.md
    - Links: resources/links.md
  - Changelog: changelog.md
  - License: license.md

markdown_extensions:
  - abbr
  - admonition
  - attr_list
  - def_list
  - footnotes
  - md_in_html
  - toc:
      permalink: true
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.betterem:
      smart_enable: all
  - pymdownx.caret
  - pymdownx.details
  - pymdownx.emoji:
      emoji_generator: !!python/name:materialx.emoji.to_svg
      emoji_index: !!python/name:materialx.emoji.twemoji
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.keys
  - pymdownx.magiclink:
      repo_url_shorthand: true
      user: prakashgbid
      repo: ${repo_name}
  - pymdownx.mark
  - pymdownx.smartsymbols
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - pymdownx.tilde

extra:
  analytics:
    provider: google
    property: !ENV GOOGLE_ANALYTICS_KEY
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/prakashgbid/${repo_name}
    - icon: fontawesome/brands/python
      link: https://pypi.org/project/${package_name}/
    - icon: fontawesome/brands/twitter
      link: https://twitter.com/${package_name}
  version:
    provider: mike

extra_css:
  - stylesheets/extra.css

extra_javascript:
  - javascripts/extra.js
  - javascripts/mathjax.js
  - https://polyfill.io/v3/polyfill.min.js?features=es6
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js
EOF

    # Create enhanced documentation structure
    mkdir -p docs/{getting-started,guide,api,examples,architecture,development,resources,assets,overrides,stylesheets,javascripts}
    
    # Create main index page with proper branding
    cat > docs/index.md << EOF
# $project_name

## $description

[![GitHub Stars](https://img.shields.io/github/stars/prakashgbid/${repo_name}?style=social)](https://github.com/prakashgbid/${repo_name})
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/prakashgbid/${repo_name}/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org)
[![PyPI Version](https://img.shields.io/pypi/v/${package_name})](https://pypi.org/project/${package_name}/)
[![Documentation Status](https://img.shields.io/badge/docs-latest-green)](https://prakashgbid.github.io/${repo_name}/)

---

## 🚀 Features

- **High Performance** - Optimized for speed and efficiency
- **Scalable Architecture** - Built to handle production workloads
- **Easy Integration** - Simple API with comprehensive documentation
- **Extensible** - Plugin system for custom extensions
- **Well Tested** - Comprehensive test coverage
- **Production Ready** - Battle-tested in real-world applications

## 📦 Quick Installation

\`\`\`bash
pip install ${package_name}
\`\`\`

## 🎯 Quick Start

\`\`\`python
from ${package_name} import ${project_name}

# Initialize
engine = ${project_name}()

# Process your data
result = engine.process(your_data)
print(result)
\`\`\`

## 📚 Documentation

<div class="grid cards" markdown>

-   :material-rocket-launch-outline:{ .lg .middle } **Getting Started**

    ---

    Installation, setup, and your first steps with $project_name

    [:octicons-arrow-right-24: Get started](getting-started/installation.md)

-   :material-book-open-variant:{ .lg .middle } **User Guide**

    ---

    Learn how to use $project_name effectively in your projects

    [:octicons-arrow-right-24: Read the guide](guide/overview.md)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Complete API documentation with examples

    [:octicons-arrow-right-24: Browse API](api/core.md)

-   :material-code-tags:{ .lg .middle } **Examples**

    ---

    Real-world examples and use cases

    [:octicons-arrow-right-24: View examples](examples/basic.md)

</div>

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](development/contributing.md) for details.

## 📄 License

$project_name is licensed under the MIT License. See [LICENSE](license.md) for details.

## 🌟 Support

- [GitHub Issues](https://github.com/prakashgbid/${repo_name}/issues)
- [Discussions](https://github.com/prakashgbid/${repo_name}/discussions)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/${package_name})

---

<p align="center">
  Made with ❤️ by the $project_name Team
</p>
EOF

    # Create installation guide
    cat > docs/getting-started/installation.md << EOF
# Installation

## System Requirements

- Python 3.8 or higher
- pip 20.0 or higher
- Operating System: Windows, macOS, or Linux

## Installation Methods

### Using pip (Recommended)

Install the latest stable version from PyPI:

\`\`\`bash
pip install ${package_name}
\`\`\`

### Using pip with extras

Install with optional dependencies:

\`\`\`bash
# With development tools
pip install ${package_name}[dev]

# With all extras
pip install ${package_name}[all]
\`\`\`

### From GitHub

Install the latest development version:

\`\`\`bash
pip install git+https://github.com/prakashgbid/${repo_name}.git
\`\`\`

### From Source

Clone and install from source:

\`\`\`bash
git clone https://github.com/prakashgbid/${repo_name}.git
cd ${repo_name}
pip install -e .
\`\`\`

## Verify Installation

\`\`\`python
import ${package_name}
print(${package_name}.__version__)
\`\`\`

## Docker Installation

\`\`\`dockerfile
FROM python:3.9-slim
RUN pip install ${package_name}
\`\`\`

## Troubleshooting

### Common Issues

!!! warning "Import Error"
    If you encounter import errors, ensure you have the correct Python version:
    \`\`\`bash
    python --version
    \`\`\`

!!! tip "Virtual Environment"
    We recommend using a virtual environment:
    \`\`\`bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\\Scripts\\activate
    pip install ${package_name}
    \`\`\`

## Next Steps

- [Quick Start Guide](quickstart.md)
- [Configuration](configuration.md)
- [Tutorials](tutorials.md)
EOF

    # Create other essential pages
    cat > docs/getting-started/quickstart.md << EOF
# Quick Start

Get up and running with $project_name in 5 minutes!

## Basic Example

\`\`\`python
from ${package_name} import ${project_name}

# Create an instance
engine = ${project_name}()

# Process data
result = engine.process("Hello, World!")
print(result)
\`\`\`

## Configuration

\`\`\`python
from ${package_name} import ${project_name}, Config

# Custom configuration
config = Config(
    verbose=True,
    max_workers=4,
    timeout=30
)

engine = ${project_name}(config=config)
\`\`\`

## Advanced Usage

\`\`\`python
# Async processing
import asyncio
from ${package_name} import Async${project_name}

async def main():
    engine = Async${project_name}()
    result = await engine.process_async(data)
    return result

asyncio.run(main())
\`\`\`

## What's Next?

- [User Guide](../guide/overview.md) - Comprehensive usage guide
- [API Reference](../api/core.md) - Detailed API documentation
- [Examples](../examples/basic.md) - More code examples
EOF

    # Create API documentation
    cat > docs/api/core.md << EOF
# Core API Reference

::: ${package_name}.core
    options:
      show_source: true
      show_bases: true
EOF

    # Create changelog
    cat > docs/changelog.md << EOF
# Changelog

All notable changes to $project_name are documented here.

## [Unreleased]

### Added
- Initial public release
- Core functionality implementation
- Comprehensive documentation
- Test suite

## [0.1.0] - 2024-12-01

### Added
- First release of $project_name
- Basic API implementation
- Documentation structure
- GitHub repository setup

### Changed
- Rebranded as independent project
- Removed external dependencies

### Fixed
- Initial bug fixes
- Documentation improvements

---

[Unreleased]: https://github.com/prakashgbid/${repo_name}/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/prakashgbid/${repo_name}/releases/tag/v0.1.0
EOF

    # Create license file
    cat > docs/license.md << EOF
# License

MIT License

Copyright (c) 2024 $project_name Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

    # Create custom CSS
    cat > docs/stylesheets/extra.css << EOF
/* Custom styles for $project_name */
.md-header {
    background-color: var(--md-primary-fg-color);
}

.md-hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

/* Card grid */
.grid.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
}

.grid.cards > * {
    border: 1px solid var(--md-default-fg-color--lightest);
    border-radius: 0.5rem;
    padding: 1rem;
}

/* Code blocks */
.highlight {
    border-radius: 0.5rem;
}

/* Admonitions */
.admonition {
    border-radius: 0.5rem;
}
EOF

    # Create requirements for docs
    cat > docs/requirements.txt << EOF
mkdocs>=1.5.0
mkdocs-material>=9.0.0
mkdocstrings[python]>=0.24.0
mkdocs-minify-plugin>=0.7.0
pymdown-extensions>=10.0
mike>=2.0.0
EOF

    # Update GitHub Actions workflow
    cat > .github/workflows/docs.yml << EOF
name: Deploy Documentation

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]
  workflow_dispatch:

permissions:
  contents: write
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install -r docs/requirements.txt
          pip install -e .
      
      - name: Build documentation
        run: mkdocs build --strict
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./site

  deploy:
    if: github.event_name == 'push' && github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master'
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: \${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
EOF

    # Commit and push
    git add -A
    git commit -m "Configure GitHub Pages documentation for $project_name" 2>/dev/null
    git push 2>/dev/null
    
    echo "✅ Docs configured for $project_name"
}

# Setup docs for all projects in parallel
setup_docs "self-learning" "evolux-ai" "Evolux" "evolux" "Self-evolving AI that learns and improves continuously" &
setup_docs "deep-reasoner" "cognitron-engine" "Cognitron" "cognitron" "Advanced multi-layer reasoning engine for complex problem solving" &
setup_docs "auto-coder" "codeforge-ai" "CodeForge" "codeforge" "Intelligent code generation and self-modification framework" &
setup_docs "smart-planner" "strategix-planner" "Strategix" "strategix" "Intelligent task planning and execution orchestrator" &
setup_docs "o-s-a-autonomous" "autonomix-engine" "Autonomix" "autonomix" "Self-directed decision engine for autonomous systems" &
setup_docs "langgraph-orchestrator" "flowmaster-orchestrator" "FlowMaster" "flowmaster" "Advanced workflow orchestration for multi-agent systems" &
setup_docs "persistent-ai-memory" "memcore-ai" "MemCore" "memcore" "Persistent memory system for intelligent applications" &

# Wait for all background jobs
wait

echo "🎉 All documentation sites configured successfully!"
echo "📄 GitHub Pages will be available at:"
echo "  - https://prakashgbid.github.io/evolux-ai/"
echo "  - https://prakashgbid.github.io/cognitron-engine/"
echo "  - https://prakashgbid.github.io/codeforge-ai/"
echo "  - https://prakashgbid.github.io/strategix-planner/"
echo "  - https://prakashgbid.github.io/autonomix-engine/"
echo "  - https://prakashgbid.github.io/flowmaster-orchestrator/"
echo "  - https://prakashgbid.github.io/memcore-ai/"