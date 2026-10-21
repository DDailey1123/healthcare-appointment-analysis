-- SQLite dialect. Source grain: one appointment; duplicates are exact copies.
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

-- Compare by clinic; retain denominators to show group size.
SELECT clinic, COUNT(*) AS appointments,
 SUM(CASE WHEN status IN ('Completed','No-show') THEN 1 ELSE 0 END) AS eligible,
 SUM(CASE WHEN status='No-show' THEN 1 ELSE 0 END) AS no_shows,
 1.0*SUM(CASE WHEN status='No-show' THEN 1 ELSE 0 END)/
 NULLIF(SUM(CASE WHEN status IN ('Completed','No-show') THEN 1 ELSE 0 END),0) AS no_show_rate
FROM appointments_clean GROUP BY clinic ORDER BY clinic;

-- Compare by month; retain denominators to show group size.
SELECT month, COUNT(*) AS appointments,
 SUM(CASE WHEN status IN ('Completed','No-show') THEN 1 ELSE 0 END) AS eligible,
 SUM(CASE WHEN status='No-show' THEN 1 ELSE 0 END) AS no_shows,
 1.0*SUM(CASE WHEN status='No-show' THEN 1 ELSE 0 END)/
 NULLIF(SUM(CASE WHEN status IN ('Completed','No-show') THEN 1 ELSE 0 END),0) AS no_show_rate
FROM appointments_clean GROUP BY month ORDER BY month;

-- Compare by lead_band; retain denominators to show group size.
SELECT lead_band, COUNT(*) AS appointments,
 SUM(CASE WHEN status IN ('Completed','No-show') THEN 1 ELSE 0 END) AS eligible,
 SUM(CASE WHEN status='No-show' THEN 1 ELSE 0 END) AS no_shows,
 1.0*SUM(CASE WHEN status='No-show' THEN 1 ELSE 0 END)/
 NULLIF(SUM(CASE WHEN status IN ('Completed','No-show') THEN 1 ELSE 0 END),0) AS no_show_rate
FROM appointments_clean GROUP BY lead_band ORDER BY lead_band;

-- Compare by reminder_sent; retain denominators to show group size.
SELECT reminder_sent, COUNT(*) AS appointments,
 SUM(CASE WHEN status IN ('Completed','No-show') THEN 1 ELSE 0 END) AS eligible,
 SUM(CASE WHEN status='No-show' THEN 1 ELSE 0 END) AS no_shows,
 1.0*SUM(CASE WHEN status='No-show' THEN 1 ELSE 0 END)/
 NULLIF(SUM(CASE WHEN status IN ('Completed','No-show') THEN 1 ELSE 0 END),0) AS no_show_rate
FROM appointments_clean GROUP BY reminder_sent ORDER BY reminder_sent;
