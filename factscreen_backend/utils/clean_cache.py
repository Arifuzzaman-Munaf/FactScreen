#!/usr/bin/env python3
"""
Script to clean Python cache files from the FactScreen project, including pytest cache.
"""

import os
import shutil
import sys
from pathlib import Path

def clean_python_cache():
    """Remove all Python cache files, pytest cache, and directories"""
    
    # Get the project root directory
    project_root = Path(__file__).parent
    
    print("🧹 Cleaning Python cache files...")
    print(f"📁 Project root: {project_root}")
    
    # Counters for removed items
    pycache_dirs_removed = 0
    pyc_files_removed = 0
    pyo_files_removed = 0
    pytest_cache_dirs_removed = 0

    # Remove __pycache__ directories
    for pycache_dir in project_root.rglob("__pycache__"):
        if pycache_dir.is_dir():
            try:
                shutil.rmtree(pycache_dir)
                pycache_dirs_removed += 1
                print(f"  ✅ Removed: {pycache_dir.relative_to(project_root)}")
            except Exception as e:
                print(f"  ❌ Error removing {pycache_dir}: {e}")

    # Remove .pyc files
    for pyc_file in project_root.rglob("*.pyc"):
        if pyc_file.is_file():
            try:
                pyc_file.unlink()
                pyc_files_removed += 1
                print(f"  ✅ Removed: {pyc_file.relative_to(project_root)}")
            except Exception as e:
                print(f"  ❌ Error removing {pyc_file}: {e}")

    # Remove .pyo files
    for pyo_file in project_root.rglob("*.pyo"):
        if pyo_file.is_file():
            try:
                pyo_file.unlink()
                pyo_files_removed += 1
                print(f"  ✅ Removed: {pyo_file.relative_to(project_root)}")
            except Exception as e:
                print(f"  ❌ Error removing {pyo_file}: {e}")

    # Remove pytest cache directories (.pytest_cache)
    for pytest_cache_dir in project_root.rglob(".pytest_cache"):
        if pytest_cache_dir.is_dir():
            try:
                shutil.rmtree(pytest_cache_dir)
                pytest_cache_dirs_removed += 1
                print(f"  ✅ Removed pytest cache: {pytest_cache_dir.relative_to(project_root)}")
            except Exception as e:
                print(f"  ❌ Error removing pytest cache {pytest_cache_dir}: {e}")

    # Summary
    print("\n📊 Cleanup Summary:")
    print(f"  🗂️  __pycache__ directories removed: {pycache_dirs_removed}")
    print(f"  🗑️  .pytest_cache directories removed: {pytest_cache_dirs_removed}")
    print(f"  📄 .pyc files removed: {pyc_files_removed}")
    print(f"  📄 .pyo files removed: {pyo_files_removed}")
    
    total_removed = pycache_dirs_removed + pyc_files_removed + pyo_files_removed + pytest_cache_dirs_removed
    
    if total_removed > 0:
        print(f"\n✅ Successfully cleaned {total_removed} cache files/directories!")
    else:
        print("\n✨ No cache files found - project is already clean!")
    
    return total_removed

def main():
    """Main function"""
    print("=" * 50)
    print("FactScreen Cache Cleaner")
    print("=" * 50)
    
    try:
        removed_count = clean_python_cache()
        print("\n" + "=" * 50)
        print("Cache cleanup completed!")
        print("=" * 50)
        
        return 0 if removed_count >= 0 else 1
        
    except Exception as e:
        print(f"\n❌ Error during cleanup: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
