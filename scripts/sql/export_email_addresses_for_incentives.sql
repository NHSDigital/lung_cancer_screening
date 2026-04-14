-- Commands are written on one line for psql execution, can be formatted for readability when running in a SQL client.
-- This script performs the following steps:
-- 1 - creates a list of email addresses of participants eligible for incentives
-- 2 - updates participants that have been exported so that they are timestamped as having received an incentive
-- 3 Incentive eligibility is based on:
-- - having submitted the questionnaire
-- - not having already received an incentive
-- - Online submitted_at date is earlier than telephone questionnaire date_conducted.

-- Find container name:
podman ps --format "{{.Names}}"
-- Copy partner csv file to server temp directory
podman cp "/Users/*YourUsername*/Downloads/SampleDataPIDRemoved230126.csv" <db_container_name>:/tmp/partner.csv

-- login to psql on local container


-- Create temp table for partner data import (can be permanent)
-- importing all date from sample file or test - would we want to do this with live data? Do we need all columns?

-- single line command for psql to Create table
CREATE TEMP TABLE tmp_incentive_partner_import_raw (nhs_number TEXT, date_of_birth TEXT, date_conducted TEXT, smoking_status TEXT, average_cigarettes_per_day_while_smoking TEXT, duration_smoked_years TEXT, years_since_quitting_smoking TEXT, height_measurement_type TEXT, height_measurement_value_metric_cm TEXT, weight_measurement_type TEXT, weight_measurement_value_metric_kg TEXT, previous_respiratory_diagnosis TEXT, personal_history_of_previous_cancer TEXT, family_history_of_lung_cancer TEXT, personal_history_of_asthma TEXT, asbestos_exposure_from_job_or_activity TEXT, education TEXT, ethnicity TEXT, plco_lung_cancer_risk_score TEXT, llp_lung_cancer_risk_score TEXT, created_at TIMESTAMPTZ NOT NULL DEFAULT now());

-- psql command to import data from CSV file into the temp table - currently 40 rows of test data in sample file:
-- One line command for psql to import data from CSV file into the temp table:
\copy tmp_incentive_partner_import_raw (nhs_number, date_of_birth, date_conducted, smoking_status, average_cigarettes_per_day_while_smoking, duration_smoked_years, years_since_quitting_smoking, height_measurement_type, height_measurement_value_metric_cm, weight_measurement_type, weight_measurement_value_metric_kg, previous_respiratory_diagnosis, personal_history_of_previous_cancer, family_history_of_lung_cancer, personal_history_of_asthma, asbestos_exposure_from_job_or_activity, education, ethnicity, plco_lung_cancer_risk_score, llp_lung_cancer_risk_score) FROM '/tmp/partner.csv' WITH (FORMAT csv, HEADER true);


-- TRANSACTION START for exporting eligible participants for incentives and updating incentivised table.
\r
BEGIN;
CREATE TEMP TABLE tmp_eligible_incentive_export AS SELECT DISTINCT ON (qrs.id) qu.id AS user_id, qrs.id AS response_set_id, qu.email FROM questions_user qu JOIN questions_responseset qrs ON qrs.user_id = qu.id JOIN tmp_incentive_partner_import_raw ipir ON ipir.nhs_number = qu.nhs_number LEFT JOIN questions_incentivised qi ON qi.response_set_id = qrs.id WHERE to_timestamp(NULLIF(ipir.date_conducted, ''), 'DD/MM/YYYY HH24:MI')::timestamptz > qrs.submitted_at::timestamptz AND qi.id IS NULL ORDER BY qrs.id, qrs.submitted_at DESC;
\copy (SELECT email FROM tmp_eligible_incentive_export ORDER BY email) TO '/tmp/eligible_participants_export.csv' WITH (FORMAT csv, HEADER true);
INSERT INTO questions_incentivised (created_at, updated_at, incentivised_at, user_id, response_set_id) SELECT now(), now(), now(), user_id, response_set_id FROM tmp_eligible_incentive_export;
SELECT count(*) AS rows_exported_and_marked FROM tmp_eligible_incentive_export;
-- COMMIT;
-- ROLLBACK;

-- TRANSACTION END

-- DELETE temp tables
DROP TABLE IF EXISTS tmp_eligible_incentive_export;
DROP TABLE IF EXISTS tmp_incentive_partner_import_raw;


-- Test data creation for testing incentive logic - creating 40 test users with varying submitted_at dates and response_set_ids to test export and incentivised table update logic.
-- This has been included for completeness, can delete before full PR.
BEGIN;

DELETE FROM questions_responseset WHERE user_id IN (SELECT id FROM questions_user WHERE nhs_number BETWEEN '11111111' AND '11111150');

INSERT INTO questions_user (password, last_login, sub, nhs_number, given_name, family_name, email, created_at, updated_at) SELECT '!' || md5('seed-' || gs::text), NULL, 'seed-' || gs::text, gs::text, 'Test', 'User' || right(gs::text, 2), 'test.' || gs::text || '@example.com', now(), now() FROM generate_series(11111111::bigint, 11111150::bigint) gs WHERE NOT EXISTS (SELECT 1 FROM questions_user WHERE nhs_number = gs::text);

INSERT INTO questions_responseset (created_at, updated_at, submitted_at, user_id) SELECT now(), now(), CASE (row_number() OVER (ORDER BY qu.nhs_number)) % 3 WHEN 0 THEN NULL WHEN 1 THEN now() ELSE timestamp '2023-06-01 09:00:00' + (((row_number() OVER (ORDER BY qu.nhs_number)) * 7) || ' days')::interval END, qu.id FROM questions_user qu WHERE qu.nhs_number BETWEEN '11111111' AND '11111150';

INSERT INTO questions_dateofbirthresponse (created_at, updated_at, value, response_set_id) SELECT now(), now(), (date '1960-01-01' + ((row_number() OVER (ORDER BY qu.nhs_number)) * 30 || ' days')::interval)::date, qrs.id FROM questions_responseset qrs JOIN questions_user qu ON qu.id = qrs.user_id WHERE qu.nhs_number BETWEEN '11111111' AND '11111150';

--COMMIT;
--ROLLBACK;

-- clean up test data

DELETE FROM questions_responseset WHERE user_id IN (SELECT id FROM questions_user WHERE nhs_number BETWEEN '11111111' AND '11111150');
DELETE FROM questions_user WHERE user_id IN (SELECT id FROM questions_user WHERE nhs_number BETWEEN '11111111' AND '11111150');

