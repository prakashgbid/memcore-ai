import orjson
#!/usr/bin/env python3
"""
Migrate custom logger to Loguru
"""

import os
import re
from pathlib import Path
from loguru import logger

def migrate_logger_imports():
    """Replace logger imports across the codebase"""
    
    # Configure Loguru with MemCore defaults
    logger.add("logs/osa_{time}.log", rotation="500 MB", retention="10 days")
    
    files_to_update = []
    osa_root = Path("/Users/MAC/Documents/projects/omnimind")
    
    # Find all Python files using the custom logger
    for py_file in osa_root.rglob("*.py"):
        if py_file.is_file():
            content = py_file.read_text()
            
            # Check if file uses the custom logger
            if "from src.core.logger import" in content or "from .logger import" in content:
                files_to_update.append(py_file)
    
    print(f"Found {len(files_to_update)} files to update")
    
    for file_path in files_to_update:
        content = file_path.read_text()
        
        # Replace imports
        content = re.sub(
            r'from (?:src\.core\.logger|\.logger|\.\.logger) import .*',
            'from loguru import logger',
            content
        )
        
        # Replace WebSocketLogger instantiation
        content = re.sub(
            r'self\.logger = WebSocketLogger\([^)]*\)',
            'self.logger = logger',
            content
        )
        
        # Replace custom logger patterns
        content = re.sub(
            r'WebSocketLogger\([^)]*\)',
            'logger',
            content
        )
        
        # Update log level methods
        content = re.sub(r'\.log_info\(', '.info(', content)
        content = re.sub(r'\.log_error\(', '.error(', content)
        content = re.sub(r'\.log_warning\(', '.warning(', content)
        content = re.sub(r'\.log_debug\(', '.debug(', content)
        
        # Save updated file
        file_path.write_text(content)
        print(f"✅ Updated: {file_path.relative_to(osa_root)}")
    
    # Create adapter for WebSocket functionality
    adapter_content = '''"""
Loguru adapter for WebSocket functionality
"""

from loguru import logger
import asyncio
import json

class WebSocketLogHandler:
    """Handler to send logs to WebSocket clients"""
    
    def __init__(self, websocket_manager=None):
        self.websocket_manager = websocket_manager
        
    def write(self, message):
        """Send log message to WebSocket clients"""
        if self.websocket_manager:
            asyncio.create_task(
                self.websocket_manager.broadcast(orjson.dumps({
                    "type": "log",
                    "message": message.strip().decode()
                }))
            )

# Add WebSocket handler to Loguru if needed
def setup_websocket_logging(websocket_manager):
    """Setup WebSocket logging handler"""
    handler = WebSocketLogHandler(websocket_manager)
    logger.add(handler, format="{message}")
    return logger
'''
    
    adapter_path = osa_root / "src" / "core" / "loguru_adapter.py"
    adapter_path.write_text(adapter_content)
    print(f"✅ Created Loguru adapter at: {adapter_path}")
    
    return len(files_to_update)

if __name__ == "__main__":
    print("🔄 Migrating custom logger to Loguru...")
    updated_count = migrate_logger_imports()
    print(f"✅ Migration complete! Updated {updated_count} files")
    print("📝 Note: Review WebSocket functionality in loguru_adapter.py")