import os
import pandas as pd
 
# iterate over all files within "data"
for file in os.listdir("data/google"):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join("data/google", file))
        df["query"] = file.replace("_", " ").replace(".csv", "")
        df.to_csv("data/google/all.csv", index=False, mode='a')