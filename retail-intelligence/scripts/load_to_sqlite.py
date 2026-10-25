"""Lesson 3 preview: create a local SQL database from cleaned sales."""

import sqlite3

from retail.analysis import ROOT, calculate_kpis, choose_data_path, clean_sales, read_transactions


def main() -> None:
    source = choose_data_path()
    sales = clean_sales(read_transactions(source))
    db_file = ROOT / "retail_sales.sqlite3"
    with sqlite3.connect(db_file) as connection:
        sales.to_sql("sales_lines", connection, if_exists="replace", index=False)
        connection.execute("CREATE INDEX IF NOT EXISTS idx_sales_invoice ON sales_lines (InvoiceNo)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales_lines (InvoiceDate)")
    print(f"Loaded {len(sales):,} completed-sales lines from {source.name}")
    print(f"Created database: {db_file}")
    print(f"Gross completed-sales value: £{calculate_kpis(sales)['gross_sales']:,.2f}")
    print("Next: open sql/01_business_questions.sql and run its queries.")


if __name__ == "__main__":
    main()
