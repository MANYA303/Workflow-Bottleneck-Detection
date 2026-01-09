import pandas as pd

def load_workflow_data(path):
    df = pd.read_csv(path)
    df["start_time"] = pd.to_datetime(df["start_time"])
    df["end_time"] = pd.to_datetime(df["end_time"])
    df["duration_minutes"] = (
        df["end_time"] - df["start_time"]
    ).dt.total_seconds() / 60
    return df