
import pandas as pd
import matplotlib.pyplot as plt

# Load the real retail dataset
df = pd.read_excel("data/raw/Online Retail.xlsx")

# Display dataset information
print("Dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nColumn names:")
print(df.columns.tolist())
print("\nMissing values in each column:")
print(df.isnull().sum())
print("\nMissing values percentage:")
print((df.isnull().sum() / len(df) * 100).round(2))
print("\nDuplicate rows:")
print(df.duplicated().sum())
print("\nFirst 10 duplicate records:")
print(df[df.duplicated(keep=False)].head(10).to_string(index=False))
# Create a copy of the original dataset
df_clean = df.copy()

# Remove exact duplicate rows
df_clean = df_clean.drop_duplicates()

# Compare before and after
print("\nOriginal rows:", len(df))
print("Cleaned rows:", len(df_clean))
print("Removed duplicates:", len(df) - len(df_clean))
# Check cancelled invoices
cancelled = df_clean[
    df_clean["InvoiceNo"].astype(str).str.startswith("C")
]

print("\nCancelled transaction rows:", len(cancelled))

# Check negative and zero quantities
print("Negative quantities:",
      (df_clean["Quantity"] < 0).sum())

print("Zero quantities:",
      (df_clean["Quantity"] == 0).sum())
# Find negative quantities without a cancellation code
negative_without_c = df_clean[
    (df_clean["Quantity"] < 0) &
    (~df_clean["InvoiceNo"].astype(str).str.startswith("C"))
]

print("\nNegative quantities without C:")
print(len(negative_without_c))

print("\nFirst 10 examples:")
print(negative_without_c.head(10).to_string(index=False))
# Keep only valid sales transactions
df_sales = df_clean[
    (df_clean["Quantity"] > 0) &
    (df_clean["UnitPrice"] > 0) &
    (~df_clean["InvoiceNo"].astype(str).str.startswith("C"))
].copy()

print("\nRows after sales filtering:", len(df_sales))
print("Rows excluded:", len(df_clean) - len(df_sales))
# Calculate revenue for each sales row
df_sales["Revenue"] = (
    df_sales["Quantity"] * df_sales["UnitPrice"]
)

# Calculate total sales revenue
total_revenue = df_sales["Revenue"].sum()

print("\nTotal Sales Revenue:")
print(f"£{total_revenue:,.2f}")
# Count unique customer orders
total_orders = df_sales["InvoiceNo"].nunique()

# Calculate average order value
average_order_value = total_revenue / total_orders

print("\nTotal Orders:")
print(f"{total_orders:,}")

print("\nAverage Order Value:")
print(f"£{average_order_value:,.2f}")
# Count unique customers
total_customers = df_sales["CustomerID"].nunique()

# Count sales rows without customer IDs
missing_customer_ids = df_sales["CustomerID"].isna().sum()

print("\nTotal Unique Customers:")
print(f"{total_customers:,}")

