-- This script:
-- 1 - creates a list of email addresses of participants eligible for incentives
-- 2 - updates participants with incentives so that they are timestamped as having received an incentive
-- 3 Incentive eligibility is based on:
-- - having submitted the questionnaire
-- - not having already received an incentive
-- - Submitted online questionnaire before telephone questionnaire conducted date

-- Find container name:
podman ps --format "{{.Names}}"
-- Copy partner csv file to server temp directory
podman cp "/Users/stephhousden/Downloads/SampleDataPIDRemoved230126.csv" <db_container_name>:/tmp/partner.csv

podman cp "/Users/stephhousden/Downloads/SampleDataPIDRemoved230126.csv" lung_cancer_screening-db-1:/tmp/partner.csv

-- login to psql on local container
psql -h localhost -p 5432 -U lung_cancer_screening -d lung_cancer_screening


-- Create table for partner data import

-- single line command for psql:
CREATE TABLE incentive_partner_import_raw (nhs_number TEXT, date_of_birth TEXT, date_conducted TEXT, smoking_status TEXT, average_cigarettes_per_day_while_smoking TEXT, duration_smoked_years TEXT, years_since_quitting_smoking TEXT, height_measurement_type TEXT, height_measurement_value_metric_cm TEXT, weight_measurement_type TEXT, weight_measurement_value_metric_kg TEXT, previous_respiratory_diagnosis TEXT, personal_history_of_previous_cancer TEXT, family_history_of_lung_cancer TEXT, personal_history_of_asthma TEXT, asbestos_exposure_from_job_or_activity TEXT, education TEXT, ethnicity TEXT, plco_lung_cancer_risk_score TEXT, llp_lung_cancer_risk_score TEXT, created_at TIMESTAMPTZ NOT NULL DEFAULT now());

CREATE TABLE incentive_partner_import_raw (
  nhs_number TEXT,
  date_of_birth TEXT,
  date_conducted TEXT,
  smoking_status TEXT,
  average_cigarettes_per_day_while_smoking TEXT,
  duration_smoked_years TEXT,
  years_since_quitting_smoking TEXT,
  height_measurement_type TEXT,
  height_measurement_value_metric_cm TEXT,
  weight_measurement_type TEXT,
  weight_measurement_value_metric_kg TEXT,
  previous_respiratory_diagnosis TEXT,
  personal_history_of_previous_cancer TEXT,
  family_history_of_lung_cancer TEXT,
  personal_history_of_asthma TEXT,
  asbestos_exposure_from_job_or_activity TEXT,
  education TEXT,
  ethnicity TEXT,
  plco_lung_cancer_risk_score TEXT,
  llp_lung_cancer_risk_score TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);


SELECT * FROM incentive_partner_import_raw;

-- psql command to import data from CSV file into the temp table

-- One line command for psql:
\copy incentive_partner_import_raw (nhs_number, date_of_birth, date_conducted, smoking_status, average_cigarettes_per_day_while_smoking, duration_smoked_years, years_since_quitting_smoking, height_measurement_type, height_measurement_value_metric_cm, weight_measurement_type, weight_measurement_value_metric_kg, previous_respiratory_diagnosis, personal_history_of_previous_cancer, family_history_of_lung_cancer, personal_history_of_asthma, asbestos_exposure_from_job_or_activity, education, ethnicity, plco_lung_cancer_risk_score, llp_lung_cancer_risk_score) FROM '/tmp/partner.csv' WITH (FORMAT csv, HEADER true);

\copy incentive_partner_import_raw (
  nhs_number,
  date_of_birth,
  date_conducted,
  smoking_status,
  average_cigarettes_per_day_while_smoking,
  duration_smoked_years,
  years_since_quitting_smoking,
  height_measurement_type,
  height_measurement_value_metric_cm,
  weight_measurement_type,
  weight_measurement_value_metric_kg,
  previous_respiratory_diagnosis,
  personal_history_of_previous_cancer,
  family_history_of_lung_cancer,
  personal_history_of_asthma,
  asbestos_exposure_from_job_or_activity,
  education,
  ethnicity,
  plco_lung_cancer_risk_score,
  llp_lung_cancer_risk_score
) FROM '/Users/stephhousden/Downloads/SampleDataPIDRemoved230126.csv' WITH (FORMAT csv, HEADER true);


-- Select distinct email addresses of eligible participants based on criteria outlined at the top of this file

-- One line command for psql:
SELECT qu.email FROM questions_user qu JOIN questions_responseset qrs ON qrs.user_id = qu.id JOIN incentive_partner_import_raw ipir ON ipir.nhs_number = qu.nhs_number WHERE (NULLIF(ipir.date_conducted, '')::timestamptz > qrs.submitted_at);
