#!/usr/bin/env python3
"""Simple test to verify the API is working"""

import sys
import time

def test_health():
    """Test the health endpoint"""
    import requests
    
    print("\n" + "="*60)
    print("Testing Backend Health")
    print("="*60)
    
    try:
        # Give the server a moment
        time.sleep(1)
        
        response = requests.get("http://localhost:8000/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"✅ Response: {data}")
            print("\n🎉 Backend is working correctly!")
            return True
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed!")
        print("   Make sure the backend is running on port 8000:")
        print("   cd backend && python -m flask --app backend.app run --port 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_health()
    sys.exit(0 if success else 1)
