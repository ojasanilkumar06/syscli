import psutil
import requests
import json
from datetime import datetime

def load_config(filepath="config.json"):

    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("ERROR: config.json not found.")
        exit(1)
    except json.JSONDecodeError:
        print("ERROR: config.json not formatted correctly.")
        exit(1)

def monitor_system():
    print(f"\n--- SYSTEM METRICS ({datetime.now().strftime('%H:%M:%S')}) ---")
    
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    print(f"CPU Usage:  {cpu}%")
    print(f"RAM Usage:  {ram}%")
    print(f"Disk Usage: {disk}%")

def probe_endpoints(endpoints):
    print("\n--- NETWORK PROBES ---")
    
    for url in endpoints:
        try:
            # request with 3 sec timeout
            response = requests.get(url, timeout=3)
            latency = round(response.elapsed.total_seconds() * 1000)
            
            if response.status_code == 200:
                print(f"[SUCCESS] {url} (Status: {response.status_code}, Latency: {latency}ms)")
            else:
                print(f"[WARNING] {url} returned Status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            # This catches timeouts, DNS failures, and invalid URLs
            print(f"[FAILED]  {url} (Error: Connection failed or timed out)")

if __name__ == "__main__":
    
    config_data = load_config()
    
    
    monitor_system()
    
  
    probe_endpoints(config_data.get("endpoints", []))
    print("\nMonitoring complete.\n")
  
