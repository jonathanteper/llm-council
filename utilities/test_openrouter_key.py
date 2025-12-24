#!/usr/bin/env python3
"""
Test OpenRouter API key validity and display account information.

This script prompts for an API key, tests it with a simple model call,
and displays available account information.
"""

import httpx
import json
from typing import Optional, Dict, Any


def get_api_key() -> str:
    """Prompt user to paste their OpenRouter API key."""
    print("=" * 60)
    print("OpenRouter API Key Tester")
    print("=" * 60)
    print("\nPlease paste your OpenRouter API key:")
    print("(Get one at https://openrouter.ai/keys)")
    print()
    
    api_key = input("API Key: ").strip()
    
    # Remove any quotes or whitespace
    api_key = api_key.strip('"\'')
    
    if not api_key:
        print("\n❌ No API key provided. Exiting.")
        exit(1)
    
    if not api_key.startswith("sk-or-v1-"):
        print("\n⚠️  Warning: API key doesn't start with 'sk-or-v1-'")
        print("   Continuing anyway...\n")
    
    return api_key


def get_account_info(api_key: str) -> Optional[Dict[str, Any]]:
    """
    Get account information from OpenRouter API.
    
    Returns:
        Dict with account info, or None if request failed
    """
    url = "https://openrouter.ai/api/v1/key"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"⚠️  Could not fetch account info: HTTP {response.status_code}")
                if response.text:
                    print(f"   Response: {response.text[:200]}")
                return None
    except Exception as e:
        print(f"⚠️  Error fetching account info: {e}")
        return None


def test_api_key_with_model(api_key: str) -> tuple:
    """
    Test the API key by making a simple model call.
    
    Returns:
        Tuple of (success: bool, response_content: str, response_headers: dict)
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "google/gemini-2.5-flash",  # Fast and cheap model
        "messages": [
            {"role": "user", "content": "Hi"}
        ],
    }
    
    try:
        with httpx.Client(timeout=15.0) as client:
            response = client.post(url, headers=headers, json=payload)
            
            # Extract response headers (might contain rate limit info, etc.)
            response_headers = dict(response.headers)
            
            if response.status_code == 200:
                data = response.json()
                content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
                return True, content, response_headers
            else:
                error_text = response.text[:500] if response.text else "No error message"
                return False, f"HTTP {response.status_code}: {error_text}", response_headers
                
    except httpx.TimeoutException:
        return False, "Request timed out after 15 seconds", None
    except httpx.RequestError as e:
        return False, f"Network error: {e}", None
    except Exception as e:
        return False, f"Unexpected error: {e}", None


def format_account_info(account_info: Dict[str, Any]) -> str:
    """Format account information for display."""
    lines = []
    
    # Common fields that might be in the response
    if 'data' in account_info:
        data = account_info['data']
        
        if 'label' in data:
            lines.append(f"  Label: {data['label']}")
        if 'created_at' in data:
            lines.append(f"  Created: {data['created_at']}")
        if 'usage' in data:
            usage = data['usage']
            if isinstance(usage, dict):
                if 'total' in usage:
                    lines.append(f"  Total Usage: ${usage['total']:.4f}")
                if 'credits' in usage:
                    lines.append(f"  Credits: ${usage['credits']:.4f}")
        if 'limits' in data:
            limits = data['limits']
            if isinstance(limits, dict):
                lines.append(f"  Limits: {json.dumps(limits, indent=4)}")
    
    # If no structured data, show raw response
    if not lines:
        lines.append(f"  Raw response: {json.dumps(account_info, indent=2)}")
    
    return "\n".join(lines)


def format_response_headers(headers: Optional[Dict]) -> str:
    """Format response headers that might contain useful info."""
    if not headers:
        return "  (No headers available)"
    
    lines = []
    
    # Look for rate limit headers (common patterns)
    rate_limit_headers = [
        'x-ratelimit-limit',
        'x-ratelimit-remaining',
        'x-ratelimit-reset',
        'ratelimit-limit',
        'ratelimit-remaining',
    ]
    
    found_any = False
    for header_name in rate_limit_headers:
        for key, value in headers.items():
            if header_name.lower() in key.lower():
                lines.append(f"  {key}: {value}")
                found_any = True
    
    if not found_any:
        # Show a few common headers
        common_headers = ['content-type', 'date', 'server']
        for key, value in headers.items():
            if any(common in key.lower() for common in common_headers):
                lines.append(f"  {key}: {value}")
    
    if not lines:
        return "  (No notable headers)"
    
    return "\n".join(lines)


def main():
    """Main function to test OpenRouter API key."""
    # Get API key from user
    api_key = get_api_key()
    
    print("\n" + "=" * 60)
    print("Testing API Key...")
    print("=" * 60)
    print()
    
    # Test with a model call
    print("1. Testing with model call (google/gemini-2.5-flash)...")
    success, result, headers = test_api_key_with_model(api_key)
    
    if success:
        print("   ✅ API Key is VALID!")
        print(f"   Model Response: {result[:100]}{'...' if len(result) > 100 else ''}")
        print()
        print("   Response Headers:")
        print(format_response_headers(headers))
    else:
        print(f"   ❌ API Key test FAILED")
        print(f"   Error: {result}")
        print()
        print("   Troubleshooting:")
        print("   • Check that your API key is correct")
        print("   • Verify you have credits at https://openrouter.ai/")
        print("   • Make sure auto-topup is enabled if needed")
        print()
        return
    
    print()
    print("2. Fetching account information...")
    account_info = get_account_info(api_key)
    
    if account_info:
        print("   ✅ Account information retrieved:")
        print(format_account_info(account_info))
    else:
        print("   ⚠️  Could not retrieve account information")
        print("   (This is okay - the key works for API calls)")
    
    print()
    print("=" * 60)
    print("✅ Test Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

