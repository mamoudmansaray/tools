# Service Records Data Quality Audit

### Business question
Which records need review before operational reporting?

### Dataset and definitions
200 records. One row is a submitted service record. Missing numeric cells are imported as NULL. Five ID values are intentionally duplicated. Issue counts can overlap and must not be added to estimate unique affected records.

Columns in order: record_id, program, service_date, hours, billed_amount.

### Workflow
1. Preserve the raw CSV before identifying problems.
2. Flag missing programs, invalid dates, missing/negative hours, negative billed amounts, and excess duplicate IDs.
3. Document corrections that require source confirmation instead of inventing replacement values.

### Run the code
Run `python analyze.py` from this folder (or `python3 analyze.py`). The script locates its inputs beside itself, creates a SQLite table, runs analysis.sql, writes results.csv, and builds dashboard.html. Python uses the standard library only. A failed schema or numeric conversion stops the run instead of silently discarding records.

### Verified sample result
Metric: affected. Missing program: 4; Invalid service date: 5; Negative hours: 4; Missing hours: 3; Negative billed amount: 4; Duplicate ID excess rows: 5.
These numbers are from the provided dataset. Percentage results use 0-100 values, not Excel percentage fractions. For forecasting, lower MAE is better. For budget variance, positive means over budget.

### Excel exercise
Open data.csv. Save As an Excel Workbook (.xlsx). Select the source range and Insert > Table, then Insert > PivotTable on a new sheet.

Create rule columns on a copy of data. Summarize issue counts in a table and insert a bar chart. Filter flagged records for review.

Formula practice (source headers in row 1): For duplicate IDs: =COUNTIF(A:A,A2)>1. This flags both occurrences; excess-duplicate count instead counts rows beyond the first.

The formula examples assume an English-language Excel installation using commas. Verify the target columns before filling down. Save your finished workbook and a dashboard screenshot in this folder.

### Interpretation and limits
This checks selected rules only. A valid-looking record can still be inaccurate. Do not silently replace missing values with zero.

### Make the project your own
Create a quarantine.csv with row-level issue reasons and retain a correction log.
Write three findings with numerical evidence, one limitation, and one next action. Explain the query, verify at least one result manually, and replace the practice description with your own completed-work summary only after reproducing the work.

### Files
Source data.csv, analyze.py, analysis.sql, config.json, results.csv, project.db, dashboard.html, and sample_output.txt.
