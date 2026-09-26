# TechPilot Phase 2 — Diagnostic Engine & Findings System

## Objective

Build a unified diagnostic and findings system that collects raw data, analyzes it against deterministic rules, produces structured findings, and stores diagnostic history.

**Phase 1:** "Here is what your computer reports."

**Phase 2:** "Here is what TechPilot thinks is worth paying attention to."

---

## 1. Unified Diagnostic Schema

Replace individual endpoints with a comprehensive diagnostic result structure.

### DiagnosticResult

```python
class DiagnosticResult:
    id: str                      # UUID
    timestamp: datetime          # When run
    hostname: str               # Computer name
    system: SystemInfo          # CPU, RAM, OS
    storage: StorageInfo        # Disk usage
    network: NetworkInfo        # Connectivity
    findings: List[Finding]    # Analysis results
    status: str                # "ok", "warning", "critical"
```

### Finding

```python
class Finding:
    id: str                     # UUID
    category: str               # Performance, Storage, Network, System, Security, Applications
    severity: str               # INFO, LOW, MEDIUM, HIGH, CRITICAL
    title: str                  # "High CPU usage"
    description: str            # Explanation
    evidence: str               # "CPU usage = 84.6%"
    recommendation: str         # What to do
    source: str                 # Which diagnostic module
```

### Example

Instead of just:
```json
{"cpu_percent": 84.6}
```

Phase 2 produces:
```json
{
  "category": "Performance",
  "severity": "MEDIUM",
  "title": "High CPU usage",
  "description": "CPU utilization is currently elevated.",
  "evidence": "CPU usage = 84.6%",
  "recommendation": "Investigate processes using CPU resources.",
  "source": "system_diagnostics"
}
```

---

## 2. Severity Levels

| Level | Meaning |
|-------|----------|
| `INFO` | Normal/interesting information |
| `LOW` | Minor issue |
| `MEDIUM` | Needs attention |
| `HIGH` | Significant issue |
| `CRITICAL` | Immediate attention required |

**Important:** Severity is based on transparent, deterministic rules, not AI opinion.

### Example Rules (can be tuned later)

```
CPU Usage
  < 70%    → INFO
  70-90%   → MEDIUM
  > 90%    → HIGH

Memory Usage
  < 70%    → INFO
  70-85%   → MEDIUM
  > 85%    → HIGH

Disk Usage
  < 70%    → INFO
  70-85%   → MEDIUM
  85-95%   → HIGH
  > 95%    → CRITICAL
```

---

## 3. Diagnostic Categories

```
Performance   - CPU, memory, process usage
Storage       - Disk space, usage trends
Network       - Connectivity, interfaces, configuration
System        - OS version, uptime, drivers
Security      - (Phase 12) Vulnerabilities, outdated software
Applications  - (Phase 8) App-specific diagnostics
```

Phase 2 focuses on: **Performance, Storage, Network, System**

---

## 4. Rule-Based Diagnostic Engine

Create a deterministic analyzer that does NOT use AI.

```
Raw Data (psutil, socket, platform)
    ↓
Diagnostic Rules (thresholds, patterns)
    ↓
Findings (structured results)
    ↓
Database (history storage)
    ↓
API Response (to frontend)
```

### Implementation Pattern

```python
def analyze_performance(system_data) -> List[Finding]:
    findings = []

    if system_data.cpu_percent > 90:
        findings.append(Finding(
            category="Performance",
            severity="HIGH",
            title="High CPU usage",
            description="CPU utilization is significantly elevated.",
            evidence=f"CPU usage = {system_data.cpu_percent}%",
            recommendation="Investigate running processes.",
            source="performance_analyzer"
        ))

    if system_data.memory_percent > 85:
        findings.append(Finding(
            category="Performance",
            severity="HIGH",
            title="High memory usage",
            description="Memory pressure is elevated.",
            evidence=f"Memory usage = {system_data.memory_percent}%",
            recommendation="Investigate applications using memory.",
            source="performance_analyzer"
        ))

    return findings
```

---

## 5. Enhanced Storage Diagnostics

Phase 2 should identify:

```
Total storage
Used storage
Free storage
Usage percentage
Drive letter/mount point
Filesystem type
```

