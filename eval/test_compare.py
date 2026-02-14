# ABOUTME: Tests for graph comparison tool (compare.py).
# Validates precision/recall metrics for node, edge, and subgraph comparison.

import pytest
from compare import parse_dot, compare_graphs, extract_nodes, extract_edges, extract_subgraphs


def test_identical_graphs():
    dot = 'digraph { a -> b; b -> c; }'
    result = compare_graphs(dot, dot)
    assert result["node_recall"] == 1.0
    assert result["node_precision"] == 1.0
    assert result["edge_recall"] == 1.0
    assert result["edge_precision"] == 1.0


def test_missing_node():
    truth = 'digraph { a -> b; b -> c; }'
    candidate = 'digraph { a -> b; }'
    result = compare_graphs(truth, candidate)
    assert result["node_recall"] < 1.0
    assert result["edge_recall"] < 1.0


def test_extra_node():
    truth = 'digraph { a -> b; }'
    candidate = 'digraph { a -> b; b -> c; }'
    result = compare_graphs(truth, candidate)
    assert result["node_recall"] == 1.0
    assert result["node_precision"] < 1.0


def test_subgraph_match():
    truth = 'digraph { subgraph cluster_a { x; y; } subgraph cluster_b { z; } }'
    candidate = 'digraph { subgraph cluster_a { x; y; } z; }'
    result = compare_graphs(truth, candidate)
    assert result["subgraph_match"] == 0.5


def test_empty_graphs():
    dot = 'digraph { }'
    result = compare_graphs(dot, dot)
    assert result["node_recall"] == 1.0
    assert result["node_precision"] == 1.0


def test_extract_nodes_from_subgraphs():
    dot = 'digraph { subgraph cluster_a { x; y; } z; }'
    import pydot
    graph = pydot.graph_from_dot_data(dot)[0]
    nodes = extract_nodes(graph)
    assert 'x' in nodes
    assert 'y' in nodes
    assert 'z' in nodes


def test_edge_direction_matters():
    truth = 'digraph { a -> b; }'
    candidate = 'digraph { b -> a; }'
    result = compare_graphs(truth, candidate)
    assert result["edge_recall"] == 0.0
    assert result["edge_precision"] == 0.0
