# RMF Control Mapper

A lightweight Python + PowerShell tool that maps NIST SP 800-53 security controls to sample evidence and produces an authorization status report.

Built as a focused demonstration of continuous monitoring concepts used in Assessment & Authorization (A&A / RMF) work.

## What it does

1. Loads a small set of NIST SP 800-53 controls (AC, IA, AU families).
2. Collects sample evidence via a PowerShell script (MFA status + last logon).
3. Maps evidence to controls and labels each one:
   - **Implemented** – evidence present and fresh
   - **Partial** – evidence present but incomplete
   - **Stale** – evidence exists but is older than the freshness threshold
4. Outputs a CSV + Markdown status report.

## Controls covered (sample set)

| Control ID | Title                        | Family |
|------------|------------------------------|--------|
| AC-2       | Account Management           | Access Control |
| AC-3       | Access Enforcement           | Access Control |
| AC-7       | Unsuccessful Logon Attempts  | Access Control |
| IA-2       | Identification and Authentication | Identification and Authentication |
| IA-5       | Authenticator Management     | Identification and Authentication |
| AU-2       | Event Logging                | Audit and Accountability |
| AU-3       | Content of Audit Records     | Audit and Accountability |
| AU-6       | Audit Record Review, Analysis, and Reporting | Audit and Accountability |

## Quick start

### 1. Collect sample evidence (PowerShell)

```powershell
pwsh scripts/collect_evidence.ps1
```

This writes `data/sample_users_mfa.csv` — used as evidence for AC-2 and IA-2.

### 2. Generate the status report

```bash
python scripts/map_controls.py
```

Outputs:
- `output/control_status.csv`
- `output/control_status.md`

### 3. Run tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Project layout

```
rmf-control-mapper/
├── data/
│   ├── controls_sample.json   # NIST control definitions
│   ├── sample_evidence.csv    # Static evidence mapping
│   └── sample_users.csv       # Input for PowerShell collector
├── scripts/
│   ├── collect_evidence.ps1   # PowerShell evidence collector
│   └── map_controls.py        # Python status report generator
├── tests/
│   └── test_mapper.py
├── .github/workflows/ci.yml   # GitHub Actions CI
└── output/                    # Generated reports
```

## Why this exists

Most people who study NIST SP 800-53 stop at reading the catalog.  
This project shows the next step: operationalizing the controls — collecting evidence, tying it to control IDs, and reporting status the way an independent assessor would consume it.

## License

MIT
