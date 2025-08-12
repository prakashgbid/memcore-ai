#!/usr/bin/env python3
"""
Migrate json to orjson for better performance
"""

import re
from pathlib import Path

def migrate_to_orjson():
    """Replace json with orjson across the codebase"""
    
    osa_root = Path("/Users/MAC/Documents/projects/omnimind")
    files_updated = 0
    
    for py_file in osa_root.rglob("*.py"):
        if py_file.is_file() and "migrate_to_orjson" not in str(py_file):
            content = py_file.read_text()
            original = content
            
            # Replace import statements
            if "import json" in content:
                # Add orjson import
                if "import orjson" not in content:
                    content = "import orjson\n" + content
                
                # Replace json.dumps with orjson.dumps
                content = re.sub(
                    r'\bjson\.dumps\(',
                    'orjson.dumps(',
                    content
                )
                
                # Replace json.loads with orjson.loads
                content = re.sub(
                    r'\bjson\.loads\(',
                    'orjson.loads(',
                    content
                )
                
                # Handle orjson.dumps returning bytes
                # Add .decode() where needed
                content = re.sub(
                    r'(orjson\.dumps\([^)]+\))',
                    r'\1.decode()',
                    content
                )
                
                # Remove redundant json import if not used elsewhere
                if "json." not in content:
                    content = re.sub(r'^import json\n', '', content, flags=re.MULTILINE)
                
            if content != original:
                py_file.write_text(content)
                files_updated += 1
                print(f"✅ Updated: {py_file.relative_to(osa_root)}")
    
    return files_updated

if __name__ == "__main__":
    print("🔄 Migrating json to orjson...")
    count = migrate_to_orjson()
    print(f"✅ Migration complete! Updated {count} files")
    print("📝 Note: orjson is 2-3x faster than standard json")