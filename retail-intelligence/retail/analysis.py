"""Clean UCI-format retail transactions and calculate honest sales metrics."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DATA = ROOT / "data" / "sample" / "retail_sample.csv"
REAL_DATA = ROOT / "data" / "raw" / "Online Retail.xlsx"
REQUIRED_COLUMNS = {
    "InvoiceNo", "StockCode", "Description", "Quantity",
    "InvoiceDate", "UnitPrice", "CustomerID", "Country",
}


def choose_data_path() -> Path:
    """Use genuine data if downloaded; otherwise use the labelled practice sample."""
    return REAL_DATA if REAL_DATA.exists() else SAMPLE_DATA


def read_transactions(path: Path | None = None) -> pd.DataFrame:
    """Read a CSV or Excel file without silently changing invoice IDs to numbers."""
    path = Path(path) if path else choose_data_path()
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    if path.suffix.lower() == ".csv":
        frame = pd.read_csv(path, dtype={"InvoiceNo": "string", "StockCode": "string", "CustomerID": "string"})
    elif path.suffix.lower() in {".xlsx", ".xls"}:
        frame = pd.read_excel(path, dtype={"InvoiceNo": "string", "StockCode": "string", "CustomerID": "string"})
    else:
        raise ValueError("The dataset must be a .csv or .xlsx file")
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return frame


def clean_sales(raw: pd.DataFrame) -> pd.DataFrame:
    """Keep only positive-price, positive-quantity, non-cancelled sale lines."""
    missing = REQUIRED_COLUMNS.difference(raw.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    frame = raw.copy()
    frame["InvoiceNo"] = frame["InvoiceNo"].astype("string").str.strip()
    frame["CustomerID"] = frame["CustomerID"].astype("string").str.replace(r"\.0$", "", regex=True)
    frame["Quantity"] = pd.to_numeric(frame["Quantity"], errors="coerce")
    frame["UnitPrice"] = pd.to_numeric(frame["UnitPrice"], errors="coerce")
    frame["InvoiceDate"] = pd.to_datetime(frame["InvoiceDate"], errors="coerce")

    good = (
        frame["InvoiceNo"].notna()
        & frame["InvoiceDate"].notna()
        & ~frame["InvoiceNo"].str.upper().str.startswith("C", na=False)
        & frame["Quantity"].gt(0)
        & frame["UnitPrice"].gt(0)
    )
    sales = frame.loc[good].copy()
    sales["LineRevenue"] = (sales["Quantity"] * sales["UnitPrice"]).round(2)
    sales["Month"] = sales["InvoiceDate"].dt.to_period("M").astype(str)
    return sales


def calculate_kpis(sales: pd.DataFrame) -> dict:
    """Return portfolio-friendly KPIs; zero rows are handled safely."""
    revenue = float(sales["LineRevenue"].sum())
    orders = int(sales["InvoiceNo"].nunique())
    return {
        "gross_sales": revenue,
        "orders": orders,
        "units": int(sales["Quantity"].sum()),
        "identified_customers": int(sales["CustomerID"].nunique()),
        "average_order_value": revenue / orders if orders else 0.0,
    }


def monthly_sales(sales: pd.DataFrame) -> pd.DataFrame:
    return sales.groupby("Month", as_index=False)["LineRevenue"].sum().sort_values("Month")


def top_products(sales: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    return (sales.groupby(["StockCode", "Description"], dropna=False, as_index=False)["LineRevenue"]
            .sum().sort_values("LineRevenue", ascending=False).head(limit))
