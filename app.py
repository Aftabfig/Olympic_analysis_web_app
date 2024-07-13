import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv("C:/Users/9861m/Downloads/athlete_events.csv")
region_data = pd.read_csv("c:/Users/9861m/Downloads/noc_regions.csv")

df = preprocessor.preprocess(df, region_data)

st.sidebar.title("Olympic Analysis")
user_menu = st.sidebar.radio(
    "Select an Option",
    ("Medal Tally", "Overall Analysis", "Country-wise Analysis", "Athlete-wise Analysis")
)

if user_menu == "Medal Tally":
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    Selected_Year = st.sidebar.selectbox("Select Year", years)
    Selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally = helper.fetch_medal_tally(df,Selected_Year, Selected_country)
    if Selected_Year == "Overall" and Selected_country == "Overall":
        st.title("Overall Tally")
    if Selected_Year != "Overall" and Selected_country == "Overall":
        st.title("Medal Tally in " + str(Selected_Year))
    if Selected_Year == "Overall" and Selected_country != "Overall":
        st.title(Selected_country + " Overall Performance")
    if Selected_Year != "Overall" and Selected_country != "Overall":
        st.title(Selected_country + " Performance in " + str(Selected_Year) + " Olympics")

    st.table(medal_tally)

if user_menu == "Overall Analysis":
    editions = df["Year"].unique().shape[0] - 1
    Cities = df["City"].unique().shape[0]
    Sports = df["Sport"].unique().shape[0]
    Events = df["Event"].unique().shape[0]
    Athletes = df["Name"].unique().shape[0]
    Nations = df["region"].unique().shape[0]

    st.title("Total Statistics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(Cities)
    with col3:
        st.header("Sports")
        st.title(Sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(Events)
    with col2:
        st.header("Nations")
        st.title(Nations)
    with col3:
        st.header("Athletes")
        st.title(Athletes)

    # Nations_Over_Time = helper.participating_nations_over_time(df)
    # fig = px.line(Nations_Over_Time, x="Year", y="No. of Countries")
    # st.title("Participating Nations Over the Year")
    # st.plotly_chart(fig)

    Nations_Over_Time = helper.data_over_time(df, "region")
    fig = px.line(Nations_Over_Time, x="Year", y="No. of Countries")
    st.title("Participating Nations Over the Years")
    st.plotly_chart(fig)

    Nations_Over_Time = helper.data_over_time1(df, "Event")
    fig = px.line(Nations_Over_Time, x="Year", y="Event")
    st.title("Event Over the Years")
    st.plotly_chart(fig)

    Nations_Over_Time = helper.data_over_time2(df, "Name")
    fig = px.line(Nations_Over_Time, x="Year", y="Name")
    st.title("Athletes Over the Years")
    st.plotly_chart(fig)

    st.title("No. of Event over time (Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(["Year", "Sport", "Event"])
    ax = sns.heatmap(x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype("int"),
                annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")

    Selected_Sport = st.selectbox("Select a Sport", sport_list)
    x = helper.most_successful(df, Selected_Sport)
    st.table(x)

if user_menu == "Country-wise Analysis":

    st.sidebar.title("Country wise Analysis")

    country_list = df["region"].dropna().unique()#.to_list()
    country_list.sort()

    Selected_country = st.sidebar.selectbox("Select a country", country_list)

    country_df = helper.year_wise_medal_tally(df, Selected_country)
    fig = px.line(country_df, x= "Year", y="Medal")
    st.title(Selected_country + " Medal Tally Over the Years")
    st.plotly_chart(fig)

    st.title(Selected_country + " excels in the following sports")

    pt = helper.country_event_heatmap(df, Selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

if user_menu == "Athlete-wise Analysis":
    athlete_df = df.drop_duplicates(subset=["Name", "region"])

    x1 = athlete_df["Age"].dropna()
    x2 = athlete_df[athlete_df["Medal"] == "Gold"]["Age"].dropna()
    x3 = athlete_df[athlete_df["Medal"] == "Silver"]["Age"].dropna()
    x4 = athlete_df[athlete_df["Medal"] == "Bronze"]["Age"].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4],
                             ["Overall Age", "Gold Medalist", "Silver Medalist", "Bronze Medalist"],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    st.title("Men Vs Women Participation over the year")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)




