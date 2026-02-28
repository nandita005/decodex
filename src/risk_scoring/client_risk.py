def compute_client_risk(signals):

    risk = {}

    for client, s in signals.items():
        risk[client] = s["network_score"] * 100

    return risk