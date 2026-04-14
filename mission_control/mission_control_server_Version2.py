from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from .jobs import JobManager
from .openclaw_adapter import openclaw_status

app = FastAPI(title="OpenClaw Mission Control (small)")
jobs = JobManager()


class RunRequest(BaseModel):
    # Example: "run --task 'hello'" or "models list"
    args: str


INDEX_HTML = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>OpenClaw Mission Control</title>
    <style>
      body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; margin: 24px; }
      input { width: 520px; padding: 8px; }
      button { padding: 8px 12px; margin: 6px 8px 6px 0; }
      pre { background: #111; color: #eee; padding: 12px; overflow: auto; }
      .row { margin: 10px 0; }
    </style>
  </head>
  <body>
    <h1>OpenClaw Mission Control (small)</h1>

    <div class="row">
      <button onclick="status()">Status</button>
      <button onclick="refresh()">Refresh jobs</button>
    </div>

    <div class="row">
      <label>OpenClaw args:</label><br/>
      <input id="args" value="--help" />
      <button onclick="run()">Run</button>
    </div>

    <h2>Status output</h2>
    <pre id="status"></pre>

    <h2>Jobs</h2>
    <pre id="jobs"></pre>

    <script>
      async function status() {
        const res = await fetch('/api/status');
        const data = await res.json();
        document.getElementById('status').textContent = JSON.stringify(data, null, 2);
      }

      async function run() {
        const args = document.getElementById('args').value;
        const res = await fetch('/api/run', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({args})
        });
        const data = await res.json();
        await refresh();
        alert('Started job: ' + data.job_id);
      }

      async function refresh() {
        const res = await fetch('/api/jobs');
        const data = await res.json();
        document.getElementById('jobs').textContent = JSON.stringify(data, null, 2);
      }

      status();
      refresh();
    </script>
  </body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def index():
    return INDEX_HTML


@app.get("/api/health")
def health():
    return {"ok": True}


@app.get("/api/status")
def status():
    code, out, err = openclaw_status()
    return {"exit_code": code, "stdout": out, "stderr": err}


@app.post("/api/run")
def run(req: RunRequest):
    job_id = jobs.run_openclaw(req.args)
    return {"job_id": job_id}


@app.get("/api/jobs")
def list_jobs():
    return jobs.list_jobs()


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):
    return jobs.get_job(job_id)