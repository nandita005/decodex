def synchronization_score(df):

    if "Buy Time" not in df.columns or "Buy Client Code" not in df.columns:
        return {}

    sync_scores = {}

    for _, row in df.iterrows():
        client = row["Buy Client Code"]
        sync_scores[client] = sync_scores.get(client, 0) + 1

    return sync_scores


def price_volume_features(trades):

    sync = synchronization_score(trades)

    return {
        "avg_price": trades["TRADE_RATE"].mean(),
        "volume": trades["TRADE_QUANTITY"].sum(),
        "sync_scores": sync
    }