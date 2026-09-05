"""
Automated Pytest Test Suite for Hereditary Cancer Syndrome Agent.
Domain: Clinical & Biomedical AI
Standard: CAP / CLSI / ISO Standards
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from agents.base import PHIGuard, AuditLogger, SecurityException, AuditTrail
from agents.models import SystemTaskPayload, UrgencyLevel, SystemIntegrityStatus
from agents.workers import InvariantQCWorker, SafetyEscalationWorker, ProtocolConformanceWorker
from agents.supervisor import SystemSupervisor
from cli import main


def test_phi_guard_enforcement():
    with pytest.raises(SecurityException):
        PHIGuard.assert_no_phi("Patient MRN-994827 blood culture positive for Staphylococcus")

    # Clean text passes
    PHIGuard.assert_no_phi("Analytical assay specimen KEY-001 optimal")


def test_phi_guard_redaction():
    redacted = PHIGuard.redact_phi("Patient John Doe MRN-12345678 test")
    assert "[REDACTED_IDENTIFIER]" in redacted
    assert "John Doe" not in redacted
    assert "MRN" not in redacted or "12345678" not in redacted


def test_specialized_workers():
    # Worker 1: QC Invariant
    p1 = SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=35.0)
    alerts1 = InvariantQCWorker.evaluate(p1)
    assert len(alerts1) == 1
    assert alerts1[0].urgency == UrgencyLevel.ELEVATED

    # Worker 2: Safety
    p2 = SystemTaskPayload(task_id="T2", target_identifier="KEY-02", primary_metric=10.0, is_critical_flag=True)
    alerts2 = SafetyEscalationWorker.evaluate(p2)
    assert len(alerts2) == 1
    assert alerts2[0].urgency == UrgencyLevel.CRITICAL_STAT

    # Worker 3: Protocol Conformance
    p3 = SystemTaskPayload(task_id="T3", target_identifier="KEY-03", primary_metric=10.0, status_descriptor="DISCORDANT_ANOMALY")
    alerts3 = ProtocolConformanceWorker.evaluate(p3)
    assert len(alerts3) == 1


def test_supervisor_consensus_and_audit():
    supervisor = SystemSupervisor(model_provider="mock")
    payload = SystemTaskPayload(
        task_id="TASK-PROD-01",
        target_identifier="KEY-PROD-01",
        primary_metric=12.0,
        secondary_metric=4.0,
        status_descriptor="NOMINAL"
    )
    dossier = supervisor.process_task(payload)
    assert dossier.overall_urgency == UrgencyLevel.ROUTINE
    assert dossier.integrity_status == SystemIntegrityStatus.VALIDATED
    assert dossier.audit_hash != ""

    # Verify cryptographic audit trail
    assert AuditLogger.verify_integrity() is True

    # CLI tests
    assert main(["audit", "--task-id", "CLI-TEST-01"]) == 0
    assert main(["chat", "Explain", "specifications"]) == 0
    assert main(["verify-audit"]) == 0


def test_input_validation_rejects_nan():
    """Metric values must be finite (no NaN or Inf)."""
    with pytest.raises(ValueError, match="finite"):
        SystemTaskPayload(task_id="T1", target_identifier="K1", primary_metric=float("nan"))

    with pytest.raises(ValueError, match="finite"):
        SystemTaskPayload(task_id="T1", target_identifier="K1", primary_metric=1.0, secondary_metric=float("inf"))


def test_input_validation_rejects_empty_identifiers():
    """Empty or whitespace-only identifiers must be rejected."""
    with pytest.raises(ValueError, match="non-empty"):
        SystemTaskPayload(task_id="", target_identifier="K1", primary_metric=1.0)

    with pytest.raises(ValueError, match="non-empty"):
        SystemTaskPayload(task_id="T1", target_identifier="   ", primary_metric=1.0)


def test_input_validation_strips_whitespace():
    """Identifier whitespace should be stripped."""
    payload = SystemTaskPayload(task_id="  T1  ", target_identifier="  K1  ", primary_metric=1.0)
    assert payload.task_id == "T1"
    assert payload.target_identifier == "K1"


def test_audit_trail_integrity_verification():
    """Audit trail should detect tampering."""
    trail = AuditTrail(secret_key="test-secret-key")
    trail.log("test_actor", "test_tier", "TEST_EVENT", {"data": "value1"})
    trail.log("test_actor", "test_tier", "TEST_EVENT", {"data": "value2"})
    assert trail.verify_integrity() is True

    # Tamper with a log entry
    if trail.logs:
        trail.logs[0]["payload_hash"] = "tampered_hash"
    assert trail.verify_integrity() is False


def test_audit_trail_with_env_key():
    """AuditTrail should work with explicit key."""
    trail = AuditTrail(secret_key="my-test-key-12345")
    entry = trail.log("actor", "tier", "EVENT", {"key": "value"})
    assert entry["current_hash"] != ""
    assert entry["prev_hash"] == "GENESIS_BLOCK_0000000000000000"


def test_batch_processing_handles_errors_gracefully():
    """Batch processing should handle malformed rows gracefully."""
    import tempfile
    import os

    # Create a temporary CSV with some invalid rows
    csv_content = "task_id,target_identifier,primary_metric,secondary_metric\nT1,K1,abc,5.0\nT2,K2,10.0,5.0\n"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        temp_path = f.name

    try:
        output_path = temp_path + ".out.csv"
        result = main(["batch", "-i", temp_path, "-o", output_path])
        assert result == 0

        # Verify output was created with valid rows
        import csv
        with open(output_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 1  # Only the valid row
            assert rows[0]["task_id"] == "T2"

        os.unlink(output_path)
    finally:
        os.unlink(temp_path)
