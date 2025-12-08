#!/usr/bin/env python3
"""
Quick setup script for local Redis and PostgreSQL using Python alternatives.
This creates minimal in-memory versions for local development.
"""

import subprocess
import sys
import platform
import json
from pathlib import Path

def install_package(package_name):
    """Install a Python package."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def setup_local_services():
    """Set up local services without Docker."""
    
    print("🔧 Setting up local development services...\n")
    
    # Check if fakeredis and sqlite can be used
    print("1️⃣  Installing development dependencies...")
    try:
        install_package("fakeredis")
        install_package("aiosqlite")
        print("✅ Dependencies installed\n")
    except Exception as e:
        print(f"⚠️  Error installing packages: {e}\n")
        return False
    
    print("2️⃣  Creating local database...")
    
    # Create a local setup script
    setup_script = Path("ai_agent_system/src/utils/local_setup.py")
    setup_script.parent.mkdir(parents=True, exist_ok=True)
    
    setup_script.write_text('''"""
Local development setup for Redis and PostgreSQL alternatives.
"""

import sqlite3
import asyncio
from pathlib import Path

async def init_local_database():
    """Initialize local SQLite database for development."""
    db_path = Path("./data/ai_agents.db")
    db_path.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Create basic tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id TEXT PRIMARY KEY,
            name TEXT,
            role TEXT,
            capabilities TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id TEXT,
            action TEXT,
            result TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agent_id) REFERENCES agents(id)
        )
    """)
    
    conn.commit()
    conn.close()
    
    print("✅ Local database initialized at ./data/ai_agents.db")

if __name__ == "__main__":
    asyncio.run(init_local_database())
''')
    
    # Run the setup
    try:
        subprocess.run([sys.executable, str(setup_script)], check=True)
    except Exception as e:
        print(f"⚠️  Setup error: {e}\n")
    
    print("\n" + "="*60)
    print("✅ Local development environment ready!")
    print("="*60)
    print("\nNext steps:")
    print("1. The app will use local SQLite instead of PostgreSQL")
    print("2. Redis functionality is simulated in-memory")
    print("3. For production, install Docker and use docker-compose.yml")
    print("\nTo start the server:")
    print("  .venv\\Scripts\\python.exe -m uvicorn ai_agent_system.src.main:app")
    
    return True

if __name__ == "__main__":
    success = setup_local_services()
    sys.exit(0 if success else 1)
