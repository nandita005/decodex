def classify_clients(
    risk,
    cycle_nodes,
    reciprocity_scores=None,
    sync_scores=None,
    infra_flags=None
):

    labels = {}

    reciprocity_scores = reciprocity_scores or {}
    sync_scores = sync_scores or {}
    infra_flags = infra_flags or {}

    for client, r in risk.items():

        rec = reciprocity_scores.get(client, 0)
        sync = sync_scores.get(client, 0)
        infra = infra_flags.get(client, False)

        # Circular Trading
        if client in cycle_nodes and r > 0.5:
            labels[client] = "Circular Trading"

        # Pump & Dump (risk proxy)
        elif r > 0.65:
            labels[client] = "Pump & Dump Coordination"

        # Infrastructure-linked
        elif infra and r > 0.5:
            labels[client] = "Infrastructure-Linked Coordination"

        # Legitimate High Activity
        elif r > 0.35 and rec < 0.2:
            labels[client] = "Legitimate High-Activity Behavior"

        else:
            labels[client] = "Insufficient Evidence"

    return labels