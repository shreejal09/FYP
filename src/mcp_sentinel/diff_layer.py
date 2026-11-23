# diff_layer.py
# Saves tool "fingerprints" in a database and checks if they change.

import sqlite3
import json
import hashlib
import os

# Path to our database
DB_PATH = "config/baseline.sqlite"

def get_db():
    # Make sure the config folder exists
    os.makedirs("config", exist_ok=True)
    # Connect to the SQLite database
    return sqlite3.connect(DB_PATH)

def create_table():
    # Create a simple table to store tool names and their hashes
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS baselines (
            tool_name TEXT PRIMARY KEY,
            hash_value TEXT
        )
    """)
    conn.commit()
    conn.close()

def hash_tool(tool):
    # Convert the tool dictionary into a consistent string
    # We use sort_keys=True so the order of keys doesn't change the hash (simplified RFC 8785)
    tool_string = json.dumps(tool, sort_keys=True)
    
    # Turn the string into a SHA-256 hash (a unique fingerprint)
    return hashlib.sha256(tool_string.encode()).hexdigest()

def check_tool(tool):
    create_table() # Make sure the table exists
    
    name = tool["name"]
    new_hash = hash_tool(tool)
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Look for this tool in the database
    cursor.execute("SELECT hash_value FROM baselines WHERE tool_name = ?", (name,))
    result = cursor.fetchone()
    
    if result is None:
        # TOOL IS NEW: Save it to the database
        cursor.execute("INSERT INTO baselines (tool_name, hash_value) VALUES (?, ?)", (name, new_hash))
        conn.commit()
        conn.close()
        return "new"
        
    else:
        # TOOL EXISTS: Compare the old hash with the new one
        old_hash = result[0]
        conn.close()
        
        if old_hash == new_hash:
            return "unchanged"
        else:
            return "changed" # DANGER! Rug pull detected!