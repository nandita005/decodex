def fuse_signals(centrality, micro):

    signals = {}

    for client, score in centrality["degree"].items():
        signals[client] = {
            "network_score": score,
            "volume": micro["volume"]
        }

    return signals