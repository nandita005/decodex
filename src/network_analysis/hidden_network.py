def expand_network(G, suspicious_nodes):

    expanded = set(suspicious_nodes)

    for node in suspicious_nodes:
        expanded.update(G.neighbors(node))

    return expanded