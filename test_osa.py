#\!/usr/bin/env python3
"""Test MemCore with actual Ollama interaction"""

import ollama
import sys

print("Testing MemCore with Ollama...")
print("=" * 50)

try:
    # Initialize client
    client = ollama.Client()
    
    # Test question
    question = "What can you do?"
    print(f"\n📝 Question: {question}")
    print("-" * 50)
    
    # Generate response
    print("🤔 Thinking...")
    response = client.generate(
        model="llama3.2:3b",
        prompt=question
    )
    
    print("\n✅ Response:")
    print("-" * 50)
    print(response['response'])
    print("-" * 50)
    
    print("\n✨ MemCore is working correctly\!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)
EOF < /dev/null