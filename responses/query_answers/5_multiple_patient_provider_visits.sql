-- Find patients who have had encounters with more than one practitioner

with patient_practioner_visits as (
    -- Get list of number of times a patient has seend a provider
    -- Note count column isn't necessary
	select patient_id,
	    practitioner_id,
	    count(1) as visits
	from "Encounter" e
	group by patient_id, practitioner_id
),
distinct_practioner_visits as (
	select patient_id,
	    count(1) as distinct_visits
	from patient_practioner_visits ppv
	group by patient_id
)
-- If distinct_visits > 1 then we know the patient has seen more than one practioner
select patient_id
from distinct_practioner_visits
where distinct_visits > 1;

