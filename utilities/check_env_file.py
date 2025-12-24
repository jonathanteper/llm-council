#!/usr/bin/env python3
"""Check what's actually in the .env file."""

from pathlib import Path

env_path = Path(".env")
print("=" * 60)
print("Checking .env file contents")
print("=" * 60)
print(f"File path: {env_path.absolute()}")
print(f"File exists: {env_path.exists()}")
print()

if env_path.exists():
    with open(env_path, 'r') as f:
        content = f.read()
        lines = content.split('\n')
        
    print(f"Total lines: {len(lines)}")
    print(f"Total characters: {len(content)}")
    print()
    
    print("All lines in file:")
    for i, line in enumerate(lines, 1):
        if 'OPENROUTER' in line.upper() or 'API_KEY' in line.upper() or line.strip():
            # Show the line with visible characters
            display = repr(line)
            print(f"  Line {i}: {display}")
    
    print()
    print("Looking for OPENROUTER_API_KEY:")
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('OPENROUTER_API_KEY='):
            key_part = line.split('=', 1)[1] if '=' in line else ''
            print(f"  Found on line {i}")
            print(f"  Full line: {repr(line)}")
            print(f"  Key value: {repr(key_part)}")
            print(f"  Key length: {len(key_part.strip())}")
            print(f"  Key starts with sk-or-v1-: {key_part.strip().startswith('sk-or-v1-')}")
            if len(key_part.strip()) == 26:
                print(f"  ⚠️  This is the placeholder (26 chars)!")
            elif len(key_part.strip()) < 50:
                print(f"  ⚠️  Key seems too short")
            else:
                print(f"  ✅ Key looks correct")
else:
    print("❌ .env file does not exist!")

