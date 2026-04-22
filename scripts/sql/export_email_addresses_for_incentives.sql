-- Commands are written on one line for psql execution, can be formatted for readability when running in a SQL client.
-- This script performs the following steps:
-- 1 - imports new data from csv file. The csv file is expected to be a full export of all partner records, but only new records will be inserted into the permanent table.
-- 2 - creates a list of email addresses of participants eligible for incentives
-- 3 - updates participants that have been exported so that they are timestamped as having received an incentive

-- Incentive eligibility is based on:
-- - having submitted the questionnaire
-- - not having already received an incentive
-- - Online submitted_at date is earlier than telephone questionnaire date_conducted.

-- Partner import strategy:
-- The partner sends a full CSV export every week. Rather than replacing all data each run, we insert only
-- new records using a UNIQUE index on (nhs_number, conducted_at) and ON CONFLICT DO NOTHING.
-- Records removed from the partner's source will NOT be deleted.


-- Steps to follow:
-- 1. Log into AVD.
-- 2. Upload csv file to AVD
-- 3. Find file in RemoteVirtualDrive and copy to accessible location for psql COPY command.
-- 4. PATH_TO_FILE - search for this and replace with actual file path.
-- 5. Login to DB in AVD.


-- ============================================================
-- RUN ONCE: Create permanent partner import table
-- Only run this block on first setup. The unique constraint on
-- (nhs_number, conducted_at) prevents duplicate rows being
-- inserted on subsequent weekly loads.
-- ============================================================
CREATE TABLE IF NOT EXISTS inhealth_partner_data (nhs_number TEXT, date_of_birth TEXT, date_conducted TEXT, conducted_at TIMESTAMPTZ, smoking_status TEXT, average_cigarettes_per_day_while_smoking TEXT, duration_smoked_years TEXT, years_since_quitting_smoking TEXT, height_measurement_type TEXT, height_measurement_value_metric_cm TEXT, weight_measurement_type TEXT, weight_measurement_value_metric_kg TEXT, previous_respiratory_diagnosis TEXT, personal_history_of_previous_cancer TEXT, family_history_of_lung_cancer TEXT, personal_history_of_asthma TEXT, asbestos_exposure_from_job_or_activity TEXT, education TEXT, ethnicity TEXT, plco_lung_cancer_risk_score TEXT, llp_lung_cancer_risk_score TEXT, created_at TIMESTAMPTZ NOT NULL DEFAULT now(), CONSTRAINT uq_partner_nhs_conducted_at UNIQUE (nhs_number, conducted_at));


-- ============================================================
-- RUN WEEKLY: Load new partner records from CSV
-- Step 1: Import CSV into a temporary staging table.
-- Step 2: Insert only rows where (nhs_number, conducted_at)
--         do not already exist in the permanent table.
--         Existing rows are silently skipped (DO NOTHING).
-- ============================================================

-- Step 1: Create staging table and load CSV
CREATE TEMP TABLE tmp_incentive_partner_staging (nhs_number TEXT, date_of_birth TEXT, date_conducted TEXT, smoking_status TEXT, average_cigarettes_per_day_while_smoking TEXT, duration_smoked_years TEXT, years_since_quitting_smoking TEXT, height_measurement_type TEXT, height_measurement_value_metric_cm TEXT, weight_measurement_type TEXT, weight_measurement_value_metric_kg TEXT, previous_respiratory_diagnosis TEXT, personal_history_of_previous_cancer TEXT, family_history_of_lung_cancer TEXT, personal_history_of_asthma TEXT, asbestos_exposure_from_job_or_activity TEXT, education TEXT, ethnicity TEXT, plco_lung_cancer_risk_score TEXT, llp_lung_cancer_risk_score TEXT);

-- Copy data from file into staging table - update PATH_TO_FILE before running

