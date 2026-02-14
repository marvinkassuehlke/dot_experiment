# ABOUTME: Compares Mermaid translations against DOT ground truth using label-based metrics.
# Used for the DOT vs Mermaid format comparison experiment.

import re
import sys
from pathlib import Path

# Reuse ground truth extraction from compare.py
sys.path.insert(0, str(Path(__file__).parent))
from compare import parse_dot, extract_node_labels, extract_edge_labels, extract_subgraph_labels, precision_recall, _normalize_label


def _extract_node_defs(mmd_text: str) -> dict[str, str]:
    """Build id -> label map from Mermaid node definitions, excluding subgraphs."""
    id_to_label = {}
    # Remove subgraph lines to avoid matching their labels as nodes
    lines = [l for l in mmd_text.split('\n')
             if not l.strip().startswith('subgraph') and l.strip() != 'end']
    clean = '\n'.join(lines)

    # Match quoted labels: id["label"], id{" label"}, id(("label"))
    for match in re.finditer(r'(\w+)\s*[\[\(\{]+[\(\[]?"([^"]+)"[\)\]]?[\]\)\}]+', clean):
        node_id = match.group(1).strip()
        label = _normalize_label(match.group(2).strip())
        id_to_label[node_id] = label

    return id_to_label


def extract_mermaid_nodes(mmd_text: str) -> set[str]:
    """Extract node labels from Mermaid text."""
    return set(_extract_node_defs(mmd_text).values())


def extract_mermaid_edges(mmd_text: str) -> set[tuple[str, str]]:
    """Extract edges as (source_label, target_label) from Mermaid text."""
    id_to_label = _extract_node_defs(mmd_text)

    # Extract edges: id1 --> id2, id1 -.-> id2, id1 -->|label| id2
    edges = set()
    for match in re.finditer(r'(\w+)\s+(?:-->|-.->)(?:\|[^|]*\|)?\s+(\w+)', mmd_text):
        src_id = match.group(1).strip()
        dst_id = match.group(2).strip()
        src_label = id_to_label.get(src_id, src_id)
        dst_label = id_to_label.get(dst_id, dst_id)
        edges.add((src_label, dst_label))
    return edges


def extract_mermaid_subgraphs(mmd_text: str) -> set[str]:
    """Extract subgraph labels from Mermaid text."""
    labels = set()
    for match in re.finditer(r'subgraph\s+\w+\s*\["([^"]+)"\]', mmd_text):
        labels.add(_normalize_label(match.group(1)))
    # Also match: subgraph Name (without quotes)
    for match in re.finditer(r'subgraph\s+(\w+)\s*$', mmd_text, re.MULTILINE):
        name = match.group(1)
        if name not in ('end',):
            labels.add(_normalize_label(name))
    return labels


def compare_mermaid_vs_dot(truth_dot: str, candidate_mmd: str) -> dict:
    """Compare Mermaid translation against DOT ground truth using label-based metrics."""
    truth = parse_dot(truth_dot)

    truth_nodes = extract_node_labels(truth)
    cand_nodes = extract_mermaid_nodes(candidate_mmd)
    node_prec, node_rec = precision_recall(truth_nodes, cand_nodes)

    truth_edges = extract_edge_labels(truth)
    cand_edges = extract_mermaid_edges(candidate_mmd)
    edge_prec, edge_rec = precision_recall(truth_edges, cand_edges)

    return {
        "node_precision": round(node_prec, 3),
        "node_recall": round(node_rec, 3),
        "edge_precision": round(edge_prec, 3),
        "edge_recall": round(edge_rec, 3),
        "truth_nodes": len(truth_nodes),
        "candidate_nodes": len(cand_nodes),
        "truth_edges": len(truth_edges),
        "candidate_edges": len(cand_edges),
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_mermaid.py <ground_truth.dot> <candidate.mmd>")
        sys.exit(1)
    truth = Path(sys.argv[1]).read_text()
    candidate = Path(sys.argv[2]).read_text()
    result = compare_mermaid_vs_dot(truth, candidate)
    for k, v in result.items():
        print(f"  {k}: {v}")
