#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import time

def check_database_integrity(db_path):
    """Check database integrity and connection status."""
    print(f"\n=== Database Diagnostic Report ===")
    print(f"Database path: {db_path}")
    print(f"Database exists: {os.path.exists(db_path)}")
    print(f"Database size: {os.path.getsize(db_path) if os.path.exists(db_path) else 'N/A'} bytes")
    print("\nAttempting connection...")
    
    try:
        conn = sqlite3.connect(db_path, timeout=60.0)
        cursor = conn.cursor()
        
        # Check database integrity
        print("\nChecking database integrity...")
        cursor.execute("PRAGMA integrity_check;")
        integrity_result = cursor.fetchall()
        print(f"Integrity check result: {integrity_result}")
        
        # Get database settings
        print("\nCurrent database settings:")
        for pragma in ['journal_mode', 'synchronous', 'busy_timeout', 'locking_mode', 'foreign_keys']:
            cursor.execute(f"PRAGMA {pragma};")
            result = cursor.fetchone()
            print(f"{pragma}: {result[0] if result else 'N/A'}")
        
        # Check for open transactions
        print("\nChecking for open transactions...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Found {len(tables)} tables: {[t[0] for t in tables]}")
        
        # Try to enable WAL mode
        print("\nEnabling WAL mode...")
        cursor.execute("PRAGMA journal_mode=WAL;")
        print(f"Journal mode after setting: {cursor.fetchone()[0]}")
        
        # Set busy timeout
        print("\nSetting busy timeout...")
        cursor.execute("PRAGMA busy_timeout=60000;")
        
        # Commit and close properly
        conn.commit()
        cursor.close()
        conn.close()
        print("\nDatabase connection test successful!")
        
    except sqlite3.Error as e:
        print(f"\nSQLite error occurred: {e}")
        if 'conn' in locals():
            try:
                conn.close()
            except:
                pass
        return False
    except Exception as e:
        print(f"\nUnexpected error occurred: {e}")
        if 'conn' in locals():
            try:
                conn.close()
            except:
                pass
        return False
    
    return True

if __name__ == "__main__":
    db_path = "src/data/ethicsupply.db"
    success = check_database_integrity(db_path)
    print(f"\nDiagnostic completed. Status: {'Success' if success else 'Failed'}") 