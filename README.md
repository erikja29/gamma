# OpenClaw Mission Control (Python)

A small local “mission control” web UI + API for running **OpenClaw** commands, with **status** as the primary command.

## Features
- Web UI at `/` (simple HTML)
- API endpoints for status + running commands
- Captures stdout/stderr and exit codes

## Requirements
- Python 3.10+ (3.11+ recommended)
- OpenClaw CLI installed and available on your PATH

## Setup
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the Mission Control server
```bash
python scripts/run_mission_control.py
```

Open your browser:
- http://127.0.0.1:8000/

## Primary command: status
The UI is designed around **status** being the top command.

If your OpenClaw binary is not named `openclaw`, change:
- `mission_control/openclaw_adapter.py` → `OPENCLAW_BIN`

## API
- `GET /api/health` — server health
- `GET /api/status` — runs the OpenClaw status command
- `POST /api/run` — run an arbitrary OpenClaw command
- `GET /api/jobs` — list job history
- `GET /api/jobs/{job_id}` — job details

## Security note
This is intended for **local use**. Do not expose it to the public internet without adding authentication.