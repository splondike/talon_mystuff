import time
from typing import Any, Optional

from talon import Module, actions, clip

from .parser_renderer import parse_graph, render_graph, MermaidGraph


mod = Module()


@mod.action_class
class MermaidLiveActions:
    """
    Actions related to the mermaid live editor.
    """

    def mermaid_empty_graph():
        """
        Returns an empty graph
        """

        return MermaidGraph.empty()

    def mermaid_parse_graph() -> MermaidGraph:
        """
        Grab the text of the page and parse it
        """

        actions.user.mouse_helper_move_active_window_relative("300", "300")
        actions.mouse_click(0)
        actions.edit.select_all()
        actions.edit.copy()
        # Sleep to allow the clipboard to be updated
        time.sleep(0.1)
        graph_text = clip.text().strip()
        return parse_graph(graph_text)

    def mermaid_set_graph(graph: MermaidGraph):
        """
        Updates the page with the given graph
        """

        graph_text = render_graph(graph)
        clip.set_text(graph_text)

        actions.user.mouse_helper_move_active_window_relative("300", "300")
        actions.mouse_click(0)
        actions.edit.select_all()

        actions.edit.paste()

    def mermaid_add_node(graph: MermaidGraph, node_name: str):
        """
        Adds the given node to the graph
        """

        graph.nodes.append({
            "name": node_name,
            "label": None,
            "styles": {}
        })
        return graph

    def mermaid_join_nodes(
            graph: MermaidGraph, node_name1: str, node_name2: str,
            label: Optional[str]=None, stroke_color: Optional[str]=None):
        """
        Draws an arrow from node1 to node2
        """

        key = (node_name1, node_name2)
        graph.edges[key] = {
            "label": label,
            "styles": {"stroke": stroke_color} if stroke_color else {}
        }

        return graph

    def mermaid_unjoin_nodes(graph: MermaidGraph, node_name1: str, node_name2: str):
        """
        Removes any connections between node1 and node2
        """

        try:
            graph.edges.pop((node_name1, node_name2))
        except KeyError:
            pass

        return graph

    def mermaid_delete_node(graph: MermaidGraph, node_name: str):
        """
        Removes the given node from the graph
        """

        new_edges = {}
        for edge in graph.edges.items():
            key, data = edge
            (name1, name2) = key
            if name1 != node_name and name2 != node_name:
                new_edges[key] = data

        new_nodes = []
        for curr_node in graph.nodes:
            if curr_node["name"] != node_name:
                new_nodes.append(curr_node)

        return MermaidGraph(
            direction=graph.direction,
            edges=new_edges,
            nodes=new_nodes
        )
