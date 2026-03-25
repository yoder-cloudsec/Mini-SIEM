import time
import random
import requests
import json
from datetime import datetime

ELASTIC_URL = "http://localhost:9200/logs/_doc"
USERNAME = "elastic"
PASSWORD = "changeme"

users = ["brent", "hacker", "admin"]
ips = ["192.168.1.10", "10.0.0.5", "8.8.8.8"]

def generate_log():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "user": random.choice(users),
        "source_ip": random.choice(ips),
        "event_type": random.choice(["login_successful", "login_failed"]),
        "message": "Login Attempt"
    }

while True:
    log = generate_log()
    res = requests.post(ELASTIC_URL, json=log, auth=(USERNAME, PASSWORD))
    print("Sent:\n", json.dumps(log, indent=4))
    

    requests.post("http://localhost:9200/logs/_refresh", auth=(USERNAME, PASSWORD))
    
    time.sleep(1)
