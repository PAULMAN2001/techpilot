from typing import Any

import platform
import socket

import psutil
from fastapi import APIRouter, Query
from sqlalchemy import desc

from app.database.database import DiagnosticRun, FindingRecord, SessionLocal, serialize_run
from app.diagnostics.analyzer import analyze_diagnostics

router = APIRouter(tags=["diagnostics"])


def system_diagnostics() -> dict[str, Any]:
    memory = psutil.virtual_memory()
    return {
        "operating_system": platform.platform(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor() or platform.uname().processor,
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "cpu_count": psutil.cpu_count(logical=True),
        "memory": {
            "total_bytes": memory.total,
            "available_bytes": memory.available,
            "used_bytes": memory.used,
            "percent": memory.percent,
        },
    }


def storage_diagnostics() -> dict[str, Any]:
    disk = psutil.disk_usage("/")
    return {
        "path": "/",
        "total_bytes": disk.total,
        "used_bytes": disk.used,
        "free_bytes": disk.free,
        "percent": disk.percent,
    }


def network_diagnostics() -> dict[str, Any]:
    interfaces = []
    for name, addresses in psutil.net_if_addrs().items():
        interfaces.append({
            "name": name,
            "addresses": [address.address for address in addresses if address.address],
        })
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except socket.error:
        hostname, local_ip = socket.gethostname(), None
    return {"hostname": hostname, "local_ip": local_ip, "interfaces": interfaces}


@router.get("/system")
def get_system() -> dict[str, Any]:
    return system_diagnostics()


@router.get("/storage")
def get_storage() -> dict[str, Any]:
    return storage_diagnostics()


@router.get("/network")
def get_network() -> dict[str, Any]:
    return network_diagnostics()


@router.post("/diagnostics/run")
def run_full_diagnostics() -> dict[str, Any]:
    system_data = system_diagnostics()
    storage_data = storage_diagnostics()
    network_data = network_diagnostics()
    status, findings = analyze_diagnostics(system_data, storage_data, network_data)

    with SessionLocal.begin() as session:
        run = DiagnosticRun(
            hostname=network_data.get("hostname", "unknown-host"),
            status=status,
            finding_count=len(findings),
        )
        session.add(run)
        session.flush()

        for finding in findings:
            session.add(
                FindingRecord(
                    diagnostic_run_id=run.id,
                    category=finding["category"],
                    severity=finding["severity"],
                    title=finding["title"],
                    description=finding["description"],
                    evidence=finding["evidence"],
                    recommendation=finding["recommendation"],
                    source=finding["source"],
                )
            )
        session.commit()
        
        return {
            "id": run.id,
            "timestamp": run.timestamp.isoformat(),
            "hostname": run.hostname,
            "status": run.status,
            "findings": findings,
        }


@router.get("/diagnostics/latest")
def get_latest_diagnostic() -> dict[str, Any]:
    with SessionLocal() as session:
        run = session.query(DiagnosticRun).order_by(desc(DiagnosticRun.timestamp)).first()
        if run is None:
            return {"status": "ok", "findings": [], "message": "No diagnostics have been recorded yet."}
        return serialize_run(run)


@router.get("/diagnostics/history")
def get_diagnostic_history(limit: int = Query(10, ge=1, le=50)) -> list[dict[str, Any]]:
    with SessionLocal() as session:
        runs = session.query(DiagnosticRun).order_by(desc(DiagnosticRun.timestamp)).limit(limit).all()
        return [serialize_run(run) for run in runs]
