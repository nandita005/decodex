def detect_wash(trades):

    return trades.groupby(
        ["Buy Client Code","Sell Client Code"]
    ).size().max()