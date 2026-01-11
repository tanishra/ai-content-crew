"""
Python Client Example for AI Content Crew API

Usage:
    python examples/python_client.py
"""

import requests
import time
import json

# Configuration
API_BASE_URL = "http://localhost:8000"
API_KEY = None  # Will be set after signup

def signup(email: str):
    """Sign up and get API key"""
    response = requests.post(
        f"{API_BASE_URL}/signup",
        json={"email": email}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Signup successful!")
        print(f"   Email: {data['email']}")
        print(f"   API Key: {data['api_key']}")
        print(f"   Plan: {data['subscription_tier']}")
        print(f"   Monthly Limit: {data['monthly_limit']}")
        return data['api_key']
    else:
        print(f"❌ Signup failed: {response.json()}")
        return None

def generate_content(api_key: str, topic: str):
    """Generate content for a topic"""
    headers = {"X-API-Key": api_key}
    response = requests.post(
        f"{API_BASE_URL}/generate",
        json={"topic": topic},
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n🚀 Generation started!")
        print(f"   Job ID: {data['job_id']}")
        print(f"   Status: {data['status']}")
        return data['job_id']
    else:
        print(f"❌ Generation failed: {response.json()}")
        return None

def check_status(api_key: str, job_id: str):
    """Check job status"""
    headers = {"X-API-Key": api_key}
    response = requests.get(
        f"{API_BASE_URL}/status/{job_id}",
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Status check failed: {response.json()}")
        return None

def wait_for_completion(api_key: str, job_id: str, max_wait: int = 300):
    """Wait for job to complete (max 5 minutes)"""
    print(f"\n⏳ Waiting for completion...")
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        status_data = check_status(api_key, job_id)
        
        if status_data:
            status = status_data['status']
            print(f"   Status: {status}", end='\r')
            
            if status == "completed":
                print(f"\n✅ Generation completed!")
                print(f"   Report: {status_data['result']['report']}")
                print(f"   Blog: {status_data['result']['blog']}")
                return status_data
            elif status == "failed":
                print(f"\n❌ Generation failed!")
                print(f"   Error: {status_data.get('error', 'Unknown error')}")
                return status_data
        
        time.sleep(5)  # Check every 5 seconds
    
    print(f"\n⏱️  Timeout: Job did not complete in {max_wait} seconds")
    return None

def get_usage(api_key: str):
    """Get usage statistics"""
    headers = {"X-API-Key": api_key}
    response = requests.get(
        f"{API_BASE_URL}/usage",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Usage Statistics:")
        print(f"   Email: {data['email']}")
        print(f"   Plan: {data['subscription_tier']}")
        print(f"   Used: {data['usage_count']}/{data['monthly_limit']}")
        print(f"   Remaining: {data['remaining']}")
        return data
    else:
        print(f"❌ Usage check failed: {response.json()}")
        return None

def main():
    """Main example workflow"""
    print("=" * 60)
    print("AI Content Crew API - Python Client Example")
    print("=" * 60)
    
    # Step 1: Sign up (or use existing API key)
    print("\n📝 Step 1: User Signup")
    email = input("Enter your email (or press Enter for default): ").strip()
    if not email:
        email = f"test_{int(time.time())}@example.com"
    
    api_key = signup(email)
    if not api_key:
        print("Signup failed. Using existing key? (y/n): ")
        use_existing = input().strip().lower()
        if use_existing == 'y':
            api_key = input("Enter your API key: ").strip()
        else:
            return
    
    # Step 2: Generate content
    print("\n📝 Step 2: Generate Content")
    topic = input("Enter topic (or press Enter for default): ").strip()
    if not topic:
        topic = "Future of Artificial Intelligence"
    
    job_id = generate_content(api_key, topic)
    if not job_id:
        return
    
    # Step 3: Wait for completion
    result = wait_for_completion(api_key, job_id)
    
    # Step 4: Check usage
    get_usage(api_key)
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()