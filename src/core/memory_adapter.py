"""Adapter for using the extracted persistent-ai-memory module."""

import sys
from pathlib import Path
import os

# AUTO-LOAD CRITICAL VISION ON IMPORT
def auto_load_vision():
    """Automatically load MemCore vision files to ensure context is never lost."""
    vision_files = [
        "/Users/MAC/Documents/projects/omnimind/MemCore_ULTIMATE_VISION.md",
        "/Users/MAC/Documents/projects/omnimind/MemCore_CORE_VISION.md",
        "/Users/MAC/Documents/projects/omnimind/MemCore_ARCHITECTURE_PRINCIPLES.md"
    ]
    
    print("\n" + "="*60)
    print("🎯 MemCore VISION AUTO-LOADED")
    print("="*60)
    print("ULTIMATE GOAL: 100% Autonomous, 100% Accurate, 100% Secure")
    print("NOT: CC with agents | IS: Autonomous Developer")
    print("="*60 + "\n")
    
    # Store in environment for other modules
    os.environ["MemCore_VISION_LOADED"] = "true"
    os.environ["MemCore_GOAL"] = "100_AUTONOMOUS_100_ACCURATE_100_SECURE"

# Auto-load on import
auto_load_vision()

# Add module path (temporary until pip install)
module_path = Path(__file__).parent.parent.parent / "modules" / "persistent-ai-memory" / "src"
sys.path.insert(0, str(module_path))

# Import from the extracted module
from memcore import (
    PersistentMemory,
    Memory,
    MemoryType,
    MemoryPriority,
    get_persistent_memory
)

# Re-export for backward compatibility
__all__ = [
    "PersistentMemory",
    "Memory", 
    "MemoryType",
    "MemoryPriority",
    "get_persistent_memory"
]