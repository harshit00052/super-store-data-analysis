import pandas as pd
import streamlit as st

st.set_page_config(page_title="e-commerce data analysis", layout="wide")
df = pd.read_csv('/workspaces/super-store-data-analysis/dataset/cleaned_data.csv')
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
st.header("E-Commerce Sales Dashboard")

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    year_list = df['year'].unique().tolist()
    tempYear = st.selectbox("YEAR ", year_list)
with col2:
    quarter_list = df['year_quarter'].unique().tolist()
    tempYear = st.selectbox("QUARTER ", quarter_list)
with col3:
    month_list = df['month'].unique().tolist()
    tempMonth = st.selectbox("MONTH ", month_list)
with col4:
    region_list = df['region'].unique().tolist()
    tempMonth = st.selectbox("REGION ", region_list)
with col5:
    product_category_list = df['product_category'].unique().tolist()
    product_cat = st.selectbox("PRODUCT CATAGORY ", product_category_list)
with col6:
    payment_method_list = df['payment_method'].unique().tolist()
    payment_mtd = st.selectbox("PAYMENT METHOD ", payment_method_list)


