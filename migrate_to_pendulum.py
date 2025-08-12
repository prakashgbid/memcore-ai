#!/usr/bin/env python3
"""
Migrate datetime to pendulum for better timezone handling
"""

import re
from pathlib import Path

def migrate_to_pendulum():
    """Replace datetime with pendulum across the codebase"""
    
    osa_root = Path("/Users/MAC/Documents/projects/omnimind")
    files_updated = 0
    
    for py_file in osa_root.rglob("*.py"):
        if py_file.is_file() and "migrate_to_pendulum" not in str(py_file):
            content = py_file.read_text()
            original = content
            
            # Replace datetime imports
            if "from datetime import" in content or "import datetime" in content:
                # Add pendulum import
                if "import pendulum" not in content:
                    content = "import pendulum\n" + content
                
                # Replace datetime.datetime.now() with pendulum.now()
                content = re.sub(
                    r'\bdatetime\.datetime\.now\(\)',
                    'pendulum.now()',
                    content
                )
                
                # Replace datetime.now() with pendulum.now()
                content = re.sub(
                    r'\bdatetime\.now\(\)',
                    'pendulum.now()',
                    content
                )
                
                # Replace datetime.utcnow() with pendulum.now("UTC")
                content = re.sub(
                    r'\bdatetime\.datetime\.utcnow\(\)',
                    'pendulum.now("UTC")',
                    content
                )
                
                # Replace datetime.timedelta with pendulum.duration
                content = re.sub(
                    r'\bdatetime\.timedelta\(',
                    'pendulum.duration(',
                    content
                )
                
                # Replace strftime with format
                content = re.sub(
                    r'\.strftime\(',
                    '.format(',
                    content
                )
                
                # Replace strptime with parse
                content = re.sub(
                    r'datetime\.datetime\.strptime\(([^,]+),\s*([^)]+)\)',
                    r'pendulum.parse(\1)',
                    content
                )
            
            if content != original:
                py_file.write_text(content)
                files_updated += 1
                print(f"✅ Updated: {py_file.relative_to(osa_root)}")
    
    return files_updated

if __name__ == "__main__":
    print("🔄 Migrating datetime to pendulum...")
    count = migrate_to_pendulum()
    print(f"✅ Migration complete! Updated {count} files")
    print("📝 Note: pendulum provides better timezone handling and more intuitive API")