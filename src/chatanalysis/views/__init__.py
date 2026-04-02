"""Corpus views and recurrence-aware analysis substrate."""

from chatanalysis.views.definitions import (
    STANDARD_SUBAGENT_POLICIES,
    STANDARD_VIEW_DEFINITIONS,
    CorpusViewDefinition,
    build_view,
    get_view_definition,
    iter_evidence_records,
    write_view_artifacts,
)
from chatanalysis.views.filters import FilterDecision, ViewFilterPolicy, apply_view_policy
from chatanalysis.views.inspect import build_inspection_record
from chatanalysis.views.recurrence import RECURRENCE_BASIS_DEFAULT, compute_recurrence_counts

__all__ = [
    "CorpusViewDefinition",
    "FilterDecision",
    "RECURRENCE_BASIS_DEFAULT",
    "STANDARD_SUBAGENT_POLICIES",
    "STANDARD_VIEW_DEFINITIONS",
    "ViewFilterPolicy",
    "apply_view_policy",
    "build_inspection_record",
    "build_view",
    "compute_recurrence_counts",
    "get_view_definition",
    "iter_evidence_records",
    "write_view_artifacts",
]
