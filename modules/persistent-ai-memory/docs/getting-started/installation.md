# Installation

## Requirements

- Python 3.8 or higher
- pip package manager

## Installation Methods

### From GitHub

```bash
pip install git+https://github.com/prakashgbid/osa-persistent-ai-memory.git
```

### From Source

```bash
git clone https://github.com/prakashgbid/osa-persistent-ai-memory.git
cd osa-persistent-ai-memory
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/prakashgbid/osa-persistent-ai-memory.git
cd osa-persistent-ai-memory
pip install -e ".[dev]"
```

## Verify Installation

```python
import persistent_ai_memory
print(persistent_ai_memory.__version__)
```
