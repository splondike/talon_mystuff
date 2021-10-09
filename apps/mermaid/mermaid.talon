title: /Mermaid Live Editor/
-
graph reset:
    graph = user.mermaid_empty_graph()
    user.mermaid_set_graph(graph)

add <user.prose>:
    graph = user.mermaid_parse_graph()
    formatted = user.formatted_text(prose, "title")
    node_name = user.mermaid_generate_new_node_name(graph)
    full_label = "{node_name}: {formatted}"
    new_graph = user.mermaid_add_node(graph, node_name, full_label)
    user.mermaid_set_graph(new_graph)
    user.mermaid_select_node_label(new_graph, node_name, 3)

relabel <user.letters>:
    graph = user.mermaid_parse_graph()
    user.mermaid_select_node_label(graph, letters, 3)

join <user.letters> through <user.letters>:
    graph = user.mermaid_parse_graph()
    new_graph = user.mermaid_join_nodes(graph, user.letters_2, user.letters_1)
    user.mermaid_set_graph(new_graph)

boost <user.letters> through <user.letters>:
    graph = user.mermaid_parse_graph()
    new_graph = user.mermaid_join_nodes(graph, user.letters_2, user.letters_1, "+", "green")
    user.mermaid_set_graph(new_graph)

squash <user.letters> through <user.letters>:
    graph = user.mermaid_parse_graph()
    new_graph = user.mermaid_join_nodes(graph, user.letters_2, user.letters_1, "-", "red")
    user.mermaid_set_graph(new_graph)

break <user.letters> through <user.letters>:
    graph = user.mermaid_parse_graph()
    new_graph = user.mermaid_unjoin_nodes(graph, user.letters_2, user.letters_1)
    user.mermaid_set_graph(new_graph)

wipe <user.letters>:
    graph = user.mermaid_parse_graph()
    new_graph = user.mermaid_delete_node(graph, user.letters)
    user.mermaid_set_graph(new_graph)

style important <user.letters>:
    graph = user.mermaid_parse_graph()
    new_graph = user.mermaid_style_node(graph, user.letters, "fill:#ffaaaa")
    user.mermaid_set_graph(new_graph)

style normal <user.letters>:
    graph = user.mermaid_parse_graph()
    new_graph = user.mermaid_style_node(graph, user.letters, "")
    user.mermaid_set_graph(new_graph)

style trivial <user.letters>:
    graph = user.mermaid_parse_graph()
    new_graph = user.mermaid_style_node(graph, user.letters, "fill:transparent,stroke:none")
    user.mermaid_set_graph(new_graph)
