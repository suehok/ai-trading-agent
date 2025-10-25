#!/usr/bin/env python3
"""
Script to set the LLM model to deepseek/deepseek-chat-v3.1
"""
import os
import shutil

def set_deepseek_model():
    """Set the LLM model to deepseek/deepseek-chat-v3.1."""
    print("Setting LLM Model to deepseek/deepseek-chat-v3.1...")
    
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
            # Set to deepseek model
            fixed_lines.append('LLM_MODEL="deepseek/deepseek-chat-v3.1"\n')
            print(f"✅ Set: {line.strip()} -> LLM_MODEL=\"deepseek/deepseek-chat-v3.1\"")
        else:
            fixed_lines.append(line)
    
    # Write the fixed .env file
    with open(env_file, 'w') as f:
        f.writelines(fixed_lines)
    
    print(f"✅ Updated {env_file} with deepseek model")
    print("🎉 .env file now uses deepseek/deepseek-chat-v3.1!")

if __name__ == "__main__":
    set_deepseek_model()
