"""Persistent AI Memory - Never lose context again."""

from .memcore import (
    PersistentMemory,
    Memory,
    MemoryType,
    MemoryPriority,
    get_persistent_memory
)

__version__ = "1.0.0"
__author__ = "MemCore Contributors"

__all__ = [
    "PersistentMemory",
    "Memory",
    "MemoryType", 
    "MemoryPriority",
    "get_persistent_memory"
]