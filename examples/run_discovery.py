"""
ISOMORPH Example: Rapid Cross-Disciplinary Discovery Script
Demonstrates how to run a scan, inspect isomorphic bridges, and export a report in 10 lines of code.
"""

import sys
import os

# Ensure package root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from isomorph.core.engine import IsomorphEngine
from isomorph.corpus.benchmark_papers import load_benchmark_corpus

def main():
    print("🔬 Initializing ISOMORPH Engine...")
    engine = IsomorphEngine(similarity_threshold=0.88)
    
    # Load multi-domain corpus
    papers = load_benchmark_corpus()
    engine.register_papers(papers)

    # Execute discovery
    summary = engine.run_scan()
    print(f"✓ Discovered {summary['bridges_discovered']} isomorphic bridges across {summary['domains_analyzed']} domains!")

    # Inspect the top bridge
    top = engine.discovered_bridges[0]
    print(f"\n🏆 Top Breakthrough Candidate:")
    print(f"Domain A: {top.source_paper.domain} ({top.source_paper.paper_id})")
    print(f"Domain B: {top.target_paper.domain} ({top.target_paper.paper_id})")
    print(f"Similarity: {top.topological_similarity * 100:.1f}%")
    print(f"Bridge Equation: {top.mathematical_bridge_equation}")
    print(f"\nHypothesis:\n{top.synthesized_hypothesis}")

if __name__ == "__main__":
    main()
