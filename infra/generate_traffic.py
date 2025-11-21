#!/usr/bin/env python3
"""
Traffic generator script for URL shortener service
Simulates load by creating URLs and accessing them
"""

import requests
import time
import random
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://localhost:8080"
NUM_REQUESTS = 100
NUM_THREADS = 10

def create_short_url(url):
    """Create a short URL"""
    try:
        response = requests.post(
            f"{BASE_URL}/shorten",
            json={"url": url},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("short_code")
        else:
            print(f"Failed to create URL: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error creating URL: {e}")
        return None

def access_short_url(short_code):
    """Access a short URL (follow redirect)"""
    try:
        response = requests.get(
            f"{BASE_URL}/{short_code}",
            allow_redirects=False,
            timeout=5
        )
        return response.status_code in [302, 404]
    except Exception as e:
        print(f"Error accessing URL: {e}")
        return False

def generate_random_url():
    """Generate a random URL for testing"""
    domains = [
        "https://example.com",
        "https://github.com",
        "https://stackoverflow.com",
        "https://google.com",
        "https://python.org",
        "https://docker.com",
        "https://kubernetes.io",
        "https://prometheus.io",
        "https://grafana.com"
    ]
    path = f"/path/{random.randint(1000, 9999)}"
    return random.choice(domains) + path

def main():
    print(f"Generating traffic to {BASE_URL}")
    print(f"Requests: {NUM_REQUESTS}, Threads: {NUM_THREADS}")
    print("-" * 50)
    
    short_codes = []
    start_time = time.time()
    
    # Phase 1: Create short URLs
    print("Phase 1: Creating short URLs...")
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        for i in range(NUM_REQUESTS):
            url = generate_random_url()
            future = executor.submit(create_short_url, url)
            futures.append(future)
        
        for i, future in enumerate(as_completed(futures)):
            short_code = future.result()
            if short_code:
                short_codes.append(short_code)
            if (i + 1) % 10 == 0:
                print(f"  Created {i + 1}/{NUM_REQUESTS} URLs")
    
    print(f"Created {len(short_codes)} short URLs")
    
    # Phase 2: Access short URLs
    print("\nPhase 2: Accessing short URLs...")
    if short_codes:
        access_count = 0
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            futures = []
            # Access each URL multiple times
            for short_code in short_codes:
                for _ in range(3):  # Access each URL 3 times
                    future = executor.submit(access_short_url, short_code)
                    futures.append(future)
            
            for i, future in enumerate(as_completed(futures)):
                if future.result():
                    access_count += 1
                if (i + 1) % 20 == 0:
                    print(f"  Accessed {i + 1}/{len(futures)} URLs")
        
        print(f"Accessed {access_count} URLs successfully")
    
    # Phase 3: Test 404s
    print("\nPhase 3: Testing 404 handling...")
    fake_codes = [f"fake{random.randint(100000, 999999)}" for _ in range(20)]
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = [executor.submit(access_short_url, code) for code in fake_codes]
        for future in as_completed(futures):
            future.result()
    print("404 tests completed")
    
    elapsed = time.time() - start_time
    print("\n" + "-" * 50)
    print(f"Traffic generation completed in {elapsed:.2f} seconds")
    print(f"Total operations: {NUM_REQUESTS + len(short_codes) * 3 + 20}")
    print(f"Average rate: {(NUM_REQUESTS + len(short_codes) * 3 + 20) / elapsed:.2f} ops/sec")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        NUM_REQUESTS = int(sys.argv[1])
    if len(sys.argv) > 2:
        NUM_THREADS = int(sys.argv[2])
    main()

