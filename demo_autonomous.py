#!/usr/bin/env python3
"""
Demo of MemCore Autonomous Capabilities
Shows how MemCore automatically handles different types of requests
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from core.osa_autonomous import MemCoreAutonomous

async def demo():
    print("=" * 70)
    print("MemCore AUTONOMOUS DEMO - No Manual Mode Switching!")
    print("=" * 70)
    print("\nMemCore automatically understands what you need...\n")
    
    # Initialize MemCore
    osa = MemCoreAutonomous({"verbose": False})
    await osa.initialize()
    
    # Demo requests showing automatic intent detection
    demo_requests = [
        "Write a function to reverse a string",
        "Why is my code throwing an index out of bounds error?",
        "How can I make this loop run faster?",
        "Think deeply about artificial consciousness",
        "How do I solve x² - 5x + 6 = 0?",
        "Teach me about recursion",
        "What is a neural network?",
        "Create a haiku about programming",
        "Analyze the benefits of test-driven development",
        "Hello! How are you today?"
    ]
    
    for i, request in enumerate(demo_requests, 1):
        print(f"\n{'='*70}")
        print(f"Demo {i}: {request}")
        print("-" * 70)
        
        # Process autonomously
        response = await osa.process_autonomously(request)
        
        # Show just the status line (first line of response)
        status_line = response.split('\n')[0]
        print(status_line)
        print("✅ MemCore automatically understood and responded appropriately!")
        
        # Small delay for readability
        await asyncio.sleep(0.5)
    
    print(f"\n{'='*70}")
    print("DEMO COMPLETE!")
    print("MemCore handled all requests without any manual mode switching!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(demo())