import networkx as nx

def detect_cycles(G):

    # FAST APPROXIMATION:
    # nodes that have both incoming and outgoing edges
    cycle_nodes = set()

    for node in G.nodes():
        if G.in_degree(node) > 0 and G.out_degree(node) > 0:
            cycle_nodes.add(node)

    return cycle_nodes