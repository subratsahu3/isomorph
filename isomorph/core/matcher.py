"""
ISOMORPH: Cross-Domain Isomorphism Matcher
Identifies structural analogues across disparate disciplines using topological invariance
and bipartite role alignment.
"""

from __future__ import annotations
import uuid
from typing import Dict, List, Tuple, Optional
from .models import (
    ResearchArtifact,
    IsomorphicBridge,
    AbstractVariable,
    DynamicRole,
    InteractionKind,
)
from .graph_topology import InvariantTopology


class IsomorphismMatcher:
    """
    Evaluates pairs of research artifacts, filters for cross-domain divergence,
    aligns dynamic variables, and extracts isomorphic bridges.
    """

    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold

    def match_pair(
        self, paper_a: ResearchArtifact, paper_b: ResearchArtifact
    ) -> Optional[IsomorphicBridge]:
        # Rule 1: Must be from distinct scientific domains
        if paper_a.domain.strip().lower() == paper_b.domain.strip().lower():
            return None

        # Rule 2: Minimum complexity
        if len(paper_a.variables) < 2 or len(paper_b.variables) < 2:
            return None

        # Compute invariant signatures
        sig_a = InvariantTopology.extract_topological_signature(paper_a)
        sig_b = InvariantTopology.extract_topological_signature(paper_b)

        sim = InvariantTopology.cosine_similarity(sig_a, sig_b)

        if sim < self.similarity_threshold:
            return None

        # Align nodes by dynamic role and degree
        node_mapping = self._align_variables(paper_a, paper_b)
        mech_mapping = self._align_mechanisms(paper_a, paper_b, node_mapping)

        bridge_id = f"ISO-{uuid.uuid4().hex[:8].upper()}"

        return IsomorphicBridge(
            bridge_id=bridge_id,
            source_paper=paper_a,
            target_paper=paper_b,
            topological_similarity=round(sim, 4),
            mapped_nodes=node_mapping,
            mapped_mechanisms=mech_mapping,
            shared_spectral_invariants=[round(x, 3) for x in sig_a[:6]],
            synthesized_hypothesis="",
            falsification_protocol="",
            mathematical_bridge_equation="",
        )

    def _align_variables(
        self, g1: ResearchArtifact, g2: ResearchArtifact
    ) -> Dict[str, str]:
        """
        Greedy bipartite matching based on role equivalence and degree proximity.
        """
        mapping: Dict[str, str] = {}
        assigned_g2 = set()

        # Group g2 nodes by role
        g2_by_role: Dict[DynamicRole, List[str]] = {}
        for name, var in g2.variables.items():
            g2_by_role.setdefault(var.role, []).append(name)

        # Match exact roles first
        for name1, var1 in g1.variables.items():
            candidates = [c for c in g2_by_role.get(var1.role, []) if c not in assigned_g2]
            if candidates:
                # Pick first available matching role
                best = candidates[0]
                mapping[name1] = best
                assigned_g2.add(best)

        # For remaining unmapped, map to available unassigned nodes
        remaining_g1 = [n for n in g1.variables if n not in mapping]
        remaining_g2 = [n for n in g2.variables if n not in assigned_g2]

        for n1, n2 in zip(remaining_g1, remaining_g2):
            mapping[n1] = n2
            assigned_g2.add(n2)

        return mapping

    def _align_mechanisms(
        self,
        g1: ResearchArtifact,
        g2: ResearchArtifact,
        node_mapping: Dict[str, str],
    ) -> List[Tuple[str, str]]:
        """
        Maps governing equations between source and target based on aligned nodes.
        """
        aligned_mechs: List[Tuple[str, str]] = []
        for m1 in g1.mechanisms:
            mapped_src = node_mapping.get(m1.source)
            mapped_tgt = node_mapping.get(m1.target)
            if not mapped_src or not mapped_tgt:
                continue

            # Look for corresponding edge in g2
            for m2 in g2.mechanisms:
                if m2.source == mapped_src and m2.target == mapped_tgt:
                    aligned_mechs.append(
                        (f"{m1.source}->{m1.target}: {m1.governing_equation}",
                         f"{m2.source}->{m2.target}: {m2.governing_equation}")
                    )
                    break
        return aligned_mechs
