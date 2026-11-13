"""
ISOMORPH Engine: Central Scientific Discovery Orchestrator
Coordinates paper ingestion, topological analysis, cross-domain matching,
conflict detection, and automated research dossier generation.
"""

from __future__ import annotations
import json
from typing import List, Dict, Optional, Any
from .models import (
    ResearchArtifact,
    IsomorphicBridge,
    DialecticCollision,
)
from .matcher import IsomorphismMatcher
from .synthesizer import HypothesisSynthesizer
from .conflict_detector import DialecticConflictDetector


class IsomorphEngine:
    """
    Main engine interface for researchers.
    """

    def __init__(self, similarity_threshold: float = 0.85):
        self.papers: Dict[str, ResearchArtifact] = {}
        self.matcher = IsomorphismMatcher(similarity_threshold=similarity_threshold)
        self.discovered_bridges: List[IsomorphicBridge] = []
        self.detected_collisions: List[DialecticCollision] = []

    def register_paper(self, paper: ResearchArtifact) -> None:
        self.papers[paper.paper_id] = paper

    def register_papers(self, papers: List[ResearchArtifact]) -> None:
        for p in papers:
            self.register_paper(p)

    def run_scan(self) -> Dict[str, Any]:
        """
        Executes an exhaustive cross-domain topological scan across all registered papers.
        """
        self.discovered_bridges.clear()
        self.detected_collisions.clear()

        paper_list = list(self.papers.values())
        n = len(paper_list)

        for i in range(n):
            for j in range(i + 1, n):
                p1, p2 = paper_list[i], paper_list[j]

                # Match for structural isomorphism
                bridge = self.matcher.match_pair(p1, p2)
                if bridge:
                    synthesized = HypothesisSynthesizer.synthesize_bridge_hypothesis(bridge)
                    self.discovered_bridges.append(synthesized)

                # Check for dialectic conflicts
                collisions = DialecticConflictDetector.detect_collisions(p1, p2)
                self.detected_collisions.extend(collisions)

        # Sort bridges by similarity descending
        self.discovered_bridges.sort(key=lambda b: b.topological_similarity, reverse=True)

        return {
            "papers_indexed": len(self.papers),
            "domains_analyzed": len(set(p.domain for p in self.papers.values())),
            "bridges_discovered": len(self.discovered_bridges),
            "collisions_detected": len(self.detected_collisions),
        }

    def generate_markdown_dossier(self) -> str:
        """
        Compiles discovered breakthroughs into a publication-ready scientific dossier.
        """
        lines = [
            "# ISOMORPH: Cross-Disciplinary Epistemic Discovery Dossier",
            f"**Indexed Papers**: {len(self.papers)} | **Discovered Bridges**: {len(self.discovered_bridges)} | **Axiomatic Collisions**: {len(self.detected_collisions)}",
            "\n---\n",
            "## 1. Discovered Cross-Disciplinary Isomorphic Bridges\n",
        ]

        if not self.discovered_bridges:
            lines.append("_No cross-domain bridges discovered above the current similarity threshold._\n")
        else:
            for b in self.discovered_bridges:
                lines.extend([
                    f"### 🌉 Bridge [{b.bridge_id}]: {b.source_paper.domain} ⟷ {b.target_paper.domain}",
                    f"- **Topological Confidence**: `{b.topological_similarity * 100:.1f}%`",
                    f"- **Source Paper**: *{b.source_paper.title}* (`{b.source_paper.paper_id}`)",
                    f"- **Target Paper**: *{b.target_paper.title}* (`{b.target_paper.paper_id}`)",
                    "",
                    "#### Variable Topological Alignment:",
                ])
                for src_v, tgt_v in b.mapped_nodes.items():
                    lines.append(f"  * `{src_v}` ({b.source_paper.domain}) ⟷ `{tgt_v}` ({b.target_paper.domain})")

                lines.extend([
                    "",
                    f"#### Synthesized Hypothesis:",
                    f"> {b.synthesized_hypothesis}",
                    "",
                    f"#### Governing Bridge Equation:",
                    f"```math\n{b.mathematical_bridge_equation}\n```",
                    "",
                    f"#### Popperian Falsification Protocol:",
                    f"```\n{b.falsification_protocol}\n```",
                    "\n---\n",
                ])

        lines.extend([
            "## 2. Detected Axiomatic Collisions (Silent Contradictions)\n",
        ])

        if not self.detected_collisions:
            lines.append("_No contradictory foundational axioms detected across domains._\n")
        else:
            for c in self.detected_collisions:
                lines.extend([
                    f"### 💥 Collision [{c.collision_id}]: {c.conflicting_premise}",
                    f"- **Paper A**: `{c.paper_a.paper_id}` ({c.paper_a.domain})",
                    f"- **Paper B**: `{c.paper_b.paper_id}` ({c.paper_b.domain})",
                    f"- **Mathematical Contradiction**: {c.mathematical_contradiction}",
                    f"- **Epistemic Implication**: {c.epistemic_implication}",
                    "",
                ])

        return "\n".join(lines)

    def to_json(self) -> str:
        return json.dumps(
            {
                "papers": [p.to_dict() for p in self.papers.values()],
                "bridges": [b.to_dict() for b in self.discovered_bridges],
                "collisions": [c.to_dict() for c in self.detected_collisions],
            },
            indent=2,
        )
