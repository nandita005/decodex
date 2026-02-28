import json
import os


def generate_evidence(signals, labels):

    evidence = {}

    # make sure folder exists
    os.makedirs("outputs/evidence_logs", exist_ok=True)

    for client in signals:

        # safe risk value
        risk_score = signals.get(client, {}).get("network_score", 0)

        # build evidence entry
        evidence[client] = {
            "label": labels.get(client, "Insufficient Evidence"),
            "network_score": signals.get(client, {}).get("network_score", 0),
            "evidence_strength": signals.get(client, {}).get("network_score", 0)
        }

    # save json
    with open("outputs/evidence_logs/evidence.json", "w") as f:
        json.dump(evidence, f, indent=2)

    return evidence