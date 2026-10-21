# Healthcare Appointment Attendance Analysis

AI-assisted portfolio case study for Dorothy Dailey. All records are simulated. No real patient or employer data is included. This project has not been implemented at a real organization.

## Start here
Read Dorothy_Dailey_Data_Analyst_Project.pdf, then open Healthcare_Appointment_Dashboard.xlsx. Read analysis.sql alongside the results. Review and reproduce the work before describing it as a skill you can demonstrate.

## Files
- appointments_raw.csv: 2,412 records including intentional duplicate and formatting issues.
- appointments_clean.csv: 2,400 unique standardized appointments, plus month and lead_band.
- analysis.sql: SQLite cleaning view and five summary queries.
- appointments.sqlite: ready-to-query database with raw table and clean view.
- build_analysis.py: deterministic source generation, SQL execution and validation. Python 3 standard library only. Run `python build_analysis.py` from the extracted folder.
- results.json: independently computed SQL summary outputs.
- quality_checks.txt: executed source checks.
- Healthcare_Appointment_Dashboard.xlsx: editable formula summaries and two native charts. Fixed source ranges for 2,400 appointments; Python reruns do not refresh this workbook.
- create_report.py: report builder, requiring reportlab.
- dashboard_preview.png: dashboard image for a portfolio preview.

## Data dictionary
| Field | Meaning |
|---|---|
| appointment_id | Fictional unique appointment identifier; duplicates are exact repeated records |
| appointment_date | Scheduled date, Jan 1-Jun 30, 2026, ISO text in CSV |
| clinic | Fictional Central, East or West clinic |
| lead_days | Days between booking and appointment, integer 0-45 |
| reminder_sent | Yes/No administrative flag; no delivery/read confirmation |
| status | Completed, No-show, or Cancelled |
| month | Derived YYYY-MM reporting key |
| lead_band | Derived 0-7, 8-21 or 22-45 days |

## Definitions and limits
No-show rate = No-show / (Completed + No-show). Cancellation rate, if calculated, uses all appointments. There are no unique patient IDs, so patient-level analysis is unavailable. Simulation uses seed 42. Cancellation probability is 10%. Among noncancelled appointments, no-show probability is 0.07 + 0.004*lead_days + 0.07 if no reminder + 0.035 if East clinic. Those design choices create the analyzed associations. This is descriptive analysis, not causal evidence or a predictive model. There is no observed revenue, cost or improvement estimate.

## Practice before an interview
1. Reproduce 381 no-shows and a denominator of 2,151.
2. Explain why using 2,400 as the denominator answers a different question.
3. Compare East and Central using percentage points, not percent change.
4. Filter a clinic and explain why counts and rates tell different stories.
5. Add a clinic-by-reminder SQL breakdown to explore confounding.
6. In a copy of Excel, change a Completed record to No-show. Confirm the counts and rates update, then restore the value.

## Suggested resume entry
Healthcare Appointment Attendance Analysis | Portfolio Project

Analyzed 2,400 simulated appointments using SQL and Excel; cleaned duplicate records, standardized clinic labels, built a formula-driven KPI dashboard, and proposed a measurable pilot to investigate missed appointments.

List only the steps you have reviewed, reproduced and can explain. Use the PDF as an attachment or place the project files in your portfolio and add that link to your resume.
