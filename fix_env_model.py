#!/usr/bin/env python3
"""
Script to fix the invalid LLM model in .env file
"""
import os
import shutil

def fix_env_model():
    """Fix the invalid LLM model in .env file."""
    print("Fixing .env LLM Model...")
    
    env_file = ".env"
    backup_file = ".env.backup"
    
    # Create backup
    if os.path.exists(env_file):
        shutil.copy2(env_file, backup_file)
        print(f"✅ Created backup: {backup_file}")
    
    # Read current .env file
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Fix the LLM_MODEL line
    fixed_lines = []
    for line in lines:
        if line.startswith("LLM_MODEL="):
            # Replace with valid model
            fixed_lines.append('LLM_MODEL="x-ai/grok-4"\n')
            print(f"✅ Fixed: {line.strip()} -> LLM_MODEL=\"x-ai/grok-4\"")
        else:
            fixed_lines.append(line)
    
    # Write the fixed .env file
    with open(env_file, 'w') as f:
        f.writelines(fixed_lines)
    
    print(f"✅ Updated {env_file} with valid model")
    print("🎉 .env file has been fixed!")

if __name__ == "__main__":
    fix_env_model()
