from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="An Overview Of Tech Students Dashboard",
    page_icon = ":mortar_board:",
    initial_sidebar_state="auto",
    layout="wide",
    menu_items={
        "Get Help": "https://docs.streamlit.io",
        "Report a bug": "mailto:ikennatimothy275@gmail.com",
        "About": "### Tech Students Dashboard\nBuilt with Streamlit for The Fhenix IT Class.",
    }
)

@st.cache_data
def get_data():
    path = Path(__file__).parent / "Tech_students.xlsx"
    df = pd.read_excel(path, sheet_name="Trainee_Data")
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")] # drop junk columns
    return df

df = get_data()

st.sidebar.header("Filters & Slicers")
track = st.sidebar.multiselect("Track", df["Track"].unique(), default=df["Track"].unique())
city = st.sidebar.multiselect("City", df["City"].unique(), default = df["City"].unique())
status = st.sidebar.multiselect("Status", df["Status"].unique(), default = df["Status"].unique())
mode = st.sidebar.multiselect("Learning Mode", df["Learning Mode"].unique(), default = df["Learning Mode"].unique())

filtered = df[
    df["Track"].isin(track)
    & df["City"].isin(city)
    & df["Status"].isin(status)
    & df["Learning Mode"].isin(mode)
]

st.title("👨‍💻Tech Students Dashboard")
st.write("📊 An Interactive Streamlit Dashbaord Built For The Fhenix Africa IT Class")

if filtered.empty:
    st.warning("No data matches your filters.")
    st.stop()

k1,k2,k3,k4,k5 = st.columns(5)
k1.metric("Total Students", f"{len(filtered):,}")
k2.metric("Graduation Rate", f"{(filtered["Status"] == "Graduated").mean() * 100:.1f}%")
k3.metric("Dropout Rate", f"{(filtered["Status"] == "Dropped").mean() * 100:.1f}%")
k4.metric("Avg Performance", f"{filtered["Performance Score"].mean():.1f}")
k5.metric("Total Revenue", f"${filtered["Training Cost"].sum():,.0f}")

st.divider()
st.header(":chart_with_upwards_trend: Dashboard Visualization Charts")
c1,c2 = st.columns(2)

by_track = filtered.groupby("Track").size().reset_index(name="Students")
fig1 = px.bar(by_track, x="Track", y="Students", color="Track", title="👩‍💻 Students By Track")
c1.plotly_chart(fig1)

by_status = filtered.groupby("Status").size().reset_index(name="Students")
fig2 = px.pie(by_status, names="Status", values="Students", hole=0.4, title= "Student Status")
c2.plotly_chart(fig2)

c3,c4 = st.columns(2)

by_city = (
    filtered.groupby("City")["Performance Score"].mean().round(1).reset_index()
    .sort_values("Performance Score")
)
fig3 = px.bar(by_city, x="Performance Score", y="City", orientation="h", title="Average Performance Score By City")
c3.plotly_chart(fig3)

monthly = (
    filtered.assign(Month=filtered["Reg Date"].dt.to_period("M").dt.to_timestamp())
    .groupby("Month").size().reset_index(name="Registrations")
)
fig4 = px.line(monthly, x="Month", y="Registrations", title="Registrations Over Time")
c4.plotly_chart(fig4)

c5,c6 = st.columns(2)

fig5 = px.histogram(filtered, x="Performance Score", nbins=20, title = "Performance Score Distribution")
c5.plotly_chart(fig5)

revenue = filtered.groupby(["Track", "Learning Mode"])["Training Cost"].sum().reset_index()
fig6 = px.bar(revenue, x="Track", y="Training Cost", color = "Learning Mode", barmode="group", title= "Revenue By Track & Learning Mode")
c6.plotly_chart(fig6)

with st.expander("View Data"):
    st.dataframe(filtered, hide_index = True)
    
