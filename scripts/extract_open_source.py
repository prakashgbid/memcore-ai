import orjson
#!/usr/bin/env python3
"""
Manual control script for Open Source Extractor Agent

Usage:
    python extract_open_source.py scan           # Scan for opportunities
    python extract_open_source.py research NAME  # Research a specific module
    python extract_open_source.py extract NAME   # Extract and publish a module
    python extract_open_source.py list          # List published projects
    python extract_open_source.py continuous    # Run continuous scanning
"""

import sys
import asyncio
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.open_source_extractor_agent import get_open_source_extractor


async def scan_command():
    """Scan for open source opportunities"""
    print("🔍 Scanning MemCore codebase for open source opportunities...")
    
    agent = get_open_source_extractor()
    candidates = await agent.scan_for_opportunities()
    
    if not candidates:
        print("No new open source opportunities found.")
        return
    
    print(f"\n📦 Found {len(candidates)} potential open source projects:\n")
    
    for i, candidate in enumerate(candidates, 1):
        print(f"{i}. {candidate.name}")
        print(f"   Description: {candidate.description}")
        print(f"   Path: {candidate.path}")
        print(f"   Files: {len(candidate.files)}")
        print()
    
    # Save candidates for later processing
    with open(".open_source_candidates.json", "w") as f:
        json.dump([{
            "name": c.name,
            "path": c.path,
            "description": c.description,
            "files": c.files
        } for c in candidates], f, indent=2)
    
    print("Candidates saved to .open_source_candidates.json")


async def research_command(name: str):
    """Research similar projects for a candidate"""
    print(f"🔬 Researching similar projects for {name}...")
    
    agent = get_open_source_extractor()
    
    # Load candidates
    try:
        with open(".open_source_candidates.json", "r") as f:
            candidates_data = json.load(f)
    except FileNotFoundError:
        print("No candidates found. Run 'scan' first.")
        return
    
    # Find the candidate
    candidate_data = None
    for c in candidates_data:
        if c["name"] == name:
            candidate_data = c
            break
    
    if not candidate_data:
        print(f"Candidate '{name}' not found.")
        return
    
    # Create candidate object
    from src.agents.open_source_extractor_agent import OpenSourceCandidate
    candidate = OpenSourceCandidate(
        name=candidate_data["name"],
        path=candidate_data["path"],
        description=candidate_data["description"]
    )
    candidate.files = candidate_data["files"]
    
    # Research
    research = await agent.research_similar_projects(candidate)
    
    print("\n📊 Market Research Results:\n")
    
    # PyPI packages
    if research["pypi_packages"]:
        print("PyPI Packages:")
        for pkg in research["pypi_packages"]:
            print(f"  - {pkg['name']}: {pkg.get('summary', 'No description')}")
    else:
        print("PyPI Packages: None found")
    
    print()
    
    # GitHub repos
    if research["github_repos"]:
        print("GitHub Repositories:")
        for repo in research["github_repos"]:
            print(f"  - {repo['name']} ⭐ {repo.get('stars', 0)}")
            print(f"    {repo.get('description', 'No description')}")
    else:
        print("GitHub Repositories: None found")
    
    print()
    
    # Similarity analysis
    print(f"Similarity Score: {candidate.similarity_score:.2f}")
    print(f"Market Gap: {research['market_gap']}")
    
    # Generate UVP
    uvp = await agent.generate_unique_value_proposition(candidate)
    print(f"\n🎯 Unique Value Proposition:\n{uvp}")
    
    # Recommendation
    print("\n📝 Recommendation:")
    if candidate.similarity_score < 0.3:
        print("✅ HIGHLY RECOMMENDED - No similar projects exist")
    elif candidate.similarity_score < 0.6:
        print("✅ RECOMMENDED - Some similar projects but unique approach")
    else:
        print("⚠️  CONSIDER CAREFULLY - Similar projects exist, ensure strong differentiation")


async def extract_command(name: str):
    """Extract and publish a module"""
    print(f"📦 Extracting and publishing {name}...")
    
    agent = get_open_source_extractor()
    
    # Load candidates
    try:
        with open(".open_source_candidates.json", "r") as f:
            candidates_data = json.load(f)
    except FileNotFoundError:
        print("No candidates found. Run 'scan' first.")
        return
    
    # Find the candidate
    candidate_data = None
    for c in candidates_data:
        if c["name"] == name:
            candidate_data = c
            break
    
    if not candidate_data:
        print(f"Candidate '{name}' not found.")
        return
    
    # Create candidate object
    from src.agents.open_source_extractor_agent import OpenSourceCandidate
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
    
    # Extract and restructure
    print("Extracting and restructuring code...")
    project_dir = await agent.extract_and_restructure(candidate)
    print(f"✅ Project created at: {project_dir}")
    
    # Ask for confirmation before publishing
    response = input("\n🚀 Publish to GitHub? (y/n): ")
    if response.lower() == 'y':
        github_url = await agent.publish_to_github(project_dir, candidate)
        if github_url:
            print(f"✅ Published to: {github_url}")
        else:
            print("❌ Failed to publish to GitHub")
    else:
        print("Skipped GitHub publishing")


def list_command():
    """List published projects"""
    print("📚 Published Open Source Projects:\n")
    
    history_file = Path("/Users/MAC/Documents/projects/omnimind/.open_source_history.json")
    
    if not history_file.exists():
        print("No projects published yet.")
        return
    
    with open(history_file, 'r') as f:
        data = json.load(f)
    
    published = data.get("published", {})
    
    if not published:
        print("No projects published yet.")
        return
    
    for name, url in published.items():
        print(f"  - {name}: {url}")
    
    print(f"\nTotal: {len(published)} projects")


async def continuous_command():
    """Run continuous scanning"""
    print("🔄 Starting continuous open source scanning...")
    print("This will run indefinitely. Press Ctrl+C to stop.\n")
    
    agent = get_open_source_extractor()
    
    try:
        await agent.run_continuous_scan()
    except KeyboardInterrupt:
        print("\n⏹️  Stopped continuous scanning")


async def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1]
    
    if command == "scan":
        await scan_command()
    elif command == "research":
        if len(sys.argv) < 3:
            print("Usage: extract_open_source.py research NAME")
            return
        await research_command(sys.argv[2])
    elif command == "extract":
        if len(sys.argv) < 3:
            print("Usage: extract_open_source.py extract NAME")
            return
        await extract_command(sys.argv[2])
    elif command == "list":
        list_command()
    elif command == "continuous":
        await continuous_command()
    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    asyncio.run(main())