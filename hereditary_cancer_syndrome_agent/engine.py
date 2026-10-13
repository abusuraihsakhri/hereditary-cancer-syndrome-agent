"""
Illustrative numerical rules only; not validated hereditary cancer criteria.
Domain: Cancer Genetics
Standard: Synthetic demonstration thresholds; not NCCN clinical criteria
"""
import math
from typing import Dict, Any, List, Optional
from .models import ClinicalCasePayload, AgentAlert, UrgencyLevel, ClinicalIntegrityStatus


class ClinicalDomainEngine:
    GUIDELINE = "Demonstration thresholds (not NCCN criteria)"
    PRIMARY_BASELINE_LIMIT = 20.0
    SECONDARY_ALERT_LIMIT = 10.0

    @classmethod
    def evaluate_primary_index(cls, value: float) -> Optional[Dict[str, Any]]:
        if value > cls.PRIMARY_BASELINE_LIMIT:
            return {
                "title": "Primary Metric Threshold Exceeded",
                "finding": f"Observed value ({value:.2f}) exceeds the illustrative primary threshold ({cls.PRIMARY_BASELINE_LIMIT:.1f}).",
                "recommendation": "Review the synthetic input and the demonstration threshold.",
            }
        return None

    @classmethod
    def evaluate_secondary_kinetics(cls, value: float, is_stat: bool) -> Optional[Dict[str, Any]]:
        if value > cls.SECONDARY_ALERT_LIMIT or is_stat:
            return {
                "title": "Demonstration Secondary Flag Triggered",
                "finding": f"Kinetic parameter ({value:.2f}) with STAT={is_stat} matched a demonstration rule.",
                "recommendation": "Review the demonstration input; no clinical action is prescribed.",
            }
        return None

    @classmethod
    def evaluate_biomarker_concordance(cls, status_flag: str, biomarkers: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        status_upper = str(status_flag).upper()
        if "DISCORDANT" in status_upper or "EQUIVOCAL" in status_upper:
            return {
                "title": "Phenotypic / Biomarker Discordance Identified",
                "finding": f"Status flag '{status_flag}' contains a demonstration review keyword.",
                "recommendation": f"Review the status description; this rule does not determine confirmatory testing.",
            }
        return None
