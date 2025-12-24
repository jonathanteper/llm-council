#!/usr/bin/env python3
"""Diagnostic script to check .env file loading and API key configuration."""

import os
from pathlib import Path
from dotenv import load_dotenv

print("=" * 60)
print("Environment Variable Diagnostic")
print("=" * 60)
print()

# Check if .env file exists
env_path = Path(".env")
print(f"1. .env file exists: {env_path.exists()}")
if env_path.exists():
    print(f"   Path: {env_path.absolute()}")
    print(f"   Size: {env_path.stat().st_size} bytes")
    print()
    
    # Try to read .env file content (safely)
    try:
        with open(env_path, 'r') as f:
            lines = f.readlines()
            print(f"   Lines in file: {len(lines)}")
            for i, line in enumerate(lines, 1):
                if 'OPENROUTER_API_KEY' in line or 'API_KEY' in line.upper():
                    # Mask the key for security
                    if '=' in line:
                        key_part = line.split('=')[1].strip()
                        masked = key_part[:15] + '...' + key_part[-5:] if len(key_part) > 20 else '***'
                        print(f"   Line {i}: {line.split('=')[0].strip()}={masked}")
                    else:
                        print(f"   Line {i}: {line.strip()[:50]}...")
    except Exception as e:
        print(f"   Error reading file: {e}")
else:
    print("   ⚠️  .env file not found!")
print()

# Check environment variable before loading
print("2. Environment variable BEFORE load_dotenv():")
key_before = os.getenv("OPENROUTER_API_KEY")
print(f"   OPENROUTER_API_KEY: {'SET' if key_before else 'NOT SET'}")
if key_before:
    print(f"   Length: {len(key_before)}")
    print(f"   Preview: {key_before[:25]}...")
print()

# Load .env file
print("3. Loading .env file with load_dotenv()...")
result = load_dotenv()
print(f"   load_dotenv() returned: {result}")
print()

# Check environment variable after loading
print("4. Environment variable AFTER load_dotenv():")
key_after = os.getenv("OPENROUTER_API_KEY")
print(f"   OPENROUTER_API_KEY: {'SET' if key_after else 'NOT SET'}")
if key_after:
    print(f"   Length: {len(key_after)}")
    print(f"   Starts with 'sk-or-v1-': {key_after.startswith('sk-or-v1-')}")
    print(f"   Preview: {key_after[:25]}...")
    print(f"   Last 10 chars: ...{key_after[-10:]}")
    
    # Check for common issues
    print()
    print("5. Key validation:")
    if key_after == "sk-or-v1-your-api-key-here":
        print("   ❌ Key is still the placeholder!")
    elif not key_after.startswith("sk-or-v1-"):
        print("   ⚠️  Key doesn't start with 'sk-or-v1-'")
    elif len(key_after) < 50:
        print(f"   ⚠️  Key seems too short (expected ~70+ chars, got {len(key_after)})")
    else:
        print("   ✅ Key format looks correct")
    
    # Check for whitespace issues
    stripped = key_after.strip()
    if stripped != key_after:
        print(f"   ⚠️  Key has leading/trailing whitespace!")
        print(f"      Original length: {len(key_after)}")
        print(f"      Stripped length: {len(stripped)}")
else:
    print("   ❌ Key is NOT SET after loading .env file!")
    print()
    print("   Troubleshooting:")
    print("   • Check that .env file contains: OPENROUTER_API_KEY=sk-or-v1-...")
    print("   • Make sure there are no spaces around the = sign")
    print("   • Check for quotes (should NOT have quotes)")
    print("   • Verify the file is in the project root directory")

print()
print("=" * 60)

# Try importing from backend.config
print()
print("6. Testing backend.config import:")
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from backend.config import OPENROUTER_API_KEY as CONFIG_KEY
    print(f"   Key from backend.config: {'SET' if CONFIG_KEY else 'NOT SET'}")
    if CONFIG_KEY:
        print(f"   Length: {len(CONFIG_KEY)}")
        print(f"   Matches env var: {CONFIG_KEY == key_after}")
except Exception as e:
    print(f"   Error importing: {e}")

print()
print("=" * 60)

