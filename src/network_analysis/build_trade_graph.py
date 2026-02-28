import networkx as nx
import matplotlib.pyplot as plt
import os


# ---------------------------------------------------
# BUILD TRADE GRAPH
# ---------------------------------------------------
def build_trade_graph(trades):

    G = nx.DiGraph()

    for _, row in trades.iterrows():

        buyer = row["Buy Client Code"]
        seller = row["Sell Client Code"]

        # increase weight if edge already exists
        if G.has_edge(seller, buyer):
            G[seller][buyer]["weight"] += 1
        else:
            G.add_edge(seller, buyer, weight=1)

    return G


# ---------------------------------------------------
# SAVE NETWORK VISUALIZATION
# ---------------------------------------------------
def save_graph_visual(G, name):

    import os
    os.makedirs("outputs/graphs", exist_ok=True)

    # ⭐ LIMIT GRAPH SIZE FOR VISUALIZATION
    MAX_NODES = 100

    if len(G.nodes()) > MAX_NODES:
        # keep top nodes by degree
        top_nodes = sorted(
            G.degree,
            key=lambda x: x[1],
            reverse=True
        )[:MAX_NODES]

        top_nodes = [n for n, _ in top_nodes]
        G_vis = G.subgraph(top_nodes)

    else:
        G_vis = G

    plt.figure(figsize=(10, 8))

    pos = nx.spring_layout(G_vis, seed=42)

    nx.draw_networkx_nodes(
        G_vis,
        pos,
        node_size=300,
        node_color="skyblue"
    )

    nx.draw_networkx_edges(
        G_vis,
        pos,
        arrows=True,
        arrowsize=10
    )

    nx.draw_networkx_labels(
        G_vis,
        pos,
        font_size=7
    )

    plt.title(f"Trade Network - {name}")
    plt.axis("off")

    plt.savefig(f"outputs/graphs/{name}.png", dpi=300)
    plt.close()