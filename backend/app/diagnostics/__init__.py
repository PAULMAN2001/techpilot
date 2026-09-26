from __future__ import annotations

from datetime import datetime
from typing import Any


def analyze_diagnostics(system_data: dict[str, Any], storage_data: dict[str, Any], network_data: dict[str, Any]) -> tuple[str, list[dict[str, str]]]:
    findings: list[dict[str, str]] = []

    cpu_percent = float(system_data.get("cpu_percent", 0.0) or 0.0)
    memory_percent = float(system_data.get("memory", {}).get("percent", 0.0) or 0.0)
    disk_percent = float(storage_data.get("percent", 0.0) or 0.0)
    interfaces = network_data.get("interfaces") or []
    local_ip = network_data.get("local_ip")

    if cpu_percent >= 90:
        findings.append({
            "category": "Performance",
            "severity": "HIGH",
            "title": "High CPU usage",
            "description": "CPU utilization is significantly elevated.",
            "evidence": f"CPU usage = {cpu_percent} %",
            "recommendation": "Investigate active processes and workloads.",
            "source": "system_analyzer",
        })
    elif cpu_percent >= 70:
        findings.append({
            "category": "Performance",
            "severity": "MEDIUM",
            "title": "Elevated CPU usage",
            "description": "CPU utilization is above the normal baseline.",
            "evidence": f"CPU usage = {cpu_percent} %",
            "recommendation": "Review running applications and background tasks.",
            "source": "system_analyzer",
        })

    if memory_percent >= 85:
        findings.append({
            "category": "Performance",
            "severity": "HIGH",
            "title": "High memory usage",
            "description": "System memory pressure is elevated.",
            "evidence": f"Memory usage = {memory_percent} %",
            "recommendation": "Identify large-memory applications or memory leaks.",
            "source": "system_analyzer",
        })
    elif memory_percent >= 70:
        findings.append({
            "category": "Performance",
            "severity": "MEDIUM",
            "title": "Elevated memory usage",
            "description": "Memory usage is above the normal baseline.",
            "evidence": f"Memory usage = {memory_percent} %",
            "recommendation": "Check for memory-heavy services or processes.",
            "source": "system_analyzer",
        })

    if disk_percent >= 95:
        findings.append({
            "category": "Storage",
            "severity": "CRITICAL",
            "title": "Critical disk usage",
            "description": "Disk capacity is nearly exhausted.",
            "evidence": f"Disk usage = {disk_percent} %",
            "recommendation": "Free up disk space or expand storage immediately.",
            "source": "storage_analyzer",
        })
    elif disk_percent >= 85:
        findings.append({
            "category": "Storage",
            "severity": "HIGH",
            "title": "Low storage space",
            "description": "The available disk space is low.",
            "evidence": f"Disk usage = {disk_percent} %",
            "recommendation": "Review large files and remove unnecessary data.",
            "source": "storage_analyzer",
        })
    elif disk_percent >= 70:
        findings.append({
            "category": "Storage",
            "severity": "MEDIUM",
            "title": "Storage usage elevated",
            "description": "Disk usage is trending higher than expected.",
            "evidence": f"Disk usage = {disk_percent} %",
            "recommendation": "Monitor available space and clean unnecessary files.",
            "source": "storage_analyzer",
        })

    if not interfaces:
        findings.append({
            "category": "Network",
            "severity": "HIGH",
            "title": "No network interfaces detected",
            "description": "No active network adapters were detected.",
            "evidence": "No network interfaces available",
            "recommendation": "Check hardware and adapter configuration.",
            "source": "network_analyzer",
        })
    elif not local_ip:
        findings.append({
            "category": "Network",
            "severity": "MEDIUM",
            "title": "Local IP address unavailable",
            "description": "The system could not resolve a local IP address.",
            "evidence": "Local IP resolution failed",
            "recommendation": "Inspect network adapter status and connectivity.",
            "source": "network_analyzer",
        })

    if not findings:
        status = "ok"
    elif any(item["severity"] == "CRITICAL" for item in findings):
        status = "critical"
    else:
        status = "warning"

    return status, findings
