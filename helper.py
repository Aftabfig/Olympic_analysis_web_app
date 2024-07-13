import numpy as np


def fetch_medal_tally(df, years, country):
    medal_df = df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])

    if years == "Overall" and country == "Overall":
        temp_df = medal_df
    if years == "Overall" and country != "Overall":
        flag = 1
        temp_df = medal_df[medal_df["region"] == country]
    if years != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df["Year"] == int(years)]
    if years != "Overall" and country != "Overall":
        temp_df = medal_df[(medal_df["Year"] == years) & (medal_df["region"] == country)]

    x = temp_df.groupby("region").sum()[["Gold", "Silver", "Bronze"]].sort_values("Gold", ascending=False).reset_index()

    x["Total"] = x["Gold"] + x["Silver"] + x["Bronze"]

    return x


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    medal_tally = medal_tally.groupby("region").sum()[["Gold", "Silver", "Bronze"]].sort_values("Gold", ascending=False).reset_index()
    medal_tally["Total"] = medal_tally["Gold"] + medal_tally["Silver"] + medal_tally["Bronze"]
    medal_tally["Gold"] = medal_tally["Gold"].astype("int")
    medal_tally["Silver"] = medal_tally["Silver"].astype("int")
    medal_tally["Bronze"] = medal_tally["Bronze"].astype("int")
    medal_tally["Total"] = medal_tally["Total"].astype("int")

    return medal_tally


def country_year_list(df):
    years = df["Year"].unique().tolist()
    years.sort()
    years.insert(0, "Overall")
    country = np.unique(df["region"].dropna().values).tolist()
    country.sort()
    country.insert(0, "Overall")
    return years,country

# def participating_nations_over_time(df):
#     Nations_Over_Time = df.drop_duplicates(["Year", "region"])["Year"].value_counts().reset_index().sort_values("Year")
#     Nations_Over_Time.rename(columns={"count": "No. of Countries"}, inplace=True)
#     return Nations_Over_Time


def data_over_time(df, col):
    Nations_Over_Time = df.drop_duplicates(["Year", col])["Year"].value_counts().reset_index()
    Nations_Over_Time.columns = ["Year", "No. of Countries"]
    Nations_Over_Time.sort_values("Year", inplace=True)
    return Nations_Over_Time


def data_over_time1(df, col):
    # Drop duplicates to get unique combinations of Year and the specified column
    Nations_Over_Time = df.drop_duplicates(["Year", col])["Year"].value_counts().reset_index()
    Nations_Over_Time.columns = ["Year", "Event"]
    Nations_Over_Time.sort_values("Year", inplace=True)
    return Nations_Over_Time


def data_over_time2(df, col):
    # Drop duplicates to get unique combinations of Year and the specified column
    Nations_Over_Time = df.drop_duplicates(["Year", col])["Year"].value_counts().reset_index()
    Nations_Over_Time.columns = ["Year", "Name"]
    Nations_Over_Time.sort_values("Year", inplace=True)
    return Nations_Over_Time


def most_successful(df, sport):
    temp_df = df.dropna(subset=["Medal"])
    if sport != "Overall":
        temp_df = temp_df[temp_df["Sport"] == sport]
    top_athletes = temp_df["Name"].value_counts().head(15)
    top_athletes_df = top_athletes.reset_index()
    top_athletes_df.columns = ["Name", "Medals"]
    x = top_athletes_df.merge(df, left_on="Name", right_on="Name", how="left")[
        ["Name", "Medals", "Sport", "region"]].drop_duplicates("Name")

    return x


def year_wise_medal_tally(df, country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"], inplace=True)
    new_df = temp_df[temp_df["region"] == country]
    final_df = new_df.groupby("Year").count()["Medal"].reset_index()
    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"], inplace=True)

    new_df = temp_df[temp_df["region"] == country]
    pt = new_df.pivot_table(index="Sport", columns="Year", values="Medal", aggfunc="count").fillna(0)
    return pt


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=["Name", "region"])

    men = athlete_df[athlete_df["Sex"] == "M"].groupby("Year").count()["Name"].reset_index()
    women = athlete_df[athlete_df["Sex"] == "F"].groupby("Year").count()["Name"].reset_index()

    final = men.merge(women, on="Year", how="left")
    final.rename(columns={"Name_x": "Male", "Name_y": "Female"}, inplace=True)

    final.fillna(0, inplace=True)
    return final


