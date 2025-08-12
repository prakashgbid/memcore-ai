# Installation

## Requirements

- Python 3.8 or higher
- pip package manager

## Installation Methods

### From GitHub

```bash
pip install git+https://github.com/prakashgbid/osa-adaptive-learner.git
```

### From Source

```bash
git clone https://github.com/prakashgbid/osa-adaptive-learner.git
cd osa-adaptive-learner
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/prakashgbid/osa-adaptive-learner.git
cd osa-adaptive-learner
pip install -e ".[dev]"
```

## Verify Installation

```python
import adaptive_learner
print(adaptive_learner.__version__)
```