Then generate findings:

```
Used < 70%        → INFO
Used 70-85%       → MEDIUM ("Storage usage is elevated")
Used 85-95%       → HIGH ("Low storage space")
Used > 95%        → CRITICAL ("Critical storage shortage")
```

---

## 6. Enhanced Network Diagnostics

Phase 2 should identify:

```
Hostname
Local IP address
Active network interfaces
Interface status (up/down)
Gateway
DNS servers
Internet connectivity (if safely testable)
```

Findings:

```
No active network interface   → HIGH ("No network connectivity")
Multiple interfaces available → INFO ("Multiple network adapters detected")
```

---

## 7. Diagnostic History

This is critical for trend detection and the foundation of Technical Memory.

### Database Schema

```sql
CREATE TABLE diagnostic_runs (
    id TEXT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    hostname TEXT NOT NULL,
    status TEXT,
    finding_count INTEGER
);

CREATE TABLE findings (
    id TEXT PRIMARY KEY,
    diagnostic_run_id TEXT NOT NULL,
    category TEXT,
    severity TEXT,
    title TEXT,
    description TEXT,
    evidence TEXT,
    recommendation TEXT,
    source TEXT,
    FOREIGN KEY (diagnostic_run_id) REFERENCES diagnostic_runs(id)
);
```

### Usage

When viewing diagnostics, TechPilot can compare:

```
Sep 26 21:07  CPU: 84%, Memory: 77%, Disk: 82%
Sep 26 20:41  CPU: 45%, Memory: 61%, Disk: 83%

↓

CPU usage increased significantly (45% → 84%)
```

---

## 8. API Endpoints (Phase 2)

### Run Diagnostic

```
POST /api/diagnostics/run
```

Response:
```json
{
  "id": "uuid-123",
  "timestamp": "2026-09-26T21:07:00Z",
  "hostname": "DESKTOP-ABC",
  "status": "warning",
  "findings": [
    {
      "category": "Performance",
      "severity": "MEDIUM",
      "title": "High CPU usage",
      "evidence": "CPU = 84.6%",
      "recommendation": "..."
    }
  ]
}
```

### Get Latest Diagnostic

```
GET /api/diagnostics/latest
```

### Get Diagnostic History

```
GET /api/diagnostics/history?limit=10
```

Response:
```json
[
  {"timestamp": "2026-09-26T21:07:00Z", "findings_count": 3, "status": "warning"},
  {"timestamp": "2026-09-26T20:41:00Z", "findings_count": 1, "status": "ok"},
  ...
]
```

### Get Specific Diagnostic

```
GET /api/diagnostics/{id}
```

---

## 9. Dashboard Enhancements

Replace raw numbers with intelligent findings display.

### New Layout

```
┌─────────────────────────────────────────┐
│          TECHPILOT DIAGNOSTICS          │
├─────────────────────────────────────────┤
│                                         │
│  System Health                          │
│  ────────────────────────────────────   │
│  🟢 System         ✓ OK                  │
│  🟡 Performance    ⚠ 1 finding          │
│  🟢 Network        ✓ OK                  │
│  🟡 Storage        ⚠ 2 findings         │
│                                         │
│  [Run Full Diagnostic]                  │
│                                         │
├─────────────────────────────────────────┤
│  Findings (3)                           │
│  ────────────────────────────────────   │
│                                         │
│  🟡 MEDIUM                              │
│  High CPU usage                         │
│  CPU = 84.6%                            │
│  Recommendation: Investigate processes  │
│  [View Details]                         │
│                                         │
│  🟡 HIGH                                │
│  Low disk space                         │
│  Storage used = 92%                     │
│  Recommendation: Free up disk space     │
│  [View Details]                         │
│                                         │
├─────────────────────────────────────────┤
│  Recent Diagnostics                     │
│  ────────────────────────────────────   │
│  Today 21:07      3 findings            │
│  Today 20:41      1 finding             │
│  Yesterday 18:30  0 findings            │
│                                         │
└─────────────────────────────────────────┘
```

---

## 10. "Run Full Diagnostic" Workflow

When user clicks the button:

