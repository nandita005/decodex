from src.preprocessing.load_data import load_all_data
from src.preprocessing.build_scrip_date_batches import build_batches

from src.network_analysis.build_trade_graph import (
    build_trade_graph,
    save_graph_visual,
    build_member_client_graph
)
from src.network_analysis.centrality_metrics import compute_centrality
from src.network_analysis.cycle_detection import detect_cycles

from src.microstructure.price_volume import price_volume_features
from src.reasoning_engine.signal_fusion import fuse_signals

from src.risk_scoring.client_risk import compute_client_risk
from src.classification.mechanism_classifier import classify_clients
from src.explainability.evidence_generator import generate_evidence


def run_pipeline():

    # ==================================================
    # 1️⃣ LOAD DATA
    # ==================================================
    orders, trades, suspicious = load_all_data()

    print("Orders rows:", len(orders))
    print("Trades rows:", len(trades))
    print("Unique BUY clients:", trades["Buy Client Code"].nunique())
    print("Unique SELL clients:", trades["Sell Client Code"].nunique())

    # ==================================================
    # 2️⃣ BUILD SCRIP-DATE BATCHES
    # ==================================================
    batches = build_batches(orders, trades)
    print("Total batches created:", len(batches))

    all_results = []

    # ==================================================
    # 3️⃣ PROCESS EACH BATCH
    # ==================================================
    for key, (o_df, t_df) in batches.items():

        print("\nProcessing batch:", key)

        # -----------------------------
        # Build trade graph
        # -----------------------------
        G = build_trade_graph(t_df)
        print("Nodes:", len(G.nodes()))
        print("Edges:", len(G.edges()))

        # -----------------------------
        # Save graph (only medium size)
        # -----------------------------
        if 10 < len(G.nodes()) < 120:
            scrip, date = key
            graph_name = f"{scrip}_{date}"

            print("Saving graph:", graph_name)
            save_graph_visual(G, graph_name)
        cycle_nodes = detect_cycles(G)
        for node in cycle_nodes:
            neighbors = list(G.neighbors(node))
            print(f"Cycle node {node} has neighbors: {neighbors}")
        # -----------------------------
        # Fast cycle detection
        # -----------------------------

        # -----------------------------
        # Network metrics
        # -----------------------------
        centrality = compute_centrality(G)
        print("Reciprocity:", centrality["reciprocity"])
        # -----------------------------
        # Microstructure features
        # -----------------------------
        micro = price_volume_features(t_df)

        # -----------------------------
        # Signal fusion
        # -----------------------------
        signals = fuse_signals(centrality, micro)

        # -----------------------------
        # Risk scoring
        # -----------------------------
        risk = compute_client_risk(signals)

        # -----------------------------
        # Classification
        # -----------------------------
        labels = classify_clients(
    risk,
    cycle_nodes,
    sync_scores=micro.get("sync_scores", {})
)
        # -----------------------------
        # Evidence generation
        # -----------------------------
        evidence = generate_evidence(signals, labels)

        all_results.append(evidence)

    # ==================================================
    # FINISH
    # ==================================================
    print("\nPipeline completed.")
    print("Total batches processed:", len(all_results))
    G_member = build_member_client_graph(t_df)
    print("Member-Client links:", len(G_member.edges()))

if __name__ == "__main__":
    run_pipeline()