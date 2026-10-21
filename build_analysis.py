"""Rebuild simulated source data and execute analysis using Python standard library only."""
from pathlib import Path
import csv, random, sqlite3, json
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parent
rng = random.Random(42)
headers = ['appointment_id','appointment_date','clinic','lead_days','reminder_sent','status']
rows = []
for i in range(1,2401):
    day = date(2026,1,1) + timedelta(days=rng.randrange(181))
    clinic = rng.choice(['Central','East','West'])
    lead = rng.randint(0,45)
    reminder = rng.choice(['Yes','Yes','Yes','No'])
    cancelled = rng.random() < .10
    p = .07 + .004*lead + (.07 if reminder=='No' else 0) + (.035 if clinic=='East' else 0)
    status = 'Cancelled' if cancelled else ('No-show' if rng.random()<p else 'Completed')
    rows.append([f'A{i:05}',day.isoformat(),clinic,lead,reminder,status])
# Deliberate source-quality issues for an auditable cleaning exercise.
raw = [r.copy() for r in rows]
for i in range(0,2400,100): raw[i][2] = ' '+raw[i][2].lower()+' '
raw += [r.copy() for r in raw[:12]]
def write_csv(name, head, data):
    with (ROOT/name).open('w',newline='') as f:
        w=csv.writer(f);w.writerow(head);w.writerows(data)
write_csv('appointments_raw.csv',headers,raw)
db = sqlite3.connect(ROOT/'appointments.sqlite')
db.execute('DROP TABLE IF EXISTS appointments_raw')
db.execute('CREATE TABLE appointments_raw (appointment_id TEXT, appointment_date TEXT, clinic TEXT, lead_days INTEGER, reminder_sent TEXT, status TEXT)')
db.executemany('INSERT INTO appointments_raw VALUES (?,?,?,?,?,?)',raw)
sql = '''-- SQLite dialect. Source grain: one appointment; duplicates are exact copies.
DROP VIEW IF EXISTS appointments_clean;
CREATE VIEW appointments_clean AS
SELECT DISTINCT appointment_id, appointment_date,
 UPPER(SUBSTR(TRIM(clinic),1,1)) || LOWER(SUBSTR(TRIM(clinic),2)) AS clinic,
 lead_days, reminder_sent, status,
 SUBSTR(appointment_date,1,7) AS month,
 CASE WHEN lead_days<=7 THEN '0-7 days' WHEN lead_days<=21 THEN '8-21 days' ELSE '22-45 days' END AS lead_band
FROM appointments_raw;

-- Overall: cancellations are excluded from the no-show rate denominator.
SELECT COUNT(*) AS appointments,
 SUM(CASE WHEN status='Completed' THEN 1 ELSE 0 END) AS completed,
 SUM(CASE WHEN status='No-show' THEN 1 ELSE 0 END) AS no_shows,
 SUM(CASE WHEN status='Cancelled' THEN 1 ELSE 0 END) AS cancelled,
 1.0*SUM(CASE WHEN status='No-show' THEN 1 ELSE 0 END)/
 NULLIF(SUM(CASE WHEN status IN ('Completed','No-show') THEN 1 ELSE 0 END),0) AS no_show_rate
FROM appointments_clean;
'''
for dim in ['clinic','month','lead_band','reminder_sent']:
    sql += f'''\n-- Compare by {dim}; retain denominators to show group size.
SELECT {dim}, COUNT(*) AS appointments,
 SUM(CASE WHEN status IN ('Completed','No-show') THEN 1 ELSE 0 END) AS eligible,
 SUM(CASE WHEN status='No-show' THEN 1 ELSE 0 END) AS no_shows,
 1.0*SUM(CASE WHEN status='No-show' THEN 1 ELSE 0 END)/
 NULLIF(SUM(CASE WHEN status IN ('Completed','No-show') THEN 1 ELSE 0 END),0) AS no_show_rate
FROM appointments_clean GROUP BY {dim} ORDER BY {dim};\n'''
(ROOT/'analysis.sql').write_text(sql)
db.executescript(sql)
clean = db.execute('SELECT * FROM appointments_clean ORDER BY appointment_id').fetchall()
write_csv('appointments_clean.csv',headers+['month','lead_band'],clean)
assert len(raw)==2412 and len(clean)==2400
assert len({r[0] for r in clean})==2400
assert all(r[2] in ['Central','East','West'] and 0<=r[3]<=45 for r in clean)
assert all(date.fromisoformat(r[1])>=date(2026,1,1) and date.fromisoformat(r[1])<=date(2026,6,30) for r in clean)
assert all(r[5] in ['Completed','No-show','Cancelled'] for r in clean)
summary={}
for dim in ['clinic','month','lead_band','reminder_sent']:
    summary[dim]=db.execute(f"SELECT {dim},COUNT(*),SUM(status IN ('Completed','No-show')),SUM(status='No-show'),1.0*SUM(status='No-show')/SUM(status IN ('Completed','No-show')) FROM appointments_clean GROUP BY {dim} ORDER BY {dim}").fetchall()
summary['overall']=db.execute("SELECT COUNT(*),SUM(status='Completed'),SUM(status='No-show'),SUM(status='Cancelled'),1.0*SUM(status='No-show')/SUM(status IN ('Completed','No-show')) FROM appointments_clean").fetchone()
(ROOT/'results.json').write_text(json.dumps(summary,indent=2))
(ROOT/'quality_checks.txt').write_text('PASS: 2,412 raw rows; 12 exact duplicate rows removed; 2,400 unique appointments.\nPASS: 24 unique clinic labels normalized.\nPASS: all IDs unique after cleaning, required fields populated, dates in Jan-Jun 2026, lead times 0-45, allowed statuses and clinics.\nNo records excluded other than exact duplicates. No values imputed.\n')
db.commit();db.close()
print(json.dumps(summary,indent=2))
