import platform
import socket

import psutil
from fastapi import APIRouter

router = APIRouter(tags=["diagnostics"])


@router.get("/system")
def system_diagnostics() -> dict:
    memory = psutil.virtual_memory()
    return {
        "operating_system": platform.platform(),
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


@router.get("/storage")
def storage_diagnostics() -> dict:
    disk = psutil.disk_usage("/")
    return {
        "path": "/",
        "total_bytes": disk.total,
        "used_bytes": disk.used,
        "free_bytes": disk.free,
        "percent": disk.percent,
    }


@router.get("/network")
def network_diagnostics() -> dict:
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