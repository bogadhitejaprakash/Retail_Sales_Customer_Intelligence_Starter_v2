"""Simple portfolio dashboard: works with practice data or the real UCI file."""

import streamlit as st

from retail.analysis import (
    REAL_DATA, calculate_kpis, choose_data_path, clean_sales,
    monthly_sales, read_transactions, top_products,
)

st.set_page_config(page_title="Retail Intelligence", page_icon="🛍️", layout="wide")
st.title("🛍️ Retail Sales & Customer Intelligence")
st.caption("An educational portfolio project by Bogadhi Teja Prakash")

source_path = choose_data_path()
if source_path == REAL_DATA:
    st.success("Source: UCI Online Retail — genuine historical UK-based retailer transactions, 2010–2011. NOT live.")
else:
    st.warning("Source: FICTIONAL PRACTICE DATA. Download UCI Online Retail.xlsx into data/raw/ for genuine analysis.")


@st.cache_data(show_spinner="Reading retail transactions...")
def load_dashboard_data(path_string: str):
    return clean_sales(read_transactions(path_string))


all_sales = load_dashboard_data(str(source_path))
countries = sorted(all_sales["Country"].dropna().astype(str).unique().tolist())
country = st.selectbox("Filter by country", ["All countries"] + countries)
sales = all_sales if country == "All countries" else all_sales.loc[all_sales["Country"] == country]

kpi = calculate_kpis(sales)
one, two, three, four = st.columns(4)
one.metric("Gross completed sales", f"£{kpi['gross_sales']:,.2f}")
two.metric("Completed invoices", f"{kpi['orders']:,}")
three.metric("Identified customers", f"{kpi['identified_customers']:,}")
four.metric("Avg. order value", f"£{kpi['average_order_value']:,.2f}")

st.subheader("Monthly completed-sales value")
st.line_chart(monthly_sales(sales).set_index("Month"), y="LineRevenue")
st.subheader("Top products by completed-sales value")
products = top_products(sales, 10)
st.bar_chart(products.set_index("Description")["LineRevenue"], horizontal=True)
with st.expander("View the cleaned sales rows"):
    st.dataframe(sales, use_container_width=True)

st.caption("Metric: positive-price, positive-quantity invoice lines excluding cancellations; not net revenue or profit.")
st.markdown("Dataset attribution: Chen, D. (2015), *Online Retail*, UCI Machine Learning Repository (CC BY 4.0). https://doi.org/10.24432/C5BW33")
