#!/usr/bin/env python3
"""Update the .env file with your OpenRouter API key."""

from pathlib import Path

env_path = Path(".env")

print("=" * 60)
print("Update OpenRouter API Key in .env file")
print("=" * 60)
print()

# Get the API key from user
print("Please paste your OpenRouter API key:")
print("(It should start with 'sk-or-v1-' and be about 70 characters long)")
print()
api_key = input("API Key: ").strip()

# Remove quotes if present
api_key = api_key.strip('"\'')

if not api_key:
    print("\n❌ No API key provided. Exiting.")
    exit(1)

if not api_key.startswith("sk-or-v1-"):
    print("\n⚠️  Warning: API key doesn't start with 'sk-or-v1-'")
    response = input("Continue anyway? (y/n): ")
    if response.lower() != 'y':
        exit(1)

if len(api_key) < 50:
    print(f"\n⚠️  Warning: API key seems too short ({len(api_key)} chars, expected ~70)")
    response = input("Continue anyway? (y/n): ")
    if response.lower() != 'y':
        exit(1)

# Read existing .env file
env_content = []
if env_path.exists():
    with open(env_path, 'r') as f:
        env_content = f.readlines()
else:
    env_content = []

# Update or add the API key
updated = False
new_content = []
for line in env_content:
    if line.strip().startswith('OPENROUTER_API_KEY='):
        new_content.append(f'OPENROUTER_API_KEY={api_key}\n')
        updated = True
    else:
        new_content.append(line)

# If not found, add it
if not updated:
    # Remove any trailing newlines
    while new_content and new_content[-1].strip() == '':
        new_content.pop()
    new_content.append(f'\nOPENROUTER_API_KEY={api_key}\n')

# Write back to file
with open(env_path, 'w') as f:
    f.writelines(new_content)

print()
print("✅ .env file updated!")
print(f"   Key length: {len(api_key)}")
print(f"   Key preview: {api_key[:25]}...")
print()
print("Now restart your server to use the new key.")

