# Log Analyzer improvement plan

This project will become a small, production-inspired observability tool:
a traffic source writes structured logs, a monitor tails and alerts on them,
and a reporting command analyzes retained log files.

## Phase 1: establish a clean baseline

- [x] Move imports to module tops and apply consistent Python naming/formatting.
- [ ] Make reporting behaviour explicit (whole file by default, clear empty-file handling).
- [ ] Add a minimal test suite for parsing, reporting, and anomaly detection.
- [ ] Add formatting/lint checks to CI.

## Phase 2: separate the product responsibilities

- [ ] Split parsing, reporting, anomaly detection, Discord alerts, and CLI code into focused modules.
- [ ] Replace `--watch` with explicit `report` and `monitor` commands.
- [ ] Keep the traffic simulator as a demo/development utility, separate from the product CLI.
- [ ] Handle malformed lines without stopping the monitor, and use meaningful exit codes.

## Phase 3: make the operational behaviour credible

- [ ] Validate configuration and document all settings.
- [ ] Make Discord delivery failures visible and preserve alert deduplication/cooldowns.
- [ ] Add a real-world log-format option (for example, Nginx combined logs) or document the custom format precisely.
- [ ] Add a Docker Compose demo that runs the generator and monitor together.

## Phase 4: polish the portfolio presentation

- [ ] Rewrite the README around the architecture, commands, design choices, and verification.
- [ ] Add a short architecture diagram and realistic terminal output.
- [ ] Add a concise CV-ready project description and resume bullet points.
- [ ] Tag a release and include a screenshot/GIF of the working monitoring demo.

## Current step

Start with the first Phase 1 item. Keep this change behaviour-preserving,
then verify the scripts still compile before making functional changes.
