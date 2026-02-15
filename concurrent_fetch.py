import requests
import time
import concurrent.futures

BASE_URL = "http://localhost:8000/users/"
NUM_REQUESTS = 10000

def fetch_users(request_id):
    """Function to fetch users, returns time taken for the request"""
    start_time = time.time()
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        data = response.json()
        end_time = time.time()
        duration = end_time - start_time
        print(f"Request {request_id}: Status {response.status_code}, Users count: {len(data)}, Time: {duration:.4f}s")
        return duration
    except Exception as e:
        print(f"Request {request_id}: Failed - {e}")
        return None

def main():
    print(f"Starting {NUM_REQUESTS} concurrent requests...")
    
    start_total_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_REQUESTS) as executor:
        # Create a list of futures/tasks
        futures = [executor.submit(fetch_users, i) for i in range(1, NUM_REQUESTS + 1)]
        
        # Wait for all to complete and get results
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    end_total_time = time.time()
    total_duration = end_total_time - start_total_time
    
    # Filter out None results (failures)
    valid_times = [t for t in results if t is not None]
    
    print("\n--- Summary ---")
    print(f"Total time for {NUM_REQUESTS} requests: {total_duration:.4f} seconds")
    if valid_times:
        avg_time = sum(valid_times) / len(valid_times)
        print(f"Average time per request: {avg_time:.4f} seconds")
    else:
        print("All requests failed.")

if __name__ == "__main__":
    main()
