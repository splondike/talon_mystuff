import time
import itertools
from typing import Any, Optional

from talon import Module, actions, clip, registry

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

        result = render_graph(graph)
        clip.set_text(result["graph_str"])

        # TODO: Extract all this to action or function
        actions.user.mouse_helper_move_active_window_relative("300", "300")
        actions.mouse_click(0)
        actions.edit.select_all()

        actions.edit.paste()

    def mermaid_generate_new_node_name(graph: MermaidGraph) -> str:
        """
        Generates a new unused node name for the given graph.
        """

        used_nodes = set([
            node["name"]
            for node in graph.nodes
        ])

        letters = list(registry.lists["user.letter"][0].values())
        for letter1, letter2 in itertools.product([""] + letters, letters):
            if letter1 == letter2:
                continue

            combo = f"{letter1}{letter2}"
            if combo not in used_nodes:
                return combo

        raise RuntimeError("No unused node names")

    def mermaid_select_node_label(graph: MermaidGraph, node_name: str, offset: int=0):
        """
        Select the given node's label in the GUI
        """

        result = render_graph(graph)
        position = result["node_positions"][node_name]

        # Ensure editor is focussed
        actions.user.mouse_helper_move_active_window_relative("300", "300")
        actions.mouse_click(0)
        # Move cursor to start of editor
        actions.key("ctrl-home")
        # Move cursor to the right line
        if position["line"] > 0:
            actions.key(f"down:{position['line']}")

        if position["label_start"]:
            # Select the existing label text
            start = position["label_start"] + offset
            length = position["label_length"] - offset
            actions.key(f"right:{start}")
            actions.key(f"shift:down right:{length} shift:up")
        else:
            # No existing label, start one up
            actions.key(f"right:{position['name_start'] + position['name_length']} pipe pipe left")

    def mermaid_add_node(graph: MermaidGraph, node_name: str, node_text: Optional[str]=None):
        """
        Adds the given node to the graph.
        """

        graph.nodes.append({
            "name": node_name,
            "label": node_text,
            "styles": {}
        })
        return graph

    def mermaid_style_node(graph: MermaidGraph, node_name: str, style_str: Optional[str]=None):
        """
        Adds the given node to the graph.
        """

        print(style_str.split(","))
        new_nodes = [
            {
                "name": node["name"],
                "label": node["label"],
                "styles": {
                    bits[0]: bits[1]

                    for style in style_str.split(",")
                    if style != ""
                    for bits in (style.split(":"),)
                } if node["name"] == node_name else node["styles"]
            }

            for node in graph.nodes
        ]
        print(new_nodes)
        return MermaidGraph(
            direction=graph.direction,
            nodes=new_nodes,
            edges=graph.edges
        )

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
