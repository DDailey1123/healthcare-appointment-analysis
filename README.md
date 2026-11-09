Healthcare Appointment Attendance Analysis

Author: Dorothy Dailey

Missed appointments cost clinics time and revenue and delay patient care. In my work in patient access and care coordination, I've seen how scheduling decisions can affect whether patients show up. This project looks at how booking lead time, appointment reminders and clinic location relate to no-show rates, and proposes a measurable pilot to look into the issue further.

Note: All records in this project are simulated. No real patient or employer data is included.

Dataset

	•	Raw data: 2,412 appointment records, including duplicates and formatting issues to clean
	•	Clean data: 2,400 unique appointments scheduled January 1 – June 30, 2026
	•	Clinics: Central, East and West
	•	Fields: clinic, lead time in days (0–45), reminder sent (Yes/No), and status (Completed, No-show or Cancelled)

Tools

	•	SQL (SQLite): a cleaning view plus five summary queries
	•	Python 3: data generation, running the SQL and validating the results
	•	Excel: a formula-driven dashboard with charts
	•	reportlab: a PDF summary report

Process

	1.	Cleaned the data: removed duplicates and standardized formats with a SQL view, bringing 2,412 raw records down to 2,400 unique appointments.
	2.	Defined the metric: No-show rate = No-shows ÷ (Completed + No-shows). Cancelled appointments are left out because the patient never had a chance to miss them.
	3.	Analyzed patterns: compared no-show rates by booking lead time, reminder status and clinic.
	4.	Validated the results: used Python checks to confirm that the SQL outputs match the clean data (see quality_checks.txt).
	5.	Reported findings: built an Excel dashboard and a PDF summary.

Results

	•	Overall: 381 no-shows out of 2,151 completed or missed appointments, a no-show rate of about 17.7%.
	•	Clinic comparisons are reported as differences in percentage points.
	•	Full query outputs are in results.json, and charts are in the dashboard.

Limitations

	•	The data is simulated, so the patterns show how the analysis works, not real-world effects.
	•	There are no unique patient IDs, so I couldn't analyze individual patients (for example, patients with repeated no-shows).
	•	This is a descriptive analysis. It doesn't prove cause and effect, it isn't a predictive model, and it doesn't estimate revenue or cost.

Files

File	Description
analysis.sql	SQLite cleaning view and summary queries
appointments.sqlite	Database with the raw table and the clean view
appointments_raw.csv / appointments_clean.csv	Raw and cleaned data
build_analysis.py	Rebuilds the data and runs the SQL validation (Python standard library only)
create_report.py	Builds the PDF report (requires reportlab)
results.json / quality_checks.txt	Query outputs and data quality checks
Healthcare_Appointment_Dashboard.xlsx	Excel dashboard (does not update automatically when the Python scripts rerun)
Dorothy_Dailey_Data_Analyst_Project.pdf	Summary report
dashboard_preview.png	Dashboard screenshot

How to Run

python3 build_analysis.py   # rebuild the data and run the validation
pip install reportlab
python3 create_report.py    # build the PDF report

Next Steps

	•	Repeat the analysis on a real public dataset of appointment no-shows.
	•	Run a pilot comparing reminder timing (for example, 48 hours vs. 24 hours before the appointment) and track the change in no-show rate.
