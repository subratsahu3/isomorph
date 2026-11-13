"""
ISOMORPH: Unit Test Suite
Verifies topological invariance, Weisfeiler-Lehman hashing, cross-domain matching,
conflict detection, pairwise matching, and dossier synthesis.
"""

import unittest
from isomorph.core.models import (
    ResearchArtifact,
    AbstractVariable,
    DynamicRole,
    InteractionKind,
    SystemRegime,
)
from isomorph.core.graph_topology import InvariantTopology
from isomorph.core.engine import IsomorphEngine
from isomorph.corpus.benchmark_papers import load_benchmark_corpus
from isomorph.core.synthesizer import HypothesisSynthesizer


class TestIsomorphEngine(unittest.TestCase):

    def setUp(self):
        self.engine = IsomorphEngine(similarity_threshold=0.85)
        self.corpus = load_benchmark_corpus()
        self.engine.register_papers(self.corpus)

    def test_corpus_loading(self):
        self.assertEqual(len(self.corpus), 6)
        domains = set(p.domain for p in self.corpus)
        self.assertEqual(len(domains), 6)

    def test_topological_signature_dimension(self):
        paper = self.corpus[0]
        sig = InvariantTopology.extract_topological_signature(paper)
        self.assertEqual(len(sig), 14)
        self.assertTrue(all(isinstance(x, (float, int)) for x in sig))

    def test_weisfeiler_lehman_hash(self):
        p1 = self.corpus[0]  # Neuro
        p2 = self.corpus[1]  # Hydro
        wl1 = InvariantTopology.compute_weisfeiler_lehman_hash(p1)
        wl2 = InvariantTopology.compute_weisfeiler_lehman_hash(p2)
        self.assertTrue(len(wl1) > 0)
        self.assertTrue(len(wl2) > 0)

    def test_engine_cross_domain_discovery(self):
        results = self.engine.run_scan()
        self.assertEqual(results["papers_indexed"], 6)
        self.assertGreater(results["bridges_discovered"], 0)
        self.assertGreater(results["collisions_detected"], 0)

        # Check top bridge
        top_bridge = self.engine.discovered_bridges[0]
        self.assertNotEqual(top_bridge.source_paper.domain, top_bridge.target_paper.domain)
        self.assertGreaterEqual(top_bridge.topological_similarity, 0.85)
        self.assertTrue(len(top_bridge.synthesized_hypothesis) > 20)
        self.assertTrue(len(top_bridge.mathematical_bridge_equation) > 10)
        self.assertTrue(len(top_bridge.falsification_protocol) > 20)

    def test_pairwise_matching(self):
        p1 = self.corpus[0]  # Neuro
        p2 = self.corpus[1]  # Hydro
        bridge = self.engine.matcher.match_pair(p1, p2)
        self.assertIsNotNone(bridge)
        synthesized = HypothesisSynthesizer.synthesize_bridge_hypothesis(bridge)
        self.assertEqual(synthesized.topological_similarity, 1.0)
        self.assertIn("Interstitial_Debris_Flux", synthesized.mapped_nodes)

    def test_axiomatic_collision_detection(self):
        self.engine.run_scan()
        collisions = self.engine.detected_collisions
        self.assertTrue(len(collisions) > 0)
        # Ensure at least one collision involves equilibrium vs far-from-equilibrium
        found_regime_clash = any(
            "Equilibrium" in c.conflicting_premise for c in collisions
        )
        self.assertTrue(found_regime_clash)

    def test_json_and_markdown_serialization(self):
        self.engine.run_scan()
        dossier = self.engine.generate_markdown_dossier()
        self.assertIn("# ISOMORPH", dossier)
        self.assertIn("Cross-Disciplinary Epistemic Discovery Dossier", dossier)

        json_data = self.engine.to_json()
        self.assertIn('"bridges":', json_data)
        self.assertIn('"collisions":', json_data)


if __name__ == "__main__":
    unittest.main()
