from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, asdict
from typing import Dict, List

from .openclaw_adapter import openclaw_run


@dataclass
class Job:
    id: str
    args: str
    status: str  # "success" | "error"
    started_at: float
    finished_at: float
    exit_code: int
    stdout: str
    stderr: str


class JobManager:
    """A tiny in-memory job history store."""

    def __init__(self):
        self._jobs: Dict[str, Job] = {}

    def run_openclaw(self, args: str) -> str:
        job_id = str(uuid.uuid4())
        started_at = time.time()

        exit_code, out, err = openclaw_run(args)

        finished_at = time.time()
        status = "success" if exit_code == 0 else "error"

        self._jobs[job_id] = Job(
            id=job_id,
            args=args,
            status=status,
            started_at=started_at,
            finished_at=finished_at,
            exit_code=exit_code,
            stdout=out,
            stderr=err,
        )

        return job_id

    def list_jobs(self) -> List[dict]:
        items = sorted(self._jobs.values(), key=lambda j: j.started_at, reverse=True)
        return [asdict(j) for j in items]

    def get_job(self, job_id: str) -> dict:
        job = self._jobs.get(job_id)
        if not job:
            return {"error": "not_found", "job_id": job_id}
        return asdict(job)