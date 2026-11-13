"""
ISOMORPH: Core Data Models
Mathematical representations of causal hypergraphs, topological invariant signatures,
cross-domain isomorphisms, and dialectic contradictions.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Any


class DynamicRole(str, Enum):
    SOURCE = "source_pool"
    SINK = "dissipation_sink"
    REGULATOR = "feedback_regulator"
    BOTTLENECK = "rate_limiting_gate"
    CATALYST = "activation_catalyst"
    ACCUMULATOR = "state_accumulator"


class InteractionKind(str, Enum):
    POSITIVE_FEEDBACK = "positive_reinforcement"
    NEGATIVE_FEEDBACK = "homeostatic_damping"
    THRESHOLD_SWITCH = "non_linear_bifurcation"
    DIFFUSION = "flux_dissipation"
    SATURATION_INHIBITION = "michaelis_menten_saturation"


class SystemRegime(str, Enum):
    EQUILIBRIUM = "thermodynamic_equilibrium"
    FAR_FROM_EQUILIBRIUM = "dissipative_non_equilibrium"
    CHAOTIC_TRANSITION = "edge_of_chaos_bifurcation"
    STEADY_STATE = "quasi_static_steady_state"


@dataclass(frozen=True)
class AbstractVariable:
    name: str
    role: DynamicRole
    conserved: bool = False
    scale_order_of_magnitude: float = 1.0  # in log10(SI)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "role": self.role.value,
            "conserved": self.conserved,
            "scale": self.scale_order_of_magnitude,
        }


@dataclass(frozen=True)
class CausalEdge:
    source: str
    target: str
    interaction: InteractionKind
    governing_equation: str
    time_constant_tau: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "interaction": self.interaction.value,
            "equation": self.governing_equation,
            "tau": self.time_constant_tau,
        }


@dataclass
class ResearchArtifact:
    paper_id: str
    title: str
    authors: str
    year: int
    domain: str
    empirical_phenomenon: str
    unresolved_bottleneck: str
    regime: SystemRegime = SystemRegime.FAR_FROM_EQUILIBRIUM
    assumed_boundary_conditions: List[str] = field(default_factory=list)
    variables: Dict[str, AbstractVariable] = field(default_factory=dict)
    mechanisms: List[CausalEdge] = field(default_factory=list)

    def add_variable(self, var: AbstractVariable) -> None:
        self.variables[var.name] = var

    def add_mechanism(
        self,
        source: AbstractVariable,
        target: AbstractVariable,
        interaction: InteractionKind,
        equation: str,
        tau: float = 1.0,
    ) -> None:
        self.add_variable(source)
        self.add_variable(target)
        self.mechanisms.append(
            CausalEdge(
                source=source.name,
                target=target.name,
                interaction=interaction,
                governing_equation=equation,
                time_constant_tau=tau,
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "paper_id": self.paper_id,
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "domain": self.domain,
            "phenomenon": self.empirical_phenomenon,
            "unresolved_bottleneck": self.unresolved_bottleneck,
            "regime": self.regime.value,
            "boundary_conditions": self.assumed_boundary_conditions,
            "variables": {k: v.to_dict() for k, v in self.variables.items()},
            "mechanisms": [m.to_dict() for m in self.mechanisms],
        }


@dataclass
class IsomorphicBridge:
    bridge_id: str
    source_paper: ResearchArtifact
    target_paper: ResearchArtifact
    topological_similarity: float
    mapped_nodes: Dict[str, str]
    mapped_mechanisms: List[Tuple[str, str]]
    shared_spectral_invariants: List[float]
    synthesized_hypothesis: str
    falsification_protocol: str
    mathematical_bridge_equation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bridge_id": self.bridge_id,
            "source_paper_id": self.source_paper.paper_id,
            "source_domain": self.source_paper.domain,
            "source_title": self.source_paper.title,
            "target_paper_id": self.target_paper.paper_id,
            "target_domain": self.target_paper.domain,
            "target_title": self.target_paper.title,
            "topological_similarity": self.topological_similarity,
            "mapped_nodes": self.mapped_nodes,
            "mapped_mechanisms": self.mapped_mechanisms,
            "shared_spectral_invariants": self.shared_spectral_invariants,
            "synthesized_hypothesis": self.synthesized_hypothesis,
            "falsification_protocol": self.falsification_protocol,
            "mathematical_bridge_equation": self.mathematical_bridge_equation,
        }


@dataclass
class DialecticCollision:
    collision_id: str
    paper_a: ResearchArtifact
    paper_b: ResearchArtifact
    conflicting_premise: str
    mathematical_contradiction: str
    epistemic_implication: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "collision_id": self.collision_id,
            "paper_a": self.paper_a.paper_id,
            "paper_a_domain": self.paper_a.domain,
            "paper_b": self.paper_b.paper_id,
            "paper_b_domain": self.paper_b.domain,
            "conflicting_premise": self.conflicting_premise,
            "mathematical_contradiction": self.mathematical_contradiction,
            "epistemic_implication": self.epistemic_implication,
        }
