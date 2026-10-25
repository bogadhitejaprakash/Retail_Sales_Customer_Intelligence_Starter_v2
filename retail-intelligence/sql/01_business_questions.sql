-- Lesson 3: Run these queries against retail_sales.sqlite3 in a SQLite tool.
-- Sales lines here have already excluded cancellations and nonpositive values.

-- Q1: How much gross completed-sales value did the company make?
SELECT ROUND(SUM(LineRevenue), 2) AS gross_sales_gbp
FROM sales_lines;

-- Q2: How many distinct orders were completed?
SELECT COUNT(DISTINCT InvoiceNo) AS completed_orders
FROM sales_lines;

-- Q3: What are the five biggest products by sales value?
SELECT StockCode, Description, ROUND(SUM(LineRevenue), 2) AS gross_sales_gbp
FROM sales_lines
GROUP BY StockCode, Description
ORDER BY gross_sales_gbp DESC
LIMIT 5;

-- Q4: What is the monthly trend?
SELECT Month, ROUND(SUM(LineRevenue), 2) AS gross_sales_gbp
FROM sales_lines
GROUP BY Month
ORDER BY Month;
