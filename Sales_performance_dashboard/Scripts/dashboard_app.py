# -------------------------------------------------------------
# 📊 Final Sales Performance Dashboard – Dark Themed Version
# -------------------------------------------------------------
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# -------------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------------
st.set_page_config(
    page_title="Sales Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# DARK THEME STYLING
# -------------------------------------------------------------
st.markdown("""
<style>
/* Global App Background */
.stApp {
    background-color: #000000;
    color: #FFFFFF;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #111111;
    color: #FFFFFF;
}

/* Metric Boxes */
div[data-testid="stMetric"] {
    background-color: #1E1E1E;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0px 0px 5px rgba(255,255,255,0.1);
}

/* Metric Labels */
div[data-testid="stMetricLabel"] {
    color: #CCCCCC;
}

/* Metric Values */
div[data-testid="stMetricValue"] {
    color: #00FFAA;
}

/* Chart Titles */
h3, h4, h5, h6 {
    color: #00B4D8;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------------
try:
    conn = sqlite3.connect('data/sales.db')
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# -------------------------------------------------------------
# HEADER / TITLE SECTION
# -------------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: #00FFAA;'>📊 Sales Performance Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #CCCCCC;'>Analyze sales, profit, and performance trends across regions and categories</h4>", unsafe_allow_html=True)
st.markdown("---")

# -------------------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------------------
st.sidebar.header("🔍 Filter Options")

regions = df['Region'].unique()
categories = df['Category'].unique()
years = sorted(df['Year'].unique())

selected_region = st.sidebar.selectbox("Select Region", ['All'] + list(regions))
selected_category = st.sidebar.selectbox("Select Category", ['All'] + list(categories))
selected_year = st.sidebar.selectbox("Select Year", ['All'] + [str(y) for y in years])

# Filter logic
filtered_df = df.copy()

if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]
if selected_year != 'All':
    filtered_df = filtered_df[filtered_df['Year'] == int(selected_year)]

# -------------------------------------------------------------
# KPI SECTION
# -------------------------------------------------------------
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
avg_margin = filtered_df['Profit Margin (%)'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("🏦 Total Profit", f"${total_profit:,.2f}")
col3.metric("📈 Avg Profit Margin", f"{avg_margin:.2f}%")

st.markdown("---")

# -------------------------------------------------------------
# CHARTS SECTION
# -------------------------------------------------------------
# 1️⃣ Sales by Region
st.subheader("🌍 Sales by Region")
region_sales = filtered_df.groupby('Region', as_index=False)['Sales'].sum().sort_values(by='Sales', ascending=False)
fig_region = px.bar(region_sales, x='Region', y='Sales', color='Region', title="Total Sales by Region", color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig_region, use_container_width=True)

# 2️⃣ Sales by Category
st.subheader("📦 Sales by Product Category")
category_sales = filtered_df.groupby('Category', as_index=False)[['Sales', 'Profit']].sum().sort_values(by='Sales', ascending=False)
fig_category = px.bar(category_sales, x='Category', y='Sales', color='Category', title="Sales by Category", color_discrete_sequence=px.colors.sequential.Tealgrn)
st.plotly_chart(fig_category, use_container_width=True)

# 3️⃣ Monthly Trend
st.subheader("📅 Monthly Sales Trend")
monthly_sales = filtered_df.groupby(['Year', 'Month'], as_index=False)['Sales'].sum()
month_order = ['January','February','March','April','May','June','July','August','September','October','November','December']
monthly_sales['Month'] = pd.Categorical(monthly_sales['Month'], categories=month_order, ordered=True)
monthly_sales = monthly_sales.sort_values(['Year', 'Month'])
fig_month = px.line(monthly_sales, x='Month', y='Sales', color='Year', markers=True, title="Monthly Sales Trend by Year")
st.plotly_chart(fig_month, use_container_width=True)

# 4️⃣ Profit by Sub-Category
st.subheader("💹 Profit by Sub-Category")
sub_profit = filtered_df.groupby('Sub-Category', as_index=False)['Profit'].sum().sort_values(by='Profit', ascending=False)
fig_sub = px.bar(sub_profit, y='Sub-Category', x='Profit', orientation='h', color='Profit', title="Profit by Product Sub-Category", color_continuous_scale='RdYlGn')
st.plotly_chart(fig_sub, use_container_width=True)

# 5️⃣ Top 10 Products
st.subheader("🏆 Top 10 Products by Sales")
top_products = filtered_df.groupby('Product Name', as_index=False)['Sales'].sum().nlargest(10, 'Sales')
fig_top = px.bar(top_products, x='Sales', y='Product Name', orientation='h', color='Sales', title="Top 10 Products by Sales", color_continuous_scale='Blues')
st.plotly_chart(fig_top, use_container_width=True)

st.markdown("---")

# -------------------------------------------------------------
# DOWNLOAD BUTTON
# -------------------------------------------------------------
st.subheader("📥 Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download as CSV",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv",
    help="Download the currently filtered dataset"
)

# -------------------------------------------------------------
# FOOTER / ABOUT SECTION
# -------------------------------------------------------------
st.markdown("---")
st.markdown("#### 📘 About this Dashboard")
st.info("""
This **Sales Performance Dashboard** was built using **Python, Pandas, Plotly, SQLite, and Streamlit**.  
It allows users to interactively explore sales data, analyze profit trends, and download filtered insights.  
Created by **Vedant Rane (Data Analyst / Engineer)** 💼
""")
