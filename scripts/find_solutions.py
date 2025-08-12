import orjson
#!/usr/bin/env python3
"""
Command-line tool for Open Source Solution Finder

Usage:
    python find_solutions.py find "description"    # Find solution for a requirement
    python find_solutions.py scan                  # Scan codebase for replacements
    python find_solutions.py interactive          # Interactive mode
    python find_solutions.py report               # Generate report
    python find_solutions.py suggest "feature"    # Suggest architecture
"""

import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.open_source_solution_finder import (
    get_solution_finder,
    check_before_coding,
    RequirementSpec,
    SolutionLevel
)


async def find_command(description: str):
    """Find solution for a requirement"""
    print(f"🔍 Finding solutions for: {description}\n")
    
    # Check for solutions
    result = await check_before_coding(description)
    
    # Display recommendation
    print(f"📌 Recommendation: {result['recommendation']}\n")
    
    if result['should_use_library']:
        print("✅ Use Open Source Library\n")
    else:
        print("⚠️  Build Custom Implementation\n")
    
    # Display solutions
    if result['solutions']:
        print("📦 Top Solutions:")
        for i, sol in enumerate(result['solutions'][:5], 1):
            print(f"\n{i}. {sol.name}")
            print(f"   Type: {sol.type.value}")
            print(f"   Score: {sol.match_score:.2f}")
            print(f"   Description: {sol.description}")
            if sol.installation:
                print(f"   Install: {sol.installation}")
            if sol.url:
                print(f"   URL: {sol.url}")
            if hasattr(sol, 'pros') and sol.pros:
                print(f"   Pros: {', '.join(sol.pros[:3])}")
            if hasattr(sol, 'cons') and sol.cons:
                print(f"   Cons: {', '.join(sol.cons[:3])}")
    
    # Display code example
    if result.get('code_example'):
        print("\n📝 Code Example:")
        print(result['code_example'])


async def scan_command():
    """Scan codebase for replacement opportunities"""
    print("🔍 Scanning MemCore codebase for replacement opportunities...\n")
    
    finder = get_solution_finder()
    opportunities = await finder.scan_codebase_for_replacements()
    
    if not opportunities:
        print("✅ No replacement opportunities found. Code is optimized!")
        return
    
    print(f"📊 Found {len(opportunities)} replacement opportunities:\n")
    
    # Group by priority
    by_priority = {}
    for opp in opportunities:
        if opp.priority not in by_priority:
            by_priority[opp.priority] = []
        by_priority[opp.priority].append(opp)
    
    # Display by priority
    for priority in sorted(by_priority.keys()):
        print(f"\n🔴 Priority {priority}:")
        for opp in by_priority[priority][:5]:  # Show top 5 per priority
            print(f"\n  📁 {opp.file_path}:{opp.line_range[0]}")
            print(f"     Current: {opp.current_code[:60]}...")
            print(f"     Replace with: {opp.suggested_library}")
            print(f"     Effort: {opp.migration_effort}")
            print(f"     Benefits: {', '.join(opp.benefits[:2])}")
    
    # Summary
    print(f"\n📈 Summary:")
    print(f"  Total opportunities: {len(opportunities)}")
    for priority in sorted(by_priority.keys()):
        print(f"  Priority {priority}: {len(by_priority[priority])} items")


async def suggest_command(feature: str):
    """Suggest architecture using open source components"""
    print(f"🏗️ Suggesting architecture for: {feature}\n")
    
    finder = get_solution_finder()
    architecture = await finder.suggest_architecture(feature)
    
    print("📋 Recommended Architecture:\n")
    
    if architecture['components']:
        print("🔧 Components:")
        for comp in architecture['components']:
            print(f"\n  {comp['purpose']}:")
            print(f"    Recommended: {comp['recommended']}")
            if comp.get('alternatives'):
                print(f"    Alternatives: {', '.join(comp['alternatives'])}")
            print(f"    Reason: {comp['reason']}")
    
    if architecture.get('integration_points'):
        print("\n🔗 Integration Points:")
        for point in architecture['integration_points']:
            print(f"  - {point}")
    
    if architecture.get('estimated_effort'):
        print(f"\n⏱️ Estimated Effort: {architecture['estimated_effort']}")


async def interactive_command():
    """Run in interactive mode"""
    finder = get_solution_finder()
    await finder.interactive_mode()


async def report_command():
    """Generate report"""
    finder = get_solution_finder()
    print(finder.generate_report())


async def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    
    if command == "find":
        if len(sys.argv) < 3:
            print("Usage: find_solutions.py find \"description\"")
            return
        description = " ".join(sys.argv[2:])
        await find_command(description)
    
    elif command == "scan":
        await scan_command()
    
    elif command == "suggest":
        if len(sys.argv) < 3:
            print("Usage: find_solutions.py suggest \"feature\"")
            return
        feature = " ".join(sys.argv[2:])
        await suggest_command(feature)
    
    elif command == "interactive":
        await interactive_command()
    
    elif command == "report":
        await report_command()
    
    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    asyncio.run(main())