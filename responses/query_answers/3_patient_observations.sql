-- List all observations recorded for a patient

select p.id as patient_id,
    p.name as patient_name,
    o.type, o.value,
    o.unit,
    o.recorded_at
from "Patient" p
join "Observation" o
	on p.id = o.patient_id
where p.id = '6fe61166-cccb-41b0-9484-1c614e2d27cd';