"""Configuration for the LLM Council."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root (parent of backend directory)
# Try multiple possible locations
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"

# Also check current working directory as fallback
cwd_env = Path.cwd() / ".env"
if not env_path.exists() and cwd_env.exists():
    print(f"[Config] .env not found at {env_path}, trying {cwd_env}")
    env_path = cwd_env

# Print what we're actually using
print(f"[Config] Using .env file at: {env_path.absolute()}")
print(f"[Config] Current working directory: {Path.cwd()}")
print(f"[Config] __file__ location: {Path(__file__).absolute()}")

# Check if key is already set in environment (before loading .env)
key_before = os.getenv("OPENROUTER_API_KEY")
if key_before:
    print(f"[Config] WARNING: OPENROUTER_API_KEY already set in environment!")
    print(f"[Config]   Environment value: {key_before[:20]}... (length: {len(key_before)})")
    print(f"[Config]   This will be OVERRIDDEN by .env file")

# Read .env file directly FIRST to see what's actually in it
key_from_file = None
if env_path.exists():
    try:
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip().startswith('OPENROUTER_API_KEY='):
                    key_from_file = line.split('=', 1)[1].strip()
                    print(f"[Config] Key found in .env file (direct read): {key_from_file[:20]}... (length: {len(key_from_file)})")
                    break
    except Exception as e:
        print(f"[Config] Error reading .env file directly: {e}")
else:
    print(f"[Config] WARNING: .env file does not exist at {env_path.absolute()}")

# Load .env file, OVERRIDE existing environment variables
load_dotenv(dotenv_path=env_path, override=True)

# OpenRouter API key - try from environment first, then fall back to direct file read
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# If load_dotenv didn't work, use the key we read directly from file
if not OPENROUTER_API_KEY and key_from_file:
    print(f"[Config] load_dotenv() didn't set key, using direct file read")
    OPENROUTER_API_KEY = key_from_file
    os.environ["OPENROUTER_API_KEY"] = key_from_file

# Debug: Print key status (first 20 chars only for security)
print(f"[Config] .env file path: {env_path}")
print(f"[Config] .env file exists: {env_path.exists()}")
if OPENROUTER_API_KEY:
    print(f"[Config] API key loaded: {OPENROUTER_API_KEY[:20]}... (length: {len(OPENROUTER_API_KEY)})")
    if OPENROUTER_API_KEY == "sk-or-v1-your-api-key-here":
        print("[Config] ❌ ERROR: Key is still the placeholder! Check your .env file!")
    elif len(OPENROUTER_API_KEY) < 50:
        print(f"[Config] ⚠️  WARNING: Key seems too short (expected ~70+ chars)")
else:
    print("[Config] WARNING: OPENROUTER_API_KEY is not set!")

# Council members - list of OpenRouter model identifiers
COUNCIL_MODELS = [
    "openai/gpt-5.1",
    "google/gemini-3-pro-preview",
    "anthropic/claude-sonnet-4.5",
    "x-ai/grok-4",
]

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = "google/gemini-3-pro-preview"

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Data directory for conversation storage
DATA_DIR = "data/conversations"