print("\nSales Rows Without Customer ID:")
print(f"{missing_customer_ids:,}")
# Find the top 10 customers by total spending
top_customers = (
    df_sales.dropna(subset=["CustomerID"])
    .groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Customers by Spending:")
print(top_customers.to_string())
# Calculate revenue by country
country_revenue = (
    df_sales.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Countries by Revenue:")
print(country_revenue.to_string())
# Create a bar chart of the top 10 countries
plt.figure(figsize=(12, 6))

country_revenue.sort_values().plot(kind="barh")

plt.title("Top 10 Countries by Sales Revenue")
plt.xlabel("Sales Revenue (£)")
plt.ylabel("Country")

plt.tight_layout()
plt.savefig("docs/top_10_countries.png", dpi=300, bbox_inches="tight")
plt.show()
# Convert invoice dates into monthly periods
df_sales["Month"] = (
    pd.to_datetime(df_sales["InvoiceDate"])
    .dt.to_period("M")
)

# Calculate total revenue for each month
monthly_revenue = (
    df_sales.groupby("Month")["Revenue"]
    .sum()
    .sort_index()
)

print("\nMonthly Sales Revenue:")
print(monthly_revenue.to_string())
# Create monthly sales trend chart
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_revenue.index.astype(str),
    monthly_revenue.values,
    marker="o"
)

plt.title("Monthly Sales Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Sales Revenue (£)")

plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save the chart
plt.savefig(
    "docs/monthly_sales_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# Revenue for November 2011
november_revenue = monthly_revenue.loc["2011-11"]

print(
    f"\nNovember 2011 Revenue: £{november_revenue:,.2f}"
)
# Compare October and November revenue
october_revenue = monthly_revenue.loc["2011-10"]
november_revenue = monthly_revenue.loc["2011-11"]

# Calculate percentage growth
growth = (
    (november_revenue - october_revenue)
    / october_revenue
) * 100

print(f"October Revenue: £{october_revenue:,.2f}")
print(f"November Revenue: £{november_revenue:,.2f}")
print(f"Revenue Growth: {growth:.2f}%")
# LESSON 6: TOP 10 PRODUCTS BY REVENUE

top_products = (
    df_sales.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Products by Revenue:")
print(top_products.to_string())

# Exclude postage from product analysis
df_products = df_sales[
    ~df_sales["Description"]
    .fillna("")
    .str.contains("POSTAGE", case=False)
]

# Top 10 products by revenue
top_products = (
    df_products.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Products (Excluding Postage):")
print(top_products.to_string())

# Top 10 Products Revenue Chart
plt.figure(figsize=(12, 7))

top_products.sort_values().plot(
    kind="barh",
    color="steelblue"
)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue (£)")
plt.ylabel("Product")

plt.tight_layout()

# Save chart
plt.savefig(
    "docs/top_10_products.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# LESSON 7: TOP PRODUCTS BY QUANTITY

top_quantity = (
    df_products.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Products by Quantity:")
print(top_quantity.to_string())

# Investigate the top-selling product
birdie_sales = df_products[
    df_products["Description"] == "PAPER CRAFT , LITTLE BIRDIE"
]

print("\nPAPER CRAFT Transaction Details:")

print(
    birdie_sales[
        ["InvoiceNo", "InvoiceDate", "Quantity", "UnitPrice", "Revenue"]
    ].to_string(index=False)
)

birdie_sales = df_products[
    df_products["Description"] == "PAPER CRAFT , LITTLE BIRDIE"
]

print("\nTransaction Details:")
print(birdie_sales[["InvoiceNo", "Quantity", "UnitPrice"]].to_string(index=False))
# Check all records related to invoice 581483
invoice_check = df_clean[
    df_clean["InvoiceNo"]
    .astype(str)
    .str.contains("581483")
]

print("\nInvoice 581483 Details:")
print(
    invoice_check[
        ["InvoiceNo", "Description", "Quantity", "UnitPrice"]
    ].to_string(index=False)
)

# Exclude the unusual invoice for comparison
df_without_outlier = df_products[
    df_products["InvoiceNo"].astype(str) != "581483"
]

# Recalculate top products by quantity
top_quantity_clean = (
    df_without_outlier.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Products Without Outlier:")
print(top_quantity_clean.to_string())

# LESSON 8: CUSTOMER PURCHASE FREQUENCY

customer_orders = (
    df_sales.dropna(subset=["CustomerID"])
    .groupby("CustomerID")["InvoiceNo"]
    .nunique()
)

repeat_customers = (customer_orders > 1).sum()
one_time_customers = (customer_orders == 1).sum()

print("\nCustomer Purchase Analysis:")
print(f"Repeat Customers: {repeat_customers}")
print(f"One-Time Customers: {one_time_customers}")

# Calculate repeat customer rate
total_customers = len(customer_orders)

repeat_rate = (
    repeat_customers / total_customers
) * 100

print(f"\nTotal Customers: {total_customers}")
print(f"Repeat Customer Rate: {repeat_rate:.2f}%")

# LESSON 9: RFM CUSTOMER ANALYSIS

# Keep only sales with valid customer IDs
rfm_data = df_sales.dropna(
    subset=["CustomerID"]
).copy()

# Ensure invoice dates are datetime values
rfm_data["InvoiceDate"] = pd.to_datetime(
    rfm_data["InvoiceDate"]
)

print("\nRFM Dataset:")
print("Rows:", len(rfm_data))
print("Customers:", rfm_data["CustomerID"].nunique())

# Set analysis date one day after last transaction
analysis_date = (
    rfm_data["InvoiceDate"].max()
    + pd.Timedelta(days=1)
)

# Find each customer's most recent purchase
customer_last_purchase = (
    rfm_data.groupby("CustomerID")["InvoiceDate"]
    .max()
)

# Calculate days since last purchase
recency = (
    analysis_date - customer_last_purchase
).dt.days

print("\nCustomer Recency:")
print(recency.head(10))

# RFM: FREQUENCY ANALYSIS

frequency = (
    rfm_data.groupby("CustomerID")["InvoiceNo"]
    .nunique()
)

print("\nCustomer Frequency:")
print(frequency.head(10))

# RFM: MONETARY ANALYSIS

monetary = (
    rfm_data.groupby("CustomerID")["Revenue"]
    .sum()
)

print("\nCustomer Monetary Value:")
print(monetary.head(10))

# Combine RFM metrics into one table
rfm = pd.DataFrame({
    "Recency": recency,
    "Frequency": frequency,
    "Monetary": monetary
})

print("\nComplete RFM Table:")
print(rfm.head(10))

print("\nRFM Table Shape:")
print(rfm.shape)

# LESSON 10: RFM SCORING

# Give customers a Recency score from 1 to 5
rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    q=5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

print("\nRFM Recency Scores:")
print(rfm[["Recency", "R_Score"]].head(10))


# ==========================================
# LESSON 10: FREQUENCY AND MONETARY SCORING
# ==========================================

# Higher frequency = higher score
rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    q=5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# Higher spending = higher score
rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    q=5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# Total RFM score: minimum 3, maximum 15
rfm["RFM_Total"] = (
    rfm["R_Score"]
    + rfm["F_Score"]
    + rfm["M_Score"]
)

print("\nComplete RFM Scores:")
print(rfm.head(10))


# ==========================================
# LESSON 11: CUSTOMER SEGMENTATION
# ==========================================

def customer_segment(row):
    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    elif r >= 3 and f >= 4:
        return "Loyal Customers"

    elif r <= 2 and m >= 4:
        return "At Risk High Value"

    elif r <= 2 and f <= 2:
        return "Inactive"

    elif r >= 4 and f <= 2:
        return "New or Promising"

    else:
        return "Regular Customers"


rfm["Segment"] = rfm.apply(
    customer_segment,
    axis=1
)

segment_counts = rfm["Segment"].value_counts()

print("\nCustomer Segments:")
print(segment_counts.to_string())


# ==========================================
# LESSON 12: EXPORT ANALYSIS RESULTS
# ==========================================

from pathlib import Path
import sqlite3

# Create folders if they don't exist
Path("data/processed").mkdir(
    parents=True,
    exist_ok=True
)
Path("docs").mkdir(exist_ok=True)

# Save RFM customer table
rfm_export = rfm.reset_index()

rfm_export.to_csv(
    "data/processed/customer_rfm_segments.csv",
    index=False
)

# Save monthly revenue
monthly_export = monthly_revenue.rename_axis(
    "Month"
).reset_index()

monthly_export["Month"] = (
    monthly_export["Month"].astype(str)
)

monthly_export.to_csv(
    "data/processed/monthly_revenue.csv",
    index=False
)

# Save product revenue
top_products.rename_axis(
    "Description"
).reset_index().to_csv(
    "data/processed/top_products.csv",
    index=False
)

print("\nCSV exports completed!")


# ==========================================
# LESSON 13: SQL DATABASE AND QUERIES
# ==========================================

database_path = (
    "data/processed/retail_intelligence.db"
)

with sqlite3.connect(database_path) as conn:

    # Prepare sales data for SQL
    sql_sales = df_sales.copy()

    sql_sales["InvoiceDate"] = (
        sql_sales["InvoiceDate"].astype(str)
    )

    sql_sales["Month"] = (
        sql_sales["Month"].astype(str)
    )

    # Create SQL sales table
    sql_sales.to_sql(
        "sales",
        conn,
        if_exists="replace",
        index=False,
        chunksize=5000
    )

    # Create SQL customer table
    rfm_export.to_sql(
        "customer_segments",
        conn,
        if_exists="replace",
        index=False
    )

    # SQL Query 1: Top countries
    sql_countries = pd.read_sql_query(
        """
        SELECT
            Country,
            ROUND(SUM(Revenue), 2) AS TotalRevenue
        FROM sales
        GROUP BY Country
        ORDER BY TotalRevenue DESC
        LIMIT 10
        """,
        conn
    )

    # SQL Query 2: Monthly revenue
    sql_monthly = pd.read_sql_query(
        """
        SELECT
            Month,
            ROUND(SUM(Revenue), 2) AS TotalRevenue
        FROM sales
        GROUP BY Month
        ORDER BY Month
        """,
        conn
    )

    # SQL Query 3: Customer segments
    sql_segments = pd.read_sql_query(
        """
        SELECT
            Segment,
            COUNT(*) AS CustomerCount,
            ROUND(SUM(Monetary), 2) AS TotalSpend
        FROM customer_segments
        GROUP BY Segment
        ORDER BY TotalSpend DESC
        """,
        conn
    )

sql_countries.to_csv(
    "data/processed/sql_countries.csv",
    index=False
)

sql_monthly.to_csv(
    "data/processed/sql_monthly.csv",
    index=False
)

sql_segments.to_csv(
    "data/processed/sql_segments.csv",
    index=False
)

print("\nSQL Analysis Completed!")
print(sql_segments.to_string(index=False))


# ==========================================
# LESSON 14: CUSTOMER SEGMENT CHART
# ==========================================

plt.figure(figsize=(11, 6))

segment_counts.sort_values().plot(
    kind="barh",
    color="steelblue"
)

plt.title("Customer Segmentation")
plt.xlabel("Number of Customers")
plt.ylabel("Customer Segment")
plt.tight_layout()

plt.savefig(
    "docs/customer_segments.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ==========================================
# LESSON 14: EXECUTIVE DASHBOARD
# ==========================================

# Four charts in one dashboard
fig, axes = plt.subplots(
    2, 2,
    figsize=(17, 12)
)

# Chart 1: Monthly revenue
axes[0, 0].plot(
    monthly_revenue.index.astype(str),
    monthly_revenue.values,
    marker="o"
)

axes[0, 0].set_title("Monthly Sales Revenue")
axes[0, 0].set_ylabel("Revenue (£)")
axes[0, 0].tick_params(
    axis="x",
    rotation=45
)

# Chart 2: Top countries
country_revenue = (
    df_sales.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

country_revenue.sort_values().plot(
    kind="barh",
    ax=axes[0, 1],
    color="steelblue"
)

axes[0, 1].set_title("Top 10 Countries")
axes[0, 1].set_xlabel("Revenue (£)")

# Chart 3: Top products
top_products.sort_values().plot(
    kind="barh",
    ax=axes[1, 0],
    color="seagreen"
)

axes[1, 0].set_title("Top 10 Products by Revenue")
axes[1, 0].set_xlabel("Revenue (£)")

# Chart 4: Customer segments
segment_counts.sort_values().plot(
    kind="barh",
    ax=axes[1, 1],
    color="darkorange"
)

axes[1, 1].set_title("Customer Segments")
axes[1, 1].set_xlabel("Number of Customers")

fig.suptitle(
    "Retail Sales & Customer Intelligence Dashboard",
    fontsize=18
)

plt.tight_layout(
    rect=[0, 0, 1, 0.96]
)

plt.savefig(
    "docs/retail_dashboard.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nDashboard saved successfully!")


# ==========================================
# LESSON 15: BUSINESS INSIGHTS
# ==========================================

total_revenue = df_sales["Revenue"].sum()
total_orders = df_sales["InvoiceNo"].nunique()
total_customers = rfm.shape[0]

average_order_value = (
    total_revenue / total_orders
)

repeat_customers = (
    rfm["Frequency"] > 1
).sum()

repeat_rate = (
    repeat_customers / total_customers
) * 100

best_month = monthly_revenue.idxmax()
best_country = country_revenue.idxmax()
best_product = top_products.idxmax()

insights = f"""
RETAIL SALES & CUSTOMER INTELLIGENCE
====================================

Total Revenue: £{total_revenue:,.2f}
Total Orders: {total_orders:,}
Identified Customers: {total_customers:,}
Average Order Value: £{average_order_value:,.2f}

Best Revenue Month: {best_month}
Top Country: {best_country}
Top Product: {best_product}

Repeat Customer Rate: {repeat_rate:.2f}%

CUSTOMER SEGMENTS
-----------------
{segment_counts.to_string()}

BUSINESS RECOMMENDATIONS
------------------------
1. Prepare inventory for high-revenue months.
2. Monitor best-performing products.
3. Reward Champions with loyalty offers.
4. Re-engage At Risk High Value customers.
5. Investigate unusually large transactions.

ANALYSIS LIMITATIONS
--------------------
- Revenue uses positive, non-cancelled sales.
- Customer analysis excludes missing CustomerID.
- RFM scores are approximate quintiles.
- Tied values may receive different scores.
- Segments are heuristic, not validated labels.
- Unusual transactions require investigation.
"""

Path("docs/business_insights.txt").write_text(
    insights,
    encoding="utf-8"
)

print(insights)
print("\nPROJECT COMPLETED SUCCESSFULLY!")
