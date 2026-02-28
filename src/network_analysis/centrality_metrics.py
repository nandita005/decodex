import networkx as nx


def compute_centrality(G):

    # degree centrality
    degree = nx.degree_centrality(G)

    # reciprocity (global metric)
    reciprocity = nx.reciprocity(G)

    # fast approximation
    sample_k = min(50, len(G.nodes()))

    betweenness = nx.betweenness_centrality(
        G,
        k=sample_k,
        seed=42
    )

    return {
        "degree": degree,
        "betweenness": betweenness,
        "reciprocity": reciprocity
    }