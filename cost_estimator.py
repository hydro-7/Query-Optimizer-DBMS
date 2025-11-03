from __future__ import annotations

from typing import Dict, Tuple

from parse import RANode, Relation, Selection, Projection, Join, Subquery


def _estimate_node_cost(node: RANode, table_stats: Dict[str, int]) -> Tuple[float, float]:
    """
    Compute (node_cost, cumulative_cost_under_node) and annotate the node with:
      - cost: estimated output cardinality/cost of that operation
      - cumulative_cost: sum of costs of this node and all descendants

    Heuristics (simple, deterministic):
      - Relation: cost = row_count from table_stats (fallback 1e5)
      - Selection: selectivity 0.1
      - Projection: pass-through (cost = child.cost)
      - Join: cost = max(50, left.cost * right.cost * 0.01)
    """

    # Relation
    if isinstance(node, Relation):
        table_name = node.table_name
        row_count = float(table_stats.get(table_name, 100_000))
        node.cost = row_count
        node.cumulative_cost = row_count
        return node.cost, node.cumulative_cost

    # Selection
    if isinstance(node, Selection):
        child_cost, child_cum = _estimate_node_cost(node.child, table_stats)
        selectivity = 0.1
        node.cost = max(1.0, child_cost * selectivity)
        node.cumulative_cost = node.cost + child_cum
        return node.cost, node.cumulative_cost

    # Projection
    if isinstance(node, Projection):
        child_cost, child_cum = _estimate_node_cost(node.child, table_stats)
        node.cost = child_cost
        node.cumulative_cost = node.cost + child_cum
        return node.cost, node.cumulative_cost

    # Join
    if isinstance(node, Join):
        left_cost, left_cum = _estimate_node_cost(node.left, table_stats)
        right_cost, right_cum = _estimate_node_cost(node.right, table_stats)
        node.cost = max(50.0, left_cost * right_cost * 0.01)
        node.cumulative_cost = node.cost + left_cum + right_cum
        return node.cost, node.cumulative_cost

    # Subquery
    if isinstance(node, Subquery):
        child_cost, child_cum = _estimate_node_cost(node.child, table_stats)
        node.cost = child_cost
        node.cumulative_cost = node.cost + child_cum
        return node.cost, node.cumulative_cost

    # Fallback (should not happen)
    node.cost = 0.0
    node.cumulative_cost = 0.0
    return node.cost, node.cumulative_cost


def estimate_cost(root: RANode, table_stats: Dict[str, int]) -> None:
    """Annotate the tree rooted at root with cost and cumulative_cost fields."""
    _estimate_node_cost(root, table_stats)


def visualize_costs(root: RANode) -> None:
    """Placeholder for API compatibility; costs are embedded in node labels already."""
    return None


