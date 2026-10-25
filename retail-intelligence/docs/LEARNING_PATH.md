# Your step-by-step learning path

## Stage 1 — Python fundamentals (now)

**Goal:** Read and understand each column, then calculate honest business KPIs.

- [ ] Run `lessons/01_first_analysis.py`.
- [ ] Explain CSV, DataFrame, row, column, quantity, unit price and an invoice.
- [ ] Change `.head(5)` to `.head(10)`.
- [ ] Display only UK rows with a boolean filter.
- [ ] Explain why cancellation/return rows are handled separately.

**Lesson 1 success:** You can explain each line of code without memorising it.

## Stage 2 — Genuine UK retail data

**Goal:** Import UCI data, explore missing customer IDs, invalid prices and cancellation rows. Keep a data-quality log with counts and examples.

- [ ] Download the UCI Excel sheet and save it at `data/raw/Online Retail.xlsx`.
- [ ] Run the app and calculate KPIs on real data.
- [ ] Confirm sales are not called *net revenue*, because return reconciliation is not yet implemented.
- [ ] Never disclose or use customer IDs as if they were personal identity details.

## Stage 3 — SQL

**Goal:** Run each question in `sql/01_business_questions.sql`, and learn SELECT, WHERE, GROUP BY and ORDER BY. Build more advanced window-function queries later.

## Stage 4 — Power BI

**Goal:** Create a dashboard with a date table, measures, monthly trends, top products and geography filters. Add plain-English stakeholder recommendations.

## Stage 5 — Customer intelligence

**Goal:** RFM customer segmentation: recency, purchase frequency and monetary value. Exclude unidentifiable customers from person-level segmentation; be explicit about the rules.

## Stage 6 — Data quality and automation

**Goal:** Unit tests, scheduled historical-data reprocessing, logging, business-metric definitions and documented reproducibility. Historical data does not magically become live because a job runs daily.

## Stage 7 — GitHub + deployment

1. Create a public GitHub repository named `retail-sales-customer-intelligence`.
2. Add the code, practice data, screenshots, README and an attribution to UCI. Check that `.env`, raw customer rows and local databases are not committed.
3. Write a case study: business question → data quality → analysis → findings → recommendations → limitations.
4. Once reviewed, run `git init`, `git add .`, `git commit -m "Initial retail analytics project"`, connect the empty GitHub repository and push.
5. Connect that repository to Streamlit Community Cloud; set the main file to `app.py`. This first deployed app uses the **fictional sample** until we deliberately publish approved, safe aggregates from real data.
6. Add automated tests and screenshots of the live URL to README. Verify the deployed app personally.

No GitHub repository or deployed site exists yet. We will do these stages together, including reviewing the data-privacy and licence conditions.

## Suggested interview narrative (after the work is genuinely done)

"I built a UK retail analytics pipeline that loads and validates transaction records, analyses completed-sales value in SQL, and surfaces trends in an interactive dashboard. I documented how cancellations and missing customer IDs affect metrics, and provided reproducible steps and tests."

Only add numerical achievements and deployment claims that you have verified.
