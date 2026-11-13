"""
ISOMORPH: Graph Topology & Invariant Kernel
Computes permutation-invariant structural signatures, Weisfeiler-Lehman colorings,
and topological homology across disparate research graphs.
"""

from __future__ import annotations
import math
import hashlib
from collections import defaultdict, deque
from typing import Dict, List, Tuple, Set, Optional, Any
from .models import ResearchArtifact, DynamicRole, InteractionKind

try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False


class InvariantTopology:
    """
    Computes permutation-invariant graph signatures for causal hypergraphs.
    Works with pure Python data structures and optionally leverages NetworkX.
    """

    @staticmethod
    def build_networkx_graph(artifact: ResearchArtifact):
        """Constructs a NetworkX DiGraph if available, else returns None."""
        if not HAS_NETWORKX:
            return None
        G = nx.DiGraph()
        for name, var in artifact.variables.items():
            G.add_node(name, role=var.role.value, conserved=var.conserved)
        for m in artifact.mechanisms:
            G.add_edge(m.source, m.target, interaction=m.interaction.value, equation=m.governing_equation)
        return G

    @staticmethod
    def compute_weisfeiler_lehman_hash(artifact: ResearchArtifact, iterations: int = 3) -> str:
        """
        Computes the Weisfeiler-Lehman (WL) graph kernel hash.
        This provides a canonical isomorphism certificate independent of variable names.
        """
        # Initial colors based on abstract dynamic roles
        colors: Dict[str, str] = {
            name: str(var.role.value) for name, var in artifact.variables.items()
        }
        
        # Build adjacency
        neighbors: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
        for m in artifact.mechanisms:
            neighbors[m.source].append((m.target, m.interaction.value))

        for it in range(iterations):
            new_colors = {}
            for node, color in colors.items():
                nbr_colors = sorted([
                    f"{colors.get(tgt, 'unknown')}:{interaction}"
                    for tgt, interaction in neighbors.get(node, [])
                ])
                color_tuple = f"{color}|" + ",".join(nbr_colors)
                new_colors[node] = hashlib.sha256(color_tuple.encode("utf-8")).hexdigest()[:8]
            colors = new_colors

        sorted_color_multiset = sorted(colors.values())
        return hashlib.sha256("".join(sorted_color_multiset).encode("utf-8")).hexdigest()[:16]

    @staticmethod
    def extract_topological_signature(artifact: ResearchArtifact) -> List[float]:
        """
        Generates a 14-dimensional continuous invariant signature vector:
        [
          in_degree_max, in_degree_mean, in_degree_std,
          out_degree_max, out_degree_mean, out_degree_std,
          positive_feedback_count, negative_feedback_count, bifurcation_count,
          cycle_count, density, reciprocity, conserved_ratio, avg_path_length
        ]
        """
        nodes = list(artifact.variables.keys())
        n = len(nodes)
        if n == 0:
            return [0.0] * 14

        in_deg = defaultdict(int)
        out_deg = defaultdict(int)
        interactions = defaultdict(int)
        adj: Dict[str, Set[str]] = defaultdict(set)

        for m in artifact.mechanisms:
            out_deg[m.source] += 1
            in_deg[m.target] += 1
            interactions[m.interaction] += 1
            adj[m.source].add(m.target)

        in_vals = [in_deg[node] for node in nodes]
        out_vals = [out_deg[node] for node in nodes]

        in_max = float(max(in_vals)) if in_vals else 0.0
        in_mean = float(sum(in_vals)) / n
        in_var = sum((x - in_mean) ** 2 for x in in_vals) / n
        in_std = math.sqrt(in_var)

        out_max = float(max(out_vals)) if out_vals else 0.0
        out_mean = float(sum(out_vals)) / n
        out_var = sum((x - out_mean) ** 2 for x in out_vals) / n
        out_std = math.sqrt(out_var)

        pos_fb = float(interactions[InteractionKind.POSITIVE_FEEDBACK])
        neg_fb = float(interactions[InteractionKind.NEGATIVE_FEEDBACK])
        bifurc = float(interactions[InteractionKind.THRESHOLD_SWITCH])

        # Simple cycle count calculation via DFS
        cycles = InvariantTopology._count_elementary_cycles(nodes, adj)

        # Graph density & reciprocity
        m_count = len(artifact.mechanisms)
        possible_edges = n * (n - 1) if n > 1 else 1
        density = float(m_count) / float(possible_edges)

        mutual_edges = 0
        for src in list(adj.keys()):
            for tgt in adj[src]:
                if tgt in adj and src in adj[tgt]:
                    mutual_edges += 1
        reciprocity = float(mutual_edges) / float(m_count) if m_count > 0 else 0.0

        conserved_count = sum(1 for v in artifact.variables.values() if v.conserved)
        conserved_ratio = float(conserved_count) / float(n)

        # Approximate average path length
        avg_path = InvariantTopology._avg_shortest_path(nodes, adj)

        return [
            in_max, in_mean, in_std,
            out_max, out_mean, out_std,
            pos_fb, neg_fb, bifurc,
            float(cycles), density, reciprocity, conserved_ratio, avg_path
        ]

    @staticmethod
    def _count_elementary_cycles(nodes: List[str], adj: Dict[str, Set[str]]) -> int:
        """Finds distinct simple cycles (up to length 5) in the directed graph."""
        cycles = 0
        visited_cycles: Set[Tuple[str, ...]] = set()

        def dfs(start: str, current: str, path: List[str]):
            nonlocal cycles
            if len(path) > 5:
                return
            for nxt in adj.get(current, set()):
                if nxt == start and len(path) > 1:
                    # Canonical cycle representation
                    min_idx = path.index(min(path))
                    canon = tuple(path[min_idx:] + path[:min_idx])
                    if canon not in visited_cycles:
                        visited_cycles.add(canon)
                        cycles += 1
                elif nxt not in path:
                    dfs(start, nxt, path + [nxt])

        for node in nodes:
            dfs(node, node, [node])

        return len(visited_cycles)

    @staticmethod
    def _avg_shortest_path(nodes: List[str], adj: Dict[str, Set[str]]) -> float:
        """Computes average shortest path over reachable pairs using BFS."""
        total_dist = 0
        pairs = 0
        for src in nodes:
            queue = deque([(src, 0)])
            visited = {src}
            while queue:
                curr, dist = queue.popleft()
                if dist > 0:
                    total_dist += dist
                    pairs += 1
                for nxt in adj.get(curr, set()):
                    if nxt not in visited:
                        visited.add(nxt)
                        queue.append((nxt, dist + 1))
        return float(total_dist) / float(pairs) if pairs > 0 else 1.0

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        """Computes normalized cosine similarity between two invariant vectors."""
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        if norm1 == 0.0 or norm2 == 0.0:
            return 0.0
        return max(0.0, min(1.0, dot / (norm1 * norm2)))
