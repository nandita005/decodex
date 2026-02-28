def price_volume_features(trades):

    return {
        "avg_price": trades["TRADE_RATE"].mean(),
        "volume": trades["TRADE_QUANTITY"].sum()
    }