def build_batches(orders, trades):

    batches = {}

    grouped = trades.groupby(["SCRIP_CODE", "TRADE_DATE"])

    for key, t_df in grouped:
        o_df = orders[
            (orders["Scrip Code"] == key[0]) &
            (orders["ORDER_DATE"] == key[1])
        ]
        batches[key] = (o_df, t_df)

    return batches