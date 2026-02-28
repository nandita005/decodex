import networkx as nx
import matplotlib.pyplot as plt
import os


# ---------------------------------------------------
# BUILD CLIENT ↔ CLIENT TRADE GRAPH
# ---------------------------------------------------
def build_trade_graph(trades):

    G = nx.DiGraph()

    for _, row in trades.iterrows():

        buyer = row["Buy Client Code"]
        seller = row["Sell Client Code"]

        # increase edge weight if already exists
        if G.has_edge(seller, buyer):
            G[seller][buyer]["weight"] += 1
        else:
            G.add_edge(seller, buyer, weight=1)

    return G


# ---------------------------------------------------
# BUILD MEMBER ↔ CLIENT GRAPH
# ---------------------------------------------------
def build_member_client_graph(trades):

    Gm = nx.Graph()

    member_col = "Member Code"

    # safety check
    if member_col not in trades.columns:
        return Gm

    for _, row in trades.iterrows():

        member = row[member_col]
        client = row["Buy Client Code"]

        Gm.add_edge(member, client)

    return Gm


# ---------------------------------------------------
# SAVE NETWORK VISUALIZATION
# ---------------------------------------------------
def save_graph_visual(G, name):

    os.makedirs("outputs/graphs", exist_ok=True)

    MAX_NODES = 100

    # limit visualization size
    if len(G.nodes()) > MAX_NODES:
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