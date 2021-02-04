import pandas as pd
from tinydb import TinyDB, where
import matplotlib.pyplot as plt
from datetime import datetime

def export_experiment_csv():
    db_path = "./data.json"
    db = TinyDB(db_path)
    df = pd.read_json(db_path, lines = False, typ = "series")
    df = pd.DataFrame.from_dict( df["_default"], orient = "index" )
    df = df.explode("value")
    df.to_csv("./data.csv")
    return df

def plot_arduino(df):
    arduino_df = df.loc[df["type"] == "arduino"]
    arduino_df.to_csv("./arduino_data.csv")
    x = []
    y = []
    for index, row in arduino_df.iterrows():
        x.append( float(row["timestamp"]) )
        y.append( float(row["value"][0]) )
    plt.plot(x,y)
    plt.savefig("./arduino.png")
    

df = export_experiment_csv()
plot_arduino(df)