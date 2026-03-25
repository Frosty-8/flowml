import pandas as pd
from sqlalchemy import create_engine


# ---------------- CSV ----------------
def load_csv(path: str):
    return pd.read_csv(path)


# ---------------- Excel ----------------
def load_excel(path: str, sheet_name=0):
    return pd.read_excel(path, sheet_name=sheet_name)


# ---------------- Database ----------------
def load_from_db(connection_string: str, query: str):
    engine = create_engine(connection_string)
    df = pd.read_sql(query, engine)
    return df