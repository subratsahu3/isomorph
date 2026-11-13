"""
ISOMORPH CLI: Terminal Interface for Cross-Disciplinary Discovery
"""

from __future__ import annotations
import sys
import argparse
from ..core.engine import IsomorphEngine
from ..corpus.benchmark_papers import load_benchmark_corpus
from ..web.server import start_server


def cmd_scan(args):
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
    for idx, b in enumerate(engine.discovered_bridges[:5], 1):
        print(f"\n[{idx}] 🌉 Bridge {b.bridge_id}: {b.source_paper.domain} ⟷ {b.target_paper.domain}")
        print(f"    Topological Match: {b.topological_similarity * 100:.1f}%")
        print(f"    Source Paper: {b.source_paper.title} ({b.source_paper.paper_id})")
        print(f"    Target Paper: {b.target_paper.title} ({b.target_paper.paper_id})")
        print("    Structural Alignments:")
        for src_var, tgt_var in list(b.mapped_nodes.items())[:3]:
            print(f"      * {src_var} <---> {tgt_var}")
        print(f"    Governing Equation:")
        print(f"      {b.mathematical_bridge_equation}")
        print(f"    Hypothesis:")
        print(f"      {b.synthesized_hypothesis[:150]}...")

    if engine.detected_collisions:
        print("\n" + "=" * 80)
        print("💥 CRITICAL AXIOMATIC COLLISIONS (SILENT CONTRADICTIONS)")
        print("=" * 80)
        for idx, c in enumerate(engine.detected_collisions[:3], 1):
            print(f"\n[{idx}] {c.conflicting_premise}")
            print(f"    Clash: {c.paper_a.paper_id} ({c.paper_a.domain}) vs. {c.paper_b.paper_id} ({c.paper_b.domain})")
            print(f"    Contradiction: {c.mathematical_contradiction}")

    print("\n" + "=" * 80)
    print("💡 Run `isomorph report --output dossier.md` to export the full scientific dossier.")
    print("💡 Run `isomorph serve` to launch the interactive visual laboratory.\n")


def cmd_report(args):
    engine = IsomorphEngine(similarity_threshold=args.threshold)
    engine.register_papers(load_benchmark_corpus())
    engine.run_scan()

    dossier = engine.generate_markdown_dossier()
    output_file = args.output
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(dossier)
    print(f"\n📄 Research Dossier compiled and saved to: {output_file}\n")


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
    scan_p.set_defaults(func=cmd_scan)

    # report
    rep_p = subparsers.add_parser("report", help="Export full scientific dossier to Markdown")
    rep_p.add_argument("--output", type=str, default="isomorph_dossier.md", help="Output file path")
    rep_p.add_argument("--threshold", type=float, default=0.85, help="Minimum topological similarity threshold")
    rep_p.set_defaults(func=cmd_report)

    # serve
    srv_p = subparsers.add_parser("serve", help="Launch interactive visual web dashboard")
    srv_p.add_argument("--port", type=int, default=8000, help="Web server port (default: 8000)")
    srv_p.set_defaults(func=cmd_serve)

    return parser


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = build_parser()
    if len(sys.argv) == 1:
        # Default action: run scan
        cmd_scan(argparse.Namespace(threshold=0.85))
        return

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
