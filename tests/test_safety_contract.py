"""Security and non-clinical behavior regression checks."""
import csv
import math

import pytest
from fastapi.testclient import TestClient

from agents.api import app
from agents.llm_factory import LLMFactory
from cli import main
from hereditary_cancer import CancerGeneticsCoordinator, VariantPathogenicityAgent
from hereditary_cancer_syndrome_agent.models import ClinicalCasePayload


def test_alternate_payload_rejects_invalid_metrics_and_ids():
    args = dict(case_id="CASE-1", patient_synthetic_id="SYNTH-1",
                primary_metric=10.0, secondary_metric=5.0, status_flag="NORMAL")
    for field, invalid in [("primary_metric", float("nan")),
                           ("secondary_metric", float("inf")),
                           ("case_id", "  "), ("patient_synthetic_id", "")]:
        with pytest.raises(ValueError):
            ClinicalCasePayload(**{**args, field: invalid})


def test_legacy_advisory_not_reported_as_normal():
    dossier = CancerGeneticsCoordinator().audit_case({
        "case_id": "DEMO-1", "metric_primary": 1, "metric_secondary": 2,
        "status_text": "DISCORDANT"
    })
    assert dossier["total_alerts"] == 1
    assert dossier["overall_status"] == "WARNING_ACTIVE"


def test_legacy_string_false_not_critical():
    worker = VariantPathogenicityAgent()
    assert worker.evaluate({"metric_secondary": 1, "critical_flag": "False"}) == []


def test_unsupported_provider_does_not_silently_use_mock():
    with pytest.raises(ValueError, match="not implemented"):
        LLMFactory.create("openai")


def test_batch_reads_supplied_case_csv_schema(tmp_path):
    source = tmp_path / "batch.csv"
    output = tmp_path / "output.csv"
    with source.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["case_id", "patient_synthetic_id", "metric_primary",
                         "metric_secondary", "is_stat", "status_flag"])
        writer.writerow(["DEMO-1", "SYNTH-1", 30, 14, "False", "DISCORDANT"])
    assert main(["batch", "-i", str(source), "-o", str(output)]) == 0
    with output.open(newline="", encoding="utf-8") as fh:
        row = next(csv.DictReader(fh))
    assert row["overall_urgency"] == "ELEVATED_RISK"
    assert int(row["total_alerts"]) == 3
    assert row["case_id"] == "DEMO-1"


def test_audit_logs_require_explicit_token(monkeypatch):
    client = TestClient(app)
    monkeypatch.delenv("AUDIT_API_TOKEN", raising=False)
    assert client.get("/api/audit/logs").status_code == 403
    monkeypatch.setenv("AUDIT_API_TOKEN", "example-development-secret")
    assert client.get("/api/audit/logs").status_code == 403
    accepted = client.get("/api/audit/logs",
                          headers={"X-Audit-Token": "example-development-secret"})
    assert accepted.status_code == 200
    assert accepted.json()["verified"] is True


def test_api_rejects_detectable_identifier_in_nested_attributes():
    client = TestClient(app)
    response = client.post("/api/audit", json={
        "task_id": "DEMO-2", "target_identifier": "SYNTH-2",
        "primary_metric": 2, "secondary_metric": 3,
        "attributes": {"comment": "MRN-12345678"}
    })
    assert response.status_code == 422
