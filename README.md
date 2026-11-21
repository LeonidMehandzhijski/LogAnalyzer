# Log Analyzer

A Python CLI tool that parses web server access logs, detects anomalies,
and can alert in real time, built to learn Python fundamentals alongside
core DevOps practices (containerization, CI, monitoring patterns).

[![Test Log Analyzer](https://github.com/LeonidMehandzhijski/LogAnalyzer/actions/workflows/github.yml/badge.svg)](https://github.com/LeonidMehandzhijski/LogAnalyzer/actions/workflows/github.yml)

## What it does

Two separate programs that read the same log format:

- **`analyze_logs.py` (batch):** reads an existing log file once, prints a summary (error count, most-hit path, most active IP, suspicious IPs), then exits.
- **`monitor_logs.py` (live):** starts at the end of a log file, watches for new entries as they are appended, and prints alerts as they happen. Runs until you press Ctrl+C.

## Features

- Parses structured log entries (timestamp, IP, method, path, status)
- Summarizes traffic from pre-generated log file: error counts, most-hit path, most active IP
- **Live monitoring** -> `monitor_logs.py` watches new entries appended to a log file and prints alerts in the CLI
- **Suspicious activity detection** -> flags IPs making an unusual number of
  requests within a short time window (possible bot/attack traffic)
- **Discord alerts** -> sends a notification when an IP reaches the configured suspicious-request threshold, not for routine errors
- Alert thresholds, time windows, and error-alert cooldown are configurable via `config.json`
- Docker image runs the batch analyzer
- GitHub Actions runs the unit tests and batch analyzer on pushes and pull requests

## Design decisions worth knowing

- **Live monitoring is silent unless something's wrong.** It prints error alerts and suspicious-IP alerts, not every request.
- **Discord alerts are sent for suspicious-IP alerts.** Routine HTTP errors print locally; the webhook is used for suspicious activity.
- **Suspicious-IP alerts fire once per incident.** An alert fires when the configured request count is reached within the configured time window.
- Secrets (the Discord webhook URL) are loaded from a `.env` file, they never get
  committed see `.env.example`.

## Project structure

| File | Purpose |
|---|---|
| `analyze_logs.py` | Batch summary of an existing log file |
| `monitor_logs.py` | Live monitor that alerts on new entries |
| `generate_logs.py` | Creates a sample `access.log` |
| `simulate_traffic.py` | Appends fake entries to `access.log`, with occasional bursts from one IP, so the monitor has something to react to |
| `config.json` | Thresholds, time windows, and cooldown |
| `.env.example` | Template for the Discord webhook URL |
| `Dockerfile` | Image for the batch analyzer |
| `.github/workflows/github.yml` | CI workflow |

## Log format

One request per line: timestamp, IP, method, path, status code.

```
2026-06-21 18:57:40 6.163.237.109 POST /products 200
```

## Running it

### Setup

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

### Batch analysis

```
python generate_logs.py    # creates a sample access.log
python analyze_logs.py     # prints a summary and exits
```

### Live monitoring

Open two terminals in the project directory.

```
# Terminal 1
python monitor_logs.py

# Terminal 2
python simulate_traffic.py
```

The monitor starts at the end of `access.log`, so it only reports entries added after it starts. `simulate_traffic.py` occasionally sends a burst of requests from one IP (`6.6.6.6`) to trigger suspicious-IP detection. Press Ctrl+C in each terminal to stop.

### Discord alerts (optional)

Put your webhook URL in `.env` as `DISCORD_WEBHOOK_URL`. Without it, alerts only print in the terminal. The `.env` file is gitignored, so the URL is never committed.

### With Docker

Generate `access.log` first (see above), then:

```powershell
docker build -t log-analyzer .
docker run --rm -v "${PWD}/access.log:/app/access.log" log-analyzer
```

On Linux / macOS, use `$(pwd)` instead of `${PWD}`. The image runs the batch analyzer only. Live monitoring and traffic simulation run locally.

### Tests

```
python -m unittest discover -s tests -v
```

## Sample output

Batch analyzer:

```
PS D:\Projects\log-analyzer> python analyze_logs.py
210 logs had status codes of 400 or higher
/ was the most-hit path
15.6.76.29 made the most requests
Suspicious IPs: []
```

Live monitor (in a separate terminal, while `simulate_traffic.py` runs):

```
ALERT: 500 from 171.59.178.147 on /products
ALERT: 500 from 6.6.6.6 on /admin
SUSPICIOUS: 6.6.6.6 made 5 requests within 10s
ALERT: 404 from 6.6.6.6 on /products
```

## What I learned building this

Note #1
This was my first journey into Python.
The language is definitely way different from what I am usually used to...
I've been dealing with C++ and Java at my faculty, privately mostly I've been using TS. It was fun albeit it causing frustrations at time.
Getting used to not typing ; at the end of every line is weird.
It is also the start of my DevOps journey. I used Claude as a teacher to guide me through and shepherd me in a way through the code.
It was all hand written right now as I want to get a grasp of Python before delving into AI assisted coding. Claude was used for code review and just as a architectural guide through the whole process.

Note #2
After stepping back and looking at the project again, I decided to clean up instead of focusing on adding new features.
I separated the code and made monitor_logs that does just what the name implies. Monitors the log as simulate_traffic makes it directly in the CLI.
Simulate traffic also writes all this down into access.log, then using analyze_logs it gives us a summary of requests amounts what path got hit the most etc.
I also learned something new along the way, unit tests!
Something you always hear about. This is the first time I've practically used them for one of my projects and I'm not sure how I haven't used it till now...
Next step is probably making a place to display everything to be more readable, probably using Flask on a webpage.
