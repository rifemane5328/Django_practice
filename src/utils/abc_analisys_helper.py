import pandas as pd 


def get_abc_statistics(data):
    df = pd.DataFrame(list(data))
    df["total_expenses_pu"] = df["total_expenses_pu"].astype(float)

    total = df["total_expenses_pu"].sum() or 1  # sum of all transactions of all materials
    df["percent"] = round(df["total_expenses_pu"] / total * 100, 2)
    df["cumulative_percent"] = df["percent"].cumsum().round(2)
    return df