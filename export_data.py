import pandas as pd
from tinydb import TinyDB, where

def export_experiment_csv():
    db_path = "./data.json"
    db = TinyDB(db_path)
    df = pd.read_json(db_path, lines = False, typ = "series")
    df = pd.DataFrame.from_dict( df["_default"], orient = "index" )
    df.to_csv("./data.csv")

export_experiment_csv()