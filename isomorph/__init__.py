"""
ISOMORPH: Cross-Disciplinary Structural Isomorphism & Dialectic Discovery Engine
"""

from .core.models import (
    ResearchArtifact,
    AbstractVariable,
    DynamicRole,
    InteractionKind,
    SystemRegime,
    IsomorphicBridge,
    DialecticCollision,
)
from .core.engine import IsomorphEngine
from .corpus.benchmark_papers import load_benchmark_corpus

__version__ = "1.0.0"

__all__ = [
    "ResearchArtifact",
    "AbstractVariable",
    "DynamicRole",
    "InteractionKind",
    "SystemRegime",
    "IsomorphicBridge",
    "DialecticCollision",
    "IsomorphEngine",
    "load_benchmark_corpus",
]
