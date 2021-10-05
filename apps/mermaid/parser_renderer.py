"""
Parser and renderer for a subset of mermaid js graph syntax.

The official parser uses inline javascript: https://github.com/mermaid-js/mermaid/blob/develop/src/diagrams/flowchart/parser/flow.jison so it'd be a little annoying to use that.
"""

from typing import NamedTuple, List, Dict, Tuple, Any

from collections import defaultdict

import lark


grammar = """
start: ((header NEWLINE (line NEWLINE)* line) | header)
header: "graph " CNAME+
//line: WS_INLINE* link_style_statement
line: WS_INLINE* (style_statement | link_style_statement | node_statement)

link_style_statement: "linkStyle" WS_INLINE INT WS_INLINE style+
?style: ((style_item ",") | style_item)
?style_item: style_name ":" style_value
style_name: (LETTER | "-")+
style_value: style_character+
?style_character: LETTER
                | INT
                | "#" -> hash

style_statement: "style" WS_INLINE CNAME+ WS_INLINE style+

node_statement: node (arrow WS_INLINE? node)?
node: CNAME+ node_label?
?node_label: (("[" label_text "]") | ("(" label_text ")") | ("{" label_text "}"))
arrow: WS_INLINE? "-->" arrow_label?
?arrow_label: "|" label_text "|"

label_text: label_char+
?label_char: /[^\\]})]/

%import common.CNAME
%import common.LETTER
%import common.NEWLINE
%import common.WS_INLINE
%import common.INT
"""


class MermaidGraph(NamedTuple):
    direction: str
    nodes: List[Dict[str, Any]]
    edges: Dict[Tuple[str, str], Dict[str, Any]]

    @staticmethod
    def empty():
        return MermaidGraph(
            direction="TD",
            nodes=[],
            edges={}
        )


class GraphTransformer(lark.Transformer):
    """
    Simplifies a mermaid.js graph
    """

    def start(self, args):
        direction = args[0]
        nodes = {}
        edges = {}
        edge_index_map = {}
        edge_counter = 0
        for line in args[1:]:
            if type(line) != dict:
                # Skip the newline in the line newline pair in start
                continue

            for (node1, node2, label) in line["edges"]:
                # Unlike mermaid we only allow one edge from n1 to n2
                key = (node1, node2)
                if key in edges:
                    styles = edges[key]["styles"]
                else:
                    styles = {}

                edge_index_map[edge_counter] = key
                edges[key] = {
                    "label": label,
                    "styles": styles,
                }
                edge_counter += 1

            for (name, label, style) in line["nodes"]:
                new_style = nodes[name]["styles"] if name in nodes else {}
                new_style.update(style)
                if name in nodes:
                    new_label = label or nodes[name]["label"]
                else:
                    new_label = label

                nodes[name] = {
                    "name": name,
                    "label": new_label,
                    "styles": new_style
                }

            for (index, styles) in line["link_styles"]:
                key = edge_index_map[index]
                edges[key]["styles"].update(styles)

        return MermaidGraph(
            direction=direction,
            nodes=list(nodes.values()),
            edges=edges
        )

    def header(self, args):
        return args[0].value

    def line(self, args):
        if len(args) == 1:
            return args[0]
        else:
            return args[1]

    def node_statement(self, args):
        node_one = self._parse_node(args[0].children)
        nodes = [node_one]
        edges = []

        if len(args) > 1:
            if len(args[1].children) == 2:
                edge_label = self._join_string(args[1].children[1].children)
            else:
                edge_label = None

            node_two = self._parse_node(args[3].children)
            nodes.append(node_two)

            edges.append(
                (node_one[0], node_two[0], edge_label)
            )

        return {
            "nodes": nodes,
            "edges": edges,
            "link_styles": {}
        }

    def style_statement(self, args):
        node_name = args[1].value
        styles = {}
        for style_item in args[3:]:
            key = self._join_string(style_item.children[0].children)
            value = self._join_string(style_item.children[1].children)
            styles[key] = value

        return {
            "nodes": [(node_name, None, styles)],
            "edges": [],
            "link_styles": {}
        }

    def link_style_statement(self, args):
        index = int(args[1].value)
        styles = {}
        for style_item in args[3:]:
            key = self._join_string(style_item.children[0].children)
            value = self._join_string(style_item.children[1].children)
            styles[key] = value

        return {
            "nodes": [],
            "edges": [],
            "link_styles": [(index, styles)]
        }

    def _parse_node(self, node):
        node_name = node[0].value
        if len(node) == 2:
            node_label = self._join_string(node[1].children)
        else:
            node_label = None

        return (node_name, node_label, {})

    def _join_string(self, bits):
        def _handle_tree(bit):
            if bit._pretty_label() == "hash":
                return "#"
            else:
                assert False
        # Don't know how to join these in the grammar itself...
        return "".join([
            label_bit.value if hasattr(label_bit, "value") else _handle_tree(label_bit)
            for label_bit in bits
        ])


parser = lark.Lark(grammar, parser="lalr")
transformer = GraphTransformer()


def parse_graph(text: str) -> MermaidGraph:
    raw_tree = parser.parse(text.strip())
    return transformer.transform(raw_tree)


def render_graph(parsed: MermaidGraph) -> str:
    indent = " " * 4
    out_lines = []
    out_lines.append(f"graph {parsed.direction}")

    nodes = sorted(parsed.nodes, key=lambda x: x["name"])
    edges = sorted(parsed.edges.items(), key=lambda x: x[0])
    have_node_styles = False
    have_edge_styles = False
    node_positions = {}

    for node in nodes:
        out = f"{indent}{node['name']}"

        if node["label"]:
            out += f"[{node['label']}]"
        out_lines.append(out)
        node_positions[node["name"]] = {
            "line": len(out_lines) - 1,
            "name_start": len(indent),
            "name_length": len(node["name"]),
            "label_start": len(indent) + len(node["name"]) + 1 if node["label"] else None,
            "label_length": len(node["label"]) if node["label"] else 0
        }

        have_node_styles = have_node_styles or (node["styles"] != {})

    if len(edges) > 0:
        out_lines.append("")

    for ((node1, node2), data) in edges:
        out = f"{indent}{node1} -->"
        if data["label"]:
            out += f"|{data['label']}|"
        out += f" {node2}"
        out_lines.append(out)

        have_edge_styles = have_edge_styles or (data["styles"] != {})

    if have_node_styles:
        out_lines.append("")
        for node in nodes:
            if node["styles"] == {}:
                continue

            styles = ",".join(
                f"{k}:{v}"
                for k, v in sorted(node["styles"].items())
            )
            out_lines.append(f"{indent}style {node['name']} {styles}")

    if have_edge_styles:
        out_lines.append("")
        for i, (_, data) in enumerate(edges):
            if data["styles"] == {}:
                continue

            styles = ",".join(
                f"{k}:{v}"
                for k, v in sorted(data["styles"].items())
            )
            out_lines.append(f"{indent}linkStyle {i} {styles}")

    return {
        "graph_str": "\n".join(out_lines),
        "node_positions": node_positions
    }


# Test
if __name__ == "__main__":
    text = """
    graph TD
        A[Christmas] -->|Get money| B(Go shopping)
        B -->|-| C{Let me think}
        C -->|One| D[Laptop]
        C -->|Two| E[iPhone]
        C -->|Three| F[fa:fa-car Car]
        style A fill:yellow,color:red
        style A fill:blue
        linkStyle 2 color:red
      
    """
    result = parse_graph(text)
    print(render_graph(result))
