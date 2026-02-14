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


def _node_label(graph: pydot.Dot, name: str) -> str:
    """Return the label for a node, falling back to its ID."""
    for node in graph.get_nodes():
        if node.get_name().strip('"') == name:
            label = node.get('label')
            if label:
                return label.strip('"')
    for sg in graph.get_subgraphs():
        result = _node_label(sg, name)
        if result != name:
            return result
    return name


def _normalize_label(label: str) -> str:
    """Normalize label: collapse newlines and extra whitespace."""
    return ' '.join(label.replace('\\n', ' ').split())


def _build_label_map(graph: pydot.Dot) -> dict[str, str]:
    """Map node ID -> normalized label for all nodes in the graph."""
    nodes = extract_nodes(graph)
    return {n: _normalize_label(_node_label(graph, n)) for n in nodes}


def extract_node_labels(graph: pydot.Dot) -> set[str]:
    return set(_build_label_map(graph).values())


def extract_edge_labels(graph: pydot.Dot) -> set[tuple[str, str]]:
    label_map = _build_label_map(graph)
    edges = set()
    for edge in graph.get_edges():
        src = label_map.get(edge.get_source().strip('"'), edge.get_source().strip('"'))
        dst = label_map.get(edge.get_destination().strip('"'), edge.get_destination().strip('"'))
        edges.add((src, dst))
    for sg in graph.get_subgraphs():
        sub_map = _build_label_map(sg)
        label_map.update(sub_map)
        for edge in sg.get_edges():
            src = label_map.get(edge.get_source().strip('"'), edge.get_source().strip('"'))
            dst = label_map.get(edge.get_destination().strip('"'), edge.get_destination().strip('"'))
            edges.add((src, dst))
    return edges


def extract_subgraph_labels(graph: pydot.Dot) -> dict[str, set[str]]:
    clusters = {}
    for sg in graph.get_subgraphs():
        name = sg.get_name().strip('"')
        if name.startswith('cluster'):
            sg_label = sg.get('label')
            key = sg_label.strip('"') if sg_label else name
            clusters[key] = extract_node_labels(sg)
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

    # ID-based comparison
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

    # Label-based comparison (robust against ID mismatches)
    truth_labels = extract_node_labels(truth)
    cand_labels = extract_node_labels(candidate)
    label_node_prec, label_node_rec = precision_recall(truth_labels, cand_labels)

    truth_edge_labels = extract_edge_labels(truth)
    cand_edge_labels = extract_edge_labels(candidate)
    label_edge_prec, label_edge_rec = precision_recall(truth_edge_labels, cand_edge_labels)

    truth_sg_labels = extract_subgraph_labels(truth)
    cand_sg_labels = extract_subgraph_labels(candidate)
    if truth_sg_labels:
        matched_labels = sum(1 for k, v in truth_sg_labels.items()
                             if k in cand_sg_labels and v == cand_sg_labels[k])
        sg_label_match = matched_labels / len(truth_sg_labels)
    else:
        sg_label_match = 1.0

    return {
        "node_precision": round(node_prec, 3),
        "node_recall": round(node_rec, 3),
        "edge_precision": round(edge_prec, 3),
        "edge_recall": round(edge_rec, 3),
        "subgraph_match": round(sg_match, 3),
        "label_node_precision": round(label_node_prec, 3),
        "label_node_recall": round(label_node_rec, 3),
        "label_edge_precision": round(label_edge_prec, 3),
        "label_edge_recall": round(label_edge_rec, 3),
        "label_subgraph_match": round(sg_label_match, 3),
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
