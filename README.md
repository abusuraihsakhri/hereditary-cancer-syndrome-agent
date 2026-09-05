# Hereditary Cancer Syndrome Agent

> **Domain:** Clinical Decision Support & Biomedical Computing  
> **Reference Guidelines & Standards:** `Standard Clinical Formulations & ISO/IEC Quality Frameworks`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Hereditary Cancer Syndrome Agent** is an advanced analytical and computational platform implementing NCCN 3-Generation Pedigree Genetic Testing Criteria Agent. It audits patient personal and 3-generation family cancer histories against NCCN criteria for BRCA1/2, Lynch syndrome (MLH1/MSH2/MSH6), and TP53.

---

## ⚙️ Key Capabilities & Algorithmic Modules

### 🔬 Core Algorithmic & Evaluation Engines

- **`DomainKnowledgeRegistry`**: Enterprise domain rules, guideline matrices, and evidence benchmarks.
- **`PedigreeCriteriaEvaluatorAgent`**: Specialized Sub-Agent 1 for hereditary-cancer-syndrome-agent
- **`VariantPathogenicityAgent`**: Specialized Sub-Agent 2 for hereditary-cancer-syndrome-agent
- **`SurveillanceProtocolAdvisorAgent`**: Specialized Sub-Agent 3 for hereditary-cancer-syndrome-agent

### Specialized Workers

- **`InvariantQCWorker`**: Primary Mathematical & Protocol Boundary Auditor
- **`SafetyEscalationWorker`**: Safety Boundary, Toxicity & Emergency Interlock Worker
- **`ProtocolConformanceWorker`**: Spec Conformance, Anomaly Triage & Discordance Checker

---

## 💻 CLI Quickstart & Usage

### Installation

```bash
pip install -r requirements.txt
# Or install with development dependencies:
pip install -e ".[dev]"
```

### 1. Run a Single Audit
```bash
python cli.py audit --task-id TASK-001 --primary 28.5 --secondary 14.2
```

### 2. Batch Process CSV Records
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 3. Interactive Chat
```bash
python cli.py chat "What is the system status?"
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch REST API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
- `--task-id`: Unique task / case identifier
- `--target`: Entity, patient key, or genomic/cryptographic target
- `--primary`: Primary domain measurement or score (float)
- `--secondary`: Secondary kinetic or confidence score (float)
- `--critical`: Trigger emergency escalation flag
- `--status`: Status code or phenotype descriptor
- `--input`: Input CSV file path for batch processing
- `--output`: Output CSV file path for batch processing

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Secure Key Management:** HMAC secret key loaded from `AUDIT_SECRET_KEY` environment variable with secure random fallback.
* **Input Validation:** All metric values validated for finite numbers; empty identifiers rejected.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 1000
```

### Running Specific Tests

```bash
pytest tests/test_hereditary_cancer_syndrome_agent.py -v
pytest tests/test_enrichment.py -v
pytest test_hereditary_cancer.py -v
```

---

## 🐳 Container Deployment

```bash
docker build -t hereditary-cancer-syndrome-agent .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=your-secret-key hereditary-cancer-syndrome-agent
```

### Docker Compose

```bash
docker-compose up
```

---

## 📁 Project Structure

```
hereditary-cancer-syndrome-agent/
├── agents/                    # Core agent package
│   ├── __init__.py
│   ├── api.py                 # FastAPI REST endpoints
│   ├── base.py                # Security, PHI Guard, Audit Trail
│   ├── models.py              # Pydantic schemas
│   ├── supervisor.py          # Supervisor orchestrator
│   ├── workers.py             # Specialized worker agents
│   ├── llm_factory.py         # LLM client factory
│   ├── metrics.py             # Prometheus metrics
│   ├── learning.py            # Bayesian calibration engine
│   └── streamer.py            # WebSocket telemetry
├── hereditary_cancer_syndrome_agent/  # Clinical package
│   ├── agents.py              # Clinical sub-agents
│   ├── cli.py                 # Clinical CLI
│   ├── models.py              # Clinical data models
│   ├── engine.py              # Clinical algorithmic engine
│   └── server.py              # Clinical FastAPI server
├── tests/                     # Test suite
├── cli.py                     # Main CLI entry point
├── hereditary_cancer.py       # Alternative CLI entry
├── enrichment.py              # Enrichment feature modules
├── simulator.py               # High-throughput simulator
├── web/                       # Web console
├── Dockerfile                 # Docker build config
├── docker-compose.yml         # Docker Compose config
└── pyproject.toml             # Project configuration
```

---

## 🔧 Configuration

Set the following environment variables for production deployments:

- `AUDIT_SECRET_KEY`: Secret key for HMAC-SHA256 audit trail (auto-generated if not set)
