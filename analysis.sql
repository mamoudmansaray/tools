-- SQLite query. Source: provided synthetic data.csv
SELECT 'Missing program' AS issue, COUNT(*) AS affected FROM data WHERE program IS NULL OR TRIM(program)=''
UNION ALL SELECT 'Invalid service date',COUNT(*) FROM data WHERE service_date IS NULL OR date(service_date) IS NULL
UNION ALL SELECT 'Negative hours',COUNT(*) FROM data WHERE hours<0
UNION ALL SELECT 'Missing hours',COUNT(*) FROM data WHERE hours IS NULL
UNION ALL SELECT 'Negative billed amount',COUNT(*) FROM data WHERE billed_amount<0
UNION ALL SELECT 'Duplicate ID excess rows',COUNT(*)-COUNT(DISTINCT record_id) FROM data;
