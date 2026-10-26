from pathlib import Path
import pandas as pd

# Find the project folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Input and output locations
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "data" / "dashboard"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Reading the retail dataset...")

# Load the original dataset
df = pd.read_excel(INPUT_FILE)

# Remove duplicate records
df = df.drop_duplicates()

# Remove cancelled transactions and invalid sales
df = df[
    (~df["InvoiceNo"].astype(str).str.startswith("C"))
    & (df["Quantity"] > 0)
    & (df["UnitPrice"] > 0)
].copy()

# Calculate revenue
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# Extract month
df["Month"] = pd.to_datetime(
    df["InvoiceDate"]
).dt.to_period("M").astype(str)

# Monthly revenue
monthly = (
    df.groupby("Month", as_index=False)
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("InvoiceNo", "nunique"),
    )
)

# Revenue by country
countries = (
    df.groupby("Country", as_index=False)
    .agg(Revenue=("Revenue", "sum"))
    .sort_values("Revenue", ascending=False)
)

# Revenue by product
products = (
    df.groupby("Description", as_index=False)
    .agg(Revenue=("Revenue", "sum"))
    .sort_values("Revenue", ascending=False)
    .head(20)
)

# Overall KPIs
identified = df.dropna(subset=["CustomerID"])
orders = df["InvoiceNo"].nunique()
revenue = df["Revenue"].sum()

kpis = pd.DataFrame([{
    "Revenue": revenue,
    "Orders": orders,
    "Customers": identified["CustomerID"].nunique(),
    "AverageOrderValue": revenue / orders if orders else 0,
}])

# Save aggregated datasets
monthly.to_csv(OUTPUT_DIR / "monthly_sales.csv", index=False)
countries.to_csv(OUTPUT_DIR / "country_sales.csv", index=False)
products.to_csv(OUTPUT_DIR / "top_products.csv", index=False)
kpis.to_csv(OUTPUT_DIR / "kpis.csv", index=False)

print("Dashboard data prepared successfully!")
print(f"Revenue: £{revenue:,.2f}")
print(f"Orders: {orders:,}")
print(f"Customers: {identified['CustomerID'].nunique():,}")