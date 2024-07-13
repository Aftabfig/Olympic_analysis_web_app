import pandas as pd

def preprocess(df, region_data):
    # Filtering for yhe summer olympics
    df = df[df["Season"] == "Summer"]
    # merge with the region_df
    df = df.merge(region_data, on="NOC", how="left")
    # Droping duplicates
    df.drop_duplicates(inplace=True)
    # One hot encoding medal
    df = pd.concat([df, pd.get_dummies(df["Medal"])], axis=1)
    return df
