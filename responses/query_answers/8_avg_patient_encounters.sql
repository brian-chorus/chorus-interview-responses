-- Find the average number of encounters per patient

-- Get number of counters per patient
with patient_encounter_count as (
	select patient_id,
	    count(1) as encounter_count
	from "Encounter"
	group by patient_id
)
-- Take average and round
select round(avg(encounter_count), 2)
from patient_encounter_count;