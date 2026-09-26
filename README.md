# Log Analyzer

A Python CLI tool that parses web server access logs, detects anomalies, 
and can alert in real time, built to learn Python fundamentals alongside 
core DevOps practices (containerization, CI, monitoring patterns).

[![Test Log Analyzer](https://github.com/LeonidMehandzhijski/LogAnalyzer/actions/workflows/github.yml/badge.svg)](https://github.com/LeonidMehandzhijski/LogAnalyzer/actions/workflows/github.yml)

## Features

- Parses structured log entries (timestamp, IP, method, path, status)
- Summarizes traffic from pre-generated log file: error counts, most-hit path, most active IP
- **Watch mode** -> Watches a simulation of traffic and sends live alerts in the CLI
- **Suspicious activity detection** -> flags IPs making an unusual number of 
  requests within a short time window (possible bot/attack traffic)
- **Discord alerts** -> sends a notification for sustained suspicious activity 
  only, not routine errors, to avoid alert fatigue
- Fully configurable via `config.json` (thresholds, windows) — no hardcoded values
- Dockerized for portable, consistent execution anywhere
- CI via GitHub Actions so that every push is automatically tested

## Design decisions worth knowing

- **Watch mode is silent unless something's wrong.** If the monitoring tool were to print every GET or POST no one would read it.
- **Discord alerts are sent for high importance alerts** Routine errors print locally; only sustained, unusual 
  patterns get pushed externally
- **Suspicious-IP alerts fire once per incident**, it's to avoid alert fatigue, it only prints after certain thresholds have been met long enough.
- Secrets (the Discord webhook URL) are loaded from a `.env` file, they never get
  committed see `.env.example`.

## Running it

### Locally
\`\`\`bash
- pip install -r requirements.txt
- cp .env.example .env   # then fill in your Discord webhook URL (optional)
- python generate_logs.py        # creates a sample access.log
- python analyze_logs.py --watch # run with live monitoring
\`\`\`

### With Docker
\`\`\`bash
- docker build -t log-analyzer .
- docker run --rm -v ${PWD}/access.log:/app/access.log log-analyzer
\`\`\`

## Sample output

\`\`\`
PS D:\Programs\log-analyzer> python analyze_logs.py --watch                                        
210 amount of logs had status requests above 400\
/ is the path that got hit the most\
15.6.76.29 is the ip that made the most requests\
Suspicious IPs: []

Watching access.log for new entries... (Ctrl+C to stop)\
ALERT: 500 from 171.59.178.147 on /products\
ALERT: 500 from 6.6.6.6 on /admin\
SUSPICIOUS: 6.6.6.6 made 5 requests within 10s\
ALERT: 404 from 6.6.6.6 on /products

Stopped watching.

First it checks the pre-generated log file, gives a report.
Secondly it watches the live traffic.
\`\`\`

## What I learned building this

[
This was my first journey into Python. 
The language is definitely way different from what I am usually used to...
I've been dealing with C++ and Java at my faculty, privately mostly I've been using TS. It was fun albeit it causing frustrations at time.
Getting used to not typing ; at the end of every line is weird.
It is also the start of my DevOps journey. I used Claude as a teacher to guide me through and shepherd me in a way through the code.
It was all hand written right now as I want to get a grasp of Python before delving into AI assisted coding.
]