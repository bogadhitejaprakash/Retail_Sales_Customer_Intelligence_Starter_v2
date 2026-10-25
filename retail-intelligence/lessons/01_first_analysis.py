"""Lesson 1: A beginner-friendly walk through a retail transaction file."""

from pathlib import Path

import pandas as pd


# __file__ means this script; parents[1] points to the project folder.
project_folder = Path(__file__).resolve().parents[1]
csv_file = project_folder / "data" / "sample" / "retail_sample.csv"

# read_csv turns a CSV (comma-separated values) file into a DataFrame (table).
sales = pd.read_csv(csv_file, dtype={"InvoiceNo": "string"})

print("\nLESSON 1 — PRACTICE DATA (NOT REAL BUSINESS SALES)")
print("\nFirst five rows:")
print(sales.head())

# Shape: (number of rows, number of columns).
print("\nRows and columns:", sales.shape)
print("\nColumn names:", list(sales.columns))

# A *line* is one product on an invoice; an invoice can contain many lines.
# A cancellation begins with 'C'. We exclude those and invalid free/negative lines.
valid_lines = (
    ~sales["InvoiceNo"].str.upper().str.startswith("C", na=False)
    & sales["Quantity"].gt(0)
    & sales["UnitPrice"].gt(0)
)
completed_sales = sales.loc[valid_lines].copy()

# Multiply the quantity of each product by its price per unit (GBP).
completed_sales["LineRevenue"] = completed_sales["Quantity"] * completed_sales["UnitPrice"]
total = completed_sales["LineRevenue"].sum()

print("\nClean completed-sales lines:", len(completed_sales))
print(f"Gross completed-sales value: £{total:,.2f}")
print("Number of unique completed invoices:", completed_sales["InvoiceNo"].nunique())
print("\nRevenue for the first five valid lines:")
print(completed_sales[["InvoiceNo", "Description", "Quantity", "UnitPrice", "LineRevenue"]].head())

# YOUR TURN:
# 1. Replace the final .head() above with .head(10).
# 2. Add: print(completed_sales[completed_sales["Country"] == "United Kingdom"])
# 3. Explain in your own words why a cancellation is not a new sale.
