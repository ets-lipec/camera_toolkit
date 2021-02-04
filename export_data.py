import pandas as pd
from tinydb import TinyDB, where
import matplotlib.pyplot as plt
from datetime import datetime
import glob

def export_experiment_csv():
    for name in glob.glob('*.json'):
        db_path = name
        db = TinyDB(db_path)
        df = pd.read_json(db_path, lines = False, typ = "series")
        df = pd.DataFrame.from_dict( df["_default"], orient = "index" )
        df = df.explode("value")
        filename = name.split(".")[0]
        df.to_csv(filename+".csv")
        plot_arduino(df, filename)

def plot_arduino(df, filename):
    arduino_df = df.loc[df["type"] == "arduino"]
    #arduino_df.to_csv("./arduino_data.csv")
    x = []
    y = []
    for index, row in arduino_df.iterrows():
        x.append( float(row["timestamp"]) )
        y.append( float(row["value"][0]) )
    plt.plot(x,y)
    plt.savefig(filename+".png")
    

export_experiment_csv()
