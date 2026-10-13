# Hereditary Cancer Syndrome Agent

A Python rule-engine demonstration with a static browser interface. Despite the repository name, **the current implementation is not a validated hereditary cancer syndrome classifier or clinical decision-support system**. It does **not** parse three-generation pedigrees, classify germline variants, or implement NCCN genetic testing criteria.

## Features

- Deterministic synthetic-input rules checking illustrative numeric thresholds and text descriptors.
- Legacy `agents/` implementation using Pydantic 2, a command-line interface, batch CSV processing, and an optional FastAPI server.
- Separate `hereditary_cancer_syndrome_agent/` data-class implementation and CLI (different numerical thresholds).
- Local in-browser rule sandbox under `web/` with JSON export. It does not call the API or require Python/Pyodide.
- Best-effort identifier-pattern checks and an **in-memory**, HMAC-chained server audit log. These do not establish HIPAA compliance, anonymity, or durable audit storage.

**Clinical limitation:** Thresholds in the Python and browser examples are arbitrary demonstration rules, not hereditary cancer risk scores, diagnostic reference intervals, or testing criteria. A normal result does not exclude hereditary cancer susceptibility. Use synthetic or otherwise non-identifiable test records only.

## Browser interface

Open `web/index.html` in a current desktop or mobile browser, or use the GitHub Pages deployment when available. Enter synthetic IDs, numeric test values, a descriptor, and an optional demonstration priority flag. Select **Evaluate locally**, review the matched rules, and optionally export a JSON result.

The browser performs its comparisons entirely on-device. It does not save inputs, perform server requests for evaluation, or generate cryptographic audit signatures. Its rules correspond to the illustrative `agents/workers.py` comparisons.

## Local Python usage

Requires Python 3.10+ for the optional FastAPI server and the supported CI matrix (project packaging supports Python 3.9+).

```bash
python -m pip install -e ".[server,dev]"
python -m pytest -q

# Pydantic-based legacy implementation
python cli.py audit --task-id DEMO-001 --target SYNTH-001 --primary 28.5 --secondary 14.2
python cli.py batch -i sample.csv -o results.csv
python cli.py verify-audit
python cli.py serve --host 127.0.0.1 --port 8000

# Separate data-class implementation
python -m hereditary_cancer_syndrome_agent.cli audit --case-id CASE-001 --primary 21 --secondary 11
```

The package-installed command `hereditary-cancer-syndrome-engine` invokes the second, data-class CLI. The root-level `cli.py` invokes the Pydantic-based legacy API. These entry points are deliberately preserved for compatibility; they are not interchangeable clinical engines.

For local API development, visit `http://127.0.0.1:8000/docs`. The `POST /api/audit` endpoint has no authentication and must not be internet-exposed or used with patient information. `GET /api/audit/logs` is disabled unless `AUDIT_API_TOKEN` is configured, and requires the `X-Audit-Token` header. `/metrics` currently returns JSON counters, not Prometheus text.

## Configuration and privacy

Set `AUDIT_SECRET_KEY` to a privately managed, long random value for server deployments; without it, the server creates an ephemeral key and audit signatures cannot be verified after restart. The audit chain also remains in memory only. Configure `AUDIT_API_TOKEN` separately if access to audit logs is required. Neither variable belongs in tracked source files or browser scripts. The `docker-compose.yml` service requires `AUDIT_SECRET_KEY` and binds to `127.0.0.1:8000` by default.

The identifier-pattern guard is incomplete by design. Avoid all real patient data, MRNs, clinical notes, and other sensitive information. There is no formal regulatory validation, authorization model for evaluations, persistent secure database, or guaranteed de-identification.

## Verification and deployment

```bash
python -m pytest -q
python -m compileall -q agents hereditary_cancer_syndrome_agent
node --check web/app.js
node web/test_app.cjs
docker build -t hereditary-cancer-demo .
```

GitHub Actions runs the Python test matrix, browser JavaScript checks, package build, and container build. The workflow is configured to deploy `web/` to GitHub Pages after successful checks on `master`, provided Pages is configured to use GitHub Actions in repository settings. GitHub Pages hosts only the static browser sandbox; it cannot host the FastAPI service.

## Stack and license

Python, Pydantic 2, optional FastAPI/Uvicorn, standard HTML/CSS/JavaScript, and GitHub Actions. The browser sandbox targets modern Chrome, Firefox, Safari, and Edge; no compatibility certification or clinical validation has been performed.

[MIT License](LICENSE).
