"""
Clinical Data Models & Enums for HereditaryCancer Sentinel: Germline Variant & NCCN Genetic Testing Criteria Agent.
Domain: Cancer Genetics
Standard: Illustrative demonstration rules, not clinical criteria
"""
import datetime
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any


class UrgencyLevel(str, Enum):
    ROUTINE = "ROUTINE"
    ADVISORY = "ADVISORY"
    WARNING = "WARNING"
    STAT_CRITICAL = "STAT_CRITICAL"


class ClinicalIntegrityStatus(str, Enum):
    CONCORDANT_NORMAL = "CONCORDANT_NORMAL"
    DISCORDANCE_DETECTED = "DISCORDANCE_DETECTED"
    CRITICAL_ACTION_REQUIRED = "CRITICAL_ACTION_REQUIRED"


@dataclass
class ClinicalCasePayload:
    case_id: str
    patient_synthetic_id: str
    primary_metric: float
    secondary_metric: float
    status_flag: str
    is_stat: bool = False
    clinical_notes: str = ""
    biomarkers: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def __post_init__(self):
        for name in ("case_id", "patient_synthetic_id"):
            val = getattr(self, name)
            if not isinstance(val, str) or not val.strip():
                raise ValueError(f"{name} must be a non-empty string")
            setattr(self, name, val.strip())
        for name in ("primary_metric", "secondary_metric"):
            val = getattr(self, name)
            if isinstance(val, bool) or not isinstance(val, (int, float)) or not math.isfinite(val):
                raise ValueError(f"{name} must be a finite number")
        if not isinstance(self.status_flag, str):
            raise ValueError("status_flag must be a string")
        if not isinstance(self.biomarkers, dict):
            raise ValueError("biomarkers must be a dictionary")


@dataclass
class AgentAlert:
    alert_id: str
    sub_agent: str
    urgency: UrgencyLevel
    title: str
    clinical_finding: str
    actionable_recommendation: str
    guideline_citation: str = "Illustrative demonstration rules (not NCCN criteria)"
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "sub_agent": self.sub_agent,
            "urgency": self.urgency.value,
            "title": self.title,
            "clinical_finding": self.clinical_finding,
            "actionable_recommendation": self.actionable_recommendation,
            "guideline_citation": self.guideline_citation,
            "timestamp": self.timestamp,
        }
