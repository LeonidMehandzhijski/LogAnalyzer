# Log Analyzer

A Python CLI tool that parses web server access logs, detects anomalies, 
and can alert in real time — built to learn Python fundamentals alongside 
core DevOps practices (containerization, CI, monitoring patterns).

## Features

- Parses structured log entries (timestamp, IP, method, path, status)
- Summarizes traffic: error counts, most-hit path, most active IP
- **Watch mode** — tails the log file live and reacts to new entries as they arrive
- **Suspicious activity detection** — flags IPs making an unusual number of 
  requests within a short time window (possible bot/attack traffic)
- **Discord alerts** — sends a notification for sustained suspicious activity 
  only, not routine errors, to avoid alert fatigue
- Fully configurable via `config.json` (thresholds, windows) — no hardcoded values
- Dockerized for portable, consistent execution anywhere
- CI via GitHub Actions — every push is automatically tested

## Design decisions worth knowing

- **Watch mode is silent unless something's wrong.** A monitoring tool that 
  prints every normal request is a monitoring tool nobody reads.
- **Discord alerts are reserved for suspicious-activity incidents, not every 
  bad status code.** Routine errors print locally; only sustained, unusual 
  patterns get pushed externally — this avoids alert fatigue, a real problem 
  in production monitoring.
- **Suspicious-IP alerts fire once per incident**, not once per request, using 
  an incident-tracking set that resets once the IP drops back under threshold.
- Secrets (the Discord webhook URL) are loaded from a `.env` file, never 
  committed — see `.env.example`.

## Running it

### Locally
\`\`\`bash
pip install -r requirements.txt
cp .env.example .env   # then fill in your Discord webhook URL (optional)
python generate_logs.py        # creates a sample access.log
python analyze_logs.py --watch # run with live monitoring
\`\`\`

### With Docker
\`\`\`bash
docker build -t log-analyzer .
docker run --rm -v ${PWD}/access.log:/app/access.log log-analyzer
\`\`\`

## Sample output

\`\`\`
[paste a real terminal output here]
\`\`\`

## What I learned building this

[Your words — 2-3 sentences. What was actually new to you: argparse, watch-mode 
file polling, datetime math, Docker layering/caching, environment-based secrets, 
whatever felt like a real "click."]