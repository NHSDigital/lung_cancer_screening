-- SQL script to export a csv file containing NHS numbers of submitted responses to a folder on an AVD.
-- A valid response is defined as a response where the user has submitted the questionnaire.
-- Run script using the psql command line tool on AVD; this file uses psql meta-commands (\set, \copy) and will not run in pgAdmin Query Tool.

\set ON_ERROR_STOP on
\copy (SELECT DISTINCT qu.nhs_number FROM questions_user qu JOIN questions_responseset qrs ON qrs.user_id = qu.id WHERE qrs.submitted_at IS NOT NULL) TO 'C:/Users/*YourUsername*/Documents/valid_responses.csv' WITH (FORMAT csv, HEADER true);

