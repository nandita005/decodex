import networkx as nx

def compute_centrality(G):

    # FAST metrics
    degree = nx.degree_centrality(G)

    # ⚡ APPROXIMATE betweenness (very fast)
    # sample only few nodes instead of full graph
    sample_k = min(50, len(G.nodes()))

    betweenness = nx.betweenness_centrality(
        G,
        k=sample_k,
        seed=42
    )

    return {
        "degree": degree,
        "betweenness": betweenness
    }