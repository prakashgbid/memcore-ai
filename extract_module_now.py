import orjson
#!/usr/bin/env python3
"""
Extract a single module with the updated extractor
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
    print(f"📦 Extracting {name} with proper naming...")
    
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
    print("Researching similar projects...")
    await agent.research_similar_projects(candidate)
    await agent.generate_unique_value_proposition(candidate)
    
    # Extract and restructure with new naming
    print("Extracting and restructuring code with proper naming...")
    project_dir = await agent.extract_and_restructure(candidate)
    
    # Show what was created
    project_name = getattr(candidate, 'project_name', candidate.name)
    package_name = getattr(candidate, 'package_name', candidate.name.replace('-', '_'))
    
    print(f"\n✅ Successfully extracted!")
    print(f"   Original name: {candidate.name}")
    print(f"   Project name:  {project_name}")
    print(f"   Package name:  {package_name}")
    print(f"   Location:      {project_dir}")
    
    return True


async def main():
    """Extract continuous-thinking module"""
    module = "continuous-thinking"
    
    success = await extract_module(module)
    if success:
        print(f"\n🎉 Module extracted successfully!")
    else:
        print(f"\n❌ Failed to extract module")


if __name__ == "__main__":
    asyncio.run(main())