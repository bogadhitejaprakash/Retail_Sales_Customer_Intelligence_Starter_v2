# Retail Sales & Customer Intelligence

An interview-ready UK retail analytics project, built one lesson at a time.

**Project owner:** Bogadhi Teja Prakash (Teja)  
**Current stage:** Lesson 1 — understand the data and calculate sales revenue.

## The business question

Imagine you are a junior data analyst for an online gift retailer. Your manager asks:

1. How much revenue did we generate from completed sales?
2. Which products sold the most?
3. How are sales changing month by month?
4. How many identified customers bought from us?
5. What opportunities should we investigate next?

The first release includes Python analysis, SQLite and a simple Streamlit dashboard. Future lessons will add advanced SQL, segmentation, Power BI, data validation, GitHub and deployment.

## Dataset: practice first, real data next

- `data/sample/retail_sample.csv` is **fictional practice data**, included to make Lesson 1 run immediately. Never present its results as genuine business performance.
- Our genuine data will be UCI's **Online Retail** dataset: transactions at a UK-based online retailer, December 2010–December 2011 (541,909 rows). It is **historical**, not real-time.
- Official source and download: https://archive.ics.uci.edu/dataset/352/online%2Bretail
- Citation: Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33
- Dataset licence: CC BY 4.0. Attribute the source when publishing visualisations or derived data.

### Download the real data (Lesson 2)

1. Open the UCI link above and click **Download**.
2. If the download is zipped, extract it.
3. Put `Online Retail.xlsx` in `data/raw/` (create that folder if needed).
4. Run the same code again. The dashboard and SQLite script will use the real Excel file automatically.

For GitHub, do not commit a raw file with customer identifiers; this starter's `.gitignore` excludes raw Excel files. We will publish safe aggregated outputs and clearly document the source.

## Your folder structure

```text
retail-intelligence/
├── app.py                     # Interactive dashboard (preview)
├── run_project.ps1            # One-file Windows PowerShell launcher
├── lessons/
│   └── 01_first_analysis.py   # Start here; prints simple results
├── retail/
│   └── analysis.py            # Reusable data-cleaning and KPI functions
├── data/
│   ├── sample/
│   │   └── retail_sample.csv  # Synthetic practice transactions
│   └── raw/                   # Real Excel goes here later
├── scripts/
│   └── load_to_sqlite.py      # Load cleaned data into a local database
├── sql/
│   └── 01_business_questions.sql
├── tests/
│   └── test_analysis.py
├── docs/
│   └── LEARNING_PATH.md
└── requirements.txt
```

## Set up on your Windows laptop (VS Code terminal / PowerShell)

Install [Python](https://www.python.org/downloads/) and [VS Code](https://code.visualstudio.com/), then extract this project ZIP and open its `retail-intelligence` folder in VS Code.

**Easiest way: run the included PowerShell file** from the VS Code terminal, while in the project folder:

```powershell
.\run_project.ps1
```

This sets up Python, installs packages, runs Lesson 1 and opens the interactive dashboard. Use `Ctrl+C` to stop the dashboard.

If your organisation's PowerShell policy blocks scripts, do not change security settings just for this project. Use the manual commands below instead.

**Manual alternative:** Run these commands **from the project folder**:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe lessons\01_first_analysis.py
```

This uses your project's own Python environment and avoids having to change the PowerShell execution policy. If `py` is not recognised, try `python` instead of `py` in the first command.

For your dashboard:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

For SQLite (Lesson 3):

```powershell
.\.venv\Scripts\python.exe -m scripts.load_to_sqlite
```

For tests:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

On macOS/Linux, use `python3 -m venv .venv` and `.venv/bin/python` instead of the Windows Python path.

## Lesson 1: your first coding task

Open `lessons/01_first_analysis.py` and read the comments before running it. It teaches:

1. What a CSV file and a Pandas DataFrame are.
2. How to inspect a dataset with `.head()`, `.shape` and `.columns`.
3. How to calculate **line revenue = quantity × unit price**.
4. Why cancellations and zero-price lines must be treated carefully.

**Challenge:** Change the final line of the lesson to show 10 rows instead of 5. Then add a line that prints only transactions from the United Kingdom.

### Important metric definitions

For this starter, **gross completed-sales value** means positive-quantity, positive-price lines whose invoice number does not start with `C`. It excludes cancellation/return lines. It is **not net revenue, profit or audited sales**. Customer counts include only non-empty customer IDs, while sale totals include valid sales with unknown customer IDs.

## What comes next

| Lesson | Deliverable | Key skill |
| --- | --- | --- |
| 1 | Read practice transactions | Python, Pandas |
| 2 | Clean genuine UK retail data | Missing values, returns, QA |
| 3 | Answer questions in a SQLite database | SQL, joins, grouping |
| 4 | Build Power BI sales dashboard | Data modelling, DAX |
| 5 | Segment customers with RFM | Business analytics |
| 6 | Test and automate the pipeline | Reproducibility, quality |
| 7 | Publish on GitHub and deploy | Version control, Streamlit |

See `docs/LEARNING_PATH.md` for interview-ready acceptance criteria and deployment steps. This repository is a starter, **not yet published or deployed**.
