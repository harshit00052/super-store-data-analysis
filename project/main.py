import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from numpy._core.defchararray import title
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / "dataset" / "cleaned_data.csv"
df = pd.read_csv(DATA_PATH)

df['order_date'] = pd.to_datetime(df['order_date'])

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.write("")
st.write("")

BASE_DIR = Path(__file__).resolve().parent
logo = Image.open(BASE_DIR / "logo.png")

st.set_page_config(page_title="e-commerce data analysis", layout="wide", page_icon=logo)


col19, col20 = st.columns([0.1, 0.9], vertical_alignment="center")
with col19:
    st.image(logo, width='stretch')
with col20:
    st.header("E-Commerce Sales Dashboard")

year_list = df['year'].unique().tolist()
tempYear = st.multiselect("YEAR ", year_list)

month_list = df['month'].unique().tolist()
temp_Month = st.multiselect("MONTH ", month_list)

col2, col4 = st.columns(2)
with col2:
    quarter_list = df['year_quarter'].unique().tolist()
    temp_quarter = st.multiselect("QUARTER ", quarter_list)

with col4:
    region_list = df['region'].unique().tolist()
    temp_region = st.multiselect("REGION ", region_list)


col5, col6 = st.columns(2)
with col5:
    product_category_list = df['product_category'].unique().tolist()
    product_cat = st.multiselect("PRODUCT CATAGORY ", product_category_list)

with col6:
    payment_method_list = df['payment_method'].unique().tolist()
    payment_mtd = st.multiselect("PAYMENT METHOD ", payment_method_list)

btn = st.button('FIND')


if(btn):
    if not tempYear:
        tempYear = year_list

    if not temp_quarter:
        temp_quarter = quarter_list

    if not temp_Month:
        temp_Month = month_list

    if not product_cat:
        product_cat = product_category_list

    if not temp_region:
        temp_region = region_list

    if not payment_mtd:
       payment_mtd = payment_method_list

df = df[(df['year'].isin(tempYear))& (df['year_quarter'].isin(temp_quarter)) &(df['month'].isin(temp_Month)) & (df['region'].isin(temp_region)) & (df['product_category'].isin(product_cat)) & (df['payment_method'].isin(payment_mtd))]
st.write("")

col7, col8, col9, col10 , col11, col12= st.columns(6)
with col7:
    st.metric("Total Revenue", f"₹{round(df['revenue'].sum(), 2)}")

with col8:
    st.metric("Total Order", f"{df['order_id'].count()}")

with col9:
    st.metric("Avg Rating", f"{round(df['customer_rating'].mean(),2)}")

with col10:
    st.metric("Avg Delivery Days", f"{round(df['delivery_days'].mean(),2)}")

with col11:
    st.metric("Total Customers", f"{df['customer_id'].nunique()}")

with col12:
    st.metric("Total Quantity Sold", f"{df['quantity'].sum()}")


col13, col14 = st.columns(2)
with col13:
    temp = df.pivot_table(columns=['product_category'], index=['month', 'month_num'], values='revenue' ,aggfunc='sum').reset_index().sort_values(by='month_num')
    fig = go.Figure()
    for cols in temp.columns[2:]:
        fig.add_trace(go.Scatter(y=temp[cols], x=temp['month'], name=cols))

    fig.update_layout(title='monthly sale of each category', xaxis_title='month', yaxis_title='sale')
    st.plotly_chart(fig, use_container_width=True)

with col14:
    temp = df.pivot_table(index=['month', 'month_num'], columns='year', values='revenue', aggfunc='sum').reset_index().sort_values(by='month_num')
    fig = go.Figure()
    for col in temp.columns[2:]:
        fig.add_trace(go.Scatter(x=temp['month'], y=temp[col], name=col))
    fig.update_layout(title="Revenue Trend", xaxis_title="Month", yaxis_title="Year")
    st.plotly_chart(fig, use_container_width=True)


col15, col16 = st.columns(2)
with col15:
    temp = df.pivot_table(columns=['region'], index=['month', 'month_num'], values='revenue' ,aggfunc='sum').reset_index().sort_values(by='month_num')
    fig = go.Figure()
    for col in temp.columns[2:]:
        fig.add_trace(go.Bar(x=temp['month'], y=temp[col], name=col))
    fig.update_layout(title="Region Wise Analysis", xaxis_title="Months", yaxis_title="Revenue")
    st.plotly_chart(fig, use_container_width=True)

with col16:
    temp = df.groupby('payment_method')['order_id'].size().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=temp['payment_method'], values=temp['order_id']))
    fig.update_layout(title="Payment Method Distribution")
    st.plotly_chart(fig, use_container_width=True)


col17, col18 = st.columns(2)
with col17:
    st.subheader("📄 Top 10 Customers by Revenue")
    temp = df.groupby('customer_id')['revenue'].sum().reset_index().sort_values(by='revenue', ascending=False).head(10)
    st.dataframe(temp, use_container_width=True, hide_index=True)

with col18:
    st.subheader("📄  Top Products-Categories")
    temp = df.groupby('product_category').agg({'quantity':'sum', 'revenue':'sum'}).reset_index().sort_values(by='revenue', ascending=False)
    st.dataframe(temp, use_container_width=True, hide_index=True)


st.subheader("📄 Raw Dataset")
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)