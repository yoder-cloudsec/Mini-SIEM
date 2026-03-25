import requests
import time
import json
from datetime import datetime

ELASTIC_SEARCH_URL = "http://localhost:9200/logs/_search"
USERNAME = "elastic"
PASSWORD = "changeme"
CHECK_INTERVAL = 10  # seconds
BRUTE_FORCE_THRESHOLD = 5

# ANSI COLORS FOR OUTPUT
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# IP TRACKING
alerted_ips = set()


def check_bruteforce():
    query = {
        "size": 0,  
        "query": {
            "match": {"event_type": "login_failed"}
        },
        "aggs": {
            "by_ip": {
                "terms": {"field": "source_ip.keyword", "size": 100}
            }
        }
    }

    try:
        res = requests.post(
            ELASTIC_SEARCH_URL,
            json=query,
            auth=(USERNAME, PASSWORD),
            timeout=5
        )

        if res.status_code != 200:
            print(f"{RED}[ERROR] HTTP {res.status_code}{RESET}")
            print(res.text)
            return

        data = res.json()

        timestamp = datetime.utcnow().isoformat()
        print(f"\n[{timestamp}] FULL RESPONSE:")
        print(json.dumps(data, indent=2, sort_keys=True))

        buckets = data.get("aggregations", {}).get("by_ip", {}).get("buckets", [])

        if not buckets:
            print(f"{GREEN}[INFO] No aggregation data found{RESET}")
            return

        for bucket in buckets:
            ip = bucket["key"]
            count = bucket["doc_count"]

            if count > BRUTE_FORCE_THRESHOLD:
                if ip not in alerted_ips:
                    print(f"{RED}[{timestamp}] 🚨 ALERT: POSSIBLE BRUTE FORCE ATTACK FROM {ip} ({count} attempts){RESET}")
                    alerted_ips.add(ip)
            else:
                print(f"{YELLOW}[{timestamp}] Info: {ip} has {count} failed attempts{RESET}")

    except requests.exceptions.RequestException as e:
        print(f"{RED}[ERROR] Request failed: {e}{RESET}")


if __name__ == "__main__":
    while True:
        check_bruteforce()
        time.sleep(CHECK_INTERVAL)
