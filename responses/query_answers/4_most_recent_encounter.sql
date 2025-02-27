-- Find the most recent encounter for each patient

with most_recent_visit AS (
	-- subquery to get most recent encounter by patient
	select patient_id,
	    max(encounter_date) as recent_visit
	from "Encounter" e
	group by patient_id
)
-- Join subquery on patient and recent_visit to get encounter status
-- Query assumes encounter_date is unique for each patient
select e.patient_id,
    e.encounter_date,
    e.status
from "Encounter" e
	join most_recent_visit mrv
	on e.patient_id = mrv.patient_id
	and e.encounter_date = mrv.recent_visit
;