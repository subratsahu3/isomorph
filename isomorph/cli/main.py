"""
ISOMORPH CLI: Terminal Interface for Cross-Disciplinary Epistemic Discovery
Provides rich terminal commands for literature scanning, bipartite matching,
bridge explanation, report generation, and web server launch.
"""

from __future__ import annotations
import sys
import json
import argparse
from typing import Optional
from ..core.engine import IsomorphEngine
from ..corpus.benchmark_papers import load_benchmark_corpus
from ..web.server import start_server


def setup_encoding():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def cmd_scan(args):
    setup_encoding()
    threshold = args.threshold
    print(f"\n🔬 [ISOMORPH] Initializing Neuro-Symbolic Literature Engine (Threshold: {threshold})...")
    engine = IsomorphEngine(similarity_threshold=threshold)
    corpus = load_benchmark_corpus()
    engine.register_papers(corpus)

    results = engine.run_scan()
    print(f"✓ Indexed {results['papers_indexed']} empirical papers across {results['domains_analyzed']} distinct disciplines.")
    print(f"✓ Found {results['bridges_discovered']} Cross-Disciplinary Isomorphic Bridges.")
    print(f"✓ Flagged {results['collisions_detected']} Axiomatic Collisions (Silent Contradictions).\n")

    print("=" * 80)
    print("🏆 TOP CROSS-DISCIPLINARY DISCOVERIES")
    print("=" * 80)
    for idx, b in enumerate(engine.discovered_bridges[:args.limit], 1):
        print(f"\n[{idx}] 🌉 Bridge {b.bridge_id}: {b.source_paper.domain} ⟷ {b.target_paper.domain}")
        print(f"    Topological Match: {b.topological_similarity * 100:.1f}%")
        print(f"    Source Paper: {b.source_paper.title} ({b.source_paper.paper_id})")
        print(f"    Target Paper: {b.target_paper.title} ({b.target_paper.paper_id})")
        print("    Structural Alignments:")
        for src_var, tgt_var in list(b.mapped_nodes.items()):
            print(f"      * {src_var} <---> {tgt_var}")
        print(f"    Governing Equation:")
        print(f"      {b.mathematical_bridge_equation}")
        print(f"    Hypothesis:")
        print(f"      {b.synthesized_hypothesis[:150]}...")

    if engine.detected_collisions:
        print("\n" + "=" * 80)
        print("💥 CRITICAL AXIOMATIC COLLISIONS (SILENT CONTRADICTIONS)")
        print("=" * 80)
        for idx, c in enumerate(engine.detected_collisions, 1):
            print(f"\n[{idx}] {c.conflicting_premise}")
            print(f"    Clash: {c.paper_a.paper_id} ({c.paper_a.domain}) vs. {c.paper_b.paper_id} ({c.paper_b.domain})")
            print(f"    Contradiction: {c.mathematical_contradiction}")
            print(f"    Implication: {c.epistemic_implication}")

    print("\n" + "=" * 80)
    print("💡 Run `isomorph explain <bridge_id>` to view complete mathematical derivation.")
    print("💡 Run `isomorph report --output dossier.md` to export the full scientific dossier.")
    print("💡 Run `isomorph serve` to launch the interactive visual laboratory.\n")


def cmd_explain(args):
    setup_encoding()
    engine = IsomorphEngine(similarity_threshold=0.50)
    corpus = load_benchmark_corpus()
    engine.register_papers(corpus)
    engine.run_scan()

    query = args.bridge_id.strip().upper()
    target = None
    for b in engine.discovered_bridges:
        if query in b.bridge_id.upper() or query in b.source_paper.paper_id.upper() or query in b.target_paper.paper_id.upper():
            target = b
            break

    if not target:
        print(f"\n❌ No bridge found matching query '{args.bridge_id}'.")
        print("Available Bridge IDs:")
        for b in engine.discovered_bridges:
            print(f"  * {b.bridge_id}: {b.source_paper.paper_id} ⟷ {b.target_paper.paper_id} ({b.source_paper.domain} ⟷ {b.target_paper.domain})")
        return

    print("=" * 80)
    print(f"🔍 DEEP DIVE: ISOMORPHIC BRIDGE {target.bridge_id}")
    print("=" * 80)
    print(f"Topological Homology Score: {target.topological_similarity * 100:.2f}%\n")
    print(f"Domain A: {target.source_paper.domain}")
    print(f"  Paper:  {target.source_paper.title} [{target.source_paper.paper_id}]")
    print(f"  Phenomenon: {target.source_paper.empirical_phenomenon}")
    print(f"  Bottleneck: {target.source_paper.unresolved_bottleneck}\n")

    print(f"Domain B: {target.target_paper.domain}")
    print(f"  Paper:  {target.target_paper.title} [{target.target_paper.paper_id}]")
    print(f"  Phenomenon: {target.target_paper.empirical_phenomenon}")
    print(f"  Bottleneck: {target.target_paper.unresolved_bottleneck}\n")

    print("--- Variable Role Mapping ---")
    for src_v, tgt_v in target.mapped_nodes.items():
        src_role = target.source_paper.variables[src_v].role.value if src_v in target.source_paper.variables else "var"
        print(f"  * {src_v:<35} ⟷  {tgt_v:<35} [{src_role}]")

    print("\n--- Synthesized Cross-Domain Hypothesis ---")
    print(target.synthesized_hypothesis)

    print("\n--- Governing Mathematical Bridge Equation ---")
    print(target.mathematical_bridge_equation)

    print("\n--- Popperian Falsification Protocol ---")
    print(target.falsification_protocol)
    print("=" * 80 + "\n")


