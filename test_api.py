#!/usr/bin/env python3
"""Test script for the YouTube Transcript Downloader API"""

import json
import requests

BASE_URL = "http://localhost:5000"

# Test 1: Health check
print("=" * 60)
print("Test 1: Health Check")
print("=" * 60)
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n")

# Test 2: Extract transcript from a public YouTube video with captions
print("=" * 60)
print("Test 2: Extract Transcript")
print("=" * 60)
print("Testing with a YouTube video URL...")
print("Note: This requires the video to have captions available")

# Using a video known to have captions
test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # "Me at the zoo" - first ever YouTube video

payload = {
    "url": test_url,
    "language": "en"
}

try:
    print(f"Sending request to: {BASE_URL}/api/transcript")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/api/transcript",
        json=payload,
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    
    if data.get("success"):
        print(f"\n✓ Success!")
        print(f"Segments: {len(data.get('segments', []))}")
        print(f"Words: ~{len(data.get('text', '').split())}")
        print(f"\nFirst 200 characters of transcript:")
        print(f"{data.get('text', '')[:200]}...")
    else:
        print(f"\n✗ Failed")
        print(f"Error: {data.get('error')}")
        
except requests.exceptions.Timeout:
    print("✗ Request timeout (API took too long)")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n")

# Test 3: Invalid URL
print("=" * 60)
print("Test 3: Invalid URL (Error Handling)")
print("=" * 60)

payload = {
    "url": "https://invalid-url.com"
}

try:
    response = requests.post(
        f"{BASE_URL}/api/transcript",
        json=payload,
        timeout=10
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
print("Tests completed!")
print("=" * 60)
