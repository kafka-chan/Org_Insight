import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title = "Customer Intelligance Dashboard", page_icon = ":bar_chart:", layout = "wide")
@st.cache_data
def load_data():
    df = pd.read_excel("ML_Testing.xlsx")
    df["Day_name"] = df["Date"].dt.day_name()
    df["Month"] = df["Date"].dt.month_name()
    return df
df = load_data()

pyear = st.sidebar.multiselect(
    "Select Year",
    options = sorted(df["Year"].unique()),
    default = sorted(df["Year"].unique())[:5]
)
csegment = st.sidebar.multiselect(
    "Select Customer Segment",
    options = df["customer_segment"].unique(),
    default = df["customer_segment"].unique()[:5]
)
mindustry = st.sidebar.multiselect(
    "Select Industry",
    options = df["businessindustrytype"].unique(),
    default = df["businessindustrytype"].unique()[:5]
)

st.title(":bar_chart: Customer intelligence dashboard")
st.markdown("Analyze customer behavior, spending trends, and segment performance interactivily")
df_select = df.query("Year == @pyear and customer_segment == @csegment and businessindustrytype == @mindustry")
total = df_select["Amount"].sum()
unique_segment = df_select["customer_segment"].nunique
avg = df_select["Amount"].mean().round(2)

left_col, mid_col, right_col = st.columns(3)
with left_col:
    st.subheader("💵 Total Revenue")
    st.subheader(f'US $ {total}')

with mid_col:
    st.subheader("Active Segment")
    st.subheader(f"{unique_segment}")
    
with right_col:
    st.subheader("Avg Transaction")
    st.subheader(f"US $ {avg}")

a_col, b_col, c_col = st.columns(3)

total_by_segment = df_select.groupby("customer_segment")["Amount"].sum().sort_values().reset_index()
fig_by_segment = px.bar(
    total_by_segment,
    x = "Amount",
    y = "customer_segment",
    color = "customer_segment",
    title = "Sales by Segment"
)

a_col.plotly_chart(fig_by_segment, use_container_width = True)

total_by_day = df_select.groupby("Day_name")["Amount"].sum().sort_values().reset_index()
day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
total_by_day["Day_name"] = pd.Categorical(total_by_day["Day_name"], categories = day_order, ordered = True)
total_by_day = total_by_day.sort_values("Day_name")
fig_by_day = px.line(
    total_by_day,
    x = "Day_name",
    y = "Amount",
    title = "Weekly Sales Pattern"
)

b_col.plotly_chart(fig_by_day, use_container_width = True)

total_by_industry = df_select.groupby("businessindustrytype")["Amount"].sum().sort_values().reset_index()
fig_by_industry = px.pie(
    total_by_industry, 
    values = "Amount",
    names = "businessindustrytype",
    title = "Revenue Shared by Industry"
)
c_col.plotly_chart(fig_by_industry, use_container_width = True)

st.subheader("📋 Dynamic Data Table")
st.caption("This table updates automatically based on your selected filters.")
st.dataframe(df_select[['Year', 'Month', 'Date', 'customer_segment', 'businessindustrytype',
       'Amount', "Day_name"]], use_container_width = True)

total_by_month = df_select.groupby("Month")["Amount"].sum().sort_values().reset_index()
month_order = ['January','February','March','April','May','June','July','August','September','October','November','December']
total_by_month["Month"] = pd.Categorical(total_by_month["Month"], categories = month_order, ordered = True)
total_by_month = total_by_month.sort_values("Month")
fig_by_month = px.area(
    total_by_month,
    x = "Month",
    y = "Amount",
    title = "Monthly Revenue Trend",
    markers = True
)
st.plotly_chart(fig_by_month, use_container_width = True)

st.markdown("**💡Insight Summary**")
st.write(f"""
- **Total revenue :** US $ {total} across {len(pyear)} years
- **Top-performing segment:** {total_by_segment.sort_values("Amount", ascending = False).iloc[0,0]}.
- **Most Active Day:** {total_by_day.sort_values("Amount", ascending = False).iloc[0,0]}.
- **Leading Industry:** {total_by_industry.sort_values("Amount", ascending = False).iloc[0,0]}
""")
