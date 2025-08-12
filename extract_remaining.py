import orjson
#!/usr/bin/env python3
"""
Extract remaining high-priority modules
"""

import sys
import asyncio
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agents.open_source_extractor_agent import get_open_source_extractor, OpenSourceCandidate


async def extract_module(name: str):
    """Extract a module with new naming system"""
    print(f"\n📦 Extracting {name}...")
    
    agent = get_open_source_extractor()
    
    # Load candidates
    try:
        with open(".open_source_candidates.json", "r") as f:
            candidates_data = json.load(f)
    except FileNotFoundError:
        print("No candidates found. Run scan first.")
        return False
    
    # Find the candidate
    candidate_data = None
    for c in candidates_data:
        if c["name"] == name:
            candidate_data = c
            break
    
    if not candidate_data:
        print(f"Candidate '{name}' not found.")
        return False
    
    # Create candidate object
    candidate = OpenSourceCandidate(
        name=candidate_data["name"],
        path=candidate_data["path"],
        description=candidate_data["description"]
    )
    candidate.files = candidate_data["files"]
    
    # Research first
    print("  → Researching similar projects...")
    await agent.research_similar_projects(candidate)
    await agent.generate_unique_value_proposition(candidate)
    
    # Extract and restructure with new naming
    print("  → Extracting and restructuring...")
    project_dir = await agent.extract_and_restructure(candidate)
    
    # Show what was created
    project_name = getattr(candidate, 'project_name', candidate.name)
    package_name = getattr(candidate, 'package_name', candidate.name.replace('-', '_'))
    
    print(f"  ✅ Extracted as: {project_name} (package: {package_name})")
    print(f"     Location: {project_dir}")
    
    return True


async def main():
    """Extract remaining priority modules"""
    modules = [
        "code-generator",     # Self-modifier capabilities
        "task-planner",       # Goal-oriented behavior
        "o-s-a-autonomous",   # Autonomous decision engine
    ]
    
    print("🚀 Extracting remaining high-priority modules...")
    print("=" * 50)
    
    for module in modules:
        success = await extract_module(module)
        if not success:
            print(f"  ❌ Failed to extract {module}")
    
    print("\n" + "=" * 50)
    print("🎉 All extractions complete!")
    
    # List all extracted modules
    modules_dir = Path("/Users/MAC/Documents/projects/omnimind/modules")
    if modules_dir.exists():
        print("\n📦 Extracted modules:")
        for module_dir in sorted(modules_dir.iterdir()):
            if module_dir.is_dir():
                print(f"  • {module_dir.name}")


if __name__ == "__main__":
    asyncio.run(main())