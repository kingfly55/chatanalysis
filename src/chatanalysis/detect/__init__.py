"""Pattern detector framework and required category-specific analyzers."""

from chatanalysis.detect.agent_failures import AgentFailuresDetector
from chatanalysis.detect.base import BaseDetector, DetectorRun, EvidenceReference, Finding, FindingCandidate
from chatanalysis.detect.change_requests import ChangeRequestsDetector
from chatanalysis.detect.corrections_frustrations import CorrectionsFrustrationsDetector
from chatanalysis.detect.output_quality import OutputQualityDetector
from chatanalysis.detect.refinement_requests import RefinementRequestsDetector
from chatanalysis.detect.repeated_instructions import RepeatedInstructionsDetector
from chatanalysis.detect.workflow_patterns import WorkflowPatternsDetector

DETECTOR_REGISTRY = {
    "repeated_instructions": RepeatedInstructionsDetector(),
    "workflow_patterns": WorkflowPatternsDetector(),
    "corrections_frustrations": CorrectionsFrustrationsDetector(),
    "refinement_requests": RefinementRequestsDetector(),
    "agent_failures": AgentFailuresDetector(),
    "output_quality": OutputQualityDetector(),
    "change_requests": ChangeRequestsDetector(),
}


def get_detector(name: str) -> BaseDetector:
    try:
        return DETECTOR_REGISTRY[name]
    except KeyError as exc:
        raise ValueError(f"unknown detector: {name}") from exc


__all__ = [
    "AgentFailuresDetector",
    "BaseDetector",
    "ChangeRequestsDetector",
    "CorrectionsFrustrationsDetector",
    "DETECTOR_REGISTRY",
    "DetectorRun",
    "EvidenceReference",
    "Finding",
    "FindingCandidate",
    "OutputQualityDetector",
    "RefinementRequestsDetector",
    "RepeatedInstructionsDetector",
    "WorkflowPatternsDetector",
    "get_detector",
]