\copy tmp_incentive_partner_staging (nhs_number, date_of_birth, date_conducted, smoking_status, average_cigarettes_per_day_while_smoking, duration_smoked_years, years_since_quitting_smoking, height_measurement_type, height_measurement_value_metric_cm, weight_measurement_type, weight_measurement_value_metric_kg, previous_respiratory_diagnosis, personal_history_of_previous_cancer, family_history_of_lung_cancer, personal_history_of_asthma, asbestos_exposure_from_job_or_activity, education, ethnicity, plco_lung_cancer_risk_score, llp_lung_cancer_risk_score) FROM 'PATH_TO_FILE' WITH (FORMAT csv, HEADER true);

-- Step 2: Insert only new records; skip any (nhs_number, conducted_at) already present
INSERT INTO inhealth_partner_data (nhs_number, date_of_birth, date_conducted, conducted_at, smoking_status, average_cigarettes_per_day_while_smoking, duration_smoked_years, years_since_quitting_smoking, height_measurement_type, height_measurement_value_metric_cm, weight_measurement_type, weight_measurement_value_metric_kg, previous_respiratory_diagnosis, personal_history_of_previous_cancer, family_history_of_lung_cancer, personal_history_of_asthma, asbestos_exposure_from_job_or_activity, education, ethnicity, plco_lung_cancer_risk_score, llp_lung_cancer_risk_score) SELECT nhs_number, date_of_birth, date_conducted, to_timestamp(NULLIF(date_conducted, ''), 'DD/MM/YYYY HH24:MI')::timestamptz, smoking_status, average_cigarettes_per_day_while_smoking, duration_smoked_years, years_since_quitting_smoking, height_measurement_type, height_measurement_value_metric_cm, weight_measurement_type, weight_measurement_value_metric_kg, previous_respiratory_diagnosis, personal_history_of_previous_cancer, family_history_of_lung_cancer, personal_history_of_asthma, asbestos_exposure_from_job_or_activity, education, ethnicity, plco_lung_cancer_risk_score, llp_lung_cancer_risk_score FROM tmp_incentive_partner_staging ON CONFLICT (nhs_number, conducted_at) DO NOTHING;

-- Delete temporary staging table
DROP TABLE IF EXISTS tmp_incentive_partner_staging;


-- TRANSACTION START for exporting eligible participants for incentives and updating incentivised table.
-- Update PATH_TO_EXPORT_FILE before running.
\r
BEGIN;
CREATE TEMP TABLE tmp_eligible_incentive_export AS WITH canonical_users AS (SELECT DISTINCT ON (nhs_number) id, email, nhs_number FROM questions_user WHERE nhs_number IS NOT NULL ORDER BY nhs_number, created_at DESC) SELECT DISTINCT ON (qrs.id) cu.id AS user_id, qrs.id AS response_set_id, cu.email FROM canonical_users cu JOIN questions_responseset qrs ON qrs.user_id = cu.id JOIN inhealth_partner_data ipd ON ipd.nhs_number = cu.nhs_number LEFT JOIN questions_incentivised qi ON qi.response_set_id = qrs.id WHERE ipd.conducted_at > qrs.submitted_at::timestamptz AND qi.id IS NULL ORDER BY qrs.id, qrs.submitted_at DESC;
\copy (SELECT email FROM tmp_eligible_incentive_export ORDER BY email) TO 'PATH_TO_EXPORT_FILE' WITH (FORMAT csv, HEADER true);
INSERT INTO questions_incentivised (created_at, updated_at, incentivised_at, user_id, response_set_id) SELECT now(), now(), now(), user_id, response_set_id FROM tmp_eligible_incentive_export;
SELECT count(*) AS rows_exported_and_marked FROM tmp_eligible_incentive_export;

-- If happy with the Select result type COMMIT; if not, ROLLBACK; to undo changes;

-- COMMIT;
-- ROLLBACK;

-- TRANSACTION END

-- DELETE tempprary export table
DROP TABLE IF EXISTS tmp_eligible_incentive_export;
