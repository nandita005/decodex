import json

def generate_evidence(signals, labels):

    evidence = {}

    for client in signals:

        evidence[client] = {
            "label": labels[client],
            "network_score": signals[client]["network_score"]
        }

    with open("outputs/evidence_logs/evidence.json","w") as f:
        json.dump(evidence,f,indent=2)

    return evidence