title: /Mermaid Live Editor/
-
graph reset:
    graph = user.mermaid_empty_graph()
    user.mermaid_set_graph(graph)

add <user.word>:
    graph = user.mermaid_parse_graph()
    new_graph = user.mermaid_add_node(graph, user.word)
    user.mermaid_set_graph(new_graph)

join <user.word> through <user.word>:
    graph = user.mermaid_parse_graph()
    new_graph = user.mermaid_join_nodes(graph, user.word_2, user.word_1)
    user.mermaid_set_graph(new_graph)

boost <user.word> through <user.word>:
    graph = user.mermaid_parse_graph()
    new_graph = user.mermaid_join_nodes(graph, user.word_2, user.word_1, "+", "green")
    user.mermaid_set_graph(new_graph)

squash <user.word> through <user.word>:
    graph = user.mermaid_parse_graph()
    new_graph = user.mermaid_join_nodes(graph, user.word_2, user.word_1, "-", "red")
    user.mermaid_set_graph(new_graph)

break <user.word> through <user.word>:
    graph = user.mermaid_parse_graph()
    new_graph = user.mermaid_unjoin_nodes(graph, user.word_2, user.word_1)
    user.mermaid_set_graph(new_graph)

wipe <user.word>:
    graph = user.mermaid_parse_graph()
    new_graph = user.mermaid_delete_node(graph, user.word)
    user.mermaid_set_graph(new_graph)
