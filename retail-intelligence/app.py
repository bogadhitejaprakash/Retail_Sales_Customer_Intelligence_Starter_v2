from pathlib import Path

import pandas as pd
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Retail Sales & Customer Intelligence",
    page_icon="📊",
    layout="wide"
)

# Dashboard data location
DATA_DIR = Path(__file__).resolve().parent / "data" / "dashboard"


@st.cache_data
def load_data():
    """Load aggregated retail data."""
    kpis = pd.read_csv(DATA_DIR / "kpis.csv")
    monthly = pd.read_csv(DATA_DIR / "monthly_sales.csv")
    countries = pd.read_csv(DATA_DIR / "country_sales.csv")
    products = pd.read_csv(DATA_DIR / "top_products.csv")

    return kpis, monthly, countries, products


# Load data
try:
    kpis, monthly, countries, products = load_data()
except FileNotFoundError:
    st.error(
        "Dashboard data files are missing. "
        "Run data/dashboard/prepare_dashboard_data.py first."
    )
    st.stop()

# Header
st.title("📊 Retail Sales & Customer Intelligence")
st.caption(
    "Interactive Retail Analytics Dashboard | "
    "Python • Pandas • Streamlit"
)

st.info(
    "Dataset: UCI Online Retail (2010–2011). "
    "Historical transaction data, not live sales."
)

# KPI cards
kpi = kpis.iloc[0]

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"£{kpi['Revenue']/1_000_000:.2f}M")
col2.metric("🛒 Total Orders", f"{int(kpi['Orders']):,}")
col3.metric("👥 Customers", f"{int(kpi['Customers']):,}")
col4.metric(
    "📈 Average Order Value",
    f"£{kpi['AverageOrderValue']:,.2f}"
)

st.divider()

# Monthly revenue chart
st.subheader("📈 Monthly Sales Revenue")

monthly = monthly.sort_values("Month")

st.line_chart(
    monthly.set_index("Month")["Revenue"]
)

st.caption(
    "Note: December 2011 contains incomplete-month data."
)

st.divider()

# Country analysis
st.subheader("🌍 Top 10 Countries by Revenue")

top_countries = countries.head(10)

st.bar_chart(
    top_countries.set_index("Country")["Revenue"],
    horizontal=True
)

st.divider()

# Product analysis
st.subheader("🛍️ Top 10 Products by Revenue")

top_products = products.head(10)

st.bar_chart(
    top_products.set_index("Description")["Revenue"],
    horizontal=True
)

st.divider()

# Business insights
st.subheader("💡 Key Business Insights")

st.markdown(
    """
    - **Revenue:** Approximately £10.64 million in completed sales.
    - **Orders:** 19,960 unique completed invoices.
    - **Customers:** 4,338 identified customers.
    - **Seasonality:** November 2011 recorded the highest monthly revenue.
    - **Geography:** The United Kingdom contributed the largest revenue share.
    - **Customer intelligence:** RFM segmentation can help identify
      valuable and at-risk customers.
    """
)

st.divider()

st.caption(
    "Data preparation: duplicate removal, cancellation exclusion, "
    "positive quantity and price filtering. "
    "Revenue represents completed positive-value sales, "
    "not profit or net revenue."
)

st.markdown(
    "Source: Chen, D. (2015), *Online Retail*, "
    "UCI Machine Learning Repository (CC BY 4.0). "
    "DOI: 10.24432/C5BW33"
)