-- SQL script to export a csv file containing NHS numbers of valid responses to a CSV file on to AVD.
-- A valid response is defined as a response where the user has either submitted a response set or has a response to the question "Do you think you need to see a doctor about your symptoms?" with a value of "Yes".
-- Run script using psql command line tool or pgAdmin query tool

\set ON_ERROR_STOP on
\copy (SELECT DISTINCT qu.nhs_number FROM questions_user qu JOIN questions_responseset qrs ON qrs.user_id = qu.id JOIN questions_checkneedappointmentresponse qcnar ON qcnar.response_set_id = qrs.id WHERE qcnar.value = TRUE OR qrs.submitted_at IS NOT NULL) TO 'C:/Users/*YourUsername*/Documents/valid_responses.csv' WITH (FORMAT csv, HEADER true);

