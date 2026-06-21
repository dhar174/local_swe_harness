"""Main orchestrator graph that dispatches to tier sub-graphs."""
from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from swe_agents.state import OrchestratorState


def build_main_graph() -> StateGraph:
    """Construct and return the main orchestrator graph."""
    graph = StateGraph(OrchestratorState)

    # Nodes are added by importing from nodes package
    # Edges implement conditional routing via routing package
    # This is a stub – full node wiring is done in subsequent issues.

    graph.add_node("intake", lambda s: s)
    graph.add_edge(START, "intake")
    graph.add_edge("intake", END)
    return graph
