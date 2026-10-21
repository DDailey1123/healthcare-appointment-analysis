from pathlib import Path
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
ROOT=Path(__file__).resolve().parent
s=json.loads((ROOT/'results.json').read_text())
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Deck',fontSize=12,leading=18,textColor=colors.HexColor('#566478'),spaceAfter=16))
styles['BodyText'].leading=15; styles['BodyText'].spaceAfter=10
story=[]
def p(text,style='BodyText'):story.append(Paragraph(text,styles[style]))
def h(text):p(text,'Heading2')
def table(head,rows,widths):
 t=Table([head]+rows,colWidths=widths,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#24354B')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),9),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#EDF2F7'),colors.white]),('ALIGN',(1,1),(-1,-1),'RIGHT')]));story.append(t);story.append(Spacer(1,12))
p('Healthcare Appointment Attendance','Title')
p('Dorothy Dailey<br/>Data analyst portfolio case study | January-June 2026','Deck')
p('<b>Project scope:</b> Analyze appointment attendance across three fictional clinics and identify operational questions for a follow-up pilot. Tools: SQL (SQLite), Excel and Python standard library.')
p('<b>Data provenance:</b> AI-assisted portfolio project using entirely simulated records. No patient, employer or external source data is used. The generator deliberately makes longer lead times, absent reminders and East Clinic appointments more likely to become no-shows. Findings illustrate analytical methods and are not independent healthcare research.')
h('Business question')
p('Where are missed appointments concentrated, and which scheduling patterns should a clinic manager investigate first?')
table(['Metric','Result'],[['Unique appointments','2,400'],['Completed','1,770'],['No-shows','381'],['Cancelled','249'],['No-show rate','17.7%']],[340,145])
p('<b>Metric definition:</b> No-show rate = No-shows / (Completed + No-shows). The denominator is 2,151 appointments. Cancellations are reported separately and excluded from this rate. Each row represents one appointment, not one unique patient.')
h('Main finding')
p('East Clinic has the highest simulated no-show rate at 21.6%, compared with 16.9% at West and 14.8% at Central. East exceeds Central by 6.8 percentage points, using unrounded rates. This identifies a review priority, not a proven cause.')
story.append(PageBreak())
p('Findings and recommended next steps','Title')
table(['Clinic','Eligible','No-shows','Rate'],[[x[0],str(x[2]),str(x[3]),f'{x[4]:.1%}'] for x in s['clinic']],[215,90,90,90])
h('Longer scheduling lead times')
table(['Lead time','Eligible','No-shows','Rate'],[[x[0],str(x[2]),str(x[3]),f'{x[4]:.1%}'] for x in sorted(s['lead_band'],key=lambda x: {'0-7 days':0,'8-21 days':1,'22-45 days':2}[x[0]])],[215,90,90,90])
p('Appointments booked 22-45 days ahead have a 22.8% no-show rate, compared with 11.1% for 0-7 days. In a real setting, investigate waitlists, access barriers and reconfirmation for longer lead times.')
h('Reminder status')
p('The rate is 23.0% without a recorded reminder (127/553) and 15.9% with one (254/1,598), a 7.1 percentage point difference. A recorded reminder does not mean a message was delivered or read. These unadjusted groups do not prove that reminders caused the difference.')
h('Proposed pilot')
p('Test additional reconfirmation for appointments booked more than 21 days ahead. Randomly assign eligible appointments to the current process or the new process where feasible. Track no-show rate, cancellations, reminder delivery, filled slots and staff time using the same definitions in both groups. Review clinic and lead-time composition before interpreting results.')
p('<b>Success measurement:</b> Compare the difference in no-show rates between pilot groups, with group counts and uncertainty intervals. Establish the sample size and a practical improvement threshold before starting. No pilot was performed and no savings or attendance improvement is claimed.')
story.append(PageBreak())
p('Method, reproducibility and interview guide','Title')
h('Cleaning and validation')
p('Start with 2,412 source rows. Remove 12 exact duplicate rows using SELECT DISTINCT, then normalize clinic labels with TRIM and case conversion. Twenty-four unique appointment records have inconsistent clinic formatting. Retain all 2,400 unique appointments. Check unique IDs, allowed clinics/statuses, nonnegative lead times and date coverage. No missing values are imputed.')
h('How to reproduce')
p('1. Extract the project ZIP into one folder.<br/>2. Run <font face="Courier">python build_analysis.py</font> with Python 3. It uses only the standard library and recreates the CSV files, SQLite database, analysis.sql, results.json and quality checks.<br/>3. Open appointments.sqlite in a SQLite client and run the SELECT queries in analysis.sql.<br/>4. Open the Excel dashboard. Its summary formulas use the Appointments sheet. The workbook is a fixed 2,400-row analysis; rebuilding the Python results does not automatically refresh Excel. To use another dataset, replace the source records and extend all formula/chart ranges as needed.')
h('What the SQL demonstrates')
p('DISTINCT removes exact duplicate rows. TRIM and string functions standardize clinic names. CASE creates scheduling lead-time bands and conditional counts. GROUP BY summarizes clinics and months. NULLIF prevents division by zero. A clean view separates the source records from analysis logic.')
h('Explain it in your own words')
p('"I used a simulated scheduling dataset to practice analyzing missed appointments. I cleaned duplicates and inconsistent clinic labels, defined a no-show rate that excludes cancellations, and compared attendance by clinic, lead time and reminder status. The main recommendation was to test reconfirmation for longer lead-time appointments. Because the data is simulated and the comparisons are descriptive, I would validate the patterns with real data before making an operational decision."')
h('Resume wording after you review and reproduce it')
p('<b>Healthcare Appointment Attendance Analysis | Portfolio Project</b><br/>Analyzed 2,400 simulated appointments using SQL and Excel; cleaned duplicate records, standardized clinic labels, built a formula-driven KPI dashboard, and proposed a measurable pilot to investigate missed appointments.')
p('<b>Before listing:</b> Reproduce the SQL results, explain the denominator, change a source status in Excel and observe the dashboard update, then restore the value. Describe this honestly as an AI-assisted portfolio project and adapt the wording to the work you personally completed.')
def footer(c,doc):
 c.setFont('Helvetica',9);c.setFillColor(colors.HexColor('#566478'));c.drawString(54,30,'Dorothy Dailey | Simulated data portfolio project');c.drawRightString(558,30,str(doc.page))
SimpleDocTemplate(str(ROOT/'Dorothy_Dailey_Data_Analyst_Project.pdf'),pagesize=(612,792),rightMargin=54,leftMargin=54,topMargin=42,bottomMargin=48).build(story,onFirstPage=footer,onLaterPages=footer)
