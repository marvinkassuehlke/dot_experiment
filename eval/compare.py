"""Graph-Diff: Vergleicht Ground Truth DOT mit LLM-generiertem DOT."""
# ABOUTME: Automated graph comparison tool for DOT translation study.
# Compares ground truth DOT with LLM-generated DOT using precision/recall metrics.

import pydot
import sys
from pathlib import Path


def parse_dot(dot_string: str) -> pydot.Dot:
    graphs = pydot.graph_from_dot_data(dot_string)
    if not graphs:
        raise ValueError("Could not parse DOT string")
    return graphs[0]


def extract_nodes(graph: pydot.Dot) -> set[str]:
    nodes = set()
    for node in graph.get_nodes():
        name = node.get_name().strip('"')
        if name not in ('node', 'edge', 'graph', '\\n', ''):
            nodes.add(name)
    # pydot does not create explicit node objects for nodes only referenced in edges,
    # so we also collect node names from edge endpoints.
    for edge in graph.get_edges():
        nodes.add(edge.get_source().strip('"'))
        nodes.add(edge.get_destination().strip('"'))
    for subgraph in graph.get_subgraphs():
        nodes.update(extract_nodes(subgraph))
    return nodes


def extract_edges(graph: pydot.Dot) -> set[tuple[str, str]]:
    edges = set()
    for edge in graph.get_edges():
        src = edge.get_source().strip('"')
        dst = edge.get_destination().strip('"')
        edges.add((src, dst))
    for subgraph in graph.get_subgraphs():
        edges.update(extract_edges(subgraph))
    return edges


def extract_subgraphs(graph: pydot.Dot) -> dict[str, set[str]]:
    clusters = {}
    for sg in graph.get_subgraphs():
        name = sg.get_name().strip('"')
        if name.startswith('cluster'):
            clusters[name] = extract_nodes(sg)
    return clusters


def precision_recall(truth: set, candidate: set) -> tuple[float, float]:
    if not truth and not candidate:
        return 1.0, 1.0
    recall = len(truth & candidate) / len(truth) if truth else 1.0
    precision = len(truth & candidate) / len(candidate) if candidate else 1.0
    return precision, recall


def compare_graphs(truth_dot: str, candidate_dot: str) -> dict:
    truth = parse_dot(truth_dot)
    candidate = parse_dot(candidate_dot)

    truth_nodes = extract_nodes(truth)
    cand_nodes = extract_nodes(candidate)
    node_prec, node_rec = precision_recall(truth_nodes, cand_nodes)

    truth_edges = extract_edges(truth)
    cand_edges = extract_edges(candidate)
    edge_prec, edge_rec = precision_recall(truth_edges, cand_edges)

    truth_sg = extract_subgraphs(truth)
    cand_sg = extract_subgraphs(candidate)
    if truth_sg:
        matched = sum(1 for k, v in truth_sg.items()
                      if k in cand_sg and v == cand_sg[k])
        sg_match = matched / len(truth_sg)
    else:
        sg_match = 1.0

    return {
        "node_precision": round(node_prec, 3),
        "node_recall": round(node_rec, 3),
        "edge_precision": round(edge_prec, 3),
        "edge_recall": round(edge_rec, 3),
        "subgraph_match": round(sg_match, 3),
        "truth_nodes": len(truth_nodes),
        "candidate_nodes": len(cand_nodes),
        "truth_edges": len(truth_edges),
        "candidate_edges": len(cand_edges),
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare.py <ground_truth.dot> <candidate.dot>")
        sys.exit(1)
    truth = Path(sys.argv[1]).read_text()
    candidate = Path(sys.argv[2]).read_text()
    result = compare_graphs(truth, candidate)
    for k, v in result.items():
        print(f"  {k}: {v}")
