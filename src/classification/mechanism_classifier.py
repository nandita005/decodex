def classify_clients(
    risk,
    cycle_nodes,
    reciprocity_scores=None,
    sync_scores=None,
    infra_flags=None
):
    """
    Regulatory mechanism classification engine.

    Parameters
    ----------
    risk : dict
        client -> risk score (0–1)

    cycle_nodes : set
        clients involved in loops / circular paths

    reciprocity_scores : dict (optional)
        client -> reciprocity value

    sync_scores : dict (optional)
        client -> synchronization score

    infra_flags : dict (optional)
        client -> infrastructure linkage flag

    Returns
    -------
    labels : dict
        client -> classification label
    """

    labels = {}

    # -----------------------------
    # Safe defaults
    # -----------------------------
    reciprocity_scores = reciprocity_scores or {}
    sync_scores = sync_scores or {}
    infra_flags = infra_flags or {}

    # -----------------------------
    # Classification Logic
    # -----------------------------
    for client, r in risk.items():

        rec = reciprocity_scores.get(client, 0)
        sync = sync_scores.get(client, 0)
        infra = infra_flags.get(client, False)

        # =====================================================
        # 1️⃣ Circular Trading
        # =====================================================
        if client in cycle_nodes and r > 0.5:
            labels[client] = "Circular Trading"

        # =====================================================
        # 2️⃣ Pump & Dump Coordination
        # high risk + synchronized behaviour
        # =====================================================
        elif r > 0.65 and sync > 0.6:
            labels[client] = "Pump & Dump Coordination"

        # =====================================================
        # 3️⃣ Infrastructure-Linked Coordination
        # =====================================================
        elif infra and r > 0.5:
            labels[client] = "Infrastructure-Linked Coordination"

        # =====================================================
        # 4️⃣ Legitimate High-Activity Behavior
        # high activity but low reciprocity
        # =====================================================
        elif r > 0.35 and rec < 0.2:
            labels[client] = "Legitimate High-Activity Behavior"

        # =====================================================
        # 5️⃣ Insufficient Evidence
        # =====================================================
        else:
            labels[client] = "Insufficient Evidence"

    return labels