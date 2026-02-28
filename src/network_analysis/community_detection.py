import networkx as nx

def detect_communities(G):
    return list(nx.connected_components(G.to_undirected()))