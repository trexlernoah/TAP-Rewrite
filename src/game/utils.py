import pandas as pd

def save_data(data: pd.DataFrame, filename: str):
    if not filename: return
    data.to_csv(filename, sep='\t', encoding='utf-8', index=False)
