-- SQL script to export a csv file containing NHS numbers of submitted responses to a folder on an AVD.
-- A valid response is defined as a response where the user has submitted the questionnaire.
-- Run script using the psql command line tool on AVD.
-- Update PATH_TO_EXPORT_FILE before running to specify the location and name of the exported file. The file will be created if it does not exist, or overwritten if it does.

\set ON_ERROR_STOP on
\copy (SELECT DISTINCT qu.nhs_number FROM questions_user qu JOIN questions_responseset qrs ON qrs.user_id = qu.id WHERE qrs.submitted_at IS NOT NULL) TO 'PATH_TO_EXPORT_FILE' WITH (FORMAT csv, HEADER true);

