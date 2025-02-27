-- Find encounters for a specific patient

select p.id as patient_id,
    p.name as patient_name,
    e.status as status,
    e.encounter_date as encounter_date
from "Patient" p
join "Encounter" e
	on p.id = e.patient_id
where p.id = '6fe61166-cccb-41b0-9484-1c614e2d27cd'