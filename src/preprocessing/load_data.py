import pandas as pd
import glob
import os


def read_file(path):
    """Read csv or excel safely"""

    ext = os.path.splitext(path)[1].lower()

    try:
        if ext == ".csv":
            return pd.read_csv(path)

        elif ext in [".xls", ".xlsx"]:
            return pd.read_excel(path)

        else:
            return None

    except Exception as e:
        print(f"⚠️ Skipping bad file: {path}")
        print("Reason:", e)
        return None


def load_all_data():

    # -------- ORDERS --------
    order_files = glob.glob("data/raw/orders/*")
    orders_list = []

    for f in order_files:
        df = read_file(f)
        if df is not None:
            print("Loading order file:", f)
            orders_list.append(df)

    orders = pd.concat(orders_list, ignore_index=True)


    # -------- TRADES --------
    trade_files = glob.glob("data/raw/trades/*")
    trades_list = []

    for f in trade_files:
        df = read_file(f)
        if df is not None:
            print("Loading trade file:", f)
            trades_list.append(df)

    trades = pd.concat(trades_list, ignore_index=True)


    # -------- SUSPICIOUS LIST --------
    suspicious_files = glob.glob("data/raw/suspicious_list/*")
    suspicious_list = []

    for f in suspicious_files:
        df = read_file(f)
        if df is not None:
            suspicious_list.append(df)

    suspicious = (
        pd.concat(suspicious_list, ignore_index=True)
        if suspicious_list else pd.DataFrame()
    )

    # clean column spaces
    orders.columns = orders.columns.str.strip()
    trades.columns = trades.columns.str.strip()

    return orders, trades, suspicious