```
1. Create diagnostic_run record
2. Collect system data
3. Analyze performance → findings
4. Analyze storage → findings
5. Analyze network → findings
6. Analyze system info → findings
7. Calculate overall status
8. Store findings to database
9. Return results to frontend
10. Display results
```

All of this is read-only. No modifications.

---

## 11. Testing (Phase 2)

Tests should verify:

```python
# Severity rules
test_cpu_50_percent_is_info()
test_cpu_80_percent_is_medium()
test_cpu_95_percent_is_high()

# Storage rules
test_disk_50_percent_is_info()
test_disk_90_percent_is_medium()
test_disk_97_percent_is_critical()

# Finding creation
test_finding_has_required_fields()
test_finding_has_valid_severity()
test_finding_has_valid_category()

# Database
test_diagnostic_run_stored()
test_findings_associated_with_run()
test_history_retrieval()

# API
test_post_diagnostics_run()
test_get_latest_diagnostic()
test_get_diagnostic_history()

# Integration
test_full_diagnostic_workflow()
```

---

## 12. Security & Read-Only Guarantee

Phase 2 must **NOT** include:

- ❌ File deletion
- ❌ Process termination
- ❌ Windows registry modification
- ❌ Firewall/network changes
- ❌ Automatic fixes
- ❌ Arbitrary command execution
- ❌ Software installation

Phase 2 is purely:
- ✅ Observation
- ✅ Analysis
- ✅ Reporting

---

## 13. Documentation (Phase 2)

Update:

```
README.md              - Phase 2 capabilities
docs/architecture.md   - Diagnostic engine design
docs/api.md            - API endpoint documentation
docs/security.md       - Security model (read-only emphasis)
docs/roadmap.md        - Phase 2 → Phase 3 progression
```

---

## Phase 2 Success Criteria

✅ User opens TechPilot  
✅ Clicks "Run Full Diagnostic"  
✅ Backend collects system data  
✅ Diagnostic rules generate findings  
✅ Results stored to SQLite  
✅ Dashboard displays findings with severity and recommendations  
✅ History view shows previous diagnostics  
✅ All tests pass  
✅ Zero system modifications  
✅ Frontend + backend integration working  

### Example Output

```
╔════════════════════════════════════════╗
║     TechPilot Diagnostics Result       ║
║                                        ║
║  Status: ⚠ WARNING                    ║
║  Findings: 3                           ║
║  Timestamp: 2026-09-26 21:07:00       ║
╟────────────────────────────────────────╢
║  1. High CPU usage (MEDIUM)           ║
║     CPU: 84.6% (threshold: 90%)       ║
║     Action: Investigate processes     ║
║                                        ║
║  2. Low disk space (HIGH)             ║
║     Storage: 92% used                 ║
║     Free: 8 GB of 100 GB              ║
║     Action: Free up storage           ║
║                                        ║
║  3. Network available (INFO)          ║
║     Status: Connected                 ║
║                                        ║
╚════════════════════════════════════════╝
```

---

## Why Phase 2 Before AI?

Phase 3 will add the AI Troubleshooter:

```
Phase 2 (Diagnostic Engine)
         ↓
  Reliable, structured findings
         ↓
Phase 3 (AI Troubleshooter)
         ↓
  "Why is this happening?"
  "What evidence supports this?"
  "What are safe solutions?"
```

Without Phase 2, AI would be reasoning about raw sensor data. With Phase 2, AI reasons about TechPilot's analysis—which is more reliable, explainable, and testable.

---

## Implementation Order

1. Define Pydantic schemas (DiagnosticResult, Finding)
2. Expand SQLite: diagnostic_runs, findings tables
3. Create diagnostic rules/analyzers (deterministic)
4. Implement API endpoints (POST /diagnostics/run, GET /history, etc.)
5. Add database persistence
6. Update frontend dashboard
7. Write comprehensive tests
8. Update documentation
9. Verify end-to-end workflow
10. Commit to main

---

## Next Step

Once Phase 2 is committed and verified working:

→ **Phase 3: AI Troubleshooter** (reasoning over Phase 2 findings)

→ **Phase 4: Error Analysis** (user submits errors, AI diagnoses)

→ **Phase 5: Permission Engine** (before any system modifications)

→ **Phase 6+: Action Execution, Developer Tools, Automation**
