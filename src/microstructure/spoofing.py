def detect_spoofing(orders):
    return (orders["Order Type"] == "Cancel").sum()