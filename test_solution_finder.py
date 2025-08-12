#!/usr/bin/env python3
"""
Demonstration of the Open Source Solution Finder Agent
Shows how it finds existing libraries before writing custom code
"""

import asyncio
import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path.cwd()))

# Import the solution finder
from src.agents.open_source_solution_finder import (
    OpenSourceSolutionFinder,
    RequirementSpec,
    SolutionLevel
)


async def demonstrate_solution_finder():
    """Run demonstrations of the Solution Finder"""
    
    print("=" * 80)
    print("🤖 Open Source Solution Finder Agent - Live Demonstration")
    print("=" * 80)
    print("\nThis agent prevents reinventing the wheel by finding existing solutions")
    print("BEFORE writing any custom code.\n")
    
    # Initialize the finder
    finder = OpenSourceSolutionFinder()
    
    # Test cases to demonstrate
    test_cases = [
        {
            "description": "Parse and validate email addresses",
            "level": SolutionLevel.FUNCTION,
            "keywords": ["email", "validation", "parse"],
        },
        {
            "description": "Create a progress bar for terminal output",
            "level": SolutionLevel.FUNCTION,
            "keywords": ["progress", "bar", "terminal", "cli"],
        },
        {
            "description": "Handle HTTP requests with retry logic",
            "level": SolutionLevel.MODULE,
            "keywords": ["http", "request", "retry", "api"],
        },
        {
            "description": "Parse command line arguments",
            "level": SolutionLevel.MODULE,
            "keywords": ["cli", "command", "argument", "parser"],
        },
        {
            "description": "Create animated loading spinner",
            "level": SolutionLevel.FUNCTION,
            "keywords": ["spinner", "loading", "animation", "terminal"],
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {test['description']}")
        print(f"Level: {test['level'].value}")
        print("-" * 40)
        
        # Create requirement
        req = RequirementSpec(
            description=test["description"],
            level=test["level"],
            keywords=test["keywords"],
            required_features=[],
            nice_to_have=[],
            constraints=[]
        )
        
        # Find solutions
        solutions = await finder.find_solution_before_coding(req)
        
        if solutions:
            # Check if we should use a library
            best = solutions[0]
            
            if best.match_score > 0.7:
                print(f"✅ FOUND SOLUTION - Use Open Source Library!")
                print(f"\n📦 Recommended: {best.name}")
                print(f"   Match Score: {best.match_score:.2f}")
                print(f"   Type: {best.type.value}")
                print(f"   Description: {best.description[:100] if best.description else 'N/A'}")
                
                if best.installation:
                    print(f"   Install: {best.installation}")
                
                if hasattr(best, 'pros') and best.pros:
                    print(f"   Pros: {', '.join(best.pros[:2])}")
                
                # Show alternatives if any
                if len(solutions) > 1:
                    print(f"\n   Alternatives:")
                    for alt in solutions[1:3]:
                        print(f"   - {alt.name} (score: {alt.match_score:.2f})")
            else:
                print(f"⚠️  Low match score ({best.match_score:.2f})")
                print(f"   Consider: {best.name} or build custom")
        else:
            print("❌ No suitable library found - build custom implementation")
    
    # Now demonstrate codebase scanning
    print(f"\n{'='*80}")
    print("🔍 Scanning MemCore Codebase for Replacement Opportunities")
    print("-" * 40)
    
    opportunities = await finder.scan_codebase_for_replacements()
    
    if opportunities:
        print(f"Found {len(opportunities)} opportunities to replace custom code:\n")
        
        # Show top 5
        for opp in opportunities[:5]:
            print(f"📁 {Path(opp.file_path).name}:{opp.line_range[0]}")
            print(f"   Current: {opp.current_code[:50]}...")
            print(f"   Replace with: {opp.suggested_library}")
            print(f"   Priority: {opp.priority}, Effort: {opp.migration_effort}")
            print()
    else:
        print("No replacement opportunities found!")
    
    # Show statistics
    print(f"\n{'='*80}")
    print("📊 Statistics")
    print("-" * 40)
    print(f"Searches performed: {finder.stats['searches_performed']}")
    print(f"Solutions found: {finder.stats['solutions_found']}")
    print(f"Custom code prevented: {finder.stats['custom_code_prevented']}")
    print(f"Replacements suggested: {finder.stats['replacements_suggested']}")
    
    print(f"\n{'='*80}")
    print("✨ Demonstration Complete!")
    print("This agent ensures MemCore follows 'Integration over Custom Code' philosophy")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(demonstrate_solution_finder())