def cmd_match(args):
    setup_encoding()
    corpus = {p.paper_id.upper(): p for p in load_benchmark_corpus()}
    p1_id = args.paper1.strip().upper()
    p2_id = args.paper2.strip().upper()

    if p1_id not in corpus:
        print(f"❌ Unknown paper ID: {args.paper1}. Available: {list(corpus.keys())}")
        return
    if p2_id not in corpus:
        print(f"❌ Unknown paper ID: {args.paper2}. Available: {list(corpus.keys())}")
        return

    p1, p2 = corpus[p1_id], corpus[p2_id]
    engine = IsomorphEngine(similarity_threshold=0.0)
    bridge = engine.matcher.match_pair(p1, p2)

    if not bridge:
        print(f"\n⚠️ Papers {p1_id} and {p2_id} are from the same domain or cannot be paired.")
        return

    from ..core.synthesizer import HypothesisSynthesizer
    synthesized = HypothesisSynthesizer.synthesize_bridge_hypothesis(bridge)

    print("=" * 80)
    print(f"🔗 PAIRWISE MATCH RESULT: {p1_id} ⟷ {p2_id}")
    print("=" * 80)
    print(f"Similarity: {synthesized.topological_similarity * 100:.2f}%")
    print(f"Synthesized Hypothesis:\n{synthesized.synthesized_hypothesis}\n")
    print(f"Bridge Equation:\n{synthesized.mathematical_bridge_equation}\n")
    print("Aligned Variables:")
    for k, v in synthesized.mapped_nodes.items():
        print(f"  * {k} ⟷ {v}")
    print("=" * 80 + "\n")


def cmd_papers(args):
    setup_encoding()
    corpus = load_benchmark_corpus()
    print("\n" + "=" * 80)
    print(f"📚 INDEXED LITERATURE CORPUS ({len(corpus)} Papers)")
    print("=" * 80)
    for idx, p in enumerate(corpus, 1):
        print(f"\n[{idx}] {p.paper_id}: {p.title}")
        print(f"    Authors: {p.authors} ({p.year}) | Domain: {p.domain}")
        print(f"    Regime:  {p.regime.value}")
        print(f"    Mystery: {p.unresolved_bottleneck}")
        print(f"    Variables ({len(p.variables)}): {', '.join(p.variables.keys())}")
        print(f"    Mechanisms ({len(p.mechanisms)}):")
        for m in p.mechanisms:
            print(f"      - {m.source} -> {m.target} [{m.interaction.value}]: {m.governing_equation}")
    print("\n" + "=" * 80 + "\n")


def cmd_report(args):
    setup_encoding()
    engine = IsomorphEngine(similarity_threshold=args.threshold)
    engine.register_papers(load_benchmark_corpus())
    engine.run_scan()

    output_file = args.output
    if args.format.lower() == "json":
        data = engine.to_json()
        if not output_file.endswith(".json"):
            output_file += ".json"
    else:
        data = engine.generate_markdown_dossier()
        if not output_file.endswith(".md"):
            output_file += ".md"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(data)
    print(f"\n📄 Research Dossier ({args.format.upper()}) compiled and saved to: {output_file}\n")


def cmd_serve(args):
    start_server(port=args.port)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="isomorph",
        description="ISOMORPH: Cross-Disciplinary Structural Isomorphism & Dialectic Discovery Engine",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # scan
    scan_p = subparsers.add_parser("scan", help="Run cross-disciplinary scan across literature corpus")
    scan_p.add_argument("--threshold", type=float, default=0.85, help="Minimum topological similarity threshold (0.0 - 1.0)")
    scan_p.add_argument("--limit", type=int, default=5, help="Maximum number of top discoveries to display")
    scan_p.set_defaults(func=cmd_scan)

    # explain
    exp_p = subparsers.add_parser("explain", help="Deep dive into a specific bridge ID or paper pair")
    exp_p.add_argument("bridge_id", type=str, help="Bridge ID or paper ID (e.g. ISO-373B or NEURO-2024-88)")
    exp_p.set_defaults(func=cmd_explain)

    # match
    match_p = subparsers.add_parser("match", help="Direct pairwise topological match between two specific papers")
    match_p.add_argument("paper1", type=str, help="First paper ID (e.g. NEURO-2024-88)")
    match_p.add_argument("paper2", type=str, help="Second paper ID (e.g. HYDRO-1998-12)")
    match_p.set_defaults(func=cmd_match)

    # papers
    papers_p = subparsers.add_parser("papers", help="List all indexed scientific papers in corpus")
    papers_p.set_defaults(func=cmd_papers)

    # report
    rep_p = subparsers.add_parser("report", help="Export full scientific dossier")
    rep_p.add_argument("--output", type=str, default="isomorph_dossier", help="Output file path (without extension or with)")
    rep_p.add_argument("--format", type=str, choices=["md", "json"], default="md", help="Export format: md or json")
    rep_p.add_argument("--threshold", type=float, default=0.85, help="Minimum topological similarity threshold")
    rep_p.set_defaults(func=cmd_report)

    # serve
    srv_p = subparsers.add_parser("serve", help="Launch interactive visual web dashboard")
    srv_p.add_argument("--port", type=int, default=8000, help="Web server port (default: 8000)")
    srv_p.set_defaults(func=cmd_serve)

    return parser


def main():
    setup_encoding()
    parser = build_parser()
    if len(sys.argv) == 1:
        # Default action: run scan
        cmd_scan(argparse.Namespace(threshold=0.85, limit=5))
        return

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
