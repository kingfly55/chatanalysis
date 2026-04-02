"""Optional semantic analysis extension points."""

from chatanalysis.semantic.base import SemanticEvidenceSlice, SemanticMethod, SemanticRun, write_semantic_run
from chatanalysis.semantic.clustering import DeterministicClusteringMethod
from chatanalysis.semantic.embeddings import FixtureEmbeddingMethod
from chatanalysis.semantic.interpretation import FixtureInterpretationMethod
from chatanalysis.semantic.skill_mining import SkillMiningMethod

SEMANTIC_METHODS = {
    "embeddings": FixtureEmbeddingMethod(),
    "clustering": DeterministicClusteringMethod(),
    "interpretation": FixtureInterpretationMethod(),
    "skill-mining": SkillMiningMethod(),
}


def get_semantic_method(name: str) -> SemanticMethod:
    try:
        return SEMANTIC_METHODS[name]
    except KeyError as exc:
        raise ValueError(f"unknown semantic method: {name}") from exc


__all__ = [
    "DeterministicClusteringMethod",
    "FixtureEmbeddingMethod",
    "FixtureInterpretationMethod",
    "SEMANTIC_METHODS",
    "SemanticEvidenceSlice",
    "SemanticMethod",
    "SemanticRun",
    "SkillMiningMethod",
    "get_semantic_method",
    "write_semantic_run",
]
