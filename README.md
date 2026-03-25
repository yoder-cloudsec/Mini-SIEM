# Mini-SIEM

A lightweight Security Information and Event Management (SIEM) system built with Python, Docker, Elasticsearch, and Kibana. This project demonstrates how to collect, store, and visualize log data in real-time.

---

## Features

- **Log Collection:** Simulates user login events and sends them to Elasticsearch.
- **Detection Engine:** Monitors for suspicious activity such as brute-force login attempts.
- **Visualization:** Explore and analyze logs using Kibana dashboards.
- **Dockerized:** Easily deployable with Docker and Docker Compose.
- **Lightweight & Extensible:** Built for learning, experimentation, and small-scale testing.

---

## Project Structure

```text
mini-siem/
│
├── logcollector.py      # Simulates logs and sends them to Elasticsearch
├── detector.py       # Monitors logs for suspicious events
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

## Prerequisites
Docker

Docker Compose

Python 3.10+ (if you want to run scripts outside Docker)

## Setup and Installation
Clone the repository:

``git clone https://github.com/yourusername/mini-siem.git``

``cd mini-siem``

Install Python dependencies (optional if running scripts outside Docker):

``pip install -r requirements.txt``

Start Elasticsearch and Kibana using Docker Compose:

``docker-compose up -d``

Elasticsearch will be available at: http://localhost:9200

Kibana will be available at: http://localhost:5601

⚠️ Make sure Elasticsearch is healthy (_cluster/health should return yellow or green) before starting Kibana.

## Usage

1. Start the Log Collector

``python3 logcollector.py``

Generates random login events (login_successful / login_failed)

Sends logs to Elasticsearch every second

Forces a refresh so logs are immediately searchable by detector.py

2. Start the Detection Engine

``python3 detector.py``

Monitors Elasticsearch for failed login attempts

Prints alerts for potential brute-force attacks

Uses ANSI colors for highlighting alerts in the terminal

3. Explore Logs in Kibana
Open Kibana at http://localhost:5601

Go to Stack Management → Data Views

Create a Data View for your index (e.g., logs*)

Set the Time Field to @timestamp or timestamp

Navigate to Discover to view your logs in real-time

## Configuration
Elasticsearch URL, credentials, and index are configured in logcollector.py and detector.py:

ELASTIC_URL = "http://localhost:9200/logs/_doc"

USERNAME = "elastic"

PASSWORD = "changeme"

Detection thresholds (e.g., brute-force attempts) can be configured in detector.py:

BRUTE_FORCE_THRESHOLD = 5

CHECK_INTERVAL = 10  # seconds

## Notes

This project is educational and experimental — do not use in production without proper security and hardening.

For real deployments, secure Elasticsearch with TLS and service accounts